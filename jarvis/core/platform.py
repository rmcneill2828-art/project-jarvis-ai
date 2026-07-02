"""JARVIS platform foundation bootstrap and status boundary."""

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping

from jarvis.services import (
    CapabilityDescriptor,
    CapabilityRegistry,
    JarvisService,
    ServiceHealth,
    ServiceStatus,
)


class PlatformBootstrapState(Enum):
    """Supported platform bootstrap states."""

    NOT_BOOTSTRAPPED = "Not bootstrapped"
    BOOTSTRAPPED = "Bootstrapped"


@dataclass(frozen=True)
class ServiceHealthSummary:
    """Snapshot of service status and health."""

    name: str
    status: ServiceStatus
    health: ServiceHealth


@dataclass(frozen=True)
class PlatformStatus:
    """Snapshot of platform availability, bootstrap state and service health."""

    available: bool
    bootstrap_state: PlatformBootstrapState
    registered_capabilities: tuple[CapabilityDescriptor, ...]
    service_health: Mapping[str, ServiceHealthSummary]


class PlatformFoundation:
    """Small service boundary for JARVIS platform foundation state."""

    def __init__(self, registry: CapabilityRegistry | None = None) -> None:
        self._bootstrap_state = PlatformBootstrapState.NOT_BOOTSTRAPPED
        self._registry = registry or CapabilityRegistry()
        self._register_foundation_capabilities()

    def bootstrap(self, services: Mapping[str, JarvisService]) -> PlatformStatus:
        """Initialise the platform foundation without starting future runtime behaviour."""

        self._bootstrap_state = PlatformBootstrapState.BOOTSTRAPPED
        return self.status(services)

    def status(self, services: Mapping[str, JarvisService]) -> PlatformStatus:
        """Return current platform foundation status."""

        service_health = {
            name: ServiceHealthSummary(
                name=name,
                status=service.status,
                health=service.health,
            )
            for name, service in services.items()
        }
        return PlatformStatus(
            available=self._bootstrap_state is PlatformBootstrapState.BOOTSTRAPPED,
            bootstrap_state=self._bootstrap_state,
            registered_capabilities=self._registry.list_capabilities(),
            service_health=MappingProxyType(service_health),
        )

    @property
    def registry(self) -> CapabilityRegistry:
        """Return the foundation capability registry."""

        return self._registry

    def _register_foundation_capabilities(self) -> None:
        foundation_capabilities = (
            CapabilityDescriptor(
                name="platform.bootstrap",
                summary="Initialise the platform foundation boundary.",
                status="Foundation",
            ),
            CapabilityDescriptor(
                name="platform.status",
                summary="Report platform bootstrap and service health state.",
                status="Foundation",
            ),
            CapabilityDescriptor(
                name="capability.registry",
                summary="Register and list capability descriptors without execution.",
                status="Foundation",
            ),
            CapabilityDescriptor(
                name="conversation.workspace",
                summary="Existing deterministic Conversation Workspace integration.",
                status="Available",
            ),
            CapabilityDescriptor(
                name="future.platform-services",
                summary="Placeholder boundary for future Platform Services.",
            ),
        )
        for descriptor in foundation_capabilities:
            self._registry.register(descriptor)