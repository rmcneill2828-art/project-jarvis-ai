"""Tests for the Anthropic Claude provider adapter (ESR-0061 WP3a, EIP-ESR0061-003)."""

import json
import time
import urllib.error

import pytest

from sentinel.anthropic_provider import ANTHROPIC_VERSION, DEFAULT_MAX_TOKENS, AnthropicProvider
from sentinel.gemini_provider import GeminiProvider
from sentinel.ollama_provider import OllamaProvider
from sentinel.openai_provider import OpenAIProvider
from sentinel.provider_config import CredentialReference, ProviderConfiguration
from sentinel.providers import (
    TRANSIENT_HTTP_STATUSES,
    ConversationTurn,
    DeadlineExceededError,
    ProviderDeclinedError,
    ProviderError,
    ProviderRequest,
    is_timeout,
    remaining_timeout,
    remaining_timeout_budget,
)

KEY_VARIABLE = "TEST_ANTHROPIC_API_KEY"


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "anthropic",
        "default_model": "claude-sonnet-5-5",
        "credential": CredentialReference(environment_variable=KEY_VARIABLE),
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def _reply(text: str = "hello back", **extra) -> bytes:
    body = {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-5-5",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 12, "output_tokens": 34, "cache_read_input_tokens": 0},
    }
    body.update(extra)
    return json.dumps(body).encode("utf-8")


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://example.invalid", code, "x", {}, None)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _key(monkeypatch):
    monkeypatch.setenv(KEY_VARIABLE, "test-anthropic-key-not-real")


def test_requires_a_credential_reference_and_a_model():
    with pytest.raises(ValueError):
        AnthropicProvider(ProviderConfiguration(provider_name="anthropic", default_model="claude-sonnet-5-5"))
    with pytest.raises(ValueError):
        AnthropicProvider(_configuration(default_model=None))


def test_rejects_an_unknown_effort_level():
    with pytest.raises(ValueError):
        AnthropicProvider(_configuration(), effort="turbo")


@pytest.mark.parametrize("value", [None, "", "   "])
def test_a_missing_or_blank_key_is_an_error_that_does_not_call_out(monkeypatch, value):
    if value is None:
        monkeypatch.delenv(KEY_VARIABLE)
    else:
        monkeypatch.setenv(KEY_VARIABLE, value)
    calls = []
    provider = AnthropicProvider(_configuration(), transport=lambda *a: calls.append(a) or b"{}")

    with pytest.raises(RuntimeError, match="not found in environment variable"):
        provider.execute(ProviderRequest(prompt="hello"))

    assert calls == []


def test_request_shape_and_successful_reply():
    captured: dict[str, object] = {}

    def transport(url, body, headers, timeout):
        captured.update(url=url, body=json.loads(body), headers=headers, timeout=timeout)
        return _reply()

    provider = AnthropicProvider(_configuration(timeout_seconds=12.5), transport=transport)
    response = provider.execute(ProviderRequest(prompt="hello", system_prompt="You are Guardian."))

    assert response.content == "hello back"
    assert response.provider_name == "anthropic"
    assert captured["url"] == "https://api.anthropic.com/v1/messages"
    assert captured["timeout"] == 12.5
    assert captured["headers"]["x-api-key"] == "test-anthropic-key-not-real"
    assert captured["headers"]["anthropic-version"] == ANTHROPIC_VERSION
    body = captured["body"]
    assert body["model"] == "claude-sonnet-5-5"
    assert body["max_tokens"] == DEFAULT_MAX_TOKENS
    assert body["system"] == "You are Guardian."
    assert body["messages"] == [{"role": "user", "content": "hello"}]
    assert body["output_config"] == {"effort": "low"}


def test_never_sends_parameters_the_default_model_rejects():
    captured: dict[str, object] = {}
    provider = AnthropicProvider(
        _configuration(), transport=lambda url, body, h, t: captured.setdefault("body", json.loads(body)) and _reply()
    )
    provider.execute(ProviderRequest(prompt="hello", history=(ConversationTurn("user", "a"), ConversationTurn("assistant", "b"))))

    body = captured["body"]
    for forbidden in ("temperature", "top_p", "top_k", "thinking", "tool_choice", "budget_tokens"):
        assert forbidden not in body
    # The last message is the user's: assistant prefill is rejected by the API.
    assert body["messages"][-1]["role"] == "user"


