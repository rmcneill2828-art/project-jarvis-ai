"""Static status model for the Guardian desktop platform shell."""

from dataclasses import dataclass
from enum import Enum


class GuardianShellState(Enum):
    """Allowed desktop shell capability states."""

    AVAILABLE = "Available"
    PLACEHOLDER = "Placeholder"
    NOT_IMPLEMENTED = "Not Implemented"
    OFFLINE = "Offline"
    UNKNOWN = "Unknown"


@dataclass(frozen=True)
class GuardianShellCapability:
    """Describe a desktop shell capability without executing it."""

    name: str
    state: GuardianShellState
    summary: str
    extends_guardian: bool = False


@dataclass(frozen=True)
class GuardianShellStatus:
    """Static status payload for the Guardian-led desktop shell."""

    guardian_message: str
    platform_message: str
    capabilities: tuple[GuardianShellCapability, ...]

    def capability_names(self) -> tuple[str, ...]:
        """Return capability names in display order."""

        return tuple(capability.name for capability in self.capabilities)


def build_guardian_shell_status() -> GuardianShellStatus:
    """Build the desktop shell status model without external services."""

    return GuardianShellStatus(
        guardian_message="Guardian interface initialised.",
        platform_message="JARVIS Platform is preparing core services.",
        capabilities=(
            GuardianShellCapability(
                name="Guardian Interface",
                state=GuardianShellState.AVAILABLE,
                summary="Primary trusted user-facing companion shell.",
            ),
            GuardianShellCapability(
                name="Sentinel Gateway",
                state=GuardianShellState.PLACEHOLDER,
                summary="Trust gateway placeholder before Platform Services.",
            ),
            GuardianShellCapability(
                name="Platform Services",
                state=GuardianShellState.PLACEHOLDER,
                summary="Future service boundary placeholder.",
            ),
            GuardianShellCapability(
                name="Memory",
                state=GuardianShellState.NOT_IMPLEMENTED,
                summary="Persistent memory is outside this package.",
            ),
            GuardianShellCapability(
                name="Providers",
                state=GuardianShellState.OFFLINE,
                summary="No provider integrations are connected.",
            ),
            GuardianShellCapability(
                name="Agent Framework",
                state=GuardianShellState.PLACEHOLDER,
                summary="Future specialists extend Guardian without separate AI identities.",
                extends_guardian=True,
            ),
            GuardianShellCapability(
                name="Diagnostics",
                state=GuardianShellState.AVAILABLE,
                summary="Static implementation boundary diagnostics.",
            ),
        ),
    )