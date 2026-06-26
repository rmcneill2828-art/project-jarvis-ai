# Project JARVIS AI

> **Review Twice. Build Once. Improve for Everyone.**

Supporting principle:

> **Assume Nothing. Verify Everything.**

---

# Project Status

| Item | Status |
|------|--------|
| Project | Project JARVIS AI |
| Current Phase | Phase 1 - Engineering Readiness |
| Repository Status | Operational |
| Engineering Framework | AIEMS v1.0 in development |
| Product Implementation | JARVIS lifecycle skeleton established |
| Current Engineering Focus | Repository integrity, AIEMS maturity and PBK-0001 operational workflow |

---

# Vision

Project JARVIS AI aims to design and build a trusted, extensible and intelligent AI platform capable of assisting users through natural conversation, automation, decision support and continuous learning.

The project is built upon strong engineering governance, ensuring decisions remain traceable, auditable and maintainable throughout the lifetime of the system.

---

# Two Deliverables

Project JARVIS AI consists of two complementary deliverables.

## AIEMS

**AI Engineering Management System**

AIEMS is the engineering framework developed alongside JARVIS. It defines how AI-enabled systems are planned, governed, engineered, validated and maintained.

Current AIEMS capabilities include:

- Platform governance.
- Controlled artefact management.
- Engineering standards.
- Architecture modelling.
- ADR management.
- Risk and action registers.
- Engineering feature reviews.
- AI engineering playbooks.
- Human-AI collaboration context.

## JARVIS

JARVIS is the intelligent AI platform and flagship implementation of AIEMS.

Current JARVIS implementation includes:

- Python package structure.
- Root `Jarvis` lifecycle object.
- `JarvisState` lifecycle enumeration.
- Package-level public API.
- Automated tests for lifecycle behaviour and public API import.
- Packaging configuration using package discovery.

---

# Repository Structure

```text
aiems/
  governance/
    charters/
    conversation/
    decisions/
    playbooks/
    registers/
    reviews/
  models/
  standards/
jarvis/
  automation/
  core/
  guardian/
  interfaces/
  memory/
  shared/
  tests/
research/
shared/
tools/
```

---

# Engineering Governance

The project follows a documentation-first and evidence-led engineering methodology.

Key controlled artefact families include:

| Artefact Family | Purpose |
|-----------------|---------|
| Charters | Vision, scope, authority and engineering constitution |
| ADRs | Architectural and engineering decisions |
| Registers | Controlled artefacts, ADRs, risks and actions |
| Reviews | Strategic reviews, engineering features and evaluations |
| Standards | Controlled artefact and documentation standards |
| Models | Platform architecture model |
| Playbooks | Practical AI engineering behaviour and workflow |
| Conversation Context | Lightweight Human-AI session operating context |

---

# AI-Assisted Engineering

Project JARVIS AI is developed using a governed Human-AI engineering model.

AI is used to support:

- Architecture.
- Documentation.
- Repository analysis.
- Engineering implementation.
- Engineering reviews.
- Development planning.

Final authority for engineering direction, approval and Git operations remains with the Human Engineer / Programme Sponsor.

---

# Development Workflow

Every significant engineering activity follows the AIEMS workflow.

```text
Review
    |
Approve
    |
Execute
    |
Verify
    |
Improve
```

Repository changes are expected to remain traceable to controlled engineering activities and approved governance artefacts.

---

# Capability Roadmap

| Capability | Status | Engineering Maturity | Comments |
|------------|--------|----------------------|----------|
| Repository Architecture | Complete | Complete | Repository structure separates AIEMS governance from JARVIS implementation. |
| Governance Framework | In Progress | Mature | Core governance exists; register and artefact consistency is actively managed. |
| Engineering Standards | In Progress | Partial | STD-0001 and STD-0002 exist; additional standards remain future work. |
| Platform Architecture | In Progress | Partial | MOD-0001 defines the platform architecture; implementation decomposition remains future work. |
| JARVIS Development | In Progress | Partial | Lifecycle skeleton, public API, packaging configuration and tests exist. |

---

# Current Roadmap

## Phase 0 - Foundation

Status: Completed and validated.

Delivered:

- Repository foundation.
- Governance foundation.
- Initial engineering standards.
- Architecture baseline.
- Development environment foundation.

## Phase 1 - Engineering Readiness

Status: In progress.

Current focus:

- Complete AIEMS standards library.
- Maintain repository integrity.
- Establish operational engineering workflow.
- Expand JARVIS core skeleton from governed architecture.
- Strengthen repeatable validation and documentation practices.

---

# Repository Standards

The primary branch (`main`) represents the approved repository baseline.

No significant repository change should be made without Human Engineer approval and traceable engineering context.

---

# Acknowledgements

Project JARVIS AI is a collaborative engineering programme between the Programme Sponsor and AI engineering collaborators working under AIEMS.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 1.0 | 22 June 2026 | Project Sponsor | Initial repository created and project introduced. |
| 2.0 | 24 June 2026 | Project Sponsor & Chief Architect | Phase 0 validated and completed. Introduced AIEMS, Engineering Philosophy, Strategic Alignment Reviews, AI-assisted engineering model, repository governance and updated project roadmap. |
| 3.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled README with current AIEMS repository structure, governance artefacts, project roadmap and JARVIS implementation baseline. |