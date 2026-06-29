"""JARVIS root object and lifecycle orchestration."""

from enum import Enum
from types import MappingProxyType
from typing import Mapping

from jarvis.services import ServiceStatus


class JarvisState(Enum):
    """Supported lifecycle states for the JARVIS platform."""

    STOPPED = "STOPPED"
    RUNNING = "RUNNING"


class Jarvis:
    """Root orchestrator for the JARVIS platform."""

    def __init__(self) -> None:
        self._state = JarvisState.STOPPED
        self._services: dict[str, ServiceStatus] = {
            "Core": ServiceStatus.ONLINE,
            "Memory": ServiceStatus.UNAVAILABLE,
            "Voice": ServiceStatus.UNAVAILABLE,
            "Vision": ServiceStatus.UNAVAILABLE,
            "Internet": ServiceStatus.OFFLINE,
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

        self._services[name] = status

    def service_statuses(self) -> Mapping[str, ServiceStatus]:
        """Return current service statuses."""

        return MappingProxyType(dict(self._services))
