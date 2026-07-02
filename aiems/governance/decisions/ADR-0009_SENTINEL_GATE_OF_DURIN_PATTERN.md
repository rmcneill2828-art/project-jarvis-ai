# ADR-0009 - Sentinel Gate of Durin Pattern

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0009 |
| Title | Sentinel Gate of Durin Pattern |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant trust gateway or platform entry change |

---

# Purpose

Record the ESR-0008 decision to establish Sentinel as the trust gateway before Platform Services.

---

# Scope

This decision covers Sentinel placement, trust-gateway responsibility and the Gate of Durin Pattern. It does not implement authentication, authorisation or runtime security controls.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]].
- [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

JARVIS requires a clear trust boundary before platform services receive external input, device events, integrations or user requests.

---

# 2. Background

ESR-0008 recovered Sentinel as separate from Guardian. Sentinel protects system, repository, AIEMS, infrastructure and cyber/security boundaries.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Trust checks inside each service | Distributed and inconsistent. |
| Guardian-only trust handling | Blurs trust validation with judgement and consent. |
| Sentinel before Platform Services | Creates a clear platform entry trust gateway. |

---

# 4. Decision

JARVIS shall apply the Sentinel Gate of Durin Pattern.

Sentinel sits before Platform Services. Everything entering JARVIS passes through Sentinel. Sentinel asks: Can this be trusted?

The phrase "Speak, friend, and enter" is retained as an architectural metaphor for trusted entry, not as a literal authentication mechanism.

---

# 5. Rationale

The pattern separates trust validation from Guardian judgement. It allows JARVIS to reject, quarantine or constrain untrusted inputs before they reach platform services or Guardian faculties.

---

# 6. Consequences

- Platform Services sit behind Sentinel.
- Sentinel and Guardian must remain distinct.
- Future trust tiers should be defined for internet and external integration.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines Sentinel relationship to Guardian and Platform Services. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model aligned to Sentinel entry pattern. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording the Gate of Durin decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records Sentinel architecture follow-up work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
