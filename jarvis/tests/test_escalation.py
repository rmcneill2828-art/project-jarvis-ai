"""Tests for confirmed escalation to the cloud provider: cues, offers and the
metered provider (ESR-0061 WP3b, EIP-ESR0061-003 6.3, 6.5, 6.6)."""

from types import SimpleNamespace

import pytest

from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
from jarvis.interfaces.escalation import (
    CAP_REACHED_RESPONSE,
    MAX_OPEN_OFFERS,
    NOT_AVAILABLE_RESPONSE,
    REASON_LOCAL_UNAVAILABLE,
    REASON_RESEARCH_CUE,
    EscalationOffers,
    MeteredCloudConversationProvider,
    allowance_payload,
    has_research_cue,
    offer_reason,
)
from jarvis.shared.spend_ledger import SpendLedger
from sentinel.audit import MemoryAuditRecorder

# --- when JARVIS offers (decision S3) -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "What is the latest on the election?",
        "Please research heat pumps",
        "can you LOOK UP this word",
        "compare these two phones",
        "explain it in depth",
        "what's in the news today",
        "see https://example.com/article",
    ],
)
def test_research_cues_are_recognised(message):
    assert has_research_cue(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "hello",
        "what is two plus two",
        "my newspaper arrived",
        "the lookups table is full",
        "the greatest film",
        "",
    ],
)
def test_ordinary_messages_have_no_cue(message):
    """A cue is a whole word or phrase: `newspaper` is not `news`."""

    assert has_research_cue(message) is False


def test_a_local_failure_is_offered_whatever_the_message_says():
    response = ConversationResponse(message="x", provider="sentinel-gated", failure="unavailable")

    assert offer_reason(response, "hello") == REASON_LOCAL_UNAVAILABLE


def test_a_local_answer_to_a_research_question_is_offered_a_deeper_one():
    response = ConversationResponse(message="x", provider="ollama", is_model_reply=True)

    assert offer_reason(response, "research solar panels") == REASON_RESEARCH_CUE
    assert offer_reason(response, "hello") is None


@pytest.mark.parametrize("failure", ["denied", "declined", "cap_reached", None])
def test_other_non_answers_are_never_offered_for_the_reply_text(failure):
    """Decided from the typed outcome: a denial or a decline is not a prompt to
    ask somebody else, and the reply's wording is never inspected."""

    response = ConversationResponse(message="latest news research", provider="p", failure=failure)

    assert offer_reason(response, "hello") is None


# --- offers: one-time, profile-bound, expiring --------------------------------------------------------------------


class _Time:
    def __init__(self) -> None:
        self.now = 1_000.0

    def __call__(self) -> float:
        return self.now


def test_a_token_returns_the_exact_message_it_was_issued_for_and_works_once():
    offers = EscalationOffers()
    token = offers.issue("profile-1", "the question")

    assert offers.redeem(token, "profile-1") == "the question"
    assert offers.redeem(token, "profile-1") is None


def test_tokens_are_unguessable_and_distinct():
    offers = EscalationOffers()

    tokens = {offers.issue("p", "m") for _ in range(50)}

    assert len(tokens) == 50
    assert all(len(token) >= 32 for token in tokens)


def test_another_profile_cannot_use_a_token_and_cannot_burn_it():
    offers = EscalationOffers()
    token = offers.issue("profile-1", "the question")

    assert offers.redeem(token, "profile-2") is None
    assert offers.redeem(token, "profile-1") == "the question"


@pytest.mark.parametrize("token", ["", "nonsense", "A" * 40])
def test_an_unknown_token_yields_nothing(token):
    assert EscalationOffers().redeem(token, "profile-1") is None


def test_a_token_expires_after_ten_minutes():
    clock = _Time()
    offers = EscalationOffers(clock=clock)
    token = offers.issue("profile-1", "the question")

    clock.now += 599
    still_valid = offers.redeem(token, "profile-1")
    expired = offers.issue("profile-1", "again")
    clock.now += 601

    assert still_valid == "the question"
    assert offers.redeem(expired, "profile-1") is None
    assert offers.ttl_seconds == 600


def test_open_offers_are_bounded_and_the_oldest_is_dropped():
    offers = EscalationOffers()
    first = offers.issue("p", "first")
    for index in range(MAX_OPEN_OFFERS):
        offers.issue("p", f"later {index}")

    assert offers.redeem(first, "p") is None


# --- the allowance as shown ---------------------------------------------------------------------------------------


def test_the_allowance_is_shown_in_dollars_and_in_the_pounds_it_was_set_in(tmp_path):
    ledger = SpendLedger(tmp_path / "s.db", cap_micro=37_500_000)
    ledger.settle(ledger.reserve(7_500_000), 7_500_000)

    payload = allowance_payload(ledger.snapshot(), 1.25)

    assert payload["capUsd"] == 37.5
    assert payload["spentUsd"] == 7.5
    assert payload["remainingUsd"] == 30.0
    assert payload["capGbp"] == 30.0
    assert payload["remainingGbp"] == 24.0
    assert payload["warning"] is False
    assert payload["capReached"] is False
    assert payload["requests"] == 1


# --- the metered provider -----------------------------------------------------------------------------------------


class _Cloud:
    name = "anthropic"
    model = "claude-sonnet-5-5"
    max_tokens = 1_024


_CLOUD = _Cloud()


