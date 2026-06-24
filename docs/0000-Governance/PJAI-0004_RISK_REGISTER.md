# PJAI-0004 – Risk Register

> *"Every identified risk is an opportunity to improve the engineering system before it becomes a problem."*

**Version:** 2.0

---

# Purpose

The Risk Register is the authoritative record of all identified risks associated with Project JARVIS AI and the AI Engineering Management System (AIEMS).

Its purpose is to identify, assess, monitor and manage risks that may affect the successful delivery of the programme, ensuring risks are actively managed rather than reactively addressed.

---

# Scope

The register includes risks relating to:

- Strategic Direction
- Programme Delivery
- Engineering
- Technology
- Operations
- AI Governance
- Security
- Knowledge Management

---

# Risk Assessment Method

Each risk is assessed using:

| Score | Probability | Impact |
|------:|-------------|---------|
| 1 | Very Low | Negligible |
| 2 | Low | Minor |
| 3 | Medium | Moderate |
| 4 | High | Major |
| 5 | Very High | Critical |

**Overall Risk Score = Probability × Impact**

| Score | Classification |
|--------|----------------|
| 1–5 | Low |
| 6–10 | Medium |
| 11–15 | High |
| 16–25 | Critical |

---

# Risk Register

| Risk ID | Category | Risk Description | Probability | Impact | Score | Owner | Mitigation | Status |
|---------|----------|------------------|------------:|--------:|------:|-------|------------|--------|
| RSK-0001 | Strategic | AIEMS and JARVIS objectives become misaligned. | 2 | 5 | 10 | Programme Sponsor | Strategic Alignment Reviews before every phase. | Monitoring |
| RSK-0002 | Strategic | AIEMS becomes tightly coupled to JARVIS, reducing reuse. | 2 | 5 | 10 | Chief Architect | Maintain clear separation between framework and product. | Monitoring |
| RSK-0003 | Programme | Programme scope expands faster than governance can support. | 3 | 4 | 12 | Programme Sponsor | Phase gates, controlled change sets and governance reviews. | Open |
| RSK-0004 | Technical | Architectural decisions become inconsistent over time. | 2 | 4 | 8 | Chief Architect | Maintain ADR Register and Architecture Reviews. | Monitoring |
| RSK-0005 | Technical | Technology choices become obsolete during development. | 3 | 4 | 12 | Chief Architect | Review technology during every Strategic Alignment Review. | Open |
| RSK-0006 | Operational | Documentation becomes outdated. | 2 | 4 | 8 | Chief Architect | Documentation reviewed at every phase close-out. | Monitoring |
| RSK-0007 | Operational | Knowledge lost between engineering sessions. | 2 | 4 | 8 | Chief Architect | Engineering Session Reports and Lessons Learned Register. | Monitoring |
| RSK-0008 | AI Governance | AI repository interaction exceeds approved governance. | 1 | 5 | 5 | Programme Sponsor | AI Repository Interaction Policy (ADR-0004). | Mitigated |
| RSK-0009 | Security | Repository credentials or integrations become compromised. | 2 | 5 | 10 | Programme Sponsor | Principle of least privilege, MFA and periodic access reviews. | Monitoring |
| RSK-0010 | Knowledge | Key engineering rationale is not recorded. | 2 | 4 | 8 | Chief Architect | ADRs, ESRs and documentation-first engineering. | Monitoring |

---

# Risk Categories

## Strategic

Risks affecting the long-term vision, objectives or viability of the programme.

---

## Programme

Risks affecting delivery of Project JARVIS AI.

---

## Technical

Risks affecting architecture, engineering or technology.

---

## Operational

Risks affecting engineering activities and day-to-day project management.

---

## AI Governance

Risks associated with AI-assisted engineering.

---

## Security

Risks relating to confidentiality, integrity and availability.

---

## Knowledge

Risks affecting organisational learning and engineering continuity.

---

# Risk Management Process

Every identified risk shall be:

1. Identified
2. Assessed
3. Assigned
4. Mitigated
5. Monitored
6. Reviewed
7. Closed or Accepted

---

# Review Policy

The Risk Register shall be reviewed:

- At every Strategic Alignment Review.
- At the completion of every project phase.
- Following significant architectural decisions.
- Following major incidents.
- When new strategic risks are identified.

---

# Engineering Principle

Risks are not recorded to discourage innovation.

They are recorded to enable informed engineering decisions.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|----------------------------|---------------------------------------------------------------|
| 1.0 | 23 June 2026 | Project Sponsor | Initial Risk Register established. |
| 2.0 | 24 June 2026 | Project Sponsor & Chief Architect | Expanded to support AIEMS with structured risk categories, scoring, governance and strategic programme risks. |