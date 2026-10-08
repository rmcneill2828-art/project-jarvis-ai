"""Confirmed escalation to the cloud provider (ESR-0061 WP3b,
EIP-ESR0061-003 6.3, 6.5, 6.6 and 6.8; ADR-0023).

An ordinary turn is answered locally and never reaches a cloud service. A
question reaches Claude only when JARVIS has *offered* it, a person allowed to
use it has *confirmed*, and the month's cap has room:

* `EscalationOffers` issues the one-time token a confirmation redeems. A token
  is random, bound to the profile it was issued to and to the exact message
  (which the server keeps - the client cannot swap the text after agreeing to
  the disclosure), expires after ten minutes and works once.
* `offer_reason()` is the deterministic rule for when JARVIS suggests
  escalating: the local route failed, or the message holds a research cue.
  Pressing "Ask Claude" is the third way and needs no rule.
* `MeteredCloudConversationProvider` sends the request through the cloud
  conversation provider and keeps the spend ledger honest around it: reserve
  the worst case, settle with the real usage, release when nothing was billed.
  Every escalation leaves one audit event holding categories and counts, never
  content.

Who may escalate is decided in two independent places (6.8): the RPC layer,
from the server-held active profile, and Sentinel's `TrustTierPolicy`, which
refuses the cloud capability to any requester that is not an Administrator or
an Adult - Child until WP6, Guest always, and anyone with no role.
"""

from __future__ import annotations

import logging
import re
import secrets
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from jarvis.shared.spend_ledger import (
    MICRO_DOLLARS_PER_DOLLAR,
    SpendCapReachedError,
    SpendLedger,
    SpendSnapshot,
    actual_cost,
    worst_case_cost,
    worst_case_input_tokens,
)
from sentinel.audit import AuditEvent, AuditRecorder
from sentinel.providers import CLOUD_TEXT_GENERATION_CAPABILITY

logger = logging.getLogger(__name__)

# Household roles that may use the cloud route. Child is excluded until WP6
# supplies consent and moderation (decision S6); Guest never escalates.
ESCALATION_ROLES = frozenset({"Administrator", "Adult"})

OFFER_TTL_SECONDS = 600.0
# Open offers kept at once; the oldest is dropped past this, so nothing grows
# without bound.
MAX_OPEN_OFFERS = 32

REASON_LOCAL_UNAVAILABLE = "local_unavailable"
REASON_RESEARCH_CUE = "research_cue"
REASON_REQUESTED = "requested"

CAP_REACHED_RESPONSE = (
    "The monthly allowance for asking Claude has been used up, so this question stays on this computer."
)
NOT_AVAILABLE_RESPONSE = "Asking Claude is not set up on this computer."

# Documented cue list (decision S3). A cue only makes JARVIS *offer*; it never
# sends anything. Easy to tune and to explain to a parent.
_RESEARCH_CUES = (
    "latest",
    "news",
    "research",
    "look up",
    "lookup",
    "compare",
    "in depth",
    "in-depth",
    "up to date",
    "up-to-date",
    "current events",
)
_CUE_PATTERN = re.compile(r"(?<![a-z])(?:" + "|".join(re.escape(cue) for cue in _RESEARCH_CUES) + r")(?![a-z])", re.IGNORECASE)
_URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)


def has_research_cue(message: str) -> bool:
    """True when `message` holds a research cue or a link."""

    return bool(_CUE_PATTERN.search(message) or _URL_PATTERN.search(message))


def offer_reason(response: ConversationResponse, message: str) -> str | None:
    """Why JARVIS should offer Claude for this turn, or None.

    Decided from the typed outcome and the user's own message - never from the
    reply text, and never by a model's judgement.
    """

    if response.failure == "unavailable":
        return REASON_LOCAL_UNAVAILABLE
    if response.is_model_reply and has_research_cue(message):
        return REASON_RESEARCH_CUE
    return None


@dataclass(frozen=True)
class _OpenOffer:
    profile_id: str
    message: str
    expires_at: float


