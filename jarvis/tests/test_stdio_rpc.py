"""Tests for the JSON-RPC 2.0 stdio bridge (ESR-0017 WP9)."""

import base64
import io
import json
import threading
import time
from datetime import UTC, datetime
from unittest.mock import patch

from jarvis.gia.observability import GiaSnapshot
from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.stdio_rpc import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    PARSE_ERROR,
    StdioRpcServer,
    build_default_runtime,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest
from sentinel.policy import TrustCategory, TrustTier, TrustTierPolicy
from sentinel.speech_providers import SpeechSynthesisResponse
from sentinel.transcription_providers import TranscriptionResponse


class _FakeKokoroProvider:
    """Stands in for a real `KokoroProvider` without ever loading a model or
    importing `kokoro_onnx` - `jarvis.interfaces.stdio_rpc.KokoroProvider` is
    patched to return this, so wiring tests exercise real branching logic
    (env var present/absent, gateway reuse, RPC serialization) without the
    ML dependency cost a real construction would pay."""

    name = "kokoro"

    def __init__(self, configuration) -> None:
        self.configuration = configuration

    def synthesize(self, request):
        return SpeechSynthesisResponse(
            provider_name="kokoro",
            audio_bytes=b"fake-wav-bytes",
            mime_type="audio/wav",
        )


class _FakeWhisperProvider:
    """Stands in for a real `WhisperProvider` without ever loading a model or
    importing `faster_whisper` - `jarvis.interfaces.stdio_rpc.WhisperProvider`
    is patched to return this, mirroring `_FakeKokoroProvider`'s pattern
    exactly for the opposite data direction."""

    name = "whisper"

    def __init__(self, configuration) -> None:
        self.configuration = configuration

    def transcribe(self, request):
        return TranscriptionResponse(provider_name="whisper", text="fake transcript")


def _server(tmp_path) -> StdioRpcServer:
    # Explicit empty environ: keeps tests deterministic and offline regardless
    # of real provider credentials the host machine may have set persistently
    # (e.g. for the manual smoke-test scripts) - never depend on, or
    # accidentally exercise, real credentials in the automated suite.
    #
    # Ollama (EBG-0075) needs no credential, so it is always in the route -
    # on a machine actually running Ollama (as this one is), a real transport
    # would make a genuine, non-deterministic network call during automated
    # tests. Pointing JARVIS_OLLAMA_ENDPOINT at a reserved, never-listening
    # port forces a fast connection failure, exercising the same real
    # exception-driven failover to local-echo the suite already relies on,
    # without depending on whether Ollama happens to be running locally.
    #
    # JARVIS_MEMORY_DB_PATH (EBG-0080) is pointed at a pytest tmp_path for the
    # same reason - without this, every test in this file would create and
    # write to the real ~/.jarvis/memory/personal.db on whatever machine runs
    # the suite, the exact test-isolation defect class ESR-0026 WP1 found for
    # Ollama's network endpoint, just for a local file instead.
    #
    # identity_service (EIP-ESR0046-001) is passed explicitly for the same
    # reason - it is decoupled from build_default_runtime()/environ (mirroring
    # the GIA precedent), so without an explicit override here every test in
    # this file would otherwise touch the real ~/.jarvis/identity/profiles.db.
    return StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def test_build_default_runtime_is_started_and_connected(tmp_path):
    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })

    assert runtime.status().value == "Running"
    assert runtime.services()["Guardian Provider Boundary"].status.value == "Online"


def test_build_default_runtime_falls_back_to_local_echo_without_credential(tmp_path):
    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })

    # Ollama (EBG-0075) is registered unconditionally - no credential gate -
    # positioned between the (absent) primary cloud provider and local-echo.
    assert runtime.configured_providers() == ("ollama", "local-echo")


def test_build_default_runtime_wires_openai_as_default_primary_when_credential_present(tmp_path):
    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), "OPENAI_API_KEY": "test-key-not-a-real-credential"})

    assert runtime.configured_providers() == ("openai", "ollama", "local-echo")


def test_build_default_runtime_respects_primary_provider_selection(tmp_path):
    runtime = build_default_runtime(
        environ={
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            "JARVIS_PRIMARY_PROVIDER": "gemini",
            "GEMINI_API_KEY": "test-key-not-a-real-credential",
        }
    )

    assert runtime.configured_providers() == ("gemini", "ollama", "local-echo")


def test_build_default_runtime_ignores_unselected_provider_credential(tmp_path):
    # OPENAI_API_KEY being set should not matter when gemini is selected but
    # has no credential of its own - ollama and local-echo remain the fallback.
    runtime = build_default_runtime(
        environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), "JARVIS_PRIMARY_PROVIDER": "gemini", "OPENAI_API_KEY": "test-key-not-a-real-credential"}
    )

    assert runtime.configured_providers() == ("ollama", "local-echo")


