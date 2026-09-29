# EIP-ESR0059-010 - Per-Item Memory Revocation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-010 |
| Title | Engineering Implementation Package: WP10 Per-Item Memory Revocation |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP10 |

---

# 2. Purpose

Implements ESR-0059 WP10, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0145, under the Programme Sponsor's standing instruction to proceed with the production code review's action plan.

`PersonalMemoryStore.delete()` has satisfied [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Section 7.4's per-item revocation requirement at the store layer since ESR-0027, but no service method, runtime method, RPC method, Tauri command or UXP control reached it: a user could not withdraw a single retained memory from the product.

---

# 3. Repository Context Investigated

* `jarvis/memory/store.py` `delete()` - returned nothing, so an unknown id could not be told apart from a real deletion.
* `memory.list` RPC existed with no Tauri command or UXP use; the Memory Management panel (EBG-0131) deliberately showed only a record count, never content.
* `src/MemoryManagementPanel.jsx` restore flow - an inline "cannot be undone" confirmation step, reused here.
* `jarvis/interfaces/activity_tracker.py` `METHOD_CLUSTERS` - a test requires it to cover every dispatched RPC method.

---

# 4. Scope

## 4A. Backend

* `PersonalMemoryStore.delete()` returns whether a record was deleted.
* `PersonalMemoryService.delete(record_id)` raises `KeyError` for an unknown id, keeps the approving consent decision as audit history, and logs the revocation by id only - never content. **Deliberately not gated by Sentinel policy**: revocation only removes the user's own data, and no policy should be able to stop a user withdrawing something they chose to retain.
* `GuardianRuntime.delete_memory()` with the usual connected/running checks. Because memory is read fresh every turn, a revoked memory stops reaching conversations immediately.
* `memory.delete` RPC (`params.recordId`), mapped in `METHOD_CLUSTERS`.

## 4B. Tauri and UXP

* New Tauri commands `list_memory` (`memory.list`) and `delete_memory` (`memory.delete`), both async per WP1.
* Memory Management panel: stored memories are listed only after the user clicks "Show memories" - the count-only default is kept, so memory text is never on screen unasked. Each memory has a "Delete..." button leading to an inline "Delete this memory? This cannot be undone." confirmation. After a delete, the list and count are re-read from the backend rather than updated optimistically.

## 4C. Tests

* New `jarvis/tests/test_memory_revocation.py`: store reports whether it deleted; service deletes only the named memory and keeps its consent record; unknown id is an error; a revoked memory disappears from the very next turn's `memory_notes`; `memory.delete` over RPC updates list and count; missing, empty or non-string ids rejected; unknown id is an RPC error.
* Playwright (3 new, 26 total): memory text hidden until the list is opened; delete requires confirmation, then removes the memory and updates the count; cancelling leaves it in place. The mock mirrors the backend, including the unknown-id error.

## 4D. Explicitly out of scope

* Bulk deletion, editing a memory, and undo.
* Deleting consent decision history - retained by design.
* Profile-scoped memory (EBG-0132).

## 4E. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: the delete runs inside the store's transaction and reports the real row count; the revocation log line carries the id only; memory content is rendered through React text nodes, never as HTML, so stored text cannot inject markup into the panel; both new Tauri commands go through `call_backend_off_main_thread()`, so neither blocks the window; `memory.delete` runs inline on the RPC main thread (it is not a slow method), and SQLite serialises it against a conversation turn reading memory on the worker; the not-gated-by-Sentinel decision is stated in the code and the EIP rather than implied. No change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`, `cargo clippy -- -D warnings`, `cargo fmt --check`, `npm run build`, `npx playwright test`.
* **Live check against the real backend process**: a memory proposed and approved over RPC was listed, deleted, then absent from both `memory.list` and `memory.status`; deleting it again returned a clear "No stored memory found" error; `backend.log` recorded the revocation by id only.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* A user can see and delete an individual stored memory from the app, after an explicit confirmation.
* A deleted memory never reaches another conversation turn.
* Memory text is not shown unless the user asks for it.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4E (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP10 draft. Per-item memory revocation from store to UXP: `memory.delete` RPC, `list_memory`/`delete_memory` Tauri commands, a hidden-by-default list with confirmed per-item delete in the Memory Management panel. pytest 707 passed/1 skipped, Playwright 26/26, ruff/clippy/fmt/build clean. Live-checked through the real backend process. Not yet reviewed, approved or committed. |
