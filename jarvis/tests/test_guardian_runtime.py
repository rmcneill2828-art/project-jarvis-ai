import pytest

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
from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.guardian.config import DEFAULT_GUARDIAN_PERSONA
from jarvis.guardian.runtime import (
    NO_MEMORY_SERVICE_RESPONSE,
    NOT_CONNECTED_RESPONSE,
    NOT_RUNNING_RESPONSE,
)
from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
from jarvis.interfaces.sentinel_agent import STATUS_UNKNOWN_AGENT, SentinelGatedAgentService
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from jarvis.interfaces.voice import (
    STATUS_NOT_CONNECTED,
    STATUS_NOT_RUNNING,
    STATUS_SYNTHESIZED,
    STATUS_TRANSCRIBED,
    SpeechOutcome,
    TranscriptionOutcome,
)
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from sentinel.core import SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.providers import ProviderRequest, ProviderResponse
from sentinel.speech_providers import SpeechSynthesisResponse


class _StubConversationProvider:
    """Minimal ConversationProvider double for boundary-behaviour tests."""

    name = "stub-conversation"

    def __init__(self) -> None:
        self.received: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.received.append(request)
        return ConversationResponse(message=f"stub: {request.message}", provider=self.name)


class _ScriptedConversationProvider:
    """ConversationProvider double returning a fixed sequence of response
    messages, one per call - used to test the Guardian Cognitive Core's
    history-exclusion and history-threading behaviour."""

    name = "scripted-conversation"

    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self.received: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.received.append(request)
        return ConversationResponse(message=self._responses.pop(0), provider=self.name)


class _StubSpeechProvider:
    """Minimal GuardianSpeechProvider double for boundary-behaviour tests."""

    def __init__(self) -> None:
        self.received: list[str] = []

    def synthesize(self, text: str) -> SpeechOutcome:
        self.received.append(text)
        audio = SpeechSynthesisResponse(
            provider_name="stub-speech", audio_bytes=f"audio:{text}".encode(), mime_type="audio/mpeg"
        )
        return SpeechOutcome(status=STATUS_SYNTHESIZED, audio=audio)


class _StubTranscriptionProvider:
    """Minimal GuardianTranscriptionProvider double for boundary-behaviour tests."""

    def __init__(self) -> None:
        self.received: list[tuple[bytes, str]] = []

    def transcribe(self, audio_bytes: bytes, mime_type: str) -> TranscriptionOutcome:
        self.received.append((audio_bytes, mime_type))
        return TranscriptionOutcome(status=STATUS_TRANSCRIBED, text=f"transcript:{len(audio_bytes)}")


class _StubSpecialistAgent:
    """Minimal SpecialistAgent double for boundary-behaviour tests."""

    name = "stub-agent"

    def __init__(self) -> None:
        self.received: list[AgentRequest] = []

    def execute(self, request: AgentRequest) -> AgentResult:
        self.received.append(request)
        return AgentResult(status="reported", payload={"task": request.task})


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
            occurred_at=datetime(2026, 1, 1),  # noqa: DTZ001 - deliberately naive, this test asserts it gets rejected
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


def test_guardian_runtime_converse_passes_configured_persona() -> None:
    provider = _StubConversationProvider()
    config = GuardianRuntimeConfig(persona="You are Guardian.")
    runtime = GuardianRuntime(config=config, conversation_provider=provider)
    runtime.start()

    runtime.converse("hello Guardian")

    assert provider.received[0].persona == "You are Guardian."


def test_guardian_runtime_converse_uses_default_persona_when_not_overridden() -> None:
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider)
    runtime.start()

    runtime.converse("hello Guardian")

    assert provider.received[0].persona == DEFAULT_GUARDIAN_PERSONA


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


def test_guardian_runtime_without_memory_service_leaves_memory_boundary_unavailable_after_start() -> None:
    runtime = GuardianRuntime()

    runtime.start()

    assert runtime.services()["Guardian Memory Boundary"].status == ServiceStatus.UNAVAILABLE
    assert runtime.services()["Guardian Memory Boundary"].health == ServiceHealth.UNKNOWN
    assert "guardian.memory_connected" not in [event.name for event in runtime.diagnostics()]