def test_build_default_runtime_falls_through_to_default_model_when_env_var_is_blank(tmp_path):
    # A present-but-blank OPENAI_MODEL must not override the fallback default
    # with an empty string - that would make OpenAIProvider's constructor
    # reject the configuration, turning a harmless placeholder into a startup
    # failure (Engineering Reviewer finding, EIP-ESR0022-001).
    runtime = build_default_runtime(
        environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), "OPENAI_API_KEY": "test-key-not-a-real-credential", "OPENAI_MODEL": ""}
    )

    assert runtime.configured_providers() == ("openai", "ollama", "local-echo")


def test_build_default_runtime_wires_trust_tier_policy_as_the_production_policy_engine(tmp_path):
    """EBG-0074 (ESR-0024): build_default_runtime()'s gateway must actually run
    TrustTierPolicy, not merely have the class available in the codebase.
    Asserted directly against the object build_default_runtime() itself
    produces - not a separately constructed gateway - so this proves the real
    wiring, not just that TrustTierPolicy is importable."""

    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })

    assert isinstance(runtime.sentinel_gateway().policy_engine, TrustTierPolicy)


def test_build_default_runtime_leaves_speech_unavailable_without_kokoro_paths(tmp_path):
    """EBG-0125: an absent JARVIS_KOKORO_MODEL_PATH/JARVIS_KOKORO_VOICES_PATH
    must mean speak() returns the honest not_connected outcome, mirroring an
    absent provider credential - never a startup failure and never a
    fabricated result."""

    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })

    outcome = runtime.speak("hello")

    assert outcome.status == "not_connected"
    assert outcome.audio is None


def test_build_default_runtime_leaves_speech_unavailable_with_only_one_kokoro_path(tmp_path):
    """EBG-0125: Kokoro requires both files - a present model path with a
    missing/blank voices path (or vice versa) must still degrade honestly,
    not attempt a construction that would fail."""

    runtime = build_default_runtime(
        environ={
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            "JARVIS_KOKORO_MODEL_PATH": "/fake/voices/kokoro-v1.0.onnx",
        }
    )

    outcome = runtime.speak("hello")

    assert outcome.status == "not_connected"


def test_build_default_runtime_wires_speech_provider_when_kokoro_paths_present(tmp_path):
    """EBG-0125: present JARVIS_KOKORO_MODEL_PATH/JARVIS_KOKORO_VOICES_PATH
    must wire a real, reachable speech provider into the runtime
    build_default_runtime() actually produces - not merely that
    KokoroProvider is importable."""

    with patch("jarvis.interfaces.stdio_rpc.KokoroProvider", _FakeKokoroProvider):
        runtime = build_default_runtime(
            environ={
                "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                "JARVIS_KOKORO_MODEL_PATH": "/fake/voices/kokoro-v1.0.onnx",
                "JARVIS_KOKORO_VOICES_PATH": "/fake/voices/voices-v1.0.bin",
            }
        )

    outcome = runtime.speak("hello")

    assert outcome.status == "synthesized"
    assert outcome.audio.audio_bytes == b"fake-wav-bytes"


def test_build_default_runtime_reuses_the_same_gateway_for_speech_and_conversation(tmp_path):
    """EBG-0114/EBG-0125: speech must share build_default_runtime()'s single
    SentinelTrustGateway instance, not construct a second one - one trust
    boundary and audit trail, matching how memory_service already reuses it."""

    with patch("jarvis.interfaces.stdio_rpc.KokoroProvider", _FakeKokoroProvider):
        runtime = build_default_runtime(
            environ={
                "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                "JARVIS_KOKORO_MODEL_PATH": "/fake/voices/kokoro-v1.0.onnx",
                "JARVIS_KOKORO_VOICES_PATH": "/fake/voices/voices-v1.0.bin",
            }
        )

    speech_gateway = runtime._speech_provider.gateway
    assert speech_gateway is runtime.sentinel_gateway()


def test_build_default_runtime_reuses_the_same_gateway_for_agent_service(tmp_path):
    """EIP-ESR0049-001: the agent service must share build_default_runtime()'s
    single SentinelTrustGateway instance too, not construct a second one -
    matching the same shared-gateway requirement already enforced for
    speech/transcription/memory."""

    runtime = build_default_runtime(
        environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
    )

    assert runtime._agent_service.gateway is runtime.sentinel_gateway()
    assert runtime.available_agents() == ("gia-observability",)


def test_guardian_speak_rpc_returns_synthesized_shape(tmp_path):
    with patch("jarvis.interfaces.stdio_rpc.KokoroProvider", _FakeKokoroProvider):
        server = StdioRpcServer(
            build_default_runtime(
                environ={
                    "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
                    "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                    "JARVIS_KOKORO_MODEL_PATH": "/fake/voices/kokoro-v1.0.onnx",
                    "JARVIS_KOKORO_VOICES_PATH": "/fake/voices/voices-v1.0.bin",
                }
            ),
            identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
        )

    result = server._methods["guardian.speak"]({"text": "hello"})

    assert result["status"] == "synthesized"
    assert base64.b64decode(result["audio"]) == b"fake-wav-bytes"
    assert result["mimeType"] == "audio/wav"


