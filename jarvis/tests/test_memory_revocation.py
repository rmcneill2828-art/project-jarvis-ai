"""Tests for EBG-0145 (ESR-0059 WP10): per-item memory revocation, end to end
from the store to the RPC surface."""

import json

import pytest

from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.conversation import ConversationResponse
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from sentinel.core import SentinelTrustGateway


def _service(tmp_path) -> PersonalMemoryService:
    return PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "m.db"))


def test_store_delete_reports_whether_a_record_was_removed(tmp_path):
    service = _service(tmp_path)
    record = service.approve(service.propose("Robert prefers dark mode.").id)
    store = service._store

    assert store.delete(record.id) is True
    assert store.delete(record.id) is False


def test_service_delete_removes_only_that_memory_and_keeps_its_consent_record(tmp_path):
    service = _service(tmp_path)
    keep = service.approve(service.propose("Keep this.").id)
    revoke = service.approve(service.propose("Revoke this.").id)

    service.delete(revoke.id)

    assert [r.content for r in service.list_records()] == ["Keep this."]
    assert service._store.get_decision(revoke.consent_decision_id).decision == "approved"
    assert keep.id != revoke.id


def test_service_delete_of_unknown_id_is_an_error_not_a_silent_success(tmp_path):
    with pytest.raises(KeyError, match="No stored memory"):
        _service(tmp_path).delete("no-such-id")


class _RecordingProvider:
    name = "recording"

    def __init__(self) -> None:
        self.received = []

    def generate(self, request):
        self.received.append(request)
        return ConversationResponse(message="ok", provider=self.name, is_model_reply=True)


def test_a_revoked_memory_stops_reaching_conversation_turns_immediately(tmp_path):
    provider = _RecordingProvider()
    runtime = GuardianRuntime(conversation_provider=provider, memory_service=_service(tmp_path))
    runtime.start()
    record = runtime.approve_memory(runtime.propose_memory("Robert dislikes cilantro.").id)

    runtime.converse("first")
    runtime.delete_memory(record.id)
    runtime.converse("second")

    assert provider.received[0].memory_notes == ("Robert dislikes cilantro.",)
    assert provider.received[1].memory_notes == ()


def _server(tmp_path) -> StdioRpcServer:
    return StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def _call(server, request_id, method, params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}))


def test_memory_delete_over_rpc(tmp_path):
    server = _server(tmp_path)
    pending = _call(server, 1, "memory.propose", {"content": "Tea, no sugar."})["result"]["pendingId"]
    record_id = _call(server, 2, "memory.approve", {"pendingId": pending})["result"]["id"]

    deleted = _call(server, 3, "memory.delete", {"recordId": record_id})

    assert deleted["result"] == {"recordId": record_id, "deleted": True}
    assert _call(server, 4, "memory.list", {})["result"]["records"] == []
    assert _call(server, 5, "memory.status", {})["result"]["recordCount"] == 0


@pytest.mark.parametrize("params", [{}, {"recordId": ""}, {"recordId": 7}])
def test_memory_delete_rejects_a_missing_or_malformed_id(tmp_path, params):
    response = _call(_server(tmp_path), 1, "memory.delete", params)

    assert "recordId" in response["error"]["message"]


def test_memory_delete_of_an_unknown_id_is_an_rpc_error(tmp_path):
    response = _call(_server(tmp_path), 1, "memory.delete", {"recordId": "no-such-id"})

    assert "No stored memory" in response["error"]["message"]
