"""ESR-0061 WP6a: the Administrator PIN and the elevation rule (EIP-ESR0061-006
P1-P5, Sections 6.1-6.2)."""

from __future__ import annotations

import itertools
import json
import logging
import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from jarvis.identity.admin_pin import (
    MAX_LOCK_SECONDS,
    AdminPin,
    lock_seconds_for,
)
from jarvis.identity.service import ProfileService, pin_required_to_switch
from jarvis.identity.store import HOUSEHOLD_ROLES, ProfileRecord, ProfileStore
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.tests.household import TEST_PIN, ensure_administrator_with_pin, rpc
from jarvis.tools import reset_admin_pin

PIN = "135790"
OTHER_PIN = "864200"
WRONG = "PIN is not right"
# A try refused unchecked during a lock-out, as distinct from the wrong try that starts one.
LOCKED = r"^Too many wrong tries\."


class Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += timedelta(seconds=seconds)


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "profiles.db"


def _service(db_path, clock):
    store = ProfileStore(db_path)
    return ProfileService(store, AdminPin(store, clock))


def _household(db_path, clock):
    """An Administrator (signed in, PIN set), an Adult, a Child and a Guest."""

    service = _service(db_path, clock)
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    service.set_first_pin(PIN)
    members = {"Administrator": admin}
    for role in ("Adult", "Child", "Guest"):
        members[role] = service.create_profile(role, role)
    return service, members


def _wrong(pin_store, times):
    for _ in range(times):
        with pytest.raises(PermissionError, match=WRONG):
            pin_store.verify(OTHER_PIN)


# --- The PIN's shape and storage (P1) ------------------------------------------------------------------------------


@pytest.mark.parametrize("pin", ["12345", "1234567890123", "12a456", "", " 123456", "123456 ", "١٢٣٤٥٦", None, 123456])
def test_a_pin_must_be_six_to_twelve_ascii_digits(db_path, clock, pin):
    service, _ = _household(db_path, clock)
    with pytest.raises(ValueError, match="6 to 12 digits") as refusal:
        service.change_pin(PIN, pin)
    assert str(pin) not in str(refusal.value) or pin in ("", None)


@pytest.mark.parametrize("pin", ["123456", "123456789012"])
def test_six_and_twelve_digits_are_accepted(db_path, clock, pin):
    service, _ = _household(db_path, clock)
    service.change_pin(PIN, pin)
    service.pin.verify(pin)


def test_only_a_salted_scrypt_hash_is_stored_never_the_pin(db_path, clock):
    _household(db_path, clock)
    with sqlite3.connect(db_path) as connection:
        row = connection.execute("SELECT salt, pin_hash, scrypt_n, scrypt_r, scrypt_p FROM admin_pin").fetchone()
        dump = "\n".join(connection.iterdump())
    salt, digest, n, r, p = row
    assert len(salt) == 16 and len(digest) == 32
    assert (n, r, p) == (2**14, 8, 1)
    assert PIN not in dump
    assert PIN.encode() not in db_path.read_bytes()


def test_two_households_with_the_same_pin_store_different_hashes(tmp_path, clock):
    _household(tmp_path / "a.db", clock)
    _household(tmp_path / "b.db", clock)
    hashes = []
    for path in (tmp_path / "a.db", tmp_path / "b.db"):
        with sqlite3.connect(path) as connection:
            hashes.append(connection.execute("SELECT pin_hash FROM admin_pin").fetchone()[0])
    assert hashes[0] != hashes[1]


def test_the_first_pin_cannot_be_set_twice(db_path, clock):
    service, _ = _household(db_path, clock)
    with pytest.raises(ValueError, match="already set"):
        service.set_first_pin(OTHER_PIN)
    service.pin.verify(PIN)


# --- Rate limiting (P1) ----------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("tries", "seconds"),
    [(1, 0), (4, 0), (5, 30), (6, 0), (10, 60), (15, 120), (20, 240), (25, 480), (30, 600), (35, 600), (100, 600)],
)
def test_the_lock_out_starts_at_five_tries_and_doubles_to_ten_minutes(tries, seconds):
    assert lock_seconds_for(tries) == seconds


