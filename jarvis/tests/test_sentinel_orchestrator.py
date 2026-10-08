from dataclasses import dataclass

import pytest

from sentinel.core import SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import (
    ProviderHealth,
    ProviderOrchestrator,
    ProviderRoute,
)
from sentinel.provider_config import RetryPolicy
from sentinel.providers import (
    DeadlineExceededError,
    ProviderDeclinedError,
    ProviderError,
    ProviderRequest,
    ProviderResponse,
    remaining_timeout,
)


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
    """EBG-0140 (ESR-0059 WP6): a non-ALLOW decision is refused up front.
    Previously it was caught as a provider failure, recorded as one and
    degraded every provider on the route."""

    called: list[str] = []

    @dataclass(frozen=True)
    class _RecordingProvider:
        name: str = "primary"
        capabilities: tuple[str, ...] = ("text-generation",)

        def execute(self, request: ProviderRequest) -> ProviderResponse:
            called.append(self.name)
            return ProviderResponse(provider_name=self.name, content="x", capability=request.capability)

    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_RecordingProvider())

    with pytest.raises(PermissionError, match="does not allow provider execution"):
        orchestrator.execute(
            review_sentinel_response(),
            ProviderRequest(prompt="hello"),
        )

    assert called == []
    assert orchestrator.health("primary") is ProviderHealth.HEALTHY
    assert orchestrator.history() == ()


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


# EBG-0139 (ESR-0059 WP5): the per-request deadline.


@dataclass(frozen=True)
class _SlowStubProvider:
    """Takes real time to fail, so a deadline can expire mid-failover."""

    name: str
    seconds: float
    capabilities: tuple[str, ...] = ("text-generation",)

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        import time

        time.sleep(self.seconds)
        msg = f"{self.name} timed out"
        raise RuntimeError(msg)


def test_orchestrator_attempts_no_provider_once_the_deadline_has_passed() -> None:
    import time

    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(OrchestratorStubProvider("primary"))
    request = ProviderRequest(prompt="hello", deadline=time.monotonic() - 1.0)

    with pytest.raises(RuntimeError, match="deadline reached"):
        orchestrator.execute(allowed_sentinel_response(), request)

    assert orchestrator.history()[-1].attempted_providers == ()
    # Skipped for time, not failed - health untouched.
    assert orchestrator.health("primary") is ProviderHealth.HEALTHY


def test_orchestrator_stops_failover_when_the_deadline_expires_mid_chain() -> None:
    import time

    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_SlowStubProvider("primary", seconds=0.3))
    orchestrator.register_provider(OrchestratorStubProvider("secondary"))
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("primary", "secondary")))
    request = ProviderRequest(prompt="hello", deadline=time.monotonic() + 0.1)

    with pytest.raises(RuntimeError, match="deadline reached after attempting: primary"):
        orchestrator.execute(allowed_sentinel_response(), request)

    assert orchestrator.history()[-1].attempted_providers == ("primary",)
    assert orchestrator.health("secondary") is ProviderHealth.HEALTHY


class _DeadlinePassedInsideProvider:
    """Raises what `remaining_timeout()` raises when the deadline passes
    between the orchestrator's own check and the provider's."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.capabilities = ("text-generation",)
        self.calls = 0

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        msg = "Request deadline reached before the provider call could start."
        raise DeadlineExceededError(msg)


def test_deadline_passing_inside_a_provider_is_not_a_provider_fault() -> None:
    # EBG-0156 (ESR-0060 WP1b): this used to mark the provider DEGRADED and
    # open its circuit for the cooldown, excluding a healthy provider.
    import time

    orchestrator = ProviderOrchestrator()
    primary = _DeadlinePassedInsideProvider("primary")
    secondary = OrchestratorStubProvider("secondary")
    orchestrator.register_provider(primary)
    orchestrator.register_provider(secondary)
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("primary", "secondary")))
    request = ProviderRequest(prompt="hello", deadline=time.monotonic() + 60.0)

    with pytest.raises(RuntimeError, match="deadline reached after attempting: primary"):
        orchestrator.execute(allowed_sentinel_response(), request)

    assert primary.calls == 1  # not retried
    assert orchestrator.health("primary") is ProviderHealth.HEALTHY
    assert orchestrator.history()[-1].attempted_providers == ("primary",)
    # Circuit still closed: the next request goes straight to the primary again.
    with pytest.raises(RuntimeError, match="deadline reached"):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hello", deadline=time.monotonic() + 60.0))
    assert primary.calls == 2


def test_remaining_timeout_raises_a_deadline_error_that_is_still_a_runtime_error() -> None:
    import time

    with pytest.raises(DeadlineExceededError) as excinfo:
        remaining_timeout(30.0, ProviderRequest(prompt="hello", deadline=time.monotonic() - 1.0))

    assert isinstance(excinfo.value, RuntimeError)


def test_orchestrator_without_a_deadline_still_fails_over_as_before() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_SlowStubProvider("primary", seconds=0.05))
    orchestrator.register_provider(OrchestratorStubProvider("secondary"))
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("primary", "secondary")))

    result = orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hello"))

    assert result.provider_response.content == "secondary:hello"


# EBG-0140 (ESR-0059 WP6): retry, backoff and circuit breaking.



class _ScriptedProvider:
    """Fails with each scripted error in turn, then succeeds."""

    def __init__(self, name: str, errors: list[Exception], retry_policy: RetryPolicy | None = None) -> None:
        self.name = name
        self.capabilities = ("text-generation",)
        self._errors = list(errors)
        self.calls = 0
        if retry_policy is not None:
            self.retry_policy = retry_policy

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        if self._errors:
            raise self._errors.pop(0)
        return ProviderResponse(provider_name=self.name, content=f"{self.name} ok", capability=request.capability)


class _FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


def _resilient_orchestrator(*providers, cooldown: float = 30.0):
    clock = _FakeClock()
    orchestrator = ProviderOrchestrator(
        circuit_cooldown_seconds=cooldown, clock=clock, sleep=clock.sleep, random_fraction=lambda: 0.5
    )
    for provider in providers:
        orchestrator.register_provider(provider)
    orchestrator.register_route(
        ProviderRoute(capability="text-generation", providers=tuple(p.name for p in providers))
    )
    return orchestrator, clock


def test_transient_failure_is_retried_with_backoff_then_succeeds() -> None:
    primary = _ScriptedProvider(
        "primary", [ProviderError("503", transient=True)], retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=1.0)
    )
    orchestrator, clock = _resilient_orchestrator(primary)

    result = orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert result.provider_response.content == "primary ok"
    assert primary.calls == 2
    assert clock.slept == [1.0]  # backoff 1.0 x 2**0 x (0.5 + 0.5 jitter)
    assert orchestrator.audit_events()[-1].metadata["attempts"] == "2"


def test_permanent_failure_is_not_retried_and_fails_over() -> None:
    primary = _ScriptedProvider(
        "primary", [ProviderError("401", transient=False)], retry_policy=RetryPolicy(max_attempts=3, backoff_seconds=1.0)
    )
    secondary = _ScriptedProvider("secondary", [])
    orchestrator, clock = _resilient_orchestrator(primary, secondary)

    result = orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert result.provider_response.content == "secondary ok"
    assert primary.calls == 1
    assert clock.slept == []


def test_plain_runtime_errors_are_treated_as_not_transient() -> None:
    primary = _ScriptedProvider("primary", [RuntimeError("bad shape")], retry_policy=RetryPolicy(max_attempts=3))
    secondary = _ScriptedProvider("secondary", [])
    orchestrator, _ = _resilient_orchestrator(primary, secondary)

    orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert primary.calls == 1


def test_retries_stop_at_max_attempts_with_exponential_backoff() -> None:
    errors = [ProviderError("503", transient=True) for _ in range(5)]
    primary = _ScriptedProvider("primary", errors, retry_policy=RetryPolicy(max_attempts=3, backoff_seconds=1.0))
    orchestrator, clock = _resilient_orchestrator(primary)

    with pytest.raises(RuntimeError, match=r"Provider execution failed: ProviderError \(transient\)$"):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert primary.calls == 3
    assert clock.slept == [1.0, 2.0]


def test_no_retry_when_the_backoff_would_pass_the_deadline() -> None:
    import time

    primary = _ScriptedProvider(
        "primary", [ProviderError("503", transient=True)], retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=60.0)
    )
    orchestrator, clock = _resilient_orchestrator(primary)

    with pytest.raises(RuntimeError):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi", deadline=time.monotonic() + 5.0))

    assert primary.calls == 1
    assert clock.slept == []


def test_failed_provider_is_skipped_while_its_circuit_is_open_then_retried() -> None:
    primary = _ScriptedProvider("primary", [ProviderError("down", transient=False)])
    secondary = _ScriptedProvider("secondary", [])
    orchestrator, clock = _resilient_orchestrator(primary, secondary, cooldown=30.0)

    orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="one"))
    assert primary.calls == 1
    assert orchestrator.health("primary") is ProviderHealth.DEGRADED

    clock.now += 10.0  # still cooling down
    result = orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="two"))
    assert primary.calls == 1  # skipped, did not cost its timeout again
    assert result.provider_response.provider_name == "secondary"

    clock.now += 25.0  # cooldown over - tried again, and now it works
    result = orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="three"))
    assert primary.calls == 2
    assert result.provider_response.provider_name == "primary"
    assert orchestrator.health("primary") is ProviderHealth.HEALTHY


def test_every_provider_cooling_down_fails_fast_without_calls() -> None:
    primary = _ScriptedProvider("primary", [ProviderError("down", transient=False)])
    orchestrator, _ = _resilient_orchestrator(primary)

    with pytest.raises(RuntimeError):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="one"))
    with pytest.raises(RuntimeError, match="cooling down after a recent failure: primary"):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="two"))

    assert primary.calls == 1


def test_circuit_breaker_leaves_operator_set_health_alone() -> None:
    primary = _ScriptedProvider("primary", [])
    orchestrator, _ = _resilient_orchestrator(primary)
    orchestrator.set_health("primary", ProviderHealth.UNAVAILABLE)

    with pytest.raises(RuntimeError, match="No healthy provider"):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert primary.calls == 0
    assert orchestrator.health("primary") is ProviderHealth.UNAVAILABLE


def test_negative_circuit_cooldown_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        ProviderOrchestrator(circuit_cooldown_seconds=-1.0)


def test_failure_reason_carries_no_free_text_but_the_log_keeps_it(caplog) -> None:
    """ESR-0061 WP2a (EBG-0157 item 2): the durable audit reason names the
    type and transience only; the message is logged locally for diagnosis."""

    errors = [ProviderError("upstream said: secret body", transient=False)]
    primary = _ScriptedProvider("primary", errors, retry_policy=RetryPolicy(max_attempts=1))
    orchestrator, _ = _resilient_orchestrator(primary)

    with caplog.at_level("WARNING"), pytest.raises(RuntimeError) as excinfo:
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hi"))

    assert str(excinfo.value) == "Provider execution failed: ProviderError (permanent)"
    assert "secret" not in orchestrator.history()[-1].reason
    assert "upstream said: secret body" in caplog.text


class _DecliningProvider:
    def __init__(self, name: str) -> None:
        self.name = name
        self.capabilities = ("text-generation",)
        self.calls = 0

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        msg = "Anthropic declined to answer this request (cyber)."
        raise ProviderDeclinedError(msg)


def test_a_decline_is_not_retried_not_failed_over_and_not_a_provider_fault() -> None:
    # ESR-0061 WP3a: a safety decline is a decision, not an outage. Asking the
    # next provider would let the decline be evaded by failover.
    orchestrator = ProviderOrchestrator()
    declining = _DecliningProvider("primary")
    secondary = OrchestratorStubProvider("secondary")
    orchestrator.register_provider(declining)
    orchestrator.register_provider(secondary)
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("primary", "secondary")))

    with pytest.raises(ProviderDeclinedError, match="declined the request: primary"):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hello"))

    assert declining.calls == 1  # not retried
    assert orchestrator.health("primary") is ProviderHealth.HEALTHY
    assert orchestrator.health("secondary") is ProviderHealth.HEALTHY
    record = orchestrator.history()[-1]
    assert record.attempted_providers == ("primary",)  # secondary never asked
    assert record.succeeded is False
    # No circuit: the very next request goes to the primary again.
    with pytest.raises(ProviderDeclinedError):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="again"))
    assert declining.calls == 2


def test_a_decline_is_audited_without_the_provider_message() -> None:
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_DecliningProvider("primary"))

    with pytest.raises(ProviderDeclinedError):
        orchestrator.execute(allowed_sentinel_response(), ProviderRequest(prompt="hello"))

    event = orchestrator.audit_events()[-1]
    assert event.outcome == "failed"
    assert "declined" in event.summary
    assert "cyber" not in event.summary


def test_a_decline_is_still_a_runtime_error_for_existing_callers() -> None:
    assert issubclass(ProviderDeclinedError, RuntimeError)
