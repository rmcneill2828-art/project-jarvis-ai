# RBL-0017 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0017 |
| Title | ESR-0029 Repository Baseline (Guardian Orb Canvas 2D Migration + GIA Phase 1) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0029 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 19 July 2026 |
| HEAD at baseline creation | `8530604` |

---

# 2. Purpose

RBL-0017 records the repository baseline accepted by the Programme Sponsor at ESR-0029 WP9, superseding [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]]. ESR-0029 materially changed the running product in two distinct ways: WP2 replaced the Guardian Orb's entire rendering engine (SVG DOM to Canvas 2D, per ADR-0021), live-verified via both Chrome DevTools Protocol measurement and the Programme Sponsor's own Windows Task Manager check; and WP3/WP4/WP6/WP7 delivered GIA's first real observability capability (a new Python module, dependency, JSON-RPC method, and live-verified host/resource/tool telemetry), closing EBG-0083 Phase 1 in full. Both independent WP8 views (Engineering Implementer and Engineering Reviewer) converged on this being at least comparable in substance to RBL-0016's own establishing delivery, not governance churn.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - stale, unchanged by this baseline, tracked as EBG-0056 |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0029 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP8 handover]] recorded two independently-reached views (Section 9), both recommending a new baseline rather than retaining RBL-0016.

**Engineering Implementer's view**: the Guardian Orb rendering-engine replacement is comparable in kind to RBL-0016's own rotation-work trigger, and GIA's Phase 1 delivery introduces a genuinely new backend capability RBL-0016 did not have any equivalent of - a new Python module, a new third-party dependency, and a new JSON-RPC method exposed to the running application, all live-verified against real host data.

**Engineering Reviewer's (Codex) independent view**: converged - "ESR-0029 materially changed the running product in two baseline-worthy ways: the Guardian Orb rendering engine moved from SVG DOM to Canvas 2D with live performance/hardware verification, and GIA introduced the first real backend observability capability via a new psutil-backed Python module, dependency, JSON-RPC method, and live-verified host/resource/tool telemetry. This is more than governance churn and at least comparable in substance to the prior RBL-0016 trigger."

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `src/GuardianOrbGraph.jsx`, `src/styles.css` | Migrated from per-element SVG DOM rendering to a single Canvas 2D surface (ADR-0021). Pre-baked glow sprites reused via `drawImage`; `Path2D` depth-banded edge stroking; circular clip scoped only to the node/glow-drawing pass after proving edges are mathematically guaranteed within the boundary (convexity argument). A genuine performance regression (initial Canvas measured worse than the SVG baseline it was meant to improve on) was found via CDP ablation study, root-caused to circular clip combined with per-edge stroke calls, and fixed - final measured cost below the SVG baseline, confirmed independently by the Programme Sponsor's own Windows Task Manager check (Power Usage: Low, a categorical change from the SVG-era's sustained "Very high"). |
| `jarvis/gia/observability.py` (new), `jarvis/interfaces/stdio_rpc.py`, `jarvis/gia/__init__.py`, `jarvis/__init__.py` | GIA (Guardian Instrumentation Agent) Phase 1 delivered in four staged, separately-approved slices: CPU/memory (WP3), storage (WP4), process health/self-observation (WP6), local engineering-environment tool presence (WP7). `GiaSnapshot`/`ResourceReader`/`PsutilResourceReader`/`LocalResourceObserver` architecture; new `gia.status` JSON-RPC method, injectable and independently testable via a fake `ResourceReader`. `jarvis/gia/bootstrap.py` (the pre-existing, unrelated GIA-BOOT readiness gate) untouched throughout. |
| `pyproject.toml` | `psutil` added as the project's first-ever declared runtime dependency. |
| [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] | v1.2, Approved-implemented. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]], [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]], [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]], [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]] | v1.1/v1.1/v1.0/v1.0, all Approved-implemented. Close EBG-0083 Phase 1 in full; Phases 2-4 remain separate future work. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | v1.4, Approved-implemented - Canvas 2D migration implemented per this session's WP2. |
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | v1.1, Approved. Decision only (no implementation): replace the AIEMS Exchange Bridge's file-based `sponsor-decision` with a remote agent-read/sponsor-write approval service; also records a binding operational-practice requirement that `submit-response` become the actual mandatory commit gate, following a self-found gap that it had never once been used as such this session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0082 (cross-module resource-interaction research) registered and Complete; EBG-0083 (GIA Phase 1) Complete in full; EBG-0084 (Sponsor Approval Service) decision half Complete via ADR-0022, implementation half not authorised. |
| Test suite | 295 tests, up from RBL-0016's 286 - all net-new tests from GIA's observability module and `gia.status` RPC coverage; no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is unchanged by this baseline. Tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056 (not actioned this session).

---

# 7. Architecture Outcomes

