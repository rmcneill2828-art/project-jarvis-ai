"""Tests for the JSON-RPC 2.0 stdio bridge (ESR-0017 WP9)."""

import io
import json

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


def _server() -> StdioRpcServer:
    # Explicit empty environ: keeps tests deterministic and offline regardless
    # of real provider credentials the host machine may have set persistently
    # (e.g. for the manual smoke-test scripts) - never depend on, or
    # accidentally exercise, real credentials in the automated suite.
    return StdioRpcServer(build_default_runtime(environ={}))


def test_build_default_runtime_is_started_and_connected():
    runtime = build_default_runtime(environ={})

    assert runtime.status().value == "Running"
    assert runtime.services()["Guardian Provider Boundary"].status.value == "Online"


def test_build_default_runtime_falls_back_to_local_echo_without_credential():
    runtime = build_default_runtime(environ={})

    assert runtime.configured_providers() == ("local-echo",)


def test_build_default_runtime_wires_openai_as_default_primary_when_credential_present():
    runtime = build_default_runtime(environ={"OPENAI_API_KEY": "test-key-not-a-real-credential"})

    assert runtime.configured_providers() == ("openai", "local-echo")


def test_build_default_runtime_respects_primary_provider_selection():
    runtime = build_default_runtime(
        environ={
            "JARVIS_PRIMARY_PROVIDER": "gemini",
            "GEMINI_API_KEY": "test-key-not-a-real-credential",
        }
    )

    assert runtime.configured_providers() == ("gemini", "local-echo")


def test_build_default_runtime_ignores_unselected_provider_credential():
    # OPENAI_API_KEY being set should not matter when gemini is selected but
    # has no credential of its own - local-echo remains the only fallback.
    runtime = build_default_runtime(
        environ={"JARVIS_PRIMARY_PROVIDER": "gemini", "OPENAI_API_KEY": "test-key-not-a-real-credential"}
    )

    assert runtime.configured_providers() == ("local-echo",)


def test_build_default_runtime_falls_through_to_default_model_when_env_var_is_blank():
    # A present-but-blank OPENAI_MODEL must not override the fallback default
    # with an empty string - that would make OpenAIProvider's constructor
    # reject the configuration, turning a harmless placeholder into a startup
    # failure (Engineering Reviewer finding, EIP-ESR0022-001).
    runtime = build_default_runtime(
        environ={"OPENAI_API_KEY": "test-key-not-a-real-credential", "OPENAI_MODEL": ""}
    )

    assert runtime.configured_providers() == ("openai", "local-echo")


def test_build_default_runtime_wires_trust_tier_policy_as_the_production_policy_engine():
    """EBG-0074 (ESR-0024): build_default_runtime()'s gateway must actually run
    TrustTierPolicy, not merely have the class available in the codebase.
    Asserted directly against the object build_default_runtime() itself
    produces - not a separately constructed gateway - so this proves the real
    wiring, not just that TrustTierPolicy is importable."""

    runtime = build_default_runtime(environ={})

    assert isinstance(runtime.sentinel_gateway().policy_engine, TrustTierPolicy)


def test_guardian_converse_request_shape_classified_routine_under_trust_tier_policy():
    """Regression, beyond re-asserting the unchanged RPC response: confirms
    *why* it is unchanged - the real conversation request shape
    (SentinelGatedConversationProvider.generate()'s fixed
    metadata={"capability": "text-generation"}, default payload_type,
    requires_approval=False) is classified TrustCategory.ROUTINE_INTERACTION /
    TrustTier.ROUTINE -> ALLOW by the production-wired TrustTierPolicy itself,
    evaluated through build_default_runtime()'s own gateway - not a separately
    constructed policy instance, and not the category-matrix already covered
    by jarvis/tests/test_sentinel_policy.py."""

    runtime = build_default_runtime(environ={})
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


def test_guardian_converse_returns_real_response_through_sentinel():
    server = _server()

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.converse", "params": {"message": "hello"}})
    )

    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"message": "local-echo: hello", "provider": "local-echo"},
    }


def test_platform_status_reflects_real_runtime_state():
    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "platform.status", "params": {}}))

    assert response["result"] == {
        "state": "Running",
        "runtimeHealth": "Healthy",
        "providerConnected": "Online",
        "providers": ["local-echo"],
    }


def test_knowledge_graph_returns_real_repository_data():
    """EBG-0055 Phase 1 (ESR-0019 WP2): dispatch-level check that the method
    is wired and returns real data, not the full parser behaviour matrix
    (already covered by jarvis/tests/test_knowledge_graph.py)."""

    server = _server()

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 6, "method": "knowledge.graph", "params": {}})
    )

    assert "error" not in response
    node_ids = {node["id"] for node in response["result"]["nodes"]}
    assert "README.md" in node_ids
    assert len(response["result"]["edges"]) > 0


def test_missing_params_defaults_to_empty_object():
    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "platform.status"}))

    assert "error" not in response
    assert response["result"]["state"] == "Running"


def test_malformed_json_returns_parse_error():
    server = _server()

    response = server.handle_line("not valid json{{{")

    assert response["error"]["code"] == PARSE_ERROR
    assert response["id"] is None


def test_missing_jsonrpc_version_returns_invalid_request():
    server = _server()

    response = server.handle_line(json.dumps({"id": 4, "method": "platform.status", "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST
    assert response["id"] == 4


def test_wrong_jsonrpc_version_returns_invalid_request():
    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "1.0", "id": 5, "method": "platform.status", "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST


def test_non_object_request_returns_invalid_request():
    server = _server()

    response = server.handle_line(json.dumps([1, 2, 3]))

    assert response["error"]["code"] == INVALID_REQUEST


def test_missing_method_returns_invalid_request():
    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 4, "params": {}}))

    assert response["error"]["code"] == INVALID_REQUEST
    assert response["id"] == 4


def test_non_object_params_returns_invalid_params():
    server = _server()

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 5, "method": "guardian.converse", "params": "not an object"})
    )

    assert response["error"]["code"] == INVALID_PARAMS


def test_unknown_method_returns_method_not_found():
    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 6, "method": "does.not.exist", "params": {}}))

    assert response["error"]["code"] == METHOD_NOT_FOUND
    assert "does.not.exist" in response["error"]["message"]


def test_handler_exception_returns_internal_error_without_leaking_details():
    server = _server()

    response = server.handle_line(
        json.dumps({"jsonrpc": "2.0", "id": 7, "method": "guardian.converse", "params": {"message": 12345}})
    )

    assert response["error"]["code"] == INTERNAL_ERROR
    assert response["error"]["message"].startswith("TypeError:")


def test_serve_forever_processes_multiple_lines_and_skips_blank_lines():
    server = _server()
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


def test_notification_without_id_still_returns_a_response_with_null_id():
    """JSON-RPC 2.0 notifications (no id) are not implemented as fire-and-forget
    here - foundation scope always responds, matching the synchronous
    request/response design recorded in ESR-0017 WP9. Documented explicitly so
    a future notification implementation is a deliberate change, not a silent
    behaviour drift."""

    server = _server()

    response = server.handle_line(json.dumps({"jsonrpc": "2.0", "method": "platform.status", "params": {}}))

    assert response["id"] is None
    assert "result" in response
