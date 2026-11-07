"""Consent for a Child profile to ask Claude (ESR-0061 WP6c, EIP-ESR0061-006
C1, C2, 6.6).

Claude for a Child is **off by default**. It is on for one Child profile only
while all of these hold, checked on every offer and every send:

* an Administrator recorded consent (`record`), with the PIN set;
* the child then acknowledged it themselves (`acknowledge`), in plain words;
* nobody has revoked it (`revoke`), and
* the Administrator who gave it is still an Administrator profile here, so a
  consent never outlives the person who gave it.

What it covers is fixed (`SCOPE`): the question and the recent conversation,
which may contain the child's name (Programme Sponsor decision, 7 November
2026: disclosed, not scrubbed). Never the child's notes: memory sharing with
Claude cannot be turned on for a Child at all.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from jarvis.identity.store import ProfileStore

SCOPE = "question_and_recent_conversation"


@dataclass(frozen=True)
class ConsentRecord:
    profile_id: str
    consented_by: str
    scope: str
    recorded_at: str
    acknowledged_at: str | None


class ChildConsentStore:
    def __init__(self, store: ProfileStore, clock: Callable[[], datetime] | None = None) -> None:
        self._store = store
        self._clock = clock or (lambda: datetime.now(UTC))

    def current(self, profile_id: str) -> ConsentRecord | None:
        """The profile's unrevoked consent, or None."""

        with self._store.transaction() as connection:
            row = connection.execute(
                "SELECT profile_id, consented_by, scope, recorded_at, acknowledged_at FROM child_consents "
                "WHERE profile_id = ? AND revoked_at IS NULL ORDER BY id DESC LIMIT 1",
                (profile_id,),
            ).fetchone()
        return None if row is None else ConsentRecord(*row)

    def record(self, profile_id: str, consented_by: str) -> ConsentRecord:
        """A new consent, not yet acknowledged. Recording again while one is
        current keeps the current one (and its acknowledgement)."""

        with self._store.write_transaction() as connection:
            existing = connection.execute(
                "SELECT 1 FROM child_consents WHERE profile_id = ? AND revoked_at IS NULL", (profile_id,)
            ).fetchone()
            if existing is None:
                connection.execute(
                    "INSERT INTO child_consents (profile_id, consented_by, scope, recorded_at) VALUES (?, ?, ?, ?)",
                    (profile_id, consented_by, SCOPE, self._clock().isoformat()),
                )
        record = self.current(profile_id)
        assert record is not None
        return record

    def acknowledge(self, profile_id: str) -> bool:
        """The child's own acknowledgement of the current consent. False when
        there is no current consent to acknowledge."""

        with self._store.write_transaction() as connection:
            current = connection.execute(
                "SELECT 1 FROM child_consents WHERE profile_id = ? AND revoked_at IS NULL", (profile_id,)
            ).fetchone()
            connection.execute(
                "UPDATE child_consents SET acknowledged_at = ? "
                "WHERE profile_id = ? AND revoked_at IS NULL AND acknowledged_at IS NULL",
                (self._clock().isoformat(), profile_id),
            )
        return current is not None

    def revoke(self, profile_id: str) -> int:
        with self._store.write_transaction() as connection:
            return connection.execute(
                "UPDATE child_consents SET revoked_at = ? WHERE profile_id = ? AND revoked_at IS NULL",
                (self._clock().isoformat(), profile_id),
            ).rowcount

    def history(self, profile_id: str) -> list[dict[str, str | None]]:
        """Every consent row for the profile, oldest first, revoked ones
        included: for the profile's own export (ESR-0061 session-wide review,
        Medium M1)."""

        with self._store.transaction() as connection:
            rows = connection.execute(
                "SELECT consented_by, scope, recorded_at, acknowledged_at, revoked_at FROM child_consents "
                "WHERE profile_id = ? ORDER BY id",
                (profile_id,),
            ).fetchall()
        return [
            {"consentedBy": row[0], "scope": row[1], "recordedAt": row[2], "acknowledgedAt": row[3], "revokedAt": row[4]}
            for row in rows
        ]

    def delete_for_profile(self, profile_id: str) -> int:
        with self._store.transaction() as connection:
            return connection.execute("DELETE FROM child_consents WHERE profile_id = ?", (profile_id,)).rowcount
