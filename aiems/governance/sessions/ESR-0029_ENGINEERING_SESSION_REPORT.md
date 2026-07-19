# ESR-0029 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0029 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0029 |
| Date Opened | 19 July 2026 |
| Date Closed | 19 July 2026 |
| Closure Status | Closed - WP1-WP7 complete, session-wide WP8 Pass, WP9 Accept (new baseline RBL-0017 established) |

---

# 2. Purpose

This report records the opening and execution of ESR-0029, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0028, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) with no manual relay anywhere - every review step across all seven Work Packages and the session-wide WP8/WP9 verification went through genuine `submit-to-review`/`return-findings`/`sponsor-decision` cycles. The fourth consecutive session run this way.

---

# 3. Scope

ESR-0029 opened with a session objective selected via several `AskUserQuestion` rounds. Rather than pick from the offered options, the Programme Sponsor redirected toward research: **"So i think we need to so some research and see how other people have approached similar projects... this isnt to say we copy or use it this just to see if we're missing a particular solution that could work for us"** - this became WP1.

The session then proceeded through: **WP2** (Guardian Orb Canvas 2D rendering migration, following through on ADR-0021's decision from ESR-0028), **WP3/WP4/WP6/WP7** (GIA - Guardian Instrumentation Agent - Phase 1 observability, delivered in four small staged slices), and **WP5** (Sponsor Approval Service architecture decision, ADR-0022, prompted by a detailed proposal the Programme Sponsor pasted directly into conversation).

All seven Work Packages completed the full real Working Report Lifecycle via the bridge: draft, Codex review, Programme Sponsor approval, implementation, commit, a second Codex review of the committed diff, and further fix cycles wherever genuine post-commit findings occurred. WP2 required a genuine, disclosed performance-regression investigation (Canvas initially measured worse than the SVG baseline it was meant to improve on) before the Guardian Orb's rendering-engine migration could be considered complete. Session-wide WP8 Independent Repository Verification and WP9 Repository Baseline Acceptance closed the session, both conducted via the bridge and requiring two rounds of post-commit fixes at WP9 before Codex confirmed no remaining drift.

---

# 4. Engineering Authority

ESR-0029 opening was authorised by Programme Sponsor instruction on 19 July 2026, following repository synchronisation confirming [[ESR-0028_ENGINEERING_SESSION_REPORT|ESR-0028]] was closed and [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Seven Work Packages, arrived at through the Programme Sponsor's own research-first redirection at WP0B, plus decisions and extensions made mid-session:

- **WP1** - Cross-module resource-interaction research (EBG-0082), directly from the Programme Sponsor's redirection.
- **WP2** - Guardian Orb Canvas 2D rendering migration (ADR-0021 implementation).
- **WP3** - GIA Phase 1a: CPU/memory local resource observability.
- **WP4** - GIA Phase 1b: Storage state.
- **WP5** - Sponsor Approval Service architecture decision (ADR-0022), added at the Programme Sponsor's request after pasting a detailed technical proposal for review.
- **WP6** - GIA Phase 1c: Process health (self-observation only).
- **WP7** - GIA Phase 1d: Local engineering-environment state, closing EBG-0083 Phase 1 in full.

All seven were met by closure. GIA's four phases (WP3/WP4/WP6/WP7) were deliberately delivered as small, separately-approved slices rather than one large package, consistent with this project's established small/evidence-led/staged delivery discipline.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation, PBK-0001 review, session objective selection (research redirection) | Complete - Section 7 |
| WP1 | Cross-module resource-interaction research (EBG-0082) | Complete - Section 8 |
| WP2 | Guardian Orb Canvas 2D rendering migration (ADR-0021) per EIP-ESR0029-001 | Complete - Section 9 |
| WP3 | GIA Phase 1a: CPU/memory observability per EIP-ESR0029-002 | Complete - Section 10 |
| WP4 | GIA Phase 1b: Storage state per EIP-ESR0029-003 | Complete - Section 10 |
| WP5 | Sponsor Approval Service architecture decision (ADR-0022) | Complete - Section 11 |
| WP6 | GIA Phase 1c: Process health per EIP-ESR0029-004 | Complete - Section 10 |
| WP7 | GIA Phase 1d: Local engineering-environment state per EIP-ESR0029-005, closing EBG-0083 Phase 1 | Complete - Section 10 |
| Session-wide WP8/WP9 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, new baseline RBL-0017 - Section 12 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- Repository state verified directly: `main` at `1df2802`, confirmed matching `origin/main`.
- Confirmed [[ESR-0028_ENGINEERING_SESSION_REPORT|ESR-0028]] formally closed and [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] the accepted baseline.
- **Three sync-staleness gaps found and explicitly deferred by the Programme Sponsor**: README.md still showed ESR-0026 as the latest closed session / RBL-0015 as baseline; PBK-0001 carried stale RBL-0015 references; JRM-0001's Track A/B tables did not reflect ESR-0028's or ESR-0029's progress. Not resolved this session - flagged again in Section 13 and in RBL-0017's own Scope Boundaries, not silently dropped.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0029 (this report, authored at closure per established practice).
- Repository baseline reference at opening: [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] (superseded at this session's own WP9 by [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]]).
- Session objective selection presented via `AskUserQuestion`; the Programme Sponsor redirected away from the offered options toward research: whether other projects' approaches to cross-module resource interaction might reveal a gap in JARVIS's own architecture, explicitly not to copy but to check for a missing pattern. This became WP1.
- WP5 (Sponsor Approval Service decision) was not part of the original WP0B selection - added mid-session after the Programme Sponsor pasted a detailed technical proposal ("aiems_bridge.py — changes to call the Sponsor Approval Service") for review.

---

# 8. WP1 - Cross-Module Resource-Interaction Research (EBG-0082)

Real external research (VS Code Extension Host, Electron/Tauri process models, Home Assistant, Mycroft) mapped directly against JARVIS's own modular architecture, to check for a missing cross-module resource-governance pattern rather than to copy any specific implementation.

**Delivered**: EBG-0082 registered and closed Complete in EBR-0001. One Medium finding was caught and fixed during the review cycle - a stale claim that a cited GitHub issue was open/unresolved, corrected after direct re-verification via `WebFetch` confirmed it was actually closed as not planned.

- Commit SHA: `541e6c1`
- `python -m pytest`: 286 passed (unchanged, research-only). `python scripts/validate_repository.py`: 0 errors, 126 warnings.

---

# 9. WP2 - Guardian Orb Canvas 2D Rendering Migration (ADR-0021)

Implements the Canvas 2D migration ADR-0021 recommended (but deliberately deferred) at ESR-0028, per [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] - this session's largest single product-code change.

**Delivered**: `GuardianOrbGraph.jsx` fully rewritten to a single Canvas 2D surface - pre-baked glow sprites reused via `drawImage`, `Path2D` depth-banded edge stroking, manual hit-testing, `ResizeObserver`/DPR-aware sizing. A static glow/gradient visual refinement toward UAM-0001's reference mock-up (look and layout only, confirmed directly against `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` after an initial scope misunderstanding was corrected mid-discussion) was included.

**A genuine performance regression was found and fixed during the WP's own live verification**: the initial Canvas implementation measured worse than the SVG baseline it was meant to improve on (~27-29% of one core via Chrome DevTools Protocol `TaskDuration`, vs. SVG's ~9%) - the opposite of the migration's purpose. Root-caused via a CDP ablation study to circular `ctx.clip()` combined with per-edge `stroke()` calls specifically. Fixed by batching edges into depth-banded `Path2D` objects and proving edges are mathematically guaranteed within the circular boundary (a disk is convex), scoping the clip to only the node/glow-drawing pass. Final measured cost (plain Canvas ~4.46%, with glow ~6.26%) fell below the SVG baseline, independently confirmed by the Programme Sponsor's own Windows Task Manager check (Power Usage: Low, a categorical change from the SVG-era's sustained "Very high").

**Review cycle**: pre-implementation approved directly. **Post-commit review found one Medium finding** - `hitTestRef` was built from `baseNodes`' arbitrary iteration order rather than the actual depth-sorted paint order `handlePointerMove` assumed, so overlapping-node tooltips could report the wrong node - fixed, then confirmed resolved (v1.2).

- Commit SHA: `c5a8340`
- At this commit: `python -m pytest`: 286 passed (unaffected, frontend-only; GIA's test additions came later at WP3-WP7). `python scripts/validate_repository.py`: 0 errors, 128 warnings. `npm run build`: clean throughout. (295 tests / 129 warnings is the session's final closure-commit state, not WP2's own.)

---

# 10. WP3/WP4/WP6/WP7 - GIA (Guardian Instrumentation Agent) Phase 1

Delivers EBG-0083 in four small, separately-approved slices, extending the same `GiaSnapshot`/`ResourceReader`/`PsutilResourceReader`/`LocalResourceObserver` architecture and the new `gia.status` JSON-RPC method throughout - per [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]], [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]], [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]], [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]].

