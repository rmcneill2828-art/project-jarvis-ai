"""User identity/profile storage layer (GAM-0001 Section 8.1, EIP-ESR0046-001).

SQLite-backed, mirroring `jarvis/memory/store.py`'s proven `_transaction()`
pattern (commit/rollback via the connection's own context manager, explicit
close in `finally` - `jarvis/memory/store.py`'s own docstring records a real
Windows file-lock `PermissionError` this exact pattern was written to fix).

Deliberately does not implement authentication, memory scoping or role
enforcement - see EIP-ESR0046-001 Section 8. A profile here is a named,
role-tagged identity a household member selects, not a secured login.
"""

from __future__ import annotations

import contextlib
import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

HOUSEHOLD_ROLES = ("Administrator", "Adult", "Child", "Guest")

_ACTIVE_PROFILE_ROW_ID = 1


@dataclass(frozen=True)
class ProfileRecord:
    """A single local Guardian profile: a display name and a household role.

    `role` must be one of GAM-0001 Section 8.1's four Household Role Model
    values. No credential field exists here by design (EIP-ESR0046-001
    Section 8 exclusion 2).
    """

    id: str
    display_name: str
    role: str
    created_at: datetime

    def __post_init__(self) -> None:
        if self.role not in HOUSEHOLD_ROLES:
            msg = f"Profile role must be one of {HOUSEHOLD_ROLES}, got {self.role!r}."
            raise ValueError(msg)


class ProfileStore:
    """SQLite-backed store for local Guardian profiles and the active selection.

    `profiles` holds every created profile. `active_profile` is a single-row
    table recording the currently selected profile id, persisted so the
    selection survives a process restart.
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS active_profile (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    profile_id TEXT NOT NULL
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
        call, which on Windows manifests as the database file staying locked
        even after the operation returns (the same issue documented and
        fixed for the Personal Memory store, `jarvis/memory/store.py`).
        """

        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def create(self, record: ProfileRecord) -> ProfileRecord:
        """Create a new profile."""

        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO profiles (id, display_name, role, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (record.id, record.display_name, record.role, record.created_at.isoformat()),
            )
        return record

    def list_all(self) -> tuple[ProfileRecord, ...]:
        """Return every stored profile, oldest first."""

        with self._transaction() as connection:
            rows = connection.execute(
                "SELECT id, display_name, role, created_at FROM profiles ORDER BY created_at"
            ).fetchall()
        return tuple(
            ProfileRecord(
                id=row[0],
                display_name=row[1],
                role=row[2],
                created_at=datetime.fromisoformat(row[3]),
            )
            for row in rows
        )

    def get(self, profile_id: str) -> ProfileRecord | None:
        """Return a single profile by id, or None if not found."""

        with self._transaction() as connection:
            row = connection.execute(
                "SELECT id, display_name, role, created_at FROM profiles WHERE id = ?",
                (profile_id,),
            ).fetchone()
        if row is None:
            return None
        return ProfileRecord(
            id=row[0],
            display_name=row[1],
            role=row[2],
            created_at=datetime.fromisoformat(row[3]),
        )

    def set_active(self, profile_id: str) -> None:
        """Persist `profile_id` as the currently active profile.

        Does not itself validate that `profile_id` refers to an existing
        profile - callers (`ProfileService`) are responsible for that check,
        matching `PersonalMemoryStore.add()`'s existing division of
        responsibility between store-level referential-integrity checks and
        service-level business rules.
        """

        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO active_profile (id, profile_id) VALUES (?, ?)
                ON CONFLICT(id) DO UPDATE SET profile_id = excluded.profile_id
                """,
                (_ACTIVE_PROFILE_ROW_ID, profile_id),
            )

    def get_active(self) -> ProfileRecord | None:
        """Return the currently active profile, or None if none has ever been
        selected, or the previously-active profile has since been deleted.

        Deletion is not authorised by this package (EIP-ESR0046-001 Section 8
        exclusion 5), so the latter case is defensive only.
        """

        with self._transaction() as connection:
            row = connection.execute(
                "SELECT profile_id FROM active_profile WHERE id = ?",
                (_ACTIVE_PROFILE_ROW_ID,),
            ).fetchone()
        if row is None:
            return None
        return self.get(row[0])


def utc_now() -> datetime:
    """Return the current UTC time, timezone-aware."""

    return datetime.now(UTC)