class _Inner:
    """Stands in for SentinelGatedConversationProvider."""

    def __init__(self, response=None, *, error=None, providers=(_CLOUD,)) -> None:
        self.calls: list[ConversationRequest] = []
        self._response = response
        self._error = error
        self.orchestrator = SimpleNamespace(eligible_providers=lambda capability: providers)

    def generate(self, request):
        self.calls.append(request)
        if self._error is not None:
            raise self._error
        return self._response


def _request(**overrides) -> ConversationRequest:
    defaults = {"message": "a private question", "persona": "persona", "requester_role": "Adult"}
    return ConversationRequest(**{**defaults, **overrides})


def _metered(tmp_path, inner, cap=10_000_000):
    audit = MemoryAuditRecorder()
    ledger = SpendLedger(tmp_path / "spend.db", cap_micro=cap)
    return MeteredCloudConversationProvider(inner, ledger, audit), ledger, audit


def _answer(**metadata):
    return ConversationResponse(message="the answer", provider="anthropic", is_model_reply=True, metadata=metadata)


def test_an_answer_is_settled_at_the_real_cost_and_audited_with_counts_only(tmp_path):
    inner = _Inner(_answer(usage_input_tokens="1000", usage_output_tokens="500"))
    metered, ledger, audit = _metered(tmp_path, inner)

    response = metered.generate(_request())

    assert response.message == "the answer"
    snapshot = ledger.snapshot()
    assert snapshot.spent_micro == 1000 * 2 + 500 * 10
    assert (snapshot.reserved_micro, snapshot.requests) == (0, 1)
    (event,) = audit.events()
    assert event.event_type == "cloud_escalation"
    assert event.outcome == "answered"
    assert dict(event.metadata) == {
        "role": "Adult",
        "input_tokens": "1000",
        "output_tokens": "500",
        "cost_micro_usd": "7000",
    }


def test_the_audit_event_never_holds_the_message_the_reply_or_any_memory(tmp_path):
    inner = _Inner(_answer(usage_input_tokens="1", usage_output_tokens="1"))
    metered, _, audit = _metered(tmp_path, inner)

    metered.generate(_request(message="my secret plan", memory_notes=("my secret note",)))

    text = repr([event.as_dict() for event in audit.events()])
    assert "secret" not in text
    assert "the answer" not in text


def test_an_answer_with_no_usage_is_charged_the_whole_reservation(tmp_path):
    metered, ledger, _ = _metered(tmp_path, _Inner(_answer()))

    metered.generate(_request())

    assert ledger.snapshot().spent_micro > 0
    assert ledger.snapshot().spent_micro >= 1_024 * 10  # at least the full output allowance


def test_a_decline_is_still_billed_from_its_usage_and_reported_honestly(tmp_path):
    declined = ConversationResponse(
        message="declined",
        provider="sentinel-gated",
        failure="declined",
        metadata={"usage_input_tokens": "300", "usage_output_tokens": "0"},
    )
    metered, ledger, audit = _metered(tmp_path, _Inner(declined))

    response = metered.generate(_request())

    assert response.failure == "declined"
    assert ledger.snapshot().spent_micro == 600
    assert audit.events()[0].outcome == "declined"


@pytest.mark.parametrize("failure", ["unavailable", "denied"])
def test_a_call_that_produced_nothing_to_bill_releases_its_reservation(tmp_path, failure):
    failed = ConversationResponse(message="no", provider="sentinel-gated", failure=failure)
    metered, ledger, audit = _metered(tmp_path, _Inner(failed))

    metered.generate(_request())

    snapshot = ledger.snapshot()
    assert (snapshot.spent_micro, snapshot.reserved_micro, snapshot.requests) == (0, 0, 0)
    assert audit.events()[0].outcome == ("denied" if failure == "denied" else "failed")


def test_an_exception_releases_the_reservation_and_propagates(tmp_path):
    metered, ledger, _ = _metered(tmp_path, _Inner(error=KeyError("boom")))

    with pytest.raises(KeyError):
        metered.generate(_request())

    assert ledger.snapshot().reserved_micro == 0


def test_at_the_cap_nothing_is_sent(tmp_path):
    inner = _Inner(_answer())
    metered, ledger, audit = _metered(tmp_path, inner, cap=100)

    response = metered.generate(_request())

    assert inner.calls == []
    assert response.message == CAP_REACHED_RESPONSE
    assert (response.failure, response.is_model_reply) == ("cap_reached", False)
    assert ledger.snapshot().spent_micro == 0
    assert audit.events()[0].outcome == "cap_reached"


def test_with_no_cloud_provider_nothing_is_sent_and_nothing_is_reserved(tmp_path):
    inner = _Inner(_answer(), providers=())
    metered, ledger, _ = _metered(tmp_path, inner)

    response = metered.generate(_request())

    assert metered.available is False
    assert metered.model is None
    assert response.message == NOT_AVAILABLE_RESPONSE
    assert inner.calls == []
    assert ledger.snapshot().reserved_micro == 0


def test_the_request_reaches_the_inner_provider_unchanged(tmp_path):
    inner = _Inner(_answer(usage_input_tokens="1", usage_output_tokens="1"))
    metered, _, _ = _metered(tmp_path, inner)
    request = _request(memory_notes=("a note",), history=(("q", "a"),))

    metered.generate(request)

    assert inner.calls == [request]
    assert metered.model == "claude-sonnet-5-5"