def test_guardian_speak_rpc_returns_not_connected_shape_without_audio(tmp_path):
    server = _server(tmp_path)

    result = server._methods["guardian.speak"]({"text": "hello"})

    assert result["status"] == "not_connected"
    assert "audio" not in result
    assert "mimeType" not in result


def test_guardian_speak_rpc_rejects_non_string_text(tmp_path):
    server = _server(tmp_path)

    try:
        server._methods["guardian.speak"]({"text": 123})
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for non-string params.text")


def test_build_default_runtime_leaves_transcription_unavailable_without_whisper_path(tmp_path):
    """EIP-ESR0047-001: an absent JARVIS_WHISPER_MODEL_PATH must mean
    transcribe() returns the honest not_connected outcome, mirroring an
    absent Kokoro voice path - never a startup failure and never a
    fabricated result."""

    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == "not_connected"
    assert outcome.text is None


def test_build_default_runtime_wires_transcription_provider_when_whisper_path_present(tmp_path):
    """EIP-ESR0047-001: a present JARVIS_WHISPER_MODEL_PATH must wire a real,
    reachable transcription provider into the runtime build_default_runtime()
    actually produces - not merely that WhisperProvider is importable."""

    with patch("jarvis.interfaces.stdio_rpc.WhisperProvider", _FakeWhisperProvider):
        runtime = build_default_runtime(
            environ={
                "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                "JARVIS_WHISPER_MODEL_PATH": "base.en",
            }
        )

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == "transcribed"
    assert outcome.text == "fake transcript"


def test_build_default_runtime_reuses_the_same_gateway_for_transcription_and_conversation(tmp_path):
    """EIP-ESR0047-001: transcription must share build_default_runtime()'s
    single SentinelTrustGateway instance, not construct a second one - one
    trust boundary and audit trail, matching speech/memory's own reuse."""

    with patch("jarvis.interfaces.stdio_rpc.WhisperProvider", _FakeWhisperProvider):
        runtime = build_default_runtime(
            environ={
                "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                "JARVIS_WHISPER_MODEL_PATH": "base.en",
            }
        )

    transcription_gateway = runtime._transcription_provider.gateway
    assert transcription_gateway is runtime.sentinel_gateway()


def test_platform_status_reports_transcription_available_when_whisper_path_present(tmp_path):
    """Engineering Reviewer WP6 finding: the frontend must be able to learn
    transcription availability *before* offering the microphone button at
    all, not only after a failed attempt - unlike speech output, activating
    a microphone is itself privacy-relevant (EIP-ESR0047-001 Section 5.2)."""

    with patch("jarvis.interfaces.stdio_rpc.WhisperProvider", _FakeWhisperProvider):
        server = StdioRpcServer(
            build_default_runtime(
                environ={
                    "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
                    "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                    "JARVIS_WHISPER_MODEL_PATH": "base.en",
                }
            ),
            identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
        )

    result = server._methods["platform.status"]({})

    assert result["transcriptionAvailable"] is True


def test_guardian_transcribe_rpc_returns_transcribed_shape(tmp_path):
    with patch("jarvis.interfaces.stdio_rpc.WhisperProvider", _FakeWhisperProvider):
        server = StdioRpcServer(
            build_default_runtime(
                environ={
                    "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
                    "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
                    "JARVIS_WHISPER_MODEL_PATH": "base.en",
                }
            ),
            identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
        )

    audio_base64 = base64.b64encode(b"fake-audio").decode("ascii")
    result = server._methods["guardian.transcribe"](
        {"audioBase64": audio_base64, "mimeType": "audio/webm"}
    )

    assert result["status"] == "transcribed"
    assert result["text"] == "fake transcript"


def test_guardian_transcribe_rpc_returns_not_connected_shape_without_text(tmp_path):
    server = _server(tmp_path)

    audio_base64 = base64.b64encode(b"fake-audio").decode("ascii")
    result = server._methods["guardian.transcribe"](
        {"audioBase64": audio_base64, "mimeType": "audio/webm"}
    )

    assert result["status"] == "not_connected"
    assert result["text"] is None


def test_guardian_transcribe_rpc_rejects_non_string_audio_base64(tmp_path):
    server = _server(tmp_path)

    try:
        server._methods["guardian.transcribe"]({"audioBase64": 123, "mimeType": "audio/webm"})
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for non-string params.audioBase64")


def test_guardian_transcribe_rpc_rejects_non_string_mime_type(tmp_path):
    server = _server(tmp_path)
    audio_base64 = base64.b64encode(b"fake-audio").decode("ascii")

    try:
        server._methods["guardian.transcribe"]({"audioBase64": audio_base64, "mimeType": 123})
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for non-string params.mimeType")


