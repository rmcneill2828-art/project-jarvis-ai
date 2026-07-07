# ADR-0018 - Sentinel AI Execution and Security Platform

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0018 |
| Title | Sentinel AI Execution and Security Platform |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor and Chief Engineering Advisor |
| Date Approved | 8 July 2026 |
| Review Trigger | Significant Sentinel architecture or execution governance change |

---

# Purpose

Record the ESR-0014 decision to designate Sentinel as the AI Execution and Security Platform for AIEMS.

This decision expands the earlier trust-gateway interpretation of Sentinel while preserving the approved Guardian and Sentinel separation.

---

# Scope

This ADR covers Sentinel's architectural positioning within AIEMS and Project JARVIS AI.

It records Sentinel as the platform layer responsible for trusted execution, AI orchestration, policy enforcement, resilience and operational governance.

This ADR does not implement additional runtime security, identity, audit, telemetry or compliance capabilities. Those remain future Sentinel workstreams.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0014 closure.

GitHub and the repository remain the authoritative source of truth for the approved architecture and implementation state.

---

# Evidence Sources

- ESR-0014 implementation work.
- Sentinel Core implementation.
- Provider abstraction implementation.
- Provider configuration implementation.
- Provider orchestrator implementation.
- PEM-001 AI Provider Evaluation Matrix.
- Final ESR-0014 validation: 100 / 100 tests passing.

---

# 1. Problem Statement

Sentinel was initially positioned primarily as a trust gateway. During ESR-0014 implementation, Sentinel evolved beyond that role by gaining provider abstraction, configuration, orchestration, health monitoring, routing, failover and execution history capabilities.

The architecture required an updated designation that reflected Sentinel's implemented and intended responsibilities while preserving Guardian as the cognition engine.

---

# 2. Background

ESR-0014 implemented Sentinel as a standalone top-level package and established it as Guardian's execution boundary.

The implementation demonstrated that Sentinel is not merely a gate before execution. It is the platform layer that determines whether, where, when and how execution occurs.

The same execution governance model also provides a future home for policy, identity, audit, telemetry, compliance and trusted runtime controls.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Keep Sentinel as Trust Gateway only | Too narrow for the implemented provider orchestration, resilience and future platform role. |
| Treat AI orchestration as separate from Sentinel | Would fragment execution governance and risk duplicating policy, health, audit and resilience controls. |
| Designate Sentinel as AI Execution and Security Platform | Accurately reflects current implementation and future direction while keeping Guardian focused on cognition. |

---

# 4. Decision

Sentinel is designated as the AI Execution and Security Platform for AIEMS.

Official mission statement:

> Sentinel is the AI Execution and Security Platform for AIEMS, providing trusted execution, AI orchestration, policy enforcement, resilience and operational governance for AI systems.

---

# 5. Rationale

This decision preserves the clean architectural boundary established during ESR-0014:

- Guardian expresses intent.
- Sentinel governs execution.

Guardian remains responsible for cognition, planning, reasoning, memory use, goals and conversation.

Sentinel becomes responsible for trust, execution governance, provider orchestration, routing, health monitoring, failover, policy enforcement and future operational governance.

This model allows Sentinel to become a reusable AIEMS platform service that can support Guardian and future AI systems without embedding JARVIS-specific cognition or identity into Sentinel.

---

# 6. Consequences

- Sentinel remains a top-level reusable package.
- Guardian must not contain provider-specific or execution-governance logic.
- Provider selection, resilience and failover belong in Sentinel.
- Future trusted-execution capabilities belong naturally within Sentinel.
- Architecture documents must describe Sentinel as the AI Execution and Security Platform.
- Future provider, identity, audit, telemetry and compliance work should be designed as Sentinel capabilities unless there is a compelling architectural reason otherwise.

---

# 7. Sentinel Responsibility Model

Sentinel responsibilities include:

- Trust boundary enforcement.
- AI provider orchestration.
- Capability routing.
- Provider configuration.
- Provider health monitoring.
- Retry and failover.
- Execution history.
- Policy enforcement.
- Identity and authentication workstreams.
- Audit and telemetry workstreams.
- Compliance and operational governance workstreams.
- Trusted execution workstreams.

---

# 8. Guardian Relationship

Guardian is the cognition engine.

Guardian is responsible for:

- Cognition.
- Reasoning.
- Planning.
- Memory utilisation.
- Goal management.
- Conversation.

Sentinel is the trusted execution environment for Guardian.

Sentinel decides:

- Can this be done?
- Is it permitted to execute?
- Where should it be executed?
- How should it be executed?
- What policy, audit or resilience controls apply?

---

# 9. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Updated architecture model reflecting Sentinel's platform role. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider ecosystem evaluation aligned to Sentinel orchestration. |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Session report recording the implementation and approval context. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Earlier Sentinel trust-gateway pattern preserved but expanded by this ADR. |
| [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] | Provider abstraction and hybrid runtime strategy supported by Sentinel orchestration. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Evidence-based provider ecosystem selection framework. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 8 July 2026 | ChatGPT Engineering Session Assistant | Initial approved ADR created during ESR-0014 closure. |
