"""Tests for the monthly spend ledger (ESR-0061 WP3b, EIP-ESR0061-003 6.3, decision S4)."""

import sqlite3
import threading
from datetime import UTC, datetime

import pytest

from jarvis.shared.spend_ledger import (
    INPUT_OVERHEAD_TOKENS,
    PRICES,
    ModelPrice,
    SpendCapReachedError,
    SpendLedger,
    actual_cost,
    price_for,
    worst_case_cost,
    worst_case_input_tokens,
)


class _Clock:
    def __init__(self, when: datetime) -> None:
        self.when = when

    def __call__(self) -> datetime:
        return self.when


def _ledger(tmp_path, cap=1_000, **kwargs) -> SpendLedger:
    return SpendLedger(tmp_path / "spend.db", cap_micro=cap, **kwargs)


# --- prices -------------------------------------------------------------------------------------------------------


def test_the_default_model_is_priced_at_two_and_ten_dollars_per_million_tokens():
    assert price_for("claude-sonnet-5-5") == ModelPrice(2, 10)


def test_an_unknown_model_is_priced_at_the_highest_known_rate():
    """Fail towards overstating: an unlisted model must never look cheaper than
    the dearest one the table knows."""

    unknown = price_for("claude-something-new")

    assert unknown.input_per_token == max(price.input_per_token for price in PRICES.values())
    assert unknown.output_per_token == max(price.output_per_token for price in PRICES.values())


def test_one_micro_dollar_per_token_is_one_dollar_per_million_tokens():
    assert worst_case_cost("claude-sonnet-5-5", 1_000_000, 0) == 2_000_000
    assert worst_case_cost("claude-sonnet-5-5", 0, 1_000_000) == 10_000_000


# --- bounds and actual cost ---------------------------------------------------------------------------------------


def test_the_input_bound_counts_utf8_bytes_so_non_english_text_cannot_exceed_it():
    text = "日本語のテキスト😀"

    assert worst_case_input_tokens(text) == len(text.encode("utf-8")) + INPUT_OVERHEAD_TOKENS
    assert worst_case_input_tokens(text) > len(text) + INPUT_OVERHEAD_TOKENS - 1


def test_a_worst_case_turn_at_the_defaults_costs_about_three_cents():
    """The design's figure (6.3): the largest message, notes and history the RPC
    layer allows, plus the default output cap."""

    largest_input = worst_case_input_tokens("x" * 4_000, "x" * 1_500, *("x" * 400 for _ in range(12)), "x" * 2_000)

    cost = worst_case_cost("claude-sonnet-5-5", largest_input, 1_024)

    assert 10_000 < cost < 40_000


def test_actual_cost_prices_input_and_output_from_the_usage_figures():
    usage = {"usage_input_tokens": "1000", "usage_output_tokens": "500"}

    assert actual_cost("claude-sonnet-5-5", usage) == 1000 * 2 + 500 * 10


def test_actual_cost_prices_cache_writes_at_one_and_a_quarter_and_reads_at_a_tenth():
    usage = {
        "usage_input_tokens": "0",
        "usage_output_tokens": "0",
        "usage_cache_creation_input_tokens": "1000",
        "usage_cache_read_input_tokens": "1000",
    }

    assert actual_cost("claude-sonnet-5-5", usage) == 2500 + 200


@pytest.mark.parametrize(
    "usage",
    [
        {},
        {"usage_input_tokens": "10"},
        {"usage_output_tokens": "10"},
        {"usage_input_tokens": "ten", "usage_output_tokens": "10"},
        {"usage_input_tokens": "-1", "usage_output_tokens": "10"},
    ],
)
def test_actual_cost_is_none_when_the_figures_are_missing_or_unusable(usage):
    assert actual_cost("claude-sonnet-5-5", usage) is None


# --- reserve, settle, release -------------------------------------------------------------------------------------


def test_a_new_ledger_starts_at_zero_for_the_current_month(tmp_path):
    clock = _Clock(datetime(2026, 10, 8, 12, 0, tzinfo=UTC))

    snapshot = _ledger(tmp_path, clock=clock).snapshot()

    assert snapshot.month == "2026-10"
    assert (snapshot.spent_micro, snapshot.reserved_micro, snapshot.requests) == (0, 0, 0)
    assert snapshot.remaining_micro == 1_000
    assert snapshot.cap_reached is False
    assert snapshot.warning is False


def test_settling_replaces_the_reservation_with_the_real_cost(tmp_path):
    ledger = _ledger(tmp_path)
    reservation = ledger.reserve(400)

    assert ledger.snapshot().reserved_micro == 400

    charged = ledger.settle(reservation, 150, input_tokens=20, output_tokens=10)

    snapshot = ledger.snapshot()
    assert charged == 150
    assert (snapshot.spent_micro, snapshot.reserved_micro, snapshot.requests) == (150, 0, 1)
    assert (snapshot.input_tokens, snapshot.output_tokens) == (20, 10)


def test_settling_with_no_usable_figure_charges_the_whole_reservation(tmp_path):
    """Never an undercount: if the provider said nothing we can price, the
    worst case is what we record."""

    ledger = _ledger(tmp_path)

    charged = ledger.settle(ledger.reserve(400), None)

    assert charged == 400
    assert ledger.snapshot().spent_micro == 400


