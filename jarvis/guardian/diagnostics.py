"""Guardian runtime diagnostic primitives."""

from dataclasses import dataclass

from jarvis.guardian.state import GuardianRuntimeState


@dataclass(frozen=True)
class GuardianDiagnosticEvent:
    """Record a lightweight Guardian runtime diagnostic event."""

    name: str
    state: GuardianRuntimeState
    message: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            msg = "Guardian diagnostic event name must not be empty."
            raise ValueError(msg)
        if not self.message.strip():
            msg = "Guardian diagnostic event message must not be empty."
            raise ValueError(msg)