- First session where the Guardian Orb's rendering engine itself is replaced (SVG DOM to Canvas 2D), following through on ADR-0021's decision recorded (but deliberately not implemented) at RBL-0016.
- First real GIA (Guardian Instrumentation Agent) capability delivered - previously GIA existed only as a design concept (ESR-0011 Section 10) and an unrelated readiness-gating bootstrap (`jarvis/gia/bootstrap.py`, GIA-BOOT). This session delivered genuine host/process/tool observability, exposed via a new JSON-RPC method, live-verified against real machine data throughout.
- First project dependency ever declared in `pyproject.toml` (`psutil`).
- A genuine, disclosed performance regression was found and fixed mid-session (WP2's Canvas implementation initially measured worse than the SVG baseline it replaced) - direct continuation of this project's live-verification-over-automated-tests-alone discipline established at RBL-0016.
- First architecture decision (ADR-0022) addressing the AIEMS Exchange Bridge's own governance tooling rather than the product itself - decision-only, surfacing a genuine gap in the Engineering Implementer's own practiced use of `submit-response` as the real commit gate.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0030 artefact is created by this baseline - ESR-0029 closes with this baseline's acceptance, per the Programme Sponsor's "Close the session" instruction;
- PCB-0001 is not refreshed - tracked as EBG-0056, not actioned here;
- ADR-0022's Sponsor Approval Service is not implemented by this baseline - decision only; `sponsor_client.py` and the `aiems_bridge.py` diff remain future-scoped, tracked as EBG-0084's remaining half;
- GIA Phases 2-4 (platform service instrumentation, engineering instrumentation, external/provider telemetry) remain not started, tracked as EBG-0083's remaining scope;
- three sync-staleness gaps found at WP0A (README.md, PBK-0001, and JRM-0001 all still carrying stale ESR-0028/RBL-0015-era references) were explicitly deferred by the Programme Sponsor earlier in the session and remain unresolved at this baseline - flagged here rather than silently dropped, for correction in a future session.

---

# 9. Verification

Repository validation performed during ESR-0029 WP8/WP9:

- Git working tree was clean; the full session range (`1df2802`..`8530604`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main`.
- 295/295 tests passing, up from RBL-0016's 286 (9 net-new tests, all GIA-related; no regressions).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 129 warnings (126 pre-existing plus 3 new, disclosed, accepted cross-document false positives).
- `npm run build` clean after every WP2 code change.
- `git diff --check 1df2802..8530604` clean, independently re-run by the Engineering Reviewer.
- Live verification throughout: CDP `TaskDuration` ablation study isolating WP2's clip/stroke performance regression; the Programme Sponsor's own Windows Task Manager confirmation (Power Usage: Low); in-memory-stream `gia.status` calls at WP3/WP4/WP6/WP7 returning genuine host data, cross-checked against independent `tasklist` evidence at WP7.
- The Engineering Reviewer performed WP8 Independent Repository Verification: **Pass, no findings** - repository state confirmed to match the handover's claims exactly (file list, diff stat, scope, disclosed observations), no drift found.
- The Programme Sponsor's own WP9 determination: establish a new baseline rather than retain RBL-0016 (Section 4).

---

# 10. Handover

**This baseline closes ESR-0029**, per the Programme Sponsor's explicit "Close the session" instruction. The ESR-0029 Engineering Session Report is authored separately, following this baseline's acceptance.

Future work against this baseline should include:

1. This document and [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - specifically EBG-0083's remaining Phases 2-4, and EBG-0084's remaining implementation half (ADR-0022's Sponsor Approval Service).
5. The three deferred sync-staleness gaps (README.md, PBK-0001, JRM-0001) noted in Section 8 - not resolved by this baseline, worth prioritising early in a future session.
6. [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] through [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]], [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]], [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]], and the [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP8 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0029 WP8 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] | Approved-implemented package this baseline's Canvas migration deliverable was implemented against. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | Approved-implemented package for GIA Phase 1a. |
| [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]] | Approved-implemented package for GIA Phase 1b. |
| [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]] | Approved-implemented package for GIA Phase 1c. |
| [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]] | Approved-implemented package for GIA Phase 1d, closing EBG-0083 Phase 1. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved-implemented rendering-engine decision, implemented by this baseline's WP2. |
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | Approved decision recorded this session, not implemented by this baseline. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - remains stale on this point, tracked as EBG-0056, not refreshed by this baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0082 Complete, EBG-0083 Complete (Phase 1), EBG-0084 decision half Complete. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Roadmap that sequenced this session's WP selection; stale, flagged as a deferred gap in Section 8. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 19 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0016, following the Engineering Reviewer's WP8 Pass and the Programme Sponsor's explicit WP9 decision to cut a new baseline rather than retain RBL-0016: the Guardian Orb's rendering-engine migration and GIA's first real observability capability materially change the running product, agreeing with both independent WP8 baseline views. |
