# ESR-0027 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0027 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0027 |
| Date Opened | 18 July 2026 |
| Date Closed | 18 July 2026 |
| Closure Status | Closed - WP1-WP2 complete, session-wide WP6 Pass, WP7 Accept (RBL-0015 retained) |

---

# 2. Purpose

This report records the opening and execution of ESR-0027, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0026, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) with no manual relay anywhere - every review step across both Work Packages and the session-wide WP6 verification went through genuine `submit-to-review`/`return-findings`/`sponsor-decision`/`submit-response` cycles.

---

# 3. Scope

ESR-0027 opened with WP0A/WP0B repository synchronisation (ESR-0026 closed, RBL-0015 accepted baseline). The Programme Sponsor selected a two-Work-Package objective at WP0B, presented as High/Medium/Low priority candidates drawn from JRM-0001's Near-term horizon and EBR-0001's backlog: **WP1** (Memory implementation, the higher-priority selection) and **WP2** (EBG-0077, UXP static placeholder reconciliation, queued behind WP1).

A WP0-style scope check preceded WP1's drafting: the Programme Sponsor's initial selection ("Personal Memory + consent gate") was found, on grounding against GAM-0001's own evidence check, to require building the first real approval-workflow mechanism in this codebase - no code path anywhere previously let a Sentinel `REVIEW` decision actually be resolved by a human. Presented as a scope fork with three options; the Programme Sponsor selected the expanded scope over deferring or descoping.

Both Work Packages completed the full real Working Report Lifecycle via the bridge: draft, Codex review, Programme Sponsor approval, implementation, commit, a second Codex review of the committed diff, and (for WP1) a fix cycle following genuine post-commit findings. Session-wide WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance closed the session, both also conducted via the bridge.

---

# 4. Engineering Authority

ESR-0027 opening was authorised by Programme Sponsor instruction on 18 July 2026, following repository synchronisation confirming [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] was closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Two Work Packages, selected by the Programme Sponsor at WP0B from a High/Medium/Low candidate menu:

- **WP1** - EBG-0080 (Personal Memory Implementation), High priority - the natural next Guardian faculty, building against the approved MDS-0001 architecture.
- **WP2** - EBG-0077 (UXP Static Placeholder Row Reconciliation), Medium priority - queued behind WP1 as a smaller, independent UXP tidy-up.

