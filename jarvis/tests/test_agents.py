"""Tests for the Agent Framework contract and GiaObservabilityAgent."""

import json
from datetime import UTC, datetime
from typing import Self

import pytest

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.agents.gia_agent import STATUS_REPORTED, GiaObservabilityAgent
from jarvis.agents.gia_engineering_agent import STATUS_REPORTED as ENGINEERING_STATUS_REPORTED
from jarvis.agents.gia_engineering_agent import GiaEngineeringAgent
from jarvis.agents.home_assistant_agent import (
    STATUS_REPORTED as HOME_ASSISTANT_STATUS_REPORTED,
)
from jarvis.agents.home_assistant_agent import HomeAssistantClient, HomeAssistantStateQueryAgent
from jarvis.gia.engineering_observability import EngineeringSnapshot
from jarvis.gia.observability import GiaSnapshot


class _FakeObserver:
    def __init__(self, snapshot: GiaSnapshot) -> None:
        self._snapshot = snapshot

    def snapshot(self) -> GiaSnapshot:
        return self._snapshot


def _snapshot() -> GiaSnapshot:
    return GiaSnapshot(
        cpu_percent=12.5,
        memory_percent=40.0,
        memory_used_mb=4096.0,
        memory_total_mb=16384.0,
        disk_percent=55.0,
        disk_used_gb=250.0,
        disk_total_gb=500.0,
        process_status="running",
        process_uptime_seconds=3600.0,
        process_cpu_percent=1.2,
        process_memory_mb=128.0,
        engineering_tools_running={"vscode": True},
        captured_at=datetime(2026, 8, 5, tzinfo=UTC),
    )


def test_agent_request_rejects_empty_task() -> None:
    with pytest.raises(ValueError, match="task"):
        AgentRequest(task="   ")


def test_agent_request_parameters_are_immutable() -> None:
    request = AgentRequest(task="snapshot", parameters={"a": "b"})

    with pytest.raises(TypeError):
        request.parameters["a"] = "c"  # type: ignore[index]


def test_agent_result_rejects_empty_status() -> None:
    with pytest.raises(ValueError, match="status"):
        AgentResult(status="")


def test_agent_result_payload_is_immutable() -> None:
    result = AgentResult(status="reported", payload={"a": "b"})

    with pytest.raises(TypeError):
        result.payload["a"] = "c"  # type: ignore[index]


def test_gia_observability_agent_name() -> None:
    assert GiaObservabilityAgent.name == "gia-observability"


def test_gia_observability_agent_reports_real_snapshot_fields() -> None:
    agent = GiaObservabilityAgent(_FakeObserver(_snapshot()))

    result = agent.execute(AgentRequest(task="snapshot"))

    assert result.status == STATUS_REPORTED
    assert result.payload["cpuPercent"] == "12.5"
    assert result.payload["memoryPercent"] == "40.0"
    assert result.payload["processStatus"] == "running"
    assert result.payload["capturedAt"] == "2026-08-05T00:00:00+00:00"


def test_gia_observability_agent_ignores_request_parameters() -> None:
    agent = GiaObservabilityAgent(_FakeObserver(_snapshot()))

    result = agent.execute(AgentRequest(task="anything", parameters={"unused": "value"}))

    assert result.status == STATUS_REPORTED


class _FakeEngineeringObserver:
    def __init__(self, snapshot: EngineeringSnapshot) -> None:
        self._snapshot = snapshot

    def snapshot(self) -> EngineeringSnapshot:
        return self._snapshot


def _engineering_snapshot() -> EngineeringSnapshot:
    return EngineeringSnapshot(
        git_branch="main",
        git_uncommitted_files=1,
        git_last_commit_sha="abc123def456",
        git_last_commit_message="ESR-0054 WP2: GIA Phase 3a",
        repository_validation_errors=0,
        repository_validation_warnings=298,
        current_repository_baseline="RBL-0034",
        latest_registered_session="ESR-0055",
        latest_registered_session_status="Open",
        captured_at=datetime(2026, 8, 28, tzinfo=UTC),
    )


def test_gia_engineering_agent_name() -> None:
    assert GiaEngineeringAgent.name == "gia-engineering"


