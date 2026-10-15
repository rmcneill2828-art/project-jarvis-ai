"""Time-based audit retention and its setting (ESR-0061 WP5b,
EIP-ESR0061-005 6.4, decision R1)."""

import json
import threading
from datetime import UTC, datetime, timedelta

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.retention import RetentionService
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.shared.settings import DEFAULT_RETENTION_DAYS, SettingsStore
from sentinel.audit import AuditEvent, JsonAuditRecorder

NOW = datetime(2026, 10, 15, 12, 0, tzinfo=UTC)


def _event(age_days: float, label: str = "x") -> AuditEvent:
    return AuditEvent(
        event_type="test_event",
        outcome="ok",
        summary=f"event {label}",
        metadata={"label": label},
        recorded_at=NOW - timedelta(days=age_days),
    )


def _lines(path):
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --- the prune ---------------------------------------------------------------------------------------------------


def test_prune_removes_only_events_older_than_the_limit(tmp_path):
    recorder = JsonAuditRecorder(tmp_path / "audit.jsonl")
    for age, label in [(200, "old"), (95, "older-than-90"), (80, "recent"), (1, "today")]:
        recorder.record(_event(age, label))

    result = recorder.prune_older_than(90, now=NOW)

    assert (result.removed, result.kept, result.unreadable_kept) == (2, 2, 0)
    assert [event.metadata["label"] for event in recorder.events()] == ["recent", "today"]
    assert not list(tmp_path.glob("*.prune"))


def test_a_line_whose_time_cannot_be_read_is_kept_and_counted(tmp_path):
    path = tmp_path / "audit.jsonl"
    good_old = json.dumps(_event(500, "old").as_dict())
    path.write_text(
        "\n".join([good_old, "this is not json", json.dumps({"summary": "no time at all"})]) + "\n",
        encoding="utf-8",
    )
    recorder = JsonAuditRecorder(path)

    result = recorder.prune_older_than(30, now=NOW)

    assert result.removed == 1
    assert result.unreadable_kept == 2
    assert len(_lines(path)) == 2


def test_rotated_copies_are_pruned_and_an_emptied_one_is_deleted(tmp_path):
    live = tmp_path / "audit.jsonl"
    first = tmp_path / "audit.jsonl.1"
    second = tmp_path / "audit.jsonl.2"
    live.write_text(json.dumps(_event(1, "live").as_dict()) + "\n", encoding="utf-8")
    first.write_text(
        json.dumps(_event(400, "gone").as_dict()) + "\n" + json.dumps(_event(10, "stays").as_dict()) + "\n",
        encoding="utf-8",
    )
    second.write_text(json.dumps(_event(700, "all-gone").as_dict()) + "\n", encoding="utf-8")
    recorder = JsonAuditRecorder(live)

    result = recorder.prune_older_than(90, now=NOW)

    assert result.removed == 2
    assert len(_lines(live)) == 1
    assert len(_lines(first)) == 1
    assert not second.exists()


def test_an_emptied_live_file_is_removed_and_the_recorder_starts_a_new_one(tmp_path):
    path = tmp_path / "audit.jsonl"
    recorder = JsonAuditRecorder(path)
    recorder.record(_event(400, "old"))

    recorder.prune_older_than(30, now=NOW)

    assert not path.exists()
    assert recorder.events() == ()
    recorder.record(_event(0, "new"))
    assert len(recorder.events()) == 1


def test_naive_times_are_read_as_utc(tmp_path):
    path = tmp_path / "audit.jsonl"
    entry = _event(400, "old").as_dict()
    entry["recorded_at"] = (NOW - timedelta(days=400)).replace(tzinfo=None).isoformat()
    path.write_text(json.dumps(entry) + "\n", encoding="utf-8")

    result = JsonAuditRecorder(path).prune_older_than(90, now=NOW)

    assert result.removed == 1


def test_a_limit_below_one_day_is_refused(tmp_path):
    with pytest.raises(ValueError):
        JsonAuditRecorder(tmp_path / "audit.jsonl").prune_older_than(0)


def test_writes_during_a_prune_are_never_lost(tmp_path):
    recorder = JsonAuditRecorder(tmp_path / "audit.jsonl")
    for index in range(200):
        recorder.record(_event(400 if index % 2 == 0 else 1, f"seed-{index}"))
    stop = threading.Event()
    written: list[str] = []

    def writer() -> None:
        index = 0
        while not stop.is_set():
            label = f"live-{index}"
            recorder.record(_event(0, label))
            written.append(label)
            index += 1

    thread = threading.Thread(target=writer)
    thread.start()
    try:
        for _ in range(20):
            recorder.prune_older_than(90, now=NOW)
    finally:
        stop.set()
        thread.join()

    labels = {event.metadata["label"] for event in recorder.events()}
    assert set(written) <= labels
    assert not any(label.startswith("seed-") and int(label.split("-")[1]) % 2 == 0 for label in labels)


# --- the setting -------------------------------------------------------------------------------------------------


def test_the_setting_defaults_to_ninety_days_and_never_to_for_ever(tmp_path):
    store = SettingsStore(tmp_path / "settings.json")
    assert store.retention_days() == DEFAULT_RETENTION_DAYS == 90


