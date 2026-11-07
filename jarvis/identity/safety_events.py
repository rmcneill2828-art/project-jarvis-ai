"""Safety events (ESR-0061 WP6b, EIP-ESR0061-006 M5).

When moderation blocks a Child's or Guest's turn, one row is kept: the
category label, whether the message or the reply was blocked, the time and the
profile. **Never the text** (D23). A parent cannot act on "an event happened",
so the profile is kept; the audit log stays free of profile ids, which is why
these live here, in the identity database, and not in the audit log.

Pruned by the same retention days as the activity log (`prune_older_than`,
registered with the retention service) and deleted with the profile on erasure.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from jarvis.identity.store import ProfileStore


class SafetyEventStore:
    def __init__(self, store: ProfileStore, clock: Callable[[], datetime] | None = None) -> None:
        self._store = store
        self._clock = clock or (lambda: datetime.now(UTC))

    def record(self, profile_id: str | None, category: str, direction: str) -> None:
        with self._store.transaction() as connection:
            connection.execute(
                "INSERT INTO safety_events (profile_id, category, direction, at) VALUES (?, ?, ?, ?)",
                (profile_id, category, direction, self._clock().isoformat()),
            )

    def list_for_profile(self, profile_id: str) -> list[dict[str, str]]:
        with self._store.transaction() as connection:
            rows = connection.execute(
                "SELECT category, direction, at FROM safety_events WHERE profile_id = ? ORDER BY id", (profile_id,)
            ).fetchall()
        return [{"category": row[0], "direction": row[1], "at": row[2]} for row in rows]

    def count(self) -> int:
        with self._store.transaction() as connection:
            return int(connection.execute("SELECT COUNT(*) FROM safety_events").fetchone()[0])

    def delete_for_profile(self, profile_id: str) -> int:
        with self._store.transaction() as connection:
            return connection.execute("DELETE FROM safety_events WHERE profile_id = ?", (profile_id,)).rowcount

    def prune_older_than(self, days: int) -> int:
        cutoff = (self._clock() - timedelta(days=days)).isoformat()
        with self._store.transaction() as connection:
            return connection.execute("DELETE FROM safety_events WHERE at < ?", (cutoff,)).rowcount
