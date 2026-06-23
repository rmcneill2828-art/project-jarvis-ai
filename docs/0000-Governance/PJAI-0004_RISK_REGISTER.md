# Risk Register

---

## Document Control

| Field | Value |
|------|------|
| Document ID | PJAI-0004 |
| Document Title | Risk Register |
| Version | 1.0 |
| Status | Approved Baseline |
| Owner | Project Sponsor & Chief Architect |
| Programme | Project JARVIS AI |
| Product | JARVIS OS |
| Classification | Internal |
| Last Updated | 23 June 2026 |
| Next Review | Phase Gate Review |

---

# 1. Purpose

The Risk Register records the significant risks that could affect the successful delivery of Project JARVIS AI.

The objective is not to eliminate all risk, but to identify, assess and actively manage risks throughout the project lifecycle.

---

# 2. Risk Assessment Scale

| Likelihood | Description |
|------------|-------------|
| Low | Unlikely |
| Medium | Possible |
| High | Likely |

| Impact | Description |
|---------|-------------|
| Low | Minor impact |
| Medium | Noticeable impact requiring management |
| High | Significant impact to the project |

Overall Risk = Professional judgement based on likelihood and impact.

---

# 3. Active Risk Register

| ID | Category | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|----|----------|------|------------|--------|------------|-------|--------|
| R-001 | Delivery | Loss of momentum or project burnout | Medium | High | Maintain realistic pace, take regular breaks, work in achievable increments | Project Sponsor | Open |
| R-002 | Governance | Process drift from agreed standards | Medium | High | Follow Engineering Constitution, ADRs and RTBO. Challenge deviations. | Joint | Open |
| R-003 | Knowledge | Important decisions not captured | Medium | Medium | Maintain ADR Register and controlled documentation. | Chief Architect | Open |
| R-004 | Technical | Overengineering delays delivery | Medium | High | Regularly review whether documentation and process continue to add value. | Joint | Open |
| R-005 | Security | Accidental exposure of credentials or sensitive information | Low | High | Use Git ignore rules, avoid storing secrets in the repository and review before committing. | Project Sponsor | Open |
| R-006 | Infrastructure | Loss of development environment or hardware failure | Low | High | Use GitHub as the primary repository and verify commits before switching devices. | Project Sponsor | Open |
| R-007 | External | Significant changes to AI platforms, APIs or licensing | Medium | Medium | Design modular architecture and regularly review technology choices. | Chief Architect | Open |
| R-008 | Delivery | Competing work or family priorities reduce available development time | High | Medium | Plan realistic milestones and prioritise consistency over speed. | Project Sponsor | Open |

---

# 4. Risk Review Process

Risks shall be reviewed:

- At each Engineering Checkpoint.
- At the end of every project phase.
- Following any significant architectural decision.
- When a new material risk is identified.

Closed risks remain recorded for historical reference.

---

# 5. Risk Response Strategy

Project JARVIS AI follows four response options:

- Avoid
- Reduce
- Transfer
- Accept

The preferred response is to reduce risk where practical through good engineering and governance.

---

# 6. Responsibilities

## Project Sponsor

Responsible for:

- Reviewing project risks.
- Accepting business risk.
- Escalating new risks.

---

## Chief Architect

Responsible for:

- Identifying technical risks.
- Recommending mitigations.
- Reviewing architectural impacts.

---

## 7. Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 23 June 2026 | Initial approved baseline. |

---

# End of Approved Content

Any content below this point is considered draft until formally approved.