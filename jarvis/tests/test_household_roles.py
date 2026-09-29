"""Tests for EBG-0132 (ESR-0059 WP14): GAM-0001 Section 8.1 household roles
enforced for memory - approval rights, Guest access to household notes, and
Administrator-only backup and restore."""

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


def _server(tmp_path) -> StdioRpcServer:
    return StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def _call(server, method, params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def _as(server, role):
    created = _call(server, "profile.create", {"displayName": role, "role": role})["result"]
    _call(server, "profile.select", {"profileId": created["id"]})
    return created["id"]


def _propose(server, content):
    return _call(server, "memory.propose", {"content": content})["result"]["pendingId"]


# --- approval rights ------------------------------------------------------


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_cannot_approve_saving_a_memory(tmp_path, role):
    server = _server(tmp_path)
    _as(server, role)
    pending = _propose(server, "I like dinosaurs.")

    response = _call(server, "memory.approve", {"pendingId": pending})

    assert "Only an Administrator or Adult profile can approve saving a memory" in response["error"]["message"]
    assert _call(server, "memory.list", {})["result"]["records"] == []


@pytest.mark.parametrize("role", ["Administrator", "Adult"])
def test_an_administrator_or_adult_can_approve(tmp_path, role):
    server = _server(tmp_path)
    _as(server, role)

    response = _call(server, "memory.approve", {"pendingId": _propose(server, "Tea, no sugar.")})

    assert response["result"]["content"] == "Tea, no sugar."


def test_approving_with_no_profile_selected_is_refused(tmp_path):
    response = _call(_server(tmp_path), "memory.approve", {"pendingId": "anything"})

    assert "Select a profile first" in response["error"]["message"]


def test_anyone_can_decline_their_own_proposal(tmp_path):
    """Declining stores nothing, so it is not restricted."""

    server = _server(tmp_path)
    _as(server, "Child")

    response = _call(server, "memory.deny", {"pendingId": _propose(server, "Never mind.")})

    assert response["result"]["decision"] == "denied"


# --- Guest access to household notes --------------------------------------


def test_a_guest_does_not_see_household_notes_in_list_or_count(tmp_path):
    server = _server(tmp_path)
    store = PersonalMemoryStore(tmp_path / "personal.db")
    household = PersonalMemoryService(gateway=SentinelTrustGateway(), store=store)
    household.approve(household.propose("The wifi password is on the fridge.", None).id)

    _as(server, "Adult")
    assert [r["content"] for r in _call(server, "memory.list", {})["result"]["records"]] == [
        "The wifi password is on the fridge."
    ]

    _as(server, "Guest")
    assert _call(server, "memory.list", {})["result"]["records"] == []
    assert _call(server, "memory.status", {})["result"]["recordCount"] == 0


class _RecordingProvider:
    name = "recording"

    def __init__(self) -> None:
        self.received = []

    def generate(self, request):
        self.received.append(request)
        return ConversationResponse(message="ok", provider=self.name, is_model_reply=True)


def test_a_guests_conversation_never_carries_household_notes(tmp_path):
    service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(tmp_path / "m.db"))
    service.approve(service.propose("The wifi password is on the fridge.", None).id)
    provider = _RecordingProvider()
    runtime = GuardianRuntime(conversation_provider=provider, memory_service=service)
    runtime.start()

    runtime.converse("hi", "guest-id", include_household=False)
    runtime.converse("hi", "adult-id")

    assert provider.received[0].memory_notes == ()
    assert provider.received[1].memory_notes == ("The wifi password is on the fridge.",)


# --- backup and restore ---------------------------------------------------


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_back_up_or_restore(tmp_path, role):
    server = _server(tmp_path)
    _as(server, role)

    backup = _call(server, "memory.backup", {"backupDir": str(tmp_path / "backups")})
    restore = _call(server, "memory.restore", {"backupPath": str(tmp_path / "none.json")})

    assert "Only an Administrator profile can back up memory" in backup["error"]["message"]
    assert "Only an Administrator profile can restore memory" in restore["error"]["message"]
    assert not (tmp_path / "backups").exists()


def test_an_administrator_can_back_up(tmp_path):
    server = _server(tmp_path)
    _as(server, "Administrator")

    response = _call(server, "memory.backup", {"backupDir": str(tmp_path / "backups")})

    assert response["result"]["path"].endswith(".json")