Both were met by closure, each exceeding its original scope in a disclosed, reviewed way: WP1 expanded from a storage-layer package into the first working consent-gate mechanism in the codebase; WP2 stayed within its originally drafted scope but surfaced and fixed a pre-existing, unrelated test-isolation gap during implementation.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation, PBK-0001 review, session objective selection, WP1 scope check | Complete - Section 7 |
| WP1 | Implemented `jarvis/memory/` (Personal Memory + minimal consent gate) per EIP-ESR0027-001, closing EBG-0080 | Complete - Section 8 |
| WP2 | Reconciled `DiagnosticsPanel`'s static rows against UAM-0001 per EIP-ESR0027-002, closing EBG-0077 | Complete - Section 9 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, RBL-0015 retained - Section 10 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[README|README.md]], [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.48), [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.26), [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] (v1.13) and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] (v1.2) reviewed at session open.
- Repository state verified directly: `git status` clean, `main` at `f4a96a0`, `core.hooksPath` confirmed set to `scripts/hooks`.
- Confirmed [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] the accepted baseline.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0027 (this report, authored at closure per established practice).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (retained throughout, confirmed again at this session's own WP7).
- Session objective selection presented as a High/Medium/Low priority menu drawn from JRM-0001's Near-term horizon and EBR-0001's ready backlog items; Programme Sponsor selected Memory implementation (High) and UXP placeholder reconciliation (Medium), to be bundled in one session as a Backlog Acceleration Opportunity.
- **Scope check**: before WP1 drafting began, the Engineering Implementer flagged that GAM-0001's own evidence check confirms no approval workflow exists in code today for any Sentinel `REVIEW` decision - only a static message. Presented as a three-way scope fork (build the minimal mechanism / storage-and-classification only / descope to storage foundation); the Programme Sponsor selected the expanded scope.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction ("Agreed") and subsequent scope-fork decision.

---

# 8. WP1 - Personal Memory Implementation (EBG-0080)

Resolves EBG-0080, registered at this session's own WP0B, itself MDS-0001 Section 11's anticipated first follow-on (open since ESR-0004's original memory vision recovery). Implements the first real slice of Guardian's Memory faculty - Personal Memory (MDS-0001 Section 6.2) - gated by GAM-0001 Section 9.2's memory-retention consent boundary.

**Design**: `jarvis/memory/store.py` (`PersonalMemoryStore`, SQLite-backed, `personal_memory` and `consent_decisions` tables) and `jarvis/memory/service.py` (`PersonalMemoryService.propose()/approve()/deny()`, reusing Sentinel's existing `requires_approval=True` classification path unmodified - no `sentinel/policy.py` or `sentinel/core.py` change was needed). Wired into `GuardianRuntime`'s previously-dormant `"Guardian Memory Boundary"` service and four new `stdio_rpc.py` JSON-RPC methods (`memory.propose`/`approve`/`deny`/`list`).

**Full real bridge review cycle**: v0.1 drafted and submitted to Codex, who returned two Medium findings (consent traceability under-specified - the original design had no durable record of a resolved decision; validation criterion inconsistent with the evidence actually submitted) and one Low finding (`propose()` should explicitly guard against non-`REVIEW` Sentinel outcomes). All three addressed at v0.2, confirmed resolved by Codex with no blocking findings; one further Low/editorial finding (a stale cross-reference to "logging output" after v0.2 added the durable table) corrected at v0.3. Programme Sponsor approved v0.3 via `sponsor-decision`.

**Two genuine defects were self-found and fixed during WP1's own required live smoke check**: a SQLite connection leak (`sqlite3.Connection`'s context manager only commits/rolls back, never closes - caused a real Windows `PermissionError`), fixed with an explicit `_transaction()` context manager; and a pre-existing test-isolation gap where every prior `build_default_runtime()` test call in `jarvis/tests/test_stdio_rpc.py` had been omitting a memory-db override, meaning the whole existing suite would have touched the real `~/.jarvis/memory/personal.db` once this package's code existed - fixed retroactively across the whole file, not just the new tests, the same defect class ESR-0026 WP1 found for Ollama's network endpoint.

**Post-commit review of the real committed diff found two further Medium findings**: `GuardianRuntime`'s memory methods checked only service connectivity, not runtime state (a connected-but-not-started runtime could propose/approve/list memory, unlike `converse()`'s two-check pattern); and `PersonalMemoryStore.add()` accepted any `consent_decision_id` without verifying a matching approved decision existed, so the storage layer itself - not just the one caller's careful ordering - could create orphan records. Both fixed in a follow-up commit (`_require_memory_service()` now also requires `RUNNING` state; `add()` now checks, inside the same transaction as the insert, that the referenced decision exists and is `"approved"`). **Codex's final confirmation: Pass, both findings resolved, no new blocking findings.**

- Commit SHAs: `505023c` (implementation), `dbd8424` (post-commit fix), `0cb70ac` (final closure)
- `python -m pytest`: 286 passed (was 254 at session start). `python scripts/validate_repository.py`: 0 errors, 120 warnings (111 pre-existing plus 9 known, disclosed cross-document Section-reference false positives).

---

# 9. WP2 - UXP DiagnosticsPanel Static Row Reconciliation (EBG-0077)

Resolves EBG-0077, registered at ESR-0025 following a Programme Sponsor question tied to preparing the UXP for planned Guardian self-awareness work.

**Reconciliation**: a row-by-row judgement of `DiagnosticsPanel`'s four permanently-static rows against UAM-0001 Section 11 (Diagnostics Philosophy) and Section 14 (Colour Language). `boundary`/`shell`/`agents` kept unchanged - honest, structural statements about the shell's own implementation, `agents` confirmed to map to the genuinely-not-started-but-roadmapped Agent Framework/GIA capability via `JARVIS_CAPABILITY_READINESS_MATRIX.md`. `first-light` removed - true in isolation, but reporting on an unrelated legacy product (the Tkinter First Light app) rather than this shell's own boundary.

**Review**: Codex confirmed the concept with no blocking findings on the pre-implementation pass (all four review questions answered in favour of the proposed design), plus one Low/editorial finding (a stale comment enumerating four rows) addressed at v0.2. Programme Sponsor approved via `sponsor-decision`. **Post-implementation review of the real committed diff: Pass, no blocking findings** - every claim independently verified (row removal, orphaned `Zap` import removed, comment corrected, `boundary`/`shell`/`agents` genuinely unchanged, no backend files touched). No fix cycle needed.

**Verified live** via an ad hoc Playwright check against the real Vite dev server (mocking the Tauri invoke bridge, no live backend, per the EBG-0072/EBG-0073 precedent): `DiagnosticsPanel` renders exactly three rows, zero console errors. `npm run build` clean.

- Commit SHAs: `f29cf66` (implementation), `05869a7` (final closure)
- `python -m pytest`: 286 passed (unaffected, frontend-only). `python scripts/validate_repository.py`: 0 errors, 120 warnings (unchanged).

---

# 10. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0027_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0027 WP6 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session diff across both Work Packages.

**Session-wide WP6 (Independent Repository Verification)**: Codex independently confirmed repository state at `05869a7` matched the handover's claims - commit chain, authorised working set (16 files, 1406 insertions, 78 deletions), scope boundaries (no `sentinel/` files touched, `src/` limited to WP2's disclosed subtraction), and accurate disclosure of all four defects found across the session. **Two Low findings** were raised on the handover's own record-keeping: overstated "clean" wording against the handover document's own untracked status at submission time, and one trailing-whitespace line in `jarvis/tests/test_stdio_rpc.py:70` (a leftover from the automated regex rewrite used during WP1's test-isolation fix). Both fixed. **Pass.**

**Session-wide WP7 (Repository Baseline Acceptance): [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline.** Both independent views converged: WP1's new backend Personal Memory capability is not yet reachable through the running UXP's conversational interface (only via direct JSON-RPC calls nothing in the live UI currently invokes), closely mirroring the ESR-0026/Ollama precedent (new backend capability, not yet UXP-reachable, retained baseline). WP2's UXP change was a small, disclosed three-line subtraction, comparable in kind to EBG-0073's DiagnosticsPanel tidy-up at ESR-0023, which also didn't independently warrant a new baseline. Neither WP, alone or combined, resembles the kind of change that established RBL-0015 itself (ESR-0022's production provider wiring, which changed the default behaviour of every live conversation). Programme Sponsor's own determination: **Accept - retain RBL-0015**.

- Commit SHAs: `d7ab1f7` (WP6 handover + Low-finding fixes), `fe690ae` (WP7 closure)
- `python -m pytest`: 286 passed. `python scripts/validate_repository.py`: 0 errors, 120 warnings.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0080, EBG-0077 both closed Complete this session. |
| [[EIP-ESR0027-001_PERSONAL_MEMORY_IMPLEMENTATION|EIP-ESR0027-001]] | Approved and implemented package for WP1, v1.1. |
| [[EIP-ESR0027-002_UXP_DIAGNOSTICS_PANEL_RECONCILIATION|EIP-ESR0027-002]] | Approved and implemented package for WP2, v1.0. |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Storage architecture WP1 implements the Personal Memory tier of. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Consent gate WP1's propose/approve/deny mechanism implements the first real instance of. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Diagnostics Philosophy and Colour Language WP2's reconciliation is judged against. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0027_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0027 WP6 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.3, Section 10. |
| [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] | Prior closed session this one continues from. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Retained as the current accepted repository baseline at Section 10. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0-WP2, the session-wide WP6 Independent Repository Verification (Pass, two Low findings fixed) and WP7 Repository Baseline Acceptance (RBL-0015 retained). Second session run entirely through the AIEMS Exchange Bridge with no manual relay. Status Open to Closed. |
