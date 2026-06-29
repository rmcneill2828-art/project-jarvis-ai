"""Conversation framework for JARVIS First Light."""

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)

DEFAULT_RESPONSE = "JARVIS Core online. AI provider integration is not enabled yet."
EMPTY_MESSAGE_RESPONSE = "JARVIS is listening. Type a message when you are ready."


@dataclass(frozen=True)
class ConversationRequest:
    """User request submitted to the conversation framework."""

    message: str


@dataclass(frozen=True)
class ConversationResponse:
    """Response returned by the conversation framework."""

    message: str
    provider: str


class ConversationProvider(Protocol):
    """Provider interface for local or future AI-backed responses."""

    name: str

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        """Generate a response for a conversation request."""


class DeterministicConversationProvider:
    """Offline deterministic provider used before AI integration exists."""

    name = "deterministic-local"

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        """Generate a local deterministic response."""

        if not request.message.strip():
            return ConversationResponse(message=EMPTY_MESSAGE_RESPONSE, provider=self.name)

        return ConversationResponse(message=DEFAULT_RESPONSE, provider=self.name)


class ConversationOrchestrator:
    """Route conversation requests to the configured provider."""

    def __init__(self, provider: ConversationProvider | None = None) -> None:
        self._provider = provider or DeterministicConversationProvider()

    def handle(self, request: ConversationRequest) -> ConversationResponse:
        """Handle a conversation request."""

        return self._provider.generate(request)


class ConversationService:
    """Conversation controller used by the GUI shell."""

    def __init__(self, orchestrator: ConversationOrchestrator | None = None) -> None:
        self._orchestrator = orchestrator or ConversationOrchestrator()

    def respond(self, message: str) -> str:
        """Return a response message without external AI providers."""

        return self.exchange(message).message

    def exchange(self, message: str) -> ConversationResponse:
        """Route a user message through the conversation framework."""

        cleaned_message = message.strip()
        LOGGER.info("User message received.")

        request = ConversationRequest(message=cleaned_message)
        response = self._orchestrator.handle(request)

        LOGGER.info("JARVIS response generated.")
        return response