**WP3 (Phase 1a - CPU/memory)**: first real GIA observability capability. `psutil` added as the project's first-ever declared runtime dependency. Two genuine findings addressed: a design-stage overstatement that `gia.status` was independent of `GuardianRuntime` as a present resilience guarantee (narrowed to method-level decoupling only, since `run()`'s startup sequence still gates all RPC methods behind `GuardianRuntime` constructing successfully); and an implementation-stage gap where the first RPC tests called the real psutil-backed observer instead of a deterministic fake snapshot, leaving serialization unproven (fixed via an injectable `gia_observer` constructor parameter, carried forward without regression through every later phase).

**WP4 (Phase 1b - Storage)**: extended with real disk usage via `STORAGE_PATH = os.path.abspath(os.sep)` (cross-platform drive/filesystem root). One Codex finding: a WP3-era "scope of this item" sentence in EBR-0001 contradicted WP4's own delivery note in the same row - fixed with an explicit correction rather than silently editing the historical sentence.

**WP6 (Phase 1c - Process health)**: extended with the JARVIS backend's own process self-observation (status, uptime, CPU, memory via `psutil.Process(os.getpid())`). Clean review, no findings either round.

**WP7 (Phase 1d - Engineering-environment state)**: extended with presence-only detection for a small, fixed, disclosed list of named engineering tools (VS Code, Obsidian, GitHub Desktop, ChatGPT Desktop), closing EBG-0083 Phase 1 in full. Real process names verified directly against the Programme Sponsor's running machine (`tasklist`) rather than assumed - found ChatGPT Desktop's real process name (`ChatGPT Classic.exe`) differs from the obvious guess. Clean review, no findings either round.

