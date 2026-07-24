"""JSON-RPC 2.0 over stdio - the UXP-backend bridge entry point (ADR-0019).

Foundation scope only (ESR-0017 WP9): a persistent, newline-delimited
JSON-RPC 2.0 loop over stdin/stdout, intended to be spawned as a long-lived
child process by the Tauri shell. Wires a zero-config Guardian+Sentinel stack
(SentinelTrustGateway, wired with TrustTierPolicy per EBG-0074/ESR-0024, +
ProviderOrchestrator + LocalEchoProvider) by default - proving the
UXP-to-Guardian-to-Sentinel path, not external model quality (deferred to
EBG-0051/a later provider toggle, per ChatGPT Engineering Reviewer's WP9
design-review finding 2).

The JSON-RPC 2.0 envelope is adopted now, even though only synchronous
request/response is implemented, specifically so EBG-0050's later streaming
notifications can be added without a breaking change (Reviewer finding 5).

EIP-ESR0031-002 (Streaming Notifications MVP) exercises that envelope for
the first time: `serve_forever()` now also runs a background heartbeat
thread that periodically writes a `system.heartbeat` JSON-RPC
notification - a message with no `id` key at all, the JSON-RPC 2.0 signal
distinguishing an unsolicited notification from a response (which always
carries `id`, even `null` for certain error cases). A single write lock is
shared between the main loop's response writes and the heartbeat thread's
notification writes so the two can never interleave partial JSON onto one
line.
"""

import json
import os
import sys
import threading
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

from jarvis.gia.observability import LocalResourceObserver
from jarvis.guardian.runtime import GuardianRuntime
from jarvis.interfaces import knowledge_graph
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from sentinel.core import SentinelTrustGateway
from sentinel.gemini_provider import GeminiProvider
from sentinel.local_provider import LocalEchoProvider
from sentinel.ollama_provider import OllamaProvider
from sentinel.openai_provider import OpenAIProvider
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.policy import TrustTierPolicy
from sentinel.provider_config import CredentialReference, ProviderConfiguration

JSONRPC_VERSION = "2.0"

# Selects which real provider build_default_runtime() tries to wire as primary;
# unset defaults to "openai" per PEM-001's Primary/Secondary designation.
PRIMARY_PROVIDER_ENV_VAR = "JARVIS_PRIMARY_PROVIDER"
DEFAULT_PRIMARY_PROVIDER = "openai"

# Per-provider credential/model env var names and default models, matching the
# established convention from scripts/wp5_first_conversation_demo.py (OpenAI)
# and scripts/gemini_provider_smoke_test.py (Gemini).
_REAL_PROVIDER_SPECS: dict[str, dict[str, str]] = {
    "openai": {
        "credential_env_var": "OPENAI_API_KEY",
        "model_env_var": "OPENAI_MODEL",
        "default_model": "gpt-5.5",
    },
    "gemini": {
        "credential_env_var": "GEMINI_API_KEY",
        "model_env_var": "GEMINI_MODEL",
        "default_model": "gemini-2.5-flash",
    },
}

# Ollama (EBG-0075, EIP-ESR0025-002): unlike the cloud providers above, this
# has no credential gate - registered unconditionally, since a local, missing
# or unreachable Ollama installation fails over identically to any other
# provider failure via ProviderOrchestrator's existing exception-driven
# failover. Default model is the fastest of the four confirmed-installed
# models at scoping time - latency matters more than peak capability for a
# fallback role. Timeout is 90s, not the 30s default, to accommodate the
# confirmed ~64s cold-start model load.
OLLAMA_MODEL_ENV_VAR = "JARVIS_OLLAMA_MODEL"
OLLAMA_ENDPOINT_ENV_VAR = "JARVIS_OLLAMA_ENDPOINT"
DEFAULT_OLLAMA_MODEL = "qwen3.5:2b"
OLLAMA_TIMEOUT_SECONDS = 90.0

# Personal Memory store location (EIP-ESR0027-001). Overridable so tests never
# touch the real store - the exact lesson learned from ESR-0026 WP1's Ollama
# test-isolation defect (a shared test helper making real network calls
# because nothing pointed it away from the real endpoint) applies here too,
# just for a local file instead of a network endpoint.
MEMORY_DB_PATH_ENV_VAR = "JARVIS_MEMORY_DB_PATH"
DEFAULT_MEMORY_DB_PATH = Path.home() / ".jarvis" / "memory" / "personal.db"

# Streaming Notifications MVP (EIP-ESR0031-002): interval between heartbeat
# notifications, overridable per JARVIS_MEMORY_DB_PATH's established
# test-isolation convention - a real 30-second sleep has no place in a test.
HEARTBEAT_INTERVAL_ENV_VAR = "JARVIS_HEARTBEAT_INTERVAL_SECONDS"
DEFAULT_HEARTBEAT_INTERVAL_SECONDS = 30.0

# Standard JSON-RPC 2.0 pre-defined error codes, plus one server-defined code
# in the reserved -32000 to -32099 range for internal handler failures.
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32000


def _build_real_provider(name: str, environ: Mapping[str, str]) -> OpenAIProvider | GeminiProvider | None:
    """Build the named real provider adapter, or None if its credential is absent or blank.

    An absent or blank credential is treated as "not available on this machine",
    not a startup failure - build_default_runtime() always keeps LocalEchoProvider
    as the route's final fallback, matching this codebase's existing
    honest-degradation pattern (ESR-0017 WP9's no-mock-fallback rule).
    """

    spec = _REAL_PROVIDER_SPECS.get(name)
    if spec is None:
        return None
    if not environ.get(spec["credential_env_var"]):
        return None
    # A present-but-blank model env var must fall through to the default model,
    # same as an absent one - environ.get(key, default) alone would let a blank
    # placeholder silently override the default with "", which the provider
    # constructor then rejects as an invalid configuration (Engineering
    # Reviewer finding, EIP-ESR0022-001).
    model = environ.get(spec["model_env_var"]) or spec["default_model"]
    configuration = ProviderConfiguration(
        provider_name=name,
        default_model=model,
        credential=CredentialReference(environment_variable=spec["credential_env_var"]),
    )
    if name == "openai":
        return OpenAIProvider(configuration)
    return GeminiProvider(configuration)


def build_default_runtime(environ: Mapping[str, str] | None = None) -> GuardianRuntime:
    """Build and start the production Guardian+Sentinel stack.

    Registers a real provider (OpenAI or Gemini, selected by
    JARVIS_PRIMARY_PROVIDER, default "openai" per PEM-001's Primary
    designation) as the primary text-generation route provider only when its
    credential env var is present and non-blank in `environ`; LocalEchoProvider
    is always registered as the final failover, so a machine with no key
    configured - or a real provider call that fails at runtime - still has a
    working conversation path (EBG-0070, ESR-0022).

    `environ` defaults to `os.environ`. Tests must pass an explicit mapping
    (e.g. `{}`) rather than relying on the default, so test runs stay
    deterministic and never depend on - or accidentally exercise - real
    credentials that happen to be set on the host machine.
    """

    environ = os.environ if environ is None else environ

    gateway = SentinelTrustGateway(policy_engine=TrustTierPolicy())
    orchestrator = ProviderOrchestrator()

    route_providers: list[str] = []
    primary_name = environ.get(PRIMARY_PROVIDER_ENV_VAR, DEFAULT_PRIMARY_PROVIDER)
    real_provider = _build_real_provider(primary_name, environ)
    if real_provider is not None:
        orchestrator.register_provider(real_provider)
        route_providers.append(real_provider.name)

    ollama_model = environ.get(OLLAMA_MODEL_ENV_VAR) or DEFAULT_OLLAMA_MODEL
    ollama_configuration = ProviderConfiguration(
        provider_name="ollama",
        default_model=ollama_model,
        endpoint=environ.get(OLLAMA_ENDPOINT_ENV_VAR) or None,
        timeout_seconds=OLLAMA_TIMEOUT_SECONDS,
    )
    ollama_provider = OllamaProvider(ollama_configuration)
    orchestrator.register_provider(ollama_provider)
    route_providers.append(ollama_provider.name)

    local_provider = LocalEchoProvider()
    orchestrator.register_provider(local_provider)
    route_providers.append(local_provider.name)

    orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=tuple(route_providers))
    )
    conversation_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)

    memory_db_path = Path(environ[MEMORY_DB_PATH_ENV_VAR]) if environ.get(MEMORY_DB_PATH_ENV_VAR) else DEFAULT_MEMORY_DB_PATH
    memory_store = PersonalMemoryStore(memory_db_path)
    # Reuses the same gateway instance conversation requests are evaluated
    # against - one trust boundary, not two (EIP-ESR0027-001 Section 4).
    memory_service = PersonalMemoryService(gateway=gateway, store=memory_store)

    runtime = GuardianRuntime(conversation_provider=conversation_provider, memory_service=memory_service)
    runtime.start()
    return runtime