def test_guardian_transcribe_rpc_rejects_invalid_base64(tmp_path):
    server = _server(tmp_path)

    try:
        server._methods["guardian.transcribe"](
            {"audioBase64": "not-valid-base64!!!", "mimeType": "audio/webm"}
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid params.audioBase64")


def test_guardian_agent_list_rpc_includes_gia_observability(tmp_path):
    server = _server(tmp_path)

    result = server._methods["guardian.agent.list"]({})

    assert result["agents"] == ["gia-observability"]


def test_guardian_agent_invoke_rpc_returns_real_gia_snapshot(tmp_path):
    server = _server(tmp_path)

    result = server._methods["guardian.agent.invoke"](
        {"agent": "gia-observability", "task": "snapshot"}
    )

    assert result["status"] == "reported"
    assert "cpuPercent" in result["payload"]
    assert "capturedAt" in result["payload"]


def test_guardian_agent_invoke_rpc_unknown_agent_returns_unknown_agent_shape(tmp_path):
    server = _server(tmp_path)

    result = server._methods["guardian.agent.invoke"]({"agent": "does-not-exist", "task": "snapshot"})

    assert result["status"] == "unknown_agent"
    assert "payload" not in result


def test_guardian_agent_invoke_rpc_rejects_non_string_agent(tmp_path):
    server = _server(tmp_path)

    try:
        server._methods["guardian.agent.invoke"]({"agent": 123, "task": "snapshot"})
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for non-string params.agent")


def test_guardian_agent_invoke_rpc_rejects_non_string_task(tmp_path):
    server = _server(tmp_path)

    try:
        server._methods["guardian.agent.invoke"]({"agent": "gia-observability", "task": 123})
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for non-string params.task")


def test_guardian_converse_request_shape_classified_routine_under_trust_tier_policy(tmp_path):
    """Regression, beyond re-asserting the unchanged RPC response: confirms
    *why* it is unchanged - the real conversation request shape
    (SentinelGatedConversationProvider.generate()'s fixed
    metadata={"capability": "text-generation"}, default payload_type,
    requires_approval=False) is classified TrustCategory.ROUTINE_INTERACTION /
    TrustTier.ROUTINE -> ALLOW by the production-wired TrustTierPolicy itself,
    evaluated through build_default_runtime()'s own gateway - not a separately
    constructed policy instance, and not the category-matrix already covered
    by jarvis/tests/test_sentinel_policy.py."""

    runtime = build_default_runtime(environ={"JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"), })
    conversation_shaped_request = SentinelRequest(
        source="jarvis.conversation",
        intent="conversation.generate",
        metadata={"capability": "text-generation"},
    )

    decision = runtime.sentinel_gateway().evaluate(conversation_shaped_request).decision

    assert decision.outcome is SentinelDecisionOutcome.ALLOW
    assert decision.requires_human_approval is False

    policy_decision = runtime.sentinel_gateway().policy_engine.evaluate(conversation_shaped_request)
    assert policy_decision.trust_tier is TrustTier.ROUTINE
    assert policy_decision.category is TrustCategory.ROUTINE_INTERACTION


def test_guardian_converse_returns_real_response_through_sentinel(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.converse", "params": {"message": "hello"}})
    )

    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"message": "local-echo: hello", "provider": "local-echo"},
    }


def test_platform_status_reflects_real_runtime_state(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "platform.status", "params": {}}))

    assert response["result"] == {
        "state": "Running",
        "runtimeHealth": "Healthy",
        "providerConnected": "Online",
        "memoryConnected": "Online",
        "transcriptionAvailable": False,
        "providers": ["ollama", "local-echo"],
        "policyEngine": "TrustTierPolicy",
    }


def test_platform_status_policy_engine_is_none_without_a_connected_gateway(tmp_path):
    """EIP-ESR0024-002: policyEngine must degrade honestly (None), not raise,
    when no conversation provider - and therefore no Sentinel gateway - is
    connected. build_default_runtime() always wires one, so this exercises
    the defensive branch directly via a bare GuardianRuntime instead."""

    server = StdioRpcServer(
        GuardianRuntime(), identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db"))
    )

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "platform.status", "params": {}}))

    assert response["result"]["policyEngine"] is None
    assert response["result"]["memoryConnected"] == "Unavailable"


def test_knowledge_graph_returns_real_repository_data(tmp_path):
    """EBG-0055 Phase 1 (ESR-0019 WP2): dispatch-level check that the method
    is wired and returns real data, not the full parser behaviour matrix
    (already covered by jarvis/tests/test_knowledge_graph.py)."""

    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 6, "method": "knowledge.graph", "params": {}})
    )

    assert "error" not in response
    node_ids = {node["id"] for node in response["result"]["nodes"]}
    assert "README.md" in node_ids
    assert len(response["result"]["edges"]) > 0


def _fake_gia_observer(snapshot: GiaSnapshot):
    class _FakeObserver:
        def snapshot(self) -> GiaSnapshot:
            return snapshot

    return _FakeObserver()


def test_gia_status_serializes_an_injected_fake_snapshot_to_exact_camel_case(tmp_path):
    """EBG-0083 Phase 1a (EIP-ESR0029-002 Section 4.6/5.5): the RPC
    serialization/shape path must be proven against a deterministic fake
    snapshot, not real host state - an Engineering Reviewer finding on the
    first implementation attempt, which called the real psutil-backed
    observer here instead. Deliberately not routed through GuardianRuntime -
    constructing a bare StdioRpcServer(GuardianRuntime(), ...) still resolves
    gia.status, confirmed by the companion test below."""

    captured_at = datetime(2026, 7, 19, 10, 0, 0, tzinfo=UTC)
    fake_snapshot = GiaSnapshot(
        cpu_percent=12.5,
        memory_percent=64.0,
        memory_used_mb=2048.0,
        memory_total_mb=4096.0,
        disk_percent=28.7,
        disk_used_gb=430.5,
        disk_total_gb=1500.3,
        process_status="running",
        process_uptime_seconds=120.5,
        process_cpu_percent=3.2,
        process_memory_mb=64.0,
        engineering_tools_running={"vscode": True, "obsidian": False, "githubDesktop": False, "chatgpt": True},
        captured_at=captured_at,
    )
    server = StdioRpcServer(
        build_default_runtime(),
        gia_observer=_fake_gia_observer(fake_snapshot),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 7, "method": "gia.status", "params": {}}))

    assert response["result"] == {
        "cpuPercent": 12.5,
        "memoryPercent": 64.0,
        "memoryUsedMb": 2048.0,
        "memoryTotalMb": 4096.0,
        "diskPercent": 28.7,
        "diskUsedGb": 430.5,
        "diskTotalGb": 1500.3,
        "processStatus": "running",
        "processUptimeSeconds": 120.5,
        "processCpuPercent": 3.2,
        "processMemoryMb": 64.0,
        "engineeringToolsRunning": {"vscode": True, "obsidian": False, "githubDesktop": False, "chatgpt": True},
        "capturedAt": "2026-07-19T10:00:00+00:00",
    }


def test_gia_status_does_not_require_a_started_or_connected_runtime(tmp_path):
    """gia.status's own handler has no dependency on GuardianRuntime's
    lifecycle or any conversation/memory boundary - a bare, unstarted
    GuardianRuntime still resolves it (method-level decoupling; see
    EIP-ESR0029-002 Section 4.3 for the disclosed process-level limitation
    this does not claim to fix). Uses an injected fake observer, not real
    host state, for the same determinism reason as the test above."""

    fake_snapshot = GiaSnapshot(
        cpu_percent=1.0,
        memory_percent=2.0,
        memory_used_mb=3.0,
        memory_total_mb=4.0,
        disk_percent=5.0,
        disk_used_gb=6.0,
        disk_total_gb=7.0,
        process_status="running",
        process_uptime_seconds=8.0,
        process_cpu_percent=9.0,
        process_memory_mb=10.0,
        engineering_tools_running={"vscode": True, "obsidian": False, "githubDesktop": False, "chatgpt": False},
        captured_at=datetime(2026, 7, 19, 10, 0, 0, tzinfo=UTC),
    )
    server = StdioRpcServer(
        GuardianRuntime(),
        gia_observer=_fake_gia_observer(fake_snapshot),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 8, "method": "gia.status", "params": {}}))

    assert "error" not in response
    assert response["result"]["cpuPercent"] == 1.0


def test_gia_status_defaults_to_the_real_psutil_backed_observer(tmp_path):
    """Supplementary sanity check that the default (no injection) wiring
    genuinely uses the real host, not asserted-away by the deterministic
    tests above - matching the live-verification requirement in
    EIP-ESR0029-002 Section 9/10, which this test alone does not replace."""

    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 9, "method": "gia.status", "params": {}}))

    assert "error" not in response
    result = response["result"]
    assert 0.0 <= result["cpuPercent"] <= 100.0
    assert 0.0 <= result["memoryPercent"] <= 100.0
    assert result["memoryTotalMb"] >= result["memoryUsedMb"] > 0
    assert 0.0 <= result["diskPercent"] <= 100.0
    assert result["diskTotalGb"] >= result["diskUsedGb"] > 0
    assert result["processStatus"]
    assert result["processUptimeSeconds"] >= 0
    assert result["processCpuPercent"] >= 0.0
    assert result["processMemoryMb"] > 0
    assert set(result["engineeringToolsRunning"]) == {"vscode", "obsidian", "githubDesktop", "chatgpt"}
    assert all(isinstance(value, bool) for value in result["engineeringToolsRunning"].values())


