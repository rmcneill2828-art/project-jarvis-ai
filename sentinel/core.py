"""Sentinel Core trust boundary primitives.

Sentinel is intentionally independent of the JARVIS package so it can become a
shared trust gateway for Guardian and future AI systems.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from types import MappingProxyType

from sentinel.audit import AuditEvent, AuditRecorder, MemoryAuditRecorder


class SentinelDecisionOutcome(Enum):
    """Supported Sentinel trust decision outcomes."""

    ALLOW = "Allow"
    DENY = "Deny"
    REVIEW = "Review"


@dataclass(frozen=True)
class SentinelRequest:
    """Request presented to Sentinel before platform execution."""

    source: str
    intent: str
    payload_type: str = "generic"
    requires_approval: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.source.strip():
            msg = "Sentinel request source must not be empty."
            raise ValueError(msg)
        if not self.intent.strip():
            msg = "Sentinel request intent must not be empty."
            raise ValueError(msg)
        if not self.payload_type.strip():
            msg = "Sentinel request payload type must not be empty."
            raise ValueError(msg)
        if self.created_at.tzinfo is None:
            msg = "Sentinel request timestamp must be timezone-aware."
            raise ValueError(msg)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class SentinelDecision:
    """Sentinel trust decision for a submitted request."""

    outcome: SentinelDecisionOutcome
    reason: str
    trust_boundary: str = "Sentinel Core"
    requires_human_approval: bool = False
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.reason.strip():
            msg = "Sentinel decision reason must not be empty."
            raise ValueError(msg)
        if not self.trust_boundary.strip():
            msg = "Sentinel trust boundary must not be empty."
            raise ValueError(msg)
        if self.decided_at.tzinfo is None:
            msg = "Sentinel decision timestamp must be timezone-aware."
            raise ValueError(msg)


@dataclass(frozen=True)
class SentinelResponse:
    """Sentinel response returned to a requesting client."""

    request: SentinelRequest
    decision: SentinelDecision
    message: str

    def __post_init__(self) -> None:
        if not self.message.strip():
            msg = "Sentinel response message must not be empty."
            raise ValueError(msg)


# Imported here, after SentinelDecisionOutcome/SentinelRequest/SentinelDecision/
# SentinelResponse are already defined, to avoid a circular import: sentinel.policy
# imports SentinelDecisionOutcome from this module, so this module cannot import
# sentinel.policy until that name already exists in this module's namespace.
from sentinel.policy import PolicyEngine, SimpleApprovalPolicy

_OUTCOME_MESSAGES = {
    SentinelDecisionOutcome.ALLOW: "Sentinel allowed the request to proceed.",
    SentinelDecisionOutcome.REVIEW: "Sentinel routed the request for review.",
    SentinelDecisionOutcome.DENY: "Sentinel denied the request.",
}


class SentinelTrustGateway:
    """Minimum Sentinel trust gateway.

    The gateway establishes the execution boundary. Trust decisions are
    delegated to a PolicyEngine; the gateway itself does not implement
    provider routing or Guardian cognition.
    """

    def __init__(
        self,
        audit_recorder: AuditRecorder | None = None,
        policy_engine: PolicyEngine | None = None,
    ) -> None:
        self._decisions: list[SentinelResponse] = []
        self._audit_recorder = audit_recorder or MemoryAuditRecorder()
        self._policy_engine = policy_engine or SimpleApprovalPolicy()

    @property
    def policy_engine(self) -> PolicyEngine:
        """Return the connected PolicyEngine, for test/diagnostic introspection."""

        return self._policy_engine

    def evaluate(self, request: SentinelRequest) -> SentinelResponse:
        """Evaluate a request at the Sentinel trust boundary."""

        policy_decision = self._policy_engine.evaluate(request)
        decision = SentinelDecision(
            outcome=policy_decision.outcome,
            reason=policy_decision.reason,
            requires_human_approval=policy_decision.requires_human_approval,
        )
        response = SentinelResponse(
            request=request,
            decision=decision,
            message=_OUTCOME_MESSAGES[decision.outcome],
        )

        self._decisions.append(response)
        self._audit_recorder.record(
            AuditEvent(
                event_type="sentinel_decision",
                outcome=decision.outcome.value,
                summary=response.message,
                metadata={
                    "source": request.source,
                    "intent": request.intent,
                    "reason": decision.reason,
                },
            )
        )
        return response

    def decisions(self) -> tuple[SentinelResponse, ...]:
        """Return immutable Sentinel decision history."""

        return tuple(self._decisions)

    def audit_events(self) -> tuple[AuditEvent, ...]:
        """Return recorded Sentinel audit events."""

        return self._audit_recorder.events()