class StdioRpcServer:
    """Minimal JSON-RPC 2.0 server dispatching Guardian/Sentinel calls over stdio."""

    def __init__(
        self,
        runtime: GuardianRuntime,
        gia_observer: LocalResourceObserver | None = None,
        heartbeat_interval_seconds: float | None = None,
    ) -> None:
        self._runtime = runtime
        # Streaming Notifications MVP (EIP-ESR0031-002): shared between the
        # main loop's response writes (serve_forever) and the heartbeat
        # thread's notification writes (_heartbeat_loop) so the two can never
        # interleave partial JSON onto the same output line.
        self._write_lock = threading.Lock()
        if heartbeat_interval_seconds is not None:
            self._heartbeat_interval_seconds = heartbeat_interval_seconds
        else:
            self._heartbeat_interval_seconds = float(
                os.environ.get(HEARTBEAT_INTERVAL_ENV_VAR, DEFAULT_HEARTBEAT_INTERVAL_SECONDS)
            )
        # GIA (EBG-0083) is deliberately not constructed from or dependent on
        # `runtime` - per ESR-0011 Section 10, it observes and publishes local
        # resource state independent of Guardian's own lifecycle. This is
        # method-level decoupling only; `gia.status` is still unreachable if
        # `build_default_runtime()` fails before this server is constructed
        # (see `run()`), a disclosed limitation, not fixed by this class.
        # `gia_observer` is injectable (defaulting to the real psutil-backed
        # observer) so RPC-layer tests can assert exact serialization from a
        # deterministic fake snapshot, per EIP-ESR0029-002 Section 4.6/5.5,
        # rather than depending on the actual host machine's live values.
        self._gia_observer = gia_observer or LocalResourceObserver()
        self._methods = {
            "guardian.converse": self._guardian_converse,
            "platform.status": self._platform_status,
            "knowledge.graph": self._knowledge_graph,
            "memory.propose": self._memory_propose,
            "memory.approve": self._memory_approve,
            "memory.deny": self._memory_deny,
            "memory.list": self._memory_list,
            "gia.status": self._gia_status,
        }

    def _guardian_converse(self, params: dict[str, Any]) -> dict[str, Any]:
        message = params.get("message")
        if not isinstance(message, str):
            msg = "params.message must be a string."
            raise TypeError(msg)
        response = self._runtime.converse(message)
        return {"message": response.message, "provider": response.provider}

    def _platform_status(self, params: dict[str, Any]) -> dict[str, Any]:
        snapshot = self._runtime.status_snapshot()
        provider_boundary = snapshot.services.get("Guardian Provider Boundary")
        gateway = self._runtime.sentinel_gateway()
        return {
            "state": snapshot.state.value,
            "runtimeHealth": snapshot.runtime_health.value,
            "providerConnected": provider_boundary.status.value if provider_boundary else "Unknown",
            "providers": list(self._runtime.configured_providers()),
            "policyEngine": type(gateway.policy_engine).__name__ if gateway is not None else None,
        }

    def _knowledge_graph(self, params: dict[str, Any]) -> dict[str, Any]:
        return knowledge_graph.build_graph()

    def _gia_status(self, params: dict[str, Any]) -> dict[str, Any]:
        snapshot = self._gia_observer.snapshot()
        return {
            "cpuPercent": snapshot.cpu_percent,
            "memoryPercent": snapshot.memory_percent,
            "memoryUsedMb": snapshot.memory_used_mb,
            "memoryTotalMb": snapshot.memory_total_mb,
            "diskPercent": snapshot.disk_percent,
            "diskUsedGb": snapshot.disk_used_gb,
            "diskTotalGb": snapshot.disk_total_gb,
            "processStatus": snapshot.process_status,
            "processUptimeSeconds": snapshot.process_uptime_seconds,
            "processCpuPercent": snapshot.process_cpu_percent,
            "processMemoryMb": snapshot.process_memory_mb,
            "engineeringToolsRunning": dict(snapshot.engineering_tools_running),
            "capturedAt": snapshot.captured_at.isoformat(),
        }

    def _memory_propose(self, params: dict[str, Any]) -> dict[str, Any]:
        content = params.get("content")
        if not isinstance(content, str):
            msg = "params.content must be a string."
            raise TypeError(msg)
        pending = self._runtime.propose_memory(content)
        return {"pendingId": pending.id, "content": pending.content}

    def _memory_approve(self, params: dict[str, Any]) -> dict[str, Any]:
        pending_id = self._require_pending_id(params)
        record = self._runtime.approve_memory(pending_id)
        return {
            "id": record.id,
            "content": record.content,
            "createdAt": record.created_at.isoformat(),
            "consentDecisionId": record.consent_decision_id,
        }

    def _memory_deny(self, params: dict[str, Any]) -> dict[str, Any]:
        pending_id = self._require_pending_id(params)
        decision = self._runtime.deny_memory(pending_id)
        return {"decisionId": decision.id, "decision": decision.decision}

    def _memory_list(self, params: dict[str, Any]) -> dict[str, Any]:
        records = self._runtime.list_memory()
        return {
            "records": [
                {
                    "id": record.id,
                    "content": record.content,
                    "createdAt": record.created_at.isoformat(),
                    "consentDecisionId": record.consent_decision_id,
                }
                for record in records
            ]
        }

    @staticmethod
    def _require_pending_id(params: dict[str, Any]) -> str:
        pending_id = params.get("pendingId")
        if not isinstance(pending_id, str):
            msg = "params.pendingId must be a string."
            raise TypeError(msg)
        return pending_id

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
        except Exception as exc:  # noqa: BLE001 - any handler failure must become a JSON-RPC error reply, not crash the loop
            # Deliberately expose only the exception type and message, matching
            # the same rationale as OpenAIProvider/GeminiProvider - never let a
            # raw internal error leak more than necessary into a client-facing
            # channel, while still being diagnostically useful.
            return self._error(request_id, INTERNAL_ERROR, f"{type(exc).__name__}: {exc}")

        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": {"code": code, "message": message}}

    def _write_line(self, out_stream: TextIO, payload: dict[str, Any]) -> None:
        """Write one JSON-RPC line to out_stream, holding the shared write lock only
        for the write itself - never across a sleep or other blocking operation."""

        with self._write_lock:
            out_stream.write(json.dumps(payload) + "\n")
            out_stream.flush()

    def _heartbeat_loop(self, out_stream: TextIO, stop_event: threading.Event) -> None:
        """Periodically emit a system.heartbeat JSON-RPC notification (no `id` key -
        the JSON-RPC 2.0 signal distinguishing a notification from a response) until
        stop_event is set. Runs as a daemon thread; does not hold the write lock
        while waiting between heartbeats."""

        while not stop_event.wait(self._heartbeat_interval_seconds):
            notification = {
                "jsonrpc": JSONRPC_VERSION,
                "method": "system.heartbeat",
                "params": {"timestamp": datetime.now(UTC).isoformat()},
            }
            self._write_line(out_stream, notification)

    def serve_forever(self, in_stream: TextIO | None = None, out_stream: TextIO | None = None) -> None:
        """Read one JSON-RPC request per line from in_stream, writing responses to
        out_stream, while a background thread periodically writes heartbeat
        notifications to the same stream (EIP-ESR0031-002)."""

        in_stream = in_stream if in_stream is not None else sys.stdin
        out_stream = out_stream if out_stream is not None else sys.stdout

        stop_heartbeat = threading.Event()
        heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(out_stream, stop_heartbeat),
            daemon=True,
            name="jarvis-heartbeat",
        )
        heartbeat_thread.start()

        try:
            for raw_line in in_stream:
                line = raw_line.strip()
                if not line:
                    continue
                response = self.handle_line(line)
                if response is not None:
                    self._write_line(out_stream, response)
        finally:
            stop_heartbeat.set()


def run() -> None:
    """Entry point: build the default runtime and serve JSON-RPC over stdio until stdin closes."""

    runtime = build_default_runtime()
    server = StdioRpcServer(runtime)
    try:
        server.serve_forever()
    finally:
        runtime.stop()
