# EIP-ESR0048-001 - Agent Framework Architecture Scope

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0048-001 |
| Artefact ID | EIP-ESR0048-001 |
| Title | Agent Framework Architecture Scope |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0042 |
| Intended Session | ESR-0048 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0042 ("Agent Framework Architecture") asks to "define specialist agent contracts, including Engineering Agent, while preserving Guardian as the singular user-facing identity." It is JRM-0001 Track B Phase 3 (the Action faculty) - the next item in the roadmap's own dependency chain, both of whose prerequisites are now delivered: Phase 1 (Guardian Cognitive Core, ESR-0039) and Phase 2 (Local Agent Permission Boundary, [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, ESR-0041).

**On EBG-0042's Candidate Backlog status**: this item was deliberately left at Candidate Backlog during ESR-0034 WP1's batch promotion (EBR-0001 v1.130), grouped with four others as having "a genuine stated blocker or a pending separate review." Confirmed directly against the register: EBG-0042's own text names no explicit blocker beyond its ESR-0008/[[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] origin; the most plausible blocker at the time was EBG-0021 (the permission boundary this package must respect), which was itself promoted to Approved Backlog in the same WP1 and delivered at ESR-0041. This package's own review and Programme Sponsor approval below serve as the confirmation that blocker no longer applies - a formal Candidate-to-Approved promotion is not separately actioned by this package, consistent with [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]'s Approval Before Change discipline treating explicit package approval as the operative gate.

This package does not implement anything. [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] already decided agents are capabilities, not identities, and explicitly states it "does not implement agents or define detailed agent contracts" - reserving that for a future package. This is that package, for the architecture only.

---

# 3. Objective

Define, as a controlled architectural extension of [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]], the specialist agent contract shape Guardian's Action faculty will use to invoke bounded, named capabilities - constrained by [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A's existing Local Agent Permission Boundary and routed through Sentinel's existing trust gateway - without implementing, wiring, or authorising any actual agent, capability, or code.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A | Defines the boundary any agent framework must obey: a "local agent action" is any Guardian-initiated action that would control, configure or modify local device/system state (8A.1); no such action may ever be classified Autonomous - the ceiling is Approval-Required, only once a future package names the specific action (8A.2); an illustrative Action Tiers table separates permanently-out-of-scope actions (data deletion outside governed storage, disabling security controls, OS/firmware changes, software install/uninstall, safety-critical smart-home commands) from conditionally-eligible ones (launching a named app, non-safety-critical smart-home commands to a named paired device, adjusting a JARVIS-owned config value) (8A.3); approval for any narrowed action requires the Administrator household role specifically (8A.4); and 8A itself does not implement a Local Agent module, wire anything, or authorise any specific action (8A.5). |
| `sentinel/policy.py` `TrustTierPolicy.classify()`/`evaluate()` | `TrustCategory.LOCAL_AGENT_ACTION` already exists as an extension point, matched when `SentinelRequest.payload_type in {"local_agent", "device_control"}` or `metadata["capability"] == "local_agent"`. `evaluate()` hard-codes `DENY` for this category today, unconditionally - confirmed directly against the live code, unchanged since GAM-0001 8A was written. This package does not change this file. |
| `sentinel/core.py` `SentinelRequest`/`SentinelTrustGateway` | The existing request/evaluate contract every other Guardian capability already uses (conversation, memory, speech, transcription). Any future agent invocation would construct a `SentinelRequest` and call the same `gateway.evaluate()` - no new gating mechanism needs inventing. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] Guardian Faculties table | The Action faculty's architectural role is already stated: "Requests authorised execution through automation, agents or platform services." The Agent Relationship section already states: "Specialist agents provide domain capability to Guardian. They are not separate AI identities. Guardian asks agents how to accomplish specialist tasks and remains the user-facing entity." This package's contract shape must be consistent with, not a departure from, this existing text. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Already places "Agent Framework" in its platform diagram (a box under Guardian, alongside Provider Architecture, Automation, Voice, Vision, Memory) and its domain-interpretation table ("Specialist capability agents serving Guardian without becoming separate user-facing identities"), but has no dedicated section with contract detail - the "Core Architectural Domains" section has subsections for AI Core, Memory Services, Voice Services, Vision Services, Guardian/Sentinel/Trust Governance, Automation Services, User Experience Platform and Platform Services, but none for Agent Framework specifically. This package adds that missing subsection, per PBK-0001's Minimise Controlled Artefact Creation guidance (extend an existing home rather than create a new artefact). |
| [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | Already decided: agents are capabilities not identities; agents do not bypass Guardian, Sentinel or policy governance; agents operate through capability boundaries; future agent implementation requires separate approved packages. Explicitly out of its own scope: "does not implement agents or define detailed agent contracts." |
| `jarvis/platform/shell.py` `GuardianShellCapability` | Contains a static status-model entry named `"Agent Framework"` with `state=PLACEHOLDER` and summary "Future specialists extend Guardian without separate AI identities" - a UI status placeholder only, not executable logic. Confirmed by direct search: no agent module, package or execution code exists anywhere under `jarvis/` today. |
| EBG-0059 (Engineering Assurance Capability) | A prior in-session proposal to fold EAC into EBG-0042 was never executed - EBG-0042's own text has no mention of EAC/EAA/EAR. This package does not revisit that decision; EAC remains a separate, adjacent Candidate Backlog item. |
| EBG-0025 (Home Assistant/Smart Home Integration Assessment) | Approved Backlog, downstream of this package, not a dependency of it. GAM-0001 8A.3 already names smart-home commands as a conditionally-eligible tier example; EBG-0025's own assessment would need to run before any smart-home-specific agent is ever named under this package's contract. |

---

# 5. Scope

This package authorises a single new subsection in [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s "Core Architectural Domains" section, titled "## Agent Framework", positioned after "Automation Services" and before "User Experience Platform" (matching the existing subsection ordering, which loosely follows the platform diagram's box order).

The new subsection shall define, as architecture/contract description only (no code):

1. **What a specialist agent is**: a bounded, named provider of one specific domain capability, invoked only by Guardian's Action faculty, never directly by the user or the UXP - consistent with AAM-0001's existing "not a separate AI identity" principle. An agent is not itself a text-generation or conversation participant; it performs or reports on a named task and returns a structured result to Guardian, which alone composes any response to the household.
2. **The contract shape**: a `SpecialistAgent` Protocol - `name: str` (property) and `execute(request: AgentRequest) -> AgentResult` (method) - deliberately mirroring the existing `ExecutionProvider`/`SpeechSynthesisProvider`/`TranscriptionProvider` Protocol pattern already proven three times in this codebase (`sentinel/providers.py`, `sentinel/speech_providers.py`, `sentinel/transcription_providers.py`), not inventing a new interface shape. `AgentRequest`/`AgentResult` are named as future frozen dataclasses (task description, structured parameters, and a result payload plus a status field) - exact field lists are left to the future implementation package that actually builds this, since no agent exists yet to validate the shape against. Accepted as an architecture-level placeholder only (Codex design-review finding): a genuine future implementation may need lifecycle/status semantics beyond a single synchronous `execute()` call if an agent proves longer-running or partially-failing in practice - this package's proposed shape is a starting point for that future package to confirm or revise, not a settled final contract.
3. **The mandatory Sentinel gate**: every specialist agent invocation, without exception, is evaluated through `SentinelTrustGateway.evaluate()` before executing - exactly the same pattern conversation, memory, speech and transcription already use, reusing the same shared gateway instance those capabilities already share (not constructing a fresh one). This distinction matters concretely: `SentinelTrustGateway` defaults to `SimpleApprovalPolicy` when constructed bare (Codex design-review finding, folded in) - `TrustCategory.LOCAL_AGENT_ACTION`'s hard `DENY` is `TrustTierPolicy`'s behaviour specifically, the policy engine `build_default_runtime()` already wires as the production default and every other capability already relies on. A future implementation package must reuse that existing shared gateway/policy wiring, not merely call `evaluate()` on any gateway instance. An agent capability that only reads/reports information (touches no local device or system state) may classify `ROUTINE_INTERACTION`; an agent capability that would control, configure or modify local device/system state must classify `TrustCategory.LOCAL_AGENT_ACTION` per GAM-0001 Section 8A.1's existing definition, and therefore remains hard `DENY` until a future, separately-approved package names that specific action under 8A.3's Action Tiers and defines its reversal path per 8A.2. This package does not decide which agents fall into which category - it states the rule a future package must apply.
4. **Where the Engineering Agent fits**: named in EBG-0042's own text as the first illustrative specialist agent. This package records that GIA-BOOT (`jarvis/gia/`, ESR-0012 Proof of Concept) is a read-only observability capability, not an action-taking agent, and would classify `ROUTINE_INTERACTION` under item 3 above if and when it is formally wired as a specialist agent - a future decision, not made by this package. No other specific agent (Home Assistant, smart-home, or otherwise) is named or authorised here.
5. **Explicit non-authorisation statement**: mirroring GAM-0001 Section 8A.5's own pattern, the new subsection states plainly that it does not implement the Agent Framework, does not wire any agent into `GuardianRuntime`, does not change `sentinel/policy.py`'s existing hard `DENY` for `LOCAL_AGENT_ACTION`, and does not authorise any specific agent or capability - all remain future, separately-approved implementation packages.

---

# 6. Authorised Files

1. `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md` - new "## Agent Framework" subsection under "Core Architectural Domains"; Version History entry.
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - EBG-0042 status/notes updated to record this package's resolution of its Candidate-status blocker and this architecture's completion; item itself remains open pending a future implementation package (architecture defined, not yet built).
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - version sync.

No other file is authorised. No `sentinel/`, `jarvis/` or `src*/` file is touched by this package - it is architecture documentation only.

---

# 7. Implementation Requirements

1. The new MOD-0001 subsection must not contradict or restate GAM-0001 Section 8A - it should cross-reference it as the authority for what agents may do, not re-derive or duplicate the Action Tiers table.
2. The `SpecialistAgent`/`AgentRequest`/`AgentResult` naming must be presented as a proposed contract shape for a future implementation package to build against, not as already-existing code - no file path should be claimed to contain these names until a future package actually creates them.
3. The Engineering Agent / GIA-BOOT reference must accurately describe its current Proof-of-Concept, read-only nature (per ESR-0012) - not overstate it as already agent-framework-wired.

---

# 8. Explicit Exclusions

This package does not authorise:

1. **Any code change.** No `sentinel/`, `jarvis/`, `src/` or `src-tauri/` file is touched. This is a documentation-only architecture package, matching GAM-0001 Section 8A's and ADR-0011's own precedent.
2. **Any change to `sentinel/policy.py`'s `TrustCategory.LOCAL_AGENT_ACTION` handling.** It remains hard `DENY` for every request, exactly as today.
3. **Naming or authorising any specific agent capability** (Home Assistant, Engineering Agent as a live execution capability, or otherwise) beyond the illustrative GIA-BOOT read-only example in Section 5 item 4.
4. **A formal EBG-0042 Candidate-to-Approved backlog promotion as a separate governance act** - this package's own Programme Sponsor approval is treated as the operative confirmation the prior blocker no longer applies (Section 2), not a distinct promotion decision requiring its own vote.
5. **Any decision on EBG-0059 (EAC)'s relationship to the Agent Framework** - the prior non-fold decision stands, unrevisited.

---

# 9. Constraints

1. No file change shall be made until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template.
3. Section 5's contract shape (items 2-3 especially) is flagged as a genuine design proposal for Engineering Reviewer and Programme Sponsor scrutiny, not a settled fact - the Protocol-mirroring rationale should be checked against whether it genuinely fits an agent's different execution shape (potentially longer-running, potentially failing partway) as well as it fits synchronous provider calls.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors.
2. No unauthorised files changed - `git diff --name-only` matches exactly the Section 6 Authorised Files list.
3. Manual cross-check: the new MOD-0001 subsection's claims about GAM-0001 Section 8A and `sentinel/policy.py`'s current behaviour are re-verified against those live files at implementation time, not merely carried over from this draft.

No `pytest`/`cargo`/`playwright` run is required - no code is touched by this package.

---

# 11. Risks and Dependencies

## Dependencies

None new. Builds entirely on already-approved architecture (GAM-0001 Section 8A, ADR-0011, AAM-0001's Action faculty and Agent Relationship text) and an already-proven code pattern (the three existing Protocol-based provider contracts).

## Risks

1. **This package defines a contract shape no implementation has yet tested.** Unlike GAM-0001 Section 8A (a pure permission boundary, no shape to get wrong) or the Voice/Identity increments (which mirrored patterns already implemented once), this is the first time a not-yet-built capability's contract is being specified in the abstract. Disclosed as a genuine risk: a future implementation package may find the proposed shape needs revision once a real agent is built against it - this package does not claim otherwise.
2. **Leaving EBG-0042's Candidate Backlog status resolved by this package's own approval, rather than a separate promotion vote, is itself a minor process judgement call** (Section 2) - flagged explicitly for Programme Sponsor confirmation rather than assumed.
3. **No agent is unblocked for implementation by this package** - Sentinel's `LOCAL_AGENT_ACTION` remains hard `DENY`. This is architecture only; a future implementation package would still need to name a specific action, narrow it under GAM-0001 8A.3, and gain its own separate approval before any agent could actually do anything beyond read-only reporting.

## New Backlog Item Registered by This Draft

None anticipated. This package directly addresses EBG-0042 as scoped by its own registration text.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation. **Result: Pass with non-blocking findings.** Codex independently verified every Section 4 Repository Context claim against the live cited files (GAM-0001 Section 8A, `sentinel/policy.py`, `sentinel/core.py`, AAM-0001, MOD-0001, ADR-0011, `jarvis/platform/shell.py`, EBR-0001's EBG-0042/0059/0025 entries), confirmed the package stays within EBG-0042's scope, confirmed Section 5's contract shape is consistent with GAM-0001 Section 8A and AAM-0001 (not a restatement or contradiction), and confirmed correct architecture-only scoping. Three non-blocking findings - `SentinelTrustGateway`'s default policy is `SimpleApprovalPolicy`, not `TrustTierPolicy` (a future implementation must reuse the existing shared gateway, not construct a fresh default one); Candidate Backlog handling confirmed as a disclosed judgement call already correctly flagged for Sponsor confirmation; `execute()`'s lifecycle/status semantics accepted as an architecture-level placeholder - all three folded into v0.2. No blocking finding.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (ESR-0048/WP2) before implementation began.

**Implemented as scoped.** Full detail recorded in [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] Section 6B.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0042 (this package's parent item). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A - the permission boundary this package's contract must obey, cross-referenced not restated. |
| [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | The prior decision this package's own scope was explicitly reserved by ("does not implement agents or define detailed agent contracts"). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Action faculty and Agent Relationship text this package's contract must remain consistent with. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Target artefact - new Agent Framework subsection added under Core Architectural Domains. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Phase 3 (Action faculty) - this package addresses the architecture prerequisite the roadmap names as still missing. |
| [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change discipline and Minimise Controlled Artefact Creation guidance this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 August 2026 | Claude Engineering Implementer | **Implemented as scoped.** Programme Sponsor approval verified via the real Sponsor Approval Service (ESR-0048/WP2). New MOD-0001 "Agent Framework" subsection delivered exactly as scoped: `SpecialistAgent` contract shape, mandatory Sentinel gate, `ROUTINE_INTERACTION`/`LOCAL_AGENT_ACTION` split, Engineering Agent/GIA-BOOT placement, explicit non-authorisation statement. EBR-0001 EBG-0042 marked Completed. No code touched. |
| 0.2 | 4 August 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: **Pass with non-blocking findings.** Every Repository Context claim independently verified; scope confirmed within EBG-0042's authority; Section 5 contract shape confirmed consistent with GAM-0001 Section 8A and AAM-0001. Folded three non-blocking findings: clarified the future implementation must reuse the existing shared Sentinel gateway/`TrustTierPolicy` wiring rather than any bare `SentinelTrustGateway` (whose default policy is `SimpleApprovalPolicy`); Candidate Backlog handling confirmed as an already-correctly-flagged judgement call; `execute()`'s shape explicitly accepted as an architecture-level placeholder pending future lifecycle/status needs. Awaiting Programme Sponsor approval. |
| 0.1 | 4 August 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0048 WP2. Scopes a new MOD-0001 "Agent Framework" subsection defining a specialist-agent contract shape (Protocol mirroring existing provider patterns), the mandatory Sentinel gate, and where the Engineering Agent/GIA-BOOT fits - architecture only, no code, no agent authorised. Not yet reviewed or approved. |
