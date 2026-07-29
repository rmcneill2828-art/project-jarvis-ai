import pytest

from jarvis.guardian.cognitive_core import GuardianCognitiveCore
from jarvis.memory.store import PersonalMemoryRecord, utc_now


def _memory_record(content: str) -> PersonalMemoryRecord:
    return PersonalMemoryRecord(id="record-1", content=content, created_at=utc_now(), consent_decision_id="decision-1")


def test_compose_with_no_memory_and_no_history_returns_persona_unchanged() -> None:
    core = GuardianCognitiveCore()

    composed = core.compose("You are Guardian.")

    assert composed == "You are Guardian."


def test_compose_includes_memory_section_when_records_exist() -> None:
    core = GuardianCognitiveCore()

    composed = core.compose("You are Guardian.", memory_records=[_memory_record("Robert prefers dark mode.")])

    assert "Retained Memory:" in composed
    assert "- Robert prefers dark mode." in composed


def test_compose_omits_memory_section_when_no_records() -> None:
    core = GuardianCognitiveCore()

    composed = core.compose("You are Guardian.", memory_records=[])

    assert "Retained Memory:" not in composed


def test_compose_never_renders_memory_metadata_fields() -> None:
    core = GuardianCognitiveCore()
    record = _memory_record("Robert prefers dark mode.")

    composed = core.compose("You are Guardian.", memory_records=[record])

    assert record.id not in composed
    assert record.consent_decision_id not in composed


def test_compose_includes_history_section_after_recorded_exchange() -> None:
    core = GuardianCognitiveCore()
    core.record_exchange("hello", "hi there")

    composed = core.compose("You are Guardian.")

    assert "Recent Conversation:" in composed
    assert "User: hello" in composed
    assert "Guardian: hi there" in composed


def test_compose_omits_history_section_with_no_recorded_exchanges() -> None:
    core = GuardianCognitiveCore()

    composed = core.compose("You are Guardian.")

    assert "Recent Conversation:" not in composed


def test_history_is_bounded_at_the_configured_limit() -> None:
    core = GuardianCognitiveCore(history_limit=2)

    core.record_exchange("first", "response-1")
    core.record_exchange("second", "response-2")
    core.record_exchange("third", "response-3")

    composed = core.compose("You are Guardian.")

    assert "first" not in composed
    assert "second" in composed
    assert "third" in composed


def test_history_limit_must_be_at_least_one() -> None:
    with pytest.raises(ValueError, match="history_limit must be at least 1"):
        GuardianCognitiveCore(history_limit=0)


def test_compose_never_mutates_persona_text() -> None:
    core = GuardianCognitiveCore()
    persona = "You are Guardian."

    composed = core.compose(persona, memory_records=[_memory_record("note")])

    assert composed.startswith(persona)
