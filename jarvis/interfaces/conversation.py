"""Deterministic conversation layer for JARVIS First Light."""

import logging

LOGGER = logging.getLogger(__name__)

DEFAULT_RESPONSE = "JARVIS Core online. AI provider integration is not enabled yet."


class ConversationService:
    """Handle local deterministic conversation responses."""

    def respond(self, message: str) -> str:
        """Return a deterministic response without external AI providers."""

        cleaned_message = message.strip()
        LOGGER.info("User message received.")

        if not cleaned_message:
            response = "JARVIS is listening. Type a message when you are ready."
        else:
            response = DEFAULT_RESPONSE

        LOGGER.info("JARVIS response generated.")
        return response
