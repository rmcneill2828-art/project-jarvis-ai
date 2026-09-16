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
    store.record_decision(_decision())
    store.add(_record())

    records = store.list_all()

    assert len(records) == 1
    assert records[0].id == "record-1"
    assert records[0].content == "Robert prefers dark mode."
    assert records[0].consent_decision_id == "decision-1"


def test_list_all_empty_store(store):
    assert store.list_all() == ()


def test_add_rejects_record_with_no_matching_decision(store):
    with pytest.raises(ValueError, match="does not reference a recorded approved decision"):
        store.add(_record())

    assert store.list_all() == ()


def test_add_rejects_record_referencing_denied_decision(store):
    store.record_decision(_decision(decision="denied"))

    with pytest.raises(ValueError, match="does not reference a recorded approved decision"):
        store.add(_record())

    assert store.list_all() == ()


def test_delete_removes_exactly_one_record(store):
    store.record_decision(_decision())
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


def test_export_snapshot_includes_both_tables(store):
    store.record_decision(_decision())
    store.add(_record())

    snapshot = store.export_snapshot()

    assert len(snapshot["personal_memory"]) == 1
    assert snapshot["personal_memory"][0]["id"] == "record-1"
    assert snapshot["personal_memory"][0]["content"] == "Robert prefers dark mode."
    assert len(snapshot["consent_decisions"]) == 1
    assert snapshot["consent_decisions"][0]["id"] == "decision-1"
    assert snapshot["consent_decisions"][0]["decision"] == "approved"


def test_export_snapshot_includes_denied_decisions_with_no_memory_row(store):
    store.record_decision(_decision(decision="denied"))

    snapshot = store.export_snapshot()

    assert snapshot["personal_memory"] == ()
    assert len(snapshot["consent_decisions"]) == 1
    assert snapshot["consent_decisions"][0]["decision"] == "denied"


def test_export_snapshot_empty_store(store):
    snapshot = store.export_snapshot()

    assert snapshot == {"personal_memory": (), "consent_decisions": ()}


def test_import_snapshot_restores_both_tables(store):
    store.record_decision(_decision())
    store.add(_record())
    snapshot = store.export_snapshot()
    fresh_store = PersonalMemoryStore(store._db_path.parent / "fresh.db")

    count = fresh_store.import_snapshot(snapshot)

    assert count == 1
    restored = fresh_store.list_all()
    assert len(restored) == 1
    assert restored[0].id == "record-1"
    assert restored[0].content == "Robert prefers dark mode."
    assert fresh_store.get_decision("decision-1").decision == "approved"


def test_import_snapshot_refuses_non_empty_store_without_confirmation(store):
    store.record_decision(_decision())
    store.add(_record())
    snapshot = store.export_snapshot()
    store.record_decision(_decision("decision-2"))
    store.add(_record("record-2", "decision-2"))

    with pytest.raises(ValueError, match="not empty"):
        store.import_snapshot(snapshot)

    # Refused before any write - existing data untouched.
    assert len(store.list_all()) == 2


def test_import_snapshot_overwrites_when_confirmed(store):
    store.record_decision(_decision())
    store.add(_record())
    snapshot = store.export_snapshot()
    store.record_decision(_decision("decision-2"))
    store.add(_record("record-2", "decision-2"))

    count = store.import_snapshot(snapshot, confirm_overwrite=True)

    assert count == 1
    restored = store.list_all()
    assert len(restored) == 1
    assert restored[0].id == "record-1"


def test_import_snapshot_rejects_malformed_snapshot_missing_keys(store):
    with pytest.raises(ValueError, match="Invalid backup snapshot"):
        store.import_snapshot({"personal_memory": []})

    assert store.list_all() == ()


def test_import_snapshot_rejects_memory_row_referencing_unknown_decision(store):
    bad_snapshot = {
        "personal_memory": [
            {"id": "record-1", "content": "x", "created_at": "2026-01-01T00:00:00+00:00", "consent_decision_id": "missing"}
        ],
        "consent_decisions": [],
    }

    with pytest.raises(ValueError, match="not present among the snapshot"):
        store.import_snapshot(bad_snapshot)

    assert store.list_all() == ()


def test_import_snapshot_into_empty_store_requires_no_confirmation(store):
    snapshot = {
        "personal_memory": (),
        "consent_decisions": (
            {
                "id": "decision-1",
                "capability": "memory_retention",
                "decision": "denied",
                "decided_at": "2026-01-01T00:00:00+00:00",
                "approver_label": "local-user",
                "sentinel_outcome": "Review",
                "sentinel_category": None,
                "sentinel_reason": "test",
            },
        ),
    }

    count = store.import_snapshot(snapshot)

    assert count == 0
    assert store.get_decision("decision-1").decision == "denied"


def test_persists_across_new_store_instance(tmp_path):
    db_path = tmp_path / "personal.db"
    first = PersonalMemoryStore(db_path)
    first.record_decision(_decision())
    first.add(_record())

    second = PersonalMemoryStore(db_path)

    assert len(second.list_all()) == 1
    assert second.get_decision("decision-1") is not None
