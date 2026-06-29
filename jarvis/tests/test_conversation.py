from jarvis.interfaces.conversation import (
    DEFAULT_RESPONSE,
    EMPTY_MESSAGE_RESPONSE,
    ConversationOrchestrator,
    ConversationRequest,
    ConversationResponse,
    ConversationService,
    DeterministicConversationProvider,
)


def test_conversation_returns_deterministic_response() -> None:
    conversation = ConversationService()

    assert conversation.respond("Hello JARVIS") == DEFAULT_RESPONSE


def test_conversation_handles_empty_message() -> None:
    conversation = ConversationService()

    assert conversation.respond("   ") == EMPTY_MESSAGE_RESPONSE


def test_deterministic_provider_returns_expected_response() -> None:
    provider = DeterministicConversationProvider()
    request = ConversationRequest(message="Status")

    response = provider.generate(request)

    assert response == ConversationResponse(message=DEFAULT_RESPONSE, provider=provider.name)


def test_conversation_orchestrator_routes_messages_to_provider() -> None:
    orchestrator = ConversationOrchestrator(provider=DeterministicConversationProvider())

    response = orchestrator.handle(ConversationRequest(message="Hello"))

    assert response.message == DEFAULT_RESPONSE
    assert response.provider == "deterministic-local"
