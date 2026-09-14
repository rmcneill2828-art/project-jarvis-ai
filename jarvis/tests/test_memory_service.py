"""Tests for the Personal Memory consent-gated service."""

import json

import pytest

from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.policy import PolicyDecision


class _AlwaysDenyPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(outcome=SentinelDecisionOutcome.DENY, reason="Denied for test.")


class _AlwaysAllowPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(outcome=SentinelDecisionOutcome.ALLOW, reason="Allowed for test.")


@pytest.fixture
def store(tmp_path):
    return PersonalMemoryStore(tmp_path / "personal.db")


def _service(store, policy_engine=None):
    gateway = SentinelTrustGateway(policy_engine=policy_engine)
    return PersonalMemoryService(gateway=gateway, store=store)


def test_propose_with_review_outcome_creates_pending_request(store):
    service = _service(store)

    pending = service.propose("Robert prefers dark mode.")

    assert pending.content == "Robert prefers dark mode."
    assert pending.sentinel_response.decision.outcome is SentinelDecisionOutcome.REVIEW


def test_propose_with_deny_outcome_refuses(store):
    service = _service(store, policy_engine=_AlwaysDenyPolicy())

    with pytest.raises(RuntimeError, match="denied"):
        service.propose("Robert prefers dark mode.")

    assert store.list_all() == ()


def test_propose_with_unexpected_allow_outcome_refuses(store):
    service = _service(store, policy_engine=_AlwaysAllowPolicy())

    with pytest.raises(RuntimeError, match="unexpected Sentinel outcome"):
        service.propose("Robert prefers dark mode.")

    assert store.list_all() == ()


def test_approve_stores_record_with_durable_consent_decision(store):
    service = _service(store)
    pending = service.propose("Robert prefers dark mode.")

    record = service.approve(pending.id)

    assert record.content == "Robert prefers dark mode."
    stored_decision = store.get_decision(record.consent_decision_id)
    assert stored_decision is not None
    assert stored_decision.decision == "approved"
    assert stored_decision.approver_label == "local-user"
    assert record in service.list_records()


def test_deny_records_durable_decision_without_storing_content(store):
    service = _service(store)
    pending = service.propose("Robert prefers dark mode.")

    decision = service.deny(pending.id)

    assert decision.decision == "denied"
    stored_decision = store.get_decision(decision.id)
    assert stored_decision is not None
    assert stored_decision.decision == "denied"
    assert store.list_all() == ()


def test_approve_unknown_pending_id_raises_key_error(store):
    service = _service(store)

    with pytest.raises(KeyError):
        service.approve("does-not-exist")


def test_deny_unknown_pending_id_raises_key_error(store):
    service = _service(store)

    with pytest.raises(KeyError):
        service.deny("does-not-exist")


def test_approve_twice_on_same_id_raises_key_error(store):
    service = _service(store)
    pending = service.propose("Robert prefers dark mode.")
    service.approve(pending.id)

    with pytest.raises(KeyError):
        service.approve(pending.id)


def test_list_records_delegates_to_store(store):
    service = _service(store)
    pending = service.propose("Robert prefers dark mode.")
    service.approve(pending.id)

    assert service.list_records() == store.list_all()


def test_export_backup_writes_json_file_with_both_tables(store, tmp_path):
    service = _service(store)
    pending = service.propose("Robert prefers dark mode.")
    service.approve(pending.id)
    backup_dir = tmp_path / "backups"

    backup_path = service.export_backup(backup_dir)

    assert backup_path.parent == backup_dir
    assert backup_path.exists()
    payload = json.loads(backup_path.read_text(encoding="utf-8"))
    assert "exported_at" in payload
    assert len(payload["personal_memory"]) == 1
    assert payload["personal_memory"][0]["content"] == "Robert prefers dark mode."
    assert len(payload["consent_decisions"]) == 1
    assert payload["consent_decisions"][0]["decision"] == "approved"


def test_export_backup_creates_backup_dir_if_missing(store, tmp_path):
    service = _service(store)
    backup_dir = tmp_path / "nested" / "backups"

    service.export_backup(backup_dir)

    assert backup_dir.exists()


def test_export_backup_empty_store_writes_empty_lists(store, tmp_path):
    service = _service(store)

    backup_path = service.export_backup(tmp_path / "backups")

    payload = json.loads(backup_path.read_text(encoding="utf-8"))
    assert payload["personal_memory"] == []
    assert payload["consent_decisions"] == []
