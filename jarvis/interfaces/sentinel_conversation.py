"""Conversation provider that routes requests through Sentinel."""

import logging
import time

from jarvis.interfaces.conversation import (
    EMPTY_MESSAGE_RESPONSE,
    ConversationRequest,
    ConversationResponse,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator
from sentinel.providers import ConversationTurn, ProviderRequest

logger = logging.getLogger(__name__)

# User-facing responses for the two non-model outcomes. Promoted to named
# constants (EBG-0141, ESR-0059 WP3), as GuardianRuntime's former duplicated
# copies of these literals asked. Callers no longer need to match on this
# text: both responses carry `is_model_reply=False`.
SENTINEL_DENIED_RESPONSE = "Sentinel did not allow this request to proceed."
PROVIDER_UNAVAILABLE_RESPONSE = "JARVIS could not reach an AI provider right now. Please try again."


class SentinelGatedConversationProvider:
    """Conversation provider that routes requests through Sentinel for trust,
    policy and provider orchestration before returning a response."""

    name = "sentinel-gated"

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        orchestrator: ProviderOrchestrator,
        capability: str = "text-generation",
        source: str = "jarvis.conversation",
        turn_deadline_seconds: float | None = None,
    ) -> None:
        if turn_deadline_seconds is not None and turn_deadline_seconds <= 0:
            msg = "turn_deadline_seconds must be greater than zero when provided."
            raise ValueError(msg)
        self._gateway = gateway
        self._orchestrator = orchestrator
        self._capability = capability
        self._source = source
        # Overall budget for one conversation turn, failover included
        # (EBG-0139, ESR-0059 WP5). None keeps the previous behaviour: only
        # each provider's own timeout applies.
        self._turn_deadline_seconds = turn_deadline_seconds

    @property
    def orchestrator(self) -> ProviderOrchestrator:
        """Return the provider orchestrator, for diagnostics and for the escalation path (ESR-0061 WP3)."""

        return self._orchestrator

    @property
    def gateway(self) -> SentinelTrustGateway:
        """Return the connected Sentinel trust gateway, for test/diagnostic introspection."""

        return self._gateway

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        """Generate a response by routing the request through Sentinel."""

        if not request.message.strip():
            return ConversationResponse(message=EMPTY_MESSAGE_RESPONSE, provider=self.name)

        sentinel_request = SentinelRequest(
            source=self._source,
            intent="conversation.generate",
            metadata={"capability": self._capability},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)

        if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
            # decision.reason is not surfaced here: PolicyEngine is an extensible
            # protocol and a future policy implementation (GuardianPolicy,
            # FamilyPolicy, etc.) could put internal reasoning in reason that
            # shouldn't be echoed into a live user-facing response. The full
            # reason is already captured in Sentinel's audit trail via
            # SentinelTrustGateway.evaluate().
            return ConversationResponse(message=SENTINEL_DENIED_RESPONSE, provider=self.name)

        provider_request = ProviderRequest(
            prompt=request.message,
            capability=self._capability,
            system_prompt=request.persona,
            # EBG-0142 (ESR-0059 WP7): history and retained memory travel as
            # data, not inside the system prompt.
            history=tuple(
                turn
                for user_message, reply in request.history
                for turn in (ConversationTurn("user", user_message), ConversationTurn("assistant", reply))
            ),
            context_notes=request.memory_notes,
            deadline=(
                time.monotonic() + self._turn_deadline_seconds
                if self._turn_deadline_seconds is not None
                else None
            ),
        )

        try:
            orchestrated = self._orchestrator.execute(sentinel_response, provider_request)
        except RuntimeError as exc:
            logger.warning("Sentinel provider execution failed: %s", type(exc).__name__)
            return ConversationResponse(message=PROVIDER_UNAVAILABLE_RESPONSE, provider=self.name)

        return ConversationResponse(
            message=orchestrated.provider_response.content,
            provider=orchestrated.execution_record.selected_provider or self.name,
            is_model_reply=True,
        )

    def configured_providers(self) -> tuple[str, ...]:
        """Return provider names currently eligible for this capability, in route order."""

        return tuple(provider.name for provider in self._orchestrator.eligible_providers(self._capability))