def test_five_wrong_tries_lock_the_pin_for_thirty_seconds_and_a_right_pin_is_then_refused(db_path, clock):
    service, _ = _household(db_path, clock)
    _wrong(service.pin, 4)
    with pytest.raises(PermissionError, match=WRONG) as fifth:
        service.pin.verify(OTHER_PIN)
    assert fifth.value.locked_for_seconds == 30
    assert "30 seconds" in str(fifth.value)

    with pytest.raises(PermissionError, match=r"^Too many wrong tries\. Try again in 30 seconds"):
        service.pin.verify(PIN)
    assert service.pin.status().to_payload() == {"set": True, "locked": True, "lockedForSeconds": 30}

    clock.advance(29)
    with pytest.raises(PermissionError, match=r"^Too many wrong tries\. Try again in 1 seconds"):
        service.pin.verify(PIN)
    clock.advance(1)
    service.pin.verify(PIN)
    assert service.pin.status().to_payload() == {"set": True, "locked": False, "lockedForSeconds": 0}


def test_tries_during_a_lock_out_are_not_checked_or_counted(db_path, clock):
    service, _ = _household(db_path, clock)
    _wrong(service.pin, 5)
    for _ in range(20):
        with pytest.raises(PermissionError, match=LOCKED):
            service.pin.verify(OTHER_PIN)
    clock.advance(30)
    # Still the sixth counted try, so no new lock-out yet.
    with pytest.raises(PermissionError, match=WRONG) as sixth:
        service.pin.verify(OTHER_PIN)
    assert sixth.value.locked_for_seconds == 0


def test_the_second_batch_locks_for_sixty_seconds_and_a_right_pin_resets_the_count(db_path, clock):
    service, _ = _household(db_path, clock)
    _wrong(service.pin, 5)
    clock.advance(30)
    _wrong(service.pin, 4)
    with pytest.raises(PermissionError, match=WRONG) as tenth:
        service.pin.verify(OTHER_PIN)
    assert tenth.value.locked_for_seconds == 60
    clock.advance(60)
    service.pin.verify(PIN)
    _wrong(service.pin, 4)
    with pytest.raises(PermissionError, match=WRONG) as fifth_again:
        service.pin.verify(OTHER_PIN)
    assert fifth_again.value.locked_for_seconds == 30


def test_the_lock_out_never_exceeds_ten_minutes(db_path, clock):
    service, _ = _household(db_path, clock)
    for _ in range(12):
        _wrong(service.pin, 4)
        with pytest.raises(PermissionError, match=WRONG) as batch_end:
            service.pin.verify(OTHER_PIN)
        assert batch_end.value.locked_for_seconds <= MAX_LOCK_SECONDS
        clock.advance(MAX_LOCK_SECONDS)
    assert batch_end.value.locked_for_seconds == MAX_LOCK_SECONDS


def test_a_restart_does_not_reset_the_lock_out(db_path, clock):
    service, _ = _household(db_path, clock)
    _wrong(service.pin, 5)

    restarted = _service(db_path, clock)
    with pytest.raises(PermissionError, match=LOCKED):
        restarted.pin.verify(PIN)
    assert restarted.pin.status().locked_for_seconds == 30


def test_switching_profile_does_not_reset_the_lock_out(db_path, clock):
    service, members = _household(db_path, clock)
    service.select_profile(members["Child"].id)
    for _ in range(5):
        with pytest.raises(PermissionError, match=WRONG):
            service.select_profile(members["Adult"].id, OTHER_PIN)
    service.select_profile(members["Guest"].id)  # Child to Guest: free
    with pytest.raises(PermissionError, match=LOCKED):
        service.select_profile(members["Administrator"].id, PIN)
    assert service.active_profile().id == members["Guest"].id


# --- The elevation rule (P2) -----------------------------------------------------------------------------------------

EXPECTED_PIN_REQUIRED = {
    # (from, to): needs the PIN
    ("Administrator", "Administrator"): False,
    ("Administrator", "Adult"): False,
    ("Administrator", "Child"): False,
    ("Administrator", "Guest"): False,
    ("Adult", "Administrator"): True,
    ("Adult", "Adult"): False,
    ("Adult", "Child"): False,
    ("Adult", "Guest"): False,
    ("Child", "Administrator"): True,
    ("Child", "Adult"): True,
    ("Child", "Child"): False,
    ("Child", "Guest"): False,
    ("Guest", "Administrator"): True,
    ("Guest", "Adult"): True,
    ("Guest", "Child"): False,
    ("Guest", "Guest"): False,
}


