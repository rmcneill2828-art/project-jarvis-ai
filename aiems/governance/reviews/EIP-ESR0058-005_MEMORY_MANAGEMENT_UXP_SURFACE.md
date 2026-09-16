# EIP-ESR0058-005 - Memory Management UXP Surface

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0058-005 |
| Title | Engineering Implementation Package: WP6 Memory Management UXP Surface |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0058 |
| Work Package | WP6 |

---

# 2. Purpose

Implements ESR-0058 WP6, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0131: a bounded backup/restore UI in the actual desktop app, closing the "RPC-only, no UXP surface" gap [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] disclosed at both prior increments (ESR-0057 WP2, ESR-0058 WP3) and independently flagged by the GitHub Copilot CLI gap analysis.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py` - confirmed `memory.backup`/`memory.restore` exist and are reachable only through the RPC layer; no Tauri command or `src/` UI calls either.
* `src-tauri/src/lib.rs` - the existing `#[tauri::command]`/`call_backend()` pattern every command follows, followed exactly for the three new commands.
* `src/AgentFrameworkPanel.jsx` - the existing dedicated-panel-file pattern (a plain function component fed pre-fetched state and callback props from `App.jsx`, reusing `.metrics-list`/`.metric-row`/`.outline-action`/`.panel-status-message` classes) - followed exactly for the new panel, no new metric-rendering CSS beyond what the two new interactive elements genuinely need.
* `jarvis/memory/store.py` `export_backup()`/`import_snapshot()` - confirmed the backend always names the backup file itself (a timestamped filename inside whatever directory it is given) and has no exact-filename parameter. This ruled out a save-file dialog for backup (it would let the user pick a filename the backend then silently ignores) in favour of a folder picker.
* `jarvis/memory/store.py` `import_snapshot()`'s `confirm_overwrite` gate - the exact refusal message text (`"...Pass confirm_overwrite=True to proceed..."`) confirmed stable enough to detect from the frontend, so the panel can turn a real backend refusal into an inline confirmation step rather than requiring the user to already know the store is non-empty before trying.
* `tests/e2e/app.spec.js` - confirmed `@tauri-apps/plugin-dialog`'s `open()` calls the same `@tauri-apps/api/core` `invoke()` (`plugin:dialog|open`) that every existing mocked Tauri command already goes through - no separate mocking mechanism needed, only new command branches in the existing mock.
* Network access to crates.io confirmed live (`cargo add --dry-run`) before committing to `tauri-plugin-dialog` as a new Rust dependency.

---

# 4. Scope

## 4A. Backend: a lightweight status query

* `PersonalMemoryStore.count()` (`jarvis/memory/store.py`) - a dedicated `SELECT COUNT(*)` query, not `len(list_all())`: the backup/restore panel only ever needs a number, and pulling every record's real content across the RPC boundary merely to display a count would be a needless privacy exposure for what this surface actually shows.
* `PersonalMemoryService.record_count()`, `GuardianRuntime.memory_status()` - same layering and connected-service/running-state boundary checks as every other memory method.
* `memory.status` JSON-RPC method (`jarvis/interfaces/stdio_rpc.py`) - returns `{"recordCount": N}` only.
* `jarvis/interfaces/activity_tracker.py`: `memory.status` added to `METHOD_CLUSTERS` proactively (an enforced completeness test - `test_activity_tracker.py` - would otherwise fail).

## 4B. Tauri command surface

* `memory_status`, `backup_memory`, `restore_memory` (`src-tauri/src/lib.rs`) - thin `call_backend()` wrappers over `memory.status`/`memory.backup`/`memory.restore`.
* New dependency: `tauri-plugin-dialog` (Rust, `Cargo.toml`) / `@tauri-apps/plugin-dialog` (JS, `package.json`) - the official Tauri v2 native file/folder dialog plugin. `dialog:default` added to `src-tauri/capabilities/default.json`.

## 4C. UXP panel

