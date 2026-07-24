"""JARVIS root object and lifecycle orchestration."""

from collections.abc import Mapping
from enum import Enum
from types import MappingProxyType

from jarvis.core.platform import PlatformFoundation, PlatformStatus
from jarvis.guardian import GuardianRuntime
from jarvis.services import JarvisService, ServiceHealth, ServiceStatus


class JarvisState(Enum):
    """Supported lifecycle states for the JARVIS platform."""

    STOPPED = "STOPPED"
    RUNNING = "RUNNING"


class Jarvis:
    """Root orchestrator for the JARVIS platform."""

    def __init__(self) -> None:
        self._state = JarvisState.STOPPED
        self._platform = PlatformFoundation()
        self._guardian_runtime = GuardianRuntime()
        self._services: dict[str, JarvisService] = {
            "Core": JarvisService(
                name="Core",
                status=ServiceStatus.ONLINE,
                health=ServiceHealth.HEALTHY,
                capabilities=("lifecycle", "conversation-routing", "service-status"),
            ),
            "Conversation": JarvisService(
                name="Conversation",
                status=ServiceStatus.ONLINE,
                health=ServiceHealth.HEALTHY,
                capabilities=("deterministic-local-provider", "session-transcript"),
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

        self._guardian_runtime.start()
        self.bootstrap_platform()
        self._state = JarvisState.RUNNING
        return self._state

    def stop(self) -> JarvisState:
        """Stop the platform."""

        self._guardian_runtime.stop()
        self._state = JarvisState.STOPPED
        return self._state

    def status(self) -> JarvisState:
        """Return the current platform state."""

        return self._state

    def bootstrap_platform(self) -> PlatformStatus:
        """Bootstrap the platform foundation boundary."""

        return self._platform.bootstrap(self._platform_services())

    def platform_status(self) -> PlatformStatus:
        """Return the current platform foundation status."""

        return self._platform.status(self._platform_services())

    def guardian_runtime(self) -> GuardianRuntime:
        """Return the Guardian runtime owned by the JARVIS lifecycle."""

        return self._guardian_runtime

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
            {name: service.status for name, service in self._platform_services().items()}
        )

    def services(self) -> Mapping[str, JarvisService]:
        """Return current service models."""

        return MappingProxyType(self._platform_services())

    def _platform_services(self) -> dict[str, JarvisService]:
        services = dict(self._services)
        services.update(self._guardian_runtime.services())
        return services
