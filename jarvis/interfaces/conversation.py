"""Conversation framework for JARVIS First Light."""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

LOGGER = logging.getLogger(__name__)

DEFAULT_RESPONSE = "JARVIS Core online. AI provider integration is not enabled yet."
EMPTY_MESSAGE_RESPONSE = "JARVIS is listening. Type a message when you are ready."
TRANSCRIPT_FORMAT_MARKDOWN = "markdown"
TRANSCRIPT_FORMAT_TEXT = "text"


@dataclass(frozen=True)
class ConversationRequest:
    """User request submitted to the conversation framework."""

    message: str


@dataclass(frozen=True)
class ConversationResponse:
    """Response returned by the conversation framework."""

    message: str
    provider: str


@dataclass(frozen=True)
class ConversationExchange:
    """Single in-memory conversation exchange."""

    sequence_number: int
    user_message: str
    jarvis_response: str
    provider: str
    timestamp: datetime


@dataclass(frozen=True)
class ConversationMetadata:
    """Current in-memory conversation session metadata."""

    session_id: str
    provider: str
    exchange_count: int


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

    @property
    def provider_name(self) -> str:
        """Return the configured provider name."""

        return self._provider.name


class ConversationService:
    """Conversation controller used by the GUI shell."""

    def __init__(
        self,
        orchestrator: ConversationOrchestrator | None = None,
        session_id: str | None = None,
    ) -> None:
        self._orchestrator = orchestrator or ConversationOrchestrator()
        self._session_id = session_id or uuid4().hex
        self._transcript: list[ConversationExchange] = []

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
        self._record_exchange(cleaned_message, response)
        return response

    def metadata(self) -> ConversationMetadata:
        """Return current conversation session metadata."""

        return ConversationMetadata(
            session_id=self._session_id,
            provider=self.provider_name,
            exchange_count=self.exchange_count,
        )

    def transcript(self) -> tuple[ConversationExchange, ...]:
        """Return the in-memory transcript for the current session."""

        return tuple(self._transcript)

    def clear_conversation(self) -> None:
        """Clear the current session transcript while preserving the session identifier."""

        self._transcript.clear()

    def new_conversation(self, session_id: str | None = None) -> str:
        """Start a new in-memory conversation session and return its identifier."""

        self._session_id = session_id or uuid4().hex
        self.clear_conversation()
        return self._session_id

    def export_transcript(self, export_format: str = TRANSCRIPT_FORMAT_MARKDOWN) -> str:
        """Export the current session transcript in a supported text format."""

        normalized_format = export_format.lower().strip()

        if normalized_format == TRANSCRIPT_FORMAT_MARKDOWN:
            return self._export_markdown()

        if normalized_format == TRANSCRIPT_FORMAT_TEXT:
            return self._export_text()

        msg = f"Unsupported transcript export format: {export_format}"
        raise ValueError(msg)

    @property
    def session_id(self) -> str:
        """Return the current conversation session identifier."""

        return self._session_id

    @property
    def provider_name(self) -> str:
        """Return the active conversation provider name."""

        return self._orchestrator.provider_name

    @property
    def exchange_count(self) -> int:
        """Return the number of recorded exchanges in the current session."""

        return len(self._transcript)

    def _record_exchange(self, user_message: str, response: ConversationResponse) -> None:
        self._transcript.append(
            ConversationExchange(
                sequence_number=len(self._transcript) + 1,
                user_message=user_message,
                jarvis_response=response.message,
                provider=response.provider,
                timestamp=datetime.now(UTC),
            )
        )

    def _export_markdown(self) -> str:
        metadata = self.metadata()
        lines = [
            "# JARVIS Conversation Transcript",
            "",
            f"- Session: `{metadata.session_id}`",
            f"- Provider: `{metadata.provider}`",
            f"- Exchanges: {metadata.exchange_count}",
            "",
        ]

        for exchange in self._transcript:
            lines.extend(
                [
                    f"## Exchange {exchange.sequence_number}",
                    "",
                    f"- Timestamp: `{_format_timestamp(exchange.timestamp)}`",
                    f"- Provider: `{exchange.provider}`",
                    "",
                    f"**User:** {exchange.user_message}",
                    "",
                    f"**JARVIS:** {exchange.jarvis_response}",
                    "",
                ]
            )

        return "\n".join(lines).rstrip() + "\n"

    def _export_text(self) -> str:
        metadata = self.metadata()
        lines = [
            "JARVIS Conversation Transcript",
            f"Session: {metadata.session_id}",
            f"Provider: {metadata.provider}",
            f"Exchanges: {metadata.exchange_count}",
            "",
        ]

        for exchange in self._transcript:
            lines.extend(
                [
                    f"Exchange {exchange.sequence_number}",
                    f"Timestamp: {_format_timestamp(exchange.timestamp)}",
                    f"Provider: {exchange.provider}",
                    f"User: {exchange.user_message}",
                    f"JARVIS: {exchange.jarvis_response}",
                    "",
                ]
            )

        return "\n".join(lines).rstrip() + "\n"


def _format_timestamp(timestamp: datetime) -> str:
    return timestamp.astimezone(UTC).isoformat()
