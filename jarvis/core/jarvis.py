"""JARVIS root object and lifecycle orchestration."""

from enum import Enum
from types import MappingProxyType
from typing import Mapping

from jarvis.services import JarvisService, ServiceHealth, ServiceStatus


class JarvisState(Enum):
    """Supported lifecycle states for the JARVIS platform."""

    STOPPED = "STOPPED"
    RUNNING = "RUNNING"


class Jarvis:
    """Root orchestrator for the JARVIS platform."""

    def __init__(self) -> None:
        self._state = JarvisState.STOPPED
        self._services: dict[str, JarvisService] = {
            "Core": JarvisService(
                name="Core",
                status=ServiceStatus.ONLINE,
                health=ServiceHealth.HEALTHY,
                capabilities=("lifecycle", "conversation-routing", "service-status"),
            ),
            "Memory": JarvisService(
                name="Memory",
                status=ServiceStatus.UNAVAILABLE,
                capabilities=("basic-conversation-context",),
            ),
            "Voice": JarvisService(
                name="Voice",
                status=ServiceStatus.UNAVAILABLE,
                capabilities=("future-voice-input",),
            ),
            "Vision": JarvisService(
                name="Vision",
                status=ServiceStatus.UNAVAILABLE,
                capabilities=("future-visual-understanding",),
            ),
            "Internet": JarvisService(
                name="Internet",
                status=ServiceStatus.OFFLINE,
                capabilities=("future-online-assistance",),
            ),
        }

    def start(self) -> JarvisState:
        """Start the platform."""

        self._state = JarvisState.RUNNING
        return self._state

    def stop(self) -> JarvisState:
        """Stop the platform."""

        self._state = JarvisState.STOPPED
        return self._state

    def status(self) -> JarvisState:
        """Return the current platform state."""

        return self._state

    def register_service(self, name: str, status: ServiceStatus) -> None:
        """Register or update a service status."""

        if not name.strip():
            msg = "Service name must not be empty."
            raise ValueError(msg)

        existing_service = self._services.get(name)
        if existing_service is None:
            self._services[name] = JarvisService(name=name, status=status)
        else:
            existing_service.status = status

    def service_statuses(self) -> Mapping[str, ServiceStatus]:
        """Return current service statuses."""

        return MappingProxyType(
            {name: service.status for name, service in self._services.items()}
        )

    def services(self) -> Mapping[str, JarvisService]:
        """Return current service models."""

        return MappingProxyType(dict(self._services))
