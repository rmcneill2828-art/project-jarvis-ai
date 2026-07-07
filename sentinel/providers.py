"""Sentinel provider abstraction.

Providers fulfil approved execution requests after Sentinel has evaluated the
trust boundary. This module defines contracts only; concrete AI providers are
implemented separately.
"""

from dataclasses import dataclass, field
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelResponse


@dataclass(frozen=True)
class ProviderRequest:
    """Provider-neutral request submitted after Sentinel approval."""

    prompt: str
    capability: str = "text-generation"
    metadata: dict[str, str] = field(default_factory=dict)

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
