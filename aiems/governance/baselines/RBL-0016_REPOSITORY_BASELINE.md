# RBL-0016 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0016 |
| Title | ESR-0028 Repository Baseline (Guardian Orb 3D Rotation) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0028 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 18 July 2026 |
| HEAD at baseline creation | `6752312` |

---

# 2. Purpose

RBL-0016 records the repository baseline accepted by the Programme Sponsor at ESR-0028 WP7, superseding [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]]. Unlike ESR-0026/ESR-0027's retained-baseline sessions (backend-only capability delivery not yet reachable through the live UXP, and a trivial three-line UXP subtraction respectively), ESR-0028 WP4 materially changes the running UXP's flagship Guardian Orb - both its appearance (decorative rings, border, glow and greeting text all removed, per direct Programme Sponsor instruction) and its behaviour (the Orb now genuinely rotates, driven by real graph data, where it was previously a static rendering). Both independent WP6 views (Engineering Implementer and Engineering Reviewer) converged on this being a user-visible product capability/experience change comparable in substance to RBL-0015's own establishing delivery (production provider wiring), not governance churn or a cosmetic tidy-up.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - stale, unchanged by this baseline, tracked as EBG-0056 |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0028 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP6 handover]] recorded two independently-reached views (Section 9), both recommending a new baseline rather than retaining RBL-0015.

**Engineering Implementer's view**: `GuardianOrbGraph.jsx` alone changed by 362 net lines across eight commits (the initial delivery plus seven live-verified fix rounds); the Guardian Orb is the first thing any user sees on opening the app, and both its appearance and behaviour changed. The Programme Sponsor personally live-verified the result multiple times across the session - screenshots, Windows Task Manager power-usage comparisons, and direct feedback that shaped each of the seven fix rounds.

**Engineering Reviewer's (Codex) independent view**: converged - "ESR-0028 materially changed the running UXP's flagship Guardian Orb appearance and behaviour... a user-visible product capability/experience change comparable in substance to the prior baseline-triggering UXP/provider milestones, not merely governance churn or a small static-row subtraction."

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `src/GuardianOrbGraph.jsx` | Full-sphere sphere-surface coordinates via a deterministic (id-hash, not random) front/back hemisphere sign per node; real Y-axis rotation with depth-based re-sorting; `prefers-reduced-motion` support; retuned `d3-force` parameters (charge, link strength, centering) informed by the Programme Sponsor's own Obsidian graph-view measurements, re-verified against the real graph (centroid, overlap count). Following a real Programme Sponsor-observed power-usage regression, rewritten to a ref-based `requestAnimationFrame` architecture (bypassing React's render cycle), with capped and decoupled node/edge update rates, an idle-timeout pause, and a `visibilitychange`-based fix for a hidden-window resume race. |
| `src/App.jsx`, `src/platformStatus.js`, `src/styles.css` | Decorative orbital-field rings, border, glow and greeting/status text removed around the Orb, per direct Programme Sponsor instruction; now-dead `deriveGuardianStatus()` and the orphaned `guardianStatus` export removed; a pre-existing, unrelated infinite box-shadow animation (`guardian-breathe`) found and removed during the power-usage investigation. |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | v1.0, Approved-implemented. Closes EBG-0055 Phase 1.5. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | v1.3, Approved. Decision only (no implementation): migrate `GuardianOrbGraph.jsx` to Canvas 2D when scoped, grounded directly in WP4's seven-round evidence; WebGL/Three.js rejected as disproportionate to current/anticipated scale. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0055 Phase 1.5 marked Complete; EBG-0081 registered mid-session and given a split disposition (rendering-engine half Complete via ADR-0021, shared-animation-scheduler half remains Candidate Backlog). Also this session: EBG-0058/0005/0068/0071 (WP1), EBG-0017 (WP2), EBG-0045/0049/0024 (WP3) all Complete. |
| Test suite | 286 tests, unchanged from RBL-0015 - WP1/2/3/5 were governance-only; WP4 has no committed frontend test infrastructure (an existing, separately-tracked gap), verified instead via live Playwright checks against the real backend graph data throughout. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is unchanged by this baseline. Tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056 (not actioned this session).

