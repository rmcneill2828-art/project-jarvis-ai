"""The Claude key in the credential store: setting, removing, testing and
applying it with no restart (ESR-0061 WP5a, EIP-ESR0061-005 6.1 to 6.3).

A fake credential backend stands in for the Windows Credential Manager, and
`urllib.request.urlopen` is replaced, so nothing real is touched and the tests
can see exactly what was sent where.
"""

import json
import logging
import os
import urllib.error

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.claude_key import (
    BAD_FORMAT_MESSAGE,
    NO_STORE_MESSAGE,
    SECRET_NAME,
    ClaudeKeyManager,
    looks_like_claude_key,
)
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.shared.secret_store import SERVICE_NAME, SecretStore, SecretStoreError

REAL_LOOKING_KEY = "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-abcdEFGH"
OTHER_KEY = "sk-ant-api03-ZzYyXxWwVvUuTtSsRrQqPpOoNnMmLlKkJjIiHh9876543210"
OLLAMA_PREFIX = "http://127.0.0.1:1"


class FakeBackend:
    """An in-memory credential store with the keyring backend's three calls."""

    priority = 1

    def __init__(self) -> None:
        self.items: dict[tuple[str, str], str] = {}
        self.fail_on: str | None = None

    def _maybe_fail(self, operation: str) -> None:
        if self.fail_on == operation:
            raise OSError(f"backend exploded and mentioned {REAL_LOOKING_KEY}")

    def get_password(self, service, username):
        self._maybe_fail("get")
        return self.items.get((service, username))

    def set_password(self, service, username, password):
        self._maybe_fail("set")
        self.items[(service, username)] = password

    def delete_password(self, service, username):
        self._maybe_fail("delete")
        if (service, username) not in self.items:
            raise _PasswordDeleteError("not found")
        del self.items[(service, username)]


class _PasswordDeleteError(Exception):
    pass


_PasswordDeleteError.__name__ = "PasswordDeleteError"


class _Response:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def read(self):
        return self._body


class _Network:
    def __init__(self):
        self.claude_calls: list[dict] = []

    def urlopen(self, request, timeout):
        url = request.full_url
        if "api.anthropic.com" in url:
            self.claude_calls.append(
                {"headers": {k.lower(): v for k, v in request.header_items()}, "body": json.loads(request.data)}
            )
            return _Response(
                {
                    "model": "claude-sonnet-5-5",
                    "content": [{"type": "text", "text": "OK"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 20, "output_tokens": 2},
                }
            )
        raise urllib.error.URLError("connection refused")


@pytest.fixture
def network(monkeypatch):
    fake = _Network()
    monkeypatch.setattr("urllib.request.urlopen", fake.urlopen)
    return fake


@pytest.fixture(autouse=True)
def no_host_key(monkeypatch):
    # The host machine's own key must never leak into these tests.
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def _server(tmp_path, *, store=None, environ_extra=None):
    environ = {
        "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        "JARVIS_OLLAMA_ENDPOINT": OLLAMA_PREFIX,
        "JARVIS_LOG_DIR": str(tmp_path / "logs"),
        **(environ_extra or {}),
    }
    runtime = build_default_runtime(environ=environ, secret_store=store)
    return StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))


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
        return created["id"]


def _admin(tmp_path, store=None, environ_extra=None):
    client = _Client(_server(tmp_path, store=store, environ_extra=environ_extra))
    client.sign_in("Robert", "Administrator")
    return client


# --- the key format ---------------------------------------------------------------------------------------------


def test_the_format_check_accepts_a_claude_key_and_refuses_everything_else():
    assert looks_like_claude_key(REAL_LOOKING_KEY)
    for bad in ["", "sk-ant-", "sk-ant-short", "sk-proj-" + "a" * 40, "not a key at all", "sk-ant-" + "a b" * 10]:
        assert not looks_like_claude_key(bad), bad


# --- the store --------------------------------------------------------------------------------------------------


def test_the_store_round_trips_and_a_missing_delete_is_not_an_error():
    backend = FakeBackend()
    store = SecretStore(backend)
    assert store.available
    store.set("k", "value")
    assert backend.items[(SERVICE_NAME, "k")] == "value"
    assert store.get("k") == "value"
    store.delete("k")
    store.delete("k")
    assert store.get("k") is None


def test_an_unavailable_store_holds_nothing_and_refuses_writes():
    store = SecretStore.unavailable()
    assert not store.available
    assert store.get("k") is None
    store.delete("k")
    with pytest.raises(SecretStoreError):
        store.set("k", "v")


def test_a_failing_backend_raises_a_fixed_message_that_never_holds_the_value():
    backend = FakeBackend()
    backend.fail_on = "set"
    store = SecretStore(backend)
    with pytest.raises(SecretStoreError) as caught:
        store.set("k", REAL_LOOKING_KEY)
    assert REAL_LOOKING_KEY not in str(caught.value)
    assert caught.value.__cause__ is None


def test_an_inert_keyring_backend_counts_as_unavailable():
    class Fail:
        __module__ = "keyring.backends.fail"
        priority = 0

    assert not SecretStore(Fail()).available


# --- the manager ------------------------------------------------------------------------------------------------


def test_the_environment_variable_wins_over_a_stored_key():
    store = SecretStore(FakeBackend())
    store.set(SECRET_NAME, OTHER_KEY)
    manager = ClaudeKeyManager(store, {"ANTHROPIC_API_KEY": f"  {REAL_LOOKING_KEY}  "})
    assert manager.resolve() == REAL_LOOKING_KEY
    assert manager.status() == {"configured": True, "source": "environment", "storeAvailable": True}


def test_a_blank_environment_variable_is_ignored_and_the_store_used():
    store = SecretStore(FakeBackend())
    store.set(SECRET_NAME, OTHER_KEY)
    manager = ClaudeKeyManager(store, {"ANTHROPIC_API_KEY": "   "})
    assert manager.resolve() == OTHER_KEY
    assert manager.status()["source"] == "store"


def test_a_broken_store_reads_as_no_key_rather_than_an_error():
    backend = FakeBackend()
    backend.fail_on = "get"
    manager = ClaudeKeyManager(SecretStore(backend), {})
    assert manager.resolve() is None
    assert manager.status()["configured"] is False


# --- the screen's methods, by role ------------------------------------------------------------------------------


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_see_or_change_the_key(tmp_path, network, role):
    client = _Client(_server(tmp_path, store=SecretStore(FakeBackend())))
    client.sign_in("Someone", role)
    for method, params in [
        ("provider.claudeKeyStatus", {}),
        ("provider.setClaudeKey", {"key": REAL_LOOKING_KEY}),
        ("provider.removeClaudeKey", {}),
        ("provider.testClaudeKey", {}),
    ]:
        assert "Only an Administrator" in client.error(method, **params)
    assert network.claude_calls == []


def test_with_no_profile_the_key_methods_ask_for_one(tmp_path):
    client = _Client(_server(tmp_path, store=SecretStore(FakeBackend())))
    assert "Select a profile" in client.error("provider.claudeKeyStatus")


# --- setting and removing, with no restart ----------------------------------------------------------------------


def test_a_key_set_in_the_app_is_used_by_the_next_question_and_a_removed_one_stops(tmp_path, network):
    backend = FakeBackend()
    client = _admin(tmp_path, store=SecretStore(backend))
    assert client.result("provider.claudeKeyStatus") == {"configured": False, "source": "none", "storeAvailable": True}
    assert client.result("provider.status")["claude"]["configured"] is False

    status = client.result("provider.setClaudeKey", key=REAL_LOOKING_KEY)
    assert status == {"configured": True, "source": "store", "storeAvailable": True}
    assert client.result("provider.status")["claude"]["configured"] is True
    assert backend.items[(SERVICE_NAME, SECRET_NAME)] == REAL_LOOKING_KEY
    # The key was never put in the process environment.
    assert "ANTHROPIC_API_KEY" not in os.environ

    offer = client.result("guardian.escalation.offer", message="hello")
    answer = client.result("guardian.escalate", token=offer["token"])
    assert answer["answeredBy"] == "claude"
    assert network.claude_calls[-1]["headers"]["x-api-key"] == REAL_LOOKING_KEY

    status = client.result("provider.removeClaudeKey")
    assert status == {"configured": False, "source": "none", "storeAvailable": True}
    assert client.result("provider.status")["claude"]["configured"] is False
    assert (SERVICE_NAME, SECRET_NAME) not in backend.items


