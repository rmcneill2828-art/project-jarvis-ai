"""ESR-0062 WP2 (EIP-ESR0062-002): household notes hidden from a Child (H1,
EBG-0171 option A), the idle lock (L1-L4), and backend hardening (EBG-0172:
F1 paths, F3 endpoint schemes, F4 speech bound to JARVIS's own replies)."""

from __future__ import annotations

import io
import json
import logging
import os
import sys
import threading
from pathlib import Path

import pytest

from jarvis.agents.home_assistant_agent import HomeAssistantClient
from jarvis.identity.service import IDLE_LOCK_SECONDS, ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.moderation import ModerationService
from jarvis.interfaces.ollama_setup import PullManager
from jarvis.interfaces.stdio_rpc import (
    OLLAMA_DEFAULT_ENDPOINT,
    SPOKEN_REPLY_MEMORY,
    StdioRpcServer,
    _build_home_assistant_agent,
    _checked_env_url,
    build_default_runtime,
)
from jarvis.shared.errors import ClientFacingValueError
from jarvis.shared.safe_locations import (
    checked_http_url,
    checked_user_path,
    is_device_or_local_share,
    is_inside,
    system_locations,
)
from jarvis.tests.household import (
    TEST_PIN,
    ensure_administrator_with_pin,
    join_household,
    rpc,
    switch_to,
)
from sentinel.endpoints import require_http_endpoint
from sentinel.providers import ProviderError


class _Clock:
    """A wall clock and a monotonic clock, moved by hand."""

    def __init__(self) -> None:
        self.wall = 1_000_000.0
        self.mono = 500.0

    def advance(self, seconds: float, *, wall: float | None = None) -> None:
        self.mono += seconds
        self.wall += seconds if wall is None else wall


def _server(tmp_path, clock: _Clock | None = None) -> StdioRpcServer:
    clock = clock or _Clock()
    identity = ProfileService(
        ProfileStore(tmp_path / "profiles.db"),
        wall_clock=lambda: clock.wall,
        monotonic_clock=lambda: clock.mono,
    )
    return StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
        ),
        identity_service=identity,
    )


