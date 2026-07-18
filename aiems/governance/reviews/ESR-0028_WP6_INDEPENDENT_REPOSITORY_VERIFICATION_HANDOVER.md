# ESR-0028 WP6 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0028-WP6 |
| Title | Independent Repository Verification Handover |
| Version | 0.2 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0028 (open; no session report artefact yet - authored later per the practice established at ESR-0022 through ESR-0027) |
| Effective Date | 18 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0028's session-wide record for WP6 Independent Repository Verification. WP6 should confirm that the current repository state matches the claims made across all five of ESR-0028's Work Packages, that disclosed scope boundaries and defects are accurately characterised, and that no unauthorised scope drift occurred. Submitted to Codex via the AIEMS Exchange Bridge for genuine independent verification, continuing the same real-cycle practice used throughout WP1-WP5.

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Local `HEAD` | `48ea84e` |
| `origin/main` | `48ea84e` (pushed, confirmed matching) |
| Working tree | Committed tree clean at `48ea84e`; working tree has only this untracked WP6 handover document itself |
| Prior accepted baseline | `RBL-0015` |
| ESR-0028 session start point | `dfa13b4` (ESR-0027's closing commit) |

---

## 4. ESR-0028 Commits in Scope

| Commit | Summary |
|---|---|
| `18b6b48` | WP0: corrected JRM-0001's overstated API-key claim in EBG-0065's rationale, per direct Programme Sponsor correction. |
| `4428a71` | WP0: discontinued new HST/FCH artefact creation, per Programme Sponsor decision, formalised in GDE-0001/PBK-0001. |
| `568aa58` | WP1: AIEMS process hygiene batch (EBG-0058/0005/0068/0071) per EIP-ESR0028-001 v0.3. |
| `1c911e5` | WP2: JARVIS product requirements backlog identification (EBG-0017) per EIP-ESR0028-002 v0.4. |
| `beb3c01` | WP2 fix: corrected a stale EBG-0069 reference in the Readiness Matrix, per Codex post-commit finding. |
| `6c0137c` | WP3: cost and strategic value framework (EBG-0045/0049/0024) per EIP-ESR0028-003 v0.2. |
| `6594ddb` | WP3 fix: preserved the policy-vs-implementation distinction in EBG-0024/0045 closure notes, per Codex post-commit finding. |
| `a5a19be`, `070eb2a` | Direct Programme Sponsor-instructed UXP decoration removal (concentric rings, greeting text, remaining orb border/glow/rings) - unrelated to and predating WP4's own scope. |
| `9bb31e2` | WP4: Guardian Orb 3D rotation (EBG-0055 Phase 1.5) per EIP-ESR0028-004 v0.1. |
| `c29492e`, `f56b966`, `a3e5b64`, `63325a3`, `3acb396`, `0ea8e19`, `003d8c9` | WP4's seven post-implementation fix rounds, following a real Programme Sponsor-observed power-usage regression: interval throttling (insufficient), a ref-based `requestAnimationFrame` rewrite, removal of an unrelated pre-existing box-shadow animation, a capped update rate, decoupled node/edge update frequencies, an idle-timeout pause, and a `visibilitychange`-based fix for a hidden-window resume race. |
| `eb5ed32` | WP5: ADR-0021 approved (Guardian Orb rendering engine decision - Canvas 2D, decision only). |
| `48ea84e` | WP6 prep: PST-0001 catch-up for WP1-WP5 (found not updated throughout the session). |

---

## 5. Authorised / Explained Working Set

The full ESR-0028 diff since `dfa13b4` (19 files changed, 1,360 insertions, 307 deletions):

**WP0 (session opening, ahead of WP1):**
1. `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md` - corrected an overstated API-key claim.
2. `aiems/guides/GDE-0001_PROJECT_KNOWLEDGE_MAP.md` - HST/FCH discontinuation formalised (from the immediately preceding session's closing decision, carried into this diff range since it landed after `dfa13b4`).

**WP1 (AIEMS process hygiene, EBG-0058/0005/0068/0071):**
3. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md` - repository-operations-authorisation cluster consolidated (Session Initialisation item 14 canonical, two restatements cross-referenced), RBL-0014 to RBL-0015 fixed.
4. `aiems/governance/reviews/EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH.md` - new, Approved-implemented v1.0.

**WP2 (product requirements backlog identification, EBG-0017):**
5. `aiems/governance/reviews/EIP-ESR0028-002_JARVIS_PRODUCT_REQUIREMENTS_BACKLOG_IDENTIFICATION.md` - new, Approved-implemented v1.0.
6. `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md` - registered in REG-0001 for the first time; Document Control identity field corrected (Document ID to Artefact ID).
7. `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md` - registered in REG-0001 for the first time; refreshed to v2.2 (Memory and Provider Architecture rows corrected against direct evidence, RBL-0014 to RBL-0015 fixed, a stale EBG-0069 reference corrected).

**WP3 (cost and strategic value framework, EBG-0045/0049/0024):**
8. `aiems/evaluations/PEM-001_AI_PROVIDER_EVALUATION_MATRIX.md` - Cost reweighted (10% to 15%), Cost and Strategic Value Principles and Cost-Aware Routing Policy sections added.
9. `aiems/governance/reviews/EIP-ESR0028-003_COST_AND_STRATEGIC_VALUE_FRAMEWORK.md` - new, Approved-implemented v1.0.

**WP4 (Guardian Orb 3D rotation, EBG-0055 Phase 1.5, plus direct-instruction UXP cleanup):**
10. `src/GuardianOrbGraph.jsx` - full-sphere coordinates, real Y-axis rotation, `prefers-reduced-motion` support, retuned force parameters, then seven further rounds of performance fixes (ref-based rAF, capped/decoupled update rates, idle-timeout and hidden-window pausing).
11. `src/App.jsx` - decorative orbital-field rings and greeting/status text block removed (direct Programme Sponsor instruction), now-dead `deriveGuardianStatus()` removed.
12. `src/platformStatus.js` - now-orphaned `guardianStatus` export removed.
13. `src/styles.css` - decorative ring/glow CSS removed (direct instruction), plus a pre-existing, unrelated infinite box-shadow animation (`guardian-breathe`) found and removed during WP4's power-usage investigation.
14. `aiems/governance/reviews/EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION.md` - new, Approved-implemented v1.0.

**WP5 (Guardian Orb rendering engine decision, ADR-0021):**
15. `aiems/governance/decisions/ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE.md` - new, Approved v1.3. Decision only - no implementation.

**Governance (session-wide, all WPs):**
16. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - EBG-0058/0005/0068/0071/0017/0045/0049/0024 all Complete; EBG-0081 split disposition (rendering-engine half Complete, shared-scheduler half Candidate Backlog); EBG-0081 itself newly registered mid-session.
17. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - registers all four new EIPs, ADR-0021, JARVIS_PRODUCT_ARCHITECTURE, JARVIS_CAPABILITY_READINESS_MATRIX; version-aligns every touched artefact throughout.
18. `aiems/governance/registers/REG-0002_ADR_REGISTER.md` - registers ADR-0021.
19. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md` - Current Mode/Phase/Workflow/Objective and Current Engineering Focus caught up for WP1-WP5 (a gap found ahead of this WP6 handover - PST-0001 was not updated throughout the session's own WPs, unlike ESR-0027's per-WP update pattern).

No files outside this set were touched. No `sentinel/` (trust boundary/policy) code was modified anywhere in the session. No backend Python code (`jarvis/`) was modified - WP2's `JARVIS_CAPABILITY_READINESS_MATRIX.md`/`JARVIS_PRODUCT_ARCHITECTURE.md` changes are architecture documents, not code, despite living under `jarvis/`.

---

## 6. Session Observations

1. **All five Work Packages completed the full real review cycle** via the AIEMS Exchange Bridge - draft, `submit-to-review`, Codex's `return-findings`, `sponsor-decision`, implementation, commit, a second `submit-to-review` of the committed diff, and a final `return-findings` confirmation. No manual relay anywhere, across a third consecutive session.
2. **WP1-WP3 and WP5 were governance-only** (no product code touched); each closed cleanly with at most one or two review rounds of genuine, evidence-grounded findings (e.g. WP1's incorrect JRM-0001 sub-section citation corrected to the real reserved section; WP3's TrustTierPolicy production-wiring status corrected after being stated incorrectly; WP5's overstated Draft-ADR-effect wording, caught twice before fully resolved).
3. **WP2 required self-correction of the Engineering Implementer's own investigation twice**: an initial HST/FCH inventory undercounted by one artefact (missed `FCH-0020_GPT`), caught by Codex's pre-implementation review; a later diff-script bug produced a meaningless comparison, redone manually against direct `git ls-files` evidence.
4. **WP4 is this session's only product-code change, and by far its largest and most iteratively-corrected**: the initial delivery (`9bb31e2`) passed pre- and post-commit review cleanly, but the Programme Sponsor found a real, measured power-usage regression via Windows Task Manager after live use - not caught by any automated check. Seven further rounds followed, each independently live-verified (Playwright against the real 195-node/1,687-edge graph, or direct Task Manager comparison on real hardware):
   - Interval throttling (50ms to 200ms) - insufficient; Programme Sponsor reported it was still "Very high" and now visibly choppy.
   - A full architectural rewrite to a ref-based `requestAnimationFrame` loop, bypassing React's render cycle entirely.
   - Removal of an unrelated, pre-existing `guardian-breathe` infinite box-shadow animation, found only because this investigation looked past `GuardianOrbGraph.jsx` at the wider `.guardian-orb` styling.
   - A capped update rate (~12/second), then decoupled node/edge update rates (edges are ~8.6x the node count).
   - An idle-timeout pause (45s of no interaction) with delta-based angle accumulation to avoid a jump-on-resume.
   - A `visibilitychange`-based fix, after Codex correctly identified that the idle-timeout fix's "keep pinning `lastFrame`" approach silently assumed `requestAnimationFrame` keeps firing while hidden - not guaranteed by browsers.
   - Codex's post-commit reviews caught two further genuine, real issues across this sequence: a submission-boundary mix-up (unrelated direct-instruction UXP commits sitting in the working tree at review time) and the rAF-suspension race just described.
5. **A separate, real leaked-process incident occurred mid-investigation, unrelated to the code itself**: `TaskStop` reported success on a verification dev-server task but the underlying `node.exe` child survived anyway, three times in this session alone (plus a fourth confirmed instance on a different port). A separate leaked `find.exe` process (from the Engineering Implementer's own earlier commands) was also found and killed, having confounded several of the Task Manager comparisons taken during the investigation before being identified. Both are disclosed as genuine operational incidents, not silently corrected - the Engineering Implementer's own persistent memory was updated mid-session to no longer trust `TaskStop`'s success message without independent `netstat` verification.
6. **WP5 (ADR-0021) is decision-only, matching the Programme Sponsor's explicit instruction to "review... but not implement"** - no product code is touched by this WP; the Canvas 2D recommendation is grounded directly in WP4's seven-round evidence and received no technical objection from Codex across three review rounds (all findings were wording/lifecycle-accuracy issues, not disagreement with the recommendation itself).
7. **PST-0001 was not updated throughout WP1-WP5**, a real process gap against the pattern established at ESR-0026/ESR-0027 (where PST-0001 was updated at each WP's closure). Found and caught up (`48ea84e`) immediately ahead of this WP6 handover, rather than left for session closure.
8. **EBG-0081 was registered mid-session** (during WP4) and given a split disposition at WP5 - a candidate-backlog item created and partially closed within the same session, rather than carried forward, since the rendering-engine half of its question could be genuinely resolved once WP4's evidence existed.

---

## 7. Validation Evidence

Re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 286 passed |
| `python scripts/validate_repository.py` (full, not governance-only) | 0 errors, 126 warnings |
| `npm run build` | Clean (confirmed after every WP4 code change) |
| `git diff --check dfa13b4..48ea84e` | Clean - no whitespace issues in the full session range. |
| `git status` | Committed tree clean on `main` at `48ea84e`, matching `origin/main`; working tree has only this untracked WP6 handover document, per the same convention used at ESR-0026/ESR-0027's own WP6 handovers. |

The 126 warnings are the session's stable, pre-existing baseline throughout - no new warnings were introduced by any WP's final committed state (several intermediate drafts introduced and then self-corrected transient warnings from the `SECTION_REF_PATTERN` heuristic matching quoted section-number text in changelog prose, disclosed and fixed in-session each time, per WP1/WP3/WP5's own version histories).

---

## 8. Scope Check

- No `sentinel/` (trust boundary/policy classification) code was touched anywhere in the session.
- No backend Python code (`jarvis/`) was modified - all `jarvis/`-path changes are architecture/documentation files (`JARVIS_PRODUCT_ARCHITECTURE.md`, `JARVIS_CAPABILITY_READINESS_MATRIX.md`), not code.
- `src/` (UXP) was touched only in WP4 and the two direct-instruction cleanup commits, all disclosed, all live-verified, all confirmed by Codex with no outstanding findings.
- WP5 (ADR-0021) touches zero code, consistent with its explicit decision-only scope.
- Both self-found operational defects (leaked `find.exe`, `TaskStop` unreliability) are disclosed in Section 6, not silently worked around.
- The working tree is clean and pushed; this handover document is the sole untracked file, being this review's own subject.

---

## 9. WP7 Baseline Recommendation

**Engineering Implementer's independent view:** cut a new baseline, `RBL-0016`.

Rationale: this session's product-code change (WP4) is materially different in kind from the backend-only changes that warranted retaining `RBL-0015` at ESR-0026 and ESR-0027. The Guardian Orb is the flagship visual centrepiece of the running UXP - the first thing any user sees on opening the app - and this session changed both its appearance (decorative rings, border, glow and greeting text all removed, per direct Programme Sponsor instruction) and its behaviour (it now genuinely rotates, driven by real graph data, where it was previously a static rendering). This is not a cosmetic tidy-up comparable to EBG-0073/EBG-0077's static-row removals (three-line net subtractions); `GuardianOrbGraph.jsx` alone changed by 362 lines net across eight commits, and the Programme Sponsor personally live-verified the result multiple times across the session (screenshots, Task Manager comparisons, direct feedback that shaped seven consecutive fix rounds). This matches the substance of the test `RBL-0015` itself was cut against - a genuine change to what the running product actually does for a user today - more closely than it matches the retained-baseline precedents.

**Engineering Reviewer's independent view (Codex):** converges - cut a new baseline, `RBL-0016`. Unlike ESR-0026/ESR-0027's retained-baseline cases, ESR-0028 materially changed the running UXP's flagship Guardian Orb appearance and behaviour, with 362 net lines in `GuardianOrbGraph.jsx` plus related visual cleanup and extensive Programme Sponsor live verification - a user-visible product capability/experience change comparable in substance to the prior baseline-triggering UXP/provider milestones, not merely governance churn or a small static-row subtraction. Reached independently, via the bridge, before comparison with the Engineering Implementer's own view above.

---

## 10. WP6 Verification Result

**Pass, no findings.** The Engineering Reviewer (Codex) independently verified repository state at `48ea84e` against this handover's claims, via the AIEMS Exchange Bridge (`.aiems-exchange/codex/outbox/20260718T232149Z-return-findings.md`):

1. Confirmed the full diff stat matches Section 5 exactly: 19 files changed, 1,360 insertions, 307 deletions.
2. Confirmed the file list matches Section 5's authorised/explained working set exactly - governance EIPs/ADR/register/status/playbook/roadmap/guide/evaluation files, two JARVIS architecture documents, and the disclosed WP4/direct-instruction UXP files.
3. Confirmed no `sentinel/` code and no backend Python code are in the diff.
4. Confirmed `HEAD` is `48ea84e` on `main`/`origin/main`, with the only untracked file being this handover itself, matching the stated convention.
5. Confirmed ADR-0021 is committed as Approved v1.3 in REG-0001, REG-0002 and the ADR text; EBG-0081's split disposition recorded accurately in EBR-0001.
6. Confirmed PST-0001 is aligned to v2.56, records ESR-0028 open with WP6 in progress, and RBL-0015 still the current baseline pending WP7.
7. Confirmed validation evidence: `pytest` 286 passed, `validate_repository.py` 0 errors/126 baseline warnings, `npm run build` clean, `git diff --check dfa13b4..48ea84e` clean.
8. Reached an independent WP7 view (Section 9) converging with the Engineering Implementer's own view.

No blocking findings on the implemented WP1-WP5 scope. WP7 (Repository Baseline Acceptance) is a Programme Sponsor determination, informed by both independent views in Section 9.

---

## 11. WP7 Baseline Acceptance Result

**Pending Programme Sponsor determination**, informed by both independent views in Section 9, which converge on cutting a new baseline `RBL-0016`.

---

## 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH|EIP-ESR0028-001]] | Approved-implemented package for WP1, v1.0. |
| [[EIP-ESR0028-002_JARVIS_PRODUCT_REQUIREMENTS_BACKLOG_IDENTIFICATION|EIP-ESR0028-002]] | Approved-implemented package for WP2, v1.0. |
| [[EIP-ESR0028-003_COST_AND_STRATEGIC_VALUE_FRAMEWORK|EIP-ESR0028-003]] | Approved-implemented package for WP3, v1.0. |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | Approved-implemented package for WP4, v1.0. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved decision for WP5, v1.3. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Eight backlog items closed this session; EBG-0081 registered and split-dispositioned. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status, caught up ahead of this handover. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for the session's controlled artefacts. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Prior accepted repository baseline; recommended for replacement at Section 9. |
| [[ESR-0027_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0027 WP6 Handover]] | Precedent handover this document follows the structure of. |

---

## 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Recorded WP6 verification result: **Pass, no findings**. Engineering Reviewer (Codex) independently confirmed repository state, scope characterisation and disclosed session observations via the AIEMS Exchange Bridge, and provided an independent baseline view (cut new baseline `RBL-0016`) converging with the Engineering Implementer's own view. WP7 now awaits the Programme Sponsor's own determination. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Drafted ESR-0028 WP6 Independent Repository Verification handover, covering the full session diff (`dfa13b4`..`48ea84e`) across five Work Packages. Records repository state, authorised working set, session observations (WP4's seven-round fix history, two leaked-process incidents, the PST-0001 catch-up gap), validation evidence, and an independent baseline view (cut new baseline `RBL-0016`, diverging from the retain-RBL-0015 pattern of the last two sessions, given WP4's substantial, live-verified UXP change) for WP7 consideration. Submitted to the Engineering Reviewer via the AIEMS Exchange Bridge for genuine independent verification. |
