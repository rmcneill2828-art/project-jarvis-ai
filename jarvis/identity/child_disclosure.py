"""The Child's first-use explanation (ESR-0061 WP6d, EIP-ESR0061-006 D1, 6.7).

A Child profile is shown a short plain-language page the first time it is
used: JARVIS is an AI, not a person; it can make mistakes; what it keeps and
what a grown-up can see. The child says they understand once, and that is
recorded here (when, never anything else). The permanent "You are talking to
JARVIS, an AI" line stays on every conversation regardless.

The page is a disclosure, not a safety control: moderation (WP6b) is what
protects a child's conversation, and it runs whether or not the page has
been acknowledged.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from jarvis.identity.store import ProfileStore


class ChildDisclosureStore:
    def __init__(self, store: ProfileStore, clock: Callable[[], datetime] | None = None) -> None:
        self._store = store
        self._clock = clock or (lambda: datetime.now(UTC))

    def acknowledged_at(self, profile_id: str) -> str | None:
        with self._store.transaction() as connection:
            row = connection.execute(
                "SELECT acknowledged_at FROM child_disclosures WHERE profile_id = ?", (profile_id,)
            ).fetchone()
        return None if row is None else str(row[0])

    def acknowledge(self, profile_id: str) -> str:
        """Record the acknowledgement; a second one keeps the first time."""

        with self._store.write_transaction() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO child_disclosures (profile_id, acknowledged_at) VALUES (?, ?)",
                (profile_id, self._clock().isoformat()),
            )
            row = connection.execute(
                "SELECT acknowledged_at FROM child_disclosures WHERE profile_id = ?", (profile_id,)
            ).fetchone()
        return str(row[0])

    def delete_for_profile(self, profile_id: str) -> int:
        with self._store.transaction() as connection:
            return connection.execute("DELETE FROM child_disclosures WHERE profile_id = ?", (profile_id,)).rowcount
