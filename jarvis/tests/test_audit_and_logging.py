"""Tests for EBG-0144 (ESR-0059 WP9): durable, rotating audit trail, bounded
in-process history, and the backend's own log file."""

import json
import logging
import threading

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.stdio_rpc import (
    AUDIT_LOG_FILENAME,
    StdioRpcServer,
    _configure_backend_log_file,
    _log_dir,
    build_default_runtime,
)
from jarvis.memory.service import MAX_PENDING_PROPOSALS, PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from sentinel.audit import AuditEvent, JsonAuditRecorder, MemoryAuditRecorder
from sentinel.core import SentinelRequest, SentinelTrustGateway


def _event(n: int = 0) -> AuditEvent:
    return AuditEvent(event_type="test", outcome="ok", summary=f"event {n}")


def test_memory_audit_recorder_keeps_only_the_most_recent_events():
    recorder = MemoryAuditRecorder(max_events=3)
    for n in range(5):
        recorder.record(_event(n))

    assert [e.summary for e in recorder.events()] == ["event 2", "event 3", "event 4"]


def test_json_audit_recorder_rotates_and_keeps_backup_count(tmp_path):
    path = tmp_path / "audit.jsonl"
    recorder = JsonAuditRecorder(path, max_bytes=400, backup_count=2)

    for n in range(40):
        recorder.record(_event(n))

    assert path.exists()
    assert (tmp_path / "audit.jsonl.1").exists()
    assert (tmp_path / "audit.jsonl.2").exists()
    assert not (tmp_path / "audit.jsonl.3").exists()
    for candidate in (path, tmp_path / "audit.jsonl.1", tmp_path / "audit.jsonl.2"):
        assert candidate.stat().st_size <= 400
    # The newest event is in the live file, readable back.
    assert recorder.events()[-1].summary == "event 39"


def test_json_audit_recorder_survives_a_new_instance(tmp_path):
    path = tmp_path / "audit.jsonl"
    JsonAuditRecorder(path).record(_event(1))

    assert [e.summary for e in JsonAuditRecorder(path).events()] == ["event 1"]


def test_json_audit_recorder_concurrent_writes_stay_whole_lines(tmp_path):
    path = tmp_path / "audit.jsonl"
    recorder = JsonAuditRecorder(path)

    def write_many(offset: int) -> None:
        for n in range(200):
            recorder.record(_event(offset + n))

    threads = [threading.Thread(target=write_many, args=(i * 1000,)) for i in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 800
    assert all(json.loads(line)["event_type"] == "test" for line in lines)


def test_gateway_decision_history_is_bounded():
    from sentinel.audit import DEFAULT_MAX_MEMORY_EVENTS

    gateway = SentinelTrustGateway()
    for _ in range(DEFAULT_MAX_MEMORY_EVENTS + 5):
        gateway.evaluate(SentinelRequest(source="test", intent="x"))

    assert len(gateway.decisions()) == DEFAULT_MAX_MEMORY_EVENTS


def test_unresolved_memory_proposals_are_bounded(tmp_path):
    service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "m.db"))
    first = service.propose("note 0")
    for n in range(1, MAX_PENDING_PROPOSALS + 1):
        service.propose(f"note {n}")

    with pytest.raises(KeyError):
        service.approve(first.id)  # oldest was dropped, never stored
    assert service.list_records() == ()


def test_log_dir_defaults_beside_the_memory_store_and_can_be_overridden(tmp_path):
    assert _log_dir({"JARVIS_MEMORY_DB_PATH": str(tmp_path / "memory" / "personal.db")}) == tmp_path / "logs"
    assert _log_dir({"JARVIS_LOG_DIR": str(tmp_path / "elsewhere")}) == tmp_path / "elsewhere"
    # Unset, it sits beside the default memory store (conftest.py sandboxes
    # that default, so this never resolves to the real home directory here).
    from jarvis.interfaces import stdio_rpc

    assert _log_dir({}) == stdio_rpc.DEFAULT_MEMORY_DB_PATH.parent.parent / "logs"


def test_runtime_writes_a_durable_audit_trail_without_conversation_text(tmp_path):
    """The audit log must record what Sentinel decided and which providers
    ran - never what the user said."""

    log_dir = tmp_path / "logs"
    runtime = build_default_runtime(
        environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            "JARVIS_LOG_DIR": str(log_dir),
        }
    )
    server = StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))
    secret = "my bank PIN is 4921"

    server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "guardian.converse", "params": {"message": secret}}))

    audit_text = (log_dir / AUDIT_LOG_FILENAME).read_text(encoding="utf-8")
    event_types = [json.loads(line)["event_type"] for line in audit_text.splitlines()]
    assert "sentinel_decision" in event_types
    assert "provider_execution" in event_types
    assert secret not in audit_text
    assert "4921" not in audit_text


def test_backend_log_file_receives_log_records(tmp_path):
    root = logging.getLogger()
    before = list(root.handlers)
    previous_level = root.level
    root.setLevel(logging.INFO)
    try:
        log_path = _configure_backend_log_file({"JARVIS_LOG_DIR": str(tmp_path)})
        logging.getLogger("jarvis.test").info("backend log check")
        for handler in root.handlers:
            handler.flush()
        assert "backend log check" in log_path.read_text(encoding="utf-8")
    finally:
        for handler in list(root.handlers):
            if handler not in before:
                root.removeHandler(handler)
                handler.close()
        root.setLevel(previous_level)