* `src/MemoryManagementPanel.jsx` (new): shows the live stored-record count; a "Back Up..." button opening a native **folder** picker (not a save-file picker, per the 4A backend constraint above) then calling `backup_memory`; a "Restore..." button opening a native **file** picker (`.json` filter) then calling `restore_memory`.
* **Restore confirmation flow**: the panel always calls `restore_memory` with `confirmOverwrite: false` first. A non-empty-store refusal (detected by matching the backend's own distinctive error text) surfaces an inline "this will permanently overwrite N existing memories" confirmation with Overwrite/Cancel buttons; only an explicit Overwrite retries with `confirmOverwrite: true`. An empty store restores immediately. This mirrors, rather than works around, the backend's own "recovery never runs silently" guarantee (BRD-0001 Section 6).
* Wired into `App.jsx`'s existing side-column alongside `AgentFrameworkPanel`/`DiagnosticsPanel`; `memory_status` fetched on mount in the same effect as `list_agents`/`list_profiles`; a `refreshMemoryStatus()` re-fetch runs after a successful restore rather than trusting the restore response's own count as a permanent proxy for the store's total.
* `src/styles.css`: `.memory-management-panel` added alongside the existing shared sidebar-panel selector groups; `.memory-action-row`/`.memory-overwrite-confirm` new, reusing `.outline-action`/`.conversation-error` for the buttons and the warning text.

## 4D. Tests

* Python: `test_count_empty_store`/`test_count_reflects_stored_records` (`test_memory_store.py`); `test_record_count_delegates_to_store` (`test_memory_service.py`); `memory_status()` added to the existing without-service/before-start/after-stop boundary-check tests plus a delegation assertion in the connected-service round-trip test (`test_guardian_runtime.py`); `test_memory_status_reports_record_count` (`test_stdio_rpc.py`, also confirms no record content leaks into the response).
* Rust: `cargo test`/`cargo clippy -- -D warnings`/`cargo fmt --check` all re-run clean against the new commands (no new Rust unit tests - the three new commands are thin wrappers with no branching logic of their own, matching every existing command's own test coverage, all of which rely on the shared `call_backend()`/`dispatch_line()` tests already covering the transport).
* Playwright: 5 new tests in `tests/e2e/app.spec.js` - status display, backup success, restore-into-empty-store (immediate success), restore-into-non-empty-store (confirmation required, then Overwrite succeeds), cancelling the confirmation (state unchanged). `mockTauriIpc()` extended with `memoryRecordCount`/`dialogOpenResult`/`backupMemoryResult`/`restoreMemoryResult` options and a stateful mock of `plugin:dialog|open`/`memory_status`/`backup_memory`/`restore_memory`, including a mocked non-empty-store refusal that mirrors the real backend's exact error text.

## 4E. Documentation

* [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] new Section 8B records this slice; Sections 8/8A's "a UXP surface" exclusion sentences corrected (Documentation Debt Discipline, Whole-Document Staleness Sweep on Edit).
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0131 closed Complete.

## 4F. Explicitly out of scope

* Encryption at rest (BRD-0001 Section 7, still an open, disclosed gap).
* A memory *content* browser/editor - the panel shows a count only, never record content; deliberately narrower than what `memory.list()` could technically provide.
* Scheduled/automatic backup - still human-triggered only, matching BRD-0001 Section 7's "no retention schedule" note.
* Session/Shared-Family tier coverage, cross-device restore, and merge/append restore semantics - all remain exactly as scoped out at the prior two BRD-0001 increments; nothing about wipe-then-replace restore changes here.

---

# 5. Validation Requirements

* `python -m pytest jarvis/tests scripts/tests -q` - full suite.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* `npx playwright test` - full suite including the 5 new tests, run at least twice at default parallelism.
* `cargo build`/`cargo test`/`cargo clippy -- -D warnings`/`cargo fmt --check` (all `--manifest-path src-tauri/Cargo.toml`, matching CI exactly) - all clean.
* `npm run build` - production frontend build succeeds with the new dependency.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* A household member can back up and restore Personal Memory entirely from the app, with no RPC call or terminal needed.
* Restoring into a non-empty store always requires an explicit, informed confirmation naming the real record count that would be overwritten - never a silent or generic confirmation.
* The panel shows a record count only, never record content.
* Full Python, Rust, and Playwright suites pass; `validate_repository.py` remains clean; `npm run build` succeeds.
* EBG-0131 closed Complete; BRD-0001's stale "no UXP surface" claims corrected.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary directly. Implemented exactly as drafted at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 16 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation routed through the real bridge (`ESR-0058`/`WP6`, complete 24-file `files_in_scope`) - **Pass**, single clean `return-findings` entry, independently verified against the transcript (`repository_ref: 636e744...` matching HEAD exactly). Confirmed `memory.status` never leaks record content (traced the dedicated `COUNT(*)` query and the RPC response shape, plus the explicit test assertion); confirmed the three Tauri commands are pure passthroughs; traced the exact restore-refusal string match between backend and frontend; independently ran `cargo build`/`test`/`clippy -D warnings`/`fmt --check`, `npm run build`, and `npx playwright test` (23/23) itself; confirmed the exact 24-file scope; confirmed the self-caught `replace_all` fix left EBR-0001's version history clean with no duplicate rows. Re-ran `pytest` (587 passed/1 skipped) and `validate_repository.py` (0 errors, 333 warnings) independently, both matching. Not yet approved or committed. |
| 0.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP6 draft. Memory Management UXP surface implemented and verified directly against the working tree: full Python suite (587 passed/1 skipped), Playwright (23/23, run twice at default parallelism), `cargo build`/`test`/`clippy -D warnings`/`fmt --check` (all clean), `npm run build` (clean), `validate_repository.py` (0 errors). Not yet reviewed, approved, or committed. |
