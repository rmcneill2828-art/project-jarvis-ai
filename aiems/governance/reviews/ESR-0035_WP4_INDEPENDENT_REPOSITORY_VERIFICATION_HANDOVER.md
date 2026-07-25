# ESR-0035 WP4 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0035-WP4 |
| Title | Independent Repository Verification Handover |
| Version | 0.3 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0035 (open; session report already exists, authored incrementally this session rather than at closure) |
| Effective Date | 25 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0035's session-wide record for WP4 Independent Repository Verification. ESR-0035 ran three Work Packages: WP1 (documentation debt - stale RBL-0019/ESR-0033 current-state references), WP2 (registered EBG-0108, Guardian Cognitive Core Implementation, to Approved Backlog), and WP3 (delivered EBG-0081 Question 1, a real UXP shared animation scheduler - this session's required product-moving work per PBK-0001's Feature-First Delivery Discipline, since WP1/WP2 were governance-only). WP4 confirms the current repository state matches the claims made across all three Work Packages, that Codex-caught defects were genuinely fixed rather than only claimed fixed, and that no unauthorised scope drift occurred. Submitted to Codex via the AIEMS Exchange Bridge for genuine independent verification, continuing the practice used throughout ESR-0025 through ESR-0034 (the tenth consecutive session run this way).

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| ESR-0035 session start point | `096a06b` (ESR-0034 formal closure commit) |
| ESR-0035's content endpoint | `2d9cf7e` - the last commit of actual session content (WP1-WP3), and the range this handover's figures describe |
| This handover's own commit | Necessarily lands after `2d9cf7e`, since the handover is committed once drafted - the same structural point every prior session's verification handover has run into. |
| `origin/main` | Pushed and green at every commit this session (`c939ecf`, `bd11c8f`, `f471648`, `2d9cf7e`) - WP3 touched `src/` and `tests/e2e/`, both CI-relevant. |
| Prior accepted baseline | `RBL-0020` |

---

## 4. ESR-0035 Commits in Scope

| Commit | Summary |
|---|---|
| `c939ecf` | WP1: corrected stale RBL-0019/ESR-0033 current-state references in README.md, COC-0001 and PBK-0001 to RBL-0020/ESR-0034/ESR-0035 (Documentation Debt Discipline), plus REG-0001 tracking-row/version alignment and ESR-0035's own registration. Codex read-only review: Pass, no findings. |
| `bd11c8f` | WP1 closure narrative: recorded commit SHA and both Codex Pass verdicts (pre-commit and post-commit) in the ESR-0035 report. |
| `f471648` | WP2: registered EBR-0001 EBG-0108 (Guardian Cognitive Core Implementation) directly to Approved Backlog, closing JRM-0001 Track B's own flagged gap ("no backlog item yet authorises this build" - the single most consequential gap in the roadmap per ESR-0034 WP3). Updated JRM-0001 Sections 7.1/7.3, REG-0001, PST-0001. Codex's first pass found two stale warning-count mentions (fixed); second pass Pass. |
| `2d9cf7e` | WP3: delivered EBG-0081 Question 1 (UXP shared animation scheduler) - `src/animationScheduler.js` (new), `GuardianOrbGraph.jsx` migrated to it, `tests/e2e/animationScheduler.spec.js` (new, 3 tests). EBR-0001's EBG-0081 closed (both questions now delivered); JRM-0001 Section 7.4/Phase 6 updated. Codex code review: Pass, no blocking findings; caught one stale warning-count mention (fixed). |

---

## 5. Authorised / Explained Working Set

The full ESR-0035 session-content diff, `096a06b`..`2d9cf7e` (11 files changed, 368 insertions, 48 deletions):

**WP1 (documentation debt):** `README.md`, `COC-0001`, `PBK-0001` - stale RBL-0019/ESR-0033 current-state references corrected to RBL-0020/ESR-0034/ESR-0035, each document's own version-history table extended; `REG-0001` - PBK-0001/COC-0001 tracking rows and REG-0001's own version aligned, ESR-0035 registered as a new Open Engineering Session Report; `ESR-0035_ENGINEERING_SESSION_REPORT.md` (new) - session opening record plus WP1 closure narrative.

**WP2 (EBG-0108 registration):** `EBR-0001` - new EBG-0108 entry (Approved Backlog, High priority) referencing AAM-0001/JRM-0001, explicitly authorising no implementation; `JRM-0001` - Sections 7.1 and 7.3 updated to record the registration; `REG-0001`/`PST-0001` - tracking rows, version and current-state narrative updated.

**WP3 (EBG-0081 Question 1):** `src/animationScheduler.js` (new) - singleton shared animation clock; `src/GuardianOrbGraph.jsx` - private `requestAnimationFrame` loop replaced with a `subscribe`/`unsubscribe` call to the new module, no behavioural change intended; `tests/e2e/animationScheduler.spec.js` (new) - 3 tests proving the scheduler's contract via a deterministic fake `requestAnimationFrame`; `EBR-0001` - EBG-0081 status Approved Backlog to Complete; `JRM-0001` - Section 7.4 and the Phase 6 Voice/Vision row updated; `REG-0001`/`PST-0001` - tracking rows, version and current-state narrative updated.

