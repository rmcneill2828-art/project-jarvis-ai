"""Test-wide safety guards.

EBG-0147 (ESR-0059 WP12) finding: several tests constructed the RPC server
or runtime without an explicit store path, so they opened the Programme
Sponsor's real `~/.jarvis/memory/personal.db` and
`~/.jarvis/identity/profiles.db` - found by running the suite against a
fake home directory. From WP12, opening a store also records its schema
version, so such a test would write to the real files, not just read them.

This fixture points every home-directory default the backend uses at the
test's own temporary directory, so no test - present or future - can touch
real user data by omission. Tests that pass explicit paths are unaffected.
"""

import pytest

from jarvis.interfaces import stdio_rpc


@pytest.fixture(autouse=True)
def _never_touch_the_real_home_directory(tmp_path, monkeypatch):
    sandbox = tmp_path / "home-sandbox" / ".jarvis"
    monkeypatch.setattr(stdio_rpc, "DEFAULT_MEMORY_DB_PATH", sandbox / "memory" / "personal.db")
    monkeypatch.setattr(stdio_rpc, "DEFAULT_MEMORY_BACKUP_DIR", sandbox / "memory" / "backups")
    monkeypatch.setattr(stdio_rpc, "DEFAULT_IDENTITY_DB_PATH", sandbox / "identity" / "profiles.db")
    for name in ("JARVIS_MEMORY_DB_PATH", "JARVIS_IDENTITY_DB_PATH", "JARVIS_MEMORY_BACKUP_DIR", "JARVIS_LOG_DIR"):
        monkeypatch.delenv(name, raising=False)
