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
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from jarvis.shared.schema_migrations import apply_migrations

# Schema history (EBG-0147, ESR-0059 WP12). Migration N brings the schema to
# version N; append new migrations, never edit a released one. Migration 1
# is the original ESR-0027 schema, `IF NOT EXISTS` so it is safe on existing
# installations created before versioning.
PERSONAL_MEMORY_MIGRATIONS: tuple[tuple[str, ...], ...] = (
    (
        """
        CREATE TABLE IF NOT EXISTS personal_memory (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            consent_decision_id TEXT NOT NULL
        )
        """,
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
        """,
    ),
    # 2 (EBG-0132, ESR-0059 WP13): the profile a memory belongs to. NULL is
    # a shared household note, visible to every profile - which every memory
    # saved before profile scoping becomes, by the Programme Sponsor's
    # decision.
    ("ALTER TABLE personal_memory ADD COLUMN profile_id TEXT",),
)


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
    # The owning profile, or None for a shared household note (EBG-0132).
    profile_id: str | None = None


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
        apply_migrations(db_path, PERSONAL_MEMORY_MIGRATIONS, "Personal Memory")

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
        """Add a Personal Memory record.

        Enforces MDS-0001 Section 7.4's durable-traceability guarantee at the
        storage layer itself, not only by caller discipline: `record` is
        rejected unless `consent_decision_id` refers to a `consent_decisions`
        row already recorded with `decision == "approved"`. Without this, the
        store's public API let any caller insert an orphan record whose
        `consent_decision_id` pointed at nothing real (Engineering Reviewer
        post-commit finding - `PersonalMemoryService.approve()` happened to
        call `record_decision()` before `add()` in the right order, but
        nothing in the store itself required that ordering).

        Both the existence check and the insert happen inside the same
        transaction/connection to avoid a check-then-insert race.
        """

        with self._transaction() as connection:
            row = connection.execute(
                "SELECT decision FROM consent_decisions WHERE id = ?",
                (record.consent_decision_id,),
            ).fetchone()
            if row is None or row[0] != "approved":
                msg = (
                    f"Cannot add Personal Memory record {record.id!r}: consent_decision_id "
                    f"{record.consent_decision_id!r} does not reference a recorded approved decision."
                )
                raise ValueError(msg)
            connection.execute(
                """
                INSERT INTO personal_memory (id, content, created_at, consent_decision_id, profile_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.content,
                    record.created_at.isoformat(),
                    record.consent_decision_id,
                    record.profile_id,
                ),
            )
        return record

    def list_all(self) -> tuple[PersonalMemoryRecord, ...]:
        """Return all stored Personal Memory records, every profile's."""

        with self._transaction() as connection:
            rows = connection.execute(f"SELECT {_RECORD_COLUMNS} FROM personal_memory ORDER BY created_at").fetchall()
        return tuple(_record_from_row(row) for row in rows)

    def list_visible(self, profile_id: str | None) -> tuple[PersonalMemoryRecord, ...]:
        """Return the records `profile_id` may see: its own plus shared
        household notes. With no profile, household notes only (EBG-0132)."""

        with self._transaction() as connection:
            rows = connection.execute(
                f"SELECT {_RECORD_COLUMNS} FROM personal_memory "
                "WHERE profile_id IS NULL OR profile_id = ? ORDER BY created_at",
                (profile_id,),
            ).fetchall()
        return tuple(_record_from_row(row) for row in rows)

    def count_visible(self, profile_id: str | None) -> int:
        """Return how many records `profile_id` may see (see list_visible)."""

        with self._transaction() as connection:
            row = connection.execute(
                "SELECT COUNT(*) FROM personal_memory WHERE profile_id IS NULL OR profile_id = ?",
                (profile_id,),
            ).fetchone()
        return int(row[0])

    def reassign_unknown_owners(self, known_profile_ids: set[str], new_owner: str) -> int:
        """Give every memory whose owning profile is not in `known_profile_ids`
        to `new_owner`; return how many were moved. Shared household notes
        (no owner) are untouched (EBG-0132, ESR-0059 WP13)."""

        with self._transaction() as connection:
            rows = connection.execute(
                "SELECT id, profile_id FROM personal_memory WHERE profile_id IS NOT NULL"
            ).fetchall()
            orphaned = [row[0] for row in rows if row[1] not in known_profile_ids]
            connection.executemany(
                "UPDATE personal_memory SET profile_id = ? WHERE id = ?",
                [(new_owner, record_id) for record_id in orphaned],
            )
        return len(orphaned)

    def get(self, record_id: str) -> PersonalMemoryRecord | None:
        """Return one record by id, or None."""

        with self._transaction() as connection:
            row = connection.execute(
                f"SELECT {_RECORD_COLUMNS} FROM personal_memory WHERE id = ?", (record_id,)
            ).fetchone()
        return None if row is None else _record_from_row(row)

    def count(self) -> int:
        """Return the number of stored Personal Memory records.

        EBG-0131 (Memory Management UXP Surface): a dedicated `COUNT(*)`
        query rather than `len(list_all())` - the backup/restore panel only
        ever needs the number of records, not their content, and pulling
        every record's real content across the RPC boundary just to display
        a count would be a needless privacy exposure for what this surface
        actually shows.
        """

        with self._transaction() as connection:
            row = connection.execute("SELECT COUNT(*) FROM personal_memory").fetchone()
        return int(row[0])

    def export_snapshot(self) -> dict[str, tuple[dict[str, str | None], ...]]:
        """Return every row in both tables as plain, JSON-serialisable dicts.

        EBG-0023 (Backup, Recovery and Data Protection): exports
        `consent_decisions` alongside `personal_memory`, never the latter
        alone - flattening to personal-memory content only would discard
        MDS-0001 Section 7.4's per-item consent traceability, turning a
        durable audit trail into an orphaned pile of text on restore. This
        is a full point-in-time export, not a partial or incremental one;
        BRD-0001 records why that is the deliberate scope for this
        increment (no incremental/differential backup yet).
        """

        with self._transaction() as connection:
            memory_rows = connection.execute(
                f"SELECT {_RECORD_COLUMNS} FROM personal_memory ORDER BY created_at"
            ).fetchall()
            decision_rows = connection.execute(
                """
                SELECT id, capability, decision, decided_at, approver_label,
                       sentinel_outcome, sentinel_category, sentinel_reason
                FROM consent_decisions ORDER BY decided_at
                """
            ).fetchall()
        return {
            "personal_memory": tuple(
                {
                    "id": row[0],
                    "content": row[1],
                    "created_at": row[2],
                    "consent_decision_id": row[3],
                    "profile_id": row[4],
                }
                for row in memory_rows
            ),
            "consent_decisions": tuple(
                {
                    "id": row[0],
                    "capability": row[1],
                    "decision": row[2],
                    "decided_at": row[3],
                    "approver_label": row[4],
                    "sentinel_outcome": row[5],
                    "sentinel_category": row[6],
                    "sentinel_reason": row[7],
                }
                for row in decision_rows
            ),
        }

    def import_snapshot(self, snapshot: dict, *, confirm_overwrite: bool = False) -> int:
        """Restore both tables from a snapshot dict shaped like
        `export_snapshot()`'s return value (BRD-0001 Section 6, EBG-0023).

        Implements BRD-0001 Section 6's three minimum requirements:

        1. Validates the snapshot's structure before writing anything - a
           malformed or truncated backup fails closed (raises ValueError),
           never partially imports. Since ESR-0059 WP1 this includes field
           types, parseable timestamps, and that every content row is
           backed by an *approved* (not merely present) consent decision.
        2. Inserts `consent_decisions` rows before their dependent
           `personal_memory` rows, in the same transaction, mirroring
           `add()`'s own insert-order constraint.
        3. Refuses to proceed if the store is already non-empty unless
           `confirm_overwrite=True` is passed explicitly - recovery is
           destructive and must never run silently.

        Restore is wipe-then-replace, not merge: a non-empty store's
        existing rows are deleted before the snapshot is written, never
        combined with it. Returns the number of `personal_memory` records
        restored.
        """

        if not isinstance(snapshot, dict) or "personal_memory" not in snapshot or "consent_decisions" not in snapshot:
            msg = "Invalid backup snapshot: expected a dict with 'personal_memory' and 'consent_decisions' keys."
            raise ValueError(msg)

        memory_rows = snapshot["personal_memory"]
        decision_rows = snapshot["consent_decisions"]
        # Accepts both: a JSON-decoded backup file yields lists, while
        # export_snapshot()'s own direct return value (its own tuples,
        # deliberately immutable) is also a valid snapshot - both call
        # paths are genuine, not just the file round trip.
        if not isinstance(memory_rows, list | tuple) or not isinstance(decision_rows, list | tuple):
            msg = "Invalid backup snapshot: 'personal_memory' and 'consent_decisions' must both be lists."
            raise ValueError(msg)  # noqa: TRY004 - ValueError is import_snapshot()'s established invalid-backup contract

        decision_ids: set[str] = set()
        approved_decision_ids: set[str] = set()
        for row in decision_rows:
            required = {"id", "capability", "decision", "decided_at", "approver_label", "sentinel_outcome", "sentinel_reason"}
            if not isinstance(row, dict) or not required.issubset(row):
                msg = f"Invalid backup snapshot: consent_decisions row missing required fields: {row!r}"
                raise ValueError(msg)
            _require_text_fields(row, ("id", "capability", "decision", "approver_label", "sentinel_outcome"), "consent_decisions")
            if not isinstance(row["sentinel_reason"], str):
                msg = f"Invalid backup snapshot: consent_decisions row {row['id']!r} has a non-text sentinel_reason."
                raise ValueError(msg)  # noqa: TRY004 - ValueError is import_snapshot()'s established invalid-backup contract
            if row.get("sentinel_category") is not None and not isinstance(row["sentinel_category"], str):
                msg = f"Invalid backup snapshot: consent_decisions row {row['id']!r} has a non-text sentinel_category."
                raise ValueError(msg)
            if row["decision"] not in ("approved", "denied"):
                msg = (
                    f"Invalid backup snapshot: consent_decisions row {row['id']!r} has decision "
                    f"{row['decision']!r} (expected 'approved' or 'denied')."
                )
                raise ValueError(msg)
            _require_timestamp(row, "decided_at", "consent_decisions")
            decision_ids.add(row["id"])
            if row["decision"] == "approved":
                approved_decision_ids.add(row["id"])

        for row in memory_rows:
            required = {"id", "content", "created_at", "consent_decision_id"}
            if not isinstance(row, dict) or not required.issubset(row):
                msg = f"Invalid backup snapshot: personal_memory row missing required fields: {row!r}"
                raise ValueError(msg)
            _require_text_fields(row, ("id", "content", "consent_decision_id"), "personal_memory")
            # Optional (EBG-0132): backups made before profile scoping have no
            # profile_id and restore as shared household notes.
            owner = row.get("profile_id")
            if owner is not None and (not isinstance(owner, str) or not owner.strip()):
                msg = f"Invalid backup snapshot: personal_memory row {row['id']!r} has an invalid profile_id."
                raise ValueError(msg)
            _require_timestamp(row, "created_at", "personal_memory")
            if row["consent_decision_id"] not in decision_ids:
                msg = (
                    f"Invalid backup snapshot: personal_memory row {row['id']!r} references "
                    f"consent_decision_id {row['consent_decision_id']!r}, not present among the "
                    "snapshot's own consent_decisions - refusing a partial/inconsistent import."
                )
                raise ValueError(msg)
            # ESR-0059 WP1: the same guarantee `add()` enforces for live
            # writes - content is only ever retained against an *approved*
            # decision. Checking presence alone let a backup restore content
            # the user had explicitly denied, which then reached every
            # conversation turn's system prompt via the Cognitive Core.
            if row["consent_decision_id"] not in approved_decision_ids:
                msg = (
                    f"Invalid backup snapshot: personal_memory row {row['id']!r} references "
                    f"consent_decision_id {row['consent_decision_id']!r}, which is not an approved "
                    "decision - refusing to restore content without recorded consent."
                )
                raise ValueError(msg)

        with self._transaction() as connection:
            existing = connection.execute("SELECT COUNT(*) FROM personal_memory").fetchone()[0]
            existing += connection.execute("SELECT COUNT(*) FROM consent_decisions").fetchone()[0]
            if existing and not confirm_overwrite:
                msg = (
                    "Store is not empty: restoring would overwrite existing data. "
                    "Pass confirm_overwrite=True to proceed - recovery never runs silently."
                )
                raise ValueError(msg)

            if existing:
                connection.execute("DELETE FROM personal_memory")
                connection.execute("DELETE FROM consent_decisions")

            for row in decision_rows:
                connection.execute(
                    """
                    INSERT INTO consent_decisions
                        (id, capability, decision, decided_at, approver_label,
                         sentinel_outcome, sentinel_category, sentinel_reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["id"],
                        row["capability"],
                        row["decision"],
                        row["decided_at"],
                        row["approver_label"],
                        row["sentinel_outcome"],
                        row.get("sentinel_category"),
                        row["sentinel_reason"],
                    ),
                )
            for row in memory_rows:
                connection.execute(
                    """
                    INSERT INTO personal_memory (id, content, created_at, consent_decision_id, profile_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (row["id"], row["content"], row["created_at"], row["consent_decision_id"], row.get("profile_id")),
                )

        return len(memory_rows)

    def delete(self, record_id: str) -> bool:
        """Delete exactly one Personal Memory record by id; return whether a
        record was actually deleted (EBG-0145, ESR-0059 WP10), so callers can
        report an unknown id honestly instead of claiming success.

        Satisfies MDS-0001 Section 7.4's per-item revocation requirement
        directly - no broader destructive operation is required or performed.
        The corresponding consent_decisions row is retained: a decision
        record for a since-deleted item is legitimate audit history, not
        something revocation should erase.
        """

        with self._transaction() as connection:
            cursor = connection.execute("DELETE FROM personal_memory WHERE id = ?", (record_id,))
            return cursor.rowcount > 0


_RECORD_COLUMNS = "id, content, created_at, consent_decision_id, profile_id"


def _record_from_row(row: tuple) -> PersonalMemoryRecord:
    return PersonalMemoryRecord(
        id=row[0],
        content=row[1],
        created_at=datetime.fromisoformat(row[2]),
        consent_decision_id=row[3],
        profile_id=row[4],
    )


def utc_now() -> datetime:
    """Return the current UTC time, timezone-aware."""

    return datetime.now(UTC)


def _require_text_fields(row: dict, fields: tuple[str, ...], table: str) -> None:
    """Reject a snapshot row whose named fields are not non-blank strings.

    ESR-0059 WP1: `import_snapshot()` previously checked only that required
    keys were present, so a restored row could carry any JSON type - and the
    first read of a malformed row failed only later, on every subsequent
    call, rather than at restore time where the backup can still be refused.
    """

    for field in fields:
        value = row[field]
        if not isinstance(value, str) or not value.strip():
            msg = f"Invalid backup snapshot: {table} row field {field!r} must be non-empty text, got {value!r}."
            raise ValueError(msg)


def _require_timestamp(row: dict, field: str, table: str) -> None:
    """Reject a snapshot row whose timestamp field would not parse on read.

    ESR-0059 WP1: `list_all()` parses `created_at` with
    `datetime.fromisoformat()` on every read, and `GuardianRuntime.converse()`
    reads memory on every turn - so a single unparseable timestamp restored
    from a backup made every later conversation request fail. Validated
    here, before any write, so a bad backup is refused instead.
    """

    value = row[field]
    if not isinstance(value, str):
        msg = f"Invalid backup snapshot: {table} row field {field!r} must be an ISO 8601 timestamp, got {value!r}."
        raise ValueError(msg)  # noqa: TRY004 - ValueError is import_snapshot()'s established invalid-backup contract
    try:
        datetime.fromisoformat(value)
    except ValueError as exc:
        msg = f"Invalid backup snapshot: {table} row field {field!r} is not a valid ISO 8601 timestamp: {value!r}."
        raise ValueError(msg) from exc
