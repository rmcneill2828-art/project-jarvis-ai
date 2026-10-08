"""Monthly spend ledger and cap for the cloud provider (ESR-0061 WP3b,
EIP-ESR0061-003 6.3, decision S4).

Cloud calls cost real money, so every escalation is metered *before* it is
sent and settled *after* it returns:

* `reserve()` takes the worst-case cost of the call under a lock and refuses -
  raising `SpendCapReachedError` - when what is already spent, plus what other
  in-flight calls have reserved, plus this call's worst case, would pass the
  cap;
* `settle()` replaces the reservation with the cost the provider actually
  reported (or, if it reported nothing usable, with the whole reservation:
  never an undercount);
* `release()` drops a reservation for a call that produced no bill.

A call that times out after the server began generating may still be billed
and is never seen here; the hard limit set in the provider's Console is the
backstop for that, and for this ledger being wrong.

The database holds **counts and totals only** - per calendar month (UTC):
micro-dollars spent, requests, token totals. No conversation text, no profile,
no message (D23). Amounts are integer micro-dollars, so there is no floating
point rounding in the arithmetic that decides whether a call may go ahead; one
micro-dollar per token equals one dollar per million tokens, the unit prices
are quoted in.
"""

from __future__ import annotations

import contextlib
import sqlite3
import threading
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from jarvis.shared.schema_migrations import apply_migrations, connect

SPEND_MIGRATIONS: tuple[tuple[str, ...], ...] = (
    (
        """
        CREATE TABLE IF NOT EXISTS spend (
            month TEXT PRIMARY KEY,
            spent_micro INTEGER NOT NULL DEFAULT 0,
            requests INTEGER NOT NULL DEFAULT 0,
            input_tokens INTEGER NOT NULL DEFAULT 0,
            output_tokens INTEGER NOT NULL DEFAULT 0
        )
        """,
    ),
)

MICRO_DOLLARS_PER_DOLLAR = 1_000_000
# The 80 percent warning of decision S4.
DEFAULT_WARNING_FRACTION = 0.8
# Added to the byte count of everything sent when bounding the input tokens: the
# framing the adapter wraps around retained notes, and the request's structure.
INPUT_OVERHEAD_TOKENS = 512


@dataclass(frozen=True)
class ModelPrice:
    """Micro-dollars per token, which is dollars per million tokens."""

    input_per_token: int
    output_per_token: int


# Read from the provider's published price list on 8 October 2026. Thinking is
# billed as output, so `output_tokens` from the response already includes it.
PRICE_TABLE_DATE = "2026-10-08"
PRICES: Mapping[str, ModelPrice] = {
    "claude-sonnet-5-5": ModelPrice(2, 10),
    "claude-opus-5-5": ModelPrice(4, 20),
    "claude-haiku-4-5": ModelPrice(1, 5),
}
# A model the table does not know is charged at the highest known rate, so the
# ledger overstates rather than understates what was spent.
_HIGHEST_PRICE = ModelPrice(
    max(price.input_per_token for price in PRICES.values()),
    max(price.output_per_token for price in PRICES.values()),
)


def price_for(model: str) -> ModelPrice:
    """The price of `model`, or the highest known price if it is not listed."""

    return PRICES.get(model, _HIGHEST_PRICE)


def worst_case_input_tokens(*texts: str) -> int:
    """An upper bound on the input tokens of a request made of `texts`.

    A token is at least one byte, so the UTF-8 byte count bounds the token
    count whatever the language; the overhead covers the framing around it.
    """

    return sum(len(text.encode("utf-8")) for text in texts) + INPUT_OVERHEAD_TOKENS


def worst_case_cost(model: str, input_tokens: int, max_output_tokens: int) -> int:
    """The most one call can cost, in micro-dollars."""

    price = price_for(model)
    return input_tokens * price.input_per_token + max_output_tokens * price.output_per_token


def actual_cost(model: str, usage: Mapping[str, str]) -> int | None:
    """The cost of a call from the adapter's `usage_*` metadata, in
    micro-dollars, or None when the provider reported no usable figures.

    Cache writes cost 1.25 times the input rate and cache reads 0.1 times; the
    adapter never asks for caching, so both are normally zero.
    """

    def count(key: str) -> int | None:
        raw = usage.get(f"usage_{key}")
        if raw is None:
            return None
        try:
            value = int(raw)
        except ValueError:
            return None
        return value if value >= 0 else None

    input_tokens = count("input_tokens")
    output_tokens = count("output_tokens")
    if input_tokens is None or output_tokens is None:
        return None
    cache_writes = count("cache_creation_input_tokens") or 0
    cache_reads = count("cache_read_input_tokens") or 0
    price = price_for(model)
    return (
        input_tokens * price.input_per_token
        + (cache_writes * price.input_per_token * 5 + 3) // 4
        + (cache_reads * price.input_per_token + 9) // 10
        + output_tokens * price.output_per_token
    )


class SpendCapReachedError(Exception):
    """The monthly cap would be passed by this call. Nothing was sent."""


@dataclass(frozen=True)
class Reservation:
    """A held amount for one in-flight call."""

    id: int
    month: str
    amount_micro: int