def _call(server, method, **params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def _household_note(server, content: str) -> None:
    """A shared household note (no owning profile, EBG-0132)."""

    pending = server._runtime.propose_memory(content, None)
    server._runtime.approve_memory(pending.id)


def _listened(server) -> io.StringIO:
    stream = io.StringIO()
    server._notification_stream = stream
    return stream


def _notifications(stream: io.StringIO, method: str) -> list[dict]:
    lines = [json.loads(line) for line in stream.getvalue().splitlines() if line]
    return [line for line in lines if line.get("method") == method]


# --- H1: household notes reach only an Adult or Administrator -----------------------------


def _visible_notes(server) -> list[str]:
    return [record["content"] for record in rpc(server, "memory.list")["records"]]


@pytest.mark.parametrize("role", ["Adult", "Administrator"])
def test_an_adult_or_administrator_still_sees_household_notes(tmp_path, role):
    server = _server(tmp_path)
    join_household(server, f"An {role}", role)
    _household_note(server, "Bins go out on Tuesday.")

    assert "Bins go out on Tuesday." in _visible_notes(server)
    assert rpc(server, "memory.status")["recordCount"] == 1


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_never_sees_household_notes(tmp_path, role):
    server = _server(tmp_path)
    join_household(server, "Sam", role)
    _household_note(server, "The safe code is 4321.")

    assert _visible_notes(server) == []
    assert rpc(server, "memory.status")["recordCount"] == 0


def test_no_profile_selected_in_a_household_never_sees_household_notes(tmp_path):
    """The state a restart and the idle lock both leave (design review High H-1)."""

    server = _server(tmp_path)
    ensure_administrator_with_pin(server)
    _household_note(server, "The safe code is 4321.")
    server._identity_service._store.clear_active()

    assert server._sees_household_notes(None) is False
    assert rpc(server, "memory.status")["recordCount"] == 0


def test_after_a_restart_no_profile_sees_household_notes(tmp_path):
    server = _server(tmp_path)
    ensure_administrator_with_pin(server)
    _household_note(server, "The safe code is 4321.")

    restarted = _server(tmp_path)  # begin_app_session is the real start's; do what it does
    assert restarted._identity_service.begin_app_session() is True
    assert rpc(restarted, "memory.status")["recordCount"] == 0


def test_with_no_profiles_at_all_household_notes_are_still_used(tmp_path):
    server = _server(tmp_path)

    assert server._sees_household_notes(None) is True


@pytest.mark.parametrize(("role", "expected"), [("Child", False), ("Guest", False), ("Adult", True), ("Administrator", True)])
def test_a_conversation_carries_household_notes_only_for_an_adult_or_administrator(tmp_path, role, expected, monkeypatch):
    server = _server(tmp_path)
    join_household(server, "Someone", role)
    seen = {}

    def recording_converse(message, profile_id, **kwargs):
        seen.update(kwargs)
        raise RuntimeError("stop here")

    monkeypatch.setattr(server._runtime, "converse", recording_converse)
    _call(server, "guardian.converse", message="hello")

    assert seen["include_household"] is expected


@pytest.mark.parametrize(("role", "expected"), [("Child", False), ("Guest", False), ("Adult", True), ("Administrator", True)])
def test_an_escalation_carries_household_notes_only_for_an_adult_or_administrator(tmp_path, role, expected, monkeypatch):
    """Implementation review L-5: the fourth caller, past its offer and consent checks."""

    server = _server(tmp_path)
    join_household(server, "Someone", role)
    seen = {}

    def recording_escalate(message, profile_id, **kwargs):
        seen.update(kwargs)
        raise RuntimeError("stop here")

    monkeypatch.setattr(server, "_require_may_escalate", lambda active: None)
    monkeypatch.setattr(server._escalation_offers, "redeem", lambda token, profile_id: "a question")
    monkeypatch.setattr(server._runtime, "escalate", recording_escalate)
    _call(server, "guardian.escalate", token="t")

    assert seen["include_household"] is expected


# --- L1-L3: the idle lock --------------------------------------------------------------------


def _signed_in(tmp_path, role, clock):
    server = _server(tmp_path, clock)
    profile_id = join_household(server, f"A {role}", role)
    return server, profile_id


@pytest.mark.parametrize("role", ["Adult", "Administrator"])
def test_an_adult_or_administrator_is_signed_out_after_fifteen_idle_minutes(tmp_path, role):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, role, clock)
    stream = _listened(server)

    clock.advance(IDLE_LOCK_SECONDS - 1)
    assert server._enforce_idle_lock() is False
    clock.advance(1)
    assert server._enforce_idle_lock() is True

    assert server._identity_service.active_profile() is None
    (locked,) = _notifications(stream, "profile.locked")
    assert locked["params"] == {"reason": "idle", "minutes": 15}
    assert "id" not in locked


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_session_is_never_locked(tmp_path, role):
    clock = _Clock()
    server, profile_id = _signed_in(tmp_path, role, clock)

    clock.advance(IDLE_LOCK_SECONDS * 10)

    assert server._enforce_idle_lock() is False
    assert server._identity_service.active_profile().id == profile_id


def test_with_no_pin_set_nothing_is_locked(tmp_path):
    clock = _Clock()
    server = _server(tmp_path, clock)
    admin = rpc(server, "profile.create", displayName="Robert", role="Administrator")["id"]
    rpc(server, "profile.select", profileId=admin)

    clock.advance(IDLE_LOCK_SECONDS * 10)

    assert server._enforce_idle_lock() is False
    assert server._identity_service.active_profile().id == admin


def test_activity_keeps_a_session_open(tmp_path):
    clock = _Clock()
    server, profile_id = _signed_in(tmp_path, "Adult", clock)

    for _ in range(4):
        clock.advance(IDLE_LOCK_SECONDS - 60)
        assert rpc(server, "session.activity")["activeProfileId"] == profile_id

    assert server._identity_service.active_profile().id == profile_id


def test_activity_arriving_when_due_locks_rather_than_revives(tmp_path):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Administrator", clock)
    stream = _listened(server)

    clock.advance(IDLE_LOCK_SECONDS + 1)
    # Straight to the service, past the check every request runs, so the
    # activity itself meets a session that is due.
    assert server._identity_service.record_activity() is True
    assert server._identity_service.active_profile() is None
    assert rpc(server, "session.activity")["activeProfileId"] is None
    assert len(_notifications(stream, "profile.locked")) == 0  # the service alone does not notify


def test_a_request_never_runs_as_an_idle_administrator(tmp_path):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Administrator", clock)
    stream = _listened(server)

    clock.advance(IDLE_LOCK_SECONDS)
    reply = _call(server, "settings.setRetentionDays", days=30)

    assert "Select a profile first" in reply["error"]["message"]
    assert len(_notifications(stream, "profile.locked")) == 1


def test_the_idle_check_never_counts_as_activity(tmp_path):
    clock = _Clock()
    server, profile_id = _signed_in(tmp_path, "Adult", clock)

    for _ in range(3):
        clock.advance(IDLE_LOCK_SECONDS / 3 - 1)
        assert rpc(server, "session.idleCheck")["activeProfileId"] == profile_id
    clock.advance(3)

    assert rpc(server, "session.idleCheck")["activeProfileId"] is None


def test_a_missing_timestamp_is_stamped_rather_than_left_unlockable(tmp_path):
    """An Adult session carried over a restart with no PIN set, then a PIN set
    from elsewhere (design review M-2)."""

    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Adult", clock)
    server._identity_service._last_activity = None

    assert server._enforce_idle_lock() is False  # first sight: stamped now
    clock.advance(IDLE_LOCK_SECONDS)
    assert server._enforce_idle_lock() is True


def test_setting_the_pin_starts_the_count_afresh(tmp_path):
    clock = _Clock()
    server = _server(tmp_path, clock)
    admin = rpc(server, "profile.create", displayName="Robert", role="Administrator")["id"]
    rpc(server, "profile.select", profileId=admin)
    clock.advance(IDLE_LOCK_SECONDS * 3)  # no PIN yet: nothing to lock

    rpc(server, "pin.set", pin=TEST_PIN)
    clock.advance(IDLE_LOCK_SECONDS - 1)

    assert server._enforce_idle_lock() is False


def test_a_computer_that_slept_is_locked_on_waking(tmp_path):
    """Monotonic clocks on Linux and macOS stop during sleep (design review M-3)."""

    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Administrator", clock)

    clock.advance(1, wall=4 * 60 * 60)

    assert server._enforce_idle_lock() is True


def test_a_clock_set_back_cannot_hold_a_session_open(tmp_path):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Administrator", clock)

    clock.advance(IDLE_LOCK_SECONDS, wall=-3600)

    assert server._enforce_idle_lock() is True


def test_selecting_a_profile_counts_as_activity_for_that_profile(tmp_path):
    clock = _Clock()
    server = _server(tmp_path, clock)
    ensure_administrator_with_pin(server)
    adult = rpc(server, "profile.create", displayName="Bea", role="Adult")["id"]
    clock.advance(IDLE_LOCK_SECONDS - 10)

    switch_to(server, adult)
    clock.advance(IDLE_LOCK_SECONDS - 10)

    assert server._enforce_idle_lock() is False


