# RBL-0021 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0021 |
| Title | ESR-0035 Repository Baseline (Documentation Debt, Guardian Cognitive Core Backlog Registration, and UXP Shared Animation Scheduler) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0035_ENGINEERING_SESSION_REPORT|ESR-0035]] |
| Previous Baseline | [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 25 July 2026 |
| HEAD at baseline creation | `2d9cf7e` |

---

# 2. Purpose

RBL-0021 records the repository baseline accepted by the Programme Sponsor at ESR-0035 WP5, superseding [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]]. ESR-0035 ran three Work Packages: WP1 (documentation debt - stale RBL-0019/ESR-0033 current-state references across README.md/COC-0001/PBK-0001/REG-0001), WP2 (registered EBR-0001 EBG-0108, Guardian Cognitive Core Implementation, directly to Approved Backlog, closing JRM-0001's own flagged Phase 1 gap), and WP3 (delivered EBG-0081 Question 1 - a real, live-verified UXP shared animation scheduler, this session's required product-moving work per PBK-0001's Feature-First Delivery Discipline, since WP1/WP2 were both governance-only). Both independent WP4 views (Engineering Implementer and Engineering Reviewer) converged on this being baseline-worthy, citing WP3's genuine product code change and new test coverage as the justification beyond pure governance churn.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; WP3's animation scheduler is an internal performance/scaling primitive, not a new user-facing product capability tier, so no PCB-0001 update was in scope |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP4 handover]] recorded two independently-reached views (Sections 9-10), both recommending a new baseline rather than retaining RBL-0020.

**Engineering Implementer's view**: unlike ESR-0034 (entirely governance/roadmap curation, correctly judged not baseline-worthy), ESR-0035 delivered a genuine, live-verified product code change at WP3 - a new shared UXP animation-scheduling module now used by a live component (`GuardianOrbGraph.jsx`), backed by new automated test coverage that did not exist before. This is the same category of change that justified RBL-0020 itself at ESR-0033 WP9: a real change to shipped product behaviour and its test coverage, not pure governance churn. The addition of a new, reusable animation-driving primitive that future UXP work (Phase 6 Voice/Vision, per JRM-0001) is expected to build on is exactly the kind of change a baseline exists to mark.

**Engineering Reviewer's (Codex) independent view**: converged - "WP3 is not merely governance churn: it added a new product module, refactored a live component to use it, and added Playwright coverage for the scheduler contract. That is a meaningful repository state change future sessions should synchronize against." Codex independently confirmed the exact diff-stat figures (11 files, 368 insertions, 48 deletions), the file-list accuracy, that no `sentinel/`/`jarvis/`/`src-tauri/`/`.github/workflows/` file changed, before reaching this view.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `README.md`, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Stale RBL-0019/ESR-0033 current-state references corrected to RBL-0020/ESR-0034/ESR-0035, applying PBK-0001's own Whole-Document Staleness Sweep on Edit discipline (WP1). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108 (Guardian Cognitive Core Implementation) registered directly to Approved Backlog (WP2); EBG-0081 (UXP Animation Performance Policy) closed Complete - both questions now delivered (WP3). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Sections 7.1/7.3 updated to record EBG-0108's registration (WP2); Section 7.4 and the Phase 6 Voice/Vision row updated to record EBG-0081's delivery (WP3). |
| `src/animationScheduler.js` | New singleton shared UXP animation clock - `subscribe(callback) -> unsubscribe`, a single `requestAnimationFrame` loop started lazily on the first subscriber and stopped once the last unsubscribes, throwing subscribers isolated via `try`/`catch` (WP3). |
| `src/GuardianOrbGraph.jsx` | Private `requestAnimationFrame`/`cancelAnimationFrame` loop replaced with a `subscribe`/`unsubscribe` call to the new shared scheduler - identical tick logic, throttling, idle and visibility-change handling, no behavioural change intended (WP3). |
| `tests/e2e/animationScheduler.spec.js` | New - 3 tests proving the scheduler's contract (shared single loop regardless of subscriber count, throwing-subscriber isolation, loop stops at zero subscribers) via a deterministic fake `requestAnimationFrame`, after a real-timing version proved flaky in headless Chromium (WP3). |
| Test suite | 374 Python tests plus 1 skip, unchanged from RBL-0020. 5 Playwright tests, up from 2 (3 net-new scheduler tests); no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. WP3's shared animation scheduler is an internal, non-functional performance/scaling primitive - it changes how the existing Guardian Orb rendering is driven, not what capability is presented to the user, and adds no new product capability tier PCB-0001 needs to record.

---

# 7. Architecture Outcomes

- The UXP now has a single shared animation clock that any future continuously-animated element registers with, rather than each spinning up its own independent `requestAnimationFrame` loop - closing EBG-0081's own stated forward-looking concern about animation cost scaling as more animated elements are added (e.g. Phase 6 Voice/Vision's voice waveform).
- The Guardian Cognitive Core - JARVIS/Guardian's most consequential undelivered capability, per JRM-0001's own roadmap analysis - now has an approved backlog authorisation (EBG-0108) to build against, closing a gap the roadmap itself had flagged as blocking every later phase.
- Both questions of EBG-0081 (UXP Animation Performance Policy) are now closed: Question 2's Canvas migration (ESR-0029 WP2) and Question 1's shared scheduler (this baseline).

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no implementation of EBG-0108 (Guardian Cognitive Core) itself is authorised by this baseline - only its backlog registration;
- EBG-0021 (Local Agent Permission Boundary) and EBG-0042 (Agent Framework Architecture) remain out of scope, not addressed by this baseline;
- all other open EBR-0001 backlog items remain out of scope, not addressed by this baseline;
- no new third-party product dependencies were introduced this session;
- `sentinel/`, `jarvis/` and `src-tauri/` were not touched at all this session - no trust-boundary or backend change of any kind.

