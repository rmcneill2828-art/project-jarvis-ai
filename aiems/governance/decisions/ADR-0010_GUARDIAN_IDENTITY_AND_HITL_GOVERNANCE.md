# ADR-0010 - Guardian Identity and HITL Governance

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0010 |
| Title | Guardian Identity and HITL Governance |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant Guardian identity or governance model change |

---

# Purpose

Record the ESR-0008 decision that Guardian is the singular trusted digital companion / AI entity and human-in-the-loop governance point.

---

# Scope

This decision covers Guardian identity, judgement, consent, policy, privacy, approval, memory retention and future trusted mobile approve/deny capability. It does not implement Guardian runtime behaviour.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]].
- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

JARVIS needs a clear user-facing AI identity and governance boundary for consent, privacy, policy, memory retention and high-risk approval.

---

# 2. Background

ESR-0008 identified Guardian as the trusted digital companion / AI entity hosted by the JARVIS Platform.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Multiple user-facing AI identities | Increases confusion and weakens trust. |
| Platform as identity | Blurs infrastructure with companion behaviour. |
| Singular Guardian identity | Preserves a coherent trusted companion and governance point. |

---

# 4. Decision

Guardian is the singular user-facing AI entity. Guardian asks: Should this happen?

Guardian governs consent, policy, privacy, approval, memory retention and human-in-the-loop decisions. Remote approve / deny from trusted mobile endpoints is a future Guardian capability.

---

# 5. Rationale

Guardian provides a coherent trust relationship for users while allowing the JARVIS Platform to host many services and specialist agents behind that identity.

---

# 6. Consequences

- Guardian remains singular.
- Human authority remains explicit for high-risk decisions.
- Mobile approval is a future capability, not current runtime implementation.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines Guardian identity and faculties. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture aligned to Guardian identity. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording Guardian identity discovery. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records Guardian architecture follow-up work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