@pytest.mark.parametrize("days", [30, 90, 365])
def test_an_allowed_value_is_kept_across_a_new_store(tmp_path, days):
    SettingsStore(tmp_path / "settings.json").set_retention_days(days)
    assert SettingsStore(tmp_path / "settings.json").retention_days() == days


@pytest.mark.parametrize("bad", [0, 1, 45, 366, -5, 10_000, True, "90", None])
def test_a_value_that_is_not_offered_is_refused(tmp_path, bad):
    with pytest.raises(ValueError):
        SettingsStore(tmp_path / "settings.json").set_retention_days(bad)


@pytest.mark.parametrize("content", ["", "not json", "[1, 2]", '{"auditRetentionDays": 7}', '{"auditRetentionDays": "90"}'])
def test_a_damaged_or_out_of_range_file_means_the_default(tmp_path, content):
    path = tmp_path / "settings.json"
    path.write_text(content, encoding="utf-8")
    assert SettingsStore(path).retention_days() == DEFAULT_RETENTION_DAYS


# --- the service -------------------------------------------------------------------------------------------------


def test_the_service_prunes_with_the_current_setting_and_survives_a_failure(tmp_path):
    recorder = JsonAuditRecorder(tmp_path / "audit.jsonl")
    recorder.record(AuditEvent("t", "ok", "old", recorded_at=datetime.now(UTC) - timedelta(days=60)))
    settings = SettingsStore(tmp_path / "settings.json")
    service = RetentionService(recorder, settings)

    settings.set_retention_days(365)
    assert service.run_once().removed == 0
    settings.set_retention_days(30)
    assert service.run_once().removed == 1
    assert service.last_result().removed == 1

    class Broken:
        def prune_older_than(self, days):
            raise OSError("disk on fire")

    assert RetentionService(Broken(), settings).run_once() is None


def test_run_forever_prunes_at_start_and_stops_when_told(tmp_path):
    recorder = JsonAuditRecorder(tmp_path / "audit.jsonl")
    recorder.record(AuditEvent("t", "ok", "old", recorded_at=datetime.now(UTC) - timedelta(days=500)))
    service = RetentionService(recorder, SettingsStore(tmp_path / "settings.json"))
    stop = threading.Event()
    thread = threading.Thread(target=service.run_forever, args=(stop, 3600))
    thread.start()
    for _ in range(100):
        if service.last_result() is not None:
            break
        threading.Event().wait(0.02)
    stop.set()
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert service.last_result().removed == 1


# --- the screen's methods ----------------------------------------------------------------------------------------


class _Client:
    def __init__(self, server):
        self.server = server
        self._next = 1

    def call(self, method, **params):
        self._next += 1
        return self.server.handle_line(
            json.dumps({"jsonrpc": "2.0", "id": self._next, "method": method, "params": params})
        )

    def result(self, method, **params):
        response = self.call(method, **params)
        assert "result" in response, response
        return response["result"]

    def error(self, method, **params):
        response = self.call(method, **params)
        assert "error" in response, response
        return response["error"]["message"]

    def sign_in(self, name, role):
        created = self.result("profile.create", displayName=name, role=role)
        self.result("profile.select", profileId=created["id"])


def _client(tmp_path, role="Administrator"):
    environ = {
        "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
        "JARVIS_LOG_DIR": str(tmp_path / "logs"),
    }
    runtime = build_default_runtime(environ=environ)
    server = StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))
    client = _Client(server)
    client.sign_in("Robert", role)
    return client


def test_an_administrator_reads_and_changes_the_retention_setting(tmp_path):
    client = _client(tmp_path)
    first = client.result("settings.get")
    assert first["auditRetentionDays"] == 90
    assert first["allowedRetentionDays"] == [30, 90, 365]

    changed = client.result("settings.setRetentionDays", days=30)
    assert changed["auditRetentionDays"] == 30
    assert changed["lastPrune"] is not None
    assert client.result("settings.get")["auditRetentionDays"] == 30
    assert (tmp_path / "settings.json").exists()


def test_a_shorter_limit_is_applied_at_once(tmp_path):
    client = _client(tmp_path)
    audit = tmp_path / "logs" / "audit.jsonl"
    audit.parent.mkdir(parents=True, exist_ok=True)
    old = AuditEvent("t", "ok", "old", recorded_at=datetime.now(UTC) - timedelta(days=60)).as_dict()
    audit.write_text(json.dumps(old) + "\n", encoding="utf-8")

    result = client.result("settings.setRetentionDays", days=30)

    assert result["lastPrune"]["removed"] >= 1


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_read_or_change_settings(tmp_path, role):
    client = _client(tmp_path, role)
    assert "Only an Administrator" in client.error("settings.get")
    assert "Only an Administrator" in client.error("settings.setRetentionDays", days=30)


@pytest.mark.parametrize("bad", [0, 7, 45, 366, 100000])
def test_a_value_that_is_not_offered_is_refused_by_the_backend(tmp_path, bad):
    client = _client(tmp_path)
    assert "one of: 30, 90, 365" in client.error("settings.setRetentionDays", days=bad)
    assert client.result("settings.get")["auditRetentionDays"] == 90


def test_a_value_of_the_wrong_type_is_refused(tmp_path):
    client = _client(tmp_path)
    assert "whole number" in client.error("settings.setRetentionDays", days="30")
    assert "whole number" in client.error("settings.setRetentionDays", days=True)
