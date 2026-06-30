from jarvis.interfaces.conversation import (
    DEFAULT_RESPONSE,
    EMPTY_MESSAGE_RESPONSE,
    TRANSCRIPT_FORMAT_MARKDOWN,
    TRANSCRIPT_FORMAT_TEXT,
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


def test_conversation_records_exchange_metadata() -> None:
    conversation = ConversationService(session_id="test-session")

    response = conversation.exchange("Hello JARVIS")

    transcript = conversation.transcript()
    metadata = conversation.metadata()

    assert response.message == DEFAULT_RESPONSE
    assert metadata.session_id == "test-session"
    assert metadata.provider == "deterministic-local"
    assert metadata.exchange_count == 1
    assert conversation.exchange_count == 1
    assert len(transcript) == 1
    assert transcript[0].sequence_number == 1
    assert transcript[0].user_message == "Hello JARVIS"
    assert transcript[0].jarvis_response == DEFAULT_RESPONSE
    assert transcript[0].provider == "deterministic-local"
    assert transcript[0].timestamp.tzinfo is not None


def test_conversation_records_empty_message_exchange() -> None:
    conversation = ConversationService(session_id="test-session")

    conversation.respond("   ")

    transcript = conversation.transcript()

    assert conversation.exchange_count == 1
    assert transcript[0].sequence_number == 1
    assert transcript[0].user_message == ""
    assert transcript[0].jarvis_response == EMPTY_MESSAGE_RESPONSE


def test_conversation_transcript_is_immutable_snapshot() -> None:
    conversation = ConversationService(session_id="test-session")

    conversation.respond("First")
    first_snapshot = conversation.transcript()
    conversation.respond("Second")

    assert len(first_snapshot) == 1
    assert conversation.exchange_count == 2
    assert conversation.transcript()[1].sequence_number == 2


def test_clear_conversation_preserves_session_metadata() -> None:
    conversation = ConversationService(session_id="test-session")
    conversation.respond("Hello")

    conversation.clear_conversation()

    metadata = conversation.metadata()
    assert metadata.session_id == "test-session"
    assert metadata.provider == "deterministic-local"
    assert metadata.exchange_count == 0
    assert conversation.transcript() == ()


def test_new_conversation_resets_transcript_and_session_id() -> None:
    conversation = ConversationService(session_id="old-session")
    conversation.respond("Hello")

    new_session_id = conversation.new_conversation(session_id="new-session")

    metadata = conversation.metadata()
    assert new_session_id == "new-session"
    assert metadata.session_id == "new-session"
    assert metadata.exchange_count == 0
    assert conversation.transcript() == ()


def test_export_markdown_transcript_includes_exchange_context() -> None:
    conversation = ConversationService(session_id="test-session")
    conversation.respond("Hello JARVIS")

    exported = conversation.export_transcript(TRANSCRIPT_FORMAT_MARKDOWN)

    assert "# JARVIS Conversation Transcript" in exported
    assert "- Session: `test-session`" in exported
    assert "- Provider: `deterministic-local`" in exported
    assert "- Exchanges: 1" in exported
    assert "## Exchange 1" in exported
    assert "- Timestamp: `" in exported
    assert "**User:** Hello JARVIS" in exported
    assert f"**JARVIS:** {DEFAULT_RESPONSE}" in exported


def test_export_text_transcript_includes_exchange_context() -> None:
    conversation = ConversationService(session_id="test-session")
    conversation.respond("Hello JARVIS")

    exported = conversation.export_transcript(TRANSCRIPT_FORMAT_TEXT)

    assert "JARVIS Conversation Transcript" in exported
    assert "Session: test-session" in exported
    assert "Provider: deterministic-local" in exported
    assert "Exchanges: 1" in exported
    assert "Exchange 1" in exported
    assert "Timestamp: " in exported
    assert "User: Hello JARVIS" in exported
    assert f"JARVIS: {DEFAULT_RESPONSE}" in exported


def test_export_transcript_rejects_unsupported_format() -> None:
    conversation = ConversationService(session_id="test-session")

    try:
        conversation.export_transcript("pdf")
    except ValueError as error:
        assert "Unsupported transcript export format" in str(error)
    else:
        raise AssertionError("Expected unsupported export format to raise ValueError.")