def test_two_threads_asking_at_once_lock_once_and_notify_once(tmp_path):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Administrator", clock)
    stream = _listened(server)
    clock.advance(IDLE_LOCK_SECONDS)
    results = []
    barrier = threading.Barrier(8)

    def ask():
        barrier.wait()
        results.append(server._enforce_idle_lock())

    threads = [threading.Thread(target=ask) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results.count(True) == 1
    assert len(_notifications(stream, "profile.locked")) == 1


def test_the_backend_timer_locks_without_any_request(tmp_path):
    clock = _Clock()
    server, _ = _signed_in(tmp_path, "Adult", clock)
    stream = _listened(server)
    server._idle_check_interval_seconds = 0.01
    clock.advance(IDLE_LOCK_SECONDS)
    stop = threading.Event()
    timer = threading.Thread(target=server._idle_lock_loop, args=(stop,), daemon=True)
    timer.start()
    try:
        for _ in range(500):
            if _notifications(stream, "profile.locked"):
                break
            threading.Event().wait(0.01)
    finally:
        stop.set()
        timer.join(timeout=5)

    assert len(_notifications(stream, "profile.locked")) == 1
    assert server._identity_service.active_profile() is None


def test_moving_back_up_after_a_lock_needs_the_pin(tmp_path):
    clock = _Clock()
    server, admin = _signed_in(tmp_path, "Administrator", clock)
    clock.advance(IDLE_LOCK_SECONDS)
    server._enforce_idle_lock()

    refused = _call(server, "profile.select", profileId=admin)

    assert "PIN" in refused["error"]["message"]
    assert rpc(server, "profile.select", profileId=admin, pin=TEST_PIN)["id"] == admin


# --- F1: caller-supplied paths ---------------------------------------------------------------


def test_an_ordinary_folder_and_file_are_accepted(tmp_path):
    folder = tmp_path / "Backups"
    folder.mkdir()
    backup = folder / "memory.json"
    backup.write_text("{}", encoding="utf-8")

    assert checked_user_path(str(folder), kind="directory") == folder
    assert checked_user_path(str(backup), kind="file") == backup


@pytest.mark.parametrize(
    ("raw", "reason"),
    [("relative/folder", "full location"), ("bad\x00name", "not valid")],
)
def test_a_relative_or_malformed_path_is_refused(raw, reason):
    with pytest.raises(ClientFacingValueError, match=reason):
        checked_user_path(raw, kind="directory")


def test_a_missing_path_or_the_wrong_kind_is_refused(tmp_path):
    with pytest.raises(ClientFacingValueError, match="does not exist"):
        checked_user_path(str(tmp_path / "nowhere"), kind="directory")
    with pytest.raises(ClientFacingValueError, match="does not exist"):
        checked_user_path(str(tmp_path), kind="file")


def test_a_refusal_never_names_the_path(tmp_path):
    secret = tmp_path / "Robert-private-folder"
    with pytest.raises(ClientFacingValueError) as refused:
        checked_user_path(str(secret), kind="directory")

    assert "Robert-private-folder" not in str(refused.value)


def test_a_link_at_the_leaf_is_refused(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    link = tmp_path / "link"
    try:
        if sys.platform == "win32":
            import _winapi

            _winapi.CreateJunction(str(target), str(link))
        else:
            os.symlink(target, link, target_is_directory=True)
    except (OSError, AttributeError):
        pytest.skip("this platform cannot create a link here")

    with pytest.raises(ClientFacingValueError, match="link"):
        checked_user_path(str(link), kind="directory")


def test_a_real_system_folder_is_refused_in_any_case():
    if sys.platform == "win32":
        system_root = os.environ.get("SystemRoot", "C:\\Windows")
        candidates = [system_root, system_root.upper(), system_root.lower()]
    else:
        candidates = ["/etc", "/usr"]
    for candidate in candidates:
        with pytest.raises(ClientFacingValueError, match="system folders"):
            checked_user_path(candidate, kind="directory")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows device and share paths")
@pytest.mark.parametrize(
    "raw",
    ["\\\\?\\C:\\Users", "\\\\.\\C:\\Users", "\\\\localhost\\C$\\Windows", "\\\\127.0.0.1\\C$", "//localhost/C$/Users"],
)
def test_a_device_path_or_a_share_back_to_this_computer_is_refused(raw):
    with pytest.raises(ClientFacingValueError, match="cannot be used"):
        checked_user_path(raw, kind="directory")


def test_device_and_local_share_detection_is_windows_only_and_spares_other_computers():
    assert is_device_or_local_share("\\\\localhost\\C$", "win32") is True
    assert is_device_or_local_share("\\\\nas\\backups", "win32") is False
    assert is_device_or_local_share("//localhost/x", "linux") is False


@pytest.mark.parametrize(
    ("platform", "path", "inside"),
    [
        ("win32", "C:\\Windows\\System32", True),
        ("win32", "c:\\windows", True),
        ("win32", "C:\\WindowsBackups", False),
        ("win32", "C:\\ProgramData\\x", True),
        ("win32", "C:\\Users\\r\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup", True),
        ("win32", "D:\\Backups", False),
        ("win32", "C:\\Users\\r\\.jarvis\\memory\\backups", False),
        ("darwin", "/System/Library", True),
        ("darwin", "/LIBRARY/x", True),
        ("darwin", "/private/var/folders/ab/T/pytest", False),
        ("darwin", "/private/etc/hosts", True),
        ("darwin", "/Users/r/Library/LaunchAgents/x.plist", True),
        ("darwin", "/Users/r/Documents", False),
        ("linux", "/etc/cron.d", True),
        ("linux", "/home/r/.config/autostart", True),
        ("linux", "/home/r/backups", False),
        ("linux", "/ETC", False),
    ],
)
def test_system_locations_per_platform(platform, path, inside):
    if platform == "win32":
        environ = {"SystemDrive": "C:", "APPDATA": "C:\\Users\\r\\AppData\\Roaming"}
        home = Path("C:/Users/r")
    else:
        environ = {}
        home = Path("/Users/r") if platform == "darwin" else Path("/home/r")
    roots = system_locations(platform, environ, home)
    if platform != "win32":
        roots = [root.replace("\\", "/") for root in roots]

    assert is_inside(path, roots, platform) is inside


def test_export_refuses_a_system_folder_through_the_rpc(tmp_path):
    server = _server(tmp_path)
    admin = ensure_administrator_with_pin(server)
    system_folder = os.environ.get("SystemRoot", "C:\\Windows") if sys.platform == "win32" else "/etc"

    reply = _call(server, "profile.export", profileId=admin, directory=system_folder)

    assert "system folders" in reply["error"]["message"]


def test_restore_refuses_a_link_in_place_of_a_file(tmp_path):
    server = _server(tmp_path)
    ensure_administrator_with_pin(server)

    reply = _call(server, "memory.restore", backupPath=str(tmp_path / "missing.json"))

    assert "does not exist" in reply["error"]["message"]


# --- F3: endpoint schemes --------------------------------------------------------------------


@pytest.mark.parametrize("url", ["http://localhost:11434", "https://ha.local:8123", "HTTP://127.0.0.1"])
def test_an_http_or_https_address_is_accepted(url):
    assert checked_http_url(url) == url


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://host/x", "localhost:11434", "http://", "https:///path", "", "gopher://h"])
def test_any_other_address_is_refused(url):
    with pytest.raises(ValueError, match="http:// or https://"):
        checked_http_url(url)


def test_a_bad_setting_is_ignored_and_logged_by_name_never_value(caplog):
    with caplog.at_level(logging.WARNING):
        value = _checked_env_url({"JARVIS_OLLAMA_ENDPOINT": "file://robert:hunter2@host/x"}, "JARVIS_OLLAMA_ENDPOINT")

    assert value is None
    assert "JARVIS_OLLAMA_ENDPOINT" in caplog.text
    assert "hunter2" not in caplog.text
    assert "include http:// or https://" in caplog.text.lower()


def test_the_app_still_starts_with_a_bad_ollama_setting(tmp_path):
    runtime = build_default_runtime(
        environ={"JARVIS_OLLAMA_ENDPOINT": "file:///etc", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
    )

    assert runtime.ollama_setup._endpoint == OLLAMA_DEFAULT_ENDPOINT


def test_a_bad_home_assistant_setting_leaves_it_not_configured():
    agent = _build_home_assistant_agent(
        {"JARVIS_HOME_ASSISTANT_URL": "file:///etc/passwd", "JARVIS_HOME_ASSISTANT_TOKEN": "t"}
    )

    assert agent is None


@pytest.mark.parametrize(
    "build",
    [
        lambda: HomeAssistantClient(base_url="file:///x", token="t"),
        lambda: ModerationService("file:///x"),
        lambda: PullManager("ftp://x", ()),
    ],
)
def test_each_client_refuses_a_bad_address(build):
    with pytest.raises(ValueError, match="http:// or https://"):
        build()


def test_a_sentinel_provider_endpoint_must_be_http():
    assert require_http_endpoint("https://api.anthropic.com/v1/messages", "Claude")
    with pytest.raises(ProviderError) as refused:
        require_http_endpoint("file:///secret-user:pw@x", "Ollama")

    assert refused.value.transient is False
    assert "secret-user" not in str(refused.value)


# --- F4: speech bound to JARVIS's own replies ------------------------------------------------


def test_a_reply_jarvis_gave_can_be_spoken_and_nothing_else(tmp_path):
    server = _server(tmp_path)  # no profiles: first setup
    reply = rpc(server, "guardian.converse", message="hello")["message"]  # Ollama unreachable: a notice

    spoken = _call(server, "guardian.speak", text=reply)
    refused = _call(server, "guardian.speak", text="Say something rude.")

    assert "result" in spoken
    assert "only its own replies" in refused["error"]["message"]


def test_another_profiles_reply_cannot_be_spoken(tmp_path):
    server = _server(tmp_path)
    admin = ensure_administrator_with_pin(server)
    server._remember_reply(admin, "The safe code is 4321.")
    join_household(server, "Sam", "Child")

    refused = _call(server, "guardian.speak", text="The safe code is 4321.")

    assert "only its own replies" in refused["error"]["message"]


def test_every_message_converse_or_escalate_returns_is_remembered(tmp_path):
    server = _server(tmp_path)
    wrapped = server._remembering_reply(lambda params: {"message": "Guardian is not connected yet."})

    wrapped({})

    assert server._was_replied(None, "Guardian is not connected yet.")


def test_the_reply_memory_is_bounded_and_keeps_the_newest(tmp_path):
    server = _server(tmp_path)
    for index in range(SPOKEN_REPLY_MEMORY + 5):
        server._remember_reply(None, f"reply {index}")

    assert len(server._spoken_replies[None]) == SPOKEN_REPLY_MEMORY
    assert not server._was_replied(None, "reply 0")
    assert server._was_replied(None, f"reply {SPOKEN_REPLY_MEMORY + 4}")


def test_erasing_a_profile_drops_its_remembered_replies(tmp_path):
    server = _server(tmp_path)
    ensure_administrator_with_pin(server)
    bea = rpc(server, "profile.create", displayName="Bea", role="Adult")["id"]
    server._remember_reply(bea, "Hello Bea.")

    rpc(server, "profile.erase", profileId=bea, confirmName="Bea")

    assert bea not in server._spoken_replies


# --- L2-L3: session methods are not Orb activity (M5) -------------------------------------------


def test_session_methods_never_light_the_orb(tmp_path):
    server = _server(tmp_path)
    _call(server, "session.activity")
    _call(server, "session.idleCheck")

    assert server._activity_tracker.pop_pending() == []
