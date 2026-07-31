# RBL-0028 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0028 |
| Title | ESR-0046 Repository Baseline (User Identity and Profile Foundation) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] |
| Previous Baseline | [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 31 July 2026 |
| HEAD at baseline creation | `02f7f39` |

---

# 2. Purpose

RBL-0028 records the repository baseline accepted by the Programme Sponsor at ESR-0046 WP7, superseding [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]]. ESR-0046 ran one Work Package: WP1, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0116 (User Identity and Profile Foundation) - a genuine, live product-capability change: Guardian now has real, working local user profiles (create/list/select, role-tagged against GAM-0001 Section 8.1's four household roles), closing RSC-0001's scored "User Profiles" Fail against MLP 0.1.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; a future refresh should add the User Identity and Profile Foundation capability. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Design review (Codex, direct `codex exec -s read-only` invocation)**: Pass, no blocking findings - confirmed every Section 4 Repository Context claim in [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] against the live cited files, confirmed the package stayed within EBG-0116's authorised scope, and assessed the disclosed exclusions (no credentialed authentication, no memory scoping by profile, no role enforcement) as defensible for an MLP 0.1 "basic" bar.

**Post-commit independent verification**: Codex's own re-review of the actual pushed diff could not be completed - two direct `codex exec -s read-only` attempts stalled indefinitely, traced to a 322 MB `~/.codex/logs_2.sqlite` plus stale lock files (global Codex CLI state outside this repository, disclosed and tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118). The Programme Sponsor selected skipping the re-review over clearing CLI state. In its place, the Engineering Implementer independently confirmed: `git diff --stat d095f48..HEAD` matches the 19 files claimed across both WP1 commits; `git diff --name-only d095f48..HEAD -- jarvis sentinel src src-tauri scripts` returns exactly the 10 files authorised by EIP-ESR0046-001 Section 6, nothing outside that list; `python -m pytest` 453 passed/1 skipped; `python scripts/validate_repository.py` (full mode) 0 errors.

**Programme Sponsor approval**: obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**The Programme Sponsor's determination**: **establish a new baseline**, since this session's WP1 delivered a genuine, live product-capability change - Guardian's identity/profile system is reachable through the actual running Tauri UXP, backed by a real end-to-end round trip (create/select/persist-across-restart/switch) through the exact new RPC wiring, matching the same threshold applied at RBL-0025/RBL-0027 (Voice faculty delivery/live-wiring) rather than the Retain threshold applied at RBL-0025/RBL-0026-era architecture-only sessions.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/identity/` (new: `store.py`, `service.py`, `__init__.py`) | `ProfileRecord`/`ProfileStore`/`ProfileService` - SQLite-backed local profile create/list/select/active, role validated against GAM-0001 Section 8.1's four household roles at the dataclass level, mirroring `jarvis/memory/store.py`'s proven `_transaction()` pattern. |
| `jarvis/interfaces/stdio_rpc.py` | Four new JSON-RPC methods (`profile.list`/`create`/`select`/`active`), `identity_service` decoupled from `runtime` construction (mirroring the existing GIA-observer precedent in the same file). |
| `jarvis/tests/test_identity_store.py`, `test_identity_service.py`, extended `test_stdio_rpc.py` | 29 new tests; test-isolation fixes applied across all 8 `StdioRpcServer` construction sites in the file to prevent any test touching the real `~/.jarvis/identity/profiles.db`. |
| `src-tauri/src/lib.rs` | `list_profiles`/`create_profile`/`select_profile`/`active_profile` commands, byte-for-byte matching `send_message`'s `call_backend` shape. `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test` all pass cleanly. Verified Tauri's command macro defaults to camelCase argument matching before relying on it for multi-word parameters. |
| `src/App.jsx`, `src/styles.css` | The static "Robert / Signed in locally" placeholder replaced with a real `ProfileCard` - a create-profile form when no profile is active, a switching picker when one is. |
| `tests/e2e/app.spec.js` | 2 new Playwright specs (create-form-appears-and-creates; picker-switches-active-profile) - full e2e suite (9 tests) passes. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 10 corrected (1.3 to 1.4): identification/switching now implemented; enforcement/authentication remain not implemented. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0116 marked Completed; EBG-0118 registered (Codex CLI tooling stall, Candidate Backlog, Low). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Must-Ship row struck through per its own Section 8 maintenance rule. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. A future session should refresh it to reflect the User Identity and Profile Foundation as a new capability row, mirroring how Voice faculty delivery was handled at prior refreshes.

---

# 7. Architecture Outcomes

- Guardian now has a real, local, role-tagged profile system - the first implementation of GAM-0001 Section 8.1's Household Role Model beyond a pure taxonomy.
- No existing conversation or memory component (`GuardianRuntime.converse()`/`speak()`, `PersonalMemoryStore`) was modified - independently confirmed via direct `git diff` grep showing neither `jarvis/guardian/runtime.py` nor `jarvis/memory/store.py` in the session's diff.
- The new `jarvis/identity/` module deliberately mirrors `jarvis/memory/`'s already-proven storage pattern rather than inventing a new one, including reuse of the Windows-file-lock-safe `_transaction()` idiom.
- `identity_service` construction is decoupled from `build_default_runtime()`, mirroring the existing GIA-observer precedent already established in `stdio_rpc.py` - a design refinement discovered and disclosed during implementation, not part of the original draft EIP.
- The new UXP affordance is deliberately minimal - a create-form and a switching picker, no redesign of the wider shell - consistent with PBK-0001's Incremental Visual Convergence discipline.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no credential/password/PIN authentication exists anywhere in the identity system - a profile is a named, role-tagged selection, not a secured login;
- no conversation or memory content is scoped by active profile - Personal Memory remains a single, unpartitioned store;
- no enforcement of GAM-0001 Section 8.1's differing role authority against Sentinel/`TrustTierPolicy` - the role field is real and persisted, but not yet consulted by any policy/approval logic;
- no profile deletion or edit - only create/list/select;
- no multi-device or account-based profile sync - a single local SQLite file per installation.

---

# 9. Verification

Repository validation performed during ESR-0046 WP1 and at WP6/WP7 closure:

- Git working tree was clean; the session's content (`d095f48..02f7f39`, two commits) pushed to `origin/main`.
- 453/454 Python tests passing plus 1 correctly-skipped test, up from 424/425 at RBL-0027 (29 new).
- `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test`: all clean.
- `npx playwright test`: 9 passed (2 new, was 7 at RBL-0027's era).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count at 268, consistent with the established pre-existing cross-document-reference false-positive category.
- Design review (Codex, one round): Pass, no blocking findings. Post-commit independent diff review (Codex): **could not be completed** - two attempts stalled, traced to local Codex CLI tooling state (`~/.codex/logs_2.sqlite` at 322 MB plus stale lock files), disclosed and tracked as EBG-0118. Independent verification for WP6/WP7 was instead performed directly: `git diff --stat`/`git diff --name-only -- jarvis sentinel src src-tauri scripts` confirmed exactly the 10 authorised code files changed and nothing else, cross-checked against EIP-ESR0046-001 Section 6.
- Live end-to-end smoke validation: a real temp SQLite file, a real `GuardianRuntime`, real JSON-RPC lines through the real `StdioRpcServer.handle_line()` dispatch path - fresh-db/create/select/active round trip, persistence across a fresh server instance against the same db file (real process-restart semantics), a second profile created and switched to, and an invalid role/unknown id both surfacing as honest JSON-RPC errors rather than crashes.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0027 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0046** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. A literal native-window visual click-through (`npm run tauri dev`, a real WebView2 window) was not performed in this implementation environment - remains available for the Programme Sponsor, matching the exact precedent already established at ESR-0040/ESR-0042/ESR-0044 for real-hardware/real-window confirmation steps this implementation environment cannot perform.
5. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0117 (Voice Faculty Increment B: Speech Input) remains the other LGB-0001 Must-Ship item, still open.
6. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118 (Codex CLI tooling stall) remains open - a future session should confirm whether clearing `~/.codex/logs_2.sqlite`/its lock files resolves `codex exec` stalling before closing it.
7. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at a future session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] | Session this baseline is drawn from. |
| [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 10 corrected to record identification/switching as now implemented. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0116 (closed this session); EBG-0117 (unaffected, remains open); EBG-0118 (registered this session, remains open). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Must-Ship row struck through this session. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 31 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0027, following Codex's design review (Pass, no blocking findings) - post-commit independent diff review could not be completed due to a disclosed Codex CLI tooling stall (EBG-0118), independently verified directly instead - and the Programme Sponsor's explicit WP7 decision to cut a new baseline rather than retain RBL-0027: WP1's real, live-verified User Identity and Profile Foundation delivery warrants a new baseline. |
