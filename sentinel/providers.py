"""Sentinel provider abstraction.

Providers fulfil approved execution requests after Sentinel has evaluated the
trust boundary. This module defines contracts only; concrete AI providers are
implemented separately.
"""

import time
from dataclasses import dataclass, field
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelResponse


@dataclass(frozen=True)
class ProviderRequest:
    """Provider-neutral request submitted after Sentinel approval."""

    prompt: str
    capability: str = "text-generation"
    metadata: dict[str, str] = field(default_factory=dict)
    system_prompt: str | None = None
    # Optional `time.monotonic()` instant by which the whole request - every
    # provider tried for it, failover included - must finish (EBG-0139,
    # ESR-0059 WP5). None means no overall deadline: each provider's own
    # configured timeout alone applies, exactly as before.
    deadline: float | None = None

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            msg = "Provider request prompt must not be empty."
            raise ValueError(msg)
        if not self.capability.strip():
            msg = "Provider request capability must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class ProviderResponse:
    """Provider-neutral response returned by an execution provider."""

    provider_name: str
    content: str
    capability: str = "text-generation"
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.provider_name.strip():
            msg = "Provider response provider name must not be empty."
            raise ValueError(msg)
        if not self.content.strip():
            msg = "Provider response content must not be empty."
            raise ValueError(msg)
        if not self.capability.strip():
            msg = "Provider response capability must not be empty."
            raise ValueError(msg)


# HTTP statuses worth retrying: the request was fine, the service was not
# (EBG-0140, ESR-0059 WP6). 401/403/404 and other 4xx are permanent - a bad
# key or model name will not fix itself between attempts.
TRANSIENT_HTTP_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class ProviderError(RuntimeError):
    """A provider call failure that says whether retrying could help.

    Subclasses `RuntimeError`, every adapter's established failure type, so
    existing callers and tests that expect `RuntimeError` are unaffected.
    `transient` is True for rate limits, server errors, timeouts and
    network failures; False for anything retrying cannot fix. A plain
    `RuntimeError` from a provider is treated as not transient.
    """

    def __init__(self, message: str, *, transient: bool) -> None:
        super().__init__(message)
        self.transient = transient


def remaining_timeout(configured_timeout_seconds: float, request: ProviderRequest) -> float:
    """Return the timeout a provider call may use for `request`.

    The provider's own configured timeout, capped by whatever remains of the
    request's overall deadline (EBG-0139, ESR-0059 WP5), so a late provider
    in a failover chain cannot run past the turn budget. Raises
    `RuntimeError` - every adapter's established failure type, which
    `ProviderOrchestrator` handles - when the deadline has already passed.
    """

    if request.deadline is None:
        return configured_timeout_seconds
    remaining = request.deadline - time.monotonic()
    if remaining <= 0:
        msg = "Request deadline reached before the provider call could start."
        raise RuntimeError(msg)
    return min(configured_timeout_seconds, remaining)


class ExecutionProvider(Protocol):
    """Protocol implemented by Sentinel execution providers."""

    @property
    def name(self) -> str:
        """Return provider name."""

    @property
    def capabilities(self) -> tuple[str, ...]:
        """Return provider capabilities."""

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        """Execute a provider request."""


class ProviderRegistry:
    """Register and resolve execution providers."""

    def __init__(self) -> None:
        self._providers: dict[str, ExecutionProvider] = {}

    def register(self, provider: ExecutionProvider) -> ExecutionProvider:
        """Register or replace an execution provider."""

        if not provider.name.strip():
            msg = "Execution provider name must not be empty."
            raise ValueError(msg)
        if not provider.capabilities:
            msg = "Execution provider must expose at least one capability."
            raise ValueError(msg)
        self._providers[provider.name] = provider
        return provider

    def resolve(self, capability: str) -> ExecutionProvider:
        """Resolve the first provider supporting a capability."""

        if not capability.strip():
            msg = "Provider capability must not be empty."
            raise ValueError(msg)

        for provider in self._providers.values():
            if capability in provider.capabilities:
                return provider

        msg = f"No execution provider supports capability: {capability}."
        raise LookupError(msg)

    def providers(self) -> tuple[ExecutionProvider, ...]:
        """Return registered providers."""

        return tuple(self._providers.values())


def execute_with_sentinel_decision(
    sentinel_response: SentinelResponse,
    provider: ExecutionProvider,
    request: ProviderRequest,
) -> ProviderResponse:
    """Execute a provider request only when Sentinel allowed execution."""

    if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
        msg = "Sentinel decision does not allow provider execution."
        raise PermissionError(msg)
    return provider.execute(request)
