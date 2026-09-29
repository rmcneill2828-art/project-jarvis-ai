import pytest

from jarvis.guardian.cognitive_core import GuardianCognitiveCore
from jarvis.memory.store import PersonalMemoryRecord, utc_now


def _memory_record(content: str) -> PersonalMemoryRecord:
    return PersonalMemoryRecord(id="record-1", content=content, created_at=utc_now(), consent_decision_id="decision-1")


def test_history_is_empty_before_any_exchange() -> None:
    assert GuardianCognitiveCore().history() == ()


def test_history_returns_recorded_exchanges_oldest_first() -> None:
    core = GuardianCognitiveCore()
    core.record_exchange("hello", "hi there")
    core.record_exchange("how are you", "well")

    assert core.history() == (("hello", "hi there"), ("how are you", "well"))


def test_history_is_bounded_at_the_configured_limit() -> None:
    core = GuardianCognitiveCore(history_limit=2)

    core.record_exchange("first", "response-1")
    core.record_exchange("second", "response-2")
    core.record_exchange("third", "response-3")

    assert core.history() == (("second", "response-2"), ("third", "response-3"))


def test_history_limit_must_be_at_least_one() -> None:
    with pytest.raises(ValueError, match="history_limit must be at least 1"):
        GuardianCognitiveCore(history_limit=0)


def test_memory_notes_are_record_contents_in_order() -> None:
    notes = GuardianCognitiveCore.memory_notes([_memory_record("Robert prefers dark mode."), _memory_record("Tea, no sugar.")])

    assert notes == ("Robert prefers dark mode.", "Tea, no sugar.")


def test_memory_notes_never_include_metadata_fields() -> None:
    record = _memory_record("Robert prefers dark mode.")

    notes = GuardianCognitiveCore.memory_notes([record])

    assert record.id not in "".join(notes)
    assert record.consent_decision_id not in "".join(notes)


def test_memory_notes_empty_without_records() -> None:
    assert GuardianCognitiveCore.memory_notes([]) == ()
