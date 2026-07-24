"""Personal Memory consent-gated service (GAM-0001 Section 9.2, EIP-ESR0027-001).

The first real instance of a Sentinel `REVIEW` decision actually being
resolved: `propose()` submits a memory-retention request through the same
Sentinel trust gateway used for conversation, `approve()`/`deny()` require a
distinct, explicit call before anything is durably stored. No code path lets
a proposal store itself.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from jarvis.memory.store import (
    ConsentDecisionRecord,
    PersonalMemoryRecord,
    PersonalMemoryStore,
    utc_now,
)
from sentinel.core import (
    SentinelDecisionOutcome,
    SentinelRequest,
    SentinelResponse,
    SentinelTrustGateway,
)

logger = logging.getLogger(__name__)

MEMORY_RETENTION_CAPABILITY = "memory_retention"
LOCAL_USER_APPROVER_LABEL = "local-user"


@dataclass(frozen=True)
class PendingMemoryRequest:
    """A proposed memory-retention request awaiting an explicit human decision.

    Held in memory only - a proposal that is never approved or denied
    (process restart, abandoned) simply disappears with the pending dict.
    Only the eventual *resolution* (approve or deny) is made durable.
    """

    id: str
    content: str
    sentinel_response: SentinelResponse
    created_at: datetime = field(default_factory=utc_now)


class PersonalMemoryService:
    """Propose, approve and deny Personal Memory retention requests."""

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        store: PersonalMemoryStore,
        source: str = "jarvis.memory",
    ) -> None:
        self._gateway = gateway
        self._store = store
        self._source = source
        self._pending: dict[str, PendingMemoryRequest] = {}

    def propose(self, content: str) -> PendingMemoryRequest:
        """Propose retaining `content`, evaluating it through Sentinel.

        Requires the resulting decision to be REVIEW before creating a
        pending request. Refuses (raises RuntimeError) on DENY or on any
        unexpected outcome (including ALLOW) rather than ever trusting a
        non-REVIEW outcome to imply consent has already been given.
        """

        sentinel_request = SentinelRequest(
            source=self._source,
            intent="memory.retain",
            requires_approval=True,
            metadata={"capability": MEMORY_RETENTION_CAPABILITY},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)
        outcome = sentinel_response.decision.outcome

        if outcome is SentinelDecisionOutcome.DENY:
            msg = "Memory retention request was denied by Sentinel policy before any human review."
            raise RuntimeError(msg)
        if outcome is not SentinelDecisionOutcome.REVIEW:
            msg = (
                f"Memory retention request received unexpected Sentinel outcome {outcome.value!r} "
                "(expected REVIEW) - refusing rather than treating this as pre-approved."
            )
            raise RuntimeError(msg)

        pending_id = str(uuid.uuid4())
        pending = PendingMemoryRequest(id=pending_id, content=content, sentinel_response=sentinel_response)
        self._pending[pending_id] = pending
        return pending

    def approve(self, pending_id: str) -> PersonalMemoryRecord:
        """Approve a pending memory-retention request, storing it durably."""

        pending = self._pop_pending(pending_id)
        decision = self._record_decision(pending, "approved")
        record = PersonalMemoryRecord(
            id=str(uuid.uuid4()),
            content=pending.content,
            created_at=utc_now(),
            consent_decision_id=decision.id,
        )
        self._store.add(record)
        return record

    def deny(self, pending_id: str) -> ConsentDecisionRecord:
        """Deny a pending memory-retention request. Content is never stored."""

        pending = self._pop_pending(pending_id)
        decision = self._record_decision(pending, "denied")
        logger.info("Memory retention request denied: decision_id=%s", decision.id)
        return decision

    def list_records(self) -> tuple[PersonalMemoryRecord, ...]:
        """Return all stored Personal Memory records."""

        return self._store.list_all()

    def _pop_pending(self, pending_id: str) -> PendingMemoryRequest:
        try:
            return self._pending.pop(pending_id)
        except KeyError as exc:
            msg = f"No pending memory request found for id: {pending_id!r} (unknown or already resolved)."
            raise KeyError(msg) from exc

    def _record_decision(self, pending: PendingMemoryRequest, decision: str) -> ConsentDecisionRecord:
        sentinel_decision = pending.sentinel_response.decision
        record = ConsentDecisionRecord(
            id=pending.id,
            capability=MEMORY_RETENTION_CAPABILITY,
            decision=decision,
            decided_at=utc_now(),
            approver_label=LOCAL_USER_APPROVER_LABEL,
            sentinel_outcome=sentinel_decision.outcome.value,
            # SentinelDecision (sentinel/core.py) does not carry PolicyDecision's
            # trust_tier/category through from evaluate() - only outcome, reason
            # and requires_human_approval survive that translation today, so
            # there is no category value to record here honestly.
            sentinel_category=None,
            sentinel_reason=sentinel_decision.reason,
        )
        return self._store.record_decision(record)