def test_history_goes_in_its_own_roles_and_notes_inside_the_user_message():
    captured: dict[str, object] = {}
    provider = AnthropicProvider(
        _configuration(), transport=lambda url, body, h, t: captured.setdefault("body", json.loads(body)) and _reply()
    )
    provider.execute(
        ProviderRequest(
            prompt="what next?",
            history=(ConversationTurn("user", "hi"), ConversationTurn("assistant", "hello")),
            context_notes=("likes tea",),
        )
    )

    messages = captured["body"]["messages"]
    assert messages[0] == {"role": "user", "content": "hi"}
    assert messages[1] == {"role": "assistant", "content": "hello"}
    assert "likes tea" in messages[2]["content"] and "what next?" in messages[2]["content"]
    assert "system" not in captured["body"]


def test_max_output_tokens_and_effort_are_configurable():
    captured: dict[str, object] = {}
    provider = AnthropicProvider(
        _configuration(max_output_tokens=300),
        transport=lambda url, body, h, t: captured.setdefault("body", json.loads(body)) and _reply(),
        effort="medium",
    )
    provider.execute(ProviderRequest(prompt="hello"))

    assert captured["body"]["max_tokens"] == 300 == provider.max_tokens
    assert captured["body"]["output_config"] == {"effort": "medium"}


def test_only_text_blocks_are_the_answer_and_usage_is_passed_on_as_strings():
    blocks = [
        {"type": "thinking", "thinking": "", "signature": "x"},
        {"type": "text", "text": "Part one. "},
        {"type": "text", "text": "Part two."},
    ]
    provider = AnthropicProvider(_configuration(), transport=lambda *a: _reply(content=blocks))
    response = provider.execute(ProviderRequest(prompt="hello"))

    assert response.content == "Part one. Part two."
    assert response.metadata["model"] == "claude-sonnet-5-5"
    assert response.metadata["stop_reason"] == "end_turn"
    assert response.metadata["usage_input_tokens"] == "12"
    assert response.metadata["usage_output_tokens"] == "34"
    assert all(isinstance(value, str) for value in response.metadata.values())


