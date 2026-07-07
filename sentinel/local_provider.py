"""Deterministic local provider for Sentinel integration testing.

This provider gives Sentinel a first concrete execution provider without adding
network access, credentials or third-party SDK dependencies.
"""

from dataclasses import dataclass

from sentinel.providers import ProviderRequest, ProviderResponse


@dataclass(frozen=True)
class LocalEchoProvider:
    """Simple local provider that returns deterministic text responses."""

    name: str = "local-echo"
    capabilities: tuple[str, ...] = ("text-generation", "echo")

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        """Return a deterministic response for a provider request."""

        return ProviderResponse(
            provider_name=self.name,
            content=f"{self.name}: {request.prompt}",
            capability=request.capability,
            metadata={"provider_type": "local", "deterministic": "true"},
        )


def create_local_provider_registry() -> object:
    """Create a provider registry containing the local echo provider."""

    from sentinel.providers import ProviderRegistry

    registry = ProviderRegistry()
    registry.register(LocalEchoProvider())
    return registry