def test_guardian_runtime_with_memory_service_connects_boundary_on_start(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    runtime = GuardianRuntime(memory_service=memory_service)

    assert runtime.services()["Guardian Memory Boundary"].status == ServiceStatus.UNAVAILABLE

    runtime.start()

    boundary = runtime.services()["Guardian Memory Boundary"]
    assert boundary.status == ServiceStatus.ONLINE
    assert boundary.health == ServiceHealth.HEALTHY
    connected_events = runtime.diagnostics(name="guardian.memory_connected")
    assert len(connected_events) == 1


def test_guardian_runtime_memory_boundary_goes_offline_on_stop(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    runtime = GuardianRuntime(memory_service=memory_service)

    runtime.start()
    runtime.stop()

    boundary = runtime.services()["Guardian Memory Boundary"]
    assert boundary.status == ServiceStatus.OFFLINE
    assert boundary.health == ServiceHealth.UNKNOWN


def test_guardian_runtime_propose_memory_without_service_raises() -> None:
    runtime = GuardianRuntime()

    with pytest.raises(RuntimeError, match=NO_MEMORY_SERVICE_RESPONSE):
        runtime.propose_memory("Robert prefers dark mode.")


def test_guardian_runtime_approve_deny_list_memory_without_service_raise() -> None:
    runtime = GuardianRuntime()

    with pytest.raises(RuntimeError, match=NO_MEMORY_SERVICE_RESPONSE):
        runtime.approve_memory("pending-1")
    with pytest.raises(RuntimeError, match=NO_MEMORY_SERVICE_RESPONSE):
        runtime.deny_memory("pending-1")
    with pytest.raises(RuntimeError, match=NO_MEMORY_SERVICE_RESPONSE):
        runtime.list_memory()


def test_guardian_runtime_memory_methods_delegate_to_connected_service(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    runtime = GuardianRuntime(memory_service=memory_service)
    runtime.start()

    pending = runtime.propose_memory("Robert prefers dark mode.")
    record = runtime.approve_memory(pending.id)

    assert record.content == "Robert prefers dark mode."
    assert record in runtime.list_memory()

    pending_2 = runtime.propose_memory("Robert dislikes cilantro.")
    decision = runtime.deny_memory(pending_2.id)

    assert decision.decision == "denied"
    assert len(runtime.list_memory()) == 1


def test_guardian_runtime_memory_methods_refuse_before_start_even_with_connected_service(tmp_path) -> None:
    """Engineering Reviewer post-commit finding: a connected memory_service
    alone must not be enough - propose/approve/deny/list must also require
    the runtime to actually be RUNNING, mirroring converse()'s second check.
    The original implementation checked only service connectivity, letting a
    constructed-but-not-started runtime propose/approve/list memory."""

    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    runtime = GuardianRuntime(memory_service=memory_service)

    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.propose_memory("Robert prefers dark mode.")
    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.approve_memory("pending-1")
    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.deny_memory("pending-1")
    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.list_memory()


def test_guardian_runtime_converse_includes_retained_memory_content(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider, memory_service=memory_service)
    runtime.start()
    pending = runtime.propose_memory("Robert prefers dark mode.")
    runtime.approve_memory(pending.id)

    runtime.converse("What theme do I like?")

    assert "Retained Memory:" in provider.received[0].persona
    assert "Robert prefers dark mode." in provider.received[0].persona


def test_guardian_runtime_converse_reads_memory_fresh_every_turn(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider, memory_service=memory_service)
    runtime.start()

    runtime.converse("first message")
    assert "Retained Memory:" not in provider.received[0].persona

    pending = runtime.propose_memory("Robert dislikes cilantro.")
    runtime.approve_memory(pending.id)
    runtime.converse("second message")

    assert "Retained Memory:" in provider.received[1].persona
    assert "Robert dislikes cilantro." in provider.received[1].persona


def test_guardian_runtime_converse_includes_recent_history_on_next_turn() -> None:
    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider)
    runtime.start()

    runtime.converse("first message")
    runtime.converse("second message")

    assert "Recent Conversation:" not in provider.received[0].persona
    assert "Recent Conversation:" in provider.received[1].persona
    assert "User: first message" in provider.received[1].persona
    assert "Guardian: stub: first message" in provider.received[1].persona


def test_guardian_runtime_converse_does_not_record_boundary_errors_into_history() -> None:
    runtime = GuardianRuntime()
    runtime.start()
    runtime.converse("hello")  # no provider connected -> NOT_CONNECTED_RESPONSE, short-circuits before composing

    provider = _StubConversationProvider()
    runtime = GuardianRuntime(conversation_provider=provider)
    runtime.converse("hello")  # not running -> NOT_RUNNING_RESPONSE, short-circuits before composing
    runtime.start()
    runtime.converse("first real message")

    assert "Recent Conversation:" not in provider.received[0].persona


def test_guardian_runtime_converse_does_not_record_sentinel_or_provider_failure_responses_into_history() -> None:
    provider = _ScriptedConversationProvider(
        [
            "Sentinel did not allow this request to proceed.",
            "JARVIS could not reach an AI provider right now. Please try again.",
            "a genuine reply",
        ]
    )
    runtime = GuardianRuntime(conversation_provider=provider)
    runtime.start()

    runtime.converse("denied message")
    runtime.converse("unreachable message")
    runtime.converse("third message")

    assert "Recent Conversation:" not in provider.received[2].persona


def test_guardian_runtime_memory_methods_refuse_after_stop(tmp_path) -> None:
    memory_service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "personal.db"))
    runtime = GuardianRuntime(memory_service=memory_service)
    runtime.start()
    runtime.stop()

    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.propose_memory("Robert prefers dark mode.")
    with pytest.raises(RuntimeError, match=NOT_RUNNING_RESPONSE):
        runtime.list_memory()


