# EIP-ESR0058-002 - BRD-0001 Recovery Implementation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0058-002 |
| Title | Engineering Implementation Package: WP3 BRD-0001 Recovery Implementation |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0058 |
| Work Package | WP3 |

---

# 2. Purpose

Implements ESR-0058 WP3, resolving the recovery half of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023 that [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] Section 6 explicitly deferred at ESR-0057 WP2 ("not implemented by this artefact's first increment"). Programme Sponsor-selected as WP3, the natural continuation of WP2's own export/backup delivery.

---

# 3. Repository Context Investigated

* [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] Section 6 - the exact three minimum requirements this implementation must satisfy: structural validation before any write; consent-decision rows inserted before dependent content rows; explicit confirmation before overwriting non-empty data.
* `jarvis/memory/store.py`, `jarvis/memory/service.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py` - the existing export/backup implementation from WP2, followed as the direct structural counterpart (mirrored method placement, boundary-check pattern, RPC method naming).
* `PersonalMemoryStore.export_snapshot()`'s actual return shape (tuples of dicts) - confirmed during implementation that `import_snapshot()`'s structural validation needed to accept both tuples (export_snapshot's direct return) and lists (a JSON-decoded backup file's arrays), not lists alone; a real gap caught by the store-level tests before the RPC layer was touched.

---

# 4. Scope

## 4A. Implement recovery

* `PersonalMemoryStore.import_snapshot(snapshot, confirm_overwrite=False) -> int` (`jarvis/memory/store.py`) - validates structure (required keys/fields; every `personal_memory` row's `consent_decision_id` present among the snapshot's own `consent_decisions`) before any write; refuses non-empty-store restore without `confirm_overwrite=True`; wipe-then-replace (delete existing rows, then insert consent_decisions before personal_memory, all in one transaction).
* `PersonalMemoryService.restore_backup(backup_path, confirm_overwrite=False) -> int` (`jarvis/memory/service.py`) - reads/JSON-parses the backup file, delegates to `import_snapshot()`.
* `GuardianRuntime.restore_memory(backup_path, confirm_overwrite=False) -> int` (`jarvis/guardian/runtime.py`) - same connected-service/running-state boundary checks as every other memory method.
* `memory.restore` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`) - `params.backupPath` (required string), `params.confirmOverwrite` (optional bool, default `false`); returns `{"recordCount": N}`.
* `jarvis/interfaces/activity_tracker.py`: `memory.restore` added to `METHOD_CLUSTERS` - the same gap class WP2 found, caught this time before the full-suite run rather than by it.

## 4B. Tests

New tests in `jarvis/tests/test_memory_store.py` (6: round trip, refuse-without-confirmation, overwrite-when-confirmed, malformed-snapshot rejection, unknown-decision-reference rejection, empty-store-needs-no-confirmation), `test_memory_service.py` (2: file round trip, refuse-without-confirmation), `test_guardian_runtime.py` (restore wired into the existing delegate test plus a new no-service-raises test and two boundary-check additions), `test_stdio_rpc.py` (3: full round trip through two independent servers, refuse-non-empty, reject-non-string-path).

## 4C. Documentation

[[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] Section 6 updated from "not implemented" to record delivery; new Section 8A documents exactly what this slice delivers and what remains deferred (merge/append semantics, UXP surface, Session/Shared-Family coverage, cross-device restore).

## 4D. Explicitly out of scope

* Merge/append restore semantics - wipe-then-replace only. Reconciling a restored snapshot against a live store's own newer data is a materially harder problem (conflict resolution, which record "wins"), deliberately deferred rather than attempted informally.
* Encryption at rest - BRD-0001 Section 7's own disclosed open gap, unchanged by this Work Package.
* Any UXP (`src/`/`src-tauri/`) surface - RPC-only, matching WP2's own precedent.
* Session/Shared-Family Memory tier coverage - neither tier exists yet.
* Cross-device restore - DRA-0001's own future scope; this restores a device's own prior backup, not another device's state.

---

# 5. Validation Requirements

* `python -m pytest jarvis/tests scripts/tests -q` - full suite.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* A backup file produced by `memory.backup` round-trips correctly through `memory.restore` into a genuinely separate, empty store.
* Restoring into a non-empty store without `confirmOverwrite: true` refuses, leaving existing data untouched.
* A malformed or structurally-inconsistent backup file is rejected before any write.
* Full test suite passes; `validate_repository.py` remains clean.
* BRD-0001 accurately reflects both increments now delivered.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary directly. Implemented exactly as drafted at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 16 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation, routed through the real bridge (`ESR-0058`/`WP3`) - **Pass**: independently traced (not merely read) all three BRD-0001 Section 6 requirements in `import_snapshot()`; confirmed `confirmOverwrite` defaults `False` at the RPC layer independently of the store/service defaults; re-ran the full test suite (574 passed/1 skipped) and `validate_repository.py` (0 errors) independently. Real finding: `submit-to-review`'s `--files` argument only listed 7 of the 14 actually-touched files (test/governance files omitted) - reviewed the unlisted diffs anyway and judged them benign, not a Fail trigger, but flagged `files_in_scope` should be complete going forward. Not yet approved or implemented/committed. |
| 0.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP3 draft. Recovery implemented and tested (574 passed/1 skipped, up from 562). Drafted directly against the working tree, same disclosed process note as prior Work Packages this session - the real `submit-response`/Sponsor Approval Service gate still governs the actual commit. Not yet reviewed, approved or implemented/committed. |