---

# 7. Architecture Outcomes

- First session where the Guardian Orb - the flagship visual presence of the running UXP - genuinely animates, driven by real graph data rather than a static hemisphere projection.
- First session where a real-hardware power-usage regression, found only through live Programme Sponsor use (not any automated check), drove seven consecutive rounds of live-verified fixes - direct evidence that live verification against real hardware, not just automated tests or a single Playwright pass, remains part of this project's acceptance process.
- First formal rendering-engine architecture decision for the knowledge-graph component (ADR-0021) - Canvas 2D selected over continued SVG or WebGL, decision-only, implementation intentionally deferred.
- Two genuine operational process incidents were found and disclosed during this session, unrelated to the code itself: a leaked `find.exe` process confounding several Task Manager comparisons, and three confirmed instances of the harness's `TaskStop` reporting success without actually terminating a background dev-server process - both now reflected in the Engineering Implementer's own standing operational practice (verify via `netstat`/`tasklist`, never trust `TaskStop`'s success message alone).

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0029 artefact is created by this baseline - ESR-0028 may continue with further Work Packages, or a future session may open separately; both are Programme Sponsor decisions not made by this baseline;
- PCB-0001 is not refreshed - tracked as EBG-0056, not actioned here;
- ADR-0021's Canvas 2D migration is not implemented by this baseline - decision only, per the Programme Sponsor's explicit "review, not implement" instruction; a future EIP must separately scope it;
- EBG-0081's shared-animation-scheduler half remains open Candidate Backlog, not resolved by this baseline;
- Phase 3 (agent-traversal animation, blocked on GIA telemetry) and Phase 4 (Guardian reasoning connection) of the Guardian Orb roadmap remain not started.

---

# 9. Verification

Repository validation performed during ESR-0028 WP6/WP7:

- Git working tree was clean; the full session range (`dfa13b4`..`6752312`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main`.
- 286/286 tests passing, zero regressions since RBL-0015's 286 (WP1/2/3/5 governance-only; WP4 touched only `src/`, which has no committed test suite).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 126 warnings - the same pre-existing baseline warning count throughout the session.
- `npm run build` clean after every WP4 code change.
- Live verification against real hardware and real backend data throughout WP4: Playwright checks against the real 195-node/1,687-edge knowledge graph for rotation smoothness, reduced-motion behaviour, idle-timeout pause/resume and hidden-window resume; direct Windows Task Manager comparisons (with and without rotation, with and without the leaked `find.exe` process) to isolate the true cost of each fix.
- The Engineering Reviewer performed WP6 Independent Repository Verification: **Pass, no findings** - repository state confirmed to match the handover's claims exactly (file list, diff stat, scope, disclosed observations).
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0015 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0028 or open a new session** - whether ESR-0028 continues with further Work Packages or closes here is a separate Programme Sponsor decision, not made by this baseline.

Future work against this baseline should include:

1. This document and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - specifically EBG-0081's remaining shared-animation-scheduler half, and any future EIP to implement ADR-0021's Canvas 2D migration.
5. [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]], [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] and the [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP6 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0028 WP6 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | Approved implementation package this baseline's Guardian Orb deliverables were implemented against. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved rendering-engine decision recorded this session, not implemented by this baseline. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - remains stale on this point, tracked as EBG-0056, not refreshed by this baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0055 Phase 1.5 completed, EBG-0081 split-dispositioned. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Roadmap that sequenced this session's WP selection. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0015, following the Engineering Reviewer's WP6 Pass and the Programme Sponsor's explicit WP7 decision to cut a new baseline rather than retain RBL-0015: the Guardian Orb's rotation and visual cleanup materially changes the running UXP's flagship product surface, a user-visible product capability/experience change, agreeing with both independent WP6 baseline views. |
