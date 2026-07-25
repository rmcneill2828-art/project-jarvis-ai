# ESR-0035 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0035 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0035 |
| Date Opened | 25 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1, WP2, WP3 complete |

---

# 2. Purpose

This report records the opening and execution of ESR-0035, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0034_ENGINEERING_SESSION_REPORT|ESR-0034]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

During WP0A repository synchronisation, the Engineering Implementer found that README.md, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] each still cited [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] as the current accepted repository baseline, and README.md's top Project Status table and Current Roadmap Phase 2 section still described ESR-0033 as the currently open session with ESR-0032 as the latest closed session. [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] has been the accepted baseline since ESR-0033 WP9 (25 July 2026), retained at ESR-0034 WP5; both ESR-0033 and ESR-0034 have since closed. This finding was not already tracked in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].

Per PBK-0001's Documentation-Debt Priority Until Backlog Cleared discipline, the Programme Sponsor directed this be WP1.

For WP2, the Programme Sponsor directed closing [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]'s own flagged gap: Track B Section 7.1/7.3 names Guardian Cognitive Core as Phase 1 of the Path to a Working Version, with "no backlog item yet authorises this build" - called out at ESR-0034 WP3 as the single most consequential gap in the whole roadmap.

WP1 and WP2 were both governance/backlog-only, touching no product code. Per PBK-0001's Feature-First Delivery Discipline, every Engineering Session must include work that moves JARVIS/Guardian forward, not governance alone - so WP3 was selected from [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]'s Approved Backlog: EBG-0081 Question 1 (UXP shared animation scheduler), a well-scoped, contained frontend feature with confirmed prior art (EBG-0082).

---

# 4. Engineering Authority

ESR-0035 opening was authorised by direct Programme Sponsor instruction on 25 July 2026, immediately following ESR-0034's closure, confirming [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] as the accepted repository baseline at session open.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Correct the stale RBL-0019/ESR-0033 current-state references identified during WP0A, applying PBK-0001's Whole-Document Staleness Sweep on Edit discipline to each affected document, then close JRM-0001's own flagged Guardian Cognitive Core backlog-authorisation gap, before selecting further engineering work for this session.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | Correct stale RBL-0019/ESR-0033 current-state references in README.md, COC-0001, PBK-0001 and REG-0001 | Complete |
| WP2 | Register EBG-0108 (Guardian Cognitive Core Implementation) to Approved Backlog, closing JRM-0001's flagged Phase 1 gap | Complete |
| WP3 | Deliver EBG-0081 Question 1 (UXP shared animation scheduler) - this session's required product-moving work | Complete |

---

# 7. WP1 - Documentation Debt: RBL-0019/ESR-0033 Staleness Correction

Corrected all active current-state references in README.md, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] from [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]]/ESR-0033/ESR-0032 to [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]]/ESR-0035/ESR-0034, applying PBK-0001's Whole-Document Staleness Sweep on Edit discipline to each document rather than fixing only the originally-cited lines. Added a version-history entry to each of the three documents, aligned [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]'s PBK-0001/COC-0001 tracking rows and REG-0001's own version, and registered this ESR-0035 report itself. No governance artefact meaning changed - only current-state accuracy.

Run entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service (ADR-0022): `submit-to-review` with the full evidence bundle, an independent Codex read-only review (Pass, no findings - relayed into the bridge by the Engineering Implementer under explicit Programme Sponsor approval for the relay act, per the EBG-0096 read-only-plus-relay precedent, since Codex's own sandbox cannot write the bridge's lock file directly), Programme Sponsor approval via the Sponsor Approval Service, `submit-response`, then commit and push.

- Commit SHA: `c939ecf`
- `python -m pytest`: 374 passed, 1 skipped (unchanged - no code touched). `python scripts/validate_repository.py` (full mode, pre-commit hook): 0 errors, 157 warnings (unchanged baseline).
- **Post-commit independent verification**: Codex re-reviewed the actual pushed diff (`git show c939ecf`) in a fresh read-only pass and independently re-ran `validate_repository.py` - **Pass**, confirming the committed content matches what was reviewed pre-commit.

---

# 8. WP2 - Guardian Cognitive Core Backlog Registration (EBG-0108)

