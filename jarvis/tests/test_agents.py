"""Tests for the Agent Framework contract and GiaObservabilityAgent."""

from datetime import UTC, datetime

import pytest

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.agents.gia_agent import STATUS_REPORTED, GiaObservabilityAgent
from jarvis.agents.gia_engineering_agent import STATUS_REPORTED as ENGINEERING_STATUS_REPORTED
from jarvis.agents.gia_engineering_agent import GiaEngineeringAgent
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
    assert result.payload["capturedAt"] == "2026-08-28T00:00:00+00:00"


def test_gia_engineering_agent_ignores_request_parameters() -> None:
    agent = GiaEngineeringAgent(_FakeEngineeringObserver(_engineering_snapshot()))

    result = agent.execute(AgentRequest(task="anything", parameters={"unused": "value"}))

    assert result.status == ENGINEERING_STATUS_REPORTED
