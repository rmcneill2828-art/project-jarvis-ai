from jarvis import Jarvis, JarvisService, JarvisState, ServiceHealth, ServiceStatus


def test_public_api_exports_lifecycle_components() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED
    assert JarvisService(name="Test").name == "Test"
    assert ServiceHealth.HEALTHY.value == "Healthy"
    assert ServiceStatus.ONLINE.value == "Online"
