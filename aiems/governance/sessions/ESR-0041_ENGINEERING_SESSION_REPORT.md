# ESR-0041 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0041 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0041 |
| Date Opened | 30 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 in progress |

---

# 2. Purpose

This report records the opening and execution of ESR-0041, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] closed (29 July 2026), [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`). No open [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] item concerns documentation staleness as its own category, so PBK-0001's Documentation-Debt Priority discipline does not constrain WP0/WP1 selection this session.

**Finding disclosed to the Programme Sponsor at WP0A, not yet actioned:** README.md is stale - it still describes [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] as open and [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] as the current baseline, four sessions and four baselines behind the real state (ESR-0040 closed, RBL-0025 current). No EBR-0001 item tracks this yet; left for a future Documentation Debt Discipline pass rather than this session's own WP1, per the Programme Sponsor's objective selection below.

`scripts/session_launcher.py` was run to surface candidate objectives. Presented to the Programme Sponsor: EBG-0021 (Local Agent Permission Boundary, High, Approved Backlog, flagged as warranting its own dedicated session at ESR-0034 WP2), EBG-0065 (STD-0006 Configuration and Secrets Standard, High, Approved), EBG-0113 (Higher-Quality Guardian Voice Model, newly registered at ESR-0040 closure), and the remaining Section 5A theme candidates. **The Programme Sponsor selected EBG-0021 (Local Agent Permission Boundary).**

EBG-0021's own registration text and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Section 7.3 (Phase 2) are explicit that this item defines the boundary only - "local agents must not receive unlimited control" - before any local-agent implementation exists, matching the scoping-first pattern established at ESR-0039 (EBG-0108) and ESR-0040 (EBG-0112). This session's objective is therefore to produce a [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] architecture amendment defining that boundary, for Codex design review and Programme Sponsor approval - no local-agent code is authorised by this session's objective.

---

# 4. Engineering Authority

ESR-0041 opening was authorised by direct Programme Sponsor instruction on 30 July 2026, following review of PBK-0001, README.md, PST-0001, GDE-0001, COC-0001 and ESR-0040, confirming [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit objective-selection question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Define [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0021 (JRM-0001 Track B Phase 2, Local Agent Permission Boundary): against [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]]'s existing permission-boundary model and Sentinel's already-implemented `TrustCategory.LOCAL_AGENT_ACTION` extension point, define the concrete boundary that would govern any future local-agent/device-control action Guardian might request, and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before any GAM-0001 change is made.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0021: scope and define the Local Agent Permission Boundary as a GAM-0001 amendment; Codex design review; Programme Sponsor approval | Complete |
| WP2 | Session-wide Independent Repository Verification | Pending |
| WP3 | Session-wide Repository Baseline Determination | Pending |

---

# 6A. WP1 - EBG-0021: Local Agent Permission Boundary

Reviewed `sentinel/policy.py`, [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (Sections 6.3, 8, 8.5, 11), [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Action faculty, [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]], `jarvis/gia/observability.py`, and the original ESR-0004 vision-recovery source before drafting scope. Confirmed directly against the live code: no local-agent, device-control or automation module exists anywhere in the repository; Sentinel's `TrustCategory.LOCAL_AGENT_ACTION` already reserves an extension point, unconditionally denied by `TrustTierPolicy` (live production default since EBG-0074/ESR-0024).

Produced [[EIP-ESR0041-001_LOCAL_AGENT_PERMISSION_BOUNDARY_SCOPE|EIP-ESR0041-001]] (v0.1, Draft): a new [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A defining what counts as a local agent action (distinct from GIA's read-only observability), a permanent ceiling that no such action may ever be classified Autonomous, an illustrative Action Tiers table, and an Administrator-only future approval requirement.

Submitted to Codex for design review via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern - **v0.1: Fail with findings**. One blocking finding: 8A.3's smart-home "command" example was too broad (could include unlocking doors, disabling alarms, garage doors, safety-critical heating/cooking/power state); a secondary finding that "closing an application" should exclude force-termination. Two non-blocking findings: 8A.2's ceiling should be framed as a deliberate policy decision under Section 7, not a forced consequence of EBG-0021's text; 8A.4's Administrator-only requirement should be framed as a new policy choice by analogy to Section 8.4, not a restatement.

**v0.2 revision**: 8A.3 narrowed - safety/security-critical smart-home commands and force-termination moved to permanently out of scope; conditionally-eligible tier limited to non-safety-critical commands and graceful application close; an ambiguity-defaults-to-out-of-scope rule added. 8A.2 and 8A.4 reframed as deliberate policy choices. Resubmitted to Codex - **v0.2/v0.3: Pass**, all three findings confirmed adequately addressed.

Codex's own `return-findings` call cannot run inside its read-only sandbox (the established EBG-0096 limitation); both review rounds' findings were relayed verbatim into the bridge transcript by the Engineering Implementer under explicit per-instance Programme Sponsor approval for that relay act.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**Implemented exactly as scoped.** [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] v1.3: new Section 8A inserted between Sections 8 and 9 (no renumbering, matching the project's existing lettered-section convention); Section 6.3 and 8.5 cross-references updated to point to Section 8A; Section 11 updated to remove EBG-0021 from the still-open list. A whole-document staleness sweep (PBK-0001, triggered by opening the file for this edit) also corrected a stale RBL-0015 "current baseline" reference (Section 12) to RBL-0025. No `sentinel/` or `jarvis/` code touched - `TrustCategory.LOCAL_AGENT_ACTION` and its unconditional deny remain byte-identical to before.

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0021 marked Completed, mirroring the EBG-0020/GAM-0001-Section-8 precedent; Section 5A Theme 3 loses its now-resolved row (open-item total corrected from 30 to 29). [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]: Track B Section 7.3 Phase 2 marked Delivered; Section 7.1 Near-term emptied (Phase 2 was its only occupant) and Section 7.2 Foundation list extended; Section 7.3 Phase 3 (Action faculty) row updated to reflect Phase 2's constraint now being delivered rather than merely pending.

- Files: `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md`, [[EIP-ESR0041-001_LOCAL_AGENT_PERMISSION_BOUNDARY_SCOPE|EIP-ESR0041-001]] (new).

---

# 7. Related Artefacts

* [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed for WP0A/WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0021 (this session's objective).
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - the artefact this session's scoping amends.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Section 7.3, Phase 2, the roadmap placement motivating this session's objective selection.
* [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] - repository baseline at session open.
* [[EIP-ESR0041-001_LOCAL_AGENT_PERMISSION_BOUNDARY_SCOPE|EIP-ESR0041-001]] - this session's WP1 deliverable, Codex design-reviewed (v0.1 Fail with findings, v0.2/v0.3 Pass) and Programme Sponsor-approved via the real Sponsor Approval Service.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 30 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0021 (Local Agent Permission Boundary) resolved via GAM-0001 v1.3's new Section 8A, per EIP-ESR0041-001 (Codex design review: v0.1 Fail with findings on 8A.3's overly broad smart-home "command" example, v0.2/v0.3 Pass after narrowing). Programme Sponsor approval verified via `submit-response` against the real Sponsor Approval Service. EBR-0001 (EBG-0021 Completed) and JRM-0001 (Track B Phase 2 Delivered) updated. Architecture/policy-definition only - no code changed. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | ESR-0041 opened at WP0B, before WP1 began. Objective: define EBG-0021 (Local Agent Permission Boundary, JRM-0001 Track B Phase 2) as a GAM-0001 amendment and produce an Engineering Implementation Package for Codex review and Programme Sponsor approval. README.md staleness (4 sessions/4 baselines behind) disclosed at WP0A, not actioned this session. |
