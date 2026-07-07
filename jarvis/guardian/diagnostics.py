"""Guardian runtime diagnostic primitives."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from jarvis.guardian.state import GuardianRuntimeState
from jarvis.services import ServiceHealth


@dataclass(frozen=True)
class GuardianDiagnosticEvent:
    """Record a lightweight Guardian runtime diagnostic event."""

    name: str
    state: GuardianRuntimeState
    message: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    health: ServiceHealth = ServiceHealth.UNKNOWN

    def __post_init__(self) -> None:
        if not self.name.strip():
            msg = "Guardian diagnostic event name must not be empty."
            raise ValueError(msg)
        if not self.message.strip():
            msg = "Guardian diagnostic event message must not be empty."
            raise ValueError(msg)
        if self.occurred_at.tzinfo is None:
            msg = "Guardian diagnostic event timestamp must be timezone-aware."
            raise ValueError(msg)
