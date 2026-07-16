# GAM-0001 - Guardian Authority and Boundary Model

> *"Guardian's trust comes from what it will not do without being asked."*

**Version:** 1.2

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | GAM-0001 |
| Title | Guardian Authority and Boundary Model |
| Version | 1.2 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] |
| Effective Date | 16 July 2026 |
| Review Frequency | At architecture review or Guardian implementation package selection |

---

# 2. Purpose

GAM-0001 defines Guardian's safety, permission, approval and protection boundaries: what Guardian may act on autonomously, what requires human approval, and what remains explicitly out of scope until separately authorised.

It resolves [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0031 (Guardian Architecture Specification, open since ESR-0005), and provides the policy content that the Sentinel trust-tier mechanism implemented at ESR-0016 was explicitly left with extension points to receive (`aiems/architecture/CURRENT_ARCHITECTURE.md`: "The trust-tier model provides extension points for EBG-0047 and future boundary work under EBG-0020 and EBG-0021").

This artefact provides architectural authority only. It does not implement enforcement, policy execution or runtime protection behaviour.

---

# 3. Scope

GAM-0001 covers:

- the boundary between Guardian actions that require no human approval and those that do;
- how Guardian-level authority concerns map onto Sentinel's already-implemented trust-tier model;
- general protection principles governing Guardian's judgement;
- the general shape of the approval/escalation path;
- explicit non-goals for current and future implementation packages.

GAM-0001 does not cover:

- Guardian identity or cognitive faculties - defined in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]];
- Sentinel's trust-boundary architecture or execution mechanics - defined in [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] and implemented under `sentinel/` per `CURRENT_ARCHITECTURE.md`;
- consent, privacy, memory-retention and trusted-mobile approve/deny mechanics - reserved for EBG-0048, referenced here, not restated;
- Sentinel Gate of Durin trust-tier/platform-entry implementation detail - reserved for EBG-0047;
- React components, Tauri behaviour, Python implementation details or executable policy logic.

---

# 4. Architectural Position

GAM-0001 sits beneath Sentinel's trust-boundary architecture and beside Guardian's identity architecture - it governs what the identified, trusted Guardian is authorised to do, not who Guardian is or how input reaches Guardian.

```text
MOD-0001
  |
  v
SAM-0001  (Sentinel: can this be trusted?)
  |
  v
AAM-0001  (Guardian: who is acting?)
  |
  v
GAM-0001  (Guardian: is this action authorised?)
  |
  v
UAM-0001  (how is this experienced by the user?)
  |
  v
Engineering Implementation Packages
```

GAM-0001 does not redefine Sentinel's trust boundary or Guardian's identity. It defines the authority Guardian exercises once both have already been established for a given interaction.

---

# 5. Relationship to Sentinel's Trust-Tier Model

Sentinel's trust-tier policy model, implemented at ESR-0016 WP1, already provides the enforcement mechanism this artefact's policy content is designed to be classified against:

| Sentinel Element | Already Implemented |
|---|---|
| Trust tiers | `ROUTINE`, `SENSITIVE`, `RESTRICTED` |
| Classification categories | `ROUTINE_INTERACTION`, `HUMAN_APPROVAL_REQUIRED`, `UNSUPPORTED_HIGH_RISK`, `EMERGENCY_CONTROL`, `LOCAL_AGENT_ACTION` |
| Decision outcomes | `ALLOW` (routine interaction), `REVIEW` (human approval), `DENY` (unsupported high-risk, emergency-control, local-agent-action) |
| Classification precedence | Conservative: unsupported high risk, then emergency control, then local-agent action, then human approval, then routine interaction |
| Softening rule | Deny-category requests cannot be softened to `REVIEW` by also setting human approval |

GAM-0001 does not alter this mechanism. It defines, at a policy level, what kinds of Guardian action belong in each category - the content Sentinel's classifier needs in order to route a given Guardian action correctly, per Section 6.

---

# 6. Permission Boundary Model

Guardian action falls into one of three general authority levels. This section defines the level; it does not define the enforcement code that reads it.

## 6.1 Autonomous (maps to `ROUTINE_INTERACTION` / `ALLOW`)

