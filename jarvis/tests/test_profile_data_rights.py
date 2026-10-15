"""Per-profile export and profile erasure (ESR-0061 WP5c,
EIP-ESR0061-005 6.5 and 6.6, decisions X1 and E1)."""

import json
import sqlite3

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.claude_key import SECRET_NAME
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from jarvis.shared.secret_store import SecretStore
from sentinel.core import SentinelTrustGateway

KEY = "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-abcdEFGH"


class _Backend:
    priority = 1

    def __init__(self):
        self.items = {}

    def get_password(self, service, username):
        return self.items.get((service, username))

    def set_password(self, service, username, password):
        self.items[(service, username)] = password

    def delete_password(self, service, username):
        self.items.pop((service, username), None)


class World:
    """A server with several profiles, notes for each, and a household note."""

    def __init__(self, tmp_path):
        self.tmp_path = tmp_path
        self.store_backend = _Backend()
        self.environ = {
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            "JARVIS_LOG_DIR": str(tmp_path / "logs"),
        }
        runtime = build_default_runtime(environ=self.environ, secret_store=SecretStore(self.store_backend))
        self.server = StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))
        self._next = 1
        self.ids: dict[str, str] = {}

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

    def make(self, name, role):
        self.ids[name] = self.result("profile.create", displayName=name, role=role)["id"]
        return self.ids[name]

    def use(self, name):
        self.result("profile.select", profileId=self.ids[name])

    def save_note(self, text):
        """Save a note for the signed-in profile (an Administrator or Adult)."""

        pending = self.result("memory.propose", content=text)["pendingId"]
        return self.result("memory.approve", pendingId=pending)

    def household_note(self, text):
        store = PersonalMemoryStore(self.tmp_path / "personal.db")
        service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=store)
        service.approve(service.propose(text, None).id)

    def rows(self, table, db="personal.db"):
        with sqlite3.connect(self.tmp_path / db) as connection:
            return connection.execute(f"SELECT * FROM {table}").fetchall()


@pytest.fixture
def world(tmp_path):
    w = World(tmp_path)
    w.make("Robert", "Administrator")
    w.make("Bea", "Adult")
    w.make("Sam", "Child")
    w.use("Robert")
    w.save_note("Robert takes tea, no sugar.")
    w.use("Bea")
    w.save_note("Bea is allergic to penicillin.")
    w.save_note("Bea runs on Tuesdays.")
    w.household_note("The bins go out on Tuesday.")
    w.use("Robert")
    return w


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _read_json(path):
    return json.loads(_read(path))


# --- export -----------------------------------------------------------------------------------------------------


def test_an_export_holds_the_profiles_own_notes_and_nothing_else(world, tmp_path):
    out = tmp_path / "exports"

    reply = world.result("profile.export", profileId=world.ids["Bea"], directory=str(out))

    assert reply["noteCount"] == 2
    portable = _read_json(reply["jsonPath"])
    assert portable["schemaVersion"] == 1
    assert portable["profile"]["displayName"] == "Bea"
    assert sorted(n["text"] for n in portable["notes"]) == ["Bea is allergic to penicillin.", "Bea runs on Tuesdays."]
    assert all(n["agreedAt"] is not None for n in portable["notes"])
    text = _read(reply["markdownPath"]) + json.dumps(portable)
    # Not Robert's note, not the household note, not any id of another profile.
    assert "tea, no sugar" not in text
    assert "bins go out" not in text
    assert world.ids["Robert"] not in text and world.ids["Sam"] not in text


def test_an_export_never_holds_the_claude_key_and_names_files_without_the_profile_name(world, tmp_path):
    world.result("provider.setClaudeKey", key=KEY)
    out = tmp_path / "exports"

    reply = world.result("profile.export", profileId=world.ids["Bea"], directory=str(out))

    for path in out.iterdir():
        assert KEY not in path.read_text(encoding="utf-8")
        assert "Bea" not in path.name
    assert reply["markdownPath"].endswith(".md") and reply["jsonPath"].endswith(".json")
    assert KEY not in json.dumps(reply)


def test_the_reply_names_files_and_counts_but_never_content(world, tmp_path):
    reply = world.result("profile.export", profileId=world.ids["Bea"], directory=str(tmp_path / "e"))
    assert set(reply) == {"markdownPath", "jsonPath", "noteCount"}
    assert "penicillin" not in json.dumps(reply)


def test_a_profile_with_no_notes_exports_a_valid_empty_file(world, tmp_path):
    reply = world.result("profile.export", profileId=world.ids["Sam"], directory=str(tmp_path / "e"))
    assert reply["noteCount"] == 0
    assert _read_json(reply["jsonPath"])["notes"] == []
    assert "No notes are saved" in _read(reply["markdownPath"])


def test_an_administrator_exports_any_profile_including_a_childs(world, tmp_path):
    assert world.result("profile.export", profileId=world.ids["Sam"], directory=str(tmp_path / "e"))["noteCount"] == 0
    assert world.result("profile.export", profileId=world.ids["Bea"], directory=str(tmp_path / "e"))["noteCount"] == 2


def test_an_adult_can_export_only_their_own_data(world, tmp_path):
    world.use("Bea")
    assert world.result("profile.export", profileId=world.ids["Bea"], directory=str(tmp_path / "e"))["noteCount"] == 2
    assert "only its own data" in world.error(
        "profile.export", profileId=world.ids["Robert"], directory=str(tmp_path / "e2")
    )
    assert not (tmp_path / "e2").exists()


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_cannot_export(world, tmp_path, role):
    world.make("Visitor", role)
    world.use("Visitor")
    assert "Ask an Administrator" in world.error(
        "profile.export", profileId=world.ids["Visitor"], directory=str(tmp_path / "e")
    )


