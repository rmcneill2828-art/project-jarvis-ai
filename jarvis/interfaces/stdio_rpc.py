"""JSON-RPC 2.0 over stdio - the UXP-backend bridge entry point (ADR-0019).

Foundation scope only (ESR-0017 WP9): a persistent, newline-delimited
JSON-RPC 2.0 loop over stdin/stdout, intended to be spawned as a long-lived
child process by the Tauri shell. Wires a zero-config Guardian+Sentinel stack
(SentinelTrustGateway + ProviderOrchestrator + LocalEchoProvider) by default -
proving the UXP-to-Guardian-to-Sentinel path, not external model quality
(deferred to EBG-0051/a later provider toggle, per ChatGPT Engineering
Reviewer's WP9 design-review finding 2).

The JSON-RPC 2.0 envelope is adopted now, even though only synchronous
request/response is implemented, specifically so EBG-0050's later streaming
notifications can be added without a breaking change (Reviewer finding 5).
"""

import json
import sys
from typing import Any, TextIO

from jarvis.guardian.runtime import GuardianRuntime
from jarvis.interfaces import knowledge_graph
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from sentinel.core import SentinelTrustGateway
from sentinel.local_provider import LocalEchoProvider
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute

JSONRPC_VERSION = "2.0"

# Standard JSON-RPC 2.0 pre-defined error codes, plus one server-defined code
# in the reserved -32000 to -32099 range for internal handler failures.
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32000


def build_default_runtime() -> GuardianRuntime:
    """Build and start the zero-config Guardian+Sentinel stack used by foundation mode."""

    gateway = SentinelTrustGateway()
    orchestrator = ProviderOrchestrator()
    local_provider = LocalEchoProvider()
    orchestrator.register_provider(local_provider)
    orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=(local_provider.name,))
    )
    conversation_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)
    runtime = GuardianRuntime(conversation_provider=conversation_provider)
    runtime.start()
    return runtime


class StdioRpcServer:
    """Minimal JSON-RPC 2.0 server dispatching Guardian/Sentinel calls over stdio."""

    def __init__(self, runtime: GuardianRuntime) -> None:
        self._runtime = runtime
        self._methods = {
            "guardian.converse": self._guardian_converse,
            "platform.status": self._platform_status,
            "knowledge.graph": self._knowledge_graph,
        }

    def _guardian_converse(self, params: dict[str, Any]) -> dict[str, Any]:
        message = params.get("message")
        if not isinstance(message, str):
            msg = "params.message must be a string."
            raise TypeError(msg)
        response = self._runtime.converse(message)
        return {"message": response.message, "provider": response.provider}

    def _platform_status(self, params: dict[str, Any]) -> dict[str, Any]:  # noqa: ARG002
        snapshot = self._runtime.status_snapshot()
        provider_boundary = snapshot.services.get("Guardian Provider Boundary")
        return {
            "state": snapshot.state.value,
            "runtimeHealth": snapshot.runtime_health.value,
            "providerConnected": provider_boundary.status.value if provider_boundary else "Unknown",
        }

    def _knowledge_graph(self, params: dict[str, Any]) -> dict[str, Any]:  # noqa: ARG002
        return knowledge_graph.build_graph()

    def handle_line(self, line: str) -> dict[str, Any] | None:
        """Handle one JSON-RPC 2.0 request line, returning the response object."""

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            return self._error(None, PARSE_ERROR, "Parse error: invalid JSON.")

        if not isinstance(request, dict):
            return self._error(None, INVALID_REQUEST, "Invalid request: expected a JSON object.")

        request_id = request.get("id")

        if request.get("jsonrpc") != JSONRPC_VERSION:
            return self._error(request_id, INVALID_REQUEST, 'Invalid request: jsonrpc must be "2.0".')

        method = request.get("method")
        params = request.get("params", {})

        if not isinstance(method, str) or not method:
            return self._error(request_id, INVALID_REQUEST, "Invalid request: method must be a non-empty string.")
        if not isinstance(params, dict):
            return self._error(request_id, INVALID_PARAMS, "Invalid params: expected a JSON object.")

        handler = self._methods.get(method)
        if handler is None:
            return self._error(request_id, METHOD_NOT_FOUND, f"Method not found: {method}.")

        try:
            result = handler(params)
        except Exception as exc:
            # Deliberately expose only the exception type and message, matching
            # the same rationale as OpenAIProvider/GeminiProvider - never let a
            # raw internal error leak more than necessary into a client-facing
            # channel, while still being diagnostically useful.
            return self._error(request_id, INTERNAL_ERROR, f"{type(exc).__name__}: {exc}")

        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": {"code": code, "message": message}}

    def serve_forever(self, in_stream: TextIO | None = None, out_stream: TextIO | None = None) -> None:
        """Read one JSON-RPC request per line from in_stream, writing responses to out_stream."""

        in_stream = in_stream if in_stream is not None else sys.stdin
        out_stream = out_stream if out_stream is not None else sys.stdout

        for raw_line in in_stream:
            line = raw_line.strip()
            if not line:
                continue
            response = self.handle_line(line)
            if response is not None:
                out_stream.write(json.dumps(response) + "\n")
                out_stream.flush()


def run() -> None:
    """Entry point: build the default runtime and serve JSON-RPC over stdio until stdin closes."""

    runtime = build_default_runtime()
    server = StdioRpcServer(runtime)
    try:
        server.serve_forever()
    finally:
        runtime.stop()
