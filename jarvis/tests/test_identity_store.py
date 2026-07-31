"""Tests for the local Guardian profile SQLite store."""

from datetime import UTC, datetime

import pytest

from jarvis.identity.store import HOUSEHOLD_ROLES, ProfileRecord, ProfileStore


@pytest.fixture
def store(tmp_path):
    return ProfileStore(tmp_path / "profiles.db")


def _record(profile_id="profile-1", display_name="Robert", role="Administrator"):
    return ProfileRecord(
        id=profile_id,
        display_name=display_name,
        role=role,
        created_at=datetime.now(UTC),
    )


def test_creates_parent_directory(tmp_path):
    db_path = tmp_path / "nested" / "profiles.db"

    ProfileStore(db_path)

    assert db_path.parent.exists()


@pytest.mark.parametrize("role", HOUSEHOLD_ROLES)
def test_profile_record_accepts_every_household_role(role):
    record = _record(role=role)

    assert record.role == role


def test_profile_record_rejects_unknown_role():
    with pytest.raises(ValueError, match="Profile role must be one of"):
        _record(role="Superuser")


def test_create_and_list_all(store):
    store.create(_record())

    profiles = store.list_all()

    assert len(profiles) == 1
    assert profiles[0].id == "profile-1"
    assert profiles[0].display_name == "Robert"
    assert profiles[0].role == "Administrator"


def test_list_all_empty_store(store):
    assert store.list_all() == ()


def test_get_unknown_id_returns_none(store):
    assert store.get("does-not-exist") is None


def test_get_returns_created_profile(store):
    store.create(_record())

    fetched = store.get("profile-1")

    assert fetched is not None
    assert fetched.display_name == "Robert"


def test_get_active_returns_none_before_any_selection(store):
    assert store.get_active() is None


def test_set_active_and_get_active(store):
    store.create(_record("profile-1", "Robert", "Administrator"))
    store.create(_record("profile-2", "Alex", "Child"))

    store.set_active("profile-2")

    active = store.get_active()
    assert active is not None
    assert active.id == "profile-2"
    assert active.display_name == "Alex"


def test_set_active_overwrites_previous_selection(store):
    store.create(_record("profile-1", "Robert", "Administrator"))
    store.create(_record("profile-2", "Alex", "Child"))

    store.set_active("profile-1")
    store.set_active("profile-2")

    assert store.get_active().id == "profile-2"


def test_get_active_returns_none_when_active_profile_since_deleted(store, tmp_path):
    """Defensive case only - deletion is not authorised by this package, but
    a corrupted/hand-edited db should degrade honestly rather than raise."""

    store.create(_record())
    store.set_active("profile-1")

    with store._transaction() as connection:  # noqa: SLF001 - direct row removal, no delete() API exists
        connection.execute("DELETE FROM profiles WHERE id = ?", ("profile-1",))

    assert store.get_active() is None


def test_persists_across_new_store_instance(tmp_path):
    db_path = tmp_path / "profiles.db"
    first = ProfileStore(db_path)
    first.create(_record())
    first.set_active("profile-1")

    second = ProfileStore(db_path)

    assert len(second.list_all()) == 1
    assert second.get_active().id == "profile-1"