def test_exporting_an_unknown_profile_or_with_bad_parameters_is_refused(world, tmp_path):
    assert "No such profile" in world.error("profile.export", profileId="nope", directory=str(tmp_path / "e"))
    assert "profileId" in world.error("profile.export", profileId=5, directory=str(tmp_path / "e"))
    assert "directory" in world.error("profile.export", profileId=world.ids["Bea"], directory="  ")


# --- erasure ----------------------------------------------------------------------------------------------------


def test_erasing_a_profile_removes_it_and_its_own_notes_only(world):
    reply = world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")

    assert reply == {"erased": True, "notesRemoved": 2, "proposalsDiscarded": 0}
    names = [p["displayName"] for p in world.result("profile.list")["profiles"]]
    assert names == ["Robert", "Sam"]
    contents = sorted(row[1] for row in world.rows("personal_memory"))
    assert contents == ["Robert takes tea, no sugar.", "The bins go out on Tuesday."]


def test_consent_decisions_are_kept_as_content_free_history(world):
    before = len(world.rows("consent_decisions"))
    world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")
    assert len(world.rows("consent_decisions")) == before


def test_pending_proposals_of_the_erased_profile_are_discarded_so_a_late_approval_cannot_recreate_a_note(world):
    world.use("Bea")
    pending = world.result("memory.propose", content="Bea wants a pony.")["pendingId"]
    world.use("Robert")

    reply = world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")

    assert reply["proposalsDiscarded"] == 1
    assert world.error("memory.approve", pendingId=pending)
    assert all("pony" not in row[1] for row in world.rows("personal_memory"))


def test_the_erased_profiles_in_memory_conversation_is_dropped(world):
    runtime = world.server._runtime
    runtime._cognitive_core_for(world.ids["Bea"])
    assert world.ids["Bea"] in runtime._cognitive_cores

    world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")

    assert world.ids["Bea"] not in runtime._cognitive_cores


def test_the_signed_in_profile_cannot_be_erased(world):
    assert "Switch to another profile first" in world.error(
        "profile.erase", profileId=world.ids["Robert"], confirmName="Robert"
    )
    assert len(world.result("profile.list")["profiles"]) == 3


def test_the_last_administrator_cannot_be_erased_by_the_service_rule(tmp_path):
    # Through the screen this cannot be reached (only an Administrator may erase, and
    # not themselves, so another Administrator always exists); the rule is the
    # service's own defence and is exercised directly.
    w = World(tmp_path)
    w.make("Robert", "Administrator")
    w.make("Helper", "Adult")
    service = w.server._identity_service
    with pytest.raises(Exception, match="last Administrator"):
        service.check_erasable(w.ids["Robert"], active_profile_id=w.ids["Helper"])


def test_with_two_administrators_one_can_be_erased_and_the_other_then_cannot_erase_themselves(tmp_path):
    w = World(tmp_path)
    w.make("Robert", "Administrator")
    w.make("Rae", "Administrator")
    w.use("Robert")

    assert w.result("profile.erase", profileId=w.ids["Rae"], confirmName="Rae")["erased"] is True

    assert "Switch to another profile first" in w.error("profile.erase", profileId=w.ids["Robert"], confirmName="Robert")
    assert [p["displayName"] for p in w.result("profile.list")["profiles"]] == ["Robert"]


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_erase(world, role):
    world.make("Actor", role)
    world.use("Actor")
    assert "Only an Administrator" in world.error("profile.erase", profileId=world.ids["Sam"], confirmName="Sam")
    assert len(world.result("profile.list")["profiles"]) == 4


@pytest.mark.parametrize("typed", ["", "bea", "Be", "Robert", "BEA "])
def test_a_wrong_typed_name_erases_nothing(world, typed):
    assert "does not match" in world.error("profile.erase", profileId=world.ids["Bea"], confirmName=typed)
    assert len(world.result("profile.list")["profiles"]) == 3
    assert len(world.rows("personal_memory")) == 4


def test_the_typed_name_may_have_stray_spaces_but_must_otherwise_match(world):
    assert world.result("profile.erase", profileId=world.ids["Bea"], confirmName="  Bea  ")["erased"] is True


def test_erasing_an_unknown_profile_or_with_bad_parameters_is_refused(world):
    assert "No such profile" in world.error("profile.erase", profileId="nope", confirmName="x")
    assert "profileId" in world.error("profile.erase", profileId=3, confirmName="x")
    assert "confirmName" in world.error("profile.erase", profileId=world.ids["Bea"], confirmName=None)


def test_erasure_leaves_the_claude_key_and_settings_alone(world):
    world.result("provider.setClaudeKey", key=KEY)
    world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")
    assert world.store_backend.items  # the key is still stored
    assert world.result("provider.claudeKeyStatus")["configured"] is True
    assert SECRET_NAME in {name for (_, name) in world.store_backend.items}


def test_an_open_offer_to_ask_claude_for_the_erased_profile_is_dropped_with_its_question(world):
    offers = world.server._escalation_offers
    token = offers.issue(world.ids["Bea"], "a private question")
    other = offers.issue(world.ids["Robert"], "robert's question")

    world.result("profile.erase", profileId=world.ids["Bea"], confirmName="Bea")

    assert offers.redeem(token, world.ids["Bea"]) is None
    assert offers.redeem(other, world.ids["Robert"]) == "robert's question"
