# EIP-ESR0057-002 - BRD-0001 Guidance and Personal Memory Export

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0057-002 |
| Title | Engineering Implementation Package: WP2 BRD-0001 Guidance and Personal Memory Export |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0057 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0057 WP2, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023 (Backup, Recovery and Data Protection Guidance).

EBG-0023 as registered authorises guidance/architecture-definition only ("No implementation is authorised by this promotion"), matching the shape of MDS-0001/GAM-0001/DRA-0001. Flagged to the Programme Sponsor before drafting: scoping WP2 to guidance alone would make this the second documentation-only Work Package this session (after WP1), leaving the session without the product-moving work PBK-0001's Feature-First Delivery Discipline requires. The Programme Sponsor directed extending WP2's scope to include a first concrete implementation slice alongside the guidance document - a disclosed scope extension, approved before implementation began, not silently absorbed.

---

# 3. Repository Context Investigated

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023's full registered text and its stated prerequisite (EBG-0019/MDS-0001, Complete).
* [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Section 9 (Relationship to EBG-0023) and Section 10 (Explicit Non-Goals) - the exact gate and boundary this guidance had to respect: preserve personal/shared-family partitioning (Section 7.2) and per-item consent traceability (Section 7.4), never define schema/migration/persistence code itself.
* `jarvis/memory/store.py`, `jarvis/memory/service.py` - the real `PersonalMemoryStore`/`PersonalMemoryService` implementation (two SQLite tables: `personal_memory`, `consent_decisions`), confirming there is no existing export/backup capability to extend rather than duplicate.
* `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py` - the existing `memory.propose`/`memory.approve`/`memory.deny`/`memory.list` RPC method pattern, followed exactly for the new `memory.backup` method (same handler-delegates-to-runtime-delegates-to-service shape, same boundary-check pattern via `_require_memory_service()`).
* `jarvis/interfaces/activity_tracker.py` - `METHOD_CLUSTERS`, which a full-suite test run confirmed requires every dispatched RPC method to be classified; `memory.backup` added to the `jarvis` cluster alongside the other three memory methods.

---

# 4. Scope

## 4A. Create BRD-0001 (Draft)

New Model-category artefact, `aiems/models/BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE.md`, parented to MDS-0001. Defines: relationship to DRA-0001 (adjacent, distinct - device-restore versus same-device backup protection); backup expectations (export tables together, never content without consent-decision rows; full point-in-time only, no incremental requirement); recovery expectations (explicitly not delivered this increment; minimum future requirements stated); data-protection principles (local-only; encryption-at-rest disclosed as an open gap, not assumed; no retention schedule mandated); and Section 8 recording exactly what this Work Package's own code delivers and does not.

## 4B. Implement the first concrete slice

* `PersonalMemoryStore.export_snapshot()` (`jarvis/memory/store.py`) - returns every row of both `personal_memory` and `consent_decisions` as plain dicts, in one read.
* `PersonalMemoryService.export_backup(backup_dir: Path) -> Path` (`jarvis/memory/service.py`) - writes a timestamped JSON file (`personal_memory_backup_<UTC timestamp>.json`), creating `backup_dir` if absent.
* `GuardianRuntime.backup_memory(backup_dir: Path) -> Path` (`jarvis/guardian/runtime.py`) - same connected-service/running-state boundary checks (`_require_memory_service()`) as every other memory method.
* `memory.backup` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`) - `params.backupDir` optionally overrides `JARVIS_MEMORY_BACKUP_DIR` (new env var, default `~/.jarvis/memory/backups`); returns `{"path": "..."}`.
* `activity_tracker.py` `METHOD_CLUSTERS["memory.backup"] = "jarvis"` - required for `test_method_clusters_covers_every_dispatched_rpc_method` to keep passing; a real defect this Work Package's own change would otherwise have introduced, caught by running the full suite rather than only the new tests.

## 4C. Tests

New tests in `jarvis/tests/test_memory_store.py` (export_snapshot, 3 cases), `test_memory_service.py` (export_backup, 3 cases), `test_guardian_runtime.py` (backup_memory wired into the existing no-service/not-running/delegates/refuse-before-start/refuse-after-stop test set, 5 call sites), `test_stdio_rpc.py` (memory.backup round-trip through the real server, plus a type-validation case).

## 4D. Documentation debt sync

MDS-0001 Sections 9/10/11 and Related Artefacts repointed from the bare "EBG-0023" name to the real BRD-0001 artefact, matching the precedent already set for DRA-0001/EBG-0046 at ESR-0056 WP3. Whole-Document Staleness Sweep on Edit (PBK-0001), triggered by opening MDS-0001 for that fix: OSE Relationships' `RBL-0015` "current accepted repository baseline" reference, stale since ESR-0028, corrected to RBL-0036.

## 4E. Explicitly out of scope

* Recovery/restore/import from a backup file - BRD-0001 Section 6 states the minimum future requirements; none are built here.
* Encryption at rest - BRD-0001 Section 7 discloses this as an open gap.
* Session/Shared-Family Memory tier coverage - neither tier is implemented yet; nothing exists there to back up.
* Any UXP (`src/`/`src-tauri/`) surface - RPC-only this increment, matching PBK-0001's "backend capability a future UXP increment will depend on" allowance.
* Any scheduling or automation of backup invocation - human/caller-triggered only.

---

# 5. Validation Requirements

* `python -m pytest jarvis/tests scripts/tests -q` - full suite, not only the new tests (the `activity_tracker` cluster-coverage defect above was only caught this way).
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* BRD-0001 exists, registered in REG-0001, resolving EBG-0023 Complete in EBR-0001.
* `memory.backup` round-trips through the real `StdioRpcServer` in a test, writing a file containing both `personal_memory` and `consent_decisions` rows.
* Full test suite passes (561 passed, 1 skipped at drafting time, prior to this increment's own additions).
* `validate_repository.py` remains clean.
* MDS-0001's EBG-0023 forward references no longer point to a bare backlog ID once a real artefact exists.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 14 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary and diff directly, in place of independent AI review given Codex/Antigravity both unavailable. Implemented exactly as drafted at v0.1 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.1 | 14 September 2026 | Claude Engineering Implementer | ESR-0057 WP2 draft. BRD-0001 created; Personal Memory export/backup slice implemented and tested (drafted directly against the working tree, same disclosed process note as WP1 - the real `submit-response`/Sponsor Approval Service gate still governs the actual commit). Codex is retired (cost); a genuine Antigravity CLI substitute for independent review remains blocked by Claude Code's own harness (Create Unsafe Agents; Self-Modification), per EBG-0126. Not yet reviewed, approved, or implemented/committed. |
