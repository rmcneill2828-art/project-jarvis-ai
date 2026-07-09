# UAM-0001 - Guardian Experience Architecture v1.0

> *"Guardian is not where the interface points; Guardian is who the experience gathers around."*

**Version:** 1.2

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | UAM-0001 |
| Title | Guardian Experience Architecture v1.0 |
| Version | 1.2 |
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

---

# 8. Guardian Orb

The Guardian Orb is Guardian's visual presence, not decoration.

The Orb represents continuity, readiness and companion presence.

It shall not be treated as an ornamental background element or generic status icon.

## 8.1 Knowledge Graph Representation

Approved as design direction under [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] Section 15, retroactively incorporated here at ESR-0017 - see Subsequent Architectural Update above.

The Orb's long-term form is a live rendering of the repository's own engineering knowledge graph, not an abstract animation:

- Nodes represent real artefacts, capabilities, systems or agents.
- Connections represent real engineering relationships between them.
- Architectural clusters (for example AIEMS Governance, Engineering Sessions, Guardian Architecture, Execution Environment) illuminate as the systems they represent are accessed.
- Newly active agents appear as distinct nodes and connect into the graph as they come online, adopting their designated cluster colour as trust and identity are established.
- The Orb is driven by observed data, not by animation scripts - consistent with Section 8's presence principle, it shall visualise observable engineering or platform state rather than simulated intelligence.

This remains a design direction, not an implementation package. Per Section 18's Capability Evolution Model, it shall be built only through approved engineering packages, in phases tracked at [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0028.

## 8.2 Orb Status Semantics

The Orb's own animation may communicate Guardian's activity state, distinct from the general capability-state colour language in Section 14:

- Calm pulse - idle or observing.
- Gentle colour flow - learning or traversing knowledge.
- Bright traversal paths - active reasoning.
- Multiple concurrent traversal paths - multi-agent collaboration.
- Gold highlight - awaiting human approval.
- Green pulse - approved action complete.

These semantics apply only where the knowledge-graph Orb (8.1) is implemented. They do not retroactively apply to the current placeholder Orb animation, which remains governed only by Sections 13-15's general visual, colour and animation principles until superseded by an approved implementation package.

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
| 1.2 | 9 July 2026 | Claude Engineering Lead | Retroactively incorporated ESR-0010 Section 15's approved Guardian Orb design direction (originally discussed in FCH-0010, never merged into this artefact at the time): new Section 8.1 Knowledge Graph Representation (Orb as live rendering of the repository's engineering knowledge graph - nodes/connections/cluster illumination/agent-as-nodes) and Section 8.2 Orb Status Semantics (idle/learning/reasoning/awaiting-approval/approved colour states, distinct from Section 14's general capability colour language). Both remain design direction only, not implementation, per Section 18. Added ESR-0010 to OSE Relationships/Related Artefacts. Gap identified when the Programme Sponsor asked whether a final UXP look had already been discussed with ChatGPT. |
| 1.1 | 8 July 2026 | Claude Engineering Implementer | Added Subsequent Architectural Update note pointing to ADR-0018 and CURRENT_ARCHITECTURE.md, since ADR-0018 broadened Sentinel's role beyond the trust-posture-only framing described here. Approved Baseline status and original content unchanged. |
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved Guardian Experience Architecture v1.0 created under EIP-ESR0009-004. |