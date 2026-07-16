"""Conversation provider that routes requests through Sentinel."""

import logging

from jarvis.interfaces.conversation import (
    EMPTY_MESSAGE_RESPONSE,
    ConversationRequest,
    ConversationResponse,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator
from sentinel.providers import ProviderRequest

logger = logging.getLogger(__name__)


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
    ) -> None:
        self._gateway = gateway
        self._orchestrator = orchestrator
        self._capability = capability
        self._source = source

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
            return ConversationResponse(
                message="Sentinel did not allow this request to proceed.",
                provider=self.name,
            )

        provider_request = ProviderRequest(prompt=request.message, capability=self._capability)

        try:
            orchestrated = self._orchestrator.execute(sentinel_response, provider_request)
        except RuntimeError as exc:
            logger.warning("Sentinel provider execution failed: %s", type(exc).__name__)
            return ConversationResponse(
                message="JARVIS could not reach an AI provider right now. Please try again.",
                provider=self.name,
            )

        return ConversationResponse(
            message=orchestrated.provider_response.content,
            provider=orchestrated.execution_record.selected_provider or self.name,
        )

    def configured_providers(self) -> tuple[str, ...]:
        """Return provider names currently eligible for this capability, in route order."""

        return tuple(provider.name for provider in self._orchestrator.eligible_providers(self._capability))