def test_gia_engineering_agent_reports_real_snapshot_fields() -> None:
    agent = GiaEngineeringAgent(_FakeEngineeringObserver(_engineering_snapshot()))

    result = agent.execute(AgentRequest(task="snapshot"))

    assert result.status == ENGINEERING_STATUS_REPORTED
    assert result.payload["gitBranch"] == "main"
    assert result.payload["gitUncommittedFiles"] == "1"
    assert result.payload["gitLastCommitSha"] == "abc123def456"
    assert result.payload["gitLastCommitMessage"] == "ESR-0054 WP2: GIA Phase 3a"
    assert result.payload["repositoryValidationErrors"] == "0"
    assert result.payload["repositoryValidationWarnings"] == "298"
    assert result.payload["currentRepositoryBaseline"] == "RBL-0034"
    assert result.payload["latestRegisteredSession"] == "ESR-0055"
    assert result.payload["latestRegisteredSessionStatus"] == "Open"
    assert result.payload["capturedAt"] == "2026-08-28T00:00:00+00:00"


def test_gia_engineering_agent_ignores_request_parameters() -> None:
    agent = GiaEngineeringAgent(_FakeEngineeringObserver(_engineering_snapshot()))

    result = agent.execute(AgentRequest(task="anything", parameters={"unused": "value"}))

    assert result.status == ENGINEERING_STATUS_REPORTED


class _FakeUrlopenResponse:
    def __init__(self, payload_bytes: bytes) -> None:
        self._payload_bytes = payload_bytes

    def read(self) -> bytes:
        return self._payload_bytes

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        return None


def test_home_assistant_client_rejects_empty_base_url() -> None:
    with pytest.raises(ValueError, match="base_url"):
        HomeAssistantClient(base_url="  ", token="secret")


def test_home_assistant_client_rejects_empty_token() -> None:
    with pytest.raises(ValueError, match="token"):
        HomeAssistantClient(base_url="http://homeassistant.local:8123", token="  ")


def test_home_assistant_client_get_state_sends_bearer_auth_header(monkeypatch) -> None:
    captured_requests = []

    def _fake_urlopen(request, timeout):
        captured_requests.append(request)
        return _FakeUrlopenResponse(json.dumps({"state": "21.5", "last_changed": "2026-09-16T08:00:00+00:00"}).encode())

    monkeypatch.setattr("jarvis.agents.home_assistant_agent.urllib.request.urlopen", _fake_urlopen)
    client = HomeAssistantClient(base_url="http://homeassistant.local:8123/", token="secret-token")

    state = client.get_state("sensor.living_room_temperature")

    assert state == {"state": "21.5", "last_changed": "2026-09-16T08:00:00+00:00"}
    assert len(captured_requests) == 1
    sent = captured_requests[0]
    assert sent.full_url == "http://homeassistant.local:8123/api/states/sensor.living_room_temperature"
    assert sent.get_header("Authorization") == "Bearer secret-token"


def test_home_assistant_client_get_state_raises_on_connection_failure(monkeypatch) -> None:
    import urllib.error

    def _fake_urlopen(request, timeout):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr("jarvis.agents.home_assistant_agent.urllib.request.urlopen", _fake_urlopen)
    client = HomeAssistantClient(base_url="http://homeassistant.local:8123", token="secret-token")

    with pytest.raises(RuntimeError, match="sensor.front_door"):
        client.get_state("sensor.front_door")


class _FakeHomeAssistantClient:
    def __init__(self, state: dict[str, object]) -> None:
        self._state = state
        self.requested_entity_id: str | None = None

    def get_state(self, entity_id: str) -> dict[str, object]:
        self.requested_entity_id = entity_id
        return self._state


def test_home_assistant_state_query_agent_name() -> None:
    assert HomeAssistantStateQueryAgent.name == "home-assistant-state-query"


def test_home_assistant_state_query_agent_reports_requested_entity_state() -> None:
    client = _FakeHomeAssistantClient({"state": "locked", "last_changed": "2026-09-16T07:00:00+00:00"})
    agent = HomeAssistantStateQueryAgent(client)

    result = agent.execute(AgentRequest(task="query", parameters={"entityId": "lock.front_door"}))

    assert result.status == HOME_ASSISTANT_STATUS_REPORTED
    assert result.payload["entityId"] == "lock.front_door"
    assert result.payload["state"] == "locked"
    assert result.payload["lastChanged"] == "2026-09-16T07:00:00+00:00"
    assert client.requested_entity_id == "lock.front_door"


def test_home_assistant_state_query_agent_requires_entity_id_parameter() -> None:
    agent = HomeAssistantStateQueryAgent(_FakeHomeAssistantClient({"state": "x"}))

    with pytest.raises(ValueError, match="entityId"):
        agent.execute(AgentRequest(task="query"))