def test_replacing_a_key_changes_what_is_sent(tmp_path, network):
    client = _admin(tmp_path, store=SecretStore(FakeBackend()))
    client.result("provider.setClaudeKey", key=REAL_LOOKING_KEY)
    client.result("provider.setClaudeKey", key=OTHER_KEY)
    offer = client.result("guardian.escalation.offer", message="hello")
    client.result("guardian.escalate", token=offer["token"])
    assert network.claude_calls[-1]["headers"]["x-api-key"] == OTHER_KEY


def test_removing_the_stored_key_leaves_an_environment_key_working(tmp_path, network):
    client = _admin(
        tmp_path, store=SecretStore(FakeBackend()), environ_extra={"ANTHROPIC_API_KEY": REAL_LOOKING_KEY}
    )
    assert client.result("provider.claudeKeyStatus")["source"] == "environment"
    client.result("provider.setClaudeKey", key=OTHER_KEY)
    assert client.result("provider.claudeKeyStatus")["source"] == "environment"
    status = client.result("provider.removeClaudeKey")
    assert status["configured"] is True and status["source"] == "environment"


def test_a_malformed_key_is_refused_and_never_echoed(tmp_path, network):
    backend = FakeBackend()
    client = _admin(tmp_path, store=SecretStore(backend))
    bad = "sk-ant-api03-this has spaces and is therefore wrong"
    message = client.error("provider.setClaudeKey", key=bad)
    assert message.endswith(BAD_FORMAT_MESSAGE)
    assert bad not in message
    assert backend.items == {}
    assert "params.key" in client.error("provider.setClaudeKey", key=12345)


def test_with_no_secure_store_the_key_is_refused_with_the_environment_advice(tmp_path, network):
    client = _admin(tmp_path, store=SecretStore.unavailable())
    status = client.result("provider.claudeKeyStatus")
    assert status == {"configured": False, "source": "none", "storeAvailable": False}
    assert client.error("provider.setClaudeKey", key=REAL_LOOKING_KEY).endswith(NO_STORE_MESSAGE)


def test_a_store_that_fails_on_write_gives_a_fixed_message(tmp_path, network):
    backend = FakeBackend()
    backend.fail_on = "set"
    client = _admin(tmp_path, store=SecretStore(backend))
    message = client.error("provider.setClaudeKey", key=REAL_LOOKING_KEY)
    assert REAL_LOOKING_KEY not in message
    assert client.result("provider.claudeKeyStatus")["configured"] is False


# --- testing the key --------------------------------------------------------------------------------------------


def test_testing_a_key_makes_one_real_call_and_is_counted_in_the_ledger(tmp_path, network):
    client = _admin(tmp_path, store=SecretStore(FakeBackend()))
    assert client.result("provider.testClaudeKey")["failure"] == "no_key"
    assert network.claude_calls == []

    client.result("provider.setClaudeKey", key=REAL_LOOKING_KEY)
    result = client.result("provider.testClaudeKey")

    assert result["ok"] is True and result["failure"] is None
    assert len(network.claude_calls) == 1
    assert result["allowance"]["requests"] == 1


# --- the key stays out of everything ----------------------------------------------------------------------------


def test_the_key_never_appears_in_a_reply_a_log_line_or_the_audit_log(tmp_path, network, caplog):
    backend = FakeBackend()
    client = _admin(tmp_path, store=SecretStore(backend))
    caplog.set_level(logging.DEBUG)

    replies = [
        client.result("provider.setClaudeKey", key=REAL_LOOKING_KEY),
        client.result("provider.claudeKeyStatus"),
        client.result("provider.status"),
        client.result("provider.testClaudeKey"),
    ]
    backend.fail_on = "get"
    replies.append(client.result("provider.claudeKeyStatus"))

    assert REAL_LOOKING_KEY not in json.dumps(replies)
    assert REAL_LOOKING_KEY not in caplog.text
    for audit_file in (tmp_path / "logs").glob("*"):
        assert REAL_LOOKING_KEY not in audit_file.read_text(encoding="utf-8", errors="replace")