def test_missing_params_defaults_to_empty_object(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "platform.status"}))

    assert "error" not in response
    assert response["result"]["state"] == "Running"


def test_malformed_json_returns_parse_error(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line("not valid json{{{")

    assert response["error"]["code"] == PARSE_ERROR
    assert response["id"] is None


def test_missing_jsonrpc_version_returns_invalid_request(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"id": 4, "method": "platform.status", "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST
    assert response["id"] == 4


def test_wrong_jsonrpc_version_returns_invalid_request(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "1.0", "id": 5, "method": "platform.status", "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST


def test_non_object_request_returns_invalid_request(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps([1, 2, 3]))

    assert response["error"]["code"] == INVALID_REQUEST


def test_missing_method_returns_invalid_request(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 4, "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST
    assert response["id"] == 4


def test_non_object_params_returns_invalid_params(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 5, "method": "guardian.converse", "params": "not an object"})
    )

    assert response["error"]["code"] == INVALID_PARAMS


def test_unknown_method_returns_method_not_found(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 6, "method": "does.not.exist", "params": {}}))

    assert response["error"]["code"] == METHOD_NOT_FOUND
    assert "does.not.exist" in response["error"]["message"]


def test_handler_exception_returns_internal_error_without_leaking_details(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 7, "method": "guardian.converse", "params": {"message": 12345}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("TypeError:")


def test_serve_forever_processes_multiple_lines_and_skips_blank_lines(tmp_path):
    server = _server(tmp_path)
    requests = (
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "platform.status", "params": {}})
        + "\n\n"
        + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "guardian.converse", "params": {"message": "hi"}})
        + "\n"
    )
    in_stream = io.StringIO(requests)
    out_stream = io.StringIO()

    server.serve_forever(in_stream=in_stream, out_stream=out_stream)

    # Both requested methods map to the "jarvis" cluster (EBG-0121), so each
    # response is now followed by a knowledge.cluster_activity notification -
    # filter to responses (always carry "id") to keep this test's original
    # assertion about request/response handling itself, not the new
    # notification stream, which the tests below cover directly.
    all_messages = [json.loads(line) for line in out_stream.getvalue().splitlines() if line]
    responses = [message for message in all_messages if "id" in message]
    assert len(responses) == 2
    first, second = responses
    assert first["id"] == 1
    assert second["result"]["message"] == "local-echo: hi"


def test_notification_without_id_still_returns_a_response_with_null_id(tmp_path):
    """JSON-RPC 2.0 notifications (no id) are not implemented as fire-and-forget
    here - foundation scope always responds, matching the synchronous
    request/response design recorded in ESR-0017 WP9. Documented explicitly so
    a future notification implementation is a deliberate change, not a silent
    behaviour drift."""

    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "method": "platform.status", "params": {}}))

    assert response["id"] is None
    assert "result" in response


def test_heartbeat_loop_emits_notification_with_no_id_key(tmp_path):
    """EIP-ESR0031-002: a heartbeat notification is a JSON-RPC object with no
    `id` key at all - the spec's own signal distinguishing a notification from
    a response, which always carries `id` (even `null`, per the test above).
    Exercises `_heartbeat_loop` directly with a short real interval rather than
    a real 30-second sleep, per the EIP's own validation requirement."""

    server = StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }),
        heartbeat_interval_seconds=0.01,
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )
    out_stream = io.StringIO()
    stop_event = threading.Event()

    thread = threading.Thread(target=server._heartbeat_loop, args=(out_stream, stop_event))
    thread.start()
    time.sleep(0.05)
    stop_event.set()
    thread.join(timeout=1.0)

    assert not thread.is_alive()
    lines = [line for line in out_stream.getvalue().splitlines() if line]
    assert len(lines) >= 1
    notification = json.loads(lines[0])
    assert "id" not in notification
    assert notification["jsonrpc"] == "2.0"
    assert notification["method"] == "system.heartbeat"
    assert "timestamp" in notification["params"]


def test_heartbeat_loop_writes_nothing_after_stop_event_set_before_first_interval(tmp_path):
    """A stop signalled before the first interval elapses must prevent any
    heartbeat write - the loop must check stop_event before writing, not just
    between writes."""

    server = _server(tmp_path)
    out_stream = io.StringIO()
    stop_event = threading.Event()
    stop_event.set()

    server._heartbeat_loop(out_stream, stop_event)

    assert out_stream.getvalue() == ""


