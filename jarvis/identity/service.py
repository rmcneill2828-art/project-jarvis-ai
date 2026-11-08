"""User identity/profile service layer (GAM-0001 Section 8.1, EIP-ESR0046-001).

Wraps `ProfileStore` with the business rules the storage layer itself does
not enforce - principally, that `select_profile` refuses an unknown id,
mirroring `PersonalMemoryStore.add()`'s existing referential-integrity
pattern in `jarvis/memory/store.py`.
"""

from __future__ import annotations

import threading
import time
import uuid
from collections.abc import Callable
from typing import Any

from jarvis.identity.admin_pin import AdminPin
from jarvis.identity.child_consent import ChildConsentStore
from jarvis.identity.child_disclosure import ChildDisclosureStore
from jarvis.identity.safety_events import SafetyEventStore
from jarvis.identity.store import ProfileRecord, ProfileStore, utc_now
from jarvis.shared.errors import ClientFacingPermissionError, ClientFacingValueError

CLOUD_MEMORY_SHARING_ROLES = frozenset({"Administrator", "Adult"})

# A Child or Guest session is a locked session (EIP-ESR0061-006 P2): leaving it
# for any profile that is not itself Child or Guest needs the PIN.
LOCKED_SESSION_ROLES = frozenset({"Child", "Guest"})

# The idle lock (ESR-0062 WP2, EIP-ESR0062-002 L1-L3): once a PIN is set, an
# Adult or Administrator left without use for this long is signed out, as
# `begin_app_session` does at a restart. Fixed in v1.0 (decision D-1).
IDLE_LOCK_SECONDS = 15 * 60
IDLE_LOCK_ROLES = frozenset({"Adult", "Administrator"})


def pin_required_to_switch(active: ProfileRecord | None, target: ProfileRecord) -> bool:
    """The elevation rule (EIP-ESR0061-006 P2, 6.2), the one place it lives.

    From a Child or Guest profile, or from no profile at all (a fresh start is
    the lowest privilege), switching to an Adult or Administrator profile
    needs the PIN; between Child and Guest it is free. From an Adult profile,
    only switching to an Administrator needs it. An Administrator switches
    freely. Staying on the same profile is not a switch.
    """

    if active is not None and active.id == target.id:
        return False
    if active is None or active.role in LOCKED_SESSION_ROLES:
        return target.role not in LOCKED_SESSION_ROLES
    if target.role == "Administrator":
        return active.role != "Administrator"
    return False


