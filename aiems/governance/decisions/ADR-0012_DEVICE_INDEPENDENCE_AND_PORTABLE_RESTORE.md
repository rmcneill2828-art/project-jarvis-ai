# ADR-0012 - Device Independence and Portable Restore

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0012 |
| Title | Device Independence and Portable Restore |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant storage, restore or device architecture change |

---

# Purpose

Record the ESR-0008 decision that devices host JARVIS but do not define JARVIS.

---

# Scope

This decision covers device independence, bootstrap, progressive restore, portable memory and portable configuration. It does not implement backup, sync or restore.

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

JARVIS must remain portable across devices without treating any single device as the system of record.

---

# 2. Background

ESR-0008 approved hybrid portable memory architecture, local-first runtime cache and encrypted sync / restore requirements.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Device as system of record | Creates lock-in and recovery risk. |
| Cloud-only system of record | Weakens local-first and privacy objectives. |
| Portable restore architecture | Balances portability, resilience, privacy and device independence. |

---

# 4. Decision

Devices host JARVIS but do not define JARVIS.

JARVIS shall require bootstrap, progressive restore, minimal data pull-down for new hardware, portable memory and portable configuration. Devices are execution environments, not the system of record.

---

# 5. Rationale

Device independence protects continuity, replacement, recovery and future multi-device operation.

---

# 6. Consequences

- Local runtime caches are not authoritative memory by themselves.
- Restore and sync require encryption and policy controls.
- Platform Services must include bootstrap, configuration, device registry, progressive restore, health, capability registry and backup/sync coordination.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines identity that must survive device changes. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model aligned to device independence. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording portable restore decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future restore architecture work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
