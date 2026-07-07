from dataclasses import dataclass

import pytest

from sentinel.core import SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import (
    ProviderHealth,
    ProviderOrchestrator,
    ProviderRoute,
)
from sentinel.providers import ProviderRequest, ProviderResponse


@dataclass(frozen=True)
class OrchestratorStubProvider:
    name: str
    capabilities: tuple[str, ...] = ("text-generation",)
    should_fail: bool = False

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        if self.should_fail:
            msg = f"{self.name} failed"
            raise RuntimeError(msg)
        return ProviderResponse(
            provider_name=self.name,
            content=f"{self.name}:{request.prompt}",
            capability=request.capability,
        )


def allowed_sentinel_response():
    gateway = SentinelTrustGateway()
    return gateway.evaluate(SentinelRequest(source="Guardian", intent="provider.request"))


def review_sentinel_response():
    gateway = SentinelTrustGateway()
    return gateway.evaluate(
        SentinelRequest(
            source="Guardian",
            intent="provider.request",
            requires_approval=True,
        )
    )


def test_provider_route_rejects_empty_capability() -> None:
    with pytest.raises(ValueError, match="Provider route capability must not be empty."):
        ProviderRoute(capability=" ", providers=("primary",))


def test_provider_route_rejects_empty_provider_list() -> None:
    with pytest.raises(ValueError, match="Provider route must contain at least one provider."):
        ProviderRoute(capability="text-generation", providers=())


def test_provider_route_rejects_empty_provider_name() -> None:
    with pytest.raises(ValueError, match="Provider route provider names must not be empty."):
        ProviderRoute(capability="text-generation", providers=(" ",))


def test_orchestrator_registers_provider_and_health() -> None:
    orchestrator = ProviderOrchestrator()
    provider = OrchestratorStubProvider(name="primary")

    registered = orchestrator.register_provider(provider)

    assert registered is provider
    assert orchestrator.health("primary") == ProviderHealth.HEALTHY


def test_orchestrator_replaces_provider_by_name() -> None:
    orchestrator = ProviderOrchestrator()
    first = OrchestratorStubProvider(name="primary", capabilities=("text-generation",))
    replacement = OrchestratorStubProvider(name="primary", capabilities=("summarisation",))

    orchestrator.register_provider(first)
    orchestrator.register_provider(replacement)

    assert orchestrator.eligible_providers("summarisation") == (replacement,)


def test_orchestrator_sets_provider_health() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(OrchestratorStubProvider(name="primary"))

    orchestrator.set_health("primary", ProviderHealth.DEGRADED)

    assert orchestrator.health("primary") == ProviderHealth.DEGRADED


def test_orchestrator_rejects_health_for_unknown_provider() -> None:
    orchestrator = ProviderOrchestrator()

    with pytest.raises(LookupError, match="Provider is not registered: missing."):
        orchestrator.set_health("missing", ProviderHealth.UNAVAILABLE)


def test_orchestrator_registers_valid_route() -> None:
    orchestrator = ProviderOrchestrator()
    primary = OrchestratorStubProvider(name="primary")
    fallback = OrchestratorStubProvider(name="fallback")
    orchestrator.register_provider(primary)
    orchestrator.register_provider(fallback)

    route = orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=("primary", "fallback"))
    )

    assert route.providers == ("primary", "fallback")
    assert orchestrator.eligible_providers("text-generation") == (primary, fallback)


def test_orchestrator_rejects_route_with_unknown_provider() -> None:
    orchestrator = ProviderOrchestrator()

    with pytest.raises(
        LookupError,
        match="Provider route references unregistered provider: missing.",
    ):
        orchestrator.register_route(
            ProviderRoute(capability="text-generation", providers=("missing",))
        )


def test_orchestrator_rejects_route_for_unsupported_capability() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(
        OrchestratorStubProvider(name="primary", capabilities=("text-generation",))
    )

    with pytest.raises(
        ValueError,
        match="Provider primary does not support capability: vision.",
    ):
        orchestrator.register_route(ProviderRoute(capability="vision", providers=("primary",)))


def test_orchestrator_excludes_unavailable_providers() -> None:
    orchestrator = ProviderOrchestrator()
    primary = OrchestratorStubProvider(name="primary")
    fallback = OrchestratorStubProvider(name="fallback")
    orchestrator.register_provider(primary, health=ProviderHealth.UNAVAILABLE)
    orchestrator.register_provider(fallback)

    assert orchestrator.eligible_providers("text-generation") == (fallback,)


def test_orchestrator_executes_first_healthy_provider() -> None:
    orchestrator = ProviderOrchestrator()
    primary = OrchestratorStubProvider(name="primary")
    fallback = OrchestratorStubProvider(name="fallback")
    orchestrator.register_provider(primary)
    orchestrator.register_provider(fallback)
    orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=("primary", "fallback"))
    )

    response = orchestrator.execute(
        allowed_sentinel_response(),
        ProviderRequest(prompt="hello"),
    )

    assert response.provider_response.provider_name == "primary"
    assert response.execution_record.selected_provider == "primary"
    assert response.execution_record.attempted_providers == ("primary",)
    assert response.execution_record.succeeded is True


def test_orchestrator_fails_over_to_secondary_provider() -> None:
    orchestrator = ProviderOrchestrator()
    primary = OrchestratorStubProvider(name="primary", should_fail=True)
    fallback = OrchestratorStubProvider(name="fallback")
    orchestrator.register_provider(primary)
    orchestrator.register_provider(fallback)
    orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=("primary", "fallback"))
    )

    response = orchestrator.execute(
        allowed_sentinel_response(),
        ProviderRequest(prompt="hello"),
    )

    assert response.provider_response.provider_name == "fallback"
    assert response.execution_record.attempted_providers == ("primary", "fallback")
    assert orchestrator.health("primary") == ProviderHealth.DEGRADED


def test_orchestrator_records_execution_history() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(OrchestratorStubProvider(name="primary"))

    response = orchestrator.execute(
        allowed_sentinel_response(),
        ProviderRequest(prompt="hello"),
    )

    assert orchestrator.history() == (response.execution_record,)


def test_orchestrator_blocks_execution_when_sentinel_does_not_allow() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(OrchestratorStubProvider(name="primary"))

    with pytest.raises(RuntimeError, match="Provider execution failed"):
        orchestrator.execute(
            review_sentinel_response(),
            ProviderRequest(prompt="hello"),
        )

    assert orchestrator.history()[0].succeeded is False
    assert orchestrator.history()[0].selected_provider is None


def test_orchestrator_raises_when_no_provider_supports_capability() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(OrchestratorStubProvider(name="primary"))

    with pytest.raises(RuntimeError, match="No healthy provider could execute the request."):
        orchestrator.execute(
            allowed_sentinel_response(),
            ProviderRequest(prompt="hello", capability="vision"),
        )

    assert orchestrator.history()[0].attempted_providers == ()


def test_orchestrator_raises_when_all_providers_unavailable() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(
        OrchestratorStubProvider(name="primary"),
        health=ProviderHealth.UNAVAILABLE,
    )

    with pytest.raises(RuntimeError, match="No healthy provider could execute the request."):
        orchestrator.execute(
            allowed_sentinel_response(),
            ProviderRequest(prompt="hello"),
        )

    assert orchestrator.history()[0].succeeded is False
