from jarvis import (
    GuardianRuntimeState,
    Jarvis,
    JarvisState,
    ServiceHealth,
    ServiceStatus,
)


def test_jarvis_starts_in_stopped_state() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED


def test_jarvis_can_start() -> None:
    jarvis = Jarvis()

    assert jarvis.start() == JarvisState.RUNNING
    assert jarvis.status() == JarvisState.RUNNING
    assert jarvis.guardian_runtime().status() == GuardianRuntimeState.RUNNING


def test_jarvis_can_stop() -> None:
    jarvis = Jarvis()

    jarvis.start()

    assert jarvis.stop() == JarvisState.STOPPED
    assert jarvis.status() == JarvisState.STOPPED
    assert jarvis.guardian_runtime().status() == GuardianRuntimeState.STOPPED


def test_jarvis_reports_initial_service_statuses() -> None:
    jarvis = Jarvis()

    statuses = jarvis.service_statuses()

    assert statuses["Core"] == ServiceStatus.ONLINE
    assert statuses["Conversation"] == ServiceStatus.ONLINE
    assert statuses["Memory"] == ServiceStatus.UNAVAILABLE
    assert statuses["Voice"] == ServiceStatus.UNAVAILABLE
    assert statuses["Vision"] == ServiceStatus.UNAVAILABLE
    assert statuses["Internet"] == ServiceStatus.OFFLINE
    assert statuses["Guardian Runtime"] == ServiceStatus.OFFLINE
    assert statuses["Guardian Memory Boundary"] == ServiceStatus.UNAVAILABLE
    assert statuses["Guardian Provider Boundary"] == ServiceStatus.UNAVAILABLE


def test_jarvis_can_register_service_status() -> None:
    jarvis = Jarvis()

    jarvis.register_service("Voice", ServiceStatus.STARTING)

    assert jarvis.service_statuses()["Voice"] == ServiceStatus.STARTING


def test_jarvis_reports_service_model_health_and_capabilities() -> None:
    jarvis = Jarvis()

    core_service = jarvis.services()["Core"]
    conversation_service = jarvis.services()["Conversation"]
    guardian_service = jarvis.services()["Guardian Runtime"]

    assert core_service.health == ServiceHealth.HEALTHY
    assert core_service.supports("conversation-routing")
    assert conversation_service.health == ServiceHealth.HEALTHY
    assert conversation_service.supports("session-transcript")
    assert guardian_service.supports("guardian.lifecycle")


def test_jarvis_exposes_owned_guardian_runtime() -> None:
    jarvis = Jarvis()

    guardian_runtime = jarvis.guardian_runtime()

    assert guardian_runtime.status() == GuardianRuntimeState.STOPPED
    assert guardian_runtime is jarvis.guardian_runtime()
