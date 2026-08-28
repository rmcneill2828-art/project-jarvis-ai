# RBL-0034 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0034 |
| Title | ESR-0054 Repository Baseline (EBG-0038 Relevance Check; GIA Phase 3a Git State Observability) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0054_ENGINEERING_SESSION_REPORT|ESR-0054]] |
| Previous Baseline | [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 28 August 2026 |
| HEAD at baseline creation | `7bbd85c` |

---

# 2. Purpose

RBL-0034 records the repository baseline accepted by the Programme Sponsor at ESR-0054 WP7, superseding [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]]. ESR-0054 opened at the Programme Sponsor's direct request, following an explicit instruction to read PBK-0001. It ran two Work Packages: WP1 (a Programme Sponsor-directed relevance check that closed EBG-0038 - "Formal AIEMS Standards Review" - Complete, concluding no new formal AIEMS standard was warranted, since the underlying need had already been met organically by other artefacts) and WP2 (resolved the first slice of EBG-0083 Phase 3, GIA Git State Observability - following a Programme Sponsor question about getting JARVIS/Guardian/Sentinel to a position where it can become aware of its own code, recommend improvements, and eventually assist with engineering work, discussed and agreed as a staged Layer 1/2/3 path). WP2 delivered a real, invokable, read-only backend capability: JARVIS can now observe its own repository's git state.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session for WP2's new GIA capability, flagged as a documentation-staleness item for a future session's Documentation Debt sync, matching the same disclosed pattern prior baselines have carried forward. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0054 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation, including a Documentation-Debt Priority check (PBK-0001) that found no open EBR-0001 item concerning governance-documentation staleness - the check does not gate this session's Work Package selection.

**WP1**: rather than committing directly to the "Formal AIEMS Standards Review" as EBG-0038 originally scoped it, the Programme Sponsor directed a relevance check first. All seven CI-0001 through CI-0007 working practices from ESR-0006 were checked against current live practice: four already formalised or absorbed under other names (OSE-0001; WP6 Independent Repository Verification; STD-0004/PBK-0001's WP6/WP7 approval-validation-verification-acceptance split), two never took hold beyond ESR-0006/ESR-0007 (zero live references found), one lapsed silently without formal retirement, one has only thin remaining substance. Conclusion: no new formal AIEMS standard warranted. Documentation-only - no code, architecture, or new standard created.

**WP2**: following the Programme Sponsor's direct question about JARVIS/Guardian/Sentinel self-awareness and future engineering assistance, a three-layer staged path was discussed and agreed - Layer 1 (awareness), Layer 2 (recommendation, via Guardian's Cognitive Core), Layer 3 (assistance, gated behind a future GAM-0001 governance decision on `LOCAL_AGENT_ACTION`). The Programme Sponsor selected starting at Layer 1 with GIA Phase 3a (Git State Observability), the cheapest, fastest-to-verify first slice of EBG-0083 Phase 3, matching the staged-increment discipline EBG-0083's own Phase 1 (1a/1b/1c/1d) already established.

**WP2 design review (Codex, `codex exec -s workspace-write`)**: [[EIP-ESR0054-002_GIA_PHASE3A_GIT_STATE_OBSERVABILITY|EIP-ESR0054-002]] v0.1 reviewed Conditional Pass with correction - repository-root resolution changed from eager (at `RealGitStateReader` construction) to lazy (on first git-command invocation, cached after success), so a missing `git` executable or transient failure cannot break unrelated runtime/RPC construction - folded into v0.2.

**Pre-implementation approval gate**: Programme Sponsor approval-to-implement obtained and verified via `submit-response` directly against the real Sponsor Approval Service for WP2, before any code was written.

**WP2 post-commit review**: genuine independent Codex review of the real committed diff (`187fd0a..d454eb5`) - **Pass, no findings**. Confirmed exactly the 13 expected files changed, no unexpected `src/`/`src-tauri/`/`sentinel/policy.py`/`GAM-0001` path; independently read `RealGitStateReader`'s lazy-resolution behaviour and the `gia.engineeringStatus` wiring directly against source.

**Session-wide WP6 Independent Repository Verification**: covering the full session range `59f9f2a..HEAD` (WP1 and WP2 combined, 3 commits, `59f9f2a` independently self-confirmed by Codex as ESR-0053's own final closure commit before reviewing). **Pass, no findings** - confirmed exactly the expected changed paths, no scope creep; `sentinel/policy.py` and `GAM-0001` byte-identical/untouched across the whole session; WP1 and WP2 both genuinely reflected in EBR-0001/REG-0001/ESR-0054 consistently with the actual diff. Codex's own advisory assessment: Establish - WP2 adds a real, invokable backend capability, even though read-only and non-disruptive to existing live behaviour.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with Codex's advisory - WP2 delivered a genuine new backend capability (JARVIS's first real observability of its own repository state), the first concrete step of a staged path toward JARVIS code/repository self-awareness and future engineering assistance.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/gia/engineering_observability.py` (new) | `EngineeringSnapshot` (frozen dataclass), `GitStateReader` Protocol, `RealGitStateReader` (real `git` CLI, lazy cached repo-root resolution), `EngineeringStateObserver` (observe-only, no thresholds/decisions). |
| `jarvis/agents/gia_engineering_agent.py` (new) | `GiaEngineeringAgent` (`gia-engineering`), classified `ROUTINE_INTERACTION`, mirrors `GiaObservabilityAgent`'s shape. |
| `jarvis/interfaces/stdio_rpc.py` | New ungated `gia.engineeringStatus` RPC method mirroring `gia.status`'s wiring; `gia-engineering` registered in `build_default_runtime()`'s `agents` dict, reusing the shared `SentinelTrustGateway`. |
| `jarvis/interfaces/activity_tracker.py` | `gia.engineeringStatus` added to `METHOD_CLUSTERS`. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0038 closed `Complete` (relevance check finding); EBG-0083's row extended with the Phase 3a delivery note. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session for WP2's new GIA capability - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync.

---

# 7. Architecture Outcomes

- JARVIS gains its first real, live-verified read access to its own repository/engineering state - a new capability, not a behaviour change to any existing one.
- `gia.engineeringStatus` and `gia-engineering` follow the identical injectable-observer/shared-gateway pattern already established by `gia.status`/`gia-observability` - no new architectural shape introduced.
- `sentinel/policy.py` and `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remain completely untouched - this WP delivers Layer 1 (awareness) only; Layer 2 (recommendation) and Layer 3 (assistance, which would require a GAM-0001 governance decision) remain distinct future work.
- No change to `src/`/`src-tauri/` - backend-only capability delivery, per PBK-0001's Feature-First Delivery Discipline allowance.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- Repository health (`validate_repository.py` invocation/parsing) and session/baseline state (REG-0001 parsing) remain explicitly deferred to future EBG-0083 Phase 3b/3c slices - not attempted here;
- no connection from this new observability data into Guardian's Cognitive Core or any recommendation-producing capability (Layer 2) - awareness data only, not reasoning over it;
- no write/mutating git operation of any kind - read-only observation only;
- no UXP/frontend surface for this data.

---

# 9. Verification

Repository validation performed across ESR-0054's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`59f9f2a..HEAD`, 3 commits) pushed to `origin/main`.
- 549 Python tests passing plus 1 correctly-skipped test - up from 538/1 at RBL-0033 (11 new tests: 5 observer/reader, 4 RPC wiring, 2 agent).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout, 298 warnings (unchanged, all pre-existing).
- WP2 design review (Codex): v0.1 Conditional Pass with correction, folded into v0.2.
- WP2 post-commit review (Codex): Pass, no findings.
- Session-wide WP6 (Codex): Pass, no findings, covering the full session diff against RBL-0033.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`) - approval-to-implement verified for real before implementation began, including a genuine drift-refusal-and-retry on one recording-only commit where the Sponsor's chat "Approved" had not yet been backed by a fresh real service decision.
- Live end-to-end verification against this repository's real git state, not fake-reader coverage alone: both a real `gia.engineeringStatus` RPC call and a real `guardian.agent.invoke` call for `gia-engineering` returned `main`/10 uncommitted files/commit `187fd0a`, independently confirmed to match `git rev-parse --abbrev-ref HEAD`/`git status --porcelain`/`git log -1` run directly.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0033 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh for this session's new GIA engineering-instrumentation capability - not yet reflected there.
5. EBG-0083 Phase 3b/3c (repository health via `validate_repository.py`; session/baseline state via REG-0001) - the next slices of the same Layer 1 (awareness) work.
6. Layer 2 (feeding GIA's engineering-state awareness into Guardian's Cognitive Core to produce read-only recommendations) - a distinct future initiative discussed but not scoped this session.
7. Layer 3 (a GAM-0001-gated capability for JARVIS to actually act on the repository) - requires an explicit future Programme Sponsor governance decision before any code is written.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0054_ENGINEERING_SESSION_REPORT|ESR-0054]] | Session this baseline is drawn from. |
| [[EIP-ESR0054-002_GIA_PHASE3A_GIT_STATE_OBSERVABILITY|EIP-ESR0054-002]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0038 closed this session; EBG-0083 extended with Phase 3a. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A's `LOCAL_AGENT_ACTION` boundary, named as the governance gate any future Layer 3 capability would need to cross. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0033, following a Codex design review (WP2 v0.1 Conditional Pass with correction, folded in before implementation), verified pre-implementation approval gate, a post-commit Codex review (Pass, no findings), session-wide WP6 Independent Repository Verification (Pass, no findings), and the Programme Sponsor's explicit WP7 decision to cut a new baseline, agreeing with Codex's own advisory: WP2's new, real, invokable GIA git-state observability capability warrants a new baseline. |
