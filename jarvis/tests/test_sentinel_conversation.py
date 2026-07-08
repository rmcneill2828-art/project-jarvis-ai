"""Tests for the Sentinel-gated conversation provider."""

from jarvis.interfaces.conversation import (
    EMPTY_MESSAGE_RESPONSE,
    ConversationOrchestrator,
    ConversationRequest,
    ConversationService,
)
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.policy import PolicyDecision
from sentinel.providers import ProviderRequest, ProviderResponse


class _StubProvider:
    def __init__(self, name: str = "stub") -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> tuple[str, ...]:
        return ("text-generation",)

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider_name=self._name,
            content=f"echo: {request.prompt}",
            capability=request.capability,
        )


class _AlwaysReviewPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(
            outcome=SentinelDecisionOutcome.REVIEW,
            reason="Internal policy detail that must not reach the user.",
            requires_human_approval=True,
        )


def _orchestrator_with_stub_provider() -> ProviderOrchestrator:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_StubProvider())
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("stub",)))
    return orchestrator


def test_empty_message_short_circuits_before_sentinel():
    gateway = SentinelTrustGateway()
    orchestrator = _orchestrator_with_stub_provider()
    provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)

    response = provider.generate(ConversationRequest(message="   "))

    assert response.message == EMPTY_MESSAGE_RESPONSE
    assert gateway.decisions() == ()


def test_allow_path_calls_orchestrator_and_returns_provider_content():
    gateway = SentinelTrustGateway()
    orchestrator = _orchestrator_with_stub_provider()
    provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)

    response = provider.generate(ConversationRequest(message="hello"))

    assert response.message == "echo: hello"
    assert response.provider == "stub"
    assert len(gateway.decisions()) == 1
    assert len(orchestrator.history()) == 1


def test_review_outcome_blocks_orchestrator_and_hides_internal_reason():
    gateway = SentinelTrustGateway(policy_engine=_AlwaysReviewPolicy())
    orchestrator = _orchestrator_with_stub_provider()
    provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)

    response = provider.generate(ConversationRequest(message="do something risky"))

    assert response.message == "Sentinel did not allow this request to proceed."
    assert "Internal policy detail" not in response.message
    assert orchestrator.history() == ()


def test_provider_failure_returns_generic_message():
    gateway = SentinelTrustGateway()
    orchestrator = ProviderOrchestrator()  # no providers registered - execute() will fail
    provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)

    response = provider.generate(ConversationRequest(message="hello"))

    assert response.message == "JARVIS could not reach an AI provider right now. Please try again."
    assert response.provider == "sentinel-gated"


def test_conversation_service_smoke_test_with_sentinel_gated_provider():
    gateway = SentinelTrustGateway()
    orchestrator = _orchestrator_with_stub_provider()
    sentinel_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)
    service = ConversationService(orchestrator=ConversationOrchestrator(provider=sentinel_provider))

    response = service.exchange("hello there")

    assert response.message == "echo: hello there"
    assert service.provider_name == "sentinel-gated"
    assert service.exchange_count == 1
