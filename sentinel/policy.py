"""Sentinel policy abstraction: decides whether a request may proceed."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelRequest


class TrustTier(Enum):
    """Forward-compatible Sentinel trust tiers for policy classification."""

    ROUTINE = "routine"
    SENSITIVE = "sensitive"
    RESTRICTED = "restricted"


class TrustCategory(Enum):
    """Policy category slots used to classify Sentinel requests.

    These categories are deliberately boundary-shaped rather than full Guardian,
    family-safety, emergency-control or local-agent specifications. EBG-0020 and
    EBG-0021 identify future boundary areas, but they do not yet define complete
    taxonomies. This model gives Sentinel stable extension points without
    implementing those future capabilities.
    """

    ROUTINE_INTERACTION = "routine_interaction"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    EMERGENCY_CONTROL = "emergency_control"
    LOCAL_AGENT_ACTION = "local_agent_action"
    UNSUPPORTED_HIGH_RISK = "unsupported_high_risk"


@dataclass(frozen=True)
class PolicyDecision:
    """Policy decision for a Sentinel request."""

    outcome: SentinelDecisionOutcome
    reason: str
    requires_human_approval: bool = False
    trust_tier: TrustTier | None = None
    category: TrustCategory | None = None

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


class TrustTierPolicy:
    """Classify Sentinel requests into trust tiers without changing defaults.

    This policy is additive. SentinelTrustGateway continues to default to
    SimpleApprovalPolicy unless a caller explicitly injects TrustTierPolicy.
    """

    _LOCAL_AGENT_PAYLOAD_TYPES = frozenset({"local_agent", "device_control"})
    _EMERGENCY_PAYLOAD_TYPES = frozenset({"emergency_control", "family_safety"})

    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        category = self.classify(request)

        if category in {
            TrustCategory.LOCAL_AGENT_ACTION,
            TrustCategory.EMERGENCY_CONTROL,
            TrustCategory.UNSUPPORTED_HIGH_RISK,
        }:
            return PolicyDecision(
                outcome=SentinelDecisionOutcome.DENY,
                reason=(
                    "Request denied by Sentinel trust-tier policy because "
                    f"{category.value} is not yet supported by an approved "
                    "implementation boundary."
                ),
                trust_tier=TrustTier.RESTRICTED,
                category=category,
            )

        if category is TrustCategory.HUMAN_APPROVAL_REQUIRED:
            return PolicyDecision(
                outcome=SentinelDecisionOutcome.REVIEW,
                reason="Request routed for human review by Sentinel trust-tier policy.",
                requires_human_approval=True,
                trust_tier=TrustTier.SENSITIVE,
                category=category,
            )

        return PolicyDecision(
            outcome=SentinelDecisionOutcome.ALLOW,
            reason="Request allowed by Sentinel trust-tier policy as routine interaction.",
            trust_tier=TrustTier.ROUTINE,
            category=TrustCategory.ROUTINE_INTERACTION,
        )

    def classify(self, request: SentinelRequest) -> TrustCategory:
        """Classify a request using current SentinelRequest fields only."""

        risk_category = request.metadata.get("risk_category", "").strip().lower()
        capability = request.metadata.get("capability", "").strip().lower()
        payload_type = request.payload_type.strip().lower()

        if request.requires_approval:
            return TrustCategory.HUMAN_APPROVAL_REQUIRED
        if risk_category == "unsupported_high_risk":
            return TrustCategory.UNSUPPORTED_HIGH_RISK
        if payload_type in self._EMERGENCY_PAYLOAD_TYPES or capability == "emergency_control":
            return TrustCategory.EMERGENCY_CONTROL
        if payload_type in self._LOCAL_AGENT_PAYLOAD_TYPES or capability == "local_agent":
            return TrustCategory.LOCAL_AGENT_ACTION
        return TrustCategory.ROUTINE_INTERACTION
