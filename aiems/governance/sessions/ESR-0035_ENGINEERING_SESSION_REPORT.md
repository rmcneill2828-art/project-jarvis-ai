# ESR-0035 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0035 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0035 |
| Date Opened | 25 July 2026 |
| Date Closed | 25 July 2026 |
| Closure Status | Closed - WP1-WP3 complete, session-wide WP4 Pass, WP5 Establish (RBL-0021 accepted) |

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
| WP4 | Session-wide Independent Repository Verification | Complete - Pass |
| WP5 | Session-wide Repository Baseline Determination | Complete - Establish (RBL-0021) |

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

# 10. Session-Wide WP4 - Independent Repository Verification

**Handover preparation**: an [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0035 WP4 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session content range (`096a06b`..`2d9cf7e`) across all three Work Packages.

**Pass, one reporting correction, no blocking findings**: Codex independently confirmed `git diff --stat 096a06b..2d9cf7e` matches the handover's claimed 11 files/368 insertions/48 deletions exactly, and that no `sentinel/`, `jarvis/`, `src-tauri/` or `.github/workflows/` file was touched anywhere in the diff. The one reporting correction: the handover file itself, being untracked at review time, adds 3 further warnings of its own (169 including it, versus 166 for the session-content diff alone) - both figures independently confirmed correct for their respective scopes, not a contradiction. Codex's own read-only sandbox could not independently reproduce `python -m pytest` or `npx playwright test` (temp-directory/write restrictions), a disclosed environmental limitation consistent with prior sessions, not a defect. Codex independently converged with the handover's own baseline recommendation: establish a new baseline, superseding RBL-0020.

- Commit SHA: pending (handover committed as part of session closure)
- `python -m pytest`: 374 passed, 1 skipped. `npx playwright test`: 5 passed. `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings (final count at session close, including this handover's own prose plus subsequent closure-narrative additions).

---

# 11. Session-Wide WP5 - Repository Baseline Determination (RBL-0021 Established)

**Both independent WP4 views recommended establishing a new baseline** rather than retaining the current one: WP3 delivered a genuine, live-verified product code change (a new shared UXP animation-scheduling module, a live-component refactor, and new automated test coverage), unlike ESR-0034's entirely governance/roadmap-only content. The Programme Sponsor's determination: **establish** - [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] is accepted as the new current repository baseline, superseding [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]].

- Commit SHA: pending (recorded as part of session closure)
- `python -m pytest`: 374 passed, 1 skipped throughout. `npx playwright test`: 5 passed. `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings.

---

# 12. Governance Process Notes

One real scope expansion occurred at this session's opening: WP0A repository synchronisation surfaced the RBL-0019/ESR-0033 documentation debt finding, and the Programme Sponsor directed it become WP1 before any other engineering objective was selected - flagged plainly before proceeding, consistent with the standing scope-creep-flagging practice. A second, deliberate expansion occurred after WP2: since WP1/WP2 were both governance-only, the Programme Sponsor directed WP3 add real product-moving work per PBK-0001's Feature-First Delivery Discipline, rather than closing the session at WP2.

No environment gaps or lost background processes occurred this session. The one tooling limitation encountered (Codex's read-only sandbox cannot reproduce `pytest`/Playwright, or write its own scheduling lock file for `return-findings`) was already known and disclosed from prior sessions, handled throughout via the standing EBG-0096 read-only-plus-relay pattern (Codex reviews read-only; the Engineering Implementer relays its verbatim findings into the bridge under explicit per-instance Programme Sponsor approval).

Every Work Package in this session followed the full cycle without exception: draft, Codex read-only review (relayed via `return-findings` under explicit per-instance Sponsor approval), a fix round wherever findings existed (WP2 and WP3 each had at least one genuine finding, both stale warning-count mentions), a second Codex confirmation pass where a fix round occurred, Sponsor approval via the real deployed Sponsor Approval Service, `submit-response`, then commit - including the session-wide WP4/WP5 activities themselves.

---

# 13. Related Artefacts

* [[ESR-0034_ENGINEERING_SESSION_REPORT|ESR-0034]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Documentation Debt Discipline (WP1) and Feature-First Delivery Discipline (WP3), both applied this session.
* [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] - current accepted repository baseline, established at this session's WP5.
* [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] - prior accepted repository baseline, superseded by RBL-0021.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - authoritative backlog; WP1's staleness finding was not already tracked here, WP2 added EBG-0108, WP3 closed EBG-0081.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Phase 1 gap closed by WP2's EBG-0108 registration; Section 7.4/Phase 6 updated by WP3's EBG-0081 delivery.
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] - existing Approved architecture EBG-0108 would build against.
* [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0035 WP4 Handover]] - session-wide Independent Repository Verification and Baseline Determination record, Section 10/11.

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 formally closed. Session-wide WP4 (Independent Repository Verification: Pass, one reporting correction) and WP5 (Repository Baseline Determination: Establish - RBL-0021 accepted, superseding RBL-0020) complete. |
| 1.2 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP3 Complete: delivered EBG-0081 Question 1 (UXP shared animation scheduler) - this session's required product-moving work per PBK-0001's Feature-First Delivery Discipline. |
| 1.1 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP2 Complete: registered EBG-0108 (Guardian Cognitive Core Implementation) to Approved Backlog, closing JRM-0001's flagged Phase 1 gap. |
| 1.0 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 opened. WP1 (RBL-0019/ESR-0033 documentation debt correction) in progress. |
