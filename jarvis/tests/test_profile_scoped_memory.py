"""Tests for EBG-0132 (ESR-0059 WP13): memory scoped to the active profile.

Programme Sponsor's decisions: memories saved before profiles existed become
shared household notes, visible to every profile and deletable only by an
Administrator; with no profile selected, saving a memory is refused and
conversation uses household notes only.
"""

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


def _save(service, content, profile_id):
    return service.approve(service.propose(content, profile_id).id)


# --- visibility -----------------------------------------------------------


def test_a_profile_sees_its_own_memories_and_household_notes_only(tmp_path):
    service = _service(tmp_path)
    _save(service, "A's secret.", "profile-a")
    _save(service, "B's secret.", "profile-b")
    _save(service, "Bins go out on Tuesday.", None)

    assert [r.content for r in service.list_visible("profile-a")] == ["A's secret.", "Bins go out on Tuesday."]
    assert [r.content for r in service.list_visible("profile-b")] == ["B's secret.", "Bins go out on Tuesday."]
    assert [r.content for r in service.list_visible(None)] == ["Bins go out on Tuesday."]
    assert service.count_visible("profile-a") == 2


class _RecordingProvider:
    name = "recording"

    def __init__(self) -> None:
        self.received = []

    def generate(self, request):
        self.received.append(request)
        return ConversationResponse(message=f"reply to {request.message}", provider=self.name, is_model_reply=True)


def test_conversation_carries_only_the_active_profiles_memory_and_history(tmp_path):
    service = _service(tmp_path)
    _save(service, "A likes tea.", "profile-a")
    _save(service, "B likes coffee.", "profile-b")
    provider = _RecordingProvider()
    runtime = GuardianRuntime(conversation_provider=provider, memory_service=service)
    runtime.start()

    runtime.converse("hello from A", "profile-a")
    runtime.converse("hello from B", "profile-b")

    a_turn, b_turn = provider.received
    assert a_turn.memory_notes == ("A likes tea.",)
    assert b_turn.memory_notes == ("B likes coffee.",)
    # B's turn must not carry A's conversation either.
    assert b_turn.history == ()


# --- deletion rules -------------------------------------------------------


def test_a_profile_can_delete_its_own_memory(tmp_path):
    service = _service(tmp_path)
    record = _save(service, "Mine.", "profile-a")

    service.delete(record.id, "profile-a")

    assert service.list_records() == ()


def test_another_profiles_memory_looks_exactly_like_a_missing_one(tmp_path):
    service = _service(tmp_path)
    record = _save(service, "A's secret.", "profile-a")

    with pytest.raises(KeyError, match="No stored memory found"):
        service.delete(record.id, "profile-b", is_administrator=True)

    assert [r.content for r in service.list_records()] == ["A's secret."]


def test_only_an_administrator_can_delete_a_household_note(tmp_path):
    service = _service(tmp_path)
    note = _save(service, "Bins go out on Tuesday.", None)

    with pytest.raises(PermissionError, match="Only an Administrator"):
        service.delete(note.id, "profile-a")

    service.delete(note.id, "profile-admin", is_administrator=True)
    assert service.list_records() == ()


# --- RPC surface ----------------------------------------------------------


def _server(tmp_path) -> StdioRpcServer:
    return StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def _call(server, method, params, request_id=1):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}))


def _profile(server, name, role):
    created = _call(server, "profile.create", {"displayName": name, "role": role})["result"]
    _call(server, "profile.select", {"profileId": created["id"]})
    return created["id"]


def _remember(server, content):
    pending = _call(server, "memory.propose", {"content": content})["result"]["pendingId"]
    return _call(server, "memory.approve", {"pendingId": pending})["result"]["id"]


def test_saving_a_memory_without_a_selected_profile_is_refused(tmp_path):
    response = _call(_server(tmp_path), "memory.propose", {"content": "Tea, no sugar."})

    assert "Select a profile before saving a memory" in response["error"]["message"]


def test_profiles_see_only_their_own_memories_over_rpc(tmp_path):
    server = _server(tmp_path)
    alice = _profile(server, "Alice", "Adult")
    _remember(server, "Alice's surprise party plan.")
    _profile(server, "Ben", "Child")
    _remember(server, "Ben's favourite dinosaur.")

    ben_view = _call(server, "memory.list", {})["result"]["records"]
    assert [r["content"] for r in ben_view] == ["Ben's favourite dinosaur."]
    assert _call(server, "memory.status", {})["result"]["recordCount"] == 1

    _call(server, "profile.select", {"profileId": alice})
    alice_view = _call(server, "memory.list", {})["result"]["records"]
    assert [r["content"] for r in alice_view] == ["Alice's surprise party plan."]
    assert alice_view[0]["profileId"] == alice


def test_restore_gives_memories_from_unknown_profiles_to_the_restoring_profile(tmp_path):
    source = _server(tmp_path / "source")
    _profile(source, "Old device user", "Adult")
    _remember(source, "Tea, no sugar.")
    backup = _call(source, "memory.backup", {"backupDir": str(tmp_path / "backups")})["result"]["path"]

    target = _server(tmp_path / "target")
    new_owner = _profile(target, "Robert", "Administrator")
    restored = _call(target, "memory.restore", {"backupPath": backup})["result"]

    assert restored == {"recordCount": 1, "reassignedToActiveProfile": 1}
    records = _call(target, "memory.list", {})["result"]["records"]
    assert [(r["content"], r["profileId"]) for r in records] == [("Tea, no sugar.", new_owner)]


def test_restore_without_a_selected_profile_is_refused(tmp_path):
    source = _server(tmp_path / "source")
    _profile(source, "Robert", "Adult")
    _remember(source, "Tea, no sugar.")
    backup = _call(source, "memory.backup", {"backupDir": str(tmp_path / "backups")})["result"]["path"]

    response = _call(_server(tmp_path / "target"), "memory.restore", {"backupPath": backup})

    assert "Select a profile before restoring memory" in response["error"]["message"]


def test_a_backup_from_before_profile_scoping_restores_as_household_notes(tmp_path):
    store = PersonalMemoryStore(tmp_path / "m.db")
    legacy_backup = {
        "personal_memory": [
            {"id": "m1", "content": "Bins go out on Tuesday.", "created_at": "2026-09-01T00:00:00+00:00", "consent_decision_id": "d1"}
        ],
        "consent_decisions": [
            {
                "id": "d1",
                "capability": "memory_retention",
                "decision": "approved",
                "decided_at": "2026-09-01T00:00:00+00:00",
                "approver_label": "local-user",
                "sentinel_outcome": "Review",
                "sentinel_reason": "r",
            }
        ],
    }

    store.import_snapshot(legacy_backup)

    assert store.list_all()[0].profile_id is None
    assert [r.content for r in store.list_visible("anyone")] == ["Bins go out on Tuesday."]
