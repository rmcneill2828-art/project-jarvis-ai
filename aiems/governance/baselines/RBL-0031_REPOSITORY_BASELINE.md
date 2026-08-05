# RBL-0031 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0031 |
| Title | ESR-0050 Repository Baseline (Agent Framework UXP Wiring; Sentinel Gate of Durin Architecture Specification) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0050_ENGINEERING_SESSION_REPORT|ESR-0050]] |
| Previous Baseline | [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 5 August 2026 |
| HEAD at baseline creation | `a7eabb0` |

---

# 2. Purpose

RBL-0031 records the repository baseline accepted by the Programme Sponsor at ESR-0050 WP7, superseding [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]]. ESR-0050 ran three Work Packages: WP1 (content-refreshed PCB-0001 and the JARVIS Capability Readiness Matrix for the Agent Framework Phase 3 capability delivered at ESR-0049, plus a Whole-Document Staleness Sweep fix to PST-0001's Repository Health block); WP2 (resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0120, Agent Framework UXP Wiring - a genuine, live product-capability change); and WP3 (resolving EBG-0047, Sentinel Gate of Durin Architecture Specification, via a broad refresh of `CURRENT_ARCHITECTURE.md`, registered as a controlled artefact for the first time). Guardian's Agent Framework is now invokable live through the UXP - not just RPC/backend-reachable as it was at RBL-0030 - and Sentinel's real trust-gateway/platform-entry-validation pattern is now properly documented.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v2.6 - content-refreshed this session (WP1) for the Agent Framework Phase 3 capability; the Agent Framework UXP Wiring capability delivered at this session's own WP2 is not yet reflected there, flagged as a documentation-staleness item for a future session's Documentation Debt sync. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0050 remains open for further Work Packages at the Programme Sponsor's direction |

---

# 4. Baseline Recommendation Rationale

**WP2 design review (Codex, direct `codex exec -s read-only` invocation)**: [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]] v0.1 reviewed Pass with 3 non-blocking findings (Section 8's exclusion wording, `deriveCapabilityStatuses()`'s parameter-signature detail, panel placement) - all folded into v0.2 before implementation.

**WP3 design review**: [[EIP-ESR0050-002_CURRENT_ARCHITECTURE_REFRESH_AND_GATE_OF_DURIN_DETAIL|EIP-ESR0050-002]] v0.1 reviewed Pass with 1 non-blocking finding (an overstated cross-reference claim about GAM-0001) - folded into v0.2.

**Pre-implementation approval gates**: Programme Sponsor approval-to-implement obtained and verified via `submit-response` directly against the real Sponsor Approval Service for both WP2 and WP3, before any code or content was written.

**WP2 post-commit review**: first attempt returned a false Fail, traced to imprecise wording in the review prompt itself (governance prose legitimately naming `GAM-0001`/`sentinel/policy.py` to disclose non-modification, misread by an over-literal claim) - not a defect in the committed code. Corrected and re-run: genuine independent Codex review of the real committed diff (`497a2e7..6e549cb`) - **Pass, no findings**.

**WP3 post-commit review**: genuine independent Codex review of the real committed diff (`6e549cb..a7eabb0`) - Pass with 1 non-blocking finding (a stale docstring in `sentinel/policy.py`, existing source code outside this documentation-only package's scope, not actioned).

**Session-wide WP6 Independent Repository Verification**: covering the full session range `0d614e0..a7eabb0` (WP1, WP2 and WP3 combined). **Pass, no findings** - confirmed exactly the expected 14 files changed, `GAM-0001` and `sentinel/policy.py` byte-identical/untouched, no backend Agent Framework code touched, every "Completed" governance claim backed by real evidence, and every REG-0001 version row matching. Codex's own advisory assessment: a genuine live product-capability change, recommending Establish.

**Push approval**: Programme Sponsor approval-to-push likewise obtained and verified via `submit-response` against the real Sponsor Approval Service before each `git push` (WP1, WP2, WP3).

**The Programme Sponsor's determination**: **establish a new baseline**, since WP2 delivered a genuine, live product-capability change - the Agent Framework moved from RPC/backend-reachable only (RBL-0030) to genuinely invokable through the live UXP - matching the same threshold applied at RBL-0025/RBL-0027/RBL-0028/RBL-0029/RBL-0030 rather than the Retain threshold applied at architecture/documentation-only sessions such as ESR-0048.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `src-tauri/src/lib.rs` | Two new Tauri commands, `list_agents`/`invoke_agent`, thin `call_backend()` wrappers matching every existing command's pattern. |
| `src/App.jsx` | `deriveCapabilityStatuses()` gains `agents`/`agentsError` parameters and a live `agent-framework` branch - first live use of `STATUS.AVAILABLE`. New `App()` state, mount-effect `list_agents` call, `handleInvokeAgent` handler mirroring `handleSpeak`'s outcome-status pattern. |
| `src/AgentFrameworkPanel.jsx` (new) | Lists registered agents, a Run button per agent, real returned payload rendered via the existing `.metrics-list`/`.metric-row` classes, denied/error outcomes shown inline - never a fabricated result. |
| `src/styles.css` | New panel classes, reusing existing shared panel/metric-row base styles. |
| `tests/e2e/app.spec.js` | 4 new Playwright tests (empty state, live registered agent, successful run, denied outcome) - 13/13 passing, 9 existing unchanged. |
| `aiems/architecture/CURRENT_ARCHITECTURE.md` | Registered as a controlled artefact for the first time (Version 1.0). Corrected a factual error (wrong production trust-policy-engine default). New Sentinel Gate of Durin subsection resolving EBG-0047. Obsolete "ESR-0015 Starting Architecture" section replaced with a historical note. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | New Agent Framework row (v2.5 to v2.6), content-refreshed for the Agent Framework Phase 3 capability delivered at ESR-0049. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | "Engineering Agent" row renamed and updated to Implemented (Foundation) (v2.4 to v2.5). |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Whole-Document Staleness Sweep fix: Repository Health block corrected (was citing RBL-0023, seven baselines stale, and outdated test/validation figures). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0120 and EBG-0047 both marked Completed. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was content-refreshed this session (WP1) for the Agent Framework Phase 3 capability, but not re-refreshed for this same session's own WP2 delivery (Agent Framework UXP Wiring) - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync.

---

# 7. Architecture Outcomes

- The Agent Framework moves from RPC/backend-reachable only (RBL-0030) to genuinely invokable through the live UXP - a household member can now see and run `gia-observability` from the Guardian desktop shell itself.
- Sentinel's trust-gateway/platform-entry-validation pattern - already real, already implemented since ESR-0016/ESR-0024 - is now properly documented for the first time in `CURRENT_ARCHITECTURE.md`'s new Sentinel Gate of Durin subsection, closing a governance gap that had persisted for 34 sessions.
- `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remains completely untouched throughout - the UXP wiring surfaces only the existing read-only `ROUTINE_INTERACTION` agent; `sentinel/policy.py` was not modified at any point this session.
- `CURRENT_ARCHITECTURE.md` is now a registered controlled artefact (Version 1.0) for the first time, closing a load-bearing-but-ungoverned gap disclosed by five other controlled artefacts that already treated it as authoritative.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- exactly one specialist agent (`gia-observability`), read-only, classified `ROUTINE_INTERACTION` - no other agent capability exists;
- no arbitrary task/parameter UI input for agent invocation - the UXP always sends a fixed task string and empty parameters;
- no `LOCAL_AGENT_ACTION`-classified capability of any kind - `sentinel/policy.py` untouched throughout the session;
- no change to backend Agent Framework code (`jarvis/agents/`, `sentinel_agent.py`, `runtime.py`, `stdio_rpc.py`) - WP2 is UXP/Tauri-side wiring only, against the existing contract;
- WP3 is documentation only - no code touched.

---

# 9. Verification

Repository validation performed across ESR-0050's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`0d614e0..a7eabb0`, 3 commits) pushed to `origin/main`.
- 512 Python tests passing plus 1 correctly-skipped test - unchanged from RBL-0030, since no backend file was touched this session.
- 13 Playwright tests passing (9 existing unchanged, 4 new) - up from 9 at RBL-0030.
- `cargo check` (`src-tauri/`) clean; `npm run build` clean.
- `python scripts/validate_repository.py` (full mode): 0 errors throughout (285 to 289 warnings, all pre-existing-pattern stray cross-references, non-blocking).
- WP2 design review (Codex): v0.1 Pass with 3 non-blocking findings, folded into v0.2.
- WP3 design review (Codex): v0.1 Pass with 1 non-blocking finding, folded into v0.2.
- WP2 post-commit review (Codex): first attempt false Fail (review-prompt wording flaw, disclosed and corrected), second attempt Pass, no findings.
- WP3 post-commit review (Codex): Pass with 1 non-blocking finding (pre-existing `sentinel/policy.py` docstring, out of scope, not actioned).
- Session-wide WP6 (Codex): Pass, no findings, covering the full session diff against RBL-0030.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`) - every push approval verified for real before `git push`, none skipped.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0030 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0050** - the Programme Sponsor may add further Work Packages before the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh for this session's own WP2 delivery (Agent Framework UXP Wiring) - not yet reflected there.
5. A second, real (non-illustrative) specialist agent, or a parameterised task/input UI for the existing agent, remain natural next extensions of the Agent Framework.
6. README.md's full "current session"/Capability Roadmap narrative sync is deferred to ESR-0050's eventual formal closure, matching established practice - this baseline's own reference-pointer propagation covers only the direct "current accepted repository baseline" citations, disclosed here rather than silently left inconsistent.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0050_ENGINEERING_SESSION_REPORT|ESR-0050]] | Session this baseline is drawn from. |
| [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[EIP-ESR0050-002_CURRENT_ARCHITECTURE_REFRESH_AND_GATE_OF_DURIN_DETAIL|EIP-ESR0050-002]] | Approved Engineering Implementation Package WP3's deliverables were built against. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A - the boundary this baseline's UXP wiring stays inside, untouched. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0120 and EBG-0047 (both closed this session). |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - content-refreshed this session (WP1), not re-refreshed for WP2's own delivery, flagged for future sync. |
| [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] | Registered as a controlled artefact for the first time this session, refreshed broadly. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0030, following Codex design reviews (WP2 v0.1 Pass with 3 non-blocking findings; WP3 v0.1 Pass with 1 non-blocking finding, both folded in before implementation), verified pre-implementation approval gates, post-commit Codex reviews (WP2's first attempt a false Fail traced to a review-prompt wording flaw, corrected and re-verified Pass; WP3 Pass with 1 non-blocking finding), session-wide WP6 Independent Repository Verification (Pass, no findings), verified push-approval gates for every commit, and the Programme Sponsor's explicit WP7 decision to cut a new baseline: WP2's real, live-verified Agent Framework UXP Wiring delivery warrants a new baseline. |
