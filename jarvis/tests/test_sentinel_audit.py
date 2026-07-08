"""Tests for Sentinel audit trail infrastructure."""

import json

import pytest

from sentinel.audit import AuditEvent, JsonAuditRecorder, MemoryAuditRecorder
from sentinel.core import SentinelRequest, SentinelTrustGateway
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.providers import ProviderRequest, ProviderResponse


class _StubProvider:
    def __init__(self, name: str, capabilities: tuple[str, ...]) -> None:
        self._name = name
        self._capabilities = capabilities

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> tuple[str, ...]:
        return self._capabilities

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider_name=self._name,
            content=f"handled: {request.prompt}",
            capability=request.capability,
        )


class _FailingProvider(_StubProvider):
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        raise RuntimeError("provider failure")


def test_audit_event_requires_non_empty_fields():
    with pytest.raises(ValueError):
        AuditEvent(event_type="", outcome="Allow", summary="summary")
    with pytest.raises(ValueError):
        AuditEvent(event_type="decision", outcome="", summary="summary")
    with pytest.raises(ValueError):
        AuditEvent(event_type="decision", outcome="Allow", summary="")


def test_memory_audit_recorder_records_events_in_order():
    recorder = MemoryAuditRecorder()
    first = AuditEvent(event_type="a", outcome="Allow", summary="first")
    second = AuditEvent(event_type="b", outcome="Deny", summary="second")

    recorder.record(first)
    recorder.record(second)

    assert recorder.events() == (first, second)


def test_memory_audit_recorder_instances_do_not_share_state():
    a = MemoryAuditRecorder()
    b = MemoryAuditRecorder()

    a.record(AuditEvent(event_type="a", outcome="Allow", summary="only in a"))

    assert a.events() != ()
    assert b.events() == ()


def test_json_audit_recorder_round_trips_events(tmp_path):
    path = tmp_path / "audit.jsonl"
    recorder = JsonAuditRecorder(path)
    event = AuditEvent(
        event_type="sentinel_decision",
        outcome="Allow",
        summary="allowed",
        metadata={"source": "test"},
    )

    recorder.record(event)

    assert path.exists()
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["event_type"] == "sentinel_decision"

    recovered = JsonAuditRecorder(path).events()
    assert len(recovered) == 1
    assert recovered[0].event_type == "sentinel_decision"
    assert recovered[0].outcome == "Allow"
    assert recovered[0].metadata == {"source": "test"}


def test_json_audit_recorder_returns_empty_tuple_when_file_missing(tmp_path):
    recorder = JsonAuditRecorder(tmp_path / "missing.jsonl")

    assert recorder.events() == ()


def test_sentinel_trust_gateway_records_audit_event_by_default():
    gateway = SentinelTrustGateway()
    request = SentinelRequest(source="test", intent="do a thing")

    gateway.evaluate(request)

    events = gateway.audit_events()
    assert len(events) == 1
    assert events[0].event_type == "sentinel_decision"
    assert events[0].outcome == "Allow"
    assert events[0].metadata["source"] == "test"


def test_sentinel_trust_gateway_uses_injected_recorder():
    recorder = MemoryAuditRecorder()
    gateway = SentinelTrustGateway(audit_recorder=recorder)
    request = SentinelRequest(source="test", intent="do a thing", requires_approval=True)

    gateway.evaluate(request)

    assert len(recorder.events()) == 1
    assert recorder.events()[0].outcome == "Review"
    assert gateway.audit_events() == recorder.events()


def test_provider_orchestrator_records_audit_event_on_success():
    orchestrator = ProviderOrchestrator()
    provider = _StubProvider("local", ("text-generation",))
    orchestrator.register_provider(provider)
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("local",)))

    gateway = SentinelTrustGateway()
    sentinel_response = gateway.evaluate(SentinelRequest(source="test", intent="generate"))

    orchestrator.execute(sentinel_response, ProviderRequest(prompt="hello"))

    events = orchestrator.audit_events()
    assert len(events) == 1
    assert events[0].event_type == "provider_execution"
    assert events[0].outcome == "succeeded"
    assert events[0].metadata["selected_provider"] == "local"


def test_provider_orchestrator_records_audit_event_on_failure():
    recorder = MemoryAuditRecorder()
    orchestrator = ProviderOrchestrator(audit_recorder=recorder)
    provider = _FailingProvider("local", ("text-generation",))
    orchestrator.register_provider(provider)
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("local",)))

    gateway = SentinelTrustGateway()
    sentinel_response = gateway.evaluate(SentinelRequest(source="test", intent="generate"))

    with pytest.raises(RuntimeError):
        orchestrator.execute(sentinel_response, ProviderRequest(prompt="hello"))

    events = recorder.events()
    assert len(events) == 1
    assert events[0].event_type == "provider_execution"
    assert events[0].outcome == "failed"