Conversational, informational and read-only actions that carry no risk of altering system state, family safety or irreversible outcomes: answering questions, holding conversation, presenting already-governed status/diagnostic information the user is entitled to see (for example the System Health panel's real `platform.status` fields).

## 6.2 Approval-Required (maps to `HUMAN_APPROVAL_REQUIRED` / `REVIEW`)

Any Guardian action that changes state, commits resources, or acts on the user's behalf outside pure conversation - falls here by default unless explicitly reclassified as autonomous through a separately approved engineering package. The default is approval-required, not autonomous: Guardian gains autonomous authority only where a specific action has been explicitly reviewed and placed in Section 6.1, mirroring Sentinel's own conservative classification precedence (Section 5).

## 6.3 Out of Scope (maps to `UNSUPPORTED_HIGH_RISK` / `EMERGENCY_CONTROL` / `LOCAL_AGENT_ACTION` / `DENY`)

Categories that are not merely approval-gated but currently unsupported entirely, regardless of approval: local-agent action (EBG-0021 not yet defined), emergency control execution (narrow exception defined in Section 8.4), automation, and any high-risk action with no current governance basis. These `DENY` outright under Sentinel's existing precedence rules - GAM-0001 does not open local-agent action; it records that it remains closed until EBG-0021 defines the boundary under which it could ever move to Section 6.2. Emergency control remains closed by the same default except for the one narrow, explicit mechanism Section 8.4 defines.

---

# 7. Protection Boundaries - General Principles

These are the principles Guardian's judgement shall follow. Concrete family-safety and emergency-control content is defined in Section 8.

- **Deny-by-default for the unclassified.** An action with no existing classification is treated as Section 6.3 (out of scope), never assumed autonomous. This matches Sentinel's existing conservative precedence rather than introducing a second, competing default.
- **No silent capability expansion.** Guardian's autonomous authority (Section 6.1) may only grow through a separately approved engineering package that explicitly reclassifies a named action - never through inference, configuration, or accumulated precedent.
- **Human authority remains explicit for high-risk decisions**, per [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]'s existing decision - GAM-0001 operationalises that decision's boundary, it does not revisit it.
- **Family safety and child protection are a distinct, higher-scrutiny concern**, not a subset of general approval-gating - defined in full in Section 8.

---

# 8. Family Safety and Emergency Controls

Resolves [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0020 (Guardian, Family Safety and Emergency Controls, open since ESR-0004's EKR-0001 vision recovery). This section extends Section 7's protection principles with the concrete content originally left deferred there.

## 8.1 Household Role Model

Sourced from the original ESR-0004 EKR-0001 vision-recovery findings (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`), never previously captured in any controlled artefact - confirmed absent from both AAM-0001 and PVTM-0001 before this section:

| Role | Authority |
|---|---|
| Administrator | Full household authority; the only role that may author or amend a pre-approved emergency action policy (Section 8.4). |
| Adult | Standard household authority; may approve `REVIEW`-classified actions within Section 6.2, subject to any Administrator-set limits. |
| Child | Restricted authority; interacts within Section 8.2's child-safe assistance boundary; cannot approve `REVIEW`-classified actions. |
| Guest | Minimal authority; Autonomous-tier interaction only (Section 6.1); no access to family-shared memory or approval capability. |

This role model governs who may direct or approve a Guardian action. It does not alter Guardian's own authority levels (Section 6) - a Child-role request is still classified the same way by Sentinel; the role model determines who may satisfy a `REVIEW` escalation, not whether one is required.

## 8.2 Child-Safe Assistance Boundary

- Guardian shall distinguish personal memory (private to the individual) from shared family memory, per the original family-first model - detailed memory-retention mechanics remain EBG-0048's scope; this section states that the boundary exists, not how it is implemented.
- Content and interaction presented to a Child-role user is a distinct, higher-scrutiny concern from general Approval-Required gating (Section 6.2) - restriction is evaluated against the Child role itself, not inferred from action type alone.
- A Child-role user cannot satisfy a `REVIEW` escalation (Section 8.1) - only Adult or Administrator roles can.

## 8.3 Emergency Assistance Scope

Guardian's emergency-assistance scope, per the original vision recovery, is bounded to: emergency assistance requests, approved camera access, security monitoring, incident logging, and emergency policies. It explicitly excludes destructive action - the original vision recovery's own words: cyber-security capability "recommends, detects and monitors but does not perform destructive actions without approval," a direct instance of Section 7's "no silent capability expansion" principle.

## 8.4 Pre-Approved Emergency Actions

EBR-0001's EBG-0020 text specifically asks for "pre-approved emergency action boundaries" - a distinct concept from Section 6.1's Autonomous tier. A pre-approved emergency action is:

- explicitly authored and signed off by an Administrator-role user, in advance, as a named policy record - never inferred, defaulted, or granted by an AI judgement call at the moment of the emergency;
- narrowly scoped to a specific, named action (for example, "notify a specified contact if smoke-alarm telemetry is detected") - not a general emergency override;
- still routed through Sentinel's `EMERGENCY_CONTROL` classification and logged - pre-approval changes who authorised the action and when, not whether Sentinel sees and records it.

Absent such an explicit, named, Administrator-authored policy, all emergency-control actions remain `DENY` under Section 6.3. This section does not soften Sentinel's existing deny-by-default for `EMERGENCY_CONTROL` - it defines the one narrow, explicit mechanism by which a specific action could ever be pre-authorised. The policy record itself is subject to the same [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] Approval Before Change discipline as any other controlled change - an Administrator authoring a pre-approved emergency action does not bypass Section 7's "no silent capability expansion" principle merely by using this mechanism.

## 8.5 Relationship to EBG-0021 (Local Agent Permission Boundary)

Camera access, security monitoring and incident logging in Section 8.3 are observation/monitoring capabilities, not device or local-agent control. They do not open Section 6.3's `LOCAL_AGENT_ACTION` category, which remains closed pending EBG-0021's own separate definition.

---

# 9. Approval and Escalation Path - General Shape

Resolves [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0048 (Guardian HITL Governance Specification), extending EBG-0031/EBG-0020's boundaries with consent, memory-retention-consent, and trusted-mobile approve/deny mechanics, per [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]'s decision that Guardian "governs consent, policy, privacy, approval, memory retention and human-in-the-loop decisions."

```text
Guardian proposes an action
  |
  v
Sentinel classifies (Section 5 categories)
  |
  +-- ROUTINE_INTERACTION --> ALLOW --> Guardian proceeds
  |
  +-- HUMAN_APPROVAL_REQUIRED --> REVIEW --> escalate to human approval (Sections 9.1/9.3)
  |
  +-- UNSUPPORTED_HIGH_RISK / EMERGENCY_CONTROL / LOCAL_AGENT_ACTION --> DENY --> Guardian does not proceed
```

Evidence check: Sentinel's `REVIEW` outcome (`sentinel/policy.py`) is currently an enum value carrying a static message only ("Sentinel routed the request for review") - no approval workflow, notification channel, or consent-recording mechanism exists in code today. The sections below define the architecture that content would implement; none of it is implemented by this artefact.

## 9.1 Consent Mechanics

Before an `HUMAN_APPROVAL_REQUIRED`-classified action proceeds, Guardian shall obtain and record an explicit consent decision from a household member entitled to give it (Section 8.1 - Adult or Administrator; Child role cannot satisfy this per Section 8.2). Consent is scoped to the specific action proposed - it is not a standing grant, and does not itself reclassify the action's Section 6 authority level for future occurrences. This mirrors Section 7's "no silent capability expansion" principle: one consented instance does not become an autonomous pattern.

## 9.2 Memory-Retention Consent Boundary

GAM-0001 governs *whether Guardian may retain something and who consented to that retention* - not the underlying storage technology, encryption, technical retention duration, or data architecture, which remains [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0019's scope (Memory and Data Storage Architecture, still open). The boundary: a memory-retention request is itself a Guardian action subject to Section 6's classification and Section 9.1's consent mechanics like any other - it requires the same explicit, scoped consent, and Section 8.2's personal/shared-family distinction determines who that consent must come from. EBG-0019, when actioned, implements the storage architecture this consent gate sits in front of; it does not need to re-derive the consent requirement, which is defined here.

## 9.3 Trusted Mobile Approve/Deny

Confirmed by ADR-0010 as a future Guardian capability, not a current one - this section records the architectural shape only, not an implementation.

- A trusted mobile endpoint is a remote approval channel, not a separate authority source: it can only exercise the approval authority Section 8.1 already grants a given household role (Adult/Administrator), never more.
- Remote approval is subject to the same Section 9.1 consent-scoping - a remote approve/deny decision is scoped to the specific escalated action, not a standing remote-approval grant.
- Endpoint trust (device registration, authentication) is Sentinel's concern (per Section 5's trust-boundary model), not redefined here - this section governs what a trusted endpoint may authorise once Sentinel has established it is trusted, not how that trust is established.

## 9.4 Privacy Boundary Reinforcement

Section 8.2 states Guardian shall distinguish personal memory from shared family memory. This section makes the consent linkage explicit: crossing that boundary - for example, surfacing an individual's personal memory in a shared-family context - is itself an `HUMAN_APPROVAL_REQUIRED` action under Section 6.2, subject to Section 9.1's consent mechanics, not a default behaviour Guardian may perform on inference alone.

---

# 10. Explicit Non-Goals

GAM-0001 does not:

- implement Sentinel enforcement or the trust-tier classifier itself;
- implement Guardian runtime behaviour;
- implement approval workflows, notification channels, consent recording, or trusted-mobile approve/deny (Section 9 defines the architecture; none of it is built here);
- implement the household role model's authentication or enforcement (Section 8.1 defines the roles and their authority; it does not implement login, identification or access control);
- implement memory storage technology, encryption, or technical retention duration policy (EBG-0019 - Section 9.2 defines only the consent gate in front of that architecture);
- implement Sentinel endpoint trust/device registration (Section 9.3 assumes Sentinel has already established endpoint trust; it does not define how);
- define Sentinel Gate of Durin trust-tier/platform-entry detail (EBG-0047);
- create a new AI identity or modify Guardian identity as defined in AAM-0001;
- create product source code.

---

# 11. Future Evolution

Future implementation packages may use GAM-0001 to guide Guardian authority and boundary development. Anticipated follow-on work, already sequenced in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]:

- EBG-0021 - Local Agent Permission Boundary (defines the boundary Section 6.3 and Section 8.5 currently leave closed, once a local agent implementation is planned);
- EBG-0019 - Memory and Data Storage Architecture (implements the storage technology sitting behind Section 9.2's consent gate, once actioned).

Any such evolution shall require separately approved engineering packages.

---

# 12. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture authority this model operates beneath. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel trust-boundary architecture; parent artefact - GAM-0001 governs authority within the boundary Sentinel establishes. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and Judgement faculty this model operationalises into concrete authority boundaries. |
| [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Decision that Guardian is the HITL governance point; GAM-0001 defines the boundary that decision governs. |
| [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] | Decision establishing Sentinel's implemented trust-tier policy model, which GAM-0001's policy content is classified against. |
| [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] | Authoritative snapshot of the implemented Sentinel trust-tier mechanism referenced throughout Sections 5-6 and 8. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Current accepted repository baseline. |

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0031, EBG-0020 and EBG-0048 (resolved by this artefact), EBG-0021, EBG-0047, EBG-0019 (sequenced follow-on work referenced in Section 11). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B sequencing for EBG-0031/EBG-0020/EBG-0048 and their dependent follow-on items. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian experience architecture that presents Guardian's authority boundary to the user where appropriate. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers GAM-0001 as a controlled architecture model. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 16 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 16 July 2026**, following Engineering Reviewer (Codex) confirmation: Section 9.2's EBG-0019 boundary is drawn in the right place (policy/consent layer only, no pre-emption, no gap - storage technology, encryption and retention duration remain EBG-0019's scope); Section 9.3's endpoint-trust framing is consistent with SAM-0001 and ADR-0010. ESR-0023 WP4, resolving EBG-0048 (Guardian HITL Governance Specification, extending EBG-0031/EBG-0020 per ADR-0010). Section 9 extended with four subsections: 9.1 consent mechanics (scoped to the specific action, not a standing grant); 9.2 memory-retention consent boundary; 9.3 trusted mobile approve/deny, confirmed by ADR-0010 as a future capability, architecture only; 9.4 privacy boundary reinforcement, making Section 8.2's personal/shared-family distinction an explicit HUMAN_APPROVAL_REQUIRED gate. Evidence checked directly: `sentinel/policy.py`'s REVIEW outcome is currently a static-message enum value only, no approval workflow implemented. |
| 1.1 | 16 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 16 July 2026**, following Engineering Reviewer (Codex) confirmation: Section 8.4's pre-approval mechanism does not create a backdoor around Sentinel's EMERGENCY_CONTROL deny-by-default, and the Child-role restrictions (8.1/8.2) are adequately conservative. Non-blocking Reviewer note incorporated: Section 8.4 now states the emergency policy record itself is subject to PBK-0001's Approval Before Change discipline, not a bypass of it. New Section 8 resolves EBG-0020 (Guardian, Family Safety and Emergency Controls, open since ESR-0004): household role model (Administrator/Adult/Child/Guest, sourced from the original ESR-0004 EKR-0001 vision recovery, confirmed absent from AAM-0001 and PVTM-0001 before this addition), child-safe assistance boundary, emergency assistance scope, and an explicit boundary against EBG-0021. Sections renumbered 8 to 13 accordingly. ESR-0023 WP3. |
| 1.0 | 16 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 16 July 2026**, following Engineering Reviewer (Codex) confirmation of the authority-level split (Section 6) and protection principles (Section 7), and confirmation that the EBG-0020/EBG-0048/EBG-0021 deferrals do not pre-empt those items' own future scope. Status Draft to Approved; version 0.1 to 1.0 marking baseline acceptance. Resolving EBG-0031 in EBR-0001 as the same action. ESR-0023 WP2. |
| 0.1 | 16 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0023 WP2, resolving EBG-0031. Defines Guardian's permission boundary model (autonomous / approval-required / out-of-scope) mapped onto Sentinel's existing trust-tier classification categories, general protection principles, and the general shape of the approval/escalation path - with family-safety specifics (EBG-0020), HITL/consent mechanics (EBG-0048) and local-agent boundary detail (EBG-0021) explicitly deferred rather than restated. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
