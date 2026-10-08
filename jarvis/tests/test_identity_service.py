"""Tests for the local Guardian profile service layer."""

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore


@pytest.fixture
def service(tmp_path):
    return ProfileService(ProfileStore(tmp_path / "profiles.db"))


def test_create_profile_persists_and_returns_record(service):
    record = service.create_profile("Robert", "Administrator")

    assert record.display_name == "Robert"
    assert record.role == "Administrator"
    assert record.id

    profiles = service.list_profiles()
    assert len(profiles) == 1
    assert profiles[0].id == record.id


def test_create_profile_rejects_unknown_role(service):
    with pytest.raises(ValueError, match="Profile role must be one of"):
        service.create_profile("Robert", "Superuser")

    assert service.list_profiles() == ()


def test_list_profiles_empty_service(service):
    assert service.list_profiles() == ()


def test_active_profile_none_before_any_selection(service):
    assert service.active_profile() is None


def test_select_profile_sets_and_returns_active(service):
    created = service.create_profile("Robert", "Administrator")

    selected = service.select_profile(created.id)

    assert selected.id == created.id
    active = service.active_profile()
    assert active is not None
    assert active.id == created.id


def test_select_profile_switches_active_selection(service):
    first = service.create_profile("Robert", "Administrator")
    second = service.create_profile("Alex", "Child")

    service.select_profile(first.id)
    service.select_profile(second.id)

    assert service.active_profile().id == second.id


def test_select_profile_rejects_unknown_id(service):
    with pytest.raises(ValueError, match="no such profile exists"):
        service.select_profile("does-not-exist")

    assert service.active_profile() is None


# --- ESR-0061 WP3b (EBG-0110 backend): per-profile memory-to-cloud control ---------------------------------------


def test_a_new_profile_shares_no_memory_with_the_cloud(service):
    assert service.create_profile("Robert", "Administrator").share_memory_with_cloud is False


@pytest.mark.parametrize("role", ["Administrator", "Adult"])
def test_memory_sharing_can_be_turned_on_and_off_for_an_administrator_or_adult(service, role):
    record = service.create_profile("Pat", role)

    assert service.set_cloud_memory_sharing(record.id, True).share_memory_with_cloud is True
    assert service.list_profiles()[0].share_memory_with_cloud is True
    assert service.set_cloud_memory_sharing(record.id, False).share_memory_with_cloud is False


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_memory_sharing_cannot_be_turned_on_for_a_child_or_guest(service, role):
    record = service.create_profile("Sam", role)

    with pytest.raises(ValueError, match="cannot share memory"):
        service.set_cloud_memory_sharing(record.id, True)

    assert service.list_profiles()[0].share_memory_with_cloud is False
    assert service.set_cloud_memory_sharing(record.id, False).share_memory_with_cloud is False


def test_memory_sharing_for_an_unknown_profile_is_an_error(service):
    with pytest.raises(ValueError, match="no such profile"):
        service.set_cloud_memory_sharing("missing", True)
