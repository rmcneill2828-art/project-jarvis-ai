"""Provider configuration primitives for Sentinel.

This module centralises provider configuration without storing secret values in
source-controlled configuration objects.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True)
class CredentialReference:
    """Reference to a credential stored outside source code."""

    environment_variable: str

    def __post_init__(self) -> None:
        if not self.environment_variable.strip():
            msg = "Credential environment variable must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class RetryPolicy:
    """Provider retry policy."""

    max_attempts: int = 1
    backoff_seconds: float = 0.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            msg = "Retry policy max attempts must be at least one."
            raise ValueError(msg)
        if self.backoff_seconds < 0:
            msg = "Retry policy backoff seconds must not be negative."
            raise ValueError(msg)


@dataclass(frozen=True)
class ProviderConfiguration:
    """Configuration for a Sentinel execution provider."""

    provider_name: str
    enabled: bool = True
    default_capability: str = "text-generation"
    default_model: str | None = None
    endpoint: str | None = None
    timeout_seconds: float = 30.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    credential: CredentialReference | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.provider_name.strip():
            msg = "Provider configuration name must not be empty."
            raise ValueError(msg)
        if not self.default_capability.strip():
            msg = "Provider configuration default capability must not be empty."
            raise ValueError(msg)
        if self.timeout_seconds <= 0:
            msg = "Provider configuration timeout seconds must be greater than zero."
            raise ValueError(msg)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


class ProviderConfigurationRegistry:
    """Register and resolve provider configuration."""

    def __init__(self) -> None:
        self._configurations: dict[str, ProviderConfiguration] = {}

    def register(self, configuration: ProviderConfiguration) -> ProviderConfiguration:
        """Register or replace provider configuration."""

        self._configurations[configuration.provider_name] = configuration
        return configuration

    def get(self, provider_name: str) -> ProviderConfiguration:
        """Return configuration for a provider."""

        if not provider_name.strip():
            msg = "Provider configuration lookup name must not be empty."
            raise ValueError(msg)
        try:
            return self._configurations[provider_name]
        except KeyError as exc:
            msg = f"No provider configuration registered for: {provider_name}."
            raise LookupError(msg) from exc

    def enabled(self) -> tuple[ProviderConfiguration, ...]:
        """Return enabled provider configurations."""

        return tuple(
            configuration
            for configuration in self._configurations.values()
            if configuration.enabled
        )

    def configurations(self) -> tuple[ProviderConfiguration, ...]:
        """Return all registered provider configurations."""

        return tuple(self._configurations.values())