class ProfileService:
    """Create, list and select local Guardian profiles, under the household
    PIN's rules (ESR-0061 WP6a)."""

    def __init__(
        self,
        store: ProfileStore,
        pin: AdminPin | None = None,
        *,
        wall_clock: Callable[[], float] = time.time,
        monotonic_clock: Callable[[], float] = time.monotonic,
        idle_lock_seconds: float = IDLE_LOCK_SECONDS,
    ) -> None:
        self._store = store
        self.pin = pin or AdminPin(store)
        # The idle lock (WP2 L1-L3). The last activity is kept in memory only (a
        # restart already signs out), as a (wall, monotonic) pair for the
        # profile it belongs to; one mutex makes the check-and-clear happen
        # exactly once however many threads ask.
        self._wall_clock = wall_clock
        self._monotonic_clock = monotonic_clock
        self.idle_lock_seconds = idle_lock_seconds
        self._idle_mutex = threading.Lock()
        self._last_activity: tuple[str, float, float] | None = None
        # Moderation's safety events share the identity database (WP6b, M5).
        self.safety_events = SafetyEventStore(store)
        # A Child's consent to ask Claude, in the same database (WP6c, C2).
        self.child_consents = ChildConsentStore(store)
        # A Child's acknowledgement of the first-use explanation (WP6d, D1).
        self.child_disclosures = ChildDisclosureStore(store)

    # -- The Child's first-use explanation and the safety summary (WP6d) -------

    def disclosure_status(self, record: ProfileRecord | None) -> dict[str, Any]:
        """Whether the signed-in profile must see the first-use explanation:
        a Child, until it has said it understands."""

        if record is None or record.role != "Child":
            return {"required": False, "acknowledged": False, "acknowledgedAt": None}
        at = self.child_disclosures.acknowledged_at(record.id)
        return {"required": at is None, "acknowledged": at is not None, "acknowledgedAt": at}

    def acknowledge_disclosure(self, child: ProfileRecord) -> dict[str, Any]:
        """The child's own acknowledgement, for itself only."""

        if child.role != "Child":
            msg = "Only a Child profile acknowledges this, for itself."
            raise ClientFacingPermissionError(msg)
        self.child_disclosures.acknowledge(child.id)
        return self.disclosure_status(child)

    def household_safety_record(self, profile_id: str) -> dict[str, Any]:
        """What the household-safety tables (WP6) keep about one profile, for
        its own export: its safety events (kind, side, time; never text), its
        Claude consents (revoked ones too) and when it acknowledged the
        first-use explanation (ESR-0061 session-wide review, Medium M1)."""

        consents = []
        for row in self.child_consents.history(profile_id):
            giver = self._store.get(str(row["consentedBy"]))
            consents.append(
                {
                    "recordedAt": row["recordedAt"],
                    "recordedBy": giver.display_name if giver is not None else "a profile since removed",
                    "acknowledgedAt": row["acknowledgedAt"],
                    "revokedAt": row["revokedAt"],
                }
            )
        return {
            "safetyEvents": self.safety_events.list_for_profile(profile_id),
            "claudeConsents": consents,
            "explanationAcknowledgedAt": self.child_disclosures.acknowledged_at(profile_id),
        }

    def safety_summary(self) -> list[dict[str, Any]]:
        """For each Child and Guest profile (the two moderated roles): how many
        turns the safety checker stopped, by day and category. Never text.
        Turns taken with nobody signed in (moderated as a Guest) are one more
        entry, with no profile id, when there are any (WP6d review, Low)."""

        entries: list[dict[str, Any]] = [
            {
                "profileId": record.id,
                "displayName": record.display_name,
                "role": record.role,
                "events": self.safety_events.daily_counts(record.id),
            }
            for record in self._store.list_all()
            if record.role in ("Child", "Guest")
        ]
        unsigned = self.safety_events.daily_counts(None)
        if unsigned:
            entries.append({"profileId": None, "displayName": "Nobody signed in", "role": "Guest", "events": unsigned})
        return entries

    # -- Claude for a Child (ESR-0061 WP6c, EIP-ESR0061-006 C1, C2, 6.6) --------

    def _child(self, profile_id: str) -> ProfileRecord:
        record = self._store.get(profile_id)
        if record is None:
            msg = "No such profile."
            raise ClientFacingValueError(msg)
        if record.role != "Child":
            msg = "Consent to ask Claude is only for a Child profile."
            raise ClientFacingValueError(msg)
        return record

    def record_child_consent(self, administrator: ProfileRecord, profile_id: str) -> dict[str, Any]:
        """An Administrator allows a Child profile to ask Claude. Needs the PIN
        set (P3), so the child cannot simply switch up and allow it themselves."""

        if administrator.role != "Administrator":
            msg = "Only an Administrator profile can allow a child to ask Claude."
            raise ClientFacingPermissionError(msg)
        if not self.pin.is_set():
            msg = "Set the Administrator PIN first: without it, a child could switch profiles and allow this themselves."
            raise ClientFacingValueError(msg)
        self._child(profile_id)
        current = self.child_consents.current(profile_id)
        if current is not None and not self._giver_is_administrator(current.consented_by):
            # A consent whose giver is no longer an Administrator is replaced,
            # not kept, so the new one is this Administrator's (review Low L2).
            self.child_consents.revoke(profile_id)
        self.child_consents.record(profile_id, administrator.id)
        return self.child_consent_status(profile_id)

    def _giver_is_administrator(self, profile_id: str) -> bool:
        giver = self._store.get(profile_id)
        return giver is not None and giver.role == "Administrator"

    def revoke_child_consent(self, profile_id: str) -> dict[str, Any]:
        self._child(profile_id)
        self.child_consents.revoke(profile_id)
        return self.child_consent_status(profile_id)

    def acknowledge_child_consent(self, child: ProfileRecord) -> dict[str, Any]:
        """The child's own acknowledgement, for themselves only."""

        if child.role != "Child":
            msg = "Only a Child profile acknowledges this, for itself."
            raise ClientFacingPermissionError(msg)
        if not self.child_consents.acknowledge(child.id):
            msg = "Nobody has allowed this profile to ask Claude."
            raise ClientFacingValueError(msg)
        return self.child_consent_status(child.id)

    def child_may_ask_claude(self, record: ProfileRecord | None) -> bool:
        """True only for a Child whose consent is recorded, acknowledged and
        unrevoked, given by a profile that is still an Administrator, with the
        PIN set. Checked on every offer and every send, so revoking takes
        effect at once."""

        if record is None or record.role != "Child" or not self.pin.is_set():
            return False
        consent = self.child_consents.current(record.id)
        if consent is None or consent.acknowledged_at is None:
            return False
        return self._giver_is_administrator(consent.consented_by)

    def child_consent_status(self, profile_id: str) -> dict[str, Any]:
        record = self._child(profile_id)
        consent = self.child_consents.current(profile_id)
        giver = None if consent is None else self._store.get(consent.consented_by)
        return {
            "profileId": profile_id,
            "recorded": consent is not None,
            "recordedAt": None if consent is None else consent.recorded_at,
            "recordedBy": None if giver is None else giver.display_name,
            "acknowledged": consent is not None and consent.acknowledged_at is not None,
            "acknowledgedAt": None if consent is None else consent.acknowledged_at,
            "allowed": self.child_may_ask_claude(record),
        }

    def create_profile(self, display_name: str, role: str) -> ProfileRecord:
        """Create and persist a new profile.

        The household's first profile can be created by anyone and must be an
        Administrator (otherwise nobody could ever manage the household). Every
        later profile needs an Administrator signed in **and** a PIN set
        (EIP-ESR0061-006 P2, P3): with no PIN, anyone can become the
        Administrator, so a new profile then protects nothing.

        `role` validation happens in `ProfileRecord.__post_init__` - an
        invalid role raises `ValueError` before the store is ever touched.
        """

        record = ProfileRecord(
            id=str(uuid.uuid4()),
            display_name=display_name,
            role=role,
            created_at=utc_now(),
        )
        if not self._store.list_all():
            if role != "Administrator":
                msg = "The first profile must be an Administrator, who manages JARVIS for the household."
                raise ClientFacingValueError(msg)
            return self._store.create(record)
        active = self._store.get_active()
        if active is None or active.role != "Administrator":
            msg = "Only an Administrator can add a profile."
            raise ClientFacingPermissionError(msg)
        if not self.pin.is_set():
            msg = "Set an Administrator PIN before adding profiles."
            raise ClientFacingPermissionError(msg)
        return self._store.create(record)

    def switch_requirements(self, profile_id: str) -> dict[str, Any]:
        """What switching to `profile_id` would need, for the screen to ask for
        the PIN only when it is needed. The backend still decides in
        `select_profile`."""

        target = self._store.get(profile_id)
        if target is None:
            msg = "No such profile."
            raise ClientFacingValueError(msg)
        status = self.pin.status()
        needed = pin_required_to_switch(self._store.get_active(), target) and status.is_set
        return {"pinRequired": needed, **status.to_payload()}

    def list_profiles(self) -> tuple[ProfileRecord, ...]:
        """Return every stored profile."""

        return self._store.list_all()

    def select_profile(self, profile_id: str, pin: object = None) -> ProfileRecord:
        """Mark `profile_id` as the active profile and return it.

        When the elevation rule (`pin_required_to_switch`) applies and a PIN is
        set, `pin` must be the household PIN: a wrong one is refused and counted
        towards the lock-out. With no PIN set, switching stays open as before
        (EIP-ESR0061-006 P3), and the screen says safety is not enforced.

        Raises `ValueError` if no profile with that id exists.
        """

        record = self._store.get(profile_id)
        if record is None:
            msg = f"Cannot select profile {profile_id!r}: no such profile exists."
            raise ClientFacingValueError(msg)
        if pin_required_to_switch(self._store.get_active(), record) and self.pin.is_set():
            if pin is None:
                msg = "The Administrator PIN is needed to switch to this profile."
                raise ClientFacingPermissionError(msg)
            self.pin.verify(pin)
        self._store.set_active(profile_id)
        self._touch()
        return record

    def set_first_pin(self, pin: object) -> None:
        """Set the household's first PIN: an Administrator must be signed in.
        Recorded, with the profile's name, for the next Administrator sign-in."""

        active = self._require_administrator("Only an Administrator can set the PIN.")
        self.pin.set_first(pin, active.display_name)
        # The lock starts counting from here, never from an older session (L2).
        self._touch()

    def change_pin(self, current_pin: object, new_pin: object) -> None:
        """Change the PIN: an Administrator signed in, and the current PIN."""

        self._require_administrator("Only an Administrator can change the PIN.")
        if not self.pin.is_set():
            msg = "No PIN is set yet."
            raise ClientFacingValueError(msg)
        self.pin.change(current_pin, new_pin)
        self._touch()

    def signin_notices(self, record: ProfileRecord) -> list[dict[str, Any]]:
        """For an Administrator just signed in, the PIN notices waiting for
        them (then cleared); nothing for anyone else."""

        if record.role != "Administrator":
            return []
        return self.pin.take_notices()

    def _require_administrator(self, message: str) -> ProfileRecord:
        active = self._store.get_active()
        if active is None or active.role != "Administrator":
            raise ClientFacingPermissionError(message)
        return active

    def set_cloud_memory_sharing(self, profile_id: str, enabled: bool) -> ProfileRecord:
        """Allow or stop a profile's retained memory notes accompanying an
        escalated (cloud) question. Off by default (ESR-0061 WP3b, EBG-0110).

        Only a profile that may escalate at all (Administrator or Adult) can
        have it on: for a Child it stays off until WP6 delivers consent, and a
        Guest never escalates.
        """

        record = self._store.get(profile_id)
        if record is None:
            msg = f"Cannot change profile {profile_id!r}: no such profile exists."
            raise ClientFacingValueError(msg)
        if enabled and record.role not in CLOUD_MEMORY_SHARING_ROLES:
            msg = f"A {record.role} profile cannot share memory with the cloud service."
            raise ClientFacingValueError(msg)
        self._store.set_share_memory_with_cloud(profile_id, enabled)
        updated = self._store.get(profile_id)
        assert updated is not None
        return updated

    def get_profile(self, profile_id: str) -> ProfileRecord | None:
        """Return one profile, or None."""

        return self._store.get(profile_id)

    def check_erasable(self, profile_id: str, active_profile_id: str | None) -> ProfileRecord:
        """The profile that would be erased, or a refusal in plain words.

        Refused for the signed-in profile (switch away first) and for the last
        Administrator (the household would have nobody who can manage it).
        """

        record = self._store.get(profile_id)
        if record is None:
            msg = "No such profile."
            raise ClientFacingValueError(msg)
        if profile_id == active_profile_id:
            msg = "Switch to another profile first: the profile you are using cannot be erased."
            raise ClientFacingValueError(msg)
        if record.role == "Administrator":
            administrators = [entry for entry in self._store.list_all() if entry.role == "Administrator"]
            if len(administrators) <= 1:
                msg = "This is the last Administrator profile, so it cannot be erased."
                raise ClientFacingValueError(msg)
        return record

    def delete_profile(self, profile_id: str) -> bool:
        """Delete the profile record only. Callers use `check_erasable` first and
        remove that profile's own data first."""

        return self._store.delete(profile_id)

    def active_profile(self) -> ProfileRecord | None:
        """Return the currently active profile, or None if none is selected."""

        return self._store.get_active()

    # -- The idle lock (ESR-0062 WP2, EIP-ESR0062-002 L1-L3) ----------------

    def lock_if_idle(self) -> bool:
        """Sign out an idle Adult or Administrator; return whether this call did.

        Applies only once a PIN is set (P3). A session with no recorded
        activity is stamped now rather than left unlockable (L2). Elapsed time
        is the larger of wall-clock and monotonic elapsed, so a computer that
        slept is locked on waking and a clock set back cannot hold a session
        open (L3)."""

        with self._idle_mutex:
            return self._lock_if_idle_held()

    def record_activity(self) -> bool:
        """A person used JARVIS. A session already due is locked, never revived
        (L2); otherwise the signed-in profile's activity is stamped now.
        Returns whether the session was locked."""

        with self._idle_mutex:
            if self._lock_if_idle_held():
                return True
            active = self._store.get_active()
            self._last_activity = None if active is None else self._stamp(active.id)
            return False

    def _touch(self) -> None:
        """Stamp the signed-in profile's activity without the due check: for a
        select or a PIN change, whose request passed that check just before,
        so a lock here could never be announced (implementation review L-1)."""

        with self._idle_mutex:
            active = self._store.get_active()
            self._last_activity = None if active is None else self._stamp(active.id)

    def _stamp(self, profile_id: str) -> tuple[str, float, float]:
        return (profile_id, self._wall_clock(), self._monotonic_clock())

    def _lock_if_idle_held(self) -> bool:
        active = self._store.get_active()
        if active is None or active.role not in IDLE_LOCK_ROLES or not self.pin.is_set():
            return False
        last = self._last_activity
        if last is None or last[0] != active.id:
            self._last_activity = self._stamp(active.id)
            return False
        elapsed = max(self._wall_clock() - last[1], self._monotonic_clock() - last[2])
        if elapsed < self.idle_lock_seconds:
            return False
        self._store.clear_active()
        self._last_activity = None
        return True

    def begin_app_session(self) -> bool:
        """Called once when the backend starts (ESR-0061 WP7; Antigravity
        technology and security review, F6).

        The signed-in profile is stored, so without this an Administrator who
        closed JARVIS would leave the next person, perhaps a child, signed in as
        the Administrator with no PIN asked, able to change Settings and allow
        themselves Claude. Once a PIN is set, an Adult or Administrator session
        is therefore not carried over: JARVIS starts with no profile selected
        (the lowest privilege, moderated as a Guest), and switching up needs the
        PIN as usual. A Child or Guest session is kept, because it already is the
        lowest level; with no PIN set there is nothing to protect yet (P3).
        Returns whether a session was cleared."""

        active = self._store.get_active()
        if active is None or active.role in LOCKED_SESSION_ROLES or not self.pin.is_set():
            return False
        self._store.clear_active()
        return True
