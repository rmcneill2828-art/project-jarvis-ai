from jarvis import (
    CapabilityDescriptor,
    CapabilityRegistry,
    Jarvis,
    JarvisService,
    PlatformBootstrapState,
    PlatformFoundation,
    ServiceHealth,
    ServiceStatus,
)
from jarvis.interfaces.conversation import DEFAULT_RESPONSE, ConversationService


def test_platform_foundation_bootstrap_reports_available_status() -> None:
    foundation = PlatformFoundation()
    services = {
        "Core": JarvisService(
            name="Core",
            status=ServiceStatus.ONLINE,
            health=ServiceHealth.HEALTHY,
        )
    }

    status = foundation.bootstrap(services)

    assert status.available is True
    assert status.bootstrap_state == PlatformBootstrapState.BOOTSTRAPPED
    assert status.service_health["Core"].status == ServiceStatus.ONLINE
    assert status.service_health["Core"].health == ServiceHealth.HEALTHY


def test_platform_status_is_available_after_jarvis_start() -> None:
    jarvis = Jarvis()

    initial_status = jarvis.platform_status()
    started_state = jarvis.start()
    platform_status = jarvis.platform_status()

    assert initial_status.available is False
    assert initial_status.bootstrap_state == PlatformBootstrapState.NOT_BOOTSTRAPPED
    assert started_state.value == "RUNNING"
    assert platform_status.available is True
    assert platform_status.bootstrap_state == PlatformBootstrapState.BOOTSTRAPPED
    assert "Core" in platform_status.service_health
    assert "Conversation" in platform_status.service_health
    assert platform_status.service_health["Guardian Runtime"].status == ServiceStatus.ONLINE
    assert (
        platform_status.service_health["Guardian Memory Boundary"].status
        == ServiceStatus.UNAVAILABLE
    )


def test_platform_foundation_registers_placeholder_capabilities_without_execution() -> None:
    foundation = PlatformFoundation()

    capabilities = foundation.registry.capabilities()

    assert "platform.bootstrap" in capabilities
    assert "platform.status" in capabilities
    assert "capability.registry" in capabilities
    assert "conversation.workspace" in capabilities
    assert "future.platform-services" in capabilities
    assert capabilities["future.platform-services"].status == "Placeholder"


def test_capability_registry_can_register_and_list_descriptors() -> None:
    registry = CapabilityRegistry()
    descriptor = CapabilityDescriptor(
        name="test.placeholder",
        summary="A placeholder capability used for registry testing.",
    )

    registered = registry.register(descriptor)
    listed = registry.list_capabilities()

    assert registered == descriptor
    assert listed == (descriptor,)
    assert registry.capabilities()["test.placeholder"] == descriptor


def test_platform_foundation_requires_no_external_provider() -> None:
    jarvis = Jarvis()
    conversation = ConversationService()

    jarvis.start()

    assert jarvis.platform_status().available is True
    assert conversation.respond("Hello") == DEFAULT_RESPONSE
    assert conversation.metadata().provider == "deterministic-local"