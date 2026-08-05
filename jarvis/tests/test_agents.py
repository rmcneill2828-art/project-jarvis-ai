"""Tests for the Agent Framework contract and GiaObservabilityAgent."""

from datetime import UTC, datetime

import pytest

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.agents.gia_agent import STATUS_REPORTED, GiaObservabilityAgent
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
