# ESR-0028 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0028 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0028 |
| Date Opened | 18 July 2026 |
| Date Closed | 18 July 2026 |
| Closure Status | Closed - WP1-WP5 complete, session-wide WP6 Pass, WP7 Accept (new baseline RBL-0016 established) |

---

# 2. Purpose

This report records the opening and execution of ESR-0028, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0027, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) with no manual relay anywhere - every review step across all five Work Packages and the session-wide WP6 verification went through genuine `submit-to-review`/`return-findings`/`sponsor-decision` cycles. The third consecutive session run this way.

---

# 3. Scope

ESR-0028 opened with WP0A/WP0B repository synchronisation (ESR-0027 closed, RBL-0015 accepted baseline). Ahead of WP0B, two corrections were made directly on Programme Sponsor instruction: JRM-0001's overstated API-key claim in EBG-0065's rationale was corrected against direct verification, and the Programme Sponsor's decision to discontinue new HST/FCH artefact creation was formalised in GDE-0001/PBK-0001.

The Programme Sponsor selected a four-Work-Package objective at WP0B, drawn through several rounds of `AskUserQuestion` covering AIEMS process hygiene, product definition, and a UXP improvement - ultimately landing on: **WP1** (a Backlog Acceleration Opportunity bundling four small process-hygiene items), **WP2** (product requirements backlog identification), **WP3** (cost and strategic value framework), and **WP4** (Guardian Orb 3D/animation). **WP5** was added mid-session at the Programme Sponsor's request, to formally review (not implement) the rendering-engine question WP4's own investigation surfaced.

All five Work Packages completed the full real Working Report Lifecycle via the bridge: draft, Codex review (often multiple rounds), Programme Sponsor approval, implementation, commit, a second Codex review of the committed diff, and further fix cycles wherever genuine post-commit findings occurred. WP4 in particular required seven additional post-implementation fix rounds after the Programme Sponsor found a real power-usage regression through live use - not caught by any automated check. Session-wide WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance closed the session, both also conducted via the bridge, converging on establishing a new repository baseline.

---

# 4. Engineering Authority

ESR-0028 opening was authorised by Programme Sponsor instruction on 18 July 2026, following repository synchronisation confirming [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] was closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Four Work Packages, selected by the Programme Sponsor at WP0B, plus a fifth added mid-session:

- **WP1** - AIEMS Process Hygiene Batch (EBG-0058/0005/0068/0071), bundling four small, unrelated backlog items as a Backlog Acceleration Opportunity.
- **WP2** - JARVIS Product Requirements Backlog Identification (EBG-0017).
- **WP3** - Cost and Strategic Value Framework (EBG-0045/0049/0024).
- **WP4** - Guardian Orb 3D/animation (EBG-0055 Phase 1.5).
- **WP5** - Guardian Orb Rendering Engine review (ADR-0021), added at the Programme Sponsor's request following a direct concern raised during WP4's fix cycle - explicitly scoped to a decision, not an implementation.

