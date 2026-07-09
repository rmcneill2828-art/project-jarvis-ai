# ESR-0016 WP2 - SAM-0001 Trust-Tier Alignment Note

## 1. Purpose

This note records the ESR-0016 WP2 architecture alignment between `SAM-0001_SENTINEL_TRUST_ARCHITECTURE.md` and the Sentinel trust-tier policy model implemented during ESR-0016 WP1.

It is intentionally additive. It does not reopen WP1, modify Sentinel runtime behaviour, change the production policy default, or authorise new Guardian, automation, local-agent, UI, provider-execution or memory capability.

## 2. Repository Evidence Reviewed

Repository evidence reviewed for WP2:

- `aiems/governance/sessions/ESR-0016_ENGINEERING_SESSION_REPORT.md`
- `aiems/models/SAM-0001_SENTINEL_TRUST_ARCHITECTURE.md`
- `sentinel/policy.py`
- `sentinel/__init__.py`

The implementation evidence confirms:

- `TrustTier` defines the forward-compatible trust tiers: `ROUTINE`, `SENSITIVE`, `RESTRICTED`.
- `TrustCategory` defines current policy category slots: `ROUTINE_INTERACTION`, `HUMAN_APPROVAL_REQUIRED`, `EMERGENCY_CONTROL`, `LOCAL_AGENT_ACTION`, `UNSUPPORTED_HIGH_RISK`.
- `TrustTierPolicy` implements the existing `PolicyEngine` seam.
- `SimpleApprovalPolicy` remains present and unchanged as the production default policy used by `SentinelTrustGateway` unless a caller explicitly injects another policy engine.
- `TrustTier`, `TrustCategory` and `TrustTierPolicy` are exported from `sentinel/__init__.py`.

## 3. SAM-0001 Alignment Assessment

SAM-0001 remains directionally correct: it positions Sentinel as the trust, governance, protection and policy layer that governs the environment in which Guardian operates.

ESR-0016 WP1 adds a concrete implementation beneath that architecture by introducing an optional trust-tier policy model. The implementation aligns with SAM-0001 because it:

- preserves Sentinel as the policy and trust boundary;
- uses existing `SentinelRequest` data rather than introducing new execution surfaces;
- keeps policy evaluation inside the Sentinel boundary;
- supports human-review routing for sensitive requests;
- denies unsupported high-risk, emergency-control and local-agent categories until separately authorised;
- preserves the separation between Guardian companion experience and Sentinel trust enforcement.

## 4. Architecture Clarification

For current repository state, SAM-0001 should be read with the following clarification:

> ESR-0016 introduced an additive Sentinel trust-tier policy model. The model classifies Sentinel requests into routine, sensitive and restricted tiers using `TrustTierPolicy`, while preserving `SimpleApprovalPolicy` as the default production policy. The trust-tier model is an optional policy engine and does not by itself implement new platform capability, local-agent execution, emergency control, provider execution, automation, Guardian Memory, UI behaviour or production approval workflow.

This clarification updates interpretation of SAM-0001 without changing its original authority boundary.

## 5. Scope Compliance

WP2 remains documentation and architecture-alignment only.

Out of scope and not implemented by this note:

- Sentinel production default change
- Guardian Memory
- Local-agent execution
- Emergency-control implementation
- Provider execution expansion
- Automation
- UI or Guardian Orb changes
- Approval workflow storage
- Repository baseline acceptance
- ESR closure approval

## 6. Operational Guidance Note

During ESR-0016 WP2 execution, a platform connector issue caused a long-running GitHub update request to remain stuck after authentication, repository reads and file lookup had already succeeded.

This is classified as an operational platform issue, not an engineering defect.

Operational guidance:

> If the Engineering Implementer encounters a platform or connector failure that prevents repository updates, treat this as an environmental issue rather than an engineering defect. Preserve the approved implementation and continue using an alternate implementation path, such as local repository application or a fresh execution session, rather than reopening engineering review solely because the platform write failed.

This preserves the distinction between engineering issues, which require ESR review and corrective validation, and tooling issues, which should be handled operationally without restarting the engineering lifecycle.

## 7. WP2 Status

ESR-0016 WP2 architecture alignment is recorded as a focused addendum pending any later controlled update to SAM-0001 itself.

Recommended next action: independent reviewer assessment of this WP2 note, followed by Programme Sponsor decision on whether a direct SAM-0001 version update is still required or whether this addendum is sufficient for ESR-0016 closure.
