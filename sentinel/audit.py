"""Sentinel audit trail: records what Sentinel decided and executed, and why."""

import json
import logging
import os
import threading
from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import MappingProxyType
from typing import Protocol


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


# Default bound on in-memory audit events (EBG-0144, ESR-0059 WP8/WP9): the
# oldest are dropped past this, so a long-running process cannot grow
# without limit. Durable history belongs in JsonAuditRecorder.
DEFAULT_MAX_MEMORY_EVENTS = 1_000


class MemoryAuditRecorder:
    """In-memory audit recorder, keeping the most recent `max_events`. Lost on
    process restart - production uses `JsonAuditRecorder` (EBG-0144)."""

    def __init__(self, max_events: int = DEFAULT_MAX_MEMORY_EVENTS) -> None:
        if max_events < 1:
            msg = "Audit recorder max_events must be at least one."
            raise ValueError(msg)
        self._events: deque[AuditEvent] = deque(maxlen=max_events)

    def record(self, event: AuditEvent) -> None:
        self._events.append(event)

    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PruneResult:
    """What a retention prune did, as counts only."""

    removed: int
    kept: int
    unreadable_kept: int


# Rotation defaults for the durable audit log (EBG-0144, ESR-0059 WP9).
DEFAULT_AUDIT_MAX_BYTES = 5_000_000
DEFAULT_AUDIT_BACKUP_COUNT = 3


class JsonAuditRecorder:
    """Append-only JSONL audit recorder. One JSON object per line.

    Rotates when the file reaches `max_bytes`: `audit.jsonl` becomes
    `audit.jsonl.1`, older copies shift up, and anything beyond
    `backup_count` is removed - so the trail survives restarts without
    growing without limit (EBG-0144, ESR-0059 WP9). Writes and rotation are
    serialised by a lock, since the backend records from more than one
    thread (EBG-0139). `events()` reads the current file only.
    """

    def __init__(
        self,
        path: Path,
        max_bytes: int = DEFAULT_AUDIT_MAX_BYTES,
        backup_count: int = DEFAULT_AUDIT_BACKUP_COUNT,
    ) -> None:
        if max_bytes < 1 or backup_count < 0:
            msg = "Audit log max_bytes must be positive and backup_count not negative."
            raise ValueError(msg)
        self._path = path
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._lock = threading.Lock()

    def record(self, event: AuditEvent) -> None:
        line = json.dumps(event.as_dict()) + "\n"
        with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            if self._path.exists() and self._path.stat().st_size + len(line.encode("utf-8")) > self._max_bytes:
                self._rotate()
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(line)

    def _rotate(self) -> None:
        oldest = self._path.with_name(f"{self._path.name}.{self._backup_count}")
        if self._backup_count == 0:
            self._path.unlink()
            return
        if oldest.exists():
            oldest.unlink()
        for index in range(self._backup_count - 1, 0, -1):
            source = self._path.with_name(f"{self._path.name}.{index}")
            if source.exists():
                source.replace(self._path.with_name(f"{self._path.name}.{index + 1}"))
        self._path.replace(self._path.with_name(f"{self._path.name}.1"))

    def events(self) -> tuple[AuditEvent, ...]:
        # Under the same lock as writing, rotating and pruning, so a reader
        # never sees a file half way through being replaced (WP5b).
        with self._lock:
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

    def prune_older_than(self, days: int, *, now: datetime | None = None) -> PruneResult:
        """Remove events recorded more than `days` days ago (ESR-0061 WP5b,
        EIP-ESR0061-005 6.4), from the live file and from every rotated copy.

        Takes the recorder's own lock, so it cannot interleave with a write or
        a rotation. Each file is rewritten to a temporary file in the same
        directory and swapped in with `os.replace`, so a crash leaves either the
        old file or the new one. A line whose time cannot be read is KEPT and
        counted: a prune must not destroy a record it cannot judge. A rotated
        copy left with nothing in it is deleted.
        """

        if days < 1:
            msg = "Audit retention must be at least one day."
            raise ValueError(msg)
        cutoff = (now or datetime.now(UTC)) - timedelta(days=days)
        removed = kept = unreadable = 0
        with self._lock:
            paths = [self._path] + [
                self._path.with_name(f"{self._path.name}.{index}") for index in range(1, self._backup_count + 1)
            ]
            for path in paths:
                if not path.exists():
                    continue
                keep_lines: list[str] = []
                file_removed = 0
                with path.open("r", encoding="utf-8") as handle:
                    for raw in handle:
                        line = raw.strip()
                        if not line:
                            continue
                        recorded_at = _line_time(line)
                        if recorded_at is None:
                            unreadable += 1
                            keep_lines.append(line)
                        elif recorded_at < cutoff:
                            file_removed += 1
                        else:
                            keep_lines.append(line)
                removed += file_removed
                kept += len(keep_lines)
                if file_removed == 0:
                    continue
                if not keep_lines:
                    path.unlink()
                    continue
                temporary = path.with_name(f"{path.name}.prune")
                temporary.write_text("\n".join(keep_lines) + "\n", encoding="utf-8")
                os.replace(temporary, path)
        logger.info("Audit retention: %d removed, %d kept, %d unreadable kept.", removed, kept, unreadable)
        return PruneResult(removed=removed, kept=kept, unreadable_kept=unreadable)


def _line_time(line: str) -> datetime | None:
    """The recorded time of one audit line, or None if it cannot be read."""

    try:
        stamp = datetime.fromisoformat(json.loads(line)["recorded_at"])
    except (ValueError, KeyError, TypeError):
        return None
    return stamp if stamp.tzinfo is not None else stamp.replace(tzinfo=UTC)
