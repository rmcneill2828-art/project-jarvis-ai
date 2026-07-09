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


def _server() -> StdioRpcServer:
    return StdioRpcServer(build_default_runtime())


def test_build_default_runtime_is_started_and_connected():
    runtime = build_default_runtime()

    assert runtime.status().value == "Running"
    assert runtime.services()["Guardian Provider Boundary"].status.value == "Online"


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
    }


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
