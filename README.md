# Project JARVIS AI

> **Review Twice. Build Once. Improve for Everyone.**

Supporting principle:

> **Assume Nothing. Verify Everything.**

---

# Project Status

| Item | Status |
|------|--------|
| Project | Project JARVIS AI |
| Current Phase | Phase 2 - Engineering Standards |
| Repository Status | Operational |
| Engineering Framework | AIEMS v1.0 in development |
| Product Implementation | Operational First Light / Conversation Workspace |
| Current Engineering Focus | Continue from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] into [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] JARVIS product engineering |

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
- Programme status and engineering session reporting.

## JARVIS

JARVIS is the intelligent AI platform and flagship implementation of AIEMS.

The authoritative product blueprint is maintained in [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]]. That document explains why JARVIS exists, how it should behave, what it should become and how product capabilities relate to each other.

Current JARVIS implementation includes:

- Product architecture blueprint in [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- First Light application skeleton launchable with `python -m jarvis`.
- Operational Conversation Workspace with deterministic offline chat, session metadata and transcript export.
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
    baselines/
    charters/
    conversation/
    decisions/
    playbooks/
    registers/
    reviews/
    sessions/
    status/
  models/
  standards/
docs/
  0000-Governance/
jarvis/
  architecture/
  automation/
  config/
  core/
  guardian/
  gui/
  interfaces/
  memory/
  services/
  shared/
  tests/
research/
  HABEI-0001/
```

---

# Engineering Governance

The project follows a documentation-first, repository-first and evidence-led engineering methodology.

The Git repository is the authoritative engineering baseline. Conversations provide working context but do not define project state.

Repository continuity replaces dependence upon long conversation history by recording engineering state, decisions and baselines in controlled artefacts.

Key controlled artefact families include:

| Artefact Family | Purpose |
|-----------------|---------|
| Charters | Vision, scope, authority and engineering constitution |
| ADRs | Architectural and engineering decisions |
| Registers | Controlled artefacts, ADRs, risks and actions |
| Reviews | Strategic reviews, engineering features and evaluations |
| Standards | Controlled artefact, documentation and software engineering standards |
| Models | Platform architecture model |
| Playbooks | Practical AI engineering behaviour and workflow |
| Conversation Context | Lightweight Human-AI session operating context |
| Programme Status | Current programme state and engineering focus |
| Session Reports | Engineering session continuity and accepted baseline records |

Key engineering artefacts include:

| Artefact | Purpose |
|----------|---------|
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Human-AI collaboration context |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | AI Engineering Playbook |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Current initialised engineering session report |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Current accepted repository baseline |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Engineering backlog register |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Controlled Artefact Standard |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] | Engineering Documentation Standard |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Software / Python Engineering Standard |

---

# AI-Assisted Engineering

Project JARVIS AI is developed using a governed Human-AI engineering model.

Human-AI engineering roles are deliberately separated.

| Role | Responsibility |
|------|----------------|
| Programme Sponsor | Engineering authority, approval and Git operations |
| Engineering Architect / Reviewer | Engineering design, review and independent verification |
| Engineering Implementer | Approved implementation and completion reporting |
| Git Repository | Authoritative engineering baseline |

Final authority for engineering direction, approval and Git operations remains with the Human Engineer / Programme Sponsor.

---

# Development Workflow

Every significant engineering activity follows the approved AIEMS workflow at a high level.

```text
WP0 - Engineering Synchronisation
    |
Engineering Design
    |
Engineering Implementation Package
    |
Programme Sponsor Approval
    |
Engineering Implementation
    |
Engineering Self Review
    |
Git Commit & Push
    |
Independent Repository Verification
    |
Baseline Acceptance
    |
Continue Engineering
```

Operational workflow detail is maintained in [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and current Engineering Session Reports. README introduces the workflow and directs engineers to the authoritative controlled artefacts.

Repository changes are expected to remain traceable to controlled engineering activities, approved Engineering Implementation Packages and approved governance artefacts.

---

# Launching JARVIS

Run the First Light application skeleton from the repository root:

```text
python -m jarvis
```

The current application provides an operational First Light Conversation Workspace with a simple GUI shell, animated orb placeholder, deterministic chat response, service status panel, session metadata, New Conversation, Clear Conversation and user-initiated transcript export. No external AI provider is required.

---

# Repository Engineering Health Review

Repository Engineering Health Reviews are performed during Engineering Synchronisation to identify governance drift, documentation inconsistencies, missing artefacts, technical debt and recommended Engineering Implementation Packages.

Operational detail is recorded in Engineering Session Reports.

---

# Engineering Philosophy

Project JARVIS AI applies repository-first engineering through small, independently verified engineering changes.

Engineering work is evidence-led: context is gathered before implementation, decisions are captured in controlled artefacts and repository changes are validated before baseline acceptance.

---

# Capability Roadmap

| Capability | Status | Engineering Maturity | Comments |
|------------|--------|----------------------|----------|
| Repository Architecture | Complete | Complete | Repository structure separates AIEMS governance from JARVIS implementation. |
| Governance Framework | In Progress | Mature | Core governance exists; register and artefact consistency is actively managed. |
| Engineering Standards | In Progress | High | [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]], [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] and [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] are approved; additional build-facing standards remain planned. |
| Platform Architecture | In Progress | Partial | [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] defines the platform architecture; [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] defines the product blueprint. |
| JARVIS Development | In Progress | Partial | Operational First Light / Conversation Workspace, lifecycle object, public API, packaging configuration and tests exist. |

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

Status: Completed and validated.

Delivered:

- Initial AIEMS standards baseline.
- Repository integrity remediation.
- Operational Engineering Workflow v3.
- Programme status reload point.
- Engineering Session Report model.

## Phase 2 - Engineering Standards

Status: In progress.

Current focus:

- Complete the minimum viable Engineering Standards baseline.
- Complete remaining build-facing engineering standards.
- Prepare for platform decomposition.
- Preserve repository-backed session continuity.

---

# Repository Standards

The primary branch (`main`) represents the approved repository baseline.

No significant repository change should be made without Human Engineer approval and traceable engineering context.

---

# Acknowledgements

Project JARVIS AI is a collaborative engineering programme between the Programme Sponsor and AI engineering collaborators working under AIEMS.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and reload point. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Current accepted repository baseline. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Current initialised engineering session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source for selecting future engineering packages. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Authoritative JARVIS product architecture. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability maturity and prioritisation support. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 1.0 | 22 June 2026 | Project Sponsor | Initial repository created and project introduced. |
| 2.0 | 24 June 2026 | Project Sponsor & Chief Architect | Phase 0 validated and completed. Introduced AIEMS, Engineering Philosophy, Strategic Alignment Reviews, AI-assisted engineering model, repository governance and updated project roadmap. |
| 3.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled README with current AIEMS repository structure, governance artefacts, project roadmap and JARVIS implementation baseline. |
| 3.1 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned README with AIEMS Workflow v3, repository-first engineering, current engineering roles, repository health review practice and STD-0003 baseline status. |
| 3.2 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added reference to the JARVIS OS product architecture blueprint. |
| 3.3 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added First Light launch guidance and updated JARVIS implementation summary. |
| 3.4 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified the JARVIS product architecture as the authoritative home for recovered product vision and behaviour. |
| 3.5 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Updated current product state to Operational First Light / Conversation Workspace following RBL-0006 acceptance. |
