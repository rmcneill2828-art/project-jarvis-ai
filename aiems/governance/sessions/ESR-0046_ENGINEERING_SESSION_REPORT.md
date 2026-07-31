# ESR-0046 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0046 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0046 |
| Date Opened | 31 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 complete |

---

# 2. Purpose

This report records the opening and execution of ESR-0046, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] closed (30 July 2026), [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), README.md and PST-0001 both current (no staleness found).

The Programme Sponsor selected this session's objective directly from [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]]'s two Must-Ship items (both newly registered at ESR-0045 WP5, neither previously actioned): **EBG-0116 (User Identity and Profile Foundation)**, over EBG-0117 (Voice Faculty Increment B: Speech Input) - selected as the higher-leverage item, since RSC-0001 Section 6 identified it as the shared prerequisite also blocking Family Profiles (MLP 0.3) and full HITL/family-safety live wiring (MLP 0.8).

EBG-0116's own registration text withholds implementation authority: "No implementation, design or scoping is authorised by this entry - a future Engineering Implementation Package would still need to be drafted, reviewed and approved." This session's objective is therefore to scope and draft an Engineering Implementation Package for EBG-0116, for Codex design review and Programme Sponsor approval before any code changes.

---

# 4. Engineering Authority

ESR-0046 opening was authorised by direct Programme Sponsor instruction on 31 July 2026, following review of PBK-0001, PST-0001, ESR-0045 and LGB-0001, confirming [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] as the accepted repository baseline at session open, and a direct choice between LGB-0001's two Must-Ship items via an explicit objective-selection question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Scope and draft [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0116 (User Identity and Profile Foundation): resolve RSC-0001's scored Fail against [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5's MLP 0.1 "User Profiles" requirement by implementing local profile identification and switching - grounded in [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's Household Role Model - and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before implementation.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0116: scope and draft User Identity and Profile Foundation; Codex design review; Programme Sponsor approval; implement | Complete |

Further Work Packages will be added if the Programme Sponsor directs the session remain open beyond WP1, matching the ESR-0045 precedent.

---

# 6A. WP1 - EBG-0116: User Identity and Profile Foundation

Investigated the existing architecture before drafting scope (Explore agent research, independently spot-checked by direct read): `jarvis/memory/store.py`'s schema has no user/owner column; `GuardianRuntime.converse()`/`speak()` take no caller identity; `jarvis/interfaces/stdio_rpc.py`'s JSON-RPC protocol reads no session/caller field; `src/App.jsx:288-297` renders a static, unwired "Robert / Signed in locally" profile card; [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 defines four household roles (Administrator/Adult/Child/Guest) but Section 10 explicitly states it does not implement login, identification or access control.

Produced [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] (v0.1, Draft), scoping a new `jarvis/identity/` module mirroring `jarvis/memory/`'s proven `ProfileStore`/`ProfileService` SQLite pattern, four new JSON-RPC methods, matching Tauri commands, and a real UXP profile picker - deliberately excluding credentialed authentication, memory scoping by profile, and role-authority enforcement (disclosed, separately-tracked follow-on work, not silently under-delivered).

Submitted to Codex for design review via direct `codex exec -s read-only` invocation - **v0.1: Pass, no blocking findings.** Codex independently verified every Section 4 Repository Context claim against the live cited files, confirmed the package stays within EBG-0116's authorised scope, confirmed the `jarvis/identity/` pattern is an appropriate mirror of `jarvis/memory/`'s proven pattern, and assessed Section 8's exclusions as defensible for an MLP 0.1 "basic" User Profiles bar.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service before implementation began.

**Implemented exactly as scoped**, with one disclosed design refinement discovered during implementation: rather than constructing `ProfileService` inside `build_default_runtime()` as the draft EIP described, it is constructed directly inside `StdioRpcServer.__init__` (env-var/default-path driven, injectable for tests) - mirroring the GIA observer's own existing decoupling precedent in the same file ("GIA is deliberately not constructed from or dependent on `runtime`"), which fits this codebase's established pattern more closely than the originally-drafted approach. Same three layers, same four RPC methods, same behaviour - a structural fit discovered while implementing, not a scope change.

- **Backend** (`jarvis/identity/` new module: `store.py`, `service.py`, `__init__.py`): `ProfileRecord` (role validated against GAM-0001 Section 8.1's four values at the dataclass level), `ProfileStore` (SQLite, reusing `jarvis/memory/store.py`'s exact `_transaction()` Windows-file-lock-safe pattern), `ProfileService` (create/list/select/active, referential-integrity check on select). `jarvis/interfaces/stdio_rpc.py`: four new `profile.*` RPC methods, `_serialize_profile` helper. 22 new tests in `jarvis/tests/test_identity_store.py`/`test_identity_service.py`; `jarvis/tests/test_stdio_rpc.py` extended with 7 new RPC-layer tests plus `identity_service` test-isolation fixes across all 8 `StdioRpcServer` construction sites in the file (an unfixed site would have touched the real `~/.jarvis/identity/profiles.db` on every test run - the same test-isolation defect class ESR-0026 WP1 found for Ollama).
- **Tauri** (`src-tauri/src/lib.rs`): `list_profiles`/`create_profile`/`select_profile`/`active_profile` commands, byte-for-byte the same thin-wrapper shape as `send_message`. Verified Tauri's command macro defaults to camelCase JSON argument matching (`ArgumentCase::Camel`, confirmed by direct read of `tauri-macros` source) before relying on it for the multi-word `display_name`/`profile_id` parameters. `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test` all pass cleanly.
- **Frontend** (`src/App.jsx`, `src/styles.css`): the static profile card replaced with a real `ProfileCard` component - a create-profile form (name + GAM-0001-role select) when no profile is active, a switching picker when one is. `npm run build` succeeds; 2 new Playwright specs added to `tests/e2e/app.spec.js` (create-form-appears-and-creates, picker-switches-active-profile), full e2e suite (9 tests) passes.
- **Governance**: [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 10 corrected (identification/switching now implemented; enforcement/authentication remain not implemented). [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0116 marked Completed. [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] Must-Ship row struck through per its own Section 8 maintenance rule.

**Live smoke check performed** (Section 10 item 5) at the RPC/storage layer - a genuine, non-mocked check: a real temp SQLite file, a real `GuardianRuntime`, real JSON-RPC lines through the real `StdioRpcServer.handle_line()` dispatch path. Confirmed: fresh db has no active profile; create-then-select-then-active round trip; persistence across a fresh `StdioRpcServer` instance pointed at the same db file (real process-restart semantics); a second profile created and switched to; an invalid role and an unknown profile id both surface as honest JSON-RPC errors, not crashes. A literal native-window visual click-through (`npm run tauri dev`, a real WebView2 window) was not performed in this implementation environment - no project skill covers launching this specific Tauri app, and this headless shell has no practical automation path for a native Windows desktop window - disclosed honestly rather than assumed, matching EIP-ESR0044-001's own disclosed audio-hardware-playback limitation.

Full Python suite: 453 passed, 1 skipped (was 424/1, 29 new). `validate_repository.py` (full mode): 0 errors, 266 warnings (pre-existing, unrelated dangling section-heading references).

- Files: `jarvis/identity/__init__.py` (new), `jarvis/identity/store.py` (new), `jarvis/identity/service.py` (new), `jarvis/tests/test_identity_store.py` (new), `jarvis/tests/test_identity_service.py` (new), `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_stdio_rpc.py`, `src-tauri/src/lib.rs`, `src/App.jsx`, `src/styles.css`, `tests/e2e/app.spec.js`, `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/baselines/LGB-0001_LAUNCH_GAP_BACKLOG.md`, `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`, `README.md`, [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] (new).
- Committed and pushed to `origin/main` (SHA reported at closure).

---

# 7. Related Artefacts

* [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0116 (this session's objective).
* [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] - source of this session's objective selection (Must-Ship item).
* [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] - scored the User Profiles gap this session addresses.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - Section 8.1 Household Role Model, the authority taxonomy this session's identity mechanism must implement against.
* [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] - repository baseline at session open.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 31 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0116 (User Identity and Profile Foundation) resolved per [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] (Codex design review: Pass, no blocking findings; Programme Sponsor approval verified via the real Sponsor Approval Service). New `jarvis/identity/` module, four new `profile.*` RPC methods, real UXP profile picker replacing the static placeholder. Full validation clean across Python/Rust/frontend/Playwright; live smoke check performed at the RPC/storage layer. |
| 1.0 | 31 July 2026 | Claude Engineering Implementer | ESR-0046 opened at WP0B, before WP1 began. Objective: scope and draft EBG-0116 (User Identity and Profile Foundation), selected by the Programme Sponsor from LGB-0001's two Must-Ship items as the higher-leverage item, producing an Engineering Implementation Package for Codex review and Programme Sponsor approval before implementation. |
