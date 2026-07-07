"""Guardian runtime status snapshot models."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from jarvis.guardian.diagnostics import GuardianDiagnosticEvent
from jarvis.guardian.state import GuardianRuntimeState
from jarvis.services import JarvisService, ServiceHealth, ServiceStatus


@dataclass(frozen=True)
class GuardianServiceSnapshot:
    """Immutable snapshot of a Guardian runtime service."""

    name: str
    status: ServiceStatus
    health: ServiceHealth
    capabilities: tuple[str, ...]

    @classmethod
    def from_service(cls, service: JarvisService) -> "GuardianServiceSnapshot":
        """Create a Guardian service snapshot from a service model."""

        return cls(
            name=service.name,
            status=service.status,
            health=service.health,
            capabilities=tuple(service.capabilities),
        )

    def supports(self, capability: str) -> bool:
        """Return whether the service snapshot reports a capability."""

        return capability in self.capabilities


@dataclass(frozen=True)
class GuardianRuntimeStatus:
    """Structured snapshot of Guardian runtime state and diagnostics."""

    state: GuardianRuntimeState
    runtime_health: ServiceHealth
    runtime_name: str
    persistence_enabled: bool
    diagnostics_enabled: bool
    services: Mapping[str, GuardianServiceSnapshot]
    events: tuple[GuardianDiagnosticEvent, ...]
    diagnostic_count: int
    latest_diagnostic: GuardianDiagnosticEvent | None

    @classmethod
    def from_runtime(
        cls,
        *,
        state: GuardianRuntimeState,
        runtime_health: ServiceHealth,
        runtime_name: str,
        persistence_enabled: bool,
        diagnostics_enabled: bool,
        services: Mapping[str, JarvisService],
        diagnostics: tuple[GuardianDiagnosticEvent, ...],
    ) -> "GuardianRuntimeStatus":
        """Create a status snapshot from Guardian runtime internals."""

        service_snapshots = {
            name: GuardianServiceSnapshot.from_service(service)
            for name, service in services.items()
        }
        return cls(
            state=state,
            runtime_health=runtime_health,
            runtime_name=runtime_name,
            persistence_enabled=persistence_enabled,
            diagnostics_enabled=diagnostics_enabled,
            services=MappingProxyType(service_snapshots),
            events=tuple(diagnostics),
            diagnostic_count=len(diagnostics),
            latest_diagnostic=diagnostics[-1] if diagnostics else None,
        )
