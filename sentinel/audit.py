"""Sentinel audit trail: records what Sentinel decided and executed, and why."""

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Protocol


@dataclass(frozen=True)
class AuditEvent:
    """A single Sentinel audit event."""

    event_type: str
    outcome: str
    summary: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            msg = "Audit event type must not be empty."
            raise ValueError(msg)
        if not self.outcome.strip():
            msg = "Audit event outcome must not be empty."
            raise ValueError(msg)
        if not self.summary.strip():
            msg = "Audit event summary must not be empty."
            raise ValueError(msg)
        if self.recorded_at.tzinfo is None:
            msg = "Audit event timestamp must be timezone-aware."
            raise ValueError(msg)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of this event."""

        return {
            "event_type": self.event_type,
            "outcome": self.outcome,
            "summary": self.summary,
            "metadata": dict(self.metadata),
            "recorded_at": self.recorded_at.isoformat(),
        }


class AuditRecorder(Protocol):
    """Protocol implemented by Sentinel audit recorders."""

    def record(self, event: AuditEvent) -> None:
        """Record an audit event."""

    def events(self) -> tuple[AuditEvent, ...]:
        """Return recorded audit events, oldest first."""


class MemoryAuditRecorder:
    """In-memory audit recorder. Lost on process restart."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        self._events.append(event)

    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)


class JsonAuditRecorder:
    """Append-only JSONL audit recorder. One JSON object per line."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def record(self, event: AuditEvent) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.as_dict()) + "\n")

    def events(self) -> tuple[AuditEvent, ...]:
        if not self._path.exists():
            return ()

        events: list[AuditEvent] = []
        with self._path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                events.append(
                    AuditEvent(
                        event_type=data["event_type"],
                        outcome=data["outcome"],
                        summary=data["summary"],
                        metadata=data.get("metadata", {}),
                        recorded_at=datetime.fromisoformat(data["recorded_at"]),
                    )
                )
        return tuple(events)
