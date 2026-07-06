from jarvis import (
    CapabilityDescriptor,
    CapabilityRegistry,
    EngineeringReadinessContext,
    EngineeringRequest,
    GiaBootstrap,
    Jarvis,
    JarvisService,
    JarvisState,
    PlatformBootstrapState,
    PlatformFoundation,
    PlatformStatus,
    ReadinessState,
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


def test_public_api_exports_gia_bootstrap_components() -> None:
    request = EngineeringRequest(
        identifier="EIP-0001",
        objective="Implement GIA-BOOT v1.",
        scope=("Export public interfaces.",),
    )

    context = GiaBootstrap().evaluate(request)

    assert context.state == ReadinessState.READY
    assert isinstance(context, EngineeringReadinessContext)
