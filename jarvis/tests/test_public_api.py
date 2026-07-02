from jarvis import (
    CapabilityDescriptor,
    CapabilityRegistry,
    Jarvis,
    JarvisService,
    JarvisState,
    PlatformBootstrapState,
    PlatformFoundation,
    PlatformStatus,
    ServiceHealth,
    ServiceHealthSummary,
    ServiceStatus,
)


def test_public_api_exports_lifecycle_components() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED
    assert JarvisService(name="Test").name == "Test"
    assert ServiceHealth.HEALTHY.value == "Healthy"
    assert ServiceStatus.ONLINE.value == "Online"


def test_public_api_exports_platform_foundation_components() -> None:
    foundation = PlatformFoundation()

    assert CapabilityDescriptor(name="Test", summary="Test capability").name == "Test"
    assert isinstance(CapabilityRegistry(), CapabilityRegistry)
    assert foundation.status({}).bootstrap_state == PlatformBootstrapState.NOT_BOOTSTRAPPED
    assert PlatformStatus is not None
    assert ServiceHealthSummary is not None