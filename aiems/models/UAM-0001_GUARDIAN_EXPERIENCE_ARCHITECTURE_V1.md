# UAM-0001 - Guardian Experience Architecture v1.0

> *"Guardian is not where the interface points; Guardian is who the experience gathers around."*

**Version:** 1.6

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | UAM-0001 |
| Title | Guardian Experience Architecture v1.0 |
| Version | 1.6 |
| Status | Approved Baseline |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] |
| Effective Date | 2 July 2026 |
| Review Frequency | At Guardian experience review or UXP implementation package selection |

---

# Subsequent Architectural Update

[[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] (approved 8 July 2026) broadened Sentinel's role beyond the "trust posture" representation described in this artefact's Sentinel Trust Posture Representation section, and beyond [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] as originally written. Sentinel is now the AI Execution and Security Platform, with implemented provider orchestration, execution governance and failover under `sentinel/`. [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] is the current authoritative architecture snapshot. This note does not change UAM-0001's Approved Baseline status or other content.

[[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] Section 15 ("Guardian UXP Design Outcome") approved a specific Guardian Orb design direction - the Orb as a live rendering of the repository's engineering knowledge graph, with cluster illumination, agent-traversal visualisation and Orb-specific status semantics - originating from a design conversation recorded in `aiems/History/Full Chat/FCH-0010_ESR-0010_FULL_CHAT_HISTORY.md`. This was never merged into UAM-0001 at the time it was approved. Retroactively incorporated at ESR-0017 (Sections 8.1 and 8.2 below) after the Programme Sponsor identified the gap. This note does not change UAM-0001's Approved Baseline status or other content.

On 2 October 2026 the Programme Sponsor directed a full Guardian experience redesign delivered as one Work Package (go-live decisions D9-D11, enacted at ESR-0061 WP1a): the incremental approach to Section 7.1's composition is retired, and the Guardian Orb is **decoupled from the knowledge graph**. The Orb becomes a state-driven presence; the repository knowledge graph remains as its own view, with no loss of functionality. Sections 7.1, 8.1 and 8.2 are amended accordingly. Reason: an Orb drawn from the development repository's own files fails on every installed machine (EBG-0148). The Version 1.0 Orb must meet the acceptance criteria in Section 8.2 (D3). UAM-0001's Approved Baseline status is unchanged.

---

# 2. Purpose

UAM-0001 defines Guardian Experience Architecture v1.0.

It establishes the stable user experience architecture for Guardian as the singular trusted digital companion experienced by the user.

UAM-0001 defines experience architecture, not React components or CSS implementation.

---

# 3. Scope

UAM-0001 covers:

- Guardian experience philosophy;
- canonical desktop layout principles;
- Guardian Orb architectural meaning;
- conversation-first interaction;
- capability awareness;
- diagnostics posture;
- Sentinel trust posture representation;
- visual, colour, animation, accessibility and responsive behaviour principles.

UAM-0001 does not implement runtime behaviour, UI components, stylesheets, provider calls or agent execution.

---

# 4. Experience Philosophy

The desktop experience exists to support the relationship between the user and Guardian.

Guardian is experienced as the singular trusted digital companion.

The interface shall make Guardian feel present, stable and trustworthy without implying that unavailable platform capabilities are implemented.

---

# 5. Guardian Experience Principle

Guardian is always central.

Guardian is not presented as one card among many capabilities.

Guardian provides the primary user-facing continuity across future platform evolution.

---

# 6. Stable Layout Principle

The layout is stable while capabilities evolve.

Capability surfaces may gain depth over time, but the core Guardian-centred structure should remain recognisable across implementation packages.

Stability supports trust, repeat use and future accessibility review.

---

# 7. Canonical Desktop Layout

The canonical desktop layout consists of:

1. Guardian presence area.
2. Conversation-first interaction space.
3. Platform and capability awareness surface.
4. Sentinel trust posture indication.
5. Diagnostics and implementation boundary surface.

Guardian presence shall remain visually and structurally primary.

## 7.1 Reference Dashboard Composition

A mock-up image ("JARVIS AI ORB - Obsidian Knowledge Graph Visualisation"), preserved at `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`, was provided by the Programme Sponsor at ESR-0017, recovering visual detail beyond the FCH-0010 text description incorporated in Section 8. It is treated here as an illustrative reference for how the five canonical layout elements above may be composed, not as a literal implementation specification - individual panels remain subject to normal engineering package approval and Section 18's Capability Evolution Model.

The reference composition surrounds the central Guardian Orb (7 above; detailed in Section 8) with:

- **System Health** - a status list of integrated systems (illustrated as AIEMS, GIA, Guardian, GitHub, Obsidian, ChatGPT, Codex), each with an individual state and rolled up to an overall status. An instance of the Platform and Capability Awareness surface (canonical element 3).
- **Knowledge Metrics** - a quantified readout of the knowledge graph itself: node count, connection count, cluster count, density, orphaned-node count, last-updated timestamp. Supports the Diagnostics and Implementation Boundary surface (canonical element 5) by making the graph's own health inspectable. **The reference mock-up's specific figures (6,842 nodes, 18,392 connections) are illustrative of an aspirational future scale, not the actual repository state** - confirmed by direct count at ESR-0017, ~135 markdown artefacts repository-wide, consistent with the Programme Sponsor's own current Obsidian graph. Implementation should render live figures for the repository's real current scale, not the mock-up's illustrated numbers.
- **Active Clusters** - the named engineering domains (illustrated as AIEMS Governance, Engineering Sessions, Guardian Architecture, GIA Telemetry, Standards & Playbooks, Execution Environment, Integration Layer) each with a live node count, corresponding to the cluster illumination described in Section 8.1.
- **Real-Time Activity** - a scrolling feed of actual engineering events (for example a session update, telemetry received, a graph sync, an agent recommendation, a repository check), timestamped. Distinct from Diagnostics (which shows structural/implementation state) - this shows recent observed activity.
- **AIEMS Principles** - a small panel surfacing governing principles (illustrated as Transparency, Evidence-Based, Human Authority, Continuous Improvement, Engineering Excellence) directly in the experience, reinforcing that Guardian's behaviour is governed rather than autonomous. Any principles shown here shall match, not diverge from, the authoritative principles recorded in PBK-0001 and `JARVIS_PRODUCT_ARCHITECTURE.md` - this panel visualises existing governance, it does not define new governance.
- **Persistent conversation bar** - beneath the Orb, per Section 9, supporting both text and voice input where Voice capability (per `JARVIS_PRODUCT_ARCHITECTURE.md`) is implemented; voice input affordance shall not be shown as available before it is.

This composition is an illustrative input to the Guardian experience redesign, delivered as one Work Package (Programme Sponsor decisions D9-D10, 2 October 2026), not approached incrementally. Each data-bearing panel still appears only when real implemented capability backs it, per Section 10 - never built ahead of the platform it represents. The System Health illustration's ChatGPT and Codex entries are illustrative only: neither is a Version 1.0 provider ([[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]]).

---

# 8. Guardian Orb

The Guardian Orb is Guardian's visual presence, not decoration.

The Orb represents continuity, readiness and companion presence.

It shall not be treated as an ornamental background element or generic status icon.

## 8.1 Knowledge Graph View (Decoupled from the Orb)

ESR-0010 Section 15 approved the repository's engineering knowledge graph as the Orb's long-term form (nodes for artefacts, capabilities, systems and agents; connections for real engineering relationships; clusters that illuminate as their systems are accessed). **On 2 October 2026 the Programme Sponsor decoupled the two (D11).** The Orb no longer renders the graph.

The knowledge graph remains a capability in its own right, presented as **its own view**, with the functionality it has today preserved. It is driven by observed repository data, not animation scripts, and is shown only where a repository is actually present. Where none is present it says so plainly rather than showing an error or placeholder data (Section 10). Further graph phases (originally phased under [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0028) remain design direction, built only through approved packages (Section 18).

## 8.2 Orb Status Semantics

The Orb is Guardian's state-driven presence. For Version 1.0 it shall meet these acceptance criteria (Programme Sponsor decision D3, 2 October 2026):

1. **Five real states** - idle, listening, thinking, speaking, and offline/error - each driven by an actual runtime event, never by a timer or script.
2. **A smooth frame rate** on the household PC and the Apple M1 Pro; the numeric target is set in the redesign Work Package's design.
3. **Reduced-motion support**, with the current state also shown as text.
4. **Works identically with no repository present.**
5. **Matches the look the Programme Sponsor approves** in the redesign prototype.

Further states (for example "awaiting human approval", per [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]) may be added by an approved package. The graph-specific semantics previously listed here (traversal paths, multi-agent paths) belong to the knowledge graph view (8.1), not the Orb. Section 14's colour language continues to apply.

## 8.3 Orb Status Panel (Textual Readout)

Recovered from the same reference mock-up as Section 7.1. Complementary to 8.2, not a replacement for it: 8.2 is the Orb's ambient/passive animation state; this is an explicit textual readout a user can read without interpreting animation. Illustrated fields:

- **Mode** - Guardian's current operating posture (for example Observe).
- **Confidence** - Guardian's stated confidence in its current assessment or recommendation.
- **Autonomy** - the level of independent action currently in effect (for example Advisory).
- **Permission** - whether an action is proceeding, blocked, or awaiting human approval.

This directly represents Human-in-the-Loop governance ([[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]) in the experience itself, and shall never show an autonomy or permission state more permissive than what is actually enforced by Guardian/Sentinel at that moment - this panel reports real governance state, it does not decorate around an assumed one.

---

# 9. Conversation-First Interaction

Conversation is the primary interaction model.

Future interaction modes may supplement conversation, but they shall not displace Guardian as the central trusted interface.

Conversation surfaces shall distinguish real implemented responses from placeholder or diagnostic text.

---

# 10. Capability Awareness

Capability awareness shall show the user what is available, placeholder, not implemented, offline or unknown.

Capability awareness exists to preserve trust.

It shall not imply that Guardian, Sentinel, memory, providers, agents, voice, vision, internet or automation are implemented unless separately authorised and verified.

---

# 11. Diagnostics Philosophy

Diagnostics should expose implementation boundaries clearly and calmly.

Diagnostics should help reviewers and future implementers understand what is available and what remains placeholder.

Diagnostics are not a substitute for Sentinel enforcement or platform policy.

---

# 12. Sentinel Trust Posture Representation

Sentinel is represented as trust posture, not as a competing companion or UI identity.

The experience may show Sentinel state, readiness or placeholder posture, but Sentinel is not personified as a second assistant.

Guardian remains the user-facing companion.

---

# 13. Visual Language

The visual language shall support calm focus, technical confidence and companion presence.

It should avoid implying operational maturity that the platform has not yet achieved.

Visual hierarchy shall reinforce Guardian centrality and clear capability boundaries.

---

# 14. Colour Language

Colour shall communicate state consistently.

Recommended semantic roles:

- available or ready;
- placeholder or preparing;
- not implemented;
- offline;
- unknown or diagnostic.

Colour shall not be the only means of communicating state.

---

# 15. Animation Principles

Animation shall support presence and state awareness.

Animation shall not distract from conversation or imply autonomous behaviour that has not been implemented.

The Guardian Orb may animate as a presence signal where implementation packages authorise it.

---

# 16. Accessibility Principles

The Guardian experience shall preserve:

- readable text contrast;
- keyboard-accessible interaction paths;
- clear focus order;
- non-colour state indicators;
- responsive text and layout behaviour.

Accessibility shall be considered part of trust, not a cosmetic enhancement.

---

# 17. Responsive Behaviour

The experience shall remain usable across supported desktop window sizes.

Guardian shall remain central on narrow and wide layouts.

Capability and diagnostics surfaces may reflow, but they shall not obscure conversation or Guardian presence.

---

# 18. Capability Evolution Model

Capability evolution shall proceed from placeholder to implemented only through approved engineering packages and validation evidence.

Future capabilities extend Guardian's usefulness without creating separate AI identities.

The experience shall continue to distinguish implemented behaviour from future architectural intent.

---

# 19. Explicit Non-Goals

UAM-0001 does not:

- define React components;
- define CSS implementation;
- implement Guardian runtime behaviour;
- implement Sentinel enforcement;
- implement providers, memory, agents, voice, vision, internet or automation;
- create a new user-facing AI identity;
- modify the Guardian Desktop Platform Shell.

---

# 20. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Parent Guardian identity and cognitive architecture authority. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel trust architecture represented as trust posture in the Guardian experience. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture authority above Sentinel and Guardian experience architecture. |
| [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Architecture decision defining Guardian identity and HITL governance context. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Engineering ecosystem and OSE context for controlled architecture navigation. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline context. |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] | Source of the Guardian Orb knowledge-graph design direction incorporated into Sections 8.1 and 8.2. |

---

# 21. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture context for Guardian desktop experience. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability readiness context for Guardian experience evolution. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Engineering session context for Guardian, Sentinel and UXP architecture outcomes. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers UAM-0001 as a controlled architecture model. |

---

# 22. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.6 | 6 October 2026 | Claude Engineering Implementer | ESR-0061 WP1a per EIP-ESR0061-001: Guardian Orb decoupled from the knowledge graph (D11); graph kept as its own view (8.1); Orb Version 1.0 acceptance criteria (8.2, D3); 7.1 incremental approach retired (D9-D10). |
| 1.5 | 9 July 2026 | Claude Engineering Lead | Corrected Section 7.1 Knowledge Metrics: the reference mock-up's specific node/connection figures (6,842/18,392) are illustrative of an aspirational future scale, not the actual repository state - confirmed by direct count (~135 markdown artefacts) and the Programme Sponsor's own current Obsidian graph screenshot at ESR-0017. Implementation should target real current scale, not the mock-up's illustrated numbers. |
| 1.4 | 9 July 2026 | Claude Engineering Lead | Referenced the now-persisted mock-up image at aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg from Section 7.1, replacing the earlier description-only reference. |
| 1.3 | 9 July 2026 | Claude Engineering Lead | Incorporated the actual Guardian Orb mock-up image provided by the Programme Sponsor at ESR-0017 (richer than the FCH-0010 text description already in 8.1/8.2): new Section 7.1 Reference Dashboard Composition (System Health, Knowledge Metrics, Active Clusters, Real-Time Activity, AIEMS Principles panel, persistent conversation bar with voice affordance) and Section 8.3 Orb Status Panel (Mode/Confidence/Autonomy/Permission textual readout, distinct from 8.2's ambient animation semantics, tied explicitly to ADR-0010 HITL governance). Both explicitly illustrative/design-direction only, not implementation, per Section 18. |
| 1.2 | 9 July 2026 | Claude Engineering Lead | Retroactively incorporated ESR-0010 Section 15's approved Guardian Orb design direction (originally discussed in FCH-0010, never merged into this artefact at the time): new Section 8.1 Knowledge Graph Representation (Orb as live rendering of the repository's engineering knowledge graph - nodes/connections/cluster illumination/agent-as-nodes) and Section 8.2 Orb Status Semantics (idle/learning/reasoning/awaiting-approval/approved colour states, distinct from Section 14's general capability colour language). Both remain design direction only, not implementation, per Section 18. Added ESR-0010 to OSE Relationships/Related Artefacts. Gap identified when the Programme Sponsor asked whether a final UXP look had already been discussed with ChatGPT. |
| 1.1 | 8 July 2026 | Claude Engineering Implementer | Added Subsequent Architectural Update note pointing to ADR-0018 and CURRENT_ARCHITECTURE.md, since ADR-0018 broadened Sentinel's role beyond the trust-posture-only framing described here. Approved Baseline status and original content unchanged. |
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved Guardian Experience Architecture v1.0 created under EIP-ESR0009-004. |