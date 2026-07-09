from jarvis import (
    GuardianDiagnosticEvent,
    GuardianRuntime,
    GuardianRuntimeConfig,
    GuardianRuntimeState,
    GuardianRuntimeStatus,
    GuardianServiceSnapshot,
    JarvisService,
    ServiceHealth,
    ServiceStatus,
)
from jarvis.guardian.runtime import NOT_CONNECTED_RESPONSE, NOT_RUNNING_RESPONSE
from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from sentinel.core import SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.providers import ProviderRequest, ProviderResponse


class _StubConversationProvider:
    """Minimal ConversationProvider double for boundary-behaviour tests."""

    name = "stub-conversation"

    def __init__(self) -> None:
        self.received: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.received.append(request)
        return ConversationResponse(message=f"stub: {request.message}", provider=self.name)


class _StubSentinelProvider:
    name = "stub-sentinel-provider"

    @property
    def capabilities(self) -> tuple[str, ...]:
        return ("text-generation",)

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider_name=self.name,
            content=f"echo: {request.prompt}",
            capability=request.capability,
        )


def test_guardian_diagnostic_event_requires_timezone_aware_timestamp() -> None:
    from datetime import datetime

    try:
        GuardianDiagnosticEvent(
            name="guardian.test",
            state=GuardianRuntimeState.STOPPED,
            message="Test event.",
            occurred_at=datetime(2026, 1, 1),
        )
    except ValueError as exc:
        assert str(exc) == "Guardian diagnostic event timestamp must be timezone-aware."
    else:
        raise AssertionError("Expected naive Guardian event timestamp to be rejected.")


def test_guardian_runtime_starts_and_stops_without_enabling_future_capabilities() -> None:
    runtime = GuardianRuntime()

    assert runtime.status() == GuardianRuntimeState.STOPPED
    assert runtime.start() == GuardianRuntimeState.RUNNING
    assert runtime.services()["Guardian Runtime"].status == ServiceStatus.ONLINE
    assert runtime.services()["Guardian Runtime"].health == ServiceHealth.HEALTHY
    assert runtime.services()["Guardian Memory Boundary"].status == ServiceStatus.UNAVAILABLE
    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE

    assert runtime.stop() == GuardianRuntimeState.STOPPED
    assert runtime.services()["Guardian Runtime"].status == ServiceStatus.OFFLINE


def test_guardian_runtime_uses_safe_configuration_defaults() -> None:
    runtime = GuardianRuntime()

    assert runtime.config == GuardianRuntimeConfig()
    assert runtime.config.runtime_name == "Guardian"
    assert runtime.config.persistence_enabled is False
    assert runtime.config.diagnostics_enabled is True


def test_guardian_runtime_rejects_empty_runtime_name() -> None:
    try:
        GuardianRuntimeConfig(runtime_name=" ")
    except ValueError as exc:
        assert str(exc) == "Guardian runtime name must not be empty."
    else:
        raise AssertionError("Expected empty Guardian runtime name to be rejected.")


def test_guardian_runtime_registers_services_and_records_diagnostics() -> None:
    runtime = GuardianRuntime()
    service = JarvisService(
        name="Guardian Test Service",
        status=ServiceStatus.UNAVAILABLE,
        capabilities=("guardian.test",),
    )

    registered = runtime.register_service(service)

    assert registered is service
    assert runtime.services()["Guardian Test Service"].supports("guardian.test")
    assert runtime.diagnostics()[-1].name == "guardian.service_registered"
    assert "Guardian Test Service" in runtime.diagnostics()[-1].message


def test_guardian_runtime_diagnostics_are_available_as_snapshots() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    diagnostics = runtime.diagnostics()

    assert all(isinstance(event, GuardianDiagnosticEvent) for event in diagnostics)
    assert diagnostics[0].name == "guardian.initialised"
    assert diagnostics[-1].state == GuardianRuntimeState.RUNNING
    assert diagnostics[0].occurred_at.tzinfo is not None
    assert diagnostics[-1].health == ServiceHealth.HEALTHY


