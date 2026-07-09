# RBL-0012 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0012 |
| Title | ESR-0017 Repository Baseline |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] |
| Previous Baseline | [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 9 July 2026 |
| HEAD at baseline creation | `3fabbca8fe974f3418948bda096e2158d0ff5aad` |

---

# 2. Purpose

RBL-0012 records the repository baseline accepted by the Programme Sponsor at the conclusion of ESR-0017. Per [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]], acceptance of a Repository Baseline is reserved to the Programme Sponsor; that acceptance was given on 9 July 2026.

It captures the accepted repository state after ESR-0017's delivery: the first architecture decision governing UXP-to-backend integration (ADR-0019), the first working connection between Guardian Runtime and Sentinel, a second external provider adapter (Gemini), a five-session backlog progression roadmap, and closure of the EE-0001 trial's designated Cold Start Validation Session with a reconciled Lead/Reviewer scorecard.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for ESR-0018 entry |

---

# 4. Baseline Recommendation Rationale

Recommended by Engineering Lead (Claude) at WP7 handover, following ChatGPT Engineering Reviewer's WP6 Independent Repository Verification (Pass - repository state, content, OSE and scope compliance all confirmed, one disclosed non-blocking commit-message deviation). Accepted by the Programme Sponsor on 9 July 2026.

[[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] (ESR-0015) was retained through ESR-0016, whose trust-tier policy delivery was judged incremental against ESR-0015's milestone. ESR-0017 is judged comparable in weight to ESR-0015 itself: it is the first session to decide how the approved UXP reaches the backend at all (ADR-0019), the first to connect Guardian to Sentinel (proven against real `SentinelTrustGateway`/`ProviderOrchestrator` components, not a stub), and the session that closed out the EE-0001 trial's Cold Start Validation Session - the first empirical proof that a fresh AI Lead can onboard from repository documentation alone.

Countervailing context recorded for completeness: the UXP itself remains disconnected in the running application - ADR-0019 decides the integration pattern, it does not implement it (EBG-0050 is that future work). A user opening the Tauri shell today still sees the same static mock-up as before ESR-0017. This did not change the recommendation - the architecture decision and the Guardian&harr;Sentinel wiring are real, durable milestones independent of when the UXP bridge itself lands - but is offered so the Programme Sponsor's acceptance decision was made with the full picture.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | UXP-Backend Integration Architecture: Tauri sidecar-managed Python process, duplex stdio JSON-RPC, v1.1 after Reviewer-driven wording revision. |
| `jarvis/guardian/runtime.py` | `GuardianRuntime` gained an optional `conversation_provider` parameter and a `converse()` method; zero regressions to existing behaviour. |
| `sentinel/gemini_provider.py` | Second external Sentinel provider adapter (`GeminiProvider`), mirroring `OpenAIProvider`'s conventions, exported but unwired by default. |
| `scripts/validate_repository.py` | Fixed `check_stale_status_references` incorrectly flagging Open (not yet Closed) sessions as stale. |
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Session report with consolidated Engineering Completion Report, WP1-WP4 all reviewed and closed, WP6 Pass recorded. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | ESR-0017 trial scorecard reconciled (Lead draft + Reviewer refinement); Documentation-only handoff verified **&check;** for the first time in the trial. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0050 through EBG-0053 added (UXP-backend bridge implementation, Gemini production readiness, and two candidate EE-0001/PBK-0001 governance refinements). |
| Test suite | Grew from 144 to 166 passing tests, zero regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] remains the accepted operational product capability baseline, unchanged by this baseline. First Light's Tkinter interface and the Tauri UXP's static shell are both unchanged in running behaviour - ESR-0017 built the architecture decision and backend wiring that a future bridge (EBG-0050) will connect to the UXP, but did not itself change what an end user sees or can do.

Guardian&harr;Sentinel conversation capability exists and is tested (`GuardianRuntime.converse()`), but is not reachable through any running application surface. Gemini as a provider exists and is tested, but is not wired into any production `ProviderOrchestrator` route and has not been proven against the real Gemini API (EBG-0051's required live smoke test is outstanding). Persistent memory, richer agent runtime, voice, vision, internet-backed assistance and automation remain outside the accepted operational product baseline.

---

# 7. Architecture Outcomes

ESR-0017 both decided new architecture and proved existing architecture operationally:

- UXP-to-backend integration pattern **decided** (not yet implemented) via [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] - the first architectural answer to a gap that existed since the UXP's original selection (ADR-0007).
- "Guardian expresses intent; Sentinel governs execution" - `CURRENT_ARCHITECTURE.md` roadmap item 6 ("Connect Guardian through Sentinel") **proven operationally** for the first time via `GuardianRuntime.converse()`, tested against real `SentinelTrustGateway`/`ProviderOrchestrator` components.
- Provider independence - **extended** from one proven provider (OpenAI, ESR-0015) to two implemented adapters (OpenAI, Gemini), the first real test of Sentinel's provider-independence claim with more than one concrete adapter to be independent *between*.

---

# 8. Scope Boundaries

Scope boundaries for this baseline acceptance:

- no ESR-0018 artefact is created;
- no new product capability baseline is created;
- the UXP-backend bridge itself is not implemented - ADR-0019 is a decision, not code (deferred to EBG-0050);
- `src/platformStatus.js`'s hardcoded state and the disabled chat input are unchanged;
- Gemini is not proven against the real Gemini API and is not wired into any production route (deferred to EBG-0051);
- PST-0001 is updated separately, immediately following this baseline's acceptance, to reflect ESR-0017 closure.

---

# 9. Verification

Repository validation performed during ESR-0017 WP6/WP7 closure confirmed:

- Git working tree was clean at each commit; four commits (`be873d1`, `6d6344a`, `e58deaf`, `3fabbca`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main`.
- 166/166 tests passing, zero regressions across the session.
- `python scripts/validate_repository.py` passed with 0 errors (31 warnings, all pre-existing/documented adjacency-heuristic false positives).
- ChatGPT Engineering Reviewer performed WP6 Independent Repository Verification: repository state, content, OSE compliance and scope compliance all Pass; one disclosed, non-blocking commit-message deviation.
- The Programme Sponsor accepted this baseline on 9 July 2026, superseding [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] as the current repository baseline.

---

# 10. Handover

**This baseline does not hand over to ESR-0018.** ESR-0017 remains **Open** at the time of this baseline's acceptance - the Programme Sponsor has indicated two further Work Packages (WP8, WP9) will follow within ESR-0017 before the session closes, scope not yet defined. This baseline acceptance (WP7) stands independently of WP8/WP9's outcome; it is not contingent on them and will not be revisited unless WP8/WP9 themselves warrant a further baseline.

ESR-0018 entry (per [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]]'s frozen Lead/Reviewer rotation, Section 3.1: **ChatGPT leads, Claude reviews**, also the trial's decision-point session per Section 7) remains a future recommendation only, to be actioned once ESR-0017 actually closes - not by this document.

Once ESR-0017 does close, opening review for ESR-0018 should include:

1. This document, RBL-0012, and [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]].
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] and all of its WP review packages, including WP8/WP9 once they exist.
5. [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9's ESR-0017 entry - includes two joint recommendations (EBG-0052, EBG-0053) not yet adopted.
6. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], specifically EBG-0050 (Phase 1 candidate per WP4's roadmap) and EBG-0051 - noting WP8/WP9 may have changed this picture.
7. [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] - the architecture EBG-0050 implementation would build against.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Engineering session this baseline is drawn from. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline, unchanged by this baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for ESR-0017 closure immediately following this acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | Architecture decision this baseline's UXP-integration milestone is drawn from. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial; ESR-0017 was its Cold Start Validation Session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0050 is the recommended next step this baseline hands to ESR-0018. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 9 July 2026 | Claude Engineering Lead | Initial ESR-0017 repository baseline drafted and recommended, following ChatGPT Engineering Reviewer's WP6 Pass. Not yet accepted - Programme Sponsor acceptance decision pending per STD-0004. |
| 1.0 | 9 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0011. |