def test_serve_forever_emits_cluster_activity_notification_with_no_id_key(tmp_path):
    """EBG-0121: a knowledge.cluster_activity notification is a JSON-RPC
    object with no `id` key, mirroring system.heartbeat's own shape
    (test_heartbeat_loop_emits_notification_with_no_id_key above), emitted
    for a real dispatched method that maps to a cluster."""

    server = StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }),
        heartbeat_interval_seconds=9999.0,
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )
    in_stream = io.StringIO(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.speak", "params": {"text": "hi"}}) + "\n"
    )
    out_stream = io.StringIO()

    server.serve_forever(in_stream=in_stream, out_stream=out_stream)

    messages = [json.loads(line) for line in out_stream.getvalue().splitlines() if line]
    notifications = [message for message in messages if "id" not in message]
    assert len(notifications) == 1
    notification = notifications[0]
    assert notification["jsonrpc"] == "2.0"
    assert notification["method"] == "knowledge.cluster_activity"
    assert notification["params"]["cluster"] == "sentinel"
    assert notification["params"]["method"] == "guardian.speak"
    assert "timestamp" in notification["params"]


def test_serve_forever_emits_no_cluster_activity_notification_for_a_failed_request(tmp_path):
    """Only a successful dispatch counts as genuine cluster access - a
    request that never reaches a real handler (invalid params) must not
    illuminate anything."""

    server = _server(tmp_path)
    in_stream = io.StringIO(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.speak", "params": {}}) + "\n"
    )
    out_stream = io.StringIO()

    server.serve_forever(in_stream=in_stream, out_stream=out_stream)

    messages = [json.loads(line) for line in out_stream.getvalue().splitlines() if line]
    assert len(messages) == 1
    assert "error" in messages[0]


def test_knowledge_graph_response_includes_active_clusters_pull_field(tmp_path):
    """EBG-0121: knowledge.graph's response gains a real active_clusters
    field reflecting activity already observed before this fetch - the
    pull-interface half of cluster illumination."""

    server = _server(tmp_path)

    server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.speak", "params": {"text": "hi"}}))
    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "knowledge.graph", "params": {}}))

    assert response["result"]["active_clusters"] == ["sentinel"]


def test_knowledge_graph_response_active_clusters_empty_with_no_prior_activity(tmp_path):
    """No-mock-fallback rule (ESR-0017 WP9): a fresh server with no prior
    dispatch activity must report an empty active_clusters list, never a
    placeholder or decorative default."""

    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "knowledge.graph", "params": {}}))

    assert response["result"]["active_clusters"] == []


def test_serve_forever_still_processes_requests_correctly_with_heartbeat_thread_running(tmp_path):
    """Regression check: serve_forever's existing request/response behaviour
    (EIP-ESR0031-002 Implementation Requirement 4) must be unaffected by the
    heartbeat thread now running alongside it. Uses a large interval so the
    heartbeat itself cannot fire during this test, isolating this assertion
    from any timing flakiness."""

    server = StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }),
        heartbeat_interval_seconds=9999.0,
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )
    requests = (
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "platform.status", "params": {}})
        + "\n\n"
        + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "guardian.converse", "params": {"message": "hi"}})
        + "\n"
    )
    in_stream = io.StringIO(requests)
    out_stream = io.StringIO()

    server.serve_forever(in_stream=in_stream, out_stream=out_stream)

    # Same filtering rationale as
    # test_serve_forever_processes_multiple_lines_and_skips_blank_lines above.
    all_messages = [json.loads(line) for line in out_stream.getvalue().splitlines() if line]
    responses = [message for message in all_messages if "id" in message]
    assert len(responses) == 2
    first, second = responses
    assert first["id"] == 1
    assert second["result"]["message"] == "local-echo: hi"


class _SlowLineStream:
    """An iterable yielding each line with a short real delay between them,
    giving a background heartbeat thread a genuine chance to interleave -
    a plain io.StringIO yields all lines instantly, never allowing that."""

    def __init__(self, lines: list[str], delay_seconds: float) -> None:
        self._lines = lines
        self._delay_seconds = delay_seconds

    def __iter__(self):
        for line in self._lines:
            time.sleep(self._delay_seconds)
            yield line


def test_serve_forever_interleaves_heartbeats_without_corrupting_any_line(tmp_path):
    """EIP-ESR0031-002 Implementation Requirement 1: a response write and a
    heartbeat write must never interleave into one corrupted line. Uses a slow
    input stream so the heartbeat thread has real chances to fire between
    requests, then asserts every single output line is independently valid
    JSON - a corruption would produce an unparsable or malformed line."""

    server = StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }),
        heartbeat_interval_seconds=0.01,
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )
    requests = [
        json.dumps({"jsonrpc": "2.0", "id": i, "method": "platform.status", "params": {}})
        for i in range(5)
    ]
    in_stream = _SlowLineStream(requests, delay_seconds=0.03)
    out_stream = io.StringIO()

    server.serve_forever(in_stream=in_stream, out_stream=out_stream)

    lines = [line for line in out_stream.getvalue().splitlines() if line]
    parsed = [json.loads(line) for line in lines]  # raises if any line is corrupted

    responses = [obj for obj in parsed if "id" in obj]
    notifications = [obj for obj in parsed if "id" not in obj]
    assert len(responses) == 5
    # Two independent notification sources now interleave with responses on
    # this shared stream: the heartbeat thread (system.heartbeat) and
    # serve_forever's own knowledge.cluster_activity emission (EBG-0121) -
    # each platform.status call maps to the "jarvis" cluster. Every line
    # already parsed cleanly above (the actual interleaving-safety
    # assertion); this just confirms no unexpected third notification type.
    assert all(notification["method"] in ("system.heartbeat", "knowledge.cluster_activity") for notification in notifications)
    cluster_activity_notifications = [n for n in notifications if n["method"] == "knowledge.cluster_activity"]
    assert len(cluster_activity_notifications) == 5
    assert all(n["params"]["cluster"] == "jarvis" for n in cluster_activity_notifications)


