# ADR-0007 - User Experience Platform Selection

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0007 |
| Title | User Experience Platform Selection |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant user experience platform change |

---

# Purpose

Record the ESR-0008 decision to evolve GUI terminology to User Experience Platform and select Tauri + React as the UXP direction.

---

# Scope

This decision covers UXP terminology, selected platform direction and separation of presentation from business logic and system state. It does not implement runtime functionality.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

JARVIS requires a presentation platform that can evolve beyond the historical GUI term while preserving separation between user experience, business logic and runtime state.

---

# 2. Background

ESR-0008 identified User Experience Platform (UXP) as the current architectural term for the presentation layer. GUI remains a historical implementation term.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Continue generic GUI terminology | Preserves history but is too narrow for the future platform surface. |
| Browser-only web application | Portable but weaker for Windows-first local application intent. |
| Native desktop only | Strong local integration but higher platform cost. |
| Tauri + React UXP | Lightweight local shell with modern UI capability and controlled platform integration. |

---

# 4. Decision

JARVIS shall use the term User Experience Platform (UXP) for current architecture. Tauri + React is selected as the UXP direction.

UXP visualises state and interaction. It does not own business logic or system state.

---

# 5. Rationale

Tauri + React supports Windows-first delivery, modern interface development, local-first operation and future portability while avoiding unnecessary runtime weight.

---

# 6. Consequences

- Current architectural references should use UXP.
- Historical GUI references remain valid as historical language.
- Business logic shall remain in platform services, core services or governed runtime components.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture consuming UXP terminology. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model consuming UXP alignment. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording UXP selection. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future UXP follow-up work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
