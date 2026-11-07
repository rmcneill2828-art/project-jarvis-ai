"""The household's Administrator PIN (ESR-0061 WP6a, EIP-ESR0061-006 P1, 6.1).

One PIN per household, held only as an `hashlib.scrypt` hash with a random
salt in the identity database. It is compared in constant time and is never
logged, returned or placed in an error message.

Wrong tries are rate limited: after 5 wrong tries in a row the PIN is refused
for 30 seconds, doubling with each further batch of 5, up to 10 minutes. The
count and the lock time are stored, so restarting JARVIS does not reset them.
While locked, a PIN is not even checked, so a lock-out cannot be guessed
through.

A child can therefore delay the Administrator by guessing. The design accepts
that and makes it visible: the wrong tries are counted for the next
Administrator sign-in, which is told how many there were and when the last one
was (`take_notices`). Setting the PIN and resetting it from the command line
(`jarvis/tools/reset_admin_pin.py`) are recorded the same way.

What a PIN is not: it stops someone switching up inside the app. It is not a
defence against a person who can open the computer's files (EIP-ESR0061-006
Section 7).
"""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from jarvis.identity.store import ProfileStore
from jarvis.shared.errors import ClientFacingPermissionError, ClientFacingValueError

PIN_PATTERN = re.compile(r"[0-9]{6,12}")
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SALT_BYTES = 16
HASH_BYTES = 32
TRIES_PER_BATCH = 5
FIRST_LOCK_SECONDS = 30
MAX_LOCK_SECONDS = 600

NOTICE_SET = "pinSet"
NOTICE_RESET = "pinReset"
NOTICE_WRONG_TRIES = "wrongTries"

# Fixed wording: a refusal never echoes what was typed.
PIN_SHAPE_MESSAGE = "The PIN must be 6 to 12 digits."
WRONG_PIN_MESSAGE = "That PIN is not right."


def lock_seconds_for(failed_count: int) -> int:
    """How long a lock-out lasts after `failed_count` wrong tries in a row, or
    0 when this try does not start one. 5 tries give 30 seconds, 10 give 60,
    15 give 120, and so on, never more than 10 minutes."""

    if failed_count <= 0 or failed_count % TRIES_PER_BATCH != 0:
        return 0
    batch = failed_count // TRIES_PER_BATCH
    return min(FIRST_LOCK_SECONDS * 2 ** (batch - 1), MAX_LOCK_SECONDS)


def validate_pin_shape(pin: object) -> str:
    """The PIN as given, if it is 6 to 12 ASCII digits; otherwise a fixed
    refusal that does not repeat the input."""

    if not isinstance(pin, str) or PIN_PATTERN.fullmatch(pin) is None:
        raise ClientFacingValueError(PIN_SHAPE_MESSAGE)
    return pin


def _hash(pin: str, salt: bytes, n: int, r: int, p: int) -> bytes:
    return hashlib.scrypt(pin.encode("ascii"), salt=salt, n=n, r=r, p=p, dklen=HASH_BYTES)


def _iso(moment: datetime) -> str:
    return moment.isoformat()


def _parse(value: str | None) -> datetime | None:
    return None if value is None else datetime.fromisoformat(value)


LOCKED_MESSAGE_START = "Too many wrong tries."


def _locked_refusal(seconds: int) -> ClientFacingPermissionError:
    """Refused because of the lock-out; says how long to wait. A plain
    `ClientFacingPermissionError`, so the reply reads "PermissionError: ..."
    like every other refusal (`public_type_name`)."""

    refusal = ClientFacingPermissionError(f"{LOCKED_MESSAGE_START} Try again in {seconds} seconds.")
    refusal.locked_for_seconds = seconds  # type: ignore[attr-defined]
    return refusal


def _wrong_pin_refusal(locked_for_seconds: int) -> ClientFacingPermissionError:
    """Refused because the PIN did not match. The message is fixed and never
    repeats what was typed; it says when this try started a lock-out."""

    if locked_for_seconds:
        message = f"{WRONG_PIN_MESSAGE} Too many wrong tries: try again in {locked_for_seconds} seconds."
    else:
        message = f"{WRONG_PIN_MESSAGE} Try again."
    refusal = ClientFacingPermissionError(message)
    refusal.locked_for_seconds = locked_for_seconds  # type: ignore[attr-defined]
    return refusal


@dataclass(frozen=True)
class PinStatus:
    is_set: bool
    locked_for_seconds: int

    def to_payload(self) -> dict[str, Any]:
        return {
            "set": self.is_set,
            "locked": self.locked_for_seconds > 0,
            "lockedForSeconds": self.locked_for_seconds,
        }


