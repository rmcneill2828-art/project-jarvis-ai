# EIP-ESR0027-001 - Personal Memory Implementation with Minimal Consent Gate

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0027-001 |
| Artefact ID | EIP-ESR0027-001 |
| Title | Personal Memory Implementation with Minimal Consent Gate |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0080, registered by this package) |
| Intended Session | ESR-0027 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Implements the first real slice of Guardian's Memory faculty: Personal Memory (MDS-0001 Section 6.2), gated by GAM-0001 Section 9.2's memory-retention consent boundary. `jarvis/memory/` is currently an empty stub; `jarvis/guardian/config.py`'s `persistence_enabled` flag is hardcoded `False` and unused; `jarvis/platform/shell.py` reports Memory as `NOT_IMPLEMENTED`. This package changes that for the Personal tier only.

The Programme Sponsor selected the full scope at ESR-0027 WP0B: not only a storage layer, but a genuinely working consent gate. Grounding this against GAM-0001 surfaced a real dependency the original selection did not anticipate - GAM-0001's own evidence check (Section 9) states plainly that **no approval workflow exists in code today**: Sentinel's `REVIEW` outcome is an enum value carrying a static message only, and `SentinelGatedConversationProvider` treats every non-`ALLOW` decision identically (refuse, do not proceed). There is no existing code path, for any action of any kind, that lets a human's "yes" actually unblock a `REVIEW`-classified request. This package therefore also builds the first minimal instance of that mechanism - scoped as narrowly as GAM-0001 itself allows.

---

# 3. Objective

Let Guardian propose retaining something about the user, require an explicit human decision before it is stored, and store approved items in a local, personal-only data store with per-item traceability back to the decision that authorised it - end to end, for real, not simulated.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `jarvis/memory/__init__.py` | Empty package stub (0 bytes) - the only file under `jarvis/memory/`, confirmed by MDS-0001's own evidence check. |
| `sentinel/core.py` | `SentinelRequest(requires_approval=True, ...)` already exists and, via `TrustTierPolicy.classify()`, already resolves to `TrustCategory.HUMAN_APPROVAL_REQUIRED` -> `REVIEW` with no code changes needed. **No changes to `sentinel/policy.py` or `sentinel/core.py` are required or authorised by this package** - the classification infrastructure GAM-0001 Section 9.2 needs already exists; the gap is entirely at the application layer above it (nothing ever submits a memory-retention request, and nothing ever resolves a `REVIEW` outcome). |
| `jarvis/interfaces/sentinel_conversation.py` | `SentinelGatedConversationProvider.generate()` treats every non-`ALLOW` decision identically ("Sentinel did not allow this request to proceed"). This package does not modify this class or its existing behaviour for ordinary conversation - a new, separate code path is added for memory-retention requests specifically, so conversation gating is unaffected. |
| `jarvis/guardian/runtime.py` | Already registers a `"Guardian Memory Boundary"` service, currently `UNAVAILABLE`/`UNKNOWN`, capabilities `("future-guardian-memory",)` - the intended integration point, mirroring how `"Guardian Provider Boundary"` goes `ONLINE`/`HEALTHY` in `start()` once a `conversation_provider` is connected. |
| `jarvis/guardian/config.py` | `GuardianRuntimeConfig.persistence_enabled` (hardcoded `False`, unused beyond threading through to a status snapshot) - left unchanged by this package; the Memory Boundary service status reports connectivity directly, following the existing Provider Boundary pattern, rather than repurposing this separate flag. |
| `jarvis/interfaces/stdio_rpc.py` | `build_default_runtime()` constructs the single `SentinelTrustGateway` instance conversation requests are evaluated against. This package reuses that same gateway instance for memory-retention requests - one trust boundary, not two. |
| GAM-0001 Section 9.3 (Trusted Mobile Approve/Deny) | Explicitly a future capability, not current - "records the architectural shape only, not an implementation." Out of scope here; see Section 8. |
| GAM-0001 Section 10 (Explicit Non-Goals) | Explicitly excludes "the household role model's authentication or enforcement" from GAM-0001's own scope. This repository has no login, identity or multi-user distinction anywhere (the UXP shows a single static "Robert / Signed in locally" profile card). This package treats the one person operating the running application as the sole party who can approve or deny - there is no other identity to check, and building one is out of scope. |

---

# 5. Scope

This package authorises a future implementation to:

1. Create `jarvis/memory/store.py`:
   - A `PersonalMemoryRecord` dataclass (id, content, `created_at`, `consent_decision_id`) and a `ConsentDecisionRecord` dataclass (id, capability, decision - `"approved"`/`"denied"`, `decided_at`, `approver_label` - fixed `"local-user"`, since no household-role identity exists per Section 4 - `sentinel_outcome`, `sentinel_category`, `sentinel_reason`).
   - A `PersonalMemoryStore` class backed by SQLite (Python stdlib `sqlite3`, per MDS-0001 Section 7.3's initial-engine recommendation), with two tables in the same file: `personal_memory` and `consent_decisions`. Methods: `add(record)`, `list_all()`, `delete(record_id)` for personal-memory records; `record_decision(decision)`, `get_decision(decision_id)` for consent decisions - both tables durable (survive a process restart), satisfying MDS-0001 Section 7.4's requirement that every retained item trace back to a real, persisted decision, not an in-memory value that can vanish. The store's schema is exclusively personal-memory-shaped - no Session or Shared-Family data is ever written to it, satisfying MDS-0001 Section 7.2's data-layer partitioning for the tier this package actually builds.
2. Create `jarvis/memory/service.py`: a `PersonalMemoryService` wrapping a `SentinelTrustGateway` and a `PersonalMemoryStore`, with:
   - `propose(content: str) -> PendingMemoryRequest` - builds a `SentinelRequest(source="jarvis.memory", intent="memory.retain", requires_approval=True, metadata={"capability": "memory_retention"})`, evaluates it via the gateway, asserts the returned decision's outcome is `REVIEW` (Section 7 item 3 below), and holds a `PendingMemoryRequest` (a generated id, the content, the Sentinel response) in an in-memory dict keyed by id. The pending request itself remains in-memory (Section 8 item 7) - only the *resolution* (approve or deny) is made durable, per Finding 1 of the Engineering Reviewer's v0.1 review.
   - `approve(pending_id: str) -> PersonalMemoryRecord` - looks up the pending request, durably records a `ConsentDecisionRecord(decision="approved", ...)` via `record_decision()`, writes the `PersonalMemoryRecord` to the store with `consent_decision_id` set to that decision record's own id (not the transient pending id), removes the request from the pending dict, returns the stored record. Raises `KeyError` for an unknown or already-resolved id.
   - `deny(pending_id: str) -> ConsentDecisionRecord` - looks up the pending request, durably records a `ConsentDecisionRecord(decision="denied", ...)` (content is never written to `personal_memory` - a denial is a real decision on record, not a discarded event), removes the request from the pending dict, returns the decision record. Raises `KeyError` for an unknown or already-resolved id.
   - `list_records() -> tuple[PersonalMemoryRecord, ...]` - delegates to the store.
3. Update `jarvis/memory/__init__.py` to export `PersonalMemoryRecord`, `ConsentDecisionRecord`, `PersonalMemoryStore`, `PersonalMemoryService`, `PendingMemoryRequest`.
4. Update `jarvis/guardian/runtime.py`: `GuardianRuntime.__init__` gains an optional `memory_service: PersonalMemoryService | None = None` parameter; `start()` brings `"Guardian Memory Boundary"` `ONLINE`/`HEALTHY` when a memory service is connected, mirroring the existing Provider Boundary pattern exactly. Add `propose_memory()`, `approve_memory()`, `deny_memory()`, `list_memory()` methods that delegate to the connected service, returning an honest "Guardian has no memory service connected." response (matching `NOT_CONNECTED_RESPONSE`'s existing style) when none is connected, rather than raising.
5. Update `jarvis/interfaces/stdio_rpc.py`: `build_default_runtime()` constructs a `PersonalMemoryStore` (default path `~/.jarvis/memory/personal.db`, overridable via a new `JARVIS_MEMORY_DB_PATH` environment variable for test isolation - the exact lesson learned from ESR-0026 WP1's Ollama test-isolation defect applies here too) and a `PersonalMemoryService` sharing the same `gateway` instance already built for conversation, passed into `GuardianRuntime(..., memory_service=...)`. `StdioRpcServer` gains four new JSON-RPC methods: `memory.propose`, `memory.approve`, `memory.deny`, `memory.list`.
6. Add `jarvis/tests/test_memory_store.py` and `jarvis/tests/test_memory_service.py`, and extend `jarvis/tests/test_guardian_runtime.py` and `jarvis/tests/test_stdio_rpc.py` for the new integration points. All tests must use an injected/temporary database path - no test may touch `~/.jarvis/memory/personal.db`.
7. Register **EBG-0080** (Personal Memory Implementation) in EBR-0001 as `Complete` only once actually implemented, validated and committed, with corresponding updates to PST-0001 and REG-0001.

No other files are authorised to change. No product UXP changes (`src/`, `src-tauri/`) are in scope - per PBK-0001's Feature-First Delivery Discipline, backend capability delivery that a future UXP increment will depend on is an explicitly permitted way to satisfy the live-UXP-progress requirement without touching `src/` itself.

---

# 6. Authorised Files

1. `jarvis/memory/__init__.py`
2. `jarvis/memory/store.py`
3. `jarvis/memory/service.py`
4. `jarvis/guardian/runtime.py`
5. `jarvis/interfaces/stdio_rpc.py`
6. `jarvis/tests/test_memory_store.py`
7. `jarvis/tests/test_memory_service.py`
8. `jarvis/tests/test_guardian_runtime.py`
9. `jarvis/tests/test_stdio_rpc.py`
10. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
11. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
12. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `PersonalMemoryStore.__init__(self, db_path: Path)`: creates the parent directory and both the `personal_memory` table (columns: `id TEXT PRIMARY KEY`, `content TEXT NOT NULL`, `created_at TEXT NOT NULL`, `consent_decision_id TEXT NOT NULL`) and the `consent_decisions` table (columns: `id TEXT PRIMARY KEY`, `capability TEXT NOT NULL`, `decision TEXT NOT NULL`, `decided_at TEXT NOT NULL`, `approver_label TEXT NOT NULL`, `sentinel_outcome TEXT NOT NULL`, `sentinel_category TEXT`, `sentinel_reason TEXT NOT NULL`) if they do not already exist. No implicit default path inside the store itself - the caller (`build_default_runtime()`) supplies it explicitly, matching how `OllamaProvider`'s endpoint is supplied by its caller rather than hardcoded.
2. `PersonalMemoryStore.delete(record_id)`: deletes exactly one row from `personal_memory` by id; must not require or perform any broader destructive operation, satisfying MDS-0001 Section 7.4's per-item revocation requirement directly. The corresponding `consent_decisions` row is retained (a decision record for a since-deleted item is legitimate audit history, not something revocation should erase).
3. `PersonalMemoryService.propose()`: must not write to either store table. Must explicitly assert `sentinel_response.decision.outcome is SentinelDecisionOutcome.REVIEW` (Engineering Reviewer Finding 3) before creating a pending request:
   - If the outcome is `DENY`, `propose()` itself refuses - raise `RuntimeError`, create no pending request, no consent bypass is possible.
   - If the outcome is unexpectedly `ALLOW` (should not happen given `requires_approval=True`, but must never be trusted blindly), `propose()` raises `RuntimeError` naming the unexpected outcome rather than silently treating it as pre-approved - an unexpected `ALLOW` must never let content skip the explicit `approve()` step.
   - A pending request that is never approved or denied (process restart, abandoned) simply disappears with the in-memory pending dict - disclosed as a known limitation (Section 11), not silently masked.
4. `PersonalMemoryService.approve()`/`deny()`: must be idempotent-safe against a double call - the second call on an already-resolved id raises `KeyError` rather than double-storing or silently succeeding.
5. `GuardianRuntime.propose_memory()` etc.: follow the exact same "honest boundary response, never raise" pattern already established by `converse()` for the no-provider-connected and not-running cases.
6. `StdioRpcServer`'s new methods follow the existing `_guardian_converse`/`_platform_status` pattern exactly: validate `params` shape, call the runtime, return a plain JSON-serialisable dict; let unexpected exceptions propagate to `handle_line`'s existing generic exception handler (exception type + message only, matching the established never-leak-more-than-necessary rule).
7. Tests must not make real filesystem writes outside a temporary directory (`tmp_path` pytest fixture) or a `JARVIS_MEMORY_DB_PATH` override pointed at one - matching the store/mock-transport isolation pattern every existing provider adapter test already follows.
8. Tests must cover `propose()` against an injected policy engine for all three outcomes - `REVIEW` (the expected path), `DENY` (refuses, no pending request created), and unexpected `ALLOW` (refuses rather than treating as pre-approved) - per Engineering Reviewer Finding 3.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Session Memory (MDS-0001 Section 6.1) or Shared Family Memory (Section 6.3) implementation - Personal Memory only.
2. Any change to `sentinel/policy.py`, `sentinel/core.py`, or `TrustCategory` - the existing `requires_approval=True` classification path is sufficient and is reused unmodified.
3. Any change to `SentinelGatedConversationProvider` or ordinary conversation-gating behaviour.
4. Trusted Mobile Approve/Deny (GAM-0001 Section 9.3) - explicitly a future capability per GAM-0001 itself; approval in this package happens via a direct JSON-RPC call from whatever is already connected to the running backend (today, the Tauri shell's stdio pipe), not a remote channel.
5. Household role model authentication or enforcement (GAM-0001 Section 8.1/Section 10) - the single running-application user is treated as the sole approver; no login, identity check, or role distinction is built.
6. Encryption or cross-device sync (MDS-0001 Section 8, ADR-0012, EBG-0046) - the store is a single local file, unencrypted, not synchronised. This is a real limitation for a "personal, private" data store and is disclosed plainly in Section 11, not hidden behind reassuring language.
7. Persisting `PendingMemoryRequest` state across a process restart, or any expiry/timeout mechanism for an unresolved pending request.
8. Recording the human approve/deny decision into Sentinel's own `AuditRecorder` - the initial classification (`propose()`'s `gateway.evaluate()` call) is captured there; the final human resolution is now durably recorded in this package's own `consent_decisions` table (Section 5 item 1-2, added in v0.2 per Engineering Reviewer Finding 1), not Sentinel's audit trail. Two separate durable records (Sentinel's classification audit log, this package's decision store) rather than one unified trail - unifying them into a single audit surface is a natural future extension, not built here.
9. Any React/Tauri UI for proposing, approving or denying a memory item - this package delivers the backend JSON-RPC methods only; a future UXP increment would call them.
10. Backup, recovery, or data-protection mechanics (EBG-0023) - explicitly gated by MDS-0001 on this package existing first, not this package's own scope.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. The `personal_memory` SQLite table shall never be shared with, or structurally mixed into, any future Session or Shared-Family table - MDS-0001 Section 7.2's partitioning requirement is non-negotiable even at this single-tier stage.
3. `PersonalMemoryService.propose()` shall always route through `SentinelTrustGateway.evaluate()` - there is no code path that stores a personal-memory item without first obtaining a `REVIEW` decision and then a distinct, separate `approve()` call. A proposal must never be able to store itself.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes, including new store/service tests (covering `propose()`'s `REVIEW`/`DENY`/unexpected-`ALLOW` handling per Section 7 item 8, and both `approve()`/`deny()` producing a durable `ConsentDecisionRecord`) and updated runtime/stdio-RPC tests.
2. A live smoke check (run by the Engineering Implementer directly - no billed external call, no Programme Sponsor "type RUN" gate needed) exercising `memory.propose` -> `memory.approve` -> `memory.list` and `memory.propose` -> `memory.deny` -> `memory.list` (confirming a denied item never appears in `personal_memory` but its decision is durably recorded) through the real `StdioRpcServer`.
3. `validate_repository.py` (full mode) passes with 0 errors. The warning count is expected to rise from the 111 pre-existing baseline by this package's own cross-document Section references (e.g. `EIP-ESR0027-001` citing specific MDS-0001/GAM-0001 sections, `EBR-0001`'s new EBG-0080 row doing the same) - each new warning is a known false positive of `validate_repository.py`'s same-document-only heading check, of the identical class already disclosed and accepted throughout this project's history (matching the "N pre-existing plus M known cross-reference false positives" pattern used for MDS-0001/ADR-0020 at ESR-0026). Amended per Engineering Reviewer Finding 2 (v0.1 review), which correctly identified the original "same pre-existing warning count" wording as inconsistent with the evidence actually submitted. The exact final count shall be disclosed at implementation/commit time, not silently absorbed into "same as before."
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

1. `SentinelTrustGateway`'s existing `requires_approval=True` classification path (`sentinel/core.py`, `sentinel/policy.py`), unchanged by this package.
2. `GuardianRuntime`'s existing `"Guardian Memory Boundary"` service registration point.

## Risks

1. **This is a genuinely minimal consent mechanism, not GAM-0001's full future vision.** No trusted-mobile channel (Section 9.3), no household-role authentication (Section 8.1/10), no notification of a pending request beyond whatever calls `memory.propose` and later polls or is told to call `memory.approve`/`memory.deny`. It satisfies Section 9.1/9.2's letter (an explicit, scoped consent decision before retention) using the only identity this application currently has - the one person running it - not the richer multi-household-member model GAM-0001 ultimately describes. This is disclosed plainly, not presented as more complete than it is.
2. **Unencrypted, unsynchronised local storage for what is explicitly "personal, private" data** (MDS-0001 Section 6.2). Acceptable as a first foundation slice consistent with MDS-0001 Section 7.3's own "starting point, not a full technology evaluation" framing, but a real limitation worth the Programme Sponsor's awareness before any actually-sensitive content is stored through it. Per Engineering Reviewer advisory: before any real sensitive-content production use, a follow-on encryption/data-protection item (Section 8 item 6) should become a mandatory prerequisite, not an optional future enhancement - recorded here as a disclosed expectation for whoever scopes that follow-on work, not a requirement this package itself satisfies.
3. **A pending proposal lost on process restart** is a minor usability rough edge (the user would need to ask Guardian to propose again), not a safety issue - nothing is stored without a fresh, explicit approval either way.
4. **The final human decision is not yet part of Sentinel's own audit trail.** `AuditRecorder` today only captures classification, not resolution - a full accounting of "what did Guardian propose, and what did the human ultimately decide" requires both records today (Sentinel's audit log plus this package's `consent_decisions` table), not one unified trail. Flagged as a natural follow-on, not built here.

---

# 12. Approval Request

v0.1 reviewed by the Engineering Reviewer (Codex) via the AIEMS Exchange Bridge: "concept is sound and appropriately scoped... but amend before Sponsor approval." Two Medium findings (consent traceability under-specified; validation criterion inconsistent with submitted evidence) and one Low finding (`propose()` should explicitly guard against non-`REVIEW` outcomes) addressed at v0.2. v0.2 confirmed by the Engineering Reviewer: "resolves all three substantive v0.1 findings; no blocking findings." One further Low/editorial finding on v0.2 corrected at v0.3. **Programme Sponsor approved v0.3 via `sponsor-decision` at ESR-0027 WP1.** Implemented exactly as scoped - see EBR-0001 EBG-0080 for full implementation detail, commit references and the one genuine defect (an unclosed SQLite connection leak) found and fixed during this package's own required live smoke check.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Storage architecture this package implements the Personal Memory tier of (Sections 6.2, 7.2, 7.3, 7.4). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Consent gate this package's `propose`/`approve`/`deny` mechanism implements the first real instance of (Sections 9.1, 9.2). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0080 (registered by this package). |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status, to record EBG-0080 completion once implemented. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Programme Sponsor approved v0.3 via `sponsor-decision` at ESR-0027 WP1. Implemented exactly as scoped: `jarvis/memory/store.py`, `jarvis/memory/service.py`, `GuardianRuntime` and `stdio_rpc.py` wiring, full test coverage including the REVIEW/DENY/unexpected-ALLOW guard and the pre-existing memory-db test-isolation gap this package's own tests exposed across the rest of `test_stdio_rpc.py`. Live smoke check found and fixed a genuine SQLite connection-leak defect (`PersonalMemoryStore` never closed its connections, causing a Windows file-lock `PermissionError`) - fixed with an explicit `_transaction()` context manager. 282 tests total (was 254), `validate_repository.py` 0 errors. Status Draft to Approved - implemented, version 0.3 to 1.0. |
| 0.3 | 18 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) confirmed v0.2 resolves all three substantive v0.1 findings, no blocking findings, and raised one further Low/editorial finding: Section 11 Risk 4 still referenced "logging output" for the final human decision, stale against v0.2's own durable `consent_decisions` table design. Corrected. Ready for Programme Sponsor approval. |
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Addressed Engineering Reviewer (Codex) findings on v0.1, returned via the bridge: Finding 1 (Medium, consent traceability) - added a durable `consent_decisions` table/`ConsentDecisionRecord`, `approve()`/`deny()` now both produce a durable decision record, `PersonalMemoryRecord.consent_decision_id` references that durable record rather than the transient in-memory pending id. Finding 2 (Medium, validation criterion) - Section 10's "same pre-existing warning count" criterion corrected to disclose and accept this package's own known cross-document Section-reference warnings, matching established project precedent, rather than promising an unchanged count the submitted evidence already contradicted. Finding 3 (Low, consent-bypass guard) - `propose()` now explicitly asserts the Sentinel decision outcome is `REVIEW`, refuses on `DENY`, and refuses rather than silently trusting an unexpected `ALLOW`; new test requirement added. Advisories incorporated as wording strengthening only (no dedicated TrustCategory; single-user consent labelling; encryption-before-production-use expectation). |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0027 WP1, following the Programme Sponsor's "Personal Memory + consent gate" selection and the scope-check finding that no approval workflow exists in code today. Scopes a minimal, single-user consent mechanism (propose/approve/deny) plus a SQLite-backed Personal Memory store with per-item consent traceability, reusing Sentinel's existing `requires_approval` classification path unmodified. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
