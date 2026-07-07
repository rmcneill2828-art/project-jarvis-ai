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


def test_guardian_runtime_status_snapshot_reports_initial_state() -> None:
    runtime = GuardianRuntime()

    snapshot = runtime.status_snapshot()

    assert isinstance(snapshot, GuardianRuntimeStatus)
    assert snapshot.state == GuardianRuntimeState.STOPPED
    assert snapshot.runtime_name == "Guardian"
    assert snapshot.persistence_enabled is False
    assert snapshot.diagnostics_enabled is True
    assert snapshot.diagnostic_count == 1
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
