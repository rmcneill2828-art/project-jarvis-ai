# AAM-0001 - Guardian Identity and Cognitive Architecture

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | AAM-0001 |
| Title | Guardian Identity and Cognitive Architecture |
| Version | 0.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Created During | ESR-0008 |
| Review Frequency | Triggered |

---

# Subsequent Architectural Update

[[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] (approved 8 July 2026) broadened Sentinel's role beyond the "trust gateway protecting platform entry" framing described in this artefact's Sentinel references (Purpose, Domain Interpretation table, Sentinel Relationship section). Sentinel is now the AI Execution and Security Platform, with implemented provider orchestration, execution governance and failover under `sentinel/`. [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] is the current authoritative architecture snapshot for Sentinel's scope. This note does not change AAM-0001's other architectural content.

---

# Purpose

AAM-0001 defines the canonical identity and cognitive architecture for Project JARVIS AI, the JARVIS Platform, Guardian, Sentinel, Platform Services and the Agent Framework.

It records the ESR-0008 architectural distinction between the runtime platform and the trusted digital companion hosted by that platform.

---

# Scope

This artefact covers:

- Project JARVIS AI as the engineering programme.
- JARVIS Platform as the runtime operating platform.
- Guardian as the trusted digital companion / AI entity.
- Sentinel as the trust gateway protecting platform entry.
- Platform Services as governed runtime services behind Sentinel.
- Agent Framework as specialist capability agents serving Guardian.
- Guardian faculties: memory, vision, voice, reasoning, action, trust and judgement.

This artefact does not implement runtime functionality, select service providers or replace [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].

---

# Engineering Authority

AAM-0001 is created under ESR-0008 Programme Sponsor authority. It shall be interpreted with repository-first engineering precedence:

1. GitHub repository.
2. Controlled artefacts.
3. OSE relationships.
4. Engineering Session Reports.
5. Engineering summaries.
6. Full historical chats.
7. Current engineering session.

---

# Evidence Sources

- [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].
- [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]].
- [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]].
- [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

## Canonical Identity Model

| Concept | Definition |
|---------|------------|
| Project JARVIS AI | The engineering programme containing AIEMS and JARVIS product engineering. |
| JARVIS Platform | The runtime operating platform that hosts Guardian and platform capabilities. |
| Guardian | The trusted digital companion / AI entity experienced by users. |
| Sentinel | The trust gateway that protects platform entry and asks whether an input can be trusted. |
| Platform Services | Bootstrap, configuration, registry, health, restore, capability and sync services behind Sentinel. |
| Agent Framework | Specialist capability agents serving Guardian without becoming separate user-facing identities. |

## Cognitive Architecture

Guardian is the singular user-facing AI entity. Guardian perceives, reasons, remembers, judges and acts through governed platform capabilities.

```text
User / Device / External Event
  |
  v
Sentinel
  |
  v
Platform Services
  |
  v
Guardian
  |
  +-- Memory
  +-- Voice
  +-- Vision
  +-- Reasoning
  +-- Trust
  +-- Judgement
  +-- Action
  |
  v
Agent Framework
```

## Guardian Faculties

| Faculty | Architectural Role |
|---------|--------------------|
| Memory | Preserves personal, family, session and governed knowledge within consent and retention boundaries. |
| Voice | Provides ears and speech channel; it does not bypass Sentinel or Guardian. |
| Vision | Provides visual perception governed by Sentinel and Guardian. |
| Reasoning | Interprets requests, options, context and planned responses. |
| Trust | Consumes Sentinel trust outcomes and provider trust evidence. |
| Judgement | Determines whether an action should happen under policy, consent, privacy and human approval rules. |
| Action | Requests authorised execution through automation, agents or platform services. |

## Sentinel Relationship

Sentinel applies the Gate of Durin Pattern before Platform Services. Everything entering JARVIS passes through Sentinel. Sentinel asks: Can this be trusted?

## Guardian Relationship

Guardian governs consent, policy, privacy, approval, memory retention and human-in-the-loop decisions. Guardian asks: Should this happen?

## Agent Relationship

Specialist agents provide domain capability to Guardian. They are not separate AI identities. Guardian asks agents how to accomplish specialist tasks and remains the user-facing entity.

## Obsidian and OSE Relationship

Obsidian is the human-facing Engineering Knowledge Workspace for OSE. It sits in the Engineering Ecosystem, not inside the JARVIS runtime platform. GitHub remains the source of truth; Obsidian visualises and navigates repository Markdown and OSE relationships.

---

# OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Provides platform architecture context for this cognitive model. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Provides product vision and user-facing behaviour context. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traces this model into ESR-0008 product vision recovery. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Records ESR-0008 closure outcomes that created this model. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Records the Guardian identity and human-in-the-loop governance decision. |
| [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Records the Sentinel trust gateway decision. |
| [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | Records the specialist agent framework decision. |
| [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] | Records device independence and restore decision affecting Guardian portability. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 8 July 2026 | Claude Engineering Implementer | Added Subsequent Architectural Update note pointing to ADR-0018 and CURRENT_ARCHITECTURE.md, since ADR-0018 broadened Sentinel's role beyond the trust-gateway-only framing described here. Original content unchanged. |
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial draft created during ESR-0008 closure to record Guardian identity and cognitive architecture. |