@pytest.mark.parametrize(
    "raw",
    [b"not json", b"[]", b'{"content": "text"}', _reply(content=[]), _reply(content=[{"type": "thinking", "thinking": ""}])],
)
def test_malformed_or_empty_replies_are_runtime_errors(raw):
    provider = AnthropicProvider(_configuration(), transport=lambda *a: raw)

    with pytest.raises(RuntimeError, match="Unexpected Anthropic response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_a_tool_use_reply_is_refused():
    provider = AnthropicProvider(_configuration(), transport=lambda *a: _reply(stop_reason="tool_use"))

    with pytest.raises(RuntimeError, match="unsupported tool-use"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_a_refusal_is_a_decline_not_a_provider_error():
    raw = _reply(stop_reason="refusal", stop_details={"type": "refusal", "category": "cyber", "explanation": "secret text"})
    provider = AnthropicProvider(_configuration(), transport=lambda *a: raw)

    with pytest.raises(ProviderDeclinedError) as caught:
        provider.execute(ProviderRequest(prompt="hello"))

    assert not isinstance(caught.value, ProviderError)
    assert "cyber" in str(caught.value)
    assert "secret text" not in str(caught.value)


@pytest.mark.parametrize("status", sorted(TRANSIENT_HTTP_STATUSES))
def test_transient_statuses_are_marked_transient(status):
    def transport(*args):
        raise _http_error(status)

    with pytest.raises(ProviderError) as caught:
        AnthropicProvider(_configuration(), transport=transport).execute(ProviderRequest(prompt="hello"))

    assert caught.value.transient is True
    assert f"status {status}" in str(caught.value)


def test_overload_529_is_transient():
    assert 529 in TRANSIENT_HTTP_STATUSES


@pytest.mark.parametrize("status", [400, 401, 402, 403, 404, 413])
def test_other_statuses_are_permanent(status):
    def transport(*args):
        raise _http_error(status)

    with pytest.raises(ProviderError) as caught:
        AnthropicProvider(_configuration(), transport=transport).execute(ProviderRequest(prompt="hello"))

    assert caught.value.transient is False


def test_errors_never_contain_the_key_or_the_exception_text():
    def transport(*args):
        raise ConnectionError("secret detail test-anthropic-key-not-real")

    with pytest.raises(ProviderError) as caught:
        AnthropicProvider(_configuration(), transport=transport).execute(ProviderRequest(prompt="hello"))

    assert "test-anthropic-key-not-real" not in str(caught.value)
    assert "secret detail" not in str(caught.value)
    assert "ConnectionError" in str(caught.value)
    assert caught.value.transient is True


# --- Deadline-capped timeouts (EBG-0157 item 6), all four text adapters -----------------------------------------


def _openai(transport):
    return OpenAIProvider(
        ProviderConfiguration(
            provider_name="openai",
            default_model="gpt-test",
            credential=CredentialReference(environment_variable=KEY_VARIABLE),
        ),
        transport=transport,
    )


def _gemini(transport):
    return GeminiProvider(
        ProviderConfiguration(
            provider_name="gemini",
            default_model="gemini-test",
            credential=CredentialReference(environment_variable=KEY_VARIABLE),
        ),
        transport=transport,
    )


def _ollama(transport):
    return OllamaProvider(ProviderConfiguration(provider_name="ollama", default_model="m"), transport=transport)


def _anthropic(transport):
    return AnthropicProvider(_configuration(), transport=transport)


ADAPTERS = [_openai, _gemini, _ollama, _anthropic]
TIMEOUTS = [TimeoutError("timed out"), TimeoutError("timed out"), urllib.error.URLError(TimeoutError("timed out"))]


@pytest.mark.parametrize("build", ADAPTERS)
@pytest.mark.parametrize("timeout_error", TIMEOUTS)
def test_a_timeout_the_deadline_caused_is_not_a_provider_fault(build, timeout_error):
    def transport(*args):
        raise timeout_error

    request = ProviderRequest(prompt="hello", deadline=time.monotonic() + 5.0)  # well under the 30-120 s defaults

    with pytest.raises(DeadlineExceededError):
        build(transport).execute(request)


@pytest.mark.parametrize("build", ADAPTERS)
def test_a_timeout_the_providers_own_limit_caused_is_still_a_transient_fault(build):
    def transport(*args):
        raise TimeoutError("timed out")

    request = ProviderRequest(prompt="hello", deadline=time.monotonic() + 100_000.0)  # deadline is not what applied

    with pytest.raises(ProviderError) as caught:
        build(transport).execute(request)

    assert caught.value.transient is True


@pytest.mark.parametrize("build", ADAPTERS)
def test_a_timeout_with_no_deadline_is_a_transient_fault(build):
    def transport(*args):
        raise TimeoutError("timed out")

    with pytest.raises(ProviderError) as caught:
        build(transport).execute(ProviderRequest(prompt="hello"))

    assert caught.value.transient is True


@pytest.mark.parametrize("build", ADAPTERS)
def test_a_non_timeout_failure_under_a_deadline_is_still_a_fault(build):
    def transport(*args):
        raise ConnectionError("refused")

    with pytest.raises(ProviderError):
        build(transport).execute(ProviderRequest(prompt="hello", deadline=time.monotonic() + 5.0))


def test_remaining_timeout_budget_reports_whether_the_deadline_shortened_it():
    assert remaining_timeout_budget(30.0, ProviderRequest(prompt="x")) == (30.0, False)

    seconds, capped = remaining_timeout_budget(30.0, ProviderRequest(prompt="x", deadline=time.monotonic() + 5.0))
    assert capped is True and 0 < seconds <= 5.0

    seconds, capped = remaining_timeout_budget(30.0, ProviderRequest(prompt="x", deadline=time.monotonic() + 500.0))
    assert (seconds, capped) == (30.0, False)

    with pytest.raises(DeadlineExceededError):
        remaining_timeout_budget(30.0, ProviderRequest(prompt="x", deadline=time.monotonic() - 1.0))


def test_remaining_timeout_still_returns_just_the_number():
    assert remaining_timeout(30.0, ProviderRequest(prompt="x")) == 30.0


def test_is_timeout_recognises_each_way_urllib_reports_one():
    assert is_timeout(TimeoutError()) and is_timeout(TimeoutError())
    assert is_timeout(urllib.error.URLError(TimeoutError()))
    assert not is_timeout(urllib.error.URLError(ConnectionRefusedError()))
    assert not is_timeout(ConnectionError())
    assert not is_timeout(_http_error(504))
