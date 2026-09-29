"""Tests for EBG-0143 (ESR-0059 WP8): input size limits, prompt budgets and
the optional output-token cap."""

import json

import pytest

from jarvis.guardian.cognitive_core import (
    HISTORY_ENTRY_CHAR_LIMIT,
    MEMORY_NOTES_CHAR_BUDGET,
    TRUNCATION_MARKER,
    GuardianCognitiveCore,
)
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.stdio_rpc import (
    MAX_AUDIO_BASE64_CHARS,
    MAX_MEMORY_CHARS,
    MAX_MESSAGE_CHARS,
    MAX_SPEAK_CHARS,
    StdioRpcServer,
    _max_output_tokens,
    build_default_runtime,
)
from jarvis.memory.store import PersonalMemoryRecord, utc_now
from sentinel.gemini_provider import GeminiProvider
from sentinel.ollama_provider import DEFAULT_NUM_CTX, OllamaProvider
from sentinel.openai_provider import OpenAIProvider
from sentinel.provider_config import CredentialReference, ProviderConfiguration
from sentinel.providers import ProviderRequest


def _server(tmp_path) -> StdioRpcServer:
    return StdioRpcServer(
        build_default_runtime(
            environ={
                "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
                "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            }
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def _call(server, method, params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


@pytest.mark.parametrize(
    ("method", "params"),
    [
        ("guardian.converse", {"message": "x" * (MAX_MESSAGE_CHARS + 1)}),
        ("guardian.speak", {"text": "x" * (MAX_SPEAK_CHARS + 1)}),
        ("guardian.transcribe", {"audioBase64": "A" * (MAX_AUDIO_BASE64_CHARS + 4), "mimeType": "audio/webm"}),
        ("memory.propose", {"content": "x" * (MAX_MEMORY_CHARS + 1)}),
    ],
)
def test_oversized_rpc_input_is_refused_with_a_clear_error(tmp_path, method, params):
    response = _call(_server(tmp_path), method, params)

    assert "too long" in response["error"]["message"]
    assert "the limit is" in response["error"]["message"]


def test_input_at_the_limit_is_accepted(tmp_path):
    response = _call(_server(tmp_path), "guardian.converse", {"message": "x" * MAX_MESSAGE_CHARS})

    assert "result" in response


def test_blank_memory_is_refused(tmp_path):
    response = _call(_server(tmp_path), "memory.propose", {"content": "   "})

    assert "must not be blank" in response["error"]["message"]


def test_frontend_message_limit_matches_the_backend():
    from pathlib import Path

    app = (Path(__file__).resolve().parents[2] / "src" / "App.jsx").read_text(encoding="utf-8")

    assert f"const MAX_MESSAGE_CHARS = {MAX_MESSAGE_CHARS};" in app
    assert "maxLength={MAX_MESSAGE_CHARS}" in app


def test_history_entries_are_truncated_with_a_visible_marker():
    core = GuardianCognitiveCore()
    core.record_exchange("u" * 5_000, "short reply")

    (user_message, reply), = core.history()

    assert len(user_message) == HISTORY_ENTRY_CHAR_LIMIT
    assert user_message.endswith(TRUNCATION_MARKER)
    assert reply == "short reply"


def _record(content: str) -> PersonalMemoryRecord:
    return PersonalMemoryRecord(id=content[:8], content=content, created_at=utc_now(), consent_decision_id="d")


def test_memory_notes_keep_the_newest_whole_notes_within_budget():
    oldest, middle, newest = "a" * 700, "b" * 700, "c" * 700  # 2100 > 1500 budget

    notes = GuardianCognitiveCore.memory_notes([_record(oldest), _record(middle), _record(newest)])

    assert notes == (middle, newest)  # oldest left out, order kept, nothing cut mid-note
    assert sum(len(n) for n in notes) <= MEMORY_NOTES_CHAR_BUDGET


def test_worst_case_turn_leaves_room_for_a_reply_in_ollama_context():
    """Estimate, at a conservative 3.5 characters per token: persona +
    message + full history + full memory budget + framing overhead must
    leave at least 400 tokens of Ollama's context for the reply (num_ctx
    covers prompt and output together)."""

    from jarvis.guardian.cognitive_core import DEFAULT_HISTORY_LIMIT
    from jarvis.guardian.config import GuardianRuntimeConfig

    framing_overhead = 600
    worst_chars = (
        len(GuardianRuntimeConfig().persona)
        + MAX_MESSAGE_CHARS
        + 2 * DEFAULT_HISTORY_LIMIT * HISTORY_ENTRY_CHAR_LIMIT
        + MEMORY_NOTES_CHAR_BUDGET
        + framing_overhead
    )

    assert worst_chars / 3.5 + 400 <= DEFAULT_NUM_CTX


@pytest.mark.parametrize(("raw", "expected"), [(None, None), ("", None), ("abc", None), ("0", None), ("-5", None), ("512", 512)])
def test_output_cap_parsing(raw, expected):
    environ = {} if raw is None else {"JARVIS_MAX_OUTPUT_TOKENS": raw}

    assert _max_output_tokens(environ) == expected


def test_configuration_rejects_a_non_positive_cap():
    with pytest.raises(ValueError, match="at least one"):
        ProviderConfiguration(provider_name="x", max_output_tokens=0)


def _sent_payload(provider_cls, configuration, response):
    sent = []

    def transport(url, body, headers, timeout):
        sent.append(json.loads(body))
        return json.dumps(response).encode("utf-8")

    provider_cls(configuration, transport=transport).execute(ProviderRequest(prompt="hi"))
    return sent[0]


@pytest.mark.parametrize("cap", [None, 256])
def test_output_cap_reaches_each_provider_only_when_set(monkeypatch, cap):
    monkeypatch.setenv("TEST_KEY_WP8", "k")
    credential = CredentialReference(environment_variable="TEST_KEY_WP8")

    openai = _sent_payload(
        OpenAIProvider,
        ProviderConfiguration(provider_name="openai", default_model="m", credential=credential, max_output_tokens=cap),
        {"choices": [{"message": {"content": "ok"}}]},
    )
    gemini = _sent_payload(
        GeminiProvider,
        ProviderConfiguration(provider_name="gemini", default_model="m", credential=credential, max_output_tokens=cap),
        {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]},
    )
    ollama = _sent_payload(
        OllamaProvider,
        ProviderConfiguration(provider_name="ollama", default_model="m", max_output_tokens=cap),
        {"response": "ok"},
    )

    if cap is None:
        assert "max_completion_tokens" not in openai and "max_tokens" not in openai
        assert "generationConfig" not in gemini
        assert "num_predict" not in ollama["options"]
    else:
        assert openai["max_completion_tokens"] == cap
        assert "max_tokens" not in openai  # rejected by the gpt-5 family
        assert gemini["generationConfig"] == {"maxOutputTokens": cap}
        assert ollama["options"]["num_predict"] == cap
