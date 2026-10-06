"""Personal Memory consent-gated service (GAM-0001 Section 9.2, EIP-ESR0027-001).

The first real instance of a Sentinel `REVIEW` decision actually being
resolved: `propose()` submits a memory-retention request through the same
Sentinel trust gateway used for conversation, `approve()`/`deny()` require a
distinct, explicit call before anything is durably stored. No code path lets
a proposal store itself.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from jarvis.memory.store import (
    ConsentDecisionRecord,
    PersonalMemoryRecord,
    PersonalMemoryStore,
    utc_now,
)
from jarvis.shared.errors import (
    ClientFacingKeyError,
    ClientFacingPermissionError,
    ClientFacingRuntimeError,
)
from sentinel.core import (
    SentinelDecisionOutcome,
    SentinelRequest,
    SentinelResponse,
    SentinelTrustGateway,
)

logger = logging.getLogger(__name__)

MEMORY_RETENTION_CAPABILITY = "memory_retention"

# Unresolved proposals kept at once (EBG-0144, ESR-0059 WP9). Past this, the
# oldest unresolved proposal is dropped - nothing is stored or decided for
# it, exactly as if the process had restarted.
MAX_PENDING_PROPOSALS = 100  # per profile (ESR-0061 WP2a)
LOCAL_USER_APPROVER_LABEL = "local-user"


@dataclass(frozen=True)
class PendingMemoryRequest:
    """A proposed memory-retention request awaiting an explicit human decision.

    Held in memory only - a proposal that is never approved or denied
    (process restart, abandoned) simply disappears with the pending dict.
    Only the eventual *resolution* (approve or deny) is made durable.
    """

    id: str
    content: str
    sentinel_response: SentinelResponse
    created_at: datetime = field(default_factory=utc_now)
    # The profile the memory will belong to; None for a shared household
    # note (EBG-0132, ESR-0059 WP13).
    profile_id: str | None = None


class PersonalMemoryService:
    """Propose, approve and deny Personal Memory retention requests."""

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        store: PersonalMemoryStore,
        source: str = "jarvis.memory",
    ) -> None:
        self._gateway = gateway
        self._store = store
        self._source = source
        self._pending: dict[str, PendingMemoryRequest] = {}

    def propose(self, content: str, profile_id: str | None = None) -> PendingMemoryRequest:
        """Propose retaining `content`, evaluating it through Sentinel.

        Requires the resulting decision to be REVIEW before creating a
        pending request. Refuses (raises RuntimeError) on DENY or on any
        unexpected outcome (including ALLOW) rather than ever trusting a
        non-REVIEW outcome to imply consent has already been given.
        """

        sentinel_request = SentinelRequest(
            source=self._source,
            intent="memory.retain",
            requires_approval=True,
            metadata={"capability": MEMORY_RETENTION_CAPABILITY},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)
        outcome = sentinel_response.decision.outcome

        if outcome is SentinelDecisionOutcome.DENY:
            msg = "Memory retention request was denied by Sentinel policy before any human review."
            raise ClientFacingRuntimeError(msg)
        if outcome is not SentinelDecisionOutcome.REVIEW:
            msg = (
                f"Memory retention request received unexpected Sentinel outcome {outcome.value!r} "
                "(expected REVIEW) - refusing rather than treating this as pre-approved."
            )
            raise RuntimeError(msg)

        pending_id = str(uuid.uuid4())
        pending = PendingMemoryRequest(
            id=pending_id, content=content, sentinel_response=sentinel_response, profile_id=profile_id
        )
        self._pending[pending_id] = pending
        # The cap applies per profile (ESR-0061 WP2a, EBG-0157 item 5): one
        # profile's proposals must not evict another's. Dicts keep insertion
        # order, so the first match is that profile's oldest.
        same_profile = [key for key, value in self._pending.items() if value.profile_id == profile_id]
        while len(same_profile) > MAX_PENDING_PROPOSALS:
            oldest_id = same_profile.pop(0)
            del self._pending[oldest_id]
            logger.info("Oldest unresolved memory proposal dropped: pending_id=%s", oldest_id)
        return pending

    def approve(self, pending_id: str) -> PersonalMemoryRecord:
        """Approve a pending memory-retention request, storing it durably."""

        pending = self._pop_pending(pending_id)
        decision = self._record_decision(pending, "approved")
        record = PersonalMemoryRecord(
            id=str(uuid.uuid4()),
            content=pending.content,
            created_at=utc_now(),
            consent_decision_id=decision.id,
            profile_id=pending.profile_id,
        )
        self._store.add(record)
        return record

    def deny(self, pending_id: str) -> ConsentDecisionRecord:
        """Deny a pending memory-retention request. Content is never stored."""

        pending = self._pop_pending(pending_id)
        decision = self._record_decision(pending, "denied")
        logger.info("Memory retention request denied: decision_id=%s", decision.id)
        return decision

    def list_records(self) -> tuple[PersonalMemoryRecord, ...]:
        """Return all stored Personal Memory records."""

        return self._store.list_all()

    def reassign_unknown_owners(self, known_profile_ids: set[str], new_owner: str) -> int:
        return self._store.reassign_unknown_owners(known_profile_ids, new_owner)

    def list_visible(self, profile_id: str | None, *, include_household: bool = True) -> tuple[PersonalMemoryRecord, ...]:
        """Return the memories `profile_id` may see: its own plus, unless
        excluded, shared household notes (EBG-0132)."""

        return self._store.list_visible(profile_id, include_household=include_household)

    def count_visible(self, profile_id: str | None, *, include_household: bool = True) -> int:
        return self._store.count_visible(profile_id, include_household=include_household)

    def delete(self, record_id: str, profile_id: str | None = None, *, is_administrator: bool = False) -> None:
        """Revoke one retained memory (EBG-0145, ESR-0059 WP10).

        Deliberately not gated by Sentinel policy: revocation only removes
        the user's own data, and no policy should be able to stop a user
        withdrawing something they chose to retain (MDS-0001 Section 7.4).
        The consent decision that approved it is kept as audit history, and
        the revocation is logged by id only - never by content. Raises
        KeyError for an unknown id rather than reporting a false success.
        """

        # EBG-0132 (ESR-0059 WP13): a profile may delete only its own
        # memories; a shared household note only by an Administrator, by the
        # Programme Sponsor's decision. Another profile's memory is reported
        # exactly like a missing one, so its existence is never revealed.
        record = self._store.get(record_id)
        not_found = f"No stored memory found for id: {record_id!r}."
        if record is None or (record.profile_id is not None and record.profile_id != profile_id):
            raise ClientFacingKeyError(not_found)
        if record.profile_id is None and not is_administrator:
            msg = "Only an Administrator can delete a shared household note."
            raise ClientFacingPermissionError(msg)
        if not self._store.delete(record_id):
            raise ClientFacingKeyError(not_found)
        logger.info("Memory record revoked: record_id=%s", record_id)

    def record_count(self) -> int:
        """Return the number of stored Personal Memory records (EBG-0131)."""

        return self._store.count()

    def export_backup(self, backup_dir: Path) -> Path:
        """Write a full, timestamped point-in-time backup file and return its path.

        BRD-0001 (Backup, Recovery and Data Protection Guidance, EBG-0023):
        first concrete increment - a human-triggered, local-filesystem-only
        export. Deliberately does not: encrypt the file (plaintext content,
        same as the source SQLite database - flagged as an explicit open
        gap in BRD-0001, not silently assumed safe); schedule itself
        (invoked only when `memory.backup` is called); or write anywhere
        but `backup_dir` (no network transmission - there is no Sentinel
        Network Exposure surface for this to route through yet, per
        ADR-0020's still-unbuilt status). Restore/import from a backup file
        is explicitly out of scope for this increment - see BRD-0001.

        `backup_dir` is created if it does not already exist, mirroring
        `PersonalMemoryStore.__init__`'s own parent-directory creation for
        the primary database file.
        """

        backup_dir.mkdir(parents=True, exist_ok=True)
        snapshot = self._store.export_snapshot()
        exported_at = utc_now()
        backup_path = backup_dir / f"personal_memory_backup_{exported_at.strftime('%Y%m%dT%H%M%S%fZ')}.json"
        payload = {
            "exported_at": exported_at.isoformat(),
            "personal_memory": list(snapshot["personal_memory"]),
            "consent_decisions": list(snapshot["consent_decisions"]),
        }
        backup_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return backup_path

    def restore_backup(self, backup_path: Path, *, confirm_overwrite: bool = False) -> int:
        """Restore Personal Memory from a backup file written by `export_backup()`.

        BRD-0001 Section 6 (EBG-0023): reads and JSON-parses `backup_path`
        (a malformed/missing file fails closed with a clear exception before
        any store write is attempted), then delegates the three minimum
        recovery requirements - structural validation, consent-before-content
        insert order, and the non-empty-store confirmation gate - to
        `PersonalMemoryStore.import_snapshot()`. Returns the number of
        records restored.
        """

        payload = json.loads(backup_path.read_text(encoding="utf-8"))
        return self._store.import_snapshot(payload, confirm_overwrite=confirm_overwrite)

    def _pop_pending(self, pending_id: str) -> PendingMemoryRequest:
        try:
            return self._pending.pop(pending_id)
        except KeyError as exc:
            msg = f"No pending memory request found for id: {pending_id!r} (unknown or already resolved)."
            raise ClientFacingKeyError(msg) from exc

    def _record_decision(self, pending: PendingMemoryRequest, decision: str) -> ConsentDecisionRecord:
        sentinel_decision = pending.sentinel_response.decision
        record = ConsentDecisionRecord(
            id=pending.id,
            capability=MEMORY_RETENTION_CAPABILITY,
            decision=decision,
            decided_at=utc_now(),
            approver_label=LOCAL_USER_APPROVER_LABEL,
            sentinel_outcome=sentinel_decision.outcome.value,
            # SentinelDecision (sentinel/core.py) does not carry PolicyDecision's
            # trust_tier/category through from evaluate() - only outcome, reason
            # and requires_human_approval survive that translation today, so
            # there is no category value to record here honestly.
            sentinel_category=None,
            sentinel_reason=sentinel_decision.reason,
        )
        return self._store.record_decision(record)
