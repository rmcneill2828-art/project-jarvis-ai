"""User identity/profile service layer (GAM-0001 Section 8.1, EIP-ESR0046-001).

Wraps `ProfileStore` with the business rules the storage layer itself does
not enforce - principally, that `select_profile` refuses an unknown id,
mirroring `PersonalMemoryStore.add()`'s existing referential-integrity
pattern in `jarvis/memory/store.py`.
"""

from __future__ import annotations

import uuid

from jarvis.identity.store import ProfileRecord, ProfileStore, utc_now


class ProfileService:
    """Create, list and select local Guardian profiles."""

    def __init__(self, store: ProfileStore) -> None:
        self._store = store

    def create_profile(self, display_name: str, role: str) -> ProfileRecord:
        """Create and persist a new profile.

        `role` validation happens in `ProfileRecord.__post_init__` - an
        invalid role raises `ValueError` before the store is ever touched.
        """

        record = ProfileRecord(
            id=str(uuid.uuid4()),
            display_name=display_name,
            role=role,
            created_at=utc_now(),
        )
        return self._store.create(record)

    def list_profiles(self) -> tuple[ProfileRecord, ...]:
        """Return every stored profile."""

        return self._store.list_all()

    def select_profile(self, profile_id: str) -> ProfileRecord:
        """Mark `profile_id` as the active profile and return it.

        Raises `ValueError` if no profile with that id exists.
        """

        record = self._store.get(profile_id)
        if record is None:
            msg = f"Cannot select profile {profile_id!r}: no such profile exists."
            raise ValueError(msg)
        self._store.set_active(profile_id)
        return record

    def active_profile(self) -> ProfileRecord | None:
        """Return the currently active profile, or None if none is selected."""

        return self._store.get_active()