def _record(role, profile_id=None):
    return ProfileRecord(id=profile_id or f"id-{role}", display_name=role, role=role, created_at=datetime.now(UTC))


@pytest.mark.parametrize(("source", "target"), list(itertools.product(HOUSEHOLD_ROLES, repeat=2)))
def test_the_elevation_rule_for_every_pair_of_roles(source, target):
    needed = pin_required_to_switch(_record(source, "a"), _record(target, "b"))
    assert needed is EXPECTED_PIN_REQUIRED[(source, target)]


@pytest.mark.parametrize("role", HOUSEHOLD_ROLES)
def test_staying_on_the_same_profile_never_needs_the_pin(role):
    record = _record(role)
    assert pin_required_to_switch(record, record) is False


@pytest.mark.parametrize(("target", "needed"), [("Administrator", True), ("Adult", True), ("Child", False), ("Guest", False)])
def test_with_no_profile_signed_in_the_lowest_privilege_applies(target, needed):
    assert pin_required_to_switch(None, _record(target)) is needed


@pytest.mark.parametrize(("source", "target"), [pair for pair, needed in EXPECTED_PIN_REQUIRED.items() if needed])
def test_every_guarded_switch_is_refused_without_the_pin_and_with_a_wrong_one(db_path, clock, source, target):
    service, members = _household(db_path, clock)
    if members[source].role == "Adult" and target == "Adult":
        pytest.skip("same profile")
    service.select_profile(members[source].id, PIN)

    with pytest.raises(PermissionError, match="PIN is needed"):
        service.select_profile(members[target].id)
    with pytest.raises(PermissionError, match=WRONG):
        service.select_profile(members[target].id, OTHER_PIN)
    assert service.active_profile().id == members[source].id

    service.select_profile(members[target].id, PIN)
    assert service.active_profile().id == members[target].id


def test_a_child_cannot_reach_an_unlocked_profile_by_any_route_of_free_switches(db_path, clock):
    service, members = _household(db_path, clock)
    service.select_profile(members["Child"].id)
    reachable = {"Child"}
    frontier = ["Child"]
    while frontier:
        current = frontier.pop()
        service.select_profile(members[current].id, PIN if current not in ("Child", "Guest") else None)
        for role, record in members.items():
            if role in reachable:
                continue
            try:
                service.select_profile(record.id)
            except PermissionError:
                continue
            reachable.add(role)
            frontier.append(role)
            service.select_profile(members[current].id, PIN)
    assert reachable == {"Child", "Guest"}


def test_a_fresh_start_with_profiles_but_none_selected_needs_the_pin_for_an_administrator(db_path, clock):
    service, members = _household(db_path, clock)
    with sqlite3.connect(db_path) as connection:
        connection.execute("DELETE FROM active_profile")
    with pytest.raises(PermissionError, match="PIN is needed"):
        service.select_profile(members["Administrator"].id)
    service.select_profile(members["Child"].id)


def test_a_restart_keeps_the_signed_in_profile(db_path, clock):
    _, members = _household(db_path, clock)
    restarted = _service(db_path, clock)
    assert restarted.active_profile().id == members["Administrator"].id


# --- No PIN yet (P3) -------------------------------------------------------------------------------------------------


def test_with_no_pin_switching_stays_open_as_before(db_path, clock):
    service = _service(db_path, clock)
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    with sqlite3.connect(db_path) as connection:
        # An existing household from before WP6a: profiles, no PIN.
        connection.execute(
            "INSERT INTO profiles (id, display_name, role, created_at) VALUES ('c', 'Sam', 'Child', '2026-01-01T00:00:00+00:00')"
        )
    service.select_profile("c")
    service.select_profile(admin.id)
    assert service.switch_requirements("c")["pinRequired"] is False


def test_with_no_pin_no_profile_can_be_added(db_path, clock):
    service = _service(db_path, clock)
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    with pytest.raises(PermissionError, match="Set an Administrator PIN"):
        service.create_profile("Sam", "Child")


