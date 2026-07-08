"""Tests for the Sentinel PolicyEngine abstraction."""

import pytest

from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.policy import (
    PolicyDecision,
    SimpleApprovalPolicy,
    TrustCategory,
    TrustTier,
    TrustTierPolicy,
)


def test_policy_decision_requires_non_empty_reason():
    with pytest.raises(ValueError):
        PolicyDecision(outcome=SentinelDecisionOutcome.ALLOW, reason="")


def test_simple_approval_policy_allows_by_default():
    policy = SimpleApprovalPolicy()
    request = SentinelRequest(source="test", intent="do a thing")

    decision = policy.evaluate(request)

    assert decision.outcome is SentinelDecisionOutcome.ALLOW
    assert decision.reason == "Request accepted by Sentinel Core boundary."
    assert decision.requires_human_approval is False


def test_simple_approval_policy_reviews_when_approval_required():
    policy = SimpleApprovalPolicy()
    request = SentinelRequest(source="test", intent="do a thing", requires_approval=True)

    decision = policy.evaluate(request)

    assert decision.outcome is SentinelDecisionOutcome.REVIEW
    assert decision.reason == "Request requires human approval before execution."
    assert decision.requires_human_approval is True


def test_sentinel_trust_gateway_uses_simple_approval_policy_by_default():
    gateway = SentinelTrustGateway()

    allowed = gateway.evaluate(SentinelRequest(source="test", intent="allowed"))
    reviewed = gateway.evaluate(
        SentinelRequest(source="test", intent="reviewed", requires_approval=True)
    )

    assert allowed.decision.outcome is SentinelDecisionOutcome.ALLOW
    assert allowed.message == "Sentinel allowed the request to proceed."
    assert reviewed.decision.outcome is SentinelDecisionOutcome.REVIEW
    assert reviewed.message == "Sentinel routed the request for review."


def test_sentinel_trust_gateway_output_unchanged_from_pre_wp2_behaviour():
    """Regression test: WP2 extracts existing inline logic behind a seam.

    These exact reason/message strings existed before the PolicyEngine seam
    was introduced. This test fails if WP2 silently changed behaviour rather
    than just relocating it.
    """

    gateway = SentinelTrustGateway()
    response = gateway.evaluate(SentinelRequest(source="test", intent="check"))

    assert response.decision.reason == "Request accepted by Sentinel Core boundary."
    assert response.message == "Sentinel allowed the request to proceed."
    assert response.decision.trust_boundary == "Sentinel Core"


class _CustomPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(
            outcome=SentinelDecisionOutcome.DENY,
            reason="Custom policy denies everything.",
        )


def test_sentinel_trust_gateway_uses_injected_policy_engine():
    gateway = SentinelTrustGateway(policy_engine=_CustomPolicy())

    response = gateway.evaluate(SentinelRequest(source="test", intent="anything"))

    assert response.decision.outcome is SentinelDecisionOutcome.DENY
    assert response.message == "Sentinel denied the request."


def test_trust_tier_policy_allows_routine_request():
    policy = TrustTierPolicy()
    request = SentinelRequest(source="guardian", intent="answer a routine question")

    decision = policy.evaluate(request)

    assert decision.outcome is SentinelDecisionOutcome.ALLOW
    assert decision.trust_tier is TrustTier.ROUTINE
    assert decision.category is TrustCategory.ROUTINE_INTERACTION
    assert decision.requires_human_approval is False
    assert "routine interaction" in decision.reason


def test_trust_tier_policy_routes_approval_request_to_review():
    policy = TrustTierPolicy()
    request = SentinelRequest(
        source="guardian",
        intent="perform an action requiring approval",
        requires_approval=True,
    )

    decision = policy.evaluate(request)

    assert decision.outcome is SentinelDecisionOutcome.REVIEW
    assert decision.trust_tier is TrustTier.SENSITIVE
    assert decision.category is TrustCategory.HUMAN_APPROVAL_REQUIRED
    assert decision.requires_human_approval is True
    assert "human review" in decision.reason


@pytest.mark.parametrize(
    ("sentinel_request", "expected_category"),
    [
        (
            SentinelRequest(
                source="guardian",
                intent="unsupported risk",
                metadata={"risk_category": "unsupported_high_risk"},
            ),
            TrustCategory.UNSUPPORTED_HIGH_RISK,
        ),
        (
            SentinelRequest(
                source="guardian",
                intent="emergency control",
                payload_type="emergency_control",
            ),
            TrustCategory.EMERGENCY_CONTROL,
        ),
        (
            SentinelRequest(
                source="guardian",
                intent="local agent action",
                payload_type="local_agent",
            ),
            TrustCategory.LOCAL_AGENT_ACTION,
        ),
    ],
)
def test_trust_tier_policy_denies_restricted_categories(
    sentinel_request: SentinelRequest, expected_category: TrustCategory
):
    policy = TrustTierPolicy()

    decision = policy.evaluate(sentinel_request)

    assert decision.outcome is SentinelDecisionOutcome.DENY
    assert decision.trust_tier is TrustTier.RESTRICTED
    assert decision.category is expected_category
    assert decision.requires_human_approval is False
    assert expected_category.value in decision.reason


@pytest.mark.parametrize(
    ("sentinel_request", "expected_category"),
    [
        (
            SentinelRequest(
                source="guardian",
                intent="unsupported risk with approval flag",
                requires_approval=True,
                metadata={"risk_category": "unsupported_high_risk"},
            ),
            TrustCategory.UNSUPPORTED_HIGH_RISK,
        ),
        (
            SentinelRequest(
                source="guardian",
                intent="emergency control with approval flag",
                payload_type="emergency_control",
                requires_approval=True,
            ),
            TrustCategory.EMERGENCY_CONTROL,
        ),
        (
            SentinelRequest(
                source="guardian",
                intent="local agent action with approval flag",
                payload_type="local_agent",
                requires_approval=True,
            ),
            TrustCategory.LOCAL_AGENT_ACTION,
        ),
    ],
)
def test_trust_tier_policy_denies_restricted_categories_before_review_routing(
    sentinel_request: SentinelRequest, expected_category: TrustCategory
):
    """Regression: requires_approval must not soften deny-category requests."""

    policy = TrustTierPolicy()

    decision = policy.evaluate(sentinel_request)

    assert decision.outcome is SentinelDecisionOutcome.DENY
    assert decision.trust_tier is TrustTier.RESTRICTED
    assert decision.category is expected_category
    assert decision.requires_human_approval is False