@dataclass(frozen=True)
class SpendSnapshot:
    """Where the month stands. All money in micro-dollars."""

    month: str
    spent_micro: int
    reserved_micro: int
    cap_micro: int
    requests: int
    input_tokens: int
    output_tokens: int
    warning_fraction: float

    @property
    def remaining_micro(self) -> int:
        return max(0, self.cap_micro - self.spent_micro - self.reserved_micro)

    @property
    def cap_reached(self) -> bool:
        return self.spent_micro + self.reserved_micro >= self.cap_micro

    @property
    def warning(self) -> bool:
        """True from the warning fraction of the cap onwards."""

        return self.spent_micro >= self.cap_micro * self.warning_fraction


def _utc_now() -> datetime:
    return datetime.now(UTC)


class SpendLedger:
    """SQLite-backed spend total per calendar month, with reservations."""

    def __init__(
        self,
        db_path: Path,
        cap_micro: int,
        warning_fraction: float = DEFAULT_WARNING_FRACTION,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        if cap_micro <= 0:
            msg = "The spend cap must be greater than zero."
            raise ValueError(msg)
        if not 0 < warning_fraction <= 1:
            msg = "The warning fraction must be greater than zero and at most one."
            raise ValueError(msg)
        self._db_path = db_path
        self._cap_micro = cap_micro
        self._warning_fraction = warning_fraction
        self._clock = clock
        db_path.parent.mkdir(parents=True, exist_ok=True)
        apply_migrations(db_path, SPEND_MIGRATIONS, "spend")
        # One lock covers the check-and-hold in reserve() and every update, so
        # two slow-lane threads can never both pass a cap only one fits under.
        self._lock = threading.Lock()
        self._reservations: dict[int, Reservation] = {}
        self._next_id = 1

    @property
    def cap_micro(self) -> int:
        return self._cap_micro

    def _month(self) -> str:
        return self._clock().astimezone(UTC).strftime("%Y-%m")

    @contextlib.contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        connection = connect(self._db_path)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _row(self, connection: sqlite3.Connection, month: str) -> tuple[int, int, int, int]:
        row = connection.execute(
            "SELECT spent_micro, requests, input_tokens, output_tokens FROM spend WHERE month = ?",
            (month,),
        ).fetchone()
        return (0, 0, 0, 0) if row is None else (row[0], row[1], row[2], row[3])

    def _reserved_in(self, month: str) -> int:
        return sum(item.amount_micro for item in self._reservations.values() if item.month == month)

    def snapshot(self) -> SpendSnapshot:
        """The current month's totals."""

        with self._lock:
            month = self._month()
            with self._transaction() as connection:
                spent, requests, input_tokens, output_tokens = self._row(connection, month)
            return SpendSnapshot(
                month=month,
                spent_micro=spent,
                reserved_micro=self._reserved_in(month),
                cap_micro=self._cap_micro,
                requests=requests,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                warning_fraction=self._warning_fraction,
            )

    def reserve(self, worst_case_micro: int) -> Reservation:
        """Hold `worst_case_micro` for one call, or refuse it.

        Raises `SpendCapReachedError` - holding nothing - when spent plus
        reserved plus this call would pass the cap.
        """

        if worst_case_micro < 0:
            msg = "A reservation cannot be negative."
            raise ValueError(msg)
        with self._lock:
            month = self._month()
            with self._transaction() as connection:
                spent = self._row(connection, month)[0]
            if spent + self._reserved_in(month) + worst_case_micro > self._cap_micro:
                msg = "The monthly spend cap would be passed."
                raise SpendCapReachedError(msg)
            reservation = Reservation(id=self._next_id, month=month, amount_micro=worst_case_micro)
            self._next_id += 1
            self._reservations[reservation.id] = reservation
            return reservation

    def settle(
        self,
        reservation: Reservation,
        cost_micro: int | None,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> int:
        """Replace the reservation with the real cost; return what was charged.

        `cost_micro=None` (the provider reported nothing usable) charges the
        whole reservation - the ledger never undercounts. The month charged is
        the one the call started in.
        """

        charged = reservation.amount_micro if cost_micro is None else cost_micro
        with self._lock:
            if self._reservations.pop(reservation.id, None) is None:
                msg = "This reservation was already settled or released."
                raise ValueError(msg)
            with self._transaction() as connection:
                connection.execute(
                    """
                    INSERT INTO spend (month, spent_micro, requests, input_tokens, output_tokens)
                    VALUES (?, ?, 1, ?, ?)
                    ON CONFLICT(month) DO UPDATE SET
                        spent_micro = spent_micro + excluded.spent_micro,
                        requests = requests + 1,
                        input_tokens = input_tokens + excluded.input_tokens,
                        output_tokens = output_tokens + excluded.output_tokens
                    """,
                    (reservation.month, charged, max(0, input_tokens), max(0, output_tokens)),
                )
        return charged

    def release(self, reservation: Reservation) -> None:
        """Drop a reservation for a call that produced no bill. Idempotent."""

        with self._lock:
            self._reservations.pop(reservation.id, None)
