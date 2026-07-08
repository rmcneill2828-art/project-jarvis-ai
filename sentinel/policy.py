"""Sentinel policy abstraction: decides whether a request may proceed."""

from dataclasses import dataclass
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelRequest


@dataclass(frozen=True)
class PolicyDecision:
    """Policy decision for a Sentinel request."""

    outcome: SentinelDecisionOutcome
    reason: str
    requires_human_approval: bool = False

    def __post_init__(self) -> None:
        if not self.reason.strip():
            msg = "Policy decision reason must not be empty."
            raise ValueError(msg)


class PolicyEngine(Protocol):
    """Protocol implemented by Sentinel policy engines."""

    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        """Evaluate a request and return a policy decision."""


class SimpleApprovalPolicy:
    """Reproduces SentinelTrustGateway's original inline approval logic.

    Requests flagged requires_approval are routed for review; everything
    else is allowed. No trust tiers, no speculative policy logic - this is
    the exact behaviour that existed inline before the seam was extracted.
    """

    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        if request.requires_approval:
            return PolicyDecision(
                outcome=SentinelDecisionOutcome.REVIEW,
                reason="Request requires human approval before execution.",
                requires_human_approval=True,
            )
        return PolicyDecision(
            outcome=SentinelDecisionOutcome.ALLOW,
            reason="Request accepted by Sentinel Core boundary.",
        )
