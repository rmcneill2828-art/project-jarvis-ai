# BRD-0001 - Backup, Recovery and Data Protection Guidance

---

# 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | BRD-0001 |
| Title | Backup, Recovery and Data Protection Guidance |
| Version | 1.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] |

---

# 2. Purpose

BRD-0001 defines backup, recovery and data-protection expectations for Project JARVIS AI's locally-held data, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023 (Backup, Recovery and Data Protection Guidance).

[[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Section 9 explicitly reserves this scope, gating EBG-0023 on MDS-0001 existing first: MDS-0001 defines the data architecture (personal/shared-family partitioning, per-item consent traceability) that a backup/recovery mechanism must preserve, not flatten, but does not itself define backup schedules, recovery procedures or data-protection operational policy. This artefact is that follow-on.

---

# 3. Scope

## In Scope

- Backup, recovery and data-protection expectations for data MDS-0001 architects: today, the Personal Memory tier (`jarvis/memory/`, implemented ESR-0027).
- The relationship between this guidance and [[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]]'s device-restore scope.
- Recording what this session's own concrete delivery (Section 6) does and does not cover, disclosed rather than left to be inferred from the code.

## Out of Scope

- Session Memory and Shared-Family Memory tiers (MDS-0001 Sections 6.1/6.3) - not yet implemented, so nothing exists there to back up. This guidance's partitioning-preservation principle (Section 5) applies to them once built; their own backup mechanics are future work.
- The AIEMS Knowledge Capability's own storage (repository-backed, already covered by Git itself as its backup mechanism).
- Selecting or implementing any cloud, remote or networked backup destination - explicitly out of scope while [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] remains an approved specification with no network-facing interface built.
- Restore/import from a backup file - a future increment, not delivered by this artefact's own first implementation slice (Section 6).

---

# 4. Relationship to DRA-0001

[[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]] and BRD-0001 cover adjacent but distinct concerns, and neither substitutes for the other:

- **DRA-0001** answers "how does a *new device* obtain existing state" - device registry, bootstrap, sync protocol, progressive restore. Its restore path assumes a source device or sync peer already holding current state.
- **BRD-0001** answers "how is *existing* state protected against loss on the device that already holds it" - point-in-time export copies, independent of any second device or sync relationship.

A future DRA-0001 implementation could reasonably read a BRD-0001 backup file as one possible restore source, but that integration is not assumed or designed here - each artefact's own scope stands independently.

---

# 5. Backup Expectations

Any backup mechanism for MDS-0001-architected data shall:

- Export every table a given memory tier's store owns together, in one atomic snapshot - never content records without their corresponding consent-decision records, which would silently discard MDS-0001 Section 7.4's per-item consent traceability on export.
- Preserve MDS-0001 Section 7.2's personal/shared-family partitioning once Shared-Family Memory exists - a shared backup mechanism must not merge tiers a live query would keep separate.
- Be a full point-in-time export by default. Incremental/differential backup is not required by this guidance and is not delivered by Section 6's implementation - a candidate future refinement once backup file volume or frequency makes full exports impractical.
- Write to local filesystem storage only, until a future Engineering Session actually builds a network-facing surface under [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] and a corresponding decision extends this guidance to cover it.

---

# 6. Recovery Expectations

Recovery (restoring a memory tier's store from a backup file) was **not implemented** by this artefact's first increment (Section 8), and is now delivered by its second (Section 8A), satisfying all three minimum requirements below:

- Validate a backup file's structure before writing anything to a live store - a malformed or truncated backup must fail closed, not partially import.
- Re-establish consent-decision rows before any dependent content row, mirroring `PersonalMemoryStore.add()`'s own existing insert-order constraint (a content record already refuses to insert without a prior approved decision row present).
- Require explicit human confirmation before overwriting a non-empty live store - recovery is a destructive operation by nature and shall never run silently or automatically.

---

# 7. Data Protection Principles

- **Local-only, matching the source data's own trust boundary.** A backup file lives under the same local-filesystem trust boundary as the SQLite database it was exported from; this guidance does not claim a stronger protection posture for the copy than the original already has.
- **Encryption at rest is an open gap, disclosed rather than assumed.** Section 8's implementation writes plaintext JSON, identical in this respect to the plaintext SQLite database it exports from. Neither is encrypted today. A future increment should evaluate whether backup files specifically (which are more portable/copyable than a live database file) warrant encryption-at-rest before this guidance is considered complete, particularly once Shared-Family data exists.
- **No retention schedule is defined.** This guidance does not mandate how many backup files should be kept, for how long, or on what cadence - a human-triggered, on-demand export (Section 8) has no automatic accumulation to manage. A scheduled/automated backup capability, if built, would need its own retention policy.

---

# 8. First Concrete Implementation Slice (ESR-0057 WP2)

Delivered against this guidance in the same Work Package that created it, per Programme Sponsor direction to extend EBG-0023's registered guidance-only scope with a first real capability rather than defer all implementation to a later session (disclosed scope extension, Sponsor-approved before implementation):

- `PersonalMemoryStore.export_snapshot()` (`jarvis/memory/store.py`) - returns every row of both `personal_memory` and `consent_decisions`, satisfying Section 5's "export together, never content alone" requirement directly at the storage layer.
- `PersonalMemoryService.export_backup(backup_dir)` (`jarvis/memory/service.py`) - writes a timestamped JSON file (`personal_memory_backup_<UTC timestamp>.json`) to `backup_dir`, creating it if absent.
- `GuardianRuntime.backup_memory(backup_dir)` (`jarvis/guardian/runtime.py`) - delegates with the same connected-service/running-state boundary checks as every other memory method.
- `memory.backup` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`) - `params.backupDir` optionally overrides the default location (`JARVIS_MEMORY_BACKUP_DIR` env var, else `~/.jarvis/memory/backups`); returns `{"path": "..."}`.

**Explicitly not delivered by this slice**: recovery/restore/import (Section 6, delivered by the second slice, Section 8A); encryption at rest (Section 7); a UXP surface (no `src/`/`src-tauri/` change at this slice - reachable only via direct RPC call at the time, matching PBK-0001's "backend capability a future UXP increment will depend on" allowance; a UXP surface was delivered at the third slice, Section 8B); Session/Shared-Family tier coverage (neither tier is built yet); any scheduling or automation of backup invocation.

---

# 8A. Second Concrete Implementation Slice - Recovery (ESR-0058 WP3)

Delivers Section 6's recovery expectations in full:

- `PersonalMemoryStore.import_snapshot(snapshot, confirm_overwrite=False)` (`jarvis/memory/store.py`) - validates the snapshot's structure (required keys and fields present; every `personal_memory` row's `consent_decision_id` must reference a `consent_decisions` row within the same snapshot) before writing anything; inserts `consent_decisions` rows before their dependent `personal_memory` rows, in the same transaction; refuses (raises `ValueError`) if the store already holds data unless `confirm_overwrite=True` is passed explicitly. Restore is wipe-then-replace, not merge - a non-empty store's existing rows are deleted before the snapshot is written, never combined with it (a deliberate scope limit, disclosed below).
- `PersonalMemoryService.restore_backup(backup_path, confirm_overwrite=False)` (`jarvis/memory/service.py`) - reads and JSON-parses the backup file (a malformed/missing file fails closed before any store write), delegates to `import_snapshot()`.
- `GuardianRuntime.restore_memory(backup_path, confirm_overwrite=False)` (`jarvis/guardian/runtime.py`) - same connected-service/running-state boundary checks as every other memory method.
- `memory.restore` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`) - `params.backupPath` (required), `params.confirmOverwrite` (optional, defaults `false` - a caller must pass it explicitly `true` to overwrite non-empty data, matching Section 6's "never runs silently" requirement); returns `{"recordCount": N}`.

**Explicitly not delivered by this slice**: merge/append semantics (restore is wipe-then-replace only - reconciling a restored snapshot against a live store's own newer data is a materially harder problem, deliberately deferred rather than attempted informally); a UXP surface (RPC-only at this slice, same allowance as Section 8; delivered at the third slice, Section 8B); Session/Shared-Family tier coverage; cross-device restore (DRA-0001's own future scope, per Section 4 - this restores a device's own prior backup, not another device's state).

---

# 8B. Third Concrete Implementation Slice - UXP Surface (ESR-0058 WP6)

Delivers a bounded Memory Management panel in the actual desktop app, closing the "RPC-only, no UXP surface" gap disclosed in Sections 8 and 8A and independently flagged by the GitHub Copilot CLI gap analysis (EBG-0131):

- `memory.status` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`, backed by a new `PersonalMemoryStore.count()`/`PersonalMemoryService.record_count()`/`GuardianRuntime.memory_status()` layered chain) - returns `{"recordCount": N}` only, a dedicated `COUNT(*)` query rather than reusing `memory.list()`'s full-content response merely to display a badge.
- `memory_status`, `backup_memory`, `restore_memory` Tauri commands (`src-tauri/src/lib.rs`) - thin wrappers over the existing `memory.status`/`memory.backup`/`memory.restore` RPC methods, following the same `call_backend()` pattern as every other command.
- `src/MemoryManagementPanel.jsx` (new) - a sidebar panel showing the live stored-record count, a "Back Up..." button (native folder picker via the newly-added `tauri-plugin-dialog`, since the backend always names the backup file itself - offering an exact filename the backend would then ignore would be misleading), and a "Restore..." button (native file picker, `.json` filter).
- **Restore retains the backend's "never runs silently" guarantee rather than working around it**: the panel always attempts restore with `confirmOverwrite: false` first; a non-empty store's refusal (a distinctive error string) is recognised and turned into an explicit inline confirmation step ("This will permanently overwrite N existing memories") before retrying with `confirmOverwrite: true`. An empty store restores immediately, with nothing to overwrite.
- New dependency: `tauri-plugin-dialog` (Rust) / `@tauri-apps/plugin-dialog` (JS), the official Tauri v2 native file/folder dialog plugin; `dialog:default` added to `src-tauri/capabilities/default.json`.

**Explicitly not delivered by this slice**: encryption at rest (Section 7, still open); a memory *content* browser (the panel shows a count only, never record content, a deliberate scope narrowing beyond what `memory.list()` could technically provide - see the RPC method's own docstring); scheduled/automatic backup (still human-triggered only); Session/Shared-Family tier coverage; any change to the wipe-then-replace restore semantics established at Section 8A.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Parent artefact; Section 9 gates this artefact's existence and defines the partitioning/consent-traceability this guidance must preserve. |
| [[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]] | Adjacent, distinct scope - device-to-device restore versus same-device backup protection (Section 4). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Defines the consent-gate/authority model whose decisions this guidance's export must preserve traceability for. |
| [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] | Gates any future network-facing backup destination this guidance does not yet cover. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0023, the backlog item this artefact resolves. |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP6: delivers a Memory Management UXP surface (new Section 8B, EBG-0131) - memory.status RPC method, Tauri commands, and src/MemoryManagementPanel.jsx (status display, native folder-picker backup, native file-picker restore with an explicit overwrite-confirmation step). Corrects Sections 8 and 8A's now-stale "a UXP surface" exclusion claims. |
| 1.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP3: delivers Section 6's recovery expectations in full (new Section 8A) - `PersonalMemoryStore.import_snapshot()`, `PersonalMemoryService.restore_backup()`, `GuardianRuntime.restore_memory()`, new `memory.restore` RPC method. Wipe-then-replace semantics only (merge/append explicitly deferred). Section 6 updated from "not implemented" to record delivery. |
| 1.0 | 14 September 2026 | Claude Engineering Implementer | Initial creation, ESR-0057 WP2, resolving EBG-0023. Defines backup/recovery/data-protection guidance for MDS-0001-architected data; delivers a first concrete implementation slice (Personal Memory export/backup only, no recovery) alongside the guidance itself, per Programme Sponsor-approved scope extension. |
