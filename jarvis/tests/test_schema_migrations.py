"""Tests for EBG-0147 (ESR-0059 WP12): schema versioning for the local
SQLite stores."""

import sqlite3

import pytest

from jarvis.identity.store import PROFILE_MIGRATIONS, ProfileStore
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PERSONAL_MEMORY_MIGRATIONS, PersonalMemoryStore
from jarvis.shared.schema_migrations import SchemaVersionError, apply_migrations, schema_version
from sentinel.core import SentinelTrustGateway


def test_a_new_memory_store_is_created_at_the_latest_version(tmp_path):
    PersonalMemoryStore(tmp_path / "m.db")

    assert schema_version(tmp_path / "m.db") == len(PERSONAL_MEMORY_MIGRATIONS) == 2


def test_a_new_profile_store_is_created_at_the_latest_version(tmp_path):
    ProfileStore(tmp_path / "p.db")

    assert schema_version(tmp_path / "p.db") == len(PROFILE_MIGRATIONS) == 1


def _legacy_memory_db(path) -> None:
    """A database exactly as a pre-versioning JARVIS left it: the ESR-0027
    tables, data in them, user_version 0."""

    connection = sqlite3.connect(path)
    with connection:
        for statement in PERSONAL_MEMORY_MIGRATIONS[0]:
            connection.execute(statement)
        connection.execute(
            "INSERT INTO consent_decisions VALUES ('d1','memory_retention','approved','2026-09-01T00:00:00+00:00','local-user','Review',NULL,'r')"
        )
        connection.execute(
            "INSERT INTO personal_memory VALUES ('m1','Robert prefers dark mode.','2026-09-01T00:00:00+00:00','d1')"
        )
    connection.close()


def test_an_existing_unversioned_database_is_upgraded_without_losing_data(tmp_path):
    path = tmp_path / "m.db"
    _legacy_memory_db(path)
    assert schema_version(path) == 0

    store = PersonalMemoryStore(path)

    assert schema_version(path) == 2
    assert [r.content for r in store.list_all()] == ["Robert prefers dark mode."]
    assert store.get_decision("d1").decision == "approved"
    # EBG-0132: a pre-existing memory becomes a shared household note,
    # visible to every profile.
    assert store.list_all()[0].profile_id is None
    assert [r.content for r in store.list_visible("any-profile")] == ["Robert prefers dark mode."]


def test_reopening_a_current_database_changes_nothing(tmp_path):
    path = tmp_path / "m.db"
    service = PersonalMemoryService(gateway=SentinelTrustGateway(), store=PersonalMemoryStore(path))
    service.approve(service.propose("Tea, no sugar.").id)

    reopened = PersonalMemoryStore(path)

    assert schema_version(path) == 2
    assert [r.content for r in reopened.list_all()] == ["Tea, no sugar."]


def test_a_database_from_a_newer_jarvis_is_refused_and_left_untouched(tmp_path):
    path = tmp_path / "m.db"
    PersonalMemoryStore(path)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA user_version = 99")
    connection.close()

    with pytest.raises(SchemaVersionError, match="schema version 99, newer than this version of JARVIS supports"):
        PersonalMemoryStore(path)

    assert schema_version(path) == 99


def test_pending_migrations_apply_in_order(tmp_path):
    path = tmp_path / "x.db"
    migrations = (
        ("CREATE TABLE a (id INTEGER)",),
        ("ALTER TABLE a ADD COLUMN name TEXT", "INSERT INTO a VALUES (1, 'one')"),
    )

    assert apply_migrations(path, migrations[:1], "test") == 1
    assert apply_migrations(path, migrations, "test") == 2

    connection = sqlite3.connect(path)
    assert connection.execute("SELECT id, name FROM a").fetchall() == [(1, "one")]
    connection.close()


def test_a_failing_migration_rolls_back_everything(tmp_path):
    """DDL included - which Python's sqlite3 would otherwise autocommit."""

    path = tmp_path / "x.db"
    apply_migrations(path, (("CREATE TABLE a (id INTEGER)",),), "test")
    broken = (
        ("CREATE TABLE a (id INTEGER)",),
        ("CREATE TABLE b (id INTEGER)", "THIS IS NOT SQL"),
    )

    with pytest.raises(sqlite3.OperationalError):
        apply_migrations(path, broken, "test")

    assert schema_version(path) == 1
    connection = sqlite3.connect(path)
    tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    connection.close()
    assert tables == {"a"}  # table b's creation was rolled back too


def test_released_migrations_are_append_only():
    """Migration 1 of each store is the original schema; editing a released
    migration would silently diverge existing installations. This pins the
    table set each first migration creates."""

    assert "CREATE TABLE IF NOT EXISTS personal_memory" in PERSONAL_MEMORY_MIGRATIONS[0][0]
    assert "CREATE TABLE IF NOT EXISTS consent_decisions" in PERSONAL_MEMORY_MIGRATIONS[0][1]
    assert "CREATE TABLE IF NOT EXISTS profiles" in PROFILE_MIGRATIONS[0][0]
    assert "CREATE TABLE IF NOT EXISTS active_profile" in PROFILE_MIGRATIONS[0][1]
