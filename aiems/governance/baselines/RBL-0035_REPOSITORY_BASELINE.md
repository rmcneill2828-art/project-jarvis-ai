# RBL-0035 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0035 |
| Title | ESR-0055 Repository Baseline (GIA Phase 3b/3c: Repository Health and Register State Observability) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0055_ENGINEERING_SESSION_REPORT|ESR-0055]] |
| Previous Baseline | [[RBL-0034_REPOSITORY_BASELINE|RBL-0034]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 28 August 2026 |
| HEAD at baseline creation | `5254641` |

---

# 2. Purpose

RBL-0035 records the repository baseline accepted by the Programme Sponsor at ESR-0055 WP7, superseding [[RBL-0034_REPOSITORY_BASELINE|RBL-0034]]. ESR-0055 opened at the Programme Sponsor's direct request, following an explicit instruction to read PBK-0001 (initially given under a stale "ESR-0054" label, corrected once flagged that ESR-0054 was already closed). The Programme Sponsor then directed continuing where ESR-0054 left off: the GIA self-awareness staged path, specifically the remainder of EBG-0083 Phase 3 (engineering instrumentation) - Phase 3b (repository health) and Phase 3c (session/baseline state) together in one Work Package, completing Phase 3 in full. WP1 delivered a real, invokable, read-only backend capability: JARVIS can now observe its own repository's validation health and controlled-artefact register state, extending the git-state observability RBL-0034 established.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0034_REPOSITORY_BASELINE|RBL-0034]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session for WP1's new GIA capability, flagged as a documentation-staleness item for a future session's Documentation Debt sync, matching the same disclosed pattern RBL-0034 already carried forward for Phase 3a. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0055 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation, including a flagged and resolved session-identifier discrepancy (the session was initially opened under the stale "ESR-0054" label; WP0A found ESR-0054 already formally closed, and the Programme Sponsor confirmed opening ESR-0055 instead) and a Documentation-Debt Priority check (PBK-0001) that found no open EBR-0001 item concerning governance-documentation staleness - the check did not gate this session's Work Package selection.

**WP1**: the Programme Sponsor directed continuing the GIA engineering-instrumentation staged path from where ESR-0054 WP2 left off, selecting the remainder of EBG-0083 Phase 3 (repository health, session/baseline state) over Layer 2 of the broader self-awareness path (a materially larger, undesigned scope), and specifically Phase 3b and 3c together in one Work Package - finishing Phase 3 in full rather than one more single-slice increment.

**WP1 design review (Codex, `codex exec -s workspace-write`)**: [[EIP-ESR0055-001_GIA_PHASE3BC_REPOSITORY_HEALTH_AND_REGISTER_STATE|EIP-ESR0055-001]] v0.1 reviewed Conditional Pass with correction - the draft was internally inconsistent about `latestRegisteredSession`/`latestRegisteredSessionStatus` semantics (named as "latest registered session" while citing a filtered-to-Closed-only model, which disagree once a session is genuinely open). The Programme Sponsor selected the unfiltered reading, matching GIA's pure observe-and-publish constraint; folded into v0.2.

**Pre-implementation approval gate**: Programme Sponsor approval-to-implement obtained via direct chat instruction ("Approved").

**WP1 post-commit review**: genuine independent Codex review of the real committed diff (`10f080a`) - **Pass, no corrective findings**. Confirmed the diff matched EIP-ESR0055-001 v1.0 exactly, no unexpected `src/`/`src-tauri/`/`sentinel/policy.py`/`GAM-0001` path; independently confirmed the `EngineeringStateReader` rename, the 5 new snapshot fields, the subprocess (not import) packaging boundary, and the unfiltered-by-status register read.

**Session-wide WP6 Independent Repository Verification**: covering the full session range `2d74cc0..HEAD` (ESR-0054's own closure commit; WP1's implementation commit and its post-commit-review-recording follow-up commit). **Pass, no corrective findings** - confirmed exactly the expected changed paths, no scope creep; independently re-ran `pytest` (553 passed/1 skipped) and `validate_repository.py` (0 errors/298 warnings), both matching; EBR-0001/REG-0001/ESR-0055 confirmed internally consistent with the actual diff and with each other. Codex's own advisory assessment: Establish - WP1 adds a real, invokable backend capability, matching the Establish threshold applied at ESR-0049/ESR-0050/ESR-0051/ESR-0053/ESR-0054.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with Codex's advisory - WP1 delivered a genuine new backend capability (repository health and register-state observability), completing EBG-0083 Phase 3 in full as the direct continuation of ESR-0054's own Phase 3a delivery.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/gia/engineering_observability.py` | `GitStateReader`/`RealGitStateReader` renamed to `EngineeringStateReader`/`RealEngineeringStateReader` (no longer git-specific); `EngineeringSnapshot` gains `repository_validation_errors`, `repository_validation_warnings`, `current_repository_baseline`, `latest_registered_session`, `latest_registered_session_status`; `repository_validation()` (subprocess-invokes `scripts/validate_repository.py`) and `register_state()` (reads REG-0001 directly, unfiltered by status) added, sharing the existing lazy-cached repo-root resolution. |
| `jarvis/interfaces/stdio_rpc.py` | `gia.engineeringStatus`'s response extended with the 5 new camelCase fields - same RPC method, no new endpoint. |
| `jarvis/agents/gia_engineering_agent.py` | `GiaEngineeringAgent.execute()`'s payload extended with the same 5 fields. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083's row extended with the Phase 3b/3c delivery note; status label now "Complete (Phase 1 and Phase 3 in full; Phase 2/4 not delivered)". |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session for WP1's new GIA capability - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync (carrying forward the same disclosed gap RBL-0034 already flagged for Phase 3a).

---

# 7. Architecture Outcomes

- JARVIS's repository/engineering self-awareness now extends beyond git state (RBL-0034) to repository validation health and controlled-artefact register state - EBG-0083 Phase 3 (engineering instrumentation) is complete in full.
- `gia.engineeringStatus` and `gia-engineering` continue the identical injectable-observer/shared-gateway pattern already established - no new architectural shape introduced, only additive fields on the existing snapshot.
- `sentinel/policy.py` and `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remain completely untouched - this WP delivers Layer 1 (awareness) only.
- No change to `src/`/`src-tauri/` - backend-only capability delivery, per PBK-0001's Feature-First Delivery Discipline allowance.
- **Disclosed limitation carried forward from design**: `repository_validation()`/`register_state()` depend on files present only in a source/repository checkout (`scripts/validate_repository.py`, REG-0001) - neither is bundled into the Guardian Desktop distributable's PyInstaller sidecar freeze, matching the same characteristic RBL-0034's git-state fields already carried unstated.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no connection from this new observability data into Guardian's Cognitive Core or any recommendation-producing capability (Layer 2) - awareness data only, not reasoning over it;
- no write/mutating operation of any kind - `validate_repository.py` invoked read-only, REG-0001 only ever read;
- no caching of the repository-validation result across calls - every snapshot re-reads fresh, a disclosed ~2.5s latency cost per call;
- no UXP/frontend surface for this data.

---

# 9. Verification

Repository validation performed across ESR-0055's Work Package and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`2d74cc0..HEAD`, 2 commits) pushed to `origin/main`.
- 553 Python tests passing plus 1 correctly-skipped test - up from 549/1 at RBL-0034 (9 new tests).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout, 298 warnings (unchanged, all pre-existing).
- WP1 design review (Codex): v0.1 Conditional Pass with correction, folded into v0.2.
- WP1 post-commit review (Codex): Pass, no corrective findings.
- Session-wide WP6 (Codex): Pass, no corrective findings, covering the full session diff against RBL-0034.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`), including a genuine drift-refusal-and-retry on the post-commit-review-recording commit, where the prior approval (for HEAD at WP1's own commit) no longer matched the current repository state.
- Live end-to-end verification against this repository's real state, not fake-reader coverage alone: a real `gia.engineeringStatus` call returned `main`/9 uncommitted files/commit `2d74cc0`/0 validation errors/298 warnings/baseline `RBL-0034`/session `ESR-0055`/`Open`, independently confirmed to match `git rev-parse --abbrev-ref HEAD`/`git status --porcelain`/`git log -1`, a direct `validate_repository.py` run and a direct REG-0001 read.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0034 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0034_REPOSITORY_BASELINE|RBL-0034]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh for this session's new GIA repository-health/register-state capability, and RBL-0034's still-outstanding GIA git-state capability - not yet reflected there.
5. Layer 2 (feeding GIA's engineering-state awareness into Guardian's Cognitive Core to produce read-only recommendations) - a distinct future initiative discussed but not scoped this session.
6. Layer 3 (a GAM-0001-gated capability for JARVIS to actually act on the repository) - requires an explicit future Programme Sponsor governance decision before any code is written.
7. EBG-0083 Phase 2 (platform service instrumentation - Guardian/Sentinel/Agent Framework/Memory/Provider state) and Phase 4 (external instrumentation) - the two GIA phases still not delivered.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0034_REPOSITORY_BASELINE|RBL-0034]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0055_ENGINEERING_SESSION_REPORT|ESR-0055]] | Session this baseline is drawn from. |
| [[EIP-ESR0055-001_GIA_PHASE3BC_REPOSITORY_HEALTH_AND_REGISTER_STATE|EIP-ESR0055-001]] | Approved Engineering Implementation Package WP1's deliverables were built against. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083 extended with Phase 3b/3c, closing Phase 3 in full. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A's `LOCAL_AGENT_ACTION` boundary, named as the governance gate any future Layer 3 capability would need to cross. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0034, following a Codex design review (WP1 v0.1 Conditional Pass with correction, folded in before implementation), verified pre-implementation approval, a post-commit Codex review (Pass, no corrective findings), session-wide WP6 Independent Repository Verification (Pass, no corrective findings), and the Programme Sponsor's explicit WP7 decision to cut a new baseline, agreeing with Codex's own advisory: WP1's new, real, invokable GIA repository-health/register-state observability capability warrants a new baseline, completing EBG-0083 Phase 3 in full. |