- Commit SHAs: `ff4ea7a` (WP3), `bac6ba9` (WP4), `e0ae3e3` (WP6), `8530604` (WP7)
- `python -m pytest`: 9 net-new tests added across the four phases, reaching 295 total by WP7's close (was 286 at ESR-0028's closure). `python scripts/validate_repository.py`: 0 errors, 129 warnings throughout. No frontend, `jarvis/gia/bootstrap.py`, or `run()` startup changes at any phase.

---

# 11. WP5 - Sponsor Approval Service Architecture Decision (ADR-0022)

Added mid-session at the Programme Sponsor's request, following a detailed proposal pasted directly into conversation: replace the AIEMS Exchange Bridge's file-based `sponsor-decision` with a remote, agent-read/sponsor-write approval service behind Tailscale.

**Decision**: [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] records eight binding requirements - a two-route service contract (`GET /decisions/latest` agent-token-gated, `POST /decisions` sponsor-token-gated), fail-closed if unreachable, durable persistence, Tailscale deployment (free/personal tier, matching the project's no-discretionary-budget default). Design-only, decision-only - no implementation code. Scoped after the Engineering Implementer's own two clarifying answers: the service doesn't exist yet (WP5 builds the decision, not the code), and the package is design-first/decision-only.

**A genuine gap in the Engineering Implementer's own practice was found and disclosed during this WP's review**: `cmd_submit_response` already correctly implements the approval and drift checks the bridge is meant to enforce, but had never actually been used as the real commit gate at any point this session - every WP's commit went through reading the local transcript directly and running `git commit` via Bash. Recorded as a binding operational-practice requirement in the decision itself (not left as an implied consequence), requiring `submit-response`-or-equivalent to become the actual mandatory gate going forward.

**Review cycle**: approved directly, no findings.

- Commit SHA: `770d292`
- `python -m pytest`: 294 passed (unaffected, decision-only, no code touched). `python scripts/validate_repository.py`: 0 errors, 129 warnings.

---

# 12. Session-Wide WP8/WP9 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0029 WP8 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session diff (`1df2802`..`8530604`) across all seven Work Packages - 19 files changed, 1,883 insertions, 203 deletions.

**Session-wide WP8 (Independent Repository Verification)**: Codex independently confirmed repository state matched the handover's claims exactly - the full diff stat, the authorised working set, scope boundaries (no `sentinel/` code touched, `jarvis/gia/bootstrap.py` and `run()` startup untouched, `src/` changes confined to the disclosed WP2 migration, WP5 confirmed decision-only). **Pass, no findings.** Codex's own independent baseline view converged with the Engineering Implementer's: cut a new baseline.

**Session-wide WP9 (Repository Baseline Acceptance): new baseline [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] established, superseding RBL-0016.** Both independent views converged - the Guardian Orb's rendering-engine replacement is comparable in kind to RBL-0016's own trigger, and GIA's Phase 1 delivery introduces a genuinely new backend capability (a new Python module, a new dependency, a new JSON-RPC method) RBL-0016 had no equivalent of. Programme Sponsor's own determination: **Accept - new baseline RBL-0017 established.**

**Two rounds of post-commit fixes followed the baseline-acceptance commit itself**, both on PST-0001's governance bookkeeping rather than the baseline decision or rationale: the first Codex return found the Current Mode/Phase rows still described ESR-0028 as the latest closed session with none open, directly contradicting the adjacent Current Repository Baseline row already updated to RBL-0017 - fixed, but a follow-up return found two more adjacent rows (Current Workflow, Current Engineering Objective) with the same staleness, requiring a second fix. Both rounds also caught the WP8 handover's own version bookkeeping falling one step behind the actual committed PST-0001 version after each fix. Codex's final return: **Pass, no findings** - both the repeated internal-consistency issue and the version-bookkeeping drift confirmed resolved.

- Commit SHAs: `d142ec4` (WP8 handover Pass recorded + WP9 baseline RBL-0017 established), `7a4953c` (WP9 post-commit fix round 1), `2080f66` (WP9 post-commit fix round 2, final Pass)
- `python -m pytest`: 295 passed throughout. `python scripts/validate_repository.py`: 0 errors, 129 warnings throughout.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0082 Complete (WP1); EBG-0083 Complete in full (WP3/4/6/7); EBG-0084 decision half Complete (WP5), implementation half remains future work. |
| [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] | Approved-implemented package for WP2, v1.2. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | Approved-implemented package for WP3, v1.1. |
| [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]] | Approved-implemented package for WP4, v1.1. |
| [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]] | Approved-implemented package for WP6, v1.0. |
| [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]] | Approved-implemented package for WP7, v1.0, closing EBG-0083 Phase 1. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved-implemented decision, implemented by WP2, v1.4. |
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | Approved decision for WP5, v1.1 - decision only. |
| [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0029 WP8 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.3, Section 12. |
| [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | New repository baseline established at Section 12. |
| [[ESR-0028_ENGINEERING_SESSION_REPORT|ESR-0028]] | Prior closed session this one continues from. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Knowledge tiering this session's WP0A followed. |

**Deferred, not resolved this session** (disclosed rather than silently dropped): README.md, PBK-0001, and JRM-0001 all still carry stale ESR-0028/RBL-0016-era (or earlier) references, explicitly deferred by the Programme Sponsor at WP0A - flagged here and in RBL-0017's own Scope Boundaries for a future session.

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Fixed two Codex post-commit findings: Section 9 (WP2) had misattributed the session's final closure-commit validation figures (295 tests/129 warnings) to WP2's own commit `c5a8340`, which actually validated at 286 tests/128 warnings - corrected to report the contemporaneous figures and explicitly note the final figures belong to session closure, not WP2; and corrected a mockup filename reference (`UAM-0001_GUARDIAN_ORB_MOCK.jpg` to the actual `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`). |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0-WP7 (research redirection at WP0B, Guardian Orb Canvas 2D migration with a genuine live-verified performance-regression fix, GIA Phase 1's four-slice staged delivery, and the Sponsor Approval Service decision), and the session-wide WP8 Independent Repository Verification (Pass, no findings) and WP9 Repository Baseline Acceptance (new baseline RBL-0017 established, superseding RBL-0016, after two rounds of post-commit PST-0001 fixes). Fourth session run entirely through the AIEMS Exchange Bridge with no manual relay. Status Open to Closed. |
