"""Where the Claude API key comes from, and what the app may do with it.

ESR-0061 WP5a (EIP-ESR0061-005 6.1 to 6.3, decisions K1 to K5). One object owns
the key's life: it reads the environment variable first (K3), then the
operating system's credential store; it sets and removes the stored key; and
it tells the Claude route whether a key exists, by switching that route's
health, so a change takes effect on the next request without a restart.

The key is never returned by anything here except `resolve`, which only the
Anthropic adapter calls, and it is never put into the process environment.
Every message this module produces is fixed text.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Callable, Mapping

from jarvis.shared.errors import ClientFacingValueError
from jarvis.shared.secret_store import SecretStore, SecretStoreError

logger = logging.getLogger(__name__)

ANTHROPIC_KEY_ENV_VAR = "ANTHROPIC_API_KEY"
SECRET_NAME = "anthropic-api-key"

SOURCE_ENVIRONMENT = "environment"
SOURCE_STORE = "store"
SOURCE_NONE = "none"

# A Claude key is "sk-ant-" then URL-safe characters. This is a format check
# only (K5): whether the key works is found out by the test button or the first
# real question.
_KEY_FORMAT = re.compile(r"^sk-ant-[A-Za-z0-9_\-]{16,400}$")

BAD_FORMAT_MESSAGE = "That does not look like a Claude API key. Copy it again from the Claude Console."
NO_STORE_MESSAGE = (
    "This computer has no secure place to keep the key. Set the ANTHROPIC_API_KEY setting instead, then restart JARVIS."
)
STORE_FAILED_MESSAGE = "The key could not be saved to this computer's credential store."


def looks_like_claude_key(value: str) -> bool:
    return bool(_KEY_FORMAT.match(value))


class ClaudeKeyManager:
    """Reads, stores and removes the Claude key, and keeps the route's health true."""

    def __init__(
        self,
        store: SecretStore,
        environ: Mapping[str, str],
        on_availability: Callable[[bool], None] | None = None,
    ) -> None:
        self._store = store
        self._environ = environ
        self._on_availability = on_availability

    def bind(self, on_availability: Callable[[bool], None]) -> None:
        """Set the function that switches the Claude route on or off. Called
        once the route exists; `apply` then makes it match reality."""

        self._on_availability = on_availability
        self.apply()

    # -- reading ----------------------------------------------------------------

    def _environment_key(self) -> str | None:
        value = self._environ.get(ANTHROPIC_KEY_ENV_VAR)
        return value.strip() if isinstance(value, str) and value.strip() else None

    def resolve(self) -> str | None:
        """The key to use right now: the environment variable if set, else the
        stored one. Called at each request by the adapter; nothing caches it."""

        found = self._environment_key()
        if found is not None:
            return found
        try:
            return self._store.get(SECRET_NAME)
        except SecretStoreError:
            return None

    def source(self) -> str:
        if self._environment_key() is not None:
            return SOURCE_ENVIRONMENT
        try:
            return SOURCE_STORE if self._store.get(SECRET_NAME) is not None else SOURCE_NONE
        except SecretStoreError:
            return SOURCE_NONE

    def status(self) -> dict[str, object]:
        """What the screen may know: whether there is a key and where it comes
        from. Never the key."""

        source = self.source()
        return {
            "configured": source != SOURCE_NONE,
            "source": source,
            "storeAvailable": self._store.available,
        }

    # -- changing ---------------------------------------------------------------

    def apply(self) -> None:
        """Make the Claude route's health match whether a key exists."""

        if self._on_availability is not None:
            self._on_availability(self.source() != SOURCE_NONE)

    def set_key(self, value: str) -> dict[str, object]:
        if not isinstance(value, str) or not looks_like_claude_key(value.strip()):
            raise ClientFacingValueError(BAD_FORMAT_MESSAGE)
        if not self._store.available:
            raise ClientFacingValueError(NO_STORE_MESSAGE)
        try:
            self._store.set(SECRET_NAME, value.strip())
        except SecretStoreError as exc:
            raise ClientFacingValueError(STORE_FAILED_MESSAGE) from exc
        self.apply()
        return self.status()

    def remove_key(self) -> dict[str, object]:
        try:
            self._store.delete(SECRET_NAME)
        except SecretStoreError as exc:
            raise ClientFacingValueError(STORE_FAILED_MESSAGE) from exc
        self.apply()
        return self.status()


__all__ = [
    "ANTHROPIC_KEY_ENV_VAR",
    "BAD_FORMAT_MESSAGE",
    "NO_STORE_MESSAGE",
    "SECRET_NAME",
    "SOURCE_ENVIRONMENT",
    "SOURCE_NONE",
    "SOURCE_STORE",
    "ClaudeKeyManager",
    "looks_like_claude_key",
]
