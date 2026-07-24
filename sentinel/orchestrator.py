"""Sentinel provider orchestration and resilience primitives."""

from dataclasses import dataclass
from enum import Enum

from sentinel.audit import AuditEvent, AuditRecorder, MemoryAuditRecorder
from sentinel.core import SentinelResponse
from sentinel.providers import (
    ExecutionProvider,
    ProviderRequest,
    ProviderResponse,
    execute_with_sentinel_decision,
)


class ProviderHealth(Enum):
    """Provider runtime health states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"


@dataclass(frozen=True)
class ProviderRoute:
    """Ordered provider route for a capability."""

    capability: str
    providers: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability.strip():
            msg = "Provider route capability must not be empty."
            raise ValueError(msg)
        if not self.providers:
            msg = "Provider route must contain at least one provider."
            raise ValueError(msg)
        if any(not provider.strip() for provider in self.providers):
            msg = "Provider route provider names must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class ProviderExecutionRecord:
    """Record of a Sentinel provider orchestration attempt."""

    capability: str
    attempted_providers: tuple[str, ...]
    selected_provider: str | None
    succeeded: bool
    reason: str


@dataclass(frozen=True)
class OrchestratedProviderResponse:
    """Provider response with orchestration metadata."""

    provider_response: ProviderResponse
    execution_record: ProviderExecutionRecord


class ProviderOrchestrator:
    """Health-aware Sentinel provider orchestrator with failover."""

    def __init__(self, audit_recorder: AuditRecorder | None = None) -> None:
        self._providers: dict[str, ExecutionProvider] = {}
        self._health: dict[str, ProviderHealth] = {}
        self._routes: dict[str, ProviderRoute] = {}
        self._history: list[ProviderExecutionRecord] = []
        self._audit_recorder = audit_recorder or MemoryAuditRecorder()

    def register_provider(
        self,
        provider: ExecutionProvider,
        health: ProviderHealth = ProviderHealth.HEALTHY,
    ) -> ExecutionProvider:
        """Register or replace a provider and its health state."""

        if not provider.name.strip():
            msg = "Execution provider name must not be empty."
            raise ValueError(msg)
        if not provider.capabilities:
            msg = "Execution provider must expose at least one capability."
            raise ValueError(msg)
        self._providers[provider.name] = provider
        self._health[provider.name] = health
        return provider

    def set_health(self, provider_name: str, health: ProviderHealth) -> None:
        """Set provider health."""

        if provider_name not in self._providers:
            msg = f"Provider is not registered: {provider_name}."
            raise LookupError(msg)
        self._health[provider_name] = health

    def health(self, provider_name: str) -> ProviderHealth:
        """Return provider health."""

        if provider_name not in self._providers:
            msg = f"Provider is not registered: {provider_name}."
            raise LookupError(msg)
        return self._health[provider_name]

    def register_route(self, route: ProviderRoute) -> ProviderRoute:
        """Register an ordered route for a capability."""

        for provider_name in route.providers:
            if provider_name not in self._providers:
                msg = f"Provider route references unregistered provider: {provider_name}."
                raise LookupError(msg)
            if route.capability not in self._providers[provider_name].capabilities:
                msg = (
                    f"Provider {provider_name} does not support capability: "
                    f"{route.capability}."
                )
                raise ValueError(msg)
        self._routes[route.capability] = route
        return route

    def eligible_providers(self, capability: str) -> tuple[ExecutionProvider, ...]:
        """Return healthy or degraded providers eligible for a capability."""

        if not capability.strip():
            msg = "Provider capability must not be empty."
            raise ValueError(msg)

        if capability in self._routes:
            provider_names = self._routes[capability].providers
        else:
            provider_names = tuple(
                provider.name
                for provider in self._providers.values()
                if capability in provider.capabilities
            )

        return tuple(
            self._providers[name]
            for name in provider_names
            if self._health[name] in (ProviderHealth.HEALTHY, ProviderHealth.DEGRADED)
        )

    def execute(
        self,
        sentinel_response: SentinelResponse,
        request: ProviderRequest,
    ) -> OrchestratedProviderResponse:
        """Execute a provider request using route order and failover."""

        attempted: list[str] = []
        last_error: Exception | None = None

        for provider in self.eligible_providers(request.capability):
            attempted.append(provider.name)
            try:
                provider_response = execute_with_sentinel_decision(
                    sentinel_response,
                    provider,
                    request,
                )
            except Exception as exc:  # noqa: BLE001 - any provider failure must fail over, not just known exception types
                last_error = exc
                self._health[provider.name] = ProviderHealth.DEGRADED
                continue

            record = ProviderExecutionRecord(
                capability=request.capability,
                attempted_providers=tuple(attempted),
                selected_provider=provider.name,
                succeeded=True,
                reason="Provider execution succeeded.",
            )
            self._history.append(record)
            self._audit_recorder.record(
                AuditEvent(
                    event_type="provider_execution",
                    outcome="succeeded",
                    summary=(
                        f"Provider {provider.name} executed capability "
                        f"{request.capability}."
                    ),
                    metadata={
                        "capability": request.capability,
                        "selected_provider": provider.name,
                        "attempted_providers": ",".join(attempted),
                    },
                )
            )
            return OrchestratedProviderResponse(
                provider_response=provider_response,
                execution_record=record,
            )

        reason = "No healthy provider could execute the request."
        if last_error is not None:
            reason = f"Provider execution failed: {last_error}"
        record = ProviderExecutionRecord(
            capability=request.capability,
            attempted_providers=tuple(attempted),
            selected_provider=None,
            succeeded=False,
            reason=reason,
        )
        self._history.append(record)
        self._audit_recorder.record(
            AuditEvent(
                event_type="provider_execution",
                outcome="failed",
                summary=reason,
                metadata={
                    "capability": request.capability,
                    "attempted_providers": ",".join(attempted),
                },
            )
        )
        raise RuntimeError(reason)

    def history(self) -> tuple[ProviderExecutionRecord, ...]:
        """Return provider orchestration history."""

        return tuple(self._history)

    def audit_events(self) -> tuple[AuditEvent, ...]:
        """Return recorded Sentinel audit events."""

        return self._audit_recorder.events()
