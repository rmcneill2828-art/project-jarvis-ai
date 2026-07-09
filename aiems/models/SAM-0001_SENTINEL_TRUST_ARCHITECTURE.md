# SAM-0001 - Sentinel Trust Architecture

> *"Trust is an architecture, not an afterthought."*

**Version:** 0.2

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | SAM-0001 |
| Title | Sentinel Trust Architecture |
| Version | 0.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] |
| Effective Date | 2 July 2026 |
| Review Frequency | At architecture review or Sentinel implementation package selection |

---

# Subsequent Architectural Update

[[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] (approved 8 July 2026) repositioned Sentinel as the AI Execution and Security Platform for AIEMS, broadening the trust-gateway-only framing this artefact describes. Sentinel Core, provider abstraction, provider configuration, provider orchestration and the Sentinel trust-tier policy model are now implemented under `sentinel/`. [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] is the current authoritative architecture snapshot for Sentinel's scope. This note does not change SAM-0001's original content, decision or approval basis.

---

# 2. Purpose

SAM-0001 defines the controlled Sentinel Trust Architecture for the JARVIS Platform.

It establishes Sentinel as the platform trust, governance, protection and policy layer that governs the environment in which Guardian operates.

This artefact provides architectural authority only. It does not implement Sentinel enforcement, policy execution or runtime protection behaviour.

---

# 3. Scope

SAM-0001 covers:

- Sentinel architectural position within the JARVIS Platform;
- Sentinel trust boundary responsibilities;
- governance and policy posture;
- human-in-the-loop approval role;
- relationship to Guardian, Platform Services, agents, providers and memory;
- explicit non-goals for current and future implementation packages.

SAM-0001 does not define React components, Tauri behaviour, Python implementation details or executable policy logic.

---

# 4. Architectural Position

Sentinel sits below [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] and above Guardian.

Within the approved architecture hierarchy:

```text
MOD-0001
  |
  v
SAM-0001
  |
  v
AAM-0001
  |
  v
UAM-0001
  |
  v
Engineering Execution Packages
```

Sentinel is not a user-facing companion.

Sentinel is not a separate AI personality.

Sentinel governs the environment in which Guardian operates.

---

# 5. Sentinel Responsibilities

Sentinel is responsible for the architectural trust posture of the JARVIS Platform.

Sentinel responsibilities include:

- defining trust boundaries before Platform Services are used;
- positioning policy and governance controls before capability execution;
- preserving separation between companion experience and trust enforcement;
- supporting future approval, audit and protection behaviour;
- preventing future services from being treated as unconstrained execution surfaces.

Sentinel does not replace Guardian and does not become a competing user-facing identity.

---

# 6. Trust Boundary Model

Sentinel defines the boundary between user-facing Guardian interaction and platform service execution.

Conceptually:

```text
User
  |
  v
Guardian Experience
  |
  v
Sentinel Trust Boundary
  |
  v
Platform Services
  |
  v
Agents, Providers, Memory and Tools
```

Guardian does not bypass Sentinel.

Platform Services operate inside Sentinel-governed boundaries.

Sentinel enforcement is not implemented by this artefact.

---

# 7. Governance and Policy Role

Sentinel is the architectural home for future policy interpretation, governance checks and trust posture evaluation.

The governance role includes:

- applying Programme Sponsor-approved policy boundaries;
- supporting future capability gating;
- providing a future location for trust diagnostics;
- preserving a single governed route from Guardian to platform execution.

Policy engines are not implemented by SAM-0001.

---

# 8. Human-in-the-Loop Approval Role

Sentinel provides the architectural position for future human-in-the-loop approval before sensitive or consequential platform actions.

The approval role is architectural only in this artefact.

SAM-0001 does not implement approval workflows, approval storage, notification logic or enforcement decisions.

---

# 9. Relationship to Guardian

Guardian remains the singular trusted companion experienced by the user.

Sentinel governs the environment in which Guardian operates, but Sentinel is not experienced as a second companion, agent or personality.

Guardian may represent Sentinel trust posture to the user where appropriate, but Guardian does not bypass Sentinel.

---

# 10. Relationship to Platform Services

Platform Services are future executable service boundaries that operate under Sentinel-governed conditions.

Sentinel sits before Platform Services in the trust path.

SAM-0001 does not implement Platform Services and does not authorise any service execution behaviour.

---

# 11. Relationship to Agents, Providers and Memory

Agents, providers and memory are future platform capabilities that shall operate inside Sentinel-governed boundaries.

Sentinel does not implement agents.

Sentinel does not connect providers.

Sentinel does not persist memory.

Sentinel establishes the future trust posture that those capabilities must respect when separately authorised.

---

# 12. Explicit Non-Goals

SAM-0001 does not:

- implement Sentinel enforcement;
- implement Guardian runtime behaviour;
- implement approval workflows;
- implement a policy engine;
- create a new AI identity;
- modify the Guardian Desktop Platform Shell;
- implement providers, memory, agents, voice, vision, internet or automation;
- create product source code.

---

# 13. Future Evolution

Future implementation packages may use SAM-0001 to guide Sentinel capability development.

Future evolution may include:

- policy evaluation;
- trust posture diagnostics;
- approval workflow design;
- capability gating;
- audit and traceability boundaries.

Any such evolution shall require separately approved engineering packages.

---

# 14. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Parent platform architecture authority. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity architecture governed beneath the Sentinel trust layer. |
| [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Architecture decision establishing the Sentinel Gate of Durin pattern. |
| [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Architecture decision linking Guardian identity and HITL governance. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Engineering ecosystem and OSE context for controlled architecture navigation. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline context. |

---

# 15. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian experience architecture that represents Sentinel as trust posture. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture context for Sentinel and Guardian platform evolution. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability readiness context for Sentinel-related future work. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Engineering session context for Sentinel, Guardian and platform architecture outcomes. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers SAM-0001 as a controlled architecture model. |

---

# 16. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 8 July 2026 | Claude Engineering Implementer | Added Subsequent Architectural Update note pointing to ADR-0018 and CURRENT_ARCHITECTURE.md, since ADR-0018 broadened Sentinel's role beyond the trust-gateway-only framing described here. Original content unchanged. |
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial Sentinel Trust Architecture created under EIP-ESR0009-004. |