**REG-0001** was updated at every version bump across all three Work Packages (PBK-0001 to 1.33, COC-0001 to 1.15, EBR-0001 to 1.133, JRM-0001 to 1.20, PST-0001 to 2.96), each an additive Version History row plus the corresponding self-row/badge update.

---

## 6. Session Observations

1. **Unlike ESR-0034 (entirely governance/roadmap curation), ESR-0035 includes a real product code change** - WP3 is genuine frontend implementation (a new shared-clock module, a refactor of an existing live UXP component, and new test coverage), not documentation or backlog curation. This is the first product-code Work Package since ESR-0033's EBG-0100 UXP Memory row.
2. **WP3 was deliberately selected to satisfy PBK-0001's Feature-First Delivery Discipline**: WP1 and WP2 were both governance-only, and the Programme Sponsor explicitly directed that WP3 add product-moving work rather than closing the session at WP2. EBG-0081 Question 1 was chosen from EBR-0001's Approved Backlog as a well-scoped, contained feature with confirmed prior art (EBG-0082), in preference to larger, definition-only items (EBG-0021, EBG-0042) that would have warranted their own dedicated future session.
3. **A test-writing mistake was caught and fixed before submission, not after**: the first version of the shared-loop scheduler test asserted on real browser `requestAnimationFrame` timing and proved flaky in headless Chromium (frame counts too low/jittery over a fixed wait). Rewritten against a fully deterministic fake `requestAnimationFrame` that only fires when the test explicitly steps it, removing the timing dependency entirely - caught by the Engineering Implementer's own test run, before Codex ever saw it.
4. **Two genuine stale warning-count mentions were caught by Codex across two different Work Packages, both fixed and independently reconfirmed**: WP2's first Codex pass found PST-0001 (157) and the ESR-0035 report (159) both understated the actual count (162) after new version-history text was added; WP3's Codex pass found the same class of drift again (163 stated vs 166 actual) after further version-history text was added by WP3 itself. Both were fixed and the fix confirmed against a fresh `validate_repository.py` run each time.
5. **Every Codex review this session ran in `-s read-only` sandbox mode**, per the standing EBG-0096 precedent - Codex's own sandbox cannot write the bridge's lock file directly, so findings were relayed into the bridge by the Engineering Implementer verbatim on Codex's behalf, under explicit per-instance Programme Sponsor approval for each relay act (never silently, never without approval).
6. **WP3's Codex code review could not independently run `npm run build`, `npx playwright test` or `python -m pytest` itself** - all three failed under Codex's read-only sandbox due to write restrictions (a Vite timestamp file, Playwright's `test-results` directory, and pytest's temp-directory requirement respectively), a disclosed environmental limitation consistent with prior sessions' own findings (e.g. ESR-0034 WP4), not a defect in this session's work. The Engineering Implementer's own direct runs outside that sandbox (374 passed/1 skipped, 5 Playwright tests passed, clean build) stand as the substantive evidence.

---

## 7. Validation Evidence

Re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 374 passed, 1 skipped (unchanged throughout - only WP3 touched non-Python code) |
| `npx playwright test` | 5 passed (2 existing app-level, 3 new scheduler tests) |
| `npm run build` | Clean |
| `python scripts/validate_repository.py` (full, not governance-only) | 0 errors, 166 warnings |
| `git status` | Clean working tree at `2d9cf7e` |
| Real GitHub Actions CI | Green at `2d9cf7e` (WP3 touched `src/` and `tests/e2e/`, both CI-relevant) |