# --- Who may create a profile (P2) -----------------------------------------------------------------------------------


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_the_first_profile_must_be_an_administrator(db_path, clock, role):
    service = _service(db_path, clock)
    with pytest.raises(ValueError, match="first profile must be an Administrator"):
        service.create_profile("Sam", role)
    assert service.list_profiles() == ()


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_add_a_profile(db_path, clock, role):
    service, members = _household(db_path, clock)
    service.select_profile(members[role].id, PIN)
    with pytest.raises(PermissionError, match="Only an Administrator"):
        service.create_profile("Intruder", "Administrator")
    assert len(service.list_profiles()) == 4


def test_an_administrator_with_a_pin_adds_any_role(db_path, clock):
    service, _ = _household(db_path, clock)
    for role in HOUSEHOLD_ROLES:
        assert service.create_profile(f"New {role}", role).role == role


# --- Setting and changing the PIN ------------------------------------------------------------------------------------


@pytest.mark.parametrize("role", ["Adult", "Child", "Guest"])
def test_only_an_administrator_can_set_or_change_the_pin(db_path, clock, role):
    service, members = _household(db_path, clock)
    service.select_profile(members[role].id, PIN)
    with pytest.raises(PermissionError, match="Only an Administrator"):
        service.change_pin(PIN, OTHER_PIN)
    service.pin.verify(PIN)


def test_changing_the_pin_needs_the_current_one_and_counts_a_wrong_one(db_path, clock):
    service, _ = _household(db_path, clock)
    with pytest.raises(PermissionError, match=WRONG):
        service.change_pin(OTHER_PIN, "111111")
    service.change_pin(PIN, OTHER_PIN)
    with pytest.raises(PermissionError, match=WRONG):
        service.pin.verify(PIN)
    service.pin.verify(OTHER_PIN)
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("SELECT wrong_since_signin FROM admin_pin").fetchone()[0] == 2


# --- Notices for the next Administrator sign-in (P1, P3, P5) -----------------------------------------------------------


def test_the_next_administrator_sign_in_is_told_who_set_the_pin_and_about_wrong_tries_once(db_path, clock):
    service, members = _household(db_path, clock)
    service.select_profile(members["Child"].id)
    clock.advance(60)
    for _ in range(3):
        with pytest.raises(PermissionError, match=WRONG):
            service.select_profile(members["Administrator"].id, OTHER_PIN)
    record = service.select_profile(members["Administrator"].id, PIN)

    notices = service.signin_notices(record)
    assert [notice["kind"] for notice in notices] == ["pinSet", "wrongTries"]
    assert notices[0]["byProfile"] == "Robert"
    assert notices[1]["count"] == 3
    assert notices[1]["at"] == clock.now.isoformat()
    assert service.signin_notices(record) == []


def test_notices_are_kept_for_an_administrator_not_given_to_anyone_else(db_path, clock):
    service, members = _household(db_path, clock)
    adult = service.select_profile(members["Adult"].id)
    assert service.signin_notices(adult) == []
    admin = service.select_profile(members["Administrator"].id, PIN)
    assert [notice["kind"] for notice in service.signin_notices(admin)] == ["pinSet"]


def test_the_command_line_reset_removes_the_pin_and_leaves_a_notice(db_path, clock, monkeypatch, capsys):
    service, members = _household(db_path, clock)
    service.signin_notices(service.active_profile())
    service.select_profile(members["Child"].id)
    monkeypatch.setenv("JARVIS_IDENTITY_DB_PATH", str(db_path))

    assert reset_admin_pin.main([]) == 0
    assert "has been removed" in capsys.readouterr().out
    assert service.pin.is_set() is False

    record = service.select_profile(members["Administrator"].id)  # open again: no PIN (P3)
    assert [notice["kind"] for notice in service.signin_notices(record)] == ["pinReset"]

    assert reset_admin_pin.main([]) == 0
    assert "nothing was changed" in capsys.readouterr().out


def test_the_reset_tool_uses_the_backends_identity_database(tmp_path, monkeypatch):
    from jarvis.interfaces import stdio_rpc

    # The test sandbox (conftest.py) has moved the backend's default; the tool follows it.
    assert reset_admin_pin.identity_db_path() == stdio_rpc.DEFAULT_IDENTITY_DB_PATH
    monkeypatch.setenv(stdio_rpc.IDENTITY_DB_PATH_ENV_VAR, str(tmp_path / "elsewhere.db"))
    assert reset_admin_pin.identity_db_path() == tmp_path / "elsewhere.db"


