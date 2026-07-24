"""Guardian runtime foundation."""

import logging
from collections.abc import Mapping
from types import MappingProxyType

from jarvis.guardian.config import GuardianRuntimeConfig
from jarvis.guardian.diagnostics import GuardianDiagnosticEvent
from jarvis.guardian.state import GuardianRuntimeState
from jarvis.guardian.status import GuardianRuntimeStatus
from jarvis.interfaces.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from jarvis.memory.service import PendingMemoryRequest, PersonalMemoryService
from jarvis.memory.store import ConsentDecisionRecord, PersonalMemoryRecord
from jarvis.services import JarvisService, ServiceHealth, ServiceStatus

logger = logging.getLogger(__name__)

NOT_CONNECTED_RESPONSE = "Guardian has no conversation provider connected."
NOT_RUNNING_RESPONSE = "Guardian runtime is not running."
NO_MEMORY_SERVICE_RESPONSE = "Guardian has no memory service connected."


class GuardianRuntime:
    """Minimum executable runtime boundary for Guardian."""

    def __init__(
        self,
        config: GuardianRuntimeConfig | None = None,
        conversation_provider: ConversationProvider | None = None,
        memory_service: PersonalMemoryService | None = None,
    ) -> None:
        self._config = config or GuardianRuntimeConfig()
        self._conversation_provider = conversation_provider
        self._memory_service = memory_service
        self._state = GuardianRuntimeState.STOPPED
        provider_capabilities = (
            ("guardian.conversation",)
            if conversation_provider is not None
            else ("future-provider-selection",)
        )
        self._services: dict[str, JarvisService] = {
            "Guardian Runtime": JarvisService(
                name="Guardian Runtime",
                status=ServiceStatus.OFFLINE,
                health=ServiceHealth.UNKNOWN,
                capabilities=("guardian.lifecycle", "guardian.diagnostics"),
            ),
            "Guardian Memory Boundary": JarvisService(
                name="Guardian Memory Boundary",
                status=ServiceStatus.UNAVAILABLE,
                health=ServiceHealth.UNKNOWN,
                capabilities=("future-guardian-memory",),
            ),
            "Guardian Provider Boundary": JarvisService(
                name="Guardian Provider Boundary",
                status=ServiceStatus.UNAVAILABLE,
                health=ServiceHealth.UNKNOWN,
                capabilities=provider_capabilities,
            ),
        }
        self._diagnostics: list[GuardianDiagnosticEvent] = [
            GuardianDiagnosticEvent(
                name="guardian.initialised",
                state=self._state,
                message="Guardian runtime foundation initialised.",
                health=self._runtime_health(),
            )
        ]

    @property
    def config(self) -> GuardianRuntimeConfig:
        """Return Guardian runtime configuration."""

        return self._config

    def start(self) -> GuardianRuntimeState:
        """Start the Guardian runtime foundation without enabling future intelligence."""

        self._state = GuardianRuntimeState.STARTING
        self._record("guardian.starting", "Guardian runtime foundation starting.")
        runtime_service = self._services["Guardian Runtime"]
        runtime_service.status = ServiceStatus.ONLINE
        runtime_service.health = ServiceHealth.HEALTHY
        if self._conversation_provider is not None:
            provider_service = self._services["Guardian Provider Boundary"]
            provider_service.status = ServiceStatus.ONLINE
            provider_service.health = ServiceHealth.HEALTHY
            self._record(
                "guardian.provider_connected",
                f"Guardian provider boundary connected: {self._conversation_provider.name}.",
            )
        if self._memory_service is not None:
            memory_service = self._services["Guardian Memory Boundary"]
            memory_service.status = ServiceStatus.ONLINE
            memory_service.health = ServiceHealth.HEALTHY
            self._record(
                "guardian.memory_connected",
                "Guardian memory boundary connected: Personal Memory service.",
            )
        self._state = GuardianRuntimeState.RUNNING
        self._record("guardian.running", "Guardian runtime foundation running.")
        logger.info("Guardian runtime foundation started.")
        return self._state

    def stop(self) -> GuardianRuntimeState:
        """Stop the Guardian runtime foundation."""

        self._services["Guardian Runtime"].stop()
        if self._conversation_provider is not None:
            self._services["Guardian Provider Boundary"].stop()
        if self._memory_service is not None:
            self._services["Guardian Memory Boundary"].stop()
        self._state = GuardianRuntimeState.STOPPED
        self._record("guardian.stopped", "Guardian runtime foundation stopped.")
        logger.info("Guardian runtime foundation stopped.")
        return self._state

    def status(self) -> GuardianRuntimeState:
        """Return the current Guardian runtime state."""

        return self._state

    def converse(self, message: str) -> ConversationResponse:
        """Route a message through the connected conversation provider.

        Returns a boundary response, rather than raising, when no provider is
        connected or the runtime is not running - matching this codebase's
        existing pattern of returning an honest message instead of a hidden
        failure (see `SentinelGatedConversationProvider`).
        """

        if self._conversation_provider is None:
            return ConversationResponse(message=NOT_CONNECTED_RESPONSE, provider="guardian-boundary")
        if self._state is not GuardianRuntimeState.RUNNING:
            return ConversationResponse(message=NOT_RUNNING_RESPONSE, provider="guardian-boundary")
        return self._conversation_provider.generate(ConversationRequest(message=message))

    def propose_memory(self, content: str) -> PendingMemoryRequest:
        """Propose retaining `content` as a Personal Memory item.

        Raises RuntimeError naming the unavailable boundary when no memory
        service is connected, or when the runtime is not RUNNING - mirroring
        both of `converse()`'s boundary checks, not just the first (Engineering
        Reviewer post-commit finding on the initial implementation, which
        checked service connectivity but never runtime state, letting a
        connected-but-not-started runtime propose/approve/list memory).
        Unlike `converse()`, there is no single response envelope shared
        across propose/approve/deny/list, so the boundary condition is
        surfaced as an explicit, clearly-named exception rather than a
        sentinel return value - `stdio_rpc.py`'s existing generic exception
        handler already turns this into an honest, never-hidden JSON-RPC
        error, the same "not silently masked" outcome `converse()`'s pattern
        achieves by other means.
        """

        self._require_memory_service()
        return self._memory_service.propose(content)

    def approve_memory(self, pending_id: str) -> PersonalMemoryRecord:
        """Approve a pending memory-retention request."""

        self._require_memory_service()
        return self._memory_service.approve(pending_id)

    def deny_memory(self, pending_id: str) -> ConsentDecisionRecord:
        """Deny a pending memory-retention request."""

        self._require_memory_service()
        return self._memory_service.deny(pending_id)

    def list_memory(self) -> tuple[PersonalMemoryRecord, ...]:
        """Return all stored Personal Memory records."""

        self._require_memory_service()
        return self._memory_service.list_records()

    def _require_memory_service(self) -> None:
        if self._memory_service is None:
            raise RuntimeError(NO_MEMORY_SERVICE_RESPONSE)
        if self._state is not GuardianRuntimeState.RUNNING:
            raise RuntimeError(NOT_RUNNING_RESPONSE)

    def register_service(self, service: JarvisService) -> JarvisService:
        """Register or replace a Guardian runtime service."""

        if not service.name.strip():
            msg = "Guardian service name must not be empty."
            raise ValueError(msg)
        self._services[service.name] = service
        self._record(
            "guardian.service_registered",
            f"Guardian service registered: {service.name}.",
        )
        return service

    def services(self) -> Mapping[str, JarvisService]:
        """Return Guardian runtime services."""

        return MappingProxyType(dict(self._services))

    def configured_providers(self) -> tuple[str, ...]:
        """Return the names of providers currently eligible to serve conversation
        requests, in route order, if the connected provider exposes that
        information; empty otherwise."""

        if self._conversation_provider is None:
            return ()
        getter = getattr(self._conversation_provider, "configured_providers", None)
        if getter is None:
            return ()
        return tuple(getter())

    def sentinel_gateway(self):
        """Return the connected Sentinel trust gateway, if the connected provider
        exposes one; None otherwise."""

        if self._conversation_provider is None:
            return None
        return getattr(self._conversation_provider, "gateway", None)

    def diagnostics(
        self,
        *,
        name: str | None = None,
        limit: int | None = None,
    ) -> tuple[GuardianDiagnosticEvent, ...]:
        """Return Guardian runtime diagnostic events."""

        diagnostics: tuple[GuardianDiagnosticEvent, ...] = tuple(self._diagnostics)
        if name is not None:
            diagnostics = tuple(event for event in diagnostics if event.name == name)
        if limit is not None:
            if limit < 1:
                msg = "Guardian diagnostic query limit must be greater than zero."
                raise ValueError(msg)
            diagnostics = diagnostics[-limit:]
        return diagnostics

    def events(self, *, limit: int | None = None) -> tuple[GuardianDiagnosticEvent, ...]:
        """Return timestamped Guardian runtime events."""

        return self.diagnostics(limit=limit)

    def lifecycle_history(self) -> tuple[GuardianDiagnosticEvent, ...]:
        """Return timestamped Guardian lifecycle events."""

        lifecycle_events = {
            "guardian.initialised",
            "guardian.starting",
            "guardian.running",
            "guardian.stopped",
        }
        return tuple(
            event for event in self._diagnostics if event.name in lifecycle_events
        )

    def status_snapshot(self) -> GuardianRuntimeStatus:
        """Return a structured Guardian runtime status snapshot."""

        return GuardianRuntimeStatus.from_runtime(
            state=self._state,
            runtime_health=self._runtime_health(),
            runtime_name=self._config.runtime_name,
            persistence_enabled=self._config.persistence_enabled,
            diagnostics_enabled=self._config.diagnostics_enabled,
            services=self._services,
            diagnostics=self.diagnostics(),
        )

    def _record(self, name: str, message: str) -> GuardianDiagnosticEvent:
        event = GuardianDiagnosticEvent(
            name=name,
            state=self._state,
            message=message,
            health=self._runtime_health(),
        )
        self._diagnostics.append(event)
        return event

    def _runtime_health(self) -> ServiceHealth:
        return self._services["Guardian Runtime"].health
