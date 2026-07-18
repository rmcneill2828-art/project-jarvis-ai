"""Personal Memory storage layer (MDS-0001 Section 6.2, EIP-ESR0027-001).

SQLite-backed, per MDS-0001 Section 7.3's initial-engine recommendation. Two
tables live in one file: `personal_memory` (the retained content itself) and
`consent_decisions` (a durable record of every propose/approve/deny outcome,
per MDS-0001 Section 7.4's per-item consent traceability requirement and the
Engineering Reviewer's Finding 1 on this package's v0.1 draft - a
PersonalMemoryRecord must trace back to a real, persisted decision, not a
transient in-memory value that disappears once resolved).
"""

from __future__ import annotations

import contextlib
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class ConsentDecisionRecord:
    """A durable record of a single memory-retention consent decision."""

    id: str
    capability: str
    decision: str
    decided_at: datetime
    approver_label: str
    sentinel_outcome: str
    sentinel_reason: str
    sentinel_category: str | None = None

    def __post_init__(self) -> None:
        if self.decision not in ("approved", "denied"):
            msg = f"Consent decision must be 'approved' or 'denied', got {self.decision!r}."
            raise ValueError(msg)


@dataclass(frozen=True)
class PersonalMemoryRecord:
    """A single retained Personal Memory item, traceable to its consent decision."""

    id: str
    content: str
    created_at: datetime
    consent_decision_id: str


class PersonalMemoryStore:
    """SQLite-backed store for Personal Memory records and consent decisions.

    The `personal_memory` table is exclusively personal-memory-shaped - no
    Session or Shared-Family data is ever written here (MDS-0001 Section 7.2's
    data-layer partitioning), and this store never shares a schema with the
    repository-backed AIEMS Knowledge Capability (MDS-0001 Section 6.4).
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS personal_memory (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    consent_decision_id TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS consent_decisions (
                    id TEXT PRIMARY KEY,
                    capability TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    decided_at TEXT NOT NULL,
                    approver_label TEXT NOT NULL,
                    sentinel_outcome TEXT NOT NULL,
                    sentinel_category TEXT,
                    sentinel_reason TEXT NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    @contextlib.contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        """Open a connection, commit/rollback via its own context manager, and
        always close it afterward.

        `sqlite3.Connection.__exit__` only commits or rolls back the
        transaction - it never closes the connection. Using `with
        self._connect() as connection:` alone leaks a file handle on every
        call; on Windows this manifests as the database file staying locked
        even after the operation returns (confirmed directly: this exact leak
        caused a `PermissionError` during this package's own live smoke check
        cleanup, before this fix).
        """

        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def record_decision(self, decision: ConsentDecisionRecord) -> ConsentDecisionRecord:
        """Durably record a consent decision (approval or denial)."""

        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO consent_decisions
                    (id, capability, decision, decided_at, approver_label,
                     sentinel_outcome, sentinel_category, sentinel_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision.id,
                    decision.capability,
                    decision.decision,
                    decision.decided_at.isoformat(),
                    decision.approver_label,
                    decision.sentinel_outcome,
                    decision.sentinel_category,
                    decision.sentinel_reason,
                ),
            )
        return decision

    def get_decision(self, decision_id: str) -> ConsentDecisionRecord | None:
        """Return a recorded consent decision by id, or None if not found."""

        with self._transaction() as connection:
            row = connection.execute(
                """
                SELECT id, capability, decision, decided_at, approver_label,
                       sentinel_outcome, sentinel_category, sentinel_reason
                FROM consent_decisions WHERE id = ?
                """,
                (decision_id,),
            ).fetchone()
        if row is None:
            return None
        return ConsentDecisionRecord(
            id=row[0],
            capability=row[1],
            decision=row[2],
            decided_at=datetime.fromisoformat(row[3]),
            approver_label=row[4],
            sentinel_outcome=row[5],
            sentinel_category=row[6],
            sentinel_reason=row[7],
        )

    def add(self, record: PersonalMemoryRecord) -> PersonalMemoryRecord:
        """Add a Personal Memory record."""

        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO personal_memory (id, content, created_at, consent_decision_id)
                VALUES (?, ?, ?, ?)
                """,
                (record.id, record.content, record.created_at.isoformat(), record.consent_decision_id),
            )
        return record

    def list_all(self) -> tuple[PersonalMemoryRecord, ...]:
        """Return all stored Personal Memory records."""

        with self._transaction() as connection:
            rows = connection.execute(
                "SELECT id, content, created_at, consent_decision_id FROM personal_memory ORDER BY created_at"
            ).fetchall()
        return tuple(
            PersonalMemoryRecord(
                id=row[0],
                content=row[1],
                created_at=datetime.fromisoformat(row[2]),
                consent_decision_id=row[3],
            )
            for row in rows
        )

    def delete(self, record_id: str) -> None:
        """Delete exactly one Personal Memory record by id.

        Satisfies MDS-0001 Section 7.4's per-item revocation requirement
        directly - no broader destructive operation is required or performed.
        The corresponding consent_decisions row is retained: a decision
        record for a since-deleted item is legitimate audit history, not
        something revocation should erase.
        """

        with self._transaction() as connection:
            connection.execute("DELETE FROM personal_memory WHERE id = ?", (record_id,))


def utc_now() -> datetime:
    """Return the current UTC time, timezone-aware."""

    return datetime.now(UTC)