def test_the_reset_tool_creates_nothing_where_there_is_no_database(tmp_path, monkeypatch):
    missing = tmp_path / "none" / "profiles.db"
    monkeypatch.setenv("JARVIS_IDENTITY_DB_PATH", str(missing))
    assert reset_admin_pin.main([]) == 0
    assert not missing.exists()


# --- Through the RPC layer: the PIN is never echoed or logged ---------------------------------------------------------


def _server(tmp_path, monkeypatch):
    del monkeypatch
    runtime = build_default_runtime(
        environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
    )
    return StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))


def _raw(server, method, **params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def test_the_pin_methods_through_rpc_never_echo_the_pin(tmp_path, monkeypatch, caplog):
    caplog.set_level(logging.DEBUG)
    server = _server(tmp_path, monkeypatch)
    secret = "975318642"
    admin = rpc(server, "profile.create", displayName="Robert", role="Administrator")["id"]
    rpc(server, "profile.select", profileId=admin)
    assert rpc(server, "pin.status") == {"set": False, "locked": False, "lockedForSeconds": 0}

    replies = [
        _raw(server, "pin.set", pin="12ab"),
        _raw(server, "pin.set", pin=secret),
        _raw(server, "pin.set", pin=secret),
        _raw(server, "pin.change", currentPin=secret[::-1], newPin=secret),
        _raw(server, "pin.change", currentPin=secret, newPin="12"),
    ]
    child = rpc(server, "profile.create", displayName="Sam", role="Child")["id"]
    rpc(server, "profile.select", profileId=child)
    replies += [
        _raw(server, "profile.switchRequirements", profileId=admin),
        _raw(server, "profile.select", profileId=admin),
        _raw(server, "profile.select", profileId=admin, pin=secret[::-1]),
        _raw(server, "profile.select", profileId=admin, pin=12345678),
        _raw(server, "profile.select", profileId=admin, pin=secret),
    ]
    assert replies[1]["result"]["set"] is True
    assert "already set" in replies[2]["error"]["message"]
    assert replies[3]["error"]["message"] == "PermissionError: That PIN is not right. Try again."
    assert replies[5]["result"] == {"pinRequired": True, "set": True, "locked": False, "lockedForSeconds": 0}
    assert "PIN is needed" in replies[6]["error"]["message"]
    assert "must be a string" in replies[8]["error"]["message"]
    signed_in = replies[9]["result"]
    assert signed_in["id"] == admin
    assert [notice["kind"] for notice in signed_in["pinNotices"]] == ["pinSet", "wrongTries"]
    assert signed_in["pinNotices"][1]["count"] == 2

    everything = json.dumps(replies) + caplog.text
    for log_file in (tmp_path / "logs").glob("*"):
        everything += log_file.read_text(encoding="utf-8", errors="replace")
    assert secret not in everything
    assert secret[::-1] not in everything


def test_a_child_cannot_create_a_profile_or_set_the_pin_through_rpc(tmp_path, monkeypatch):
    server = _server(tmp_path, monkeypatch)
    ensure_administrator_with_pin(server)
    child = rpc(server, "profile.create", displayName="Sam", role="Child")["id"]
    rpc(server, "profile.select", profileId=child)

    assert "Only an Administrator" in _raw(server, "profile.create", displayName="Me", role="Administrator")["error"]["message"]
    assert "Only an Administrator" in _raw(server, "pin.change", currentPin=TEST_PIN, newPin="000000")["error"]["message"]
    assert "Only an Administrator" in _raw(server, "pin.set", pin="000000")["error"]["message"]
    assert len(rpc(server, "profile.list")["profiles"]) == 2


def test_the_lock_out_survives_a_backend_restart_through_rpc(tmp_path, monkeypatch):
    server = _server(tmp_path, monkeypatch)
    admin = ensure_administrator_with_pin(server)
    child = rpc(server, "profile.create", displayName="Sam", role="Child")["id"]
    rpc(server, "profile.select", profileId=child)
    for _ in range(5):
        _raw(server, "profile.select", profileId=admin, pin="000000")

    restarted = _server(tmp_path, monkeypatch)
    status = rpc(restarted, "pin.status")
    assert status["locked"] is True and 0 < status["lockedForSeconds"] <= 30
    assert "Too many wrong tries" in _raw(restarted, "profile.select", profileId=admin, pin=TEST_PIN)["error"]["message"]
    assert rpc(restarted, "profile.active")["profile"]["id"] == child


def test_an_administrator_signed_in_at_startup_gets_the_notices_once_and_no_one_else_does(tmp_path, monkeypatch):
    """WP6a review (Copilot Medium M1): an Administrator whose app starts already
    signed in never switches in, so `pin.takeNotices` hands the notices over."""

    server = _server(tmp_path, monkeypatch)
    admin = ensure_administrator_with_pin(server)
    child = rpc(server, "profile.create", displayName="Sam", role="Child")["id"]
    rpc(server, "profile.select", profileId=child)
    assert "Only an Administrator" in _raw(server, "pin.takeNotices")["error"]["message"]
    for _ in range(2):
        _raw(server, "profile.select", profileId=admin, pin="000000")
    rpc(server, "profile.select", profileId=admin, pin=TEST_PIN)  # takes the notices so far
    reset_admin_pin.reset(tmp_path / "profiles.db")

    restarted = _server(tmp_path, monkeypatch)
    assert rpc(restarted, "profile.active")["profile"]["id"] == admin
    taken = rpc(restarted, "pin.takeNotices")["pinNotices"]
    assert [notice["kind"] for notice in taken] == ["pinReset"]
    assert rpc(restarted, "pin.takeNotices")["pinNotices"] == []

# --- A new start never inherits an Adult or Administrator session (ESR-0061 WP7, review finding F6) -------------------


def _household_db(tmp_path, *, with_pin=True):
    path = tmp_path / "profiles.db"
    service = ProfileService(ProfileStore(path))
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    if with_pin:
        service.set_first_pin(TEST_PIN)
    adult = service.create_profile("Jo", "Adult") if with_pin else None
    child = service.create_profile("Sam", "Child") if with_pin else None
    return path, service, admin, adult, child


def test_an_administrator_session_is_not_carried_over_to_a_new_start(tmp_path):
    path, _service, _admin, _adult, _child = _household_db(tmp_path)
    restarted = ProfileService(ProfileStore(path))
    assert restarted.begin_app_session() is True
    assert restarted.active_profile() is None


def test_an_adult_session_is_not_carried_over_either(tmp_path):
    path, service, _admin, adult, _child = _household_db(tmp_path)
    service.select_profile(adult.id)
    restarted = ProfileService(ProfileStore(path))
    assert restarted.begin_app_session() is True
    assert restarted.active_profile() is None


def test_a_child_session_is_kept_because_it_is_already_the_lowest_level(tmp_path):
    path, service, _admin, _adult, child = _household_db(tmp_path)
    service.select_profile(child.id)
    restarted = ProfileService(ProfileStore(path))
    assert restarted.begin_app_session() is False
    assert restarted.active_profile().id == child.id


def test_with_no_pin_set_the_session_is_kept(tmp_path):
    path, _service, admin, _adult, _child = _household_db(tmp_path, with_pin=False)
    restarted = ProfileService(ProfileStore(path))
    assert restarted.begin_app_session() is False
    assert restarted.active_profile().id == admin.id


def test_the_real_backend_start_clears_an_administrator_session(tmp_path, monkeypatch):
    from jarvis.interfaces import stdio_rpc

    path, _service, admin, _adult, _child = _household_db(tmp_path)
    monkeypatch.setenv(stdio_rpc.IDENTITY_DB_PATH_ENV_VAR, str(path))
    runtime = build_default_runtime(
        environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
    )
    server = StdioRpcServer(runtime)
    response = server.handle_line('{"jsonrpc": "2.0", "id": 1, "method": "profile.active", "params": {}}')
    assert response["result"]["profile"] is None
    # Coming back as the Administrator needs the PIN, as for anyone switching up.
    assert ProfileService(ProfileStore(path)).switch_requirements(admin.id)["pinRequired"] is True
