"""Lightweight service model for JARVIS OS."""

from dataclasses import dataclass, field

from jarvis.services.status import ServiceHealth, ServiceStatus


@dataclass
class JarvisService:
    """Represent a JARVIS service and its current operating state."""

    name: str
    status: ServiceStatus = ServiceStatus.UNAVAILABLE
    health: ServiceHealth = ServiceHealth.UNKNOWN
    capabilities: tuple[str, ...] = field(default_factory=tuple)

    def start(self) -> None:
        """Start the service where lightweight startup is supported."""

        self.status = ServiceStatus.ONLINE
        self.health = ServiceHealth.HEALTHY

    def stop(self) -> None:
        """Stop the service where lightweight shutdown is supported."""

        self.status = ServiceStatus.OFFLINE
        self.health = ServiceHealth.UNKNOWN

    def supports(self, capability: str) -> bool:
        """Return whether the service reports a capability."""

        return capability in self.capabilities