def test_guardian_runtime_status_snapshot_reports_initial_state() -> None:
    runtime = GuardianRuntime()

    snapshot = runtime.status_snapshot()

    assert isinstance(snapshot, GuardianRuntimeStatus)
    assert snapshot.state == GuardianRuntimeState.STOPPED
    assert snapshot.runtime_health == ServiceHealth.UNKNOWN
    assert snapshot.runtime_name == "Guardian"
    assert snapshot.persistence_enabled is False
    assert snapshot.diagnostics_enabled is True
    assert snapshot.diagnostic_count == 1
    assert len(snapshot.events) == 1
    assert snapshot.latest_diagnostic is not None
    assert snapshot.latest_diagnostic.name == "guardian.initialised"
    assert snapshot.services["Guardian Runtime"].status == ServiceStatus.OFFLINE
    assert snapshot.services["Guardian Memory Boundary"].status == ServiceStatus.UNAVAILABLE
    assert snapshot.services["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE


def test_guardian_runtime_status_snapshot_reports_running_state() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    snapshot = runtime.status_snapshot()

    assert snapshot.state == GuardianRuntimeState.RUNNING
    assert snapshot.runtime_health == ServiceHealth.HEALTHY
    assert snapshot.services["Guardian Runtime"].status == ServiceStatus.ONLINE
    assert snapshot.services["Guardian Runtime"].health == ServiceHealth.HEALTHY
    assert snapshot.latest_diagnostic is not None
    assert snapshot.latest_diagnostic.name == "guardian.running"


def test_guardian_runtime_status_snapshot_reports_stopped_state_after_stop() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    runtime.stop()
    snapshot = runtime.status_snapshot()

    assert snapshot.state == GuardianRuntimeState.STOPPED
    assert snapshot.runtime_health == ServiceHealth.UNKNOWN
    assert snapshot.services["Guardian Runtime"].status == ServiceStatus.OFFLINE
    assert snapshot.latest_diagnostic is not None
    assert snapshot.latest_diagnostic.name == "guardian.stopped"


def test_guardian_runtime_status_snapshot_contains_service_snapshots() -> None:
    runtime = GuardianRuntime()

    snapshot = runtime.status_snapshot()

    guardian_service = snapshot.services["Guardian Runtime"]
    assert isinstance(guardian_service, GuardianServiceSnapshot)
    assert guardian_service.supports("guardian.lifecycle")


def test_guardian_runtime_status_snapshot_is_not_a_live_service_view() -> None:
    runtime = GuardianRuntime()
    snapshot = runtime.status_snapshot()

    runtime.start()

    assert snapshot.state == GuardianRuntimeState.STOPPED
    assert snapshot.services["Guardian Runtime"].status == ServiceStatus.OFFLINE
    assert runtime.status_snapshot().services["Guardian Runtime"].status == ServiceStatus.ONLINE


def test_guardian_runtime_events_are_queryable_by_limit() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    runtime.stop()
    events = runtime.events(limit=2)

    assert [event.name for event in events] == ["guardian.running", "guardian.stopped"]
    assert all(event.occurred_at.tzinfo is not None for event in events)


def test_guardian_runtime_diagnostics_are_queryable_by_name() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    running_events = runtime.diagnostics(name="guardian.running")

    assert len(running_events) == 1
    assert running_events[0].state == GuardianRuntimeState.RUNNING


def test_guardian_runtime_rejects_invalid_event_query_limit() -> None:
    runtime = GuardianRuntime()

    try:
        runtime.events(limit=0)
    except ValueError as exc:
        assert str(exc) == "Guardian diagnostic query limit must be greater than zero."
    else:
        raise AssertionError("Expected invalid Guardian event query limit to be rejected.")


def test_guardian_runtime_lifecycle_history_is_queryable() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    runtime.stop()
    lifecycle_history = runtime.lifecycle_history()

    assert [event.name for event in lifecycle_history] == [
        "guardian.initialised",
        "guardian.starting",
        "guardian.running",
        "guardian.stopped",
    ]


def test_guardian_runtime_status_snapshot_contains_event_history() -> None:
    runtime = GuardianRuntime()

    runtime.start()
    snapshot = runtime.status_snapshot()

    assert snapshot.events == runtime.events()
    assert snapshot.events[-1].name == "guardian.running"


def test_guardian_runtime_without_provider_leaves_provider_boundary_unavailable_after_start() -> None:
    """Regression guard: default construction must be unaffected by the new
    optional conversation_provider parameter."""

    runtime = GuardianRuntime()

    runtime.start()

    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE
    assert runtime.services()["Guardian Provider Boundary"].health == ServiceHealth.UNKNOWN
    assert "guardian.provider_connected" not in [event.name for event in runtime.diagnostics()]


def test_guardian_runtime_with_provider_connects_boundary_on_start() -> None:
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider)

    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE

    runtime.start()

    boundary = runtime.services()["Guardian Provider Boundary"]
    assert boundary.status == ServiceStatus.ONLINE
    assert boundary.health == ServiceHealth.HEALTHY
    assert boundary.supports("guardian.conversation")
    connected_events = runtime.diagnostics(name="guardian.provider_connected")
    assert len(connected_events) == 1
    assert provider.name in connected_events[0].message


def test_guardian_runtime_provider_boundary_goes_offline_on_stop() -> None:
    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())

    runtime.start()
    runtime.stop()

    boundary = runtime.services()["Guardian Provider Boundary"]
    assert boundary.status == ServiceStatus.OFFLINE
    assert boundary.health == ServiceHealth.UNKNOWN


def test_guardian_runtime_converse_without_provider_returns_boundary_message() -> None:
    runtime = GuardianRuntime()
    runtime.start()

    response = runtime.converse("hello")

    assert response.message == NOT_CONNECTED_RESPONSE
    assert response.provider == "guardian-boundary"


def test_guardian_runtime_converse_before_start_returns_not_running_message() -> None:
    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())

    response = runtime.converse("hello")

    assert response.message == NOT_RUNNING_RESPONSE
    assert response.provider == "guardian-boundary"


def test_guardian_runtime_converse_after_stop_returns_not_running_message() -> None:
    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())
    runtime.start()
    runtime.stop()

    response = runtime.converse("hello")

    assert response.message == NOT_RUNNING_RESPONSE


def test_guardian_runtime_converse_delegates_to_connected_provider() -> None:
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider)
    runtime.start()

    response = runtime.converse("hello Guardian")

    assert response.message == "stub: hello Guardian"
    assert response.provider == "stub-conversation"
    assert provider.received[0].message == "hello Guardian"


def test_guardian_runtime_converse_end_to_end_through_real_sentinel_gateway() -> None:
    """Proves the Guardian<->Sentinel wiring against real Sentinel components
    (SentinelTrustGateway + ProviderOrchestrator), not just a conversation-level
    stub - closing the gap flagged in ESR-0017: GuardianRuntime previously held
    no reference to Sentinel at all."""

    gateway = SentinelTrustGateway()
    orchestrator = ProviderOrchestrator()
    orchestrator.register_provider(_StubSentinelProvider())
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("stub-sentinel-provider",)))
    sentinel_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)
    runtime = GuardianRuntime(conversation_provider=sentinel_provider)

    runtime.start()
    response = runtime.converse("hello Guardian")

    assert response.message == "echo: hello Guardian"
    assert response.provider == "stub-sentinel-provider"
    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.ONLINE
    assert len(gateway.decisions()) == 1