All five were met by closure. WP4 substantially exceeded its original scope in a disclosed, live-verified way: what began as a rotation/3D delivery required seven further fix rounds after a real, Programme Sponsor-found power-usage regression, culminating in a full architectural rewrite of the animation approach.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation, PBK-0001 review, session objective selection, two pre-WP1 corrections | Complete - Section 7 |
| WP1 | AIEMS process hygiene batch (EBG-0058/0005/0068/0071) per EIP-ESR0028-001 | Complete - Section 8 |
| WP2 | JARVIS product requirements backlog identification (EBG-0017) per EIP-ESR0028-002 | Complete - Section 9 |
| WP3 | Cost and strategic value framework (EBG-0045/0049/0024) per EIP-ESR0028-003 | Complete - Section 10 |
| WP4 | Guardian Orb 3D rotation (EBG-0055 Phase 1.5) per EIP-ESR0028-004, plus seven post-implementation fix rounds | Complete - Section 11 |
| WP5 | Guardian Orb Rendering Engine decision (ADR-0021) | Complete - Section 12 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, new baseline RBL-0016 - Section 13 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[README|README.md]], [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.55), [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.27), [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] reviewed at session open.
- Repository state verified directly: `main` at `dfa13b4`, confirmed matching `origin/main`.
- Confirmed [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] the accepted baseline.
- **Two corrections made directly on Programme Sponsor instruction ahead of WP0B**: JRM-0001's EBG-0065 rationale had overstated that JARVIS held real persistent API keys - corrected after direct verification (`env`/registry checks) confirmed no persistent key exists anywhere on the machine (`18b6b48`). The Programme Sponsor's decision to discontinue new HST/FCH artefact creation (since the ESR process itself now captures session history more efficiently) was formalised as a new GDE-0001 Section 6.1 and reflected in PBK-0001's breadcrumb wording (`4428a71`).

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0028 (this report, authored at closure per established practice).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (superseded at this session's own WP7 by [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]]).
- Session objective selection presented across several `AskUserQuestion` rounds (AIEMS process hygiene vs. product definition; then a UXP improvement, specified via free-text as "Guardian Orb 3D/animation"). Programme Sponsor approved the resulting four-WP breakdown.
- WP5 was not part of the original WP0B selection - added mid-session at the Programme Sponsor's explicit request, following a concern raised directly during WP4's fix cycle about animation-cost scaling as more UXP features are added.
- Programme Sponsor approval of WP0B session opening: given directly via "Approved."

---

# 8. WP1 - AIEMS Process Hygiene Batch (EBG-0058/0005/0068/0071)

Bundled four small, unrelated backlog items as a Backlog Acceleration Opportunity per [[EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH|EIP-ESR0028-001]].

**Delivered**: 10 previously-untracked HST/FCH artefacts registered in REG-0001, closing EBG-0071 against JRM-0001's already-reserved number; EBG-0005 (26-session-old P2-004A intent) closed Resolved by Attrition; EBG-0068 (EIB artefact type) closed Superseded, confirmed via direct `git ls-files`/REG-0001 evidence that no EIB artefact was ever registered; EBG-0058 closed Complete after reviewing all three of its own named candidate clusters plus one independently-found cluster - the repository-operations-authorisation sentence, restated three times near-verbatim across PBK-0001, was consolidated to a single canonical statement with two cross-references, while three other candidate clusters were deliberately retained unchanged with disclosed reasons.

**Review cycle**: v0.1 to v0.3, addressing two Medium findings (an incomplete HST/FCH inventory that had missed `FCH-0020_GPT`; EBG-0058 scoped too narrowly against its own named candidates) and one Low finding (an incorrect JRM-0001 cross-reference number). Programme Sponsor approved v0.3. **Post-commit review: Pass, no blocking findings.**

- Commit SHA: `568aa58`
- `python -m pytest`: 286 passed. `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 9. WP2 - JARVIS Product Requirements Backlog Identification (EBG-0017)

Resolves EBG-0017 per [[EIP-ESR0028-002_JARVIS_PRODUCT_REQUIREMENTS_BACKLOG_IDENTIFICATION|EIP-ESR0028-002]].

**Investigation**: traced the item's cited source (EIP-EKR-0001, an ESR-0004 transcript-only Codex package that created EBG-0017 as future work rather than satisfying it) and surveyed all candidate existing documents. Found `JARVIS_PRODUCT_ARCHITECTURE.md` (vision/MLP/roadmap/capability hierarchy) plus the `JARVIS_CAPABILITY_READINESS_MATRIX` (per-capability maturity tracking) already provide exactly what the item asks for - identified, not created, avoiding the duplicate documentation the item's own text cautions against. Both registered in REG-0001 for the first time; the Matrix refreshed (v2.0 to v2.2 across this WP and WP4) with two rows corrected against direct evidence (Memory, Provider Architecture).

**Review cycle**: v0.1's HST/FCH-style inventory initially undercounted by one artefact (missed `FCH-0020_GPT`), caught by Codex's pre-implementation review; a separate diff-script bug produced a meaningless comparison at one point, redone manually against direct `git ls-files` evidence. v0.4 approved by the Programme Sponsor. **Post-commit review found one Low finding** (a stale EBR-0001 relationship note still crediting the Matrix's v2.0 refresh to the wrong backlog item) - fixed, then confirmed resolved.

- Commit SHAs: `1c911e5` (implementation), `beb3c01` (post-commit fix)
- `python -m pytest`: 286 passed. `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 10. WP3 - Cost and Strategic Value Framework (EBG-0045/0049/0024)

Bundles three overlapping backlog items per [[EIP-ESR0028-003_COST_AND_STRATEGIC_VALUE_FRAMEWORK|EIP-ESR0028-003]], timely since real billed provider usage now exists (EBG-0070).

**Delivered**: revised [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] rather than creating a new document - Cost reweighted from a tied-lowest 10% to a genuine first-class 15%, with an explicit no-discretionary-recurring-spend default generalising the precedent already established for EBG-0057. A Cost-Aware Routing Policy design principle was recorded for EBG-0049, explicitly excluding any dynamic routing implementation as premature given no per-request cost data exists anywhere in the repository. EBG-0024's cost-principles ask was folded into the same revision rather than left as a fourth near-duplicate item.

**Review cycle**: v0.1 incorrectly stated `TrustTierPolicy` remained unwired from production - corrected at v0.2 against direct evidence that it has been production-wired since EBG-0074. Programme Sponsor approved v0.2. **Post-commit review found one Medium finding** - the EBG-0024/EBG-0045 closure notes hadn't preserved the same explicit policy-defined-versus-code-not-implemented distinction EBG-0049's closure note already carried - fixed, then confirmed resolved.

- Commit SHAs: `6c0137c` (implementation), `6594ddb` (post-commit fix)
- `python -m pytest`: 286 passed. `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 11. WP4 - Guardian Orb 3D Rotation (EBG-0055 Phase 1.5)

Delivers EBG-0055's own explicitly-deferred continuation per [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] - this session's only product-code change, and by far its largest.

**Initial delivery**: `layoutSphere()` extended with a deterministic (id-hash, not random) front/back hemisphere sign per node, giving every node a real `(x, y, z)` sphere-surface position; a slow (~90-second) idle rotation around the Y axis; `prefers-reduced-motion` support; force parameters retuned using the Programme Sponsor's own tuned Obsidian graph-view measurements as directional signal (not literal values, given this system's hard circular containment doesn't exist in Obsidian's unbounded canvas), re-verified against the real graph. v0.1's pre-implementation review found a Medium submission-boundary finding (unrelated, direct-instruction UXP decoration-removal commits sitting in the working tree at review time, ahead of and separate from WP4's own scope) - resolved by committing those changes separately and confirming the tree clean. Programme Sponsor approved. **Post-commit review: Pass, no blocking findings.**

**Seven further live-verified fix rounds followed**, after the Programme Sponsor found a real, sustained power-usage regression via Windows Task Manager during ordinary live use - not caught by any automated check:

1. Interval throttling (50ms to 200ms) - insufficient; still "Very high," and now visibly choppy.
2. A full architectural rewrite to a ref-based `requestAnimationFrame` loop, mutating existing DOM nodes directly and bypassing React's render cycle entirely.
3. Removal of an unrelated, pre-existing `guardian-breathe` infinite box-shadow animation, found only because this investigation looked past `GuardianOrbGraph.jsx` at the wider `.guardian-orb` styling.
4. A capped update rate (~12/second).
5. Decoupled node/edge update rates (edges are ~8.6x the node count on the real graph).
6. An idle-timeout pause (45s of no interaction), with delta-based angle accumulation specifically to avoid a jump-on-resume.
7. A `visibilitychange`-based fix, after Codex correctly identified that the idle-timeout fix's pinning approach silently assumed `requestAnimationFrame` keeps firing while the window is hidden - not guaranteed by browsers.

Each round was live-verified via Playwright against the real 195-node/1,687-edge graph, or direct Task Manager comparison on real hardware. Two genuinely leaked operational processes were found and disclosed during this investigation, unrelated to the code itself: a leaked `find.exe` (from the Engineering Implementer's own earlier commands) that had confounded several Task Manager readings before being identified and killed; and three confirmed instances of the harness's `TaskStop` reporting success on a verification dev-server task without actually terminating the underlying process, prompting a standing change to the Engineering Implementer's own operational practice (always verify via `netstat`/`tasklist`, never trust `TaskStop`'s success message alone).

- Commit SHAs: `9bb31e2` (initial delivery), `c29492e`, `f56b966`, `a3e5b64`, `63325a3`, `3acb396`, `0ea8e19`, `003d8c9` (seven fix rounds)
- `python -m pytest`: 286 passed (unaffected, frontend-only). `python scripts/validate_repository.py`: 0 errors, 126 warnings. `npm run build`: clean throughout.

---

# 12. WP5 - Guardian Orb Rendering Engine Decision (ADR-0021)

Added mid-session at the Programme Sponsor's request: review, but explicitly do not implement, the rendering-engine question WP4's seven-round investigation surfaced.

**Decision**: [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] recommends migrating `GuardianOrbGraph.jsx` from SVG DOM rendering to Canvas 2D when that work is eventually scoped, grounded directly in WP4's evidence - seven rounds of real, measured optimisation reduced but never eliminated the cost, evidence that the architecture itself is the limiting factor, not any single implementation detail. WebGL/Three.js/PixiJS explicitly rejected as disproportionate to the current (~195 node) and anticipated scale. `d3-force` retained as the layout engine regardless of rendering surface. The real cost of migration (losing SVG's free hit-testing/tooltips/DOM-accessibility) is disclosed, not glossed over.

**Review cycle**: three rounds, all wording/lifecycle-accuracy findings rather than technical disagreement - the package initially overstated a still-Draft ADR's effect on EBG-0081's backlog status, corrected across two follow-up rounds (the same wording issue was missed in one table and only caught in a second pass). No technical objection to the Canvas 2D recommendation was raised at any point. Programme Sponsor approved. Applied a split disposition to EBG-0081: the rendering-engine half Complete via this ADR, the separately-raised shared-animation-scheduler half remains open Candidate Backlog.

- Commit SHA: `eb5ed32`
- `python -m pytest`: 286 passed (unaffected, no code touched). `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 13. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**PST-0001 catch-up**: ahead of WP6, found PST-0001 had not been updated throughout WP1-WP5 (a gap against the pattern established at ESR-0026/ESR-0027). Caught up (`48ea84e`) before drafting the handover, rather than left for session closure.

**Handover preparation**: an [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0028 WP6 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session diff (`dfa13b4`..`48ea84e`) across all five Work Packages.

**Session-wide WP6 (Independent Repository Verification)**: Codex independently confirmed repository state at `48ea84e` matched the handover's claims exactly - the full diff stat (19 files, 1,360 insertions, 307 deletions), the authorised working set, scope boundaries (no `sentinel/` or backend Python code touched anywhere in the session), and accurate disclosure of WP4's seven-round fix history and the two leaked-process incidents. **Pass, no findings.**

**Session-wide WP7 (Repository Baseline Acceptance): new baseline [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] established, superseding RBL-0015.** Both independent views converged, diverging from the retain-RBL-0015 pattern of the last two sessions: WP4's Guardian Orb change is materially different in kind from ESR-0026/ESR-0027's backend-only or trivial-UXP-subtraction changes - `GuardianOrbGraph.jsx` alone changed by 362 net lines across eight commits, the Guardian Orb is the flagship visual presence of the running UXP, and both its appearance and behaviour changed, extensively live-verified by the Programme Sponsor across the session. Programme Sponsor's own determination: **Accept - new baseline RBL-0016 established.**

- Commit SHAs: `6752312` (WP6 handover, Pass), `0104426` (WP7 closure, RBL-0016)
- `python -m pytest`: 286 passed. `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour; revised this session (WP1). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Eight backlog items closed Complete this session; EBG-0081 registered mid-session and split-dispositioned. |
| [[EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH|EIP-ESR0028-001]] | Approved-implemented package for WP1, v1.0. |
| [[EIP-ESR0028-002_JARVIS_PRODUCT_REQUIREMENTS_BACKLOG_IDENTIFICATION|EIP-ESR0028-002]] | Approved-implemented package for WP2, v1.0. |
| [[EIP-ESR0028-003_COST_AND_STRATEGIC_VALUE_FRAMEWORK|EIP-ESR0028-003]] | Approved-implemented package for WP3, v1.0. |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | Approved-implemented package for WP4, v1.0. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved decision for WP5, v1.3. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Revised this session (WP3), not created new. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Registered in REG-0001 for the first time this session (WP2). |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Registered in REG-0001 for the first time and refreshed to v2.2 this session (WP2, WP4). |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Orb visual presence architecture, continued (WP4) and its rendering surface decided (WP5). |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0028 WP6 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.3, Section 13. |
| [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] | Prior closed session this one continues from. |
| [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] | New repository baseline established at Section 13. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0-WP5, the session-wide WP6 Independent Repository Verification (Pass, no findings) and WP7 Repository Baseline Acceptance (new baseline RBL-0016 established, superseding RBL-0015). Third session run entirely through the AIEMS Exchange Bridge with no manual relay. Status Open to Closed. |