def test_guardian_runtime_speak_without_provider_returns_not_connected_outcome() -> None:
    runtime = GuardianRuntime()
    runtime.start()

    outcome = runtime.speak("Guardian's response.")

    assert outcome.status == STATUS_NOT_CONNECTED
    assert outcome.audio is None


def test_guardian_runtime_speak_before_start_returns_not_running_outcome() -> None:
    runtime = GuardianRuntime(speech_provider=_StubSpeechProvider())

    outcome = runtime.speak("Guardian's response.")

    assert outcome.status == STATUS_NOT_RUNNING
    assert outcome.audio is None


def test_guardian_runtime_speak_after_stop_returns_not_running_outcome() -> None:
    runtime = GuardianRuntime(speech_provider=_StubSpeechProvider())
    runtime.start()
    runtime.stop()

    outcome = runtime.speak("Guardian's response.")

    assert outcome.status == STATUS_NOT_RUNNING


def test_guardian_runtime_speak_delegates_to_connected_provider() -> None:
    provider = _StubSpeechProvider()
    runtime = GuardianRuntime(speech_provider=provider)
    runtime.start()

    outcome = runtime.speak("Guardian's response.")

    assert outcome.status == STATUS_SYNTHESIZED
    assert outcome.audio.audio_bytes == b"audio:Guardian's response."
    assert provider.received == ["Guardian's response."]


def test_guardian_runtime_transcribe_without_provider_returns_not_connected_outcome() -> None:
    runtime = GuardianRuntime()
    runtime.start()

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == STATUS_NOT_CONNECTED
    assert outcome.text is None


def test_guardian_runtime_transcribe_before_start_returns_not_running_outcome() -> None:
    runtime = GuardianRuntime(transcription_provider=_StubTranscriptionProvider())

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == STATUS_NOT_RUNNING
    assert outcome.text is None


def test_guardian_runtime_transcribe_after_stop_returns_not_running_outcome() -> None:
    runtime = GuardianRuntime(transcription_provider=_StubTranscriptionProvider())
    runtime.start()
    runtime.stop()

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == STATUS_NOT_RUNNING


def test_guardian_runtime_transcription_available_reflects_provider_presence() -> None:
    assert GuardianRuntime().transcription_available is False
    assert GuardianRuntime(transcription_provider=_StubTranscriptionProvider()).transcription_available is True


def test_guardian_runtime_transcribe_delegates_to_connected_provider() -> None:
    provider = _StubTranscriptionProvider()
    runtime = GuardianRuntime(transcription_provider=provider)
    runtime.start()

    outcome = runtime.transcribe(b"fake-audio", "audio/webm")

    assert outcome.status == STATUS_TRANSCRIBED
    assert outcome.text == "transcript:10"
    assert provider.received == [(b"fake-audio", "audio/webm")]


def _agent_service(agent: _StubSpecialistAgent) -> SentinelGatedAgentService:
    return SentinelGatedAgentService(gateway=SentinelTrustGateway(), agents={agent.name: agent})


def test_guardian_runtime_invoke_agent_without_service_returns_not_connected_outcome() -> None:
    runtime = GuardianRuntime()
    runtime.start()

    outcome = runtime.invoke_agent("stub-agent", AgentRequest(task="snapshot"))

    assert outcome.status == STATUS_NOT_CONNECTED
    assert outcome.result is None


def test_guardian_runtime_invoke_agent_before_start_returns_not_running_outcome() -> None:
    agent = _StubSpecialistAgent()
    runtime = GuardianRuntime(agent_service=_agent_service(agent))

    outcome = runtime.invoke_agent(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == STATUS_NOT_RUNNING
    assert agent.received == []


def test_guardian_runtime_invoke_agent_after_stop_returns_not_running_outcome() -> None:
    agent = _StubSpecialistAgent()
    runtime = GuardianRuntime(agent_service=_agent_service(agent))
    runtime.start()
    runtime.stop()

    outcome = runtime.invoke_agent(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == STATUS_NOT_RUNNING


def test_guardian_runtime_invoke_agent_delegates_to_connected_service() -> None:
    agent = _StubSpecialistAgent()
    runtime = GuardianRuntime(agent_service=_agent_service(agent))
    runtime.start()

    outcome = runtime.invoke_agent(agent.name, AgentRequest(task="snapshot"))

    assert outcome.status == "reported"
    assert outcome.result.payload["task"] == "snapshot"
    assert agent.received[0].task == "snapshot"


def test_guardian_runtime_invoke_agent_unknown_name_returns_unknown_agent_outcome() -> None:
    agent = _StubSpecialistAgent()
    runtime = GuardianRuntime(agent_service=_agent_service(agent))
    runtime.start()

    outcome = runtime.invoke_agent("does-not-exist", AgentRequest(task="snapshot"))

    assert outcome.status == STATUS_UNKNOWN_AGENT


def test_guardian_runtime_available_agents_reflects_service_presence() -> None:
    agent = _StubSpecialistAgent()

    assert GuardianRuntime().available_agents() == ()
    assert GuardianRuntime(agent_service=_agent_service(agent)).available_agents() == ("stub-agent",)