class EscalationOffers:
    """One-time, profile-bound, expiring confirmation tokens."""

    def __init__(
        self,
        ttl_seconds: float = OFFER_TTL_SECONDS,
        max_open: int = MAX_OPEN_OFFERS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._ttl_seconds = ttl_seconds
        self._max_open = max_open
        self._clock = clock
        self._lock = threading.Lock()
        self._open: OrderedDict[str, _OpenOffer] = OrderedDict()

    @property
    def ttl_seconds(self) -> float:
        return self._ttl_seconds

    def issue(self, profile_id: str, message: str) -> str:
        """Issue a token for `profile_id` and exactly `message`."""

        token = secrets.token_urlsafe(24)
        now = self._clock()
        with self._lock:
            self._drop_expired(now)
            self._open[token] = _OpenOffer(profile_id, message, now + self._ttl_seconds)
            while len(self._open) > self._max_open:
                self._open.popitem(last=False)
        return token

    def redeem(self, token: str, profile_id: str) -> str | None:
        """Return the message the token was issued for and spend the token, or
        None for an unknown, expired, already-used or another profile's token.

        A token presented by the wrong profile is *not* spent, so it cannot be
        burned by someone else; it still yields nothing to them.
        """

        now = self._clock()
        with self._lock:
            self._drop_expired(now)
            offer = self._open.get(token)
            if offer is None or offer.profile_id != profile_id:
                return None
            del self._open[token]
            return offer.message

    def _drop_expired(self, now: float) -> None:
        for token in [token for token, offer in self._open.items() if offer.expires_at <= now]:
            del self._open[token]


def allowance_payload(snapshot: SpendSnapshot, usd_per_gbp: float) -> dict[str, object]:
    """The month's allowance as the UI shows it (USD, with the GBP the cap was
    set in). Totals only."""

    def usd(micro: int) -> float:
        return round(micro / MICRO_DOLLARS_PER_DOLLAR, 4)

    return {
        "month": snapshot.month,
        "capUsd": usd(snapshot.cap_micro),
        "spentUsd": usd(snapshot.spent_micro),
        "remainingUsd": usd(snapshot.remaining_micro),
        "capGbp": round(usd(snapshot.cap_micro) / usd_per_gbp, 2),
        "remainingGbp": round(usd(snapshot.remaining_micro) / usd_per_gbp, 2),
        "requests": snapshot.requests,
        "warning": snapshot.warning,
        "capReached": snapshot.cap_reached,
    }


class MeteredCloudConversationProvider:
    """Conversation provider for the cloud route, with the spend ledger around it."""

    name = "metered-cloud"

    def __init__(
        self,
        inner: SentinelGatedConversationProvider,
        ledger: SpendLedger,
        audit_recorder: AuditRecorder,
        usd_per_gbp: float = 1.25,
    ) -> None:
        self._inner = inner
        self._ledger = ledger
        self._audit_recorder = audit_recorder
        self._usd_per_gbp = usd_per_gbp

    @property
    def usd_per_gbp(self) -> float:
        """The fixed rate the pounds cap was converted at (decision S4)."""

        return self._usd_per_gbp

    @property
    def ledger(self) -> SpendLedger:
        return self._ledger

    def _provider(self):
        providers = self._inner.orchestrator.eligible_providers(CLOUD_TEXT_GENERATION_CAPABILITY)
        return providers[0] if providers else None

    @property
    def available(self) -> bool:
        """True when a cloud provider is registered (a key is configured)."""

        return self._provider() is not None

    @property
    def model(self) -> str | None:
        provider = self._provider()
        return getattr(provider, "model", None) if provider is not None else None

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        provider = self._provider()
        if provider is None:
            return ConversationResponse(message=NOT_AVAILABLE_RESPONSE, provider=self.name, failure="unavailable")
        model = getattr(provider, "model", "")
        max_output_tokens = getattr(provider, "max_tokens", 1024)
        input_bound = worst_case_input_tokens(
            request.persona or "",
            request.message,
            *(text for pair in request.history for text in pair),
            *request.memory_notes,
        )
        try:
            reservation = self._ledger.reserve(worst_case_cost(model, input_bound, max_output_tokens))
        except SpendCapReachedError:
            self._audit(request, "cap_reached", {})
            return ConversationResponse(message=CAP_REACHED_RESPONSE, provider=self.name, failure="cap_reached")

        try:
            response = self._inner.generate(request)
        except BaseException:
            self._ledger.release(reservation)
            raise

        billed = response.is_model_reply or response.failure == "declined"
        if not billed:
            # Nothing came back to bill (denied, unavailable): hold nothing.
            self._ledger.release(reservation)
            outcome = "denied" if response.failure == "denied" else "failed"
            self._audit(request, outcome, {})
            return response

        usage = response.metadata
        charged = self._ledger.settle(
            reservation,
            actual_cost(model, usage),
            _token_count(usage, "input_tokens"),
            _token_count(usage, "output_tokens"),
        )
        self._audit(
            request,
            "declined" if response.failure == "declined" else "answered",
            {
                "input_tokens": str(_token_count(usage, "input_tokens")),
                "output_tokens": str(_token_count(usage, "output_tokens")),
                "cost_micro_usd": str(charged),
            },
        )
        return response

    def _audit(self, request: ConversationRequest, outcome: str, counts: Mapping[str, str]) -> None:
        """One audit event per escalation: the requester's role, the outcome and
        counts. Never the message, the reply or any memory."""

        try:
            self._audit_recorder.record(
                AuditEvent(
                    event_type="cloud_escalation",
                    outcome=outcome,
                    summary=f"Escalation to the cloud provider: {outcome}.",
                    metadata={"role": request.requester_role or "none", **counts},
                )
            )
        except Exception:  # noqa: BLE001 - a failing audit write must not turn an answered question into an error
            logger.error("Could not record the escalation audit event.")


def _token_count(usage: Mapping[str, str], name: str) -> int:
    try:
        return max(0, int(usage.get(f"usage_{name}", "0")))
    except ValueError:
        return 0


__all__ = [
    "CAP_REACHED_RESPONSE",
    "ESCALATION_ROLES",
    "NOT_AVAILABLE_RESPONSE",
    "OFFER_TTL_SECONDS",
    "REASON_LOCAL_UNAVAILABLE",
    "REASON_REQUESTED",
    "REASON_RESEARCH_CUE",
    "EscalationOffers",
    "MeteredCloudConversationProvider",
    "allowance_payload",
    "has_research_cue",
    "offer_reason",
]