class AdminPin:
    """The household PIN over the identity database's `admin_pin` table."""

    def __init__(self, store: ProfileStore, clock: Callable[[], datetime] | None = None) -> None:
        self._store = store
        self._clock = clock or (lambda: datetime.now(UTC))

    def _locked_for(self, locked_until: str | None, now: datetime) -> int:
        until = _parse(locked_until)
        if until is None or until <= now:
            return 0
        # Round up, so "0 seconds" is never shown while still locked.
        return max(1, int((until - now).total_seconds() + 0.999))

    def status(self) -> PinStatus:
        with self._store.transaction() as connection:
            row = connection.execute("SELECT locked_until FROM admin_pin WHERE id = 1").fetchone()
        if row is None:
            return PinStatus(is_set=False, locked_for_seconds=0)
        return PinStatus(is_set=True, locked_for_seconds=self._locked_for(row[0], self._clock()))

    def is_set(self) -> bool:
        return self.status().is_set

    def set_first(self, pin: object, set_by_name: str) -> None:
        """Set the household's first PIN. Refused if one is already set (it is
        then changed with `change`, which needs the current PIN)."""

        validated = validate_pin_shape(pin)
        salt = secrets.token_bytes(SALT_BYTES)
        digest = _hash(validated, salt, SCRYPT_N, SCRYPT_R, SCRYPT_P)
        now = self._clock()
        with self._store.write_transaction() as connection:
            if connection.execute("SELECT 1 FROM admin_pin WHERE id = 1").fetchone() is not None:
                msg = "A PIN is already set. Change it with the current PIN."
                raise ClientFacingValueError(msg)
            connection.execute(
                """
                INSERT INTO admin_pin (id, salt, pin_hash, scrypt_n, scrypt_r, scrypt_p, set_at)
                VALUES (1, ?, ?, ?, ?, ?, ?)
                """,
                (salt, digest, SCRYPT_N, SCRYPT_R, SCRYPT_P, _iso(now)),
            )
            connection.execute(
                "INSERT INTO pin_notices (kind, at, detail) VALUES (?, ?, ?)",
                (NOTICE_SET, _iso(now), set_by_name),
            )

    def verify(self, pin: object) -> None:
        """Return quietly if `pin` is the household PIN; otherwise refuse and
        count the try. Refused without checking while a lock-out runs. Assumes
        a PIN is set (callers check `is_set` first); with none set every PIN
        is refused."""

        now = self._clock()
        with self._store.write_transaction() as connection:
            row = connection.execute(
                """
                SELECT salt, pin_hash, scrypt_n, scrypt_r, scrypt_p, failed_count, locked_until
                FROM admin_pin WHERE id = 1
                """
            ).fetchone()
            if row is None:
                raise _wrong_pin_refusal(0)
            salt, stored, n, r, p, failed_count, locked_until = row
            waiting = self._locked_for(locked_until, now)
            if waiting:
                raise _locked_refusal(waiting)
            matches = (
                isinstance(pin, str)
                and PIN_PATTERN.fullmatch(pin) is not None
                and hmac.compare_digest(_hash(pin, salt, n, r, p), stored)
            )
            if matches:
                connection.execute("UPDATE admin_pin SET failed_count = 0, locked_until = NULL WHERE id = 1")
                return
            failed_count += 1
            lock = lock_seconds_for(failed_count)
            connection.execute(
                """
                UPDATE admin_pin
                SET failed_count = ?, locked_until = ?, wrong_since_signin = wrong_since_signin + 1,
                    last_wrong_at = ?
                WHERE id = 1
                """,
                (failed_count, _iso(now + timedelta(seconds=lock)) if lock else None, _iso(now)),
            )
        # Raised after the transaction commits, so the count is kept.
        raise _wrong_pin_refusal(lock)

    def change(self, current_pin: object, new_pin: object) -> None:
        """Replace the PIN. The current PIN is checked (and counted) first."""

        validated = validate_pin_shape(new_pin)
        self.verify(current_pin)
        salt = secrets.token_bytes(SALT_BYTES)
        digest = _hash(validated, salt, SCRYPT_N, SCRYPT_R, SCRYPT_P)
        with self._store.write_transaction() as connection:
            connection.execute(
                """
                UPDATE admin_pin
                SET salt = ?, pin_hash = ?, scrypt_n = ?, scrypt_r = ?, scrypt_p = ?, set_at = ?
                WHERE id = 1
                """,
                (salt, digest, SCRYPT_N, SCRYPT_R, SCRYPT_P, _iso(self._clock())),
            )

    def reset(self) -> bool:
        """Remove the PIN (the command-line reset, P5) and leave a notice for
        the next Administrator sign-in. Returns whether a PIN was removed."""

        with self._store.write_transaction() as connection:
            removed = connection.execute("DELETE FROM admin_pin WHERE id = 1").rowcount > 0
            if removed:
                connection.execute(
                    "INSERT INTO pin_notices (kind, at, detail) VALUES (?, ?, NULL)",
                    (NOTICE_RESET, _iso(self._clock())),
                )
        return removed

    def take_notices(self) -> list[dict[str, Any]]:
        """What the Administrator signing in must be told, oldest first, then
        forgotten: the PIN was set (and from which profile), the PIN was reset,
        and how many wrong tries there were since the last such sign-in."""

        with self._store.write_transaction() as connection:
            rows = connection.execute("SELECT kind, at, detail FROM pin_notices ORDER BY id").fetchall()
            connection.execute("DELETE FROM pin_notices")
            wrong = connection.execute("SELECT wrong_since_signin, last_wrong_at FROM admin_pin WHERE id = 1").fetchone()
            connection.execute("UPDATE admin_pin SET wrong_since_signin = 0, last_wrong_at = NULL WHERE id = 1")
        notices: list[dict[str, Any]] = []
        for kind, at, detail in rows:
            notice: dict[str, Any] = {"kind": kind, "at": at}
            if kind == NOTICE_SET:
                notice["byProfile"] = detail
            notices.append(notice)
        if wrong is not None and wrong[0] > 0:
            notices.append({"kind": NOTICE_WRONG_TRIES, "count": wrong[0], "at": wrong[1]})
        return notices