---

# 9. Verification

Repository validation performed during ESR-0035 WP4/WP5:

- Git working tree was clean; the session's intended content range (`096a06b`..`2d9cf7e`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main` at every commit in the session, with real GitHub Actions CI green at every CI-relevant push (WP3, the first session commit touching `src/`/`tests/`).
- 374/374 Python tests passing plus 1 correctly-skipped win32-conditional test, unchanged from RBL-0020. 5/5 Playwright tests passing (2 existing, 3 new).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 166 warnings for the session-content diff itself (169 including the WP4 handover's own prose, both figures independently confirmed by the Engineering Reviewer as correct for their respective scopes).
- `npm run build` clean.
- `git diff --stat 096a06b..2d9cf7e` independently re-run by the Engineering Reviewer, confirmed to match exactly (11 files, 368 insertions, 48 deletions).
- The Engineering Reviewer performed WP4 Independent Repository Verification: **Pass, one reporting correction (warning-count scope clarification), no blocking findings** - independently confirmed the diff-stat figures, file-list accuracy, and that `sentinel/`/`jarvis/`/`src-tauri/`/`.github/workflows/` were untouched. Could not independently reproduce `pytest`/Playwright in its own read-only sandbox (disclosed environmental limitation, consistent with prior sessions).
- The Programme Sponsor's own WP5 determination: establish a new baseline rather than retain RBL-0020 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0035** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0108 registered Approved Backlog; EBG-0081 Complete.
5. The [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP4 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0035 WP4 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not affected by this session's scope. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0108 registered, EBG-0081 closed this session. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Phase 1 gap and Section 7.4 shared-scheduler constraint both updated this session. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 25 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0020, following the Engineering Reviewer's WP4 Pass and the Programme Sponsor's explicit WP5 decision to cut a new baseline rather than retain RBL-0020: WP3's real UXP shared animation scheduler (new module, live-component refactor, new test coverage) together with WP1/WP2's documentation and backlog governance warrant a new baseline, agreeing with both independent WP4 baseline views. |
