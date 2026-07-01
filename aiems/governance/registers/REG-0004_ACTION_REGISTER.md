# REG-0004 - Action Register

> *"Actions transform strategy into delivery. Every action should have a purpose, an owner and a measurable outcome."*

**Version:** 2.3

---

# Purpose

The Action Register is the authoritative record of approved engineering, governance and programme activities within Project JARVIS AI and AIEMS.

It ensures all significant work is planned, prioritised, traceable and linked to the decisions and risks that justified it.

---

# Scope

The register records actions arising from:

- Strategic Alignment Reviews (SAR)
- Architecture Decision Records (ADR)
- Engineering Session Reports (ESR)
- Risk Reviews
- Phase Gates
- Engineering Reviews
- Programme Governance

---

# Action Register

| Action ID | Title | Description | Linked ADR | Linked Risk | Change Set | Owner | Priority | Target Phase | Status | Completion Date |
|------------|------------------------------|------------------------------------------------------|-------------|-------------|------------|-----------------|----------|--------------|-------------|----------------|
| ACT-0001 | Complete Phase 0 Close-out | Complete all governance updates following Phase 0 validation. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0003 | CS-0001 | Programme Sponsor / Chief Architect | Critical | Phase 0 | Completed | 24 Jun 2026 |
| ACT-0002 | Conduct SAR-0001 | Complete the first Strategic Alignment Review before opening Phase 1. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0001 | CS-0002 | Programme Sponsor | Critical | Phase 0 | Completed | 24 Jun 2026 |
| ACT-0003 | Open Phase 1 | Formally open Phase 1 following successful completion of SAR-0001. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0003 | CS-0003 | Programme Sponsor | Critical | Phase 1 | Completed | 24 Jun 2026 |
| ACT-0004 | Create AI Repository Interaction Policy | Produce [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY]] defining AI repository governance. | [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY]] | RSK-0008 | CS-0001 | Chief Architect | High | Phase 0 | Completed | 24 Jun 2026 |
| ACT-0005 | Create Development Environment Guide | Document the verified development environment and AI integration process. | [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY]] | RSK-0009 | CS-0001 | Chief Architect | High | Phase 0 | Open | - |
| ACT-0006 | Create Engineering Session Log | Establish the permanent Engineering Session Log. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0007 | CS-0001 | Chief Architect | Medium | Phase 0 | Open | - |
| ACT-0007 | Create Lessons Learned Register | Establish a permanent organisational learning register. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0010 | CS-0001 | Chief Architect | Medium | Phase 0 | Open | - |
| ACT-0008 | Validate AI Repository Maintenance Workflow | Confirm whether AI can reliably perform ongoing repository maintenance. | [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY]] | RSK-0008 | CS-0001 | Programme Sponsor / Chief Architect | Medium | Phase 1 | Open | - |
| ACT-0009 | Develop AIEMS Documentation Standard | Create a common documentation standard for all controlled artefacts. | [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | RSK-0006 | Phase 1 | Chief Architect | High | Phase 1 | Completed | 26 Jun 2026 |

---

# Action Lifecycle

Every action progresses through the following lifecycle.

```text
Proposed
    |
    v
Approved
    |
    v
Open
    |
    v
In Progress
    |
    v
Completed
    |
    v
Closed
```

Deferred actions remain within the register until either completed or formally cancelled.

---

# Action Management Principles

Every action shall:

- Have a unique identifier.
- Have a clearly defined owner.
- Be traceable.
- Have a measurable outcome.
- Support programme objectives.
- Be reviewed regularly.
- Remain within the register after completion.

---

# Review Policy

The Action Register shall be reviewed:

- During every Engineering Session.
- During every Strategic Alignment Review.
- At the completion of every programme phase.
- Following major architectural decisions.
- When new risks or priorities emerge.

---

# Engineering Principle

Actions should never exist without purpose.

Every action should contribute towards improving AIEMS, JARVIS or both.

---

# Related Artefacts

* [[REG-0002_ADR_REGISTER|REG-0002]] records architectural decisions linked from action records.
* [[REG-0003_RISK_REGISTER|REG-0003]] records risks linked from action records.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.
* [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] records the current Engineering Session context.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] records engineering backlog items that may supersede or continue action register work.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|----------------------------|---------------------------------------------------------------|
| 1.0 | 23 June 2026 | Project Sponsor | Initial Action Register established. |
| 2.0 | 24 June 2026 | Project Sponsor & Chief Architect | Expanded to support AIEMS with linked ADRs, risks, change sets, ownership, priorities and lifecycle management. |
| 2.1 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Repository architecture alignment. Updated artefact identifiers, Platform terminology and repository references. |
| 2.2 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled Phase 0 and SAR-0001 action statuses with the current repository baseline. |
| 2.3 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled completed AIEMS Documentation Standard action following standards baselining. |
