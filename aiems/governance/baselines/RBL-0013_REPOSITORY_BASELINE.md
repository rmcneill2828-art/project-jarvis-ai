# RBL-0013 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0013 |
| Title | ESR-0017 Repository Baseline (Refresh - Post-WP9) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] |
| Previous Baseline | [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 10 July 2026 |
| HEAD at baseline creation | `62c44b99dd408558e9ff1a583dc0fc49fbd1c6a5` |

---

# 2. Purpose

RBL-0013 records the refreshed repository baseline accepted by the Programme Sponsor at the close of ESR-0017, superseding [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]]. RBL-0012 explicitly stated it would not be revisited "unless WP8/WP9 themselves warrant a further baseline" - they did, and substantial further work landed after WP9 as well. This baseline captures that full state: WP8 (Feature-First Delivery Discipline), WP9 (the first live, interactive UXP), dev-environment setup automation, the Guardian Orb design-baseline recovery into UAM-0001, a WP4 roadmap revision, and a mock-up scale correction - then closes ESR-0017 itself.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - **stale, see Section 6** |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for ESR-0018 entry |

---

# 4. Baseline Recommendation Rationale

Recommended by Engineering Lead (Claude) at WP7 refresh handover, following ChatGPT Engineering Reviewer's WP6 Refresh Independent Repository Verification (Accepted, with one non-blocking discrepancy - see Section 9). Accepted by the Programme Sponsor on 10 July 2026.

RBL-0012 was accepted mid-session, before WP8/WP9, and named their completion as its own trigger for reconsideration. This baseline is judged materially heavier than RBL-0012: WP9 delivered the first genuinely interactive UXP in the project's history - not just an architecture decision (ADR-0019, RBL-0012) but the real, working, end-to-end path (React &rarr; Tauri &rarr; Python &rarr; Guardian &rarr; Sentinel &rarr; Provider), verified through an actual running windowed desktop application with a live conversation, not only through tests. This closes the exact gap RBL-0012 flagged as its own countervailing context: "A user opening the Tauri shell today still sees the same static mock-up as before ESR-0017" - that sentence is no longer true.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Feature-First Delivery Discipline added (v1.19): minimise controlled artefact creation, every session delivers product-moving work, every session makes demonstrable UXP progress. |
| `jarvis/interfaces/stdio_rpc.py` | JSON-RPC 2.0 stdio bridge - `StdioRpcServer`, `guardian.converse`/`platform.status` methods, `--ipc-stdio` entry point. Verified by real CLI execution and 14 tests. |
| `src-tauri/src/lib.rs` | Tauri sidecar process management - lazy spawn/reuse, no silent mock fallback on failure, state cleared on write/EOF/read/malformed-response failure. Verified by `cargo build` and a real windowed session. |
| `src/App.jsx`, `platformStatus.js`, `styles.css` | The UXP is no longer a static mock-up: chat input enabled, calls the real backend, renders real responses or explicit errors; capability/diagnostics panels derive from live `platform.status` data, corrected to no longer contradict each other. |
| `setup.bat`, `scripts/setup-dev-environment.ps1` | One-command dev-environment bootstrap (npm/cargo/Python venv/pre-commit hook/smoke test), verified idempotent. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | v1.5. Recovered a previously-approved-but-never-merged Guardian Orb knowledge-graph design direction (ESR-0010/FCH-0010) into Sections 8.1-8.3; incorporated the real reference mock-up image (Section 7.1); corrected its scale claims against the real repository (~135 artefacts, not the mock-up's illustrated thousands). |
| `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` | The actual design reference image, now a real repository asset. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | v1.23. EBG-0050 corrected from stale Candidate Backlog to Completed (Foundation Scope); EBG-0054 (setup automation expansion) and EBG-0055 (Knowledge Graph Phase 1) added. |
| `ESR-0017_WP4_ENGINEERING_REVIEW_PACKAGE.md` | Revised in place: EBG-0050's originally two-session plan marked complete early; EBG-0055 recommended into the freed ESR-0018/ESR-0019 capacity. |
| `scripts/bump_version.py` | Fixed a self-referential bug (bumping REG-0001 as its own tracked artefact silently discarded the requested version); 4 regression tests. |
| `scripts/validate_repository.py` | (Carried from RBL-0012) `latest_closed_numbered()` fix for open-session false positives. |
| Test suite | Grew from 166 (RBL-0012) to 184 passing tests, zero regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is **not updated by this baseline and is now materially stale**, flagged here rather than silently carried forward as "unchanged" the way RBL-0012 did:

- PCB-0001 Section 6 states "Guardian capability is not implemented" - false since WP2 (Guardian&harr;Sentinel connected) and more visibly since WP9 (Guardian is now conversationally reachable through the real UXP).
- PCB-0001 Section 4's "GUI" row describes only the Tkinter First Light interface - it does not reflect the Tauri UXP, which is now the live, interactive product surface.

Refreshing PCB-0001 accurately requires characterising the *entire* current product capability set, not a one-line patch, and is judged out of scope for this repository baseline refresh. Recorded as a new candidate backlog item ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056, added alongside this baseline) rather than left as a silent gap.

What actually changed operationally: Guardian&harr;Sentinel conversation capability is now reachable end-to-end through the real, approved UXP (not just through tests) - verified via a real running windowed Tauri session with a live round trip. `GeminiProvider` exists and is tested but remains unwired into any production route and unvalidated against the real Gemini API (EBG-0051's required live smoke test is still outstanding). Persistent memory, richer agent runtime, voice, vision, internet-backed assistance and automation remain outside any accepted operational baseline.

---

# 7. Architecture Outcomes

- First genuinely interactive UXP in the project's history - `CURRENT_ARCHITECTURE.md` roadmap item 7 ("Deliver Guardian's first interactive conversation") delivered through the real, approved desktop application, not a mock-up or a test harness.
- Guardian Orb design direction (knowledge-graph representation, cluster illumination, agent-traversal visualisation, Orb status semantics) formally recovered into [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] as the architecture-of-record, closing a gap where it had been approved in a prior session (ESR-0010) but never actually merged into the persistent artefact.
- EBG-0050 (UXP-Backend Bridge Implementation), originally roadmapped as a two-session effort (WP4), delivered in a single session - freeing real capacity for EBG-0055 (Knowledge Graph Phase 1) in the sessions immediately following.

---

# 8. Scope Boundaries

Scope boundaries for this baseline refresh:

- no ESR-0018 artefact is created by this baseline - it hands over to ESR-0018 (see Section 10), it does not open it;
- PCB-0001 (Product Capability Baseline) is not refreshed - flagged stale, tracked as EBG-0056, not actioned here (Section 6);
- `JARVIS_CAPABILITY_READINESS_MATRIX.md` remains stale (pre-dates WP2/WP9), noted at ESR-0017 Section 15.3, not actioned here;
- streaming JSON-RPC notifications, production sidecar packaging (`tauri-plugin-shell`), and full crash-restart policy remain deferred under EBG-0050's still-open remaining scope;
- Knowledge Graph Phases 2-4 (cluster colours beyond static styling, agent-traversal animation, Guardian reasoning connection) remain not started - only Phase 1 (EBG-0055) is recommended as a near-term next step;
- Gemini remains unvalidated against the real Gemini API (EBG-0051's live smoke test outstanding).

---

# 9. Verification

Repository validation performed during ESR-0017's WP6 refresh/WP7 refresh closure confirmed:

- Git working tree was clean at each commit; nine commits (`490997b` through `62c44b9`) pushed to `origin/main` since RBL-0012.
- Repository branch was `main`, synchronised with `origin/main` (`HEAD` confirmed at `62c44b9` by both the Engineering Lead and independently by the Engineering Reviewer via GitHub).
- 184/184 tests passing, zero regressions since RBL-0012's 166.
- `python scripts/validate_repository.py` passed with 0 errors (69 warnings, all pre-existing/documented adjacency-heuristic false positives - the same class accepted at RBL-0012 and earlier baselines).
- ChatGPT Engineering Reviewer performed WP6 Refresh Independent Repository Verification: **Accepted, with one non-blocking discrepancy** (the handover's stated expected `HEAD` was one commit stale - the handover-authoring commit itself, `62c44b9` - not product or uncontrolled scope; folded into this baseline rather than requiring a second refresh cycle). Content, scope and OSE compliance all Pass; UAM-0001's newly-recovered content independently spot-checked as faithful and non-speculative against its cited sources.
- The Programme Sponsor accepted this baseline on 10 July 2026, superseding [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] as the current repository baseline.

---

# 10. Handover

**This baseline hands over to ESR-0018.** Unlike RBL-0012, ESR-0017 formally closes immediately following this baseline's acceptance (see the session report's Document Control, updated in the same closure step).

Per [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]]'s frozen Lead/Reviewer rotation (Section 3.1), ESR-0018 is **ChatGPT-led, Claude-reviewed** - also the trial's decision-point session (adopt/reject/modify the Lead/Reviewer rotation, per EE-0001 Section 7).

ESR-0018 opening review should include:

1. This document, RBL-0013, and [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for ESR-0017 closure immediately following this acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] in full - nine Work Packages (WP0-WP9, no WP5), Sections 15.1-15.7 record substantial post-WP9 activity worth reading, not just the WP table.
5. [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9's ESR-0017 entry (scoped to WP1-WP4 by explicit Programme Sponsor decision at closure) and Section 7 (the decision-point mechanics ESR-0018 itself must resolve).
6. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], specifically EBG-0050 (now Completed - Foundation Scope, remaining hardening scope still open), EBG-0055 (Knowledge Graph Phase 1, recommended for ESR-0018 or ESR-0019), EBG-0051 (Gemini production readiness, still recommended for ESR-0018), and the new EBG-0056 (PCB-0001 refresh, not yet prioritised).
7. [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] - the Guardian Orb design direction any future UXP work should be checked against, per the gap this baseline's own predecessor left unclosed.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Engineering session this baseline is drawn from; closes immediately following this baseline's acceptance. |
| [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - flagged stale by this baseline (Section 6), not refreshed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for ESR-0017 closure immediately following this acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture; this baseline's design-recovery milestone. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial; ESR-0017 was its Cold Start Validation Session; ESR-0018 is its decision-point session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0055/EBG-0051 are the recommended next steps this baseline hands to ESR-0018. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 10 July 2026 | Claude Engineering Lead | Initial ESR-0017 refreshed repository baseline drafted and recommended, following ChatGPT Engineering Reviewer's WP6 Refresh (Accepted, one non-blocking discrepancy). Not yet accepted - Programme Sponsor acceptance decision pending per STD-0004. |
| 1.0 | 10 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0012. |
