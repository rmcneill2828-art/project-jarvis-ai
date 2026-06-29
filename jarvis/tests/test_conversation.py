from jarvis.interfaces.conversation import DEFAULT_RESPONSE, ConversationService


def test_conversation_returns_deterministic_response() -> None:
    conversation = ConversationService()

    assert conversation.respond("Hello JARVIS") == DEFAULT_RESPONSE


def test_conversation_handles_empty_message() -> None:
    conversation = ConversationService()

    assert conversation.respond("   ") == "JARVIS is listening. Type a message when you are ready."
