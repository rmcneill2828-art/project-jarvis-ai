"""Tests for the Sentinel-gated specialist agent invocation service."""

import pytest

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.interfaces.sentinel_agent import (
    STATUS_DENIED,
    STATUS_UNKNOWN_AGENT,
    AgentOutcome,
    SentinelGatedAgentService,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.policy import PolicyDecision, TrustTierPolicy


class _StubAgent:
    name = "stub-agent"

    def __init__(self) -> None:
        self.received: list[AgentRequest] = []

    def execute(self, request: AgentRequest) -> AgentResult:
        self.received.append(request)
        return AgentResult(status="reported", payload={"echo": request.task})


class _AlwaysDenyPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(
            outcome=SentinelDecisionOutcome.DENY,
            reason="Internal policy detail that must not reach the caller.",
        )


def test_agent_outcome_rejects_empty_status() -> None:
    with pytest.raises(ValueError, match="status"):
        AgentOutcome(status="")


def test_agent_outcome_denied_or_unknown_agent_must_not_carry_a_result() -> None:
    with pytest.raises(ValueError, match="result"):
        AgentOutcome(status=STATUS_DENIED, result=AgentResult(status="reported"))


def test_unknown_agent_short_circuits_before_sentinel() -> None:
    gateway = SentinelTrustGateway()
    service = SentinelGatedAgentService(gateway=gateway, agents={})

    outcome = service.invoke("does-not-exist", AgentRequest(task="anything"))

    assert outcome.status == STATUS_UNKNOWN_AGENT
    assert outcome.result is None
    assert gateway.decisions() == ()


def test_allow_path_calls_agent_and_echoes_its_status() -> None:
    gateway = SentinelTrustGateway()
    agent = _StubAgent()
    service = SentinelGatedAgentService(gateway=gateway, agents={agent.name: agent})

    outcome = service.invoke(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == "reported"
    assert outcome.result.payload["echo"] == "snapshot"
    assert agent.received[0].task == "snapshot"
    assert len(gateway.decisions()) == 1


def test_routine_interaction_classification_never_touches_local_agent_action() -> None:
    # Confirms this service's own request shape - metadata={"capability":
    # "routine_interaction"}, default payload_type - genuinely classifies
    # ROUTINE_INTERACTION under the real TrustTierPolicy, not merely under a
    # permissive test double (Engineering Reviewer design-review concern).
    gateway = SentinelTrustGateway(policy_engine=TrustTierPolicy())
    agent = _StubAgent()
    service = SentinelGatedAgentService(gateway=gateway, agents={agent.name: agent})

    outcome = service.invoke(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == "reported"
    response = gateway.decisions()[0]
    assert response.decision.outcome is SentinelDecisionOutcome.ALLOW


def test_deny_outcome_hides_internal_reason_and_never_calls_agent() -> None:
    gateway = SentinelTrustGateway(policy_engine=_AlwaysDenyPolicy())
    agent = _StubAgent()
    service = SentinelGatedAgentService(gateway=gateway, agents={agent.name: agent})

    outcome = service.invoke(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == STATUS_DENIED
    assert outcome.result is None
    assert "Internal policy detail" not in (outcome.message or "")
    assert agent.received == []


def test_available_agents_lists_registered_names() -> None:
    agent = _StubAgent()
    service = SentinelGatedAgentService(gateway=SentinelTrustGateway(), agents={agent.name: agent})

    assert service.available_agents() == ("stub-agent",)
