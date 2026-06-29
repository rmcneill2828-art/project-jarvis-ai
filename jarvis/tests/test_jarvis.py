from jarvis import Jarvis, JarvisState, ServiceStatus


def test_jarvis_starts_in_stopped_state() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED


def test_jarvis_can_start() -> None:
    jarvis = Jarvis()

    assert jarvis.start() == JarvisState.RUNNING
    assert jarvis.status() == JarvisState.RUNNING


def test_jarvis_can_stop() -> None:
    jarvis = Jarvis()

    jarvis.start()

    assert jarvis.stop() == JarvisState.STOPPED
    assert jarvis.status() == JarvisState.STOPPED


def test_jarvis_reports_initial_service_statuses() -> None:
    jarvis = Jarvis()

    statuses = jarvis.service_statuses()

    assert statuses["Core"] == ServiceStatus.ONLINE
    assert statuses["Memory"] == ServiceStatus.UNAVAILABLE
    assert statuses["Voice"] == ServiceStatus.UNAVAILABLE
    assert statuses["Vision"] == ServiceStatus.UNAVAILABLE
    assert statuses["Internet"] == ServiceStatus.OFFLINE


def test_jarvis_can_register_service_status() -> None:
    jarvis = Jarvis()

    jarvis.register_service("Voice", ServiceStatus.STARTING)

    assert jarvis.service_statuses()["Voice"] == ServiceStatus.STARTING
