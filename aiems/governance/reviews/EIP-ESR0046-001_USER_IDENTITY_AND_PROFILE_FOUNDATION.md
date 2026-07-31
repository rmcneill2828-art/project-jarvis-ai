# EIP-ESR0046-001 - User Identity and Profile Foundation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0046-001 |
| Artefact ID | EIP-ESR0046-001 |
| Title | User Identity and Profile Foundation |
| Version | 1.0 |
| Status | Approved - implementing |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0116 |
| Intended Session | ESR-0046 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] scored "User Profiles" **Fail** against [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5's explicit MLP 0.1 requirement: "no user identification, login or profile-switching code path exists anywhere under `jarvis/` today." [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 defines a Household Role Model (Administrator/Adult/Child/Guest) but explicitly states (Section 10) that it "does not implement login, identification or access control" - it is a permission taxonomy, not an identity system. Confirmed directly against the live code before drafting (not assumed): `jarvis/memory/store.py`'s schema has no user/owner column at all; `jarvis/guardian/runtime.py`'s `converse()`/`speak()` take no caller identity; `jarvis/interfaces/stdio_rpc.py`'s JSON-RPC protocol reads no session/caller field; `src/App.jsx:288-297` renders a static, non-interactive profile card hardcoding the name "Robert" with no click handler or switching logic. This package closes that gap.

---

# 3. Objective

Implement a local Guardian profile system: create, list and select a profile (display name plus one of GAM-0001 Section 8.1's four household roles), exposed via new JSON-RPC methods and wired into the live UXP, replacing the static placeholder profile card with a real profile picker.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `jarvis/memory/` | Established pattern this package mirrors: a `store.py` (SQLite-backed, `_transaction()` context-manager pattern closing the Windows file-lock leak documented in its own docstring) plus a `service.py` wrapping it with business logic. No existing user/owner concept anywhere in its schema (confirmed by direct read of `store.py`). |
| `jarvis/guardian/runtime.py` `GuardianRuntime.converse(self, message: str)` / `speak(self, text: str)` | Neither method takes any caller/session/profile parameter today (line 160, 189). Not changed by this package - see Section 8 exclusions. |
| `jarvis/interfaces/stdio_rpc.py` `StdioRpcServer._methods` | Dict-based JSON-RPC method registry (line 281): `guardian.converse`, `guardian.speak`, `platform.status`, `knowledge.graph`, `memory.propose`, `memory.approve`, `memory.deny`, `memory.list`, `gia.status`. New `profile.*` entries follow this exact pattern. |
| `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` | Constructs `memory_store`/`memory_service` from `MEMORY_DB_PATH_ENV_VAR` (`JARVIS_MEMORY_DB_PATH`, default `Path.home() / ".jarvis" / "memory" / "personal.db"`, line 103-104, 232-233) - the exact pattern this package's `JARVIS_IDENTITY_DB_PATH` / `ProfileStore` construction mirrors. |
| `src-tauri/src/lib.rs` | `send_message`/`platform_status`/`knowledge_graph` are thin `#[tauri::command]` wrappers around a shared `call_backend(state, app_handle, method, params)` helper - new `list_profiles`/`create_profile`/`select_profile`/`active_profile` commands follow this exact pattern. |
| `src/App.jsx:288-297` | Static `<section className="profile-card">` hardcoding `<strong>Robert</strong>` / "Signed in locally", with an unwired `ChevronDown` icon suggesting an intended but never implemented dropdown. This package makes it real. |
| GAM-0001 Section 8.1 | Four roles only, no credential/authentication field: Administrator (full household authority), Adult (standard authority, may approve `REVIEW`-classified actions), Child (restricted, child-safe boundary, cannot approve `REVIEW`-classified actions), Guest (minimal, Autonomous-tier only, no shared-memory or approval access). This package's `Profile.role` is validated against exactly these four values. |

---

# 5. Scope

This package authorises, across three layers:

## 5.1 Backend - new `jarvis/identity/` module

1. `jarvis/identity/store.py` (new): `ProfileRecord` dataclass (`id`, `display_name`, `role`, `created_at`) with `__post_init__` validation restricting `role` to exactly GAM-0001 Section 8.1's four values (`Administrator`, `Adult`, `Child`, `Guest`), mirroring `ConsentDecisionRecord`'s existing validation pattern in `jarvis/memory/store.py`. `ProfileStore` (SQLite-backed, reusing the identical `_transaction()` context-manager pattern from `jarvis/memory/store.py` to avoid the same Windows file-lock leak that pattern was written to fix): `create(record) -> ProfileRecord`, `list_all() -> tuple[ProfileRecord, ...]`, `get(profile_id) -> ProfileRecord | None`. A second single-row table, `active_profile (id INTEGER PRIMARY KEY CHECK (id = 1), profile_id TEXT NOT NULL)`, persists the current selection across process restarts; `ProfileStore.set_active(profile_id)` / `get_active() -> ProfileRecord | None` (`None` when no profile has ever been selected, or when the previously-active profile has since been deleted - deletion is not authorised by this package, so the latter case is defensive only).
2. `jarvis/identity/service.py` (new): `ProfileService` wrapping `ProfileStore` - `create_profile(display_name, role) -> ProfileRecord`, `list_profiles() -> tuple[ProfileRecord, ...]`, `select_profile(profile_id) -> ProfileRecord` (raises `ValueError` if `profile_id` does not exist, mirroring `PersonalMemoryStore.add()`'s existing referential-integrity check), `active_profile() -> ProfileRecord | None`.
3. `jarvis/interfaces/stdio_rpc.py`: add `IDENTITY_DB_PATH_ENV_VAR = "JARVIS_IDENTITY_DB_PATH"`, `DEFAULT_IDENTITY_DB_PATH = Path.home() / ".jarvis" / "identity" / "profiles.db"`, mirroring the memory-store env-var/default pattern exactly (lines 103-104). `build_default_runtime()` constructs a `ProfileStore`/`ProfileService` unconditionally (identity storage is always-on local functionality, not a credential-gated external capability - it has no absent-config degraded state to model, unlike a provider or the speech path) and holds the `ProfileService` instance on `StdioRpcServer` (not on `GuardianRuntime` - see Section 8 exclusion 1).
4. Add four entries to `StdioRpcServer._methods`: `"profile.list"`, `"profile.create"`, `"profile.select"`, `"profile.active"`.
5. `_profile_list(params) -> dict`: returns `{"profiles": [{"id", "displayName", "role", "createdAt"} for each]}`.
6. `_profile_create(params) -> dict`: reads `params["displayName"]` (str) and `params["role"]` (str, one of the four GAM-0001 values - `ValueError` surfaced as a JSON-RPC error otherwise, matching `_guardian_converse`'s existing `TypeError`-on-bad-input pattern), calls `service.create_profile(...)`, returns the created profile's serialized shape.
7. `_profile_select(params) -> dict`: reads `params["profileId"]` (str), calls `service.select_profile(...)`, returns the now-active profile's serialized shape (or a JSON-RPC error if the id does not exist).
8. `_profile_active(params) -> dict`: returns `{"profile": <serialized or null>}`.

## 5.2 Tauri Bridge (`src-tauri/src/lib.rs`)

9. Add `list_profiles`, `create_profile(state, app_handle, display_name: String, role: String)`, `select_profile(state, app_handle, profile_id: String)`, `active_profile` - four thin `#[tauri::command]` wrappers around `call_backend`, byte-for-byte the same shape as `send_message`/`platform_status`.
10. Register all four in the existing `tauri::generate_handler![...]` list.

## 5.3 Frontend (`src/App.jsx`)

11. Replace the static `profile-card` section (lines 288-297) with a stateful component: on mount, call `active_profile` and `list_profiles`.
12. If an active profile exists, render its `displayName`/`role` in place of the current hardcoded "Robert" text, with the existing `ChevronDown` now wired to open a picker listing every profile from `list_profiles`; selecting one calls `select_profile` and re-renders.
13. If no active profile exists (first run, or a fresh `identity.db`), render a minimal inline create form (display name text input, role `<select>` constrained to the four GAM-0001 values) calling `create_profile`, then `select_profile` on the newly created id.
14. Any RPC failure (rejected `invoke`, malformed response) surfaces as a small, non-blocking inline note in the profile card, matching the established pattern from `speak_message`'s frontend error handling (EIP-ESR0044-001 Section 5.3 item 11) - not a hard failure of the wider UXP.

## 5.4 Tests

15. New `jarvis/tests/test_identity_store.py`: `ProfileRecord` role validation (accepts all four GAM-0001 values, rejects any other string); `ProfileStore` create/list/get/set_active/get_active round-trips; the Windows-file-lock-safe `_transaction()` pattern is exercised (mirroring `jarvis/tests/test_memory_store.py`'s existing coverage shape).
16. New `jarvis/tests/test_identity_service.py`: `ProfileService.select_profile` raises `ValueError` on an unknown id; `active_profile()` returns `None` before any selection.
17. Extend `jarvis/tests/test_stdio_rpc.py`: `build_default_runtime()` constructs a working `ProfileService` against an injected/temp db path; all four `profile.*` RPC methods return the correct shape, including the create-then-select-then-active round trip and the unknown-id error case.
18. Extend `src-tauri`'s existing test module with tests for the four new commands mirroring `send_message`'s own test pattern, to the same proportionate thinness already applied to `platform_status`/`knowledge_graph` (`call_backend` itself is already well-tested).
19. Extend `tests/e2e/app.spec.js` (or add a new spec): mocks the four new Tauri commands, confirms the create-profile form appears when no active profile exists, and that selecting a profile from the picker calls `select_profile` with the correct id.

---

# 6. Authorised Files

1. `jarvis/identity/__init__.py` (new)
2. `jarvis/identity/store.py` (new)
3. `jarvis/identity/service.py` (new)
4. `jarvis/tests/test_identity_store.py` (new)
5. `jarvis/tests/test_identity_service.py` (new)
6. `jarvis/interfaces/stdio_rpc.py`
7. `jarvis/tests/test_stdio_rpc.py`
8. `src-tauri/src/lib.rs`
9. `src/App.jsx`
10. `tests/e2e/app.spec.js`
11. `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` - recording the role model as now operationally implemented, not only defined.
12. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
13. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
14. `aiems/governance/baselines/LGB-0001_LAUNCH_GAP_BACKLOG.md` - per its own Section 8 maintenance rule, refreshed when a Must-Ship item is delivered.
15. `src/styles.css` - anticipated for the profile picker/create-form styling, matching the disclosed-dependency precedent from EIP-ESR0044-001; confirmed and disclosed at implementation if actually touched.

No other file is authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `ProfileRecord.role` validation happens at the dataclass level (`__post_init__`, raising `ValueError`), not only at the RPC boundary - matching `ConsentDecisionRecord`'s existing pattern, so an invalid role can never reach storage regardless of caller.
2. `ProfileStore` must reuse the identical `_transaction()` context-manager pattern already proven in `jarvis/memory/store.py` (commit/rollback via the connection's own context manager, explicit `close()` in `finally`) - not a fresh implementation that could reintroduce the Windows file-lock leak that pattern was written to fix.
3. No password, PIN or other credential field is added to `ProfileRecord` in this package - see Section 8 exclusion 2.
4. The frontend create-form must not block the rest of the UXP from rendering - `CommandPanel` and the conversation flow remain fully functional even before any profile is created or selected.
5. No change to `GuardianRuntime.converse()`, `GuardianRuntime.speak()`, `PersonalMemoryStore`, `PersonalMemoryService`, or any existing memory/conversation RPC method - see Section 8 exclusion 1.

---

# 8. Explicit Exclusions

This package does not authorise:

1. **Scoping conversation or memory content by active profile.** `GuardianRuntime.converse()`/`speak()` and `PersonalMemoryStore`'s schema are unchanged - Personal Memory remains a single, unpartitioned store exactly as it is today. Wiring the active profile into what Guardian remembers or how it addresses the user is a distinct, separately-scoped follow-on (naturally feeding MLP 0.3 Family Profiles and MLP 0.4 Session/Shared-Family memory tiers, per RSC-0001 Section 6's own dependency note) - not attempted here, to keep this package's diff reviewable and its claim honest: it resolves RSC-0001's literal "no identification, login or profile-switching code path exists" gap, not the larger memory-partitioning architecture.
2. **Any password, PIN, biometric or other credential-based authentication.** A profile in this package is a named, role-tagged identity a household member selects, not a secured login - GAM-0001 Section 8.1 itself defines only roles, no credential concept, and MLP 0.1's "basic" bar (matching "Basic Voice Input" being speech-only, not full NLU) does not require it. Credentialed authentication, if ever wanted, is a distinct future package.
3. **Any enforcement of GAM-0001 Section 8.1's authority differences** (e.g. Child-role restrictions actually gating capabilities, Guest-role's shared-memory exclusion actually being enforced). This package makes the role a real, selectable, persisted field; it does not wire that field into `TrustTierPolicy` or any approval-gating logic. Enforcement is the natural next step this package deliberately leaves open, not an oversight.
4. **Multi-device or account-based profile sync.** Profiles are stored in a single local SQLite file per installation (`~/.jarvis/identity/profiles.db`, mirroring the Personal Memory store's own locality), exactly like every other local store in this codebase today.
5. **Deleting or editing an existing profile.** Only create/list/select are authorised; deletion/edit would need `PersonalMemoryStore.delete()`-equivalent design (audit/orphan-reference handling) not scoped here.

---

# 9. Constraints

1. No file change shall be made until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0045.
3. Rust changes must pass `cargo check`/`cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check` (the existing CI gate, EBG-0103) before being considered complete.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
cd src-tauri && cargo build && cargo clippy -- -D warnings && cargo fmt --check && cargo test
cd .. && npx playwright test
```

Validation should confirm:

1. Full pytest suite passes, including new `test_identity_store.py`/`test_identity_service.py`/extended `test_stdio_rpc.py` cases, with no regression.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. Rust build/clippy/fmt/test all pass cleanly.
4. Playwright suite passes, including the new/extended profile-picker spec.
5. **A genuine live smoke check**, not merely mocked tests: `npm run tauri dev` against a fresh (non-existent) `identity.db`, confirming the create-profile form appears, a profile can genuinely be created and is immediately shown as active, the app restarted to confirm the selection persists across process restart, and a second profile created and switched to via the picker - matching this project's Operational Verification Before Reporting discipline.
6. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

None new. Builds entirely on already-approved, already-shipped patterns (`jarvis/memory/store.py`'s `_transaction()` pattern, `call_backend`'s established Tauri pattern, GAM-0001 Section 8.1's role definitions).

## Risks

1. **This package resolves RSC-0001's literal gap without yet delivering multi-user value** - conversations and memory remain global regardless of which profile is active until a follow-on package wires profile-scoping in (Section 8 exclusion 1). Disclosed upfront: a Programme Sponsor reviewing "is User Profiles now real" should understand this delivers identification/switching, not yet personalisation.
2. **No authentication means any household member can select any profile**, including Administrator - acceptable at MLP 0.1's basic bar per Section 8 exclusion 2's reasoning, but a real security boundary is not established by this package and should not be assumed by any future package building on it without saying so explicitly.
3. **SQLite file-lock behaviour on Windows** was already a proven risk in the memory store (`jarvis/memory/store.py`'s own docstring records a genuine `PermissionError` this pattern was written to fix); reusing that exact pattern is the mitigation, not a new untested approach.

## New Backlog Item Registered by This Draft

None anticipated. This package directly implements EBG-0116 as scoped by its own registration text (identification/login/profile-switching); the explicit exclusions above (memory-scoping, role enforcement) are pre-existing, separately-tracked gaps (RSC-0001 Section 6, LGB-0001 Defer table) rather than new discoveries.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern. **Result: Pass, no blocking findings.** Codex independently verified every Section 4 Repository Context claim against the live cited files (`jarvis/memory/store.py`'s schema and `_transaction()` pattern, `GuardianRuntime.converse()`/`speak()`'s signatures, `stdio_rpc.py`'s `_methods` registry and env/default-path pattern, `src/App.jsx`'s static profile card, `src-tauri/src/lib.rs`'s command pattern, GAM-0001 Section 8.1/10), confirmed the EIP's Section 2 accurately reflects EBG-0116/RSC-0001/LGB-0001's actual text and stays within EBG-0116's authorised scope, confirmed the `jarvis/identity/` module pattern is an appropriate mirror of `jarvis/memory/`'s proven pattern, and assessed Section 8's exclusions (no memory-scoping, no credentials/authentication, no role enforcement, no multi-device sync, no delete/edit) as defensible for an MLP 0.1 "basic" User Profiles increment - RSC-0001's Fail criterion is the literal absence of identification/login/profile-switching code, not absence of memory partitioning or role enforcement, and LGB-0001 explicitly defers Family Profiles/full HITL wiring beyond MLP 0.1. No blocking findings; hit the same disclosed, pre-existing `CreateProcessAsUserW` Windows sandbox limitation as prior sessions when spawning subprocess commands (`rg`/`Get-ChildItem` via `pwsh`), recovered by reading files directly instead.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (ESR-0046/WP1) before implementation began.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0116 (this package's parent item, to be marked Complete on approval and implementation). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Must-Ship item this package delivers; to be refreshed per its own Section 8 maintenance rule. |
| [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] | Scored the User Profiles gap this package resolves. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.1 Household Role Model - the role taxonomy `Profile.role` is validated against; to be updated recording operational implementation. |
| [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] | Precedent for this package's three-layer (backend/Tauri/frontend) scoping and disclosed-dependency handling. |
| [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Operational Verification Before Reporting discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 31 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: **Pass, no blocking findings.** Every Repository Context claim independently verified against live cited files; scope confirmed within EBG-0116's authority; Section 8 exclusions assessed as defensible for the MLP 0.1 basic bar. Awaiting Programme Sponsor approval. |
| 0.1 | 31 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0046 WP1. |