Registered [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 (Guardian Cognitive Core Implementation) directly to Approved Backlog, on Programme Sponsor direction, closing [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B's own flagged gap: Section 7.1/7.3 named Guardian Cognitive Core as Phase 1 of the Path to a Working Version with "no backlog item yet authorises this build" - called out at ESR-0034 WP3 as the single most consequential gap in the whole roadmap, since every later phase (Action faculty, Memory expansion, Knowledge Graph Phase 4, Voice/Vision) either extends this core or depends on it existing. [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] (v0.3, Approved) remains architecture only - no implementation is authorised by this registration. Updated JRM-0001 Sections 7.1 and 7.3 to record the registration.

Run entirely through the AIEMS Exchange Bridge and the deployed Sponsor Approval Service, the same pattern as WP1: `submit-to-review`, independent Codex read-only review (Pass, no findings, relayed under explicit Programme Sponsor approval), Programme Sponsor approval, `submit-response`, commit and push, then post-commit independent re-verification.

- Files: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (EBG-0108 entry, version history), [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (Sections 7.1/7.3, version history), [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] (EBR-0001/JRM-0001/PST-0001 tracking rows and version), [[PST-0001_PROGRAMME_STATUS|PST-0001]] (Current Mode/Phase/Workflow/Objective, Section 4A).
- `python -m pytest`: 374 passed, 1 skipped (unchanged - no code touched). `python scripts/validate_repository.py` (full mode): 0 errors, 162 warnings (incremental growth from new version-history entries, consistent with the established pattern).
- Codex's first read-only pass found two stale warning-count mentions (PST-0001 said 157, this section said 159, actual was 162) - both corrected; a second Codex pass reconfirmed the fix (Pass).
- Commit SHA: `f471648`, pushed (`bd11c8f..f471648`).
- **Post-commit independent verification**: Codex re-reviewed the actual pushed diff (`git show f471648`) in a fresh read-only pass - **Pass**.

---

# 9. WP3 - EBG-0081 Question 1: UXP Shared Animation Scheduler

Delivered EBG-0081 Question 1, selected as this session's required product-moving work per PBK-0001's Feature-First Delivery Discipline (WP1 and WP2 were both governance/backlog-only). `src/animationScheduler.js` (new): a singleton shared clock exposing `subscribe(callback) -> unsubscribe`, running a single `requestAnimationFrame` loop started lazily on the first subscriber and stopped once the last unsubscribes - so nothing runs when nothing is animating. A subscriber that throws is caught and logged rather than breaking other subscribers' frames, since a shared driver is more fragile than each element running its own private loop.

`src/GuardianOrbGraph.jsx` refactored: its own private `requestAnimationFrame`/`cancelAnimationFrame` calls replaced with `subscribe`/`unsubscribe` from the new module - identical tick logic, throttling, idle and visibility-change handling, no behavioural change intended. No other UXP element currently animates continuously, so this WP builds the driver and migrates the one existing consumer; future animated elements (e.g. a Phase 6 voice waveform) register with it later, as EBG-0081 itself anticipated.

Verification: `npm run build` clean. The existing Playwright suite's 2 tests still pass unchanged - they already mount the Orb with mocked graph data, so they exercise the new scheduler path. Three new dedicated tests added in `tests/e2e/animationScheduler.spec.js`, proving the scheduler's actual contract: a shared single `requestAnimationFrame` loop regardless of subscriber count, a throwing subscriber not affecting others, and the loop stopping once the last subscriber unsubscribes. The first version of the shared-loop test asserted on real rAF timing and proved flaky in headless Chromium (frame counts too low/jittery over a fixed wait to assert reliably); rewritten against a fully deterministic fake `requestAnimationFrame` that only fires when the test explicitly steps it, removing the timing dependency entirely. A separate, uncommitted, ad hoc Playwright check (deleted after use) confirmed the Orb canvas genuinely still changes frame-to-frame in the running app - two `toDataURL()` snapshots two seconds apart differed.

Updated [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (EBG-0081 status Approved Backlog to Complete - both questions now closed) and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (Section 7.4 and the Phase 6 Voice/Vision row in Section 7.3).

Run through the same AIEMS Exchange Bridge / Sponsor Approval Service cycle as WP1/WP2.

- Files: `src/animationScheduler.js` (new), `src/GuardianOrbGraph.jsx`, `tests/e2e/animationScheduler.spec.js` (new), [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[JRM-0001_PROJECT_ROADMAP|JRM-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]], [[PST-0001_PROGRAMME_STATUS|PST-0001]].
- `python -m pytest`: 374 passed, 1 skipped (unchanged - no Python touched). `npx playwright test`: 5 passed (2 existing, 3 new). `npm run build`: clean. `python scripts/validate_repository.py` (full mode): 0 errors, 166 warnings.

---

# 10. Related Artefacts

* [[ESR-0034_ENGINEERING_SESSION_REPORT|ESR-0034]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Documentation Debt Discipline, applied by WP1.
* [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] - current accepted repository baseline, the corrected target reference.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - authoritative backlog; WP1's staleness finding was not already tracked here, WP2 added EBG-0108, WP3 closed EBG-0081.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Phase 1 gap closed by WP2's EBG-0108 registration; Section 7.4/Phase 6 updated by WP3's EBG-0081 delivery.
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] - existing Approved architecture EBG-0108 would build against.

---

# 11. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP3 Complete: delivered EBG-0081 Question 1 (UXP shared animation scheduler) - this session's required product-moving work per PBK-0001's Feature-First Delivery Discipline. |
| 1.1 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP2 Complete: registered EBG-0108 (Guardian Cognitive Core Implementation) to Approved Backlog, closing JRM-0001's flagged Phase 1 gap. |
| 1.0 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 opened. WP1 (RBL-0019/ESR-0033 documentation debt correction) in progress. |
