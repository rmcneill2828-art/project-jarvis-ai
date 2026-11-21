"""The PIN reset and Administrator recovery reachable from the packaged backend
(ESR-0062 WP5): an installed household has no Python to run
`python -m jarvis.tools...`, so the backend executable takes the same two
actions as options, with the same rules."""

import os
import subprocess
import sys
from pathlib import Path

from jarvis.identity.admin_pin import AdminPin
from jarvis.identity.store import ProfileStore

REPO = Path(__file__).resolve().parents[2]
PIN = "135790"


def _entry(db_path, *args):
    env = dict(os.environ, JARVIS_IDENTITY_DB_PATH=str(db_path), PYTHONPATH=str(REPO))
    return subprocess.run(
        [sys.executable, "scripts/jarvis_backend_entry.py", *args],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
        cwd=REPO,
        env=env,
    )


def _roles(db_path):
    return [record.role for record in ProfileStore(db_path).list_all()]


def test_reset_admin_pin_removes_the_pin_and_leaves_a_notice(tmp_path):
    db_path = tmp_path / "profiles.db"
    AdminPin(ProfileStore(db_path)).set_first(PIN, "Robert")

    result = _entry(db_path, "--reset-admin-pin")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "has been removed" in result.stdout
    pin = AdminPin(ProfileStore(db_path))
    assert pin.is_set() is False
    assert "pinReset" in [notice["kind"] for notice in pin.take_notices()]


def test_reset_admin_pin_with_no_pin_changes_nothing(tmp_path):
    result = _entry(tmp_path / "none" / "profiles.db", "--reset-admin-pin")

    assert result.returncode == 0
    assert "nothing was changed" in result.stdout
    assert not (tmp_path / "none").exists()


def test_add_administrator_adds_one_only_when_there_is_none(tmp_path):
    db_path = tmp_path / "profiles.db"
    ProfileStore(db_path)  # a household from before Administrators, with no profiles yet

    first = _entry(db_path, "--add-administrator", "Robert")
    second = _entry(db_path, "--add-administrator", "Someone Else")

    assert first.returncode == 0, first.stdout + first.stderr
    assert "Added Robert" in first.stdout
    assert second.returncode == 1
    assert "already has an Administrator" in second.stdout
    assert _roles(db_path) == ["Administrator"]


def test_a_mistyped_recovery_command_explains_itself_and_changes_nothing(tmp_path):
    db_path = tmp_path / "profiles.db"
    AdminPin(ProfileStore(db_path)).set_first(PIN, "Robert")

    for args in (["--add-administrator"], ["--reset-admin-pin", "extra"], ["--add-administrator", "A", "B"]):
        result = _entry(db_path, *args)

        assert result.returncode == 2, args
        assert "Usage" in result.stdout and "Nothing was changed" in result.stdout
    assert AdminPin(ProfileStore(db_path)).is_set() is True
    assert _roles(db_path) == []
