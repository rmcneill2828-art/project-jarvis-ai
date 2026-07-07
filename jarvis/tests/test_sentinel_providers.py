from dataclasses import dataclass

import pytest

from sentinel import (
    ProviderRegistry,
    ProviderRequest,
    ProviderResponse,
    SentinelDecisionOutcome,
    SentinelRequest,
    SentinelTrustGateway,
    execute_with_sentinel_decision,
)


@dataclass(frozen=True)
class StubProvider:
    name: str = "stub-provider"
    capabilities: tuple[str, ...] = ("text-generation",)

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider_name=self.name,
            content=f"executed:{request.prompt}",
            capability=request.capability,
            metadata={"source": "stub"},
        )


def test_provider_request_rejects_empty_prompt() -> None:
    with pytest.raises(ValueError, match="Provider request prompt must not be empty."):
        ProviderRequest(prompt=" ")


def test_provider_response_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="Provider response content must not be empty."):
        ProviderResponse(provider_name="stub-provider", content=" ")


def test_provider_registry_registers_provider() -> None:
    registry = ProviderRegistry()
    provider = StubProvider()

    registered = registry.register(provider)

    assert registered is provider
    assert registry.providers() == (provider,)


def test_provider_registry_replaces_provider_by_name() -> None:
    registry = ProviderRegistry()
    first = StubProvider(capabilities=("text-generation",))
    replacement = StubProvider(capabilities=("summarisation",))

    registry.register(first)
    registry.register(replacement)

    assert registry.providers() == (replacement,)
    assert registry.resolve("summarisation") is replacement


def test_provider_registry_resolves_by_capability() -> None:
    registry = ProviderRegistry()
    provider = StubProvider(capabilities=("text-generation", "summarisation"))

    registry.register(provider)

    assert registry.resolve("summarisation") is provider


def test_provider_registry_rejects_unknown_capability() -> None:
    registry = ProviderRegistry()
    registry.register(StubProvider())

    with pytest.raises(LookupError, match="No execution provider supports capability"):
        registry.resolve("vision")


def test_provider_registry_rejects_provider_without_capabilities() -> None:
    registry = ProviderRegistry()

    with pytest.raises(ValueError, match="Execution provider must expose at least one capability."):
        registry.register(StubProvider(capabilities=()))


def test_sentinel_allow_decision_executes_provider() -> None:
    gateway = SentinelTrustGateway()
    provider = StubProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(source="Guardian", intent="provider.request")
    )

    provider_response = execute_with_sentinel_decision(
        sentinel_response,
        provider,
        ProviderRequest(prompt="hello"),
    )

    assert sentinel_response.decision.outcome == SentinelDecisionOutcome.ALLOW
    assert provider_response.provider_name == "stub-provider"
    assert provider_response.content == "executed:hello"


def test_sentinel_review_decision_blocks_provider_execution() -> None:
    gateway = SentinelTrustGateway()
    provider = StubProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(
            source="Guardian",
            intent="execute.high_risk_action",
            requires_approval=True,
        )
    )

    with pytest.raises(PermissionError, match="Sentinel decision does not allow provider execution."):
        execute_with_sentinel_decision(
            sentinel_response,
            provider,
            ProviderRequest(prompt="open the pod bay doors"),
        )