def test_memory_propose_approve_list_round_trip(tmp_path):
    """EBG-0080: memory.propose -> memory.approve -> memory.list through the
    real StdioRpcServer, proving the consent gate end to end, not just at the
    service-unit level (jarvis/tests/test_memory_service.py)."""

    server = _server(tmp_path)

    propose_response = server.handle_line(
        json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "memory.propose", "params": {"content": "Robert prefers dark mode."}}
        )
    )
    pending_id = propose_response["result"]["pendingId"]

    approve_response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "memory.approve", "params": {"pendingId": pending_id}})
    )

    assert approve_response["result"]["content"] == "Robert prefers dark mode."
    assert approve_response["result"]["consentDecisionId"]

    list_response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "memory.list", "params": {}}))

    assert len(list_response["result"]["records"]) == 1
    assert list_response["result"]["records"][0]["content"] == "Robert prefers dark mode."


def test_memory_propose_deny_list_round_trip_confirms_denied_item_never_appears(tmp_path):
    server = _server(tmp_path)

    propose_response = server.handle_line(
        json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "memory.propose", "params": {"content": "Robert dislikes cilantro."}}
        )
    )
    pending_id = propose_response["result"]["pendingId"]

    deny_response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "memory.deny", "params": {"pendingId": pending_id}})
    )

    assert deny_response["result"]["decision"] == "denied"

    list_response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "memory.list", "params": {}}))

    assert list_response["result"]["records"] == []


def test_memory_propose_rejects_non_string_content(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "memory.propose", "params": {"content": 12345}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("TypeError:")


def test_memory_approve_rejects_non_string_pending_id(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "memory.approve", "params": {"pendingId": 12345}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("TypeError:")


def test_memory_approve_unknown_pending_id_returns_internal_error(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "memory.approve", "params": {"pendingId": "does-not-exist"}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("KeyError:")


def test_profile_list_empty_before_any_profile_created(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "profile.list", "params": {}}))

    assert response["result"] == {"profiles": []}


def test_profile_active_none_before_any_selection(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "profile.active", "params": {}}))

    assert response["result"] == {"profile": None}


def test_profile_create_list_select_active_round_trip(tmp_path):
    server = _server(tmp_path)

    create_response = server.handle_line(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "profile.create",
                "params": {"displayName": "Robert", "role": "Administrator"},
            }
        )
    )
    created = create_response["result"]
    assert created["displayName"] == "Robert"
    assert created["role"] == "Administrator"
    assert "id" in created
    assert "createdAt" in created

    list_response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "profile.list", "params": {}}))
    assert list_response["result"] == {"profiles": [created]}

    select_response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "profile.select", "params": {"profileId": created["id"]}})
    )
    assert select_response["result"] == created

    active_response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 4, "method": "profile.active", "params": {}})
    )
    assert active_response["result"] == {"profile": created}


def test_profile_create_rejects_non_string_display_name(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "profile.create", "params": {"displayName": 123, "role": "Adult"}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("TypeError:")


def test_profile_create_rejects_unknown_role(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "profile.create",
                "params": {"displayName": "Robert", "role": "Superuser"},
            }
        )
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("ValueError:")


def test_profile_select_unknown_id_returns_internal_error(tmp_path):
    server = _server(tmp_path)

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "profile.select", "params": {"profileId": "does-not-exist"}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("ValueError:")


def test_profile_active_persists_across_new_server_instance_against_same_db(tmp_path):
    """Mirrors the memory store's own persists-across-instance precedent -
    the active profile selection must survive a process restart, since
    ProfileStore persists it to the same SQLite file rather than holding it
    only in memory."""

    db_path = tmp_path / "profiles.db"
    first_server = StdioRpcServer(
        GuardianRuntime(), identity_service=ProfileService(ProfileStore(db_path))
    )
    created = first_server.handle_line(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "profile.create",
                "params": {"displayName": "Robert", "role": "Administrator"},
            }
        )
    )["result"]
    first_server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "profile.select", "params": {"profileId": created["id"]}})
    )

    second_server = StdioRpcServer(
        GuardianRuntime(), identity_service=ProfileService(ProfileStore(db_path))
    )
    response = second_server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "profile.active", "params": {}})
    )

    assert response["result"] == {"profile": created}