def test_releasing_holds_nothing_and_records_no_request(tmp_path):
    ledger = _ledger(tmp_path)
    reservation = ledger.reserve(400)

    ledger.release(reservation)
    ledger.release(reservation)  # idempotent

    snapshot = ledger.snapshot()
    assert (snapshot.spent_micro, snapshot.reserved_micro, snapshot.requests) == (0, 0, 0)


def test_a_reservation_cannot_be_settled_twice_or_after_release(tmp_path):
    ledger = _ledger(tmp_path)
    first = ledger.reserve(100)
    ledger.settle(first, 50)
    second = ledger.reserve(100)
    ledger.release(second)

    with pytest.raises(ValueError, match="already settled or released"):
        ledger.settle(first, 50)
    with pytest.raises(ValueError, match="already settled or released"):
        ledger.settle(second, 50)
    assert ledger.snapshot().spent_micro == 50


def test_a_call_that_would_pass_the_cap_is_refused_and_holds_nothing(tmp_path):
    ledger = _ledger(tmp_path, cap=1_000)
    ledger.settle(ledger.reserve(900), 900)

    with pytest.raises(SpendCapReachedError):
        ledger.reserve(200)

    assert ledger.snapshot().reserved_micro == 0
    ledger.reserve(100)  # exactly the cap is allowed


def test_calls_in_flight_count_against_the_cap(tmp_path):
    ledger = _ledger(tmp_path, cap=1_000)
    ledger.reserve(600)

    with pytest.raises(SpendCapReachedError):
        ledger.reserve(500)


def test_the_warning_starts_at_eighty_percent_of_the_cap(tmp_path):
    ledger = _ledger(tmp_path, cap=1_000)
    ledger.settle(ledger.reserve(790), 790)
    assert ledger.snapshot().warning is False

    ledger.settle(ledger.reserve(10), 10)

    assert ledger.snapshot().warning is True
    assert ledger.snapshot().cap_reached is False


def test_the_cap_resets_at_the_start_of_the_next_utc_month(tmp_path):
    clock = _Clock(datetime(2026, 10, 31, 23, 59, tzinfo=UTC))
    ledger = _ledger(tmp_path, cap=1_000, clock=clock)
    ledger.settle(ledger.reserve(1_000), 1_000)
    assert ledger.snapshot().cap_reached is True

    clock.when = datetime(2026, 11, 1, 0, 1, tzinfo=UTC)

    snapshot = ledger.snapshot()
    assert snapshot.month == "2026-11"
    assert snapshot.spent_micro == 0
    assert snapshot.cap_reached is False
    ledger.reserve(1_000)


def test_a_call_that_started_last_month_is_charged_to_last_month(tmp_path):
    clock = _Clock(datetime(2026, 10, 31, 23, 59, tzinfo=UTC))
    ledger = _ledger(tmp_path, clock=clock)
    reservation = ledger.reserve(100)

    clock.when = datetime(2026, 11, 1, 0, 0, 30, tzinfo=UTC)
    ledger.settle(reservation, 100)

    assert ledger.snapshot().spent_micro == 0
    clock.when = datetime(2026, 10, 31, 23, 59, tzinfo=UTC)
    assert ledger.snapshot().spent_micro == 100


def test_totals_survive_a_restart(tmp_path):
    first = _ledger(tmp_path)
    first.settle(first.reserve(300), 300, input_tokens=5, output_tokens=7)

    snapshot = _ledger(tmp_path).snapshot()

    assert (snapshot.spent_micro, snapshot.requests, snapshot.input_tokens, snapshot.output_tokens) == (300, 1, 5, 7)


def test_concurrent_reservations_can_never_pass_the_cap(tmp_path):
    """Two slow-lane threads must not both pass a cap only one fits under."""

    ledger = _ledger(tmp_path, cap=10)
    granted: list[object] = []
    refused: list[object] = []
    barrier = threading.Barrier(25)

    def attempt() -> None:
        barrier.wait()
        try:
            granted.append(ledger.reserve(1))
        except SpendCapReachedError:
            refused.append(None)

    threads = [threading.Thread(target=attempt) for _ in range(25)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(granted) == 10
    assert len(refused) == 15
    assert ledger.snapshot().reserved_micro == 10


def test_the_database_holds_totals_only_never_any_text(tmp_path):
    ledger = _ledger(tmp_path)
    ledger.settle(ledger.reserve(100), 100, input_tokens=1, output_tokens=1)

    connection = sqlite3.connect(tmp_path / "spend.db")
    try:
        tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
        columns = {row[1]: row[2] for row in connection.execute("PRAGMA table_info(spend)")}
    finally:
        connection.close()

    assert tables == ["spend"]
    assert set(columns) == {"month", "spent_micro", "requests", "input_tokens", "output_tokens"}
    assert {name for name, kind in columns.items() if kind == "TEXT"} == {"month"}


@pytest.mark.parametrize("cap", [0, -1])
def test_a_cap_must_be_above_zero(tmp_path, cap):
    with pytest.raises(ValueError, match="greater than zero"):
        _ledger(tmp_path, cap=cap)


@pytest.mark.parametrize("fraction", [0, -0.1, 1.5])
def test_the_warning_fraction_must_be_in_range(tmp_path, fraction):
    with pytest.raises(ValueError, match="warning fraction"):
        _ledger(tmp_path, warning_fraction=fraction)
