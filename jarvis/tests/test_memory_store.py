"""Tests for the Personal Memory SQLite store."""

from datetime import UTC, datetime

import pytest

from jarvis.memory.store import ConsentDecisionRecord, PersonalMemoryRecord, PersonalMemoryStore


@pytest.fixture
def store(tmp_path):
    return PersonalMemoryStore(tmp_path / "personal.db")


def _decision(decision_id="decision-1", decision="approved"):
    return ConsentDecisionRecord(
        id=decision_id,
        capability="memory_retention",
        decision=decision,
        decided_at=datetime.now(UTC),
        approver_label="local-user",
        sentinel_outcome="Review",
        sentinel_reason="Request routed for human review by Sentinel trust-tier policy.",
    )


def _record(record_id="record-1", consent_decision_id="decision-1"):
    return PersonalMemoryRecord(
        id=record_id,
        content="Robert prefers dark mode.",
        created_at=datetime.now(UTC),
        consent_decision_id=consent_decision_id,
    )


def test_creates_parent_directory(tmp_path):
    db_path = tmp_path / "nested" / "personal.db"

    PersonalMemoryStore(db_path)

    assert db_path.parent.exists()


def test_add_and_list_all(store):
    store.add(_record())

    records = store.list_all()

    assert len(records) == 1
    assert records[0].id == "record-1"
    assert records[0].content == "Robert prefers dark mode."
    assert records[0].consent_decision_id == "decision-1"


def test_list_all_empty_store(store):
    assert store.list_all() == ()


def test_delete_removes_exactly_one_record(store):
    store.add(_record("record-1"))
    store.add(_record("record-2"))

    store.delete("record-1")

    remaining = store.list_all()
    assert len(remaining) == 1
    assert remaining[0].id == "record-2"


def test_record_decision_and_get_decision(store):
    decision = _decision()

    store.record_decision(decision)
    fetched = store.get_decision("decision-1")

    assert fetched is not None
    assert fetched.id == "decision-1"
    assert fetched.decision == "approved"
    assert fetched.approver_label == "local-user"
    assert fetched.sentinel_category is None


def test_get_decision_unknown_id_returns_none(store):
    assert store.get_decision("does-not-exist") is None


def test_denied_decision_recorded_without_personal_memory_row(store):
    store.record_decision(_decision(decision="denied"))

    assert store.list_all() == ()
    assert store.get_decision("decision-1").decision == "denied"


def test_persists_across_new_store_instance(tmp_path):
    db_path = tmp_path / "personal.db"
    first = PersonalMemoryStore(db_path)
    first.record_decision(_decision())
    first.add(_record())

    second = PersonalMemoryStore(db_path)

    assert len(second.list_all()) == 1
    assert second.get_decision("decision-1") is not None
