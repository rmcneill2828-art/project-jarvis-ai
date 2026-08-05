"""Sentinel-gated specialist agent invocation.

`SentinelGatedAgentService` mirrors
`jarvis.interfaces.sentinel_conversation.SentinelGatedConversationProvider`'s
gateway-evaluate-then-proceed flow exactly: construct one `SentinelRequest`
per invocation, call `gateway.evaluate()`, and only proceed on
`SentinelDecisionOutcome.ALLOW` - otherwise return a named, non-`None`
denial outcome, never raising or silently failing.

`AgentOutcome` mirrors `jarvis.interfaces.voice.SpeechOutcome`/
`TranscriptionOutcome`'s boundary-safe, named-status envelope pattern: every
outcome - success, unknown agent, Sentinel denial, runtime not running - is
a distinct, separately assertable `status` value, never `None` or a raised
exception standing in for a boundary failure.

Every invocation classifies `TrustCategory.ROUTINE_INTERACTION` under
`sentinel/policy.py`'s `TrustTierPolicy` - this module never sets a
`payload_type`/`capability` value that could classify
`TrustCategory.LOCAL_AGENT_ACTION`.
"""

import logging
from collections.abc import Mapping
from dataclasses import dataclass

from jarvis.agents.contracts import AgentRequest, AgentResult, SpecialistAgent
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway

logger = logging.getLogger(__name__)

STATUS_DENIED = "denied"
STATUS_UNKNOWN_AGENT = "unknown_agent"

DENIED_MESSAGE = "Sentinel did not allow this agent request to proceed."


@dataclass(frozen=True)
class AgentOutcome:
    """Boundary-safe outcome for a specialist agent invocation.

    A successful invocation's `status` is whatever the agent's own
    `AgentResult.status` reports (see `AgentResult`'s docstring) - this
    envelope does not hardcode a single success value. `unknown_agent` and
    `denied` are this service's own boundary-level statuses, distinct from
    anything an agent itself could report.
    """

    status: str
    result: AgentResult | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        if not self.status.strip():
            msg = "Agent outcome status must not be empty."
            raise ValueError(msg)
        if self.status in {STATUS_DENIED, STATUS_UNKNOWN_AGENT} and self.result is not None:
            msg = "A denied or unknown-agent outcome must not include a result."
            raise ValueError(msg)


class SentinelGatedAgentService:
    """Routes specialist agent invocations through Sentinel before executing."""

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        agents: Mapping[str, SpecialistAgent],
        source: str = "jarvis.agents",
    ) -> None:
        self._gateway = gateway
        self._agents = dict(agents)
        self._source = source

    @property
    def gateway(self) -> SentinelTrustGateway:
        """Return the connected Sentinel trust gateway, for test/diagnostic introspection."""

        return self._gateway

    def available_agents(self) -> tuple[str, ...]:
        """Return the names of all registered specialist agents."""

        return tuple(self._agents)

    def invoke(self, agent_name: str, request: AgentRequest) -> AgentOutcome:
        """Invoke the named agent's `execute()`, gated through Sentinel.

        Returns `unknown_agent` before any Sentinel call when `agent_name`
        is not registered - there is nothing to evaluate. Otherwise
        constructs one `SentinelRequest` classified `ROUTINE_INTERACTION`
        and proceeds only on `ALLOW`.
        """

        agent = self._agents.get(agent_name)
        if agent is None:
            return AgentOutcome(status=STATUS_UNKNOWN_AGENT)

        sentinel_request = SentinelRequest(
            source=self._source,
            intent=f"agent.invoke.{agent_name}",
            metadata={"capability": "routine_interaction"},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)

        if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
            # decision.reason is not surfaced here, matching
            # SentinelGatedConversationProvider's own precedent: PolicyEngine
            # is an extensible protocol whose internal reasoning should not
            # be echoed into a caller-facing response. The full reason is
            # already captured in Sentinel's audit trail via
            # SentinelTrustGateway.evaluate().
            logger.warning("Sentinel denied agent invocation: %s", agent_name)
            return AgentOutcome(status=STATUS_DENIED, message=DENIED_MESSAGE)

        result = agent.execute(request)
        return AgentOutcome(status=result.status, result=result)