The warning count rose from 157 (ESR-0034's closing figure) to 166 by WP3's close - all confirmed to be the same known false-positive class (cross-document "Section N.N" prose references), growing incrementally as each version bump added further Version History prose mentioning other documents' section numbers, not a new class of problem.

---

## 8. Scope Check

- WP1/WP2 touched only governance artefacts (`README.md`, `COC-0001`, `PBK-0001`, `EBR-0001`, `JRM-0001`, `REG-0001`, `PST-0001`, `ESR-0035`'s own report). WP3 additionally touched `src/animationScheduler.js` (new), `src/GuardianOrbGraph.jsx`, and `tests/e2e/animationScheduler.spec.js` (new) - real product/test code, disclosed and reviewed as such, not silently smuggled in as a "documentation" change.
- No `jarvis/`, `sentinel/`, `src-tauri/`, or `.github/workflows/` file was touched at all this session.
- No new third-party dependencies introduced.
- Every Work Package went through the same cycle: draft, Codex read-only review (relayed via `return-findings` under explicit per-instance Sponsor approval), fix round where findings existed, a second Codex confirmation pass where a fix round occurred, Sponsor approval via the real deployed Sponsor Approval Service, `submit-response`, then commit - no step skipped in any of the three. WP3 additionally received post-commit independent re-verification, as did WP1 and WP2.
- Working tree was clean and at `2d9cf7e` at the point this handover was drafted, with the handover document itself the sole new file at that moment, prior to being committed as its own follow-on commit (Section 3).

---

## 9. WP5 Baseline Recommendation

**Engineering Implementer's independent view:** establish a new baseline - do not retain `RBL-0020`.

Rationale: unlike ESR-0034 (entirely backlog-register curation and a roadmap-sequencing document rewrite, correctly judged not baseline-worthy), ESR-0035 delivered a genuine, live-verified product code change at WP3 - a new shared UXP animation-scheduling module now used by a live component (`GuardianOrbGraph.jsx`), backed by new automated test coverage that did not exist before. This is the same category of change that justified RBL-0020 itself at ESR-0033 WP9 (that session's WP3 UXP Memory-row change): a real, user-facing (if currently invisible-by-design, since it's a non-functional/performance-scaling change rather than a new visible feature) change to shipped product behaviour and its test coverage, not pure governance churn. A new baseline exists to mark a meaningfully different repository state for future sessions to synchronise against - the addition of a new, reusable animation-driving primitive that future UXP work (Phase 6 Voice/Vision, per JRM-0001) is expected to build on is exactly that kind of change.

---

## 10. WP4 Verification Result

**Pass, with one reporting correction - no blocking findings.** Codex independently confirmed `git diff --stat 096a06b..2d9cf7e` matches Section 5's claimed 11 files/368 insertions/48 deletions exactly, and `git diff --name-status` confirms no `sentinel/`, `jarvis/`, `src-tauri/`, or `.github/workflows/` file was touched. **Reporting correction**: this handover document itself (being drafted and reviewed before its own commit, the same structural point every prior session's verification handover runs into) was untracked at review time and adds 3 further "Section N.N" false-positive warnings of its own; `validate_repository.py` against the working tree including this file reads 0 errors/169 warnings, while the ESR-0035 session-content diff itself (`096a06b`..`2d9cf7e`, excluding this handover) is consistent with Section 7's claimed 166 - both figures are correct, describing different scopes, not a contradiction. Codex's own read-only sandbox could not independently reproduce `python -m pytest` (temp-directory restriction) or `npx playwright test` (blocked writing `test-results`/`.last-run.json`) - both disclosed as environmental limitations consistent with every prior session's own findings, not defects in this session's work. **Codex independently converges with Section 9: establish a new baseline, superseding `RBL-0020`** - "WP3 is not merely governance churn: it added a new product module, refactored a live component to use it, and added Playwright coverage for the scheduler contract. That is a meaningful repository state change future sessions should synchronize against."

---

## 11. WP5 Baseline Acceptance Result

**Establish a new baseline - [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] supersedes `RBL-0020`.** The Programme Sponsor determined at ESR-0035 WP5 to establish a new baseline, agreeing with both independent views in Sections 9-10: WP3's real product code change (a new shared animation-scheduling module, a live-component refactor, and new automated test coverage) marks a meaningfully different repository state than pure governance/backlog curation, warranting a new baseline for future sessions to synchronise against.

---

## 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108 registered (WP2); EBG-0081 closed (WP3). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Phase 1 gap closed by WP2; Section 7.4/Phase 6 updated by WP3. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for every version bump this session. |
| [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] | Prior accepted repository baseline; recommended (Section 9) to be superseded. |
| [[ESR-0034_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0034 WP4 Handover]] | Precedent handover this document follows the structure of. |
| [[ESR-0035_ENGINEERING_SESSION_REPORT|ESR-0035]] | Parent session report, authored incrementally across WP1-WP3 rather than at closure. |

---

## 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 25 July 2026 | Claude Engineering Implementer | Recorded the Programme Sponsor's WP5 determination: establish a new baseline - RBL-0021 supersedes RBL-0020, agreeing with both independent WP4 views. |
| 0.2 | 25 July 2026 | Claude Engineering Implementer | Recorded the Engineering Reviewer's (Codex) independent verification result: Pass, one reporting correction (this handover's own untracked file adds 3 further warnings; 166 vs 169 both correct, describing different scopes), pytest/Playwright sandbox-blocked (disclosed, consistent with prior sessions). Codex independently converges with Section 9: establish a new baseline, superseding RBL-0020. |
| 0.1 | 25 July 2026 | Claude Engineering Implementer | Drafted ESR-0035 WP4 Independent Repository Verification handover, covering the full session diff (`096a06b`..`2d9cf7e`) across three Work Packages (WP1 documentation debt, WP2 EBG-0108 registration, WP3 EBG-0081 Question 1 shared animation scheduler). Records repository state, authorised working set, six session observations, validation evidence, and an independent baseline view (establish a new baseline, superseding RBL-0020). Submitted to the Engineering Reviewer via the AIEMS Exchange Bridge for genuine independent verification. |
