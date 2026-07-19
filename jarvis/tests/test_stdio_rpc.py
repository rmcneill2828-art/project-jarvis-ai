"""Tests for the JSON-RPC 2.0 stdio bridge (ESR-0017 WP9)."""

import io
import json
from datetime import datetime, timezone

from jarvis.gia.observability import GiaSnapshot
from jarvis.interfaces.stdio_rpc import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    PARSE_ERROR,
    StdioRpcServer,
    build_default_runtime,
)
from jarvis.guardian.runtime import GuardianRuntime
from sentinel.core import SentinelDecisionOutcome, SentinelRequest
from sentinel.policy import TrustCategory, TrustTier, TrustTierPolicy


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
    return StdioRpcServer(
        build_default_runtime(environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        })
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
        "providers": ["ollama", "local-echo"],
        "policyEngine": "TrustTierPolicy",
    }


def test_platform_status_policy_engine_is_none_without_a_connected_gateway():
    """EIP-ESR0024-002: policyEngine must degrade honestly (None), not raise,
    when no conversation provider - and therefore no Sentinel gateway - is
    connected. build_default_runtime() always wires one, so this exercises
    the defensive branch directly via a bare GuardianRuntime instead."""

    server = StdioRpcServer(GuardianRuntime())

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "platform.status", "params": {}}))

    assert response["result"]["policyEngine"] is None


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

    captured_at = datetime(2026, 7, 19, 10, 0, 0, tzinfo=timezone.utc)
    fake_snapshot = GiaSnapshot(
        cpu_percent=12.5,
        memory_percent=64.0,
        memory_used_mb=2048.0,
        memory_total_mb=4096.0,
        disk_percent=28.7,
        disk_used_gb=430.5,
        disk_total_gb=1500.3,
        captured_at=captured_at,
    )
    server = StdioRpcServer(build_default_runtime(), gia_observer=_fake_gia_observer(fake_snapshot))

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 7, "method": "gia.status", "params": {}}))

    assert response["result"] == {
        "cpuPercent": 12.5,
        "memoryPercent": 64.0,
        "memoryUsedMb": 2048.0,
        "memoryTotalMb": 4096.0,
        "diskPercent": 28.7,
        "diskUsedGb": 430.5,
        "diskTotalGb": 1500.3,
        "capturedAt": "2026-07-19T10:00:00+00:00",
    }


def test_gia_status_does_not_require_a_started_or_connected_runtime():
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
        captured_at=datetime(2026, 7, 19, 10, 0, 0, tzinfo=timezone.utc),
    )
    server = StdioRpcServer(GuardianRuntime(), gia_observer=_fake_gia_observer(fake_snapshot))

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

    lines = [line for line in out_stream.getvalue().splitlines() if line]
    assert len(lines) == 2
    first, second = (json.loads(line) for line in lines)
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
