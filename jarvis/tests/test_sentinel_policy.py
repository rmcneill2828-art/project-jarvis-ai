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


# --- ESR-0061 WP3b: the cloud text route is for Administrators and Adults only (EIP-ESR0061-003 6.8) -------------


def _cloud_request(role: str | None, *, requires_approval: bool = False) -> SentinelRequest:
    metadata = {"capability": "text-generation-cloud"}
    if role is not None:
        metadata["role"] = role
    return SentinelRequest(
        source="jarvis.escalation",
        intent="conversation.escalate",
        requires_approval=requires_approval,
        metadata=metadata,
    )


@pytest.mark.parametrize("role", ["Administrator", "Adult", "administrator", " Adult "])
def test_an_administrator_or_adult_may_use_the_cloud_route(role):
    decision = TrustTierPolicy().evaluate(_cloud_request(role))

    assert decision.outcome is SentinelDecisionOutcome.ALLOW
    assert decision.category is TrustCategory.ROUTINE_INTERACTION


@pytest.mark.parametrize("role", ["Child", "Guest", "child", "Superuser", "", "   "])
def test_a_child_a_guest_or_an_unknown_role_is_denied_the_cloud_route(role):
    decision = TrustTierPolicy().evaluate(_cloud_request(role))

    assert decision.outcome is SentinelDecisionOutcome.DENY
    assert decision.category is TrustCategory.CLOUD_ESCALATION_NOT_PERMITTED
    assert decision.trust_tier is TrustTier.RESTRICTED


def test_a_cloud_request_with_no_role_at_all_is_denied():
    """The role is supplied by the server from the active profile, so its
    absence means something is wrong - the safe reading is a refusal."""

    decision = TrustTierPolicy().evaluate(_cloud_request(None))

    assert decision.outcome is SentinelDecisionOutcome.DENY
    assert decision.category is TrustCategory.CLOUD_ESCALATION_NOT_PERMITTED


def test_the_cloud_rule_cannot_be_softened_by_asking_for_approval():
    decision = TrustTierPolicy().evaluate(_cloud_request("Child", requires_approval=True))

    assert decision.outcome is SentinelDecisionOutcome.DENY


def test_the_role_means_nothing_off_the_cloud_route():
    """The ordinary local route is unaffected: a Child's turn needs no role."""

    local = SentinelRequest(source="s", intent="conversation.generate", metadata={"capability": "text-generation"})
    with_role = SentinelRequest(
        source="s", intent="conversation.generate", metadata={"capability": "text-generation", "role": "Child"}
    )

    assert TrustTierPolicy().evaluate(local).outcome is SentinelDecisionOutcome.ALLOW
    assert TrustTierPolicy().evaluate(with_role).outcome is SentinelDecisionOutcome.ALLOW


def test_the_gateway_denies_a_childs_cloud_request_and_audits_it():
    gateway = SentinelTrustGateway(policy_engine=TrustTierPolicy())

    response = gateway.evaluate(_cloud_request("Child"))

    assert response.decision.outcome is SentinelDecisionOutcome.DENY
    assert "cloud_escalation_not_permitted" in response.decision.reason
