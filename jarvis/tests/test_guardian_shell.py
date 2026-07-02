from jarvis import Jarvis, JarvisState
from jarvis.interfaces.conversation import ConversationService, DEFAULT_RESPONSE
from jarvis.platform import GuardianShellState, build_guardian_shell_status


def test_guardian_shell_status_centres_guardian() -> None:
    status = build_guardian_shell_status()

    assert status.guardian_message == "Guardian interface initialised."
    assert status.platform_message == "JARVIS Platform is preparing core services."
    assert status.capability_names()[0] == "Guardian Interface"
    assert status.capabilities[0].state == GuardianShellState.AVAILABLE


def test_guardian_shell_marks_future_capabilities_as_placeholders_or_unavailable() -> None:
    status = build_guardian_shell_status()
    states = {capability.name: capability.state for capability in status.capabilities}

    assert states["Sentinel Gateway"] == GuardianShellState.PLACEHOLDER
    assert states["Platform Services"] == GuardianShellState.PLACEHOLDER
    assert states["Memory"] == GuardianShellState.NOT_IMPLEMENTED
    assert states["Providers"] == GuardianShellState.OFFLINE
    assert states["Agent Framework"] == GuardianShellState.PLACEHOLDER


def test_agents_are_modelled_as_guardian_extensions_not_identities() -> None:
    status = build_guardian_shell_status()
    agent_framework = next(
        capability for capability in status.capabilities if capability.name == "Agent Framework"
    )

    assert agent_framework.extends_guardian is True
    assert "separate AI identities" in agent_framework.summary


def test_existing_python_public_api_and_conversation_behaviour_are_preserved() -> None:
    jarvis = Jarvis()
    conversation = ConversationService()

    assert jarvis.status() == JarvisState.STOPPED
    assert jarvis.start() == JarvisState.RUNNING
    assert conversation.respond("Hello Guardian") == DEFAULT_RESPONSE
    assert conversation.metadata().provider == "deterministic-local"