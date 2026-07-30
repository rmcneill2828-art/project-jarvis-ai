# EIP-ESR0041-001 - Local Agent Permission Boundary

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0041-001 |
| Artefact ID | EIP-ESR0041-001 |
| Title | Local Agent Permission Boundary |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0021 |
| Intended Session | ESR-0041 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0021 (JARVIS Local Agent Permission Boundary) has been open since ESR-0004's original vision recovery, and was promoted to Approved Backlog at ESR-0034 WP2 with explicit text: "no stated prerequisite blocks acceptance - unlike WP1's items, this one is itself the prerequisite gate for the Action faculty (per EBG-0041's recommended sequencing: wiring, then Memory, then Voice/Vision, then Action) and touches GAM-0001 trust-boundary territory... warrants its own dedicated future session rather than incidental treatment... No implementation is authorised by this promotion." [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Section 7.3 records it as Phase 2, directly ahead of Phase 3 (Action faculty implementation). This package is that dedicated definition.

Confirmed directly against the live code before drafting: no local-agent, device-control or automation module exists anywhere in the repository. `sentinel/policy.py`'s `TrustTierPolicy` already reserves a classification slot for this category (`TrustCategory.LOCAL_AGENT_ACTION`, matched when `payload_type in {"local_agent", "device_control"}` or `capability == "local_agent"`) and unconditionally denies it - this has been the live production policy since EBG-0074 wired `TrustTierPolicy` as `SentinelCore`'s default (ESR-0024). No code path constructs such a request today, so the deny is real but currently dormant. [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 6.3 and Section 8.5 both already name this category as closed "pending EBG-0021's own separate definition," and Section 11 lists EBG-0021 as anticipated future evolution requiring "a separately approved engineering package." This package is that amendment.

---

# 3. Objective

Define, as a new section of [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]], the permission boundary that would govern any future local-agent/device-control action Guardian might request - what counts as a local agent action, the maximum authority ceiling any such action may ever reach, illustrative action tiers, and who may approve one - without implementing a Local Agent module, without moving any specific action out of Section 6.3's current `DENY`, and without changing Sentinel's classifier behaviour.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `sentinel/policy.py` `TrustCategory.LOCAL_AGENT_ACTION` | Exists since ESR-0016 WP1 as a forward-compatible extension point (`TrustCategory` docstring: "EBG-0020 and EBG-0021 identify future boundary areas, but they do not yet define complete taxonomies"). `TrustTierPolicy.classify()` matches it on `payload_type in {"local_agent", "device_control"}` or `capability == "local_agent"`. |
| `sentinel/policy.py` `TrustTierPolicy.evaluate()` | Unconditionally `DENY`s `LOCAL_AGENT_ACTION`, `EMERGENCY_CONTROL` and `UNSUPPORTED_HIGH_RISK` alike, with reason text "not yet supported by an approved implementation boundary." |
| `EBG-0074` (EBR-0001, Complete, ESR-0024) | `TrustTierPolicy` is the live production policy engine (`build_default_runtime()`), not merely additive/opt-in - confirmed via `runtime.sentinel_gateway().policy_engine` isinstance check. No production call site currently varies request shape to trigger `LOCAL_AGENT_ACTION`, since no such action-producing code exists. |
| `jarvis/gia/observability.py` | GIA's local resource observability (CPU/memory/disk/process presence via `psutil`) is read-only, never modifies device state, and does not route through Sentinel at all. It is observation, not control - the same distinction GAM-0001 Section 8.5 already draws between camera/monitoring and device control for family safety. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 6.3 | "local-agent action (EBG-0021 not yet defined)... GAM-0001 does not open local-agent action; it records that it remains closed until EBG-0021 defines the boundary under which it could ever move to Section 6.2." |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 | Household role model: Administrator (full authority, sole author of Section 8.4 pre-approved emergency policy), Adult (may approve Section 6.2 `REVIEW` actions), Child (cannot approve `REVIEW`), Guest (Autonomous-tier only). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.4 | Pre-approved emergency actions require Administrator-role authorship specifically, not the general Adult approval authority Section 6.2 otherwise grants - precedent for a stricter role requirement on a higher-risk action category. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 11 | Lists EBG-0021 as anticipated future evolution: "defines the boundary Section 6.3 and Section 8.5 currently leave closed, once a local agent implementation is planned... Any such evolution shall require separately approved engineering packages." |
| Original vision source (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`) | "Avoid background services that are difficult to stop," "Avoid system-level permissions," "Avoid local device control" listed as things to avoid at the MVP stage; Local Agent recorded as its own distinct future module (MLP 0.5). EBG-0021's own registered text: "local agents must not receive unlimited control." |

---

# 5. Scope

This package authorises amending [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] by inserting a new Section 8A (between Section 8 Family Safety and Section 9 Approval and Escalation Path, avoiding renumbering of Sections 9-14, matching the project's existing lettered-section convention used elsewhere for post-hoc additions) with the following content, verbatim subject to Codex/Programme Sponsor review:

```text
# 8A. Local Agent Permission Boundary

Resolves EBR-0001 EBG-0021 (JARVIS Local Agent Permission Boundary, open
since ESR-0004's EKR-0001 vision recovery, promoted to Approved Backlog at
ESR-0034 WP2 as "the root gate for the Action faculty," per JRM-0001 Track B
Section 7.3 Phase 2). This section defines the permission boundary; it does
not implement a Local Agent module, and it does not move any action out of
Section 6.3.

## 8A.1 What This Boundary Governs

A "local agent action" is any Guardian-initiated action that would control,
configure or modify state on the local device or a connected local system,
outside JARVIS's own already-governed conversational/data path - the same
category Sentinel's TrustCategory.LOCAL_AGENT_ACTION already reserves an
extension point for (sentinel/policy.py: TrustTierPolicy.classify() matches
payload_type in {"local_agent", "device_control"} or capability ==
"local_agent"). No such request is ever constructed anywhere in the
repository today - confirmed directly against the live code: no local-agent,
device-control or automation module exists under jarvis/ or elsewhere. This
section defines the boundary content in advance of that capability, per
EBG-0021's own text ("Define local device control limits before local agent
implementation").

Observation is not control. GIA's existing local resource observability
(jarvis/gia/observability.py - CPU, memory, disk, process presence) reads
local system state but never modifies it, and does not go through
Sentinel's request path at all. It is not a "local agent action" under this
section and is unaffected by it, matching Section 8.5's existing
distinction between observation/monitoring and device control.

## 8A.2 Category Ceiling: No Local Agent Action May Ever Be Autonomous

EBG-0021's own text states "local agents must not receive unlimited
control." That text supports, but does not by itself logically compel, a
rule this strict - the stricter rule below is a deliberate GAM-0001 policy
decision, made under Section 7's "no silent capability expansion"
principle, not a direct unavoidable consequence of the backlog text alone.
This section sets a hard ceiling: no local agent action may ever be
classified Section 6.1 (Autonomous) - the ceiling for any local agent
action, however narrow or reversible, is Section 6.2 (Approval-Required),
and only once a future, separately approved Engineering Implementation
Package defines the concrete enforcement mechanism for that specific named
action. This is a permanent constraint on this category, not a default
that a future package may quietly loosen - loosening it would itself
require a further explicit amendment to this section, not merely an
implementation package citing it.

## 8A.3 Action Tiers

| Tier | Examples | Ceiling |
|---|---|---|
| Permanently out of scope | Deleting or modifying data outside JARVIS's own governed storage; disabling or weakening security controls, backups or Sentinel itself; operating-system or firmware-level changes; installing, uninstalling or updating software; force-terminating an application (bypassing unsaved-work/save prompts); any smart-home command touching physical security or safety-critical state - locks, alarms, garage doors, gates, or heating/cooking/power controls capable of causing harm or property damage; any action with no realistic undo | Section 6.3 (DENY), permanently - not eligible to move to 6.2 under this section. Moving any of these would require a future amendment to this section itself, not merely an implementation package. |
| Conditionally eligible | Launching, or gracefully requesting the close of (respecting normal user-facing save prompts, never force-terminating), a specific, named, already-installed application at explicit user request; sending a notification, or a command with no physical-security or safety-critical effect (for example switching a labelled light or plug on/off), to a specific, named, already-paired smart-home device the user has explicitly configured; adjusting a JARVIS-owned configuration value | Section 6.2 (REVIEW) at most, only once a future implementation package names the specific action, defines its reversal path, and is itself separately approved. Remains Section 6.3 (DENY) until that happens - this section does not itself reclassify anything. |

This table is illustrative, not exhaustive - a future implementation
package proposing a local agent action not listed here shall be assessed
against 8A.2's ceiling and 8A.4's approval requirement, not assumed
permitted by omission, consistent with Section 7's "deny-by-default for the
unclassified" principle. Any smart-home or device command whose
physical-security or safety classification is ambiguous shall be treated
as permanently out of scope until a future amendment to this section
resolves the ambiguity - the conditionally-eligible tier does not extend to
uncertain cases by default.

## 8A.4 Approval Authority

Where a future package narrows a specific local agent action to Section
6.2, approval for that action requires the Administrator household role
(Section 8.1), not the general Adult approval authority Section 6.2
otherwise grants. This is a new, category-specific policy choice, by
analogy to (not a restatement of) Section 8.4's requirement that
pre-approved emergency actions be Administrator-authored: local agent
actions carry materially higher risk (they act on the device itself, not
within JARVIS's own governed data) than the ordinary approval-required
actions Section 6.2 contemplates, even though the two mechanisms differ
(Section 8.4 is advance policy authorship, this is per-instance approval).
This does not amend Section 8.1's role table; it states a stricter
application of it for this one category.

## 8A.5 Non-Goals

This section does not:

- implement a Local Agent module, agent framework wiring, or any
  device-control code;
- change Sentinel's TrustCategory.LOCAL_AGENT_ACTION classification
  behaviour - it remains DENY for every request today, exactly as before
  this section existed;
- authorise any specific named action to move to Section 6.2 - 8A.3's
  "conditionally eligible" tier states a ceiling, not a grant;
- define the Local Agent module's own architecture (transport, sandboxing,
  process isolation) - that remains a future implementation package's
  scope, constrained by this boundary.
```

This package also authorises the following consequential, minimal edits to keep GAM-0001 internally consistent:

1. Section 6.3: replace "local-agent action (EBG-0021 not yet defined)" and the trailing "it records that it remains closed until EBG-0021 defines the boundary under which it could ever move to Section 6.2" with a cross-reference to Section 8A, stating the boundary is now defined there while the classification itself remains unchanged (`DENY`).
2. Section 8.5: replace "which remains closed pending EBG-0021's own separate definition" with a cross-reference to Section 8A.
3. Section 11 (Future Evolution): remove EBG-0021 from the still-open anticipated list, since this package resolves it; retain EBG-0019 unchanged.
4. Document Control: version 1.2 to 1.3; Effective Date updated; Version History entry added.
5. Related Artefacts / OSE Relationships: add [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] cross-reference for Track B Phase 2 if not already present (GAM-0001's current Related Artefacts/OSE tables reference EBR-0001 but should be checked for JRM-0001 presence during implementation).

Mark [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0021 Complete, mirroring the precedent set when GAM-0001 Section 8 resolved EBG-0020 (EBR-0001 row: "Completed"). Update [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Section 7.3's Phase 2 row to record delivery at ESR-0041 WP1, mirroring the Phase 1/EBG-0108 update pattern at ESR-0035 WP2 (v1.19).

No other files are authorised to change. No source code (`sentinel/`, `jarvis/`) changes are required or in scope - this is an architecture/policy-definition package only, matching the precedent set by GAM-0001's own original creation (EBG-0031/0020/0048, ESR-0023) and by EIP-ESR0040-001's scoping-first pattern.

---

# 6. Authorised Files

1. `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md`
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
4. `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. Section 8A's text shall be inserted verbatim as drafted in Section 5 above (subject to any changes required by Codex/Programme Sponsor review before approval), preserving the existing lettered-section convention rather than renumbering Sections 9-14.
2. Section 6.3 and Section 8.5's cross-reference updates shall not alter their surrounding sentences beyond replacing the "not yet defined" / "pending EBG-0021" language with a pointer to Section 8A - Section 6.3's classification-precedence content and Section 8.5's observation/control distinction are otherwise unchanged.
3. No enum, classifier, or runtime code shall be touched - `TrustCategory.LOCAL_AGENT_ACTION` and `TrustTierPolicy.evaluate()`'s unconditional deny for it remain byte-identical to today.
4. Version History entries in GAM-0001, EBR-0001, REG-0001 and JRM-0001 shall each record this package's ID and a one-line summary, matching the precedent format used for GAM-0001 v1.1/EBG-0020 (REG-0001 3.159) and v1.2/EBG-0048 (REG-0001 3.163).

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any Local Agent module, device-control code, or agent framework implementation ([[ADR-0011_AGENT_FRAMEWORK|ADR-0011]]'s own scope, unchanged).
2. Any change to `sentinel/policy.py`, `TrustCategory`, `TrustTierPolicy`, or any Sentinel classification/enforcement behaviour.
3. Reclassifying any specific named action out of Section 6.3 - 8A.3's "conditionally eligible" tier is a ceiling for future packages to work within, not a present grant.
4. Any change to [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Action faculty description - it remains "Requests authorised execution through automation, agents or platform services," Not Started, unchanged by this package.
5. Any UXP (`src/`, `src-tauri/`) change.
6. Fixing the README.md staleness disclosed at this session's WP0A (four sessions/four baselines behind) - explicitly deferred to a future Documentation Debt Discipline pass per the Programme Sponsor's session-objective selection, not this package's scope.

---

# 9. Constraints

1. No GAM-0001 change shall be made until this package reaches Approved status, per PBK-0001 Principle 3 and EBG-0021's own registration text ("No implementation is authorised by this promotion").
2. This package must be reviewed by the Engineering Reviewer (Codex) both at design stage (this package) and post-commit against the real pushed diff, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0040.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors (warning count may shift by the same disclosed cross-document Section-reference false-positive category noted in recent sessions).
2. All WikiLinks in the new Section 8A and the edited cross-references resolve to real, existing artefacts.
3. No unauthorised files changed; no `sentinel/` or `jarvis/` file touched.
4. GAM-0001's Document Control version, Section 6.3, Section 8.5 and Section 11 are mutually consistent with the new Section 8A - no remaining "not yet defined"/"pending EBG-0021" language survives outside Section 8A's own resolves-line.

`python -m pytest` is not expected to change (no code touched) but should be re-run to confirm no regression, consistent with PBK-0001's Operational Verification Before Reporting.

---

# 11. Risks and Dependencies

## Dependencies

None new. This package builds entirely on already-approved architecture (GAM-0001 v1.2, Sentinel's `TrustCategory.LOCAL_AGENT_ACTION` extension point from ESR-0016, `TrustTierPolicy`'s production wiring from EBG-0074/ESR-0024).

## Risks

1. **8A.3's Action Tiers table is illustrative, not exhaustive**, by design - a future implementation package will need to classify actions this table does not literally name. 8A.3's own closing sentence addresses this by falling back to 8A.2's ceiling and Section 7's deny-by-default principle, but the table's concrete examples were chosen by the Engineering Implementer without a full survey of what a real Local Agent module would eventually need to do - a future scoping session may find the tiers need refinement once a concrete first local-agent capability is actually proposed. Disclosed, not solved, by this package - consistent with GAM-0001's own stated purpose ("architectural authority only").
2. **8A.4's Administrator-only approval requirement for local agent actions is a new, stricter-than-default policy choice** not dictated by any single existing GAM-0001 clause - it follows Section 8.4's precedent by analogy (higher risk than ordinary Section 6.2 actions) but is this package's own judgement call, not a restatement of existing text. Flagged explicitly for Programme Sponsor approval alongside the rest of this package, since it materially narrows who could ever approve a future local-agent action compared to Section 6.2's general Adult-approval default.

## New Backlog Item Registered by This Draft

None. This package resolves EBG-0021 without surfacing a new distinct gap - unlike EIP-ESR0039-001's EBG-0110, no new operational question is disclosed here that isn't already captured by Risk 1/2 above and by EBG-0021's own remaining sequencing note (a future package must still define the Action faculty implementation itself, already tracked as JRM-0001 Track B Phase 3, no new item needed).

---

# 12. Approval Request

Draft v0.1 submitted to Codex via the AIEMS Exchange Bridge (`ESR-0041`/`WP1`), reviewed by direct `codex exec -s read-only` invocation per the established EBG-0096 pattern. **Result: Fail with findings.** One real classification problem in 8A.3: "sending a notification or command to a specific, named, already-paired smart-home device" was too broad - an unqualified "command" could include unlocking doors, disabling alarms, opening garages or changing safety-critical heating/cooking/power state, none of which belongs in a conditionally-eligible tier. "Closing a specific application" was similarly too broad if it included force-termination with unsaved-work loss. Codex confirmed `sentinel/policy.py`'s claims (`TrustCategory.LOCAL_AGENT_ACTION` existence, classification predicates, unconditional deny) were accurate, confirmed the Section 6.3/8.5/11 cross-reference edits were correctly scoped, and confirmed closing EBG-0021 on a policy-only package is consistent with the EBG-0020/GAM-0001-Section-8 precedent. Non-blocking: 8A.2's justification should be framed as a deliberate GAM-0001 policy decision under Section 7's no-silent-expansion principle rather than a forced consequence of EBG-0021's text alone; 8A.4's Administrator-only requirement should be framed as a new policy choice by analogy to Section 8.4, not an exact restatement of it (the two mechanisms differ: advance policy authorship versus per-instance approval).

**v0.2 revision**, addressing all findings: 8A.3's Action Tiers table now moves any smart-home command touching physical security or safety-critical state (locks, alarms, garage doors, gates, heating/cooking/power capable of causing harm or property damage) to "permanently out of scope," narrows the conditionally-eligible smart-home example to notifications and non-safety-critical commands (for example switching a labelled light or plug), narrows "closing an application" to graceful/request-close only (force-termination moved to "permanently out of scope"), and adds an explicit "ambiguous classification defaults to permanently out of scope" closing rule. 8A.2 reframed to state the stricter-than-EBG-0021-alone ceiling is a deliberate GAM-0001 policy decision under Section 7, not a forced consequence. 8A.4 reframed to state the Administrator-only requirement is a new policy choice by analogy to Section 8.4, naming the mechanism difference explicitly rather than implying equivalence.

**v0.2 resubmitted to Codex for confirmation via direct `codex exec -s read-only` invocation. Result: Pass.** Codex confirmed all three findings adequately addressed: 8A.3's narrowed tiers correctly move force-termination and safety/security-critical smart-home commands to permanently out of scope, limit conditionally-eligible smart-home commands to non-safety-critical cases, and add the ambiguity-defaults-out-of-scope rule; 8A.2 now correctly frames the ceiling as a deliberate policy decision under Section 7 rather than a forced consequence of EBG-0021's text; 8A.4 now correctly frames Administrator-only approval as a new category-specific policy choice by analogy, naming the mechanism difference from Section 8.4 explicitly.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**Implemented exactly as scoped.** [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] v1.3: new Section 8A inserted between Section 8 and Section 9 (no renumbering); Section 6.3 and Section 8.5 cross-references updated to point to Section 8A; Section 11 updated to remove EBG-0021 from the still-open future-evolution list; Related Artefacts/OSE Relationships EBR-0001/JRM-0001 rows updated to include EBG-0021 among resolved items. Whole-document staleness sweep (PBK-0001) also corrected a stale RBL-0015 "current baseline" reference in Section 12 to RBL-0025. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0021 marked Completed; Section 5A Theme 3 loses its now-resolved row, open-item total corrected from 30 to 29. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]: Track B Section 7.3 Phase 2 marked Delivered; Section 7.1 Near-term emptied (Phase 2 was its only occupant); Section 7.2 Foundation list extended; Section 7.3 Phase 3 row updated to reflect Phase 2's constraint now being delivered. No `sentinel/` or `jarvis/` file touched - `TrustCategory.LOCAL_AGENT_ACTION` and `TrustTierPolicy.evaluate()`'s unconditional deny remain byte-identical to before this package.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Architecture this package amends. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0021 (this package's parent item), to be marked Complete on approval and implementation. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Section 7.3, Phase 2 - the roadmap placement this package delivers. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Action faculty definition this boundary will eventually gate; not itself changed by this package. |
| [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | Agent Framework decision this boundary would constrain once a Local Agent implementation is proposed; not itself changed by this package. |
| [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Working Report Lifecycle discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Programme Sponsor approved**, verified via `submit-response` against the real Sponsor Approval Service. **Implemented exactly as scoped**: GAM-0001 v1.3 (new Section 8A, Section 6.3/8.5/11 cross-reference updates, RBL-0015-to-RBL-0025 staleness fix), EBR-0001 v1.145 (EBG-0021 Completed, Section 5A Theme 3 updated), JRM-0001 v1.22 (Track B Phase 2 Delivered, Section 7.1/7.2/7.3 updated). No code touched. |
| 0.3 | 30 July 2026 | Claude Engineering Implementer | v0.2 resubmitted to Codex via direct `codex exec -s read-only` invocation for confirmation: **Pass**, all three prior findings adequately addressed. Pending Programme Sponsor approval. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: Fail with findings. Addressed the one blocking finding (8A.3's smart-home "command" example too broad - split into safety-critical/permanently-out-of-scope versus narrow non-safety-critical/conditionally-eligible; "closing an application" narrowed to graceful close only, force-termination moved to permanently out of scope) and both non-blocking findings (8A.2 and 8A.4 reframed as deliberate policy choices, not forced consequences of existing text). |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0041 WP1. Reviewed by Codex: Fail with findings (see v0.2). |
