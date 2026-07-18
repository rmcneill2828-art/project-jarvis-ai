# Project JARVIS AI

> **Review Twice. Build Once. Improve for Everyone.**

Supporting principle:

> **Assume Nothing. Verify Everything.**

---

# Project Status

| Item | Status |
|------|--------|
| Project | Project JARVIS AI |
| Current Phase | [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] closed (17 July 2026) / Sentinel provider expansion and Memory & Network-Exposure architecture specifications |
| Repository Status | Operational |
| Engineering Framework | AIEMS v1.0 in development |
| Product Implementation | Operational First Light (Tkinter) / Guardian Desktop Platform Shell (Tauri + React, live UXP-backend bridge) |
| Current Engineering Focus | No engineering session currently open. [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] is the latest closed session, with [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained as the accepted repository baseline. See [[PST-0001_PROGRAMME_STATUS|PST-0001]] for the current authoritative programme-state snapshot. |

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
- First Light application skeleton launchable with `python -m jarvis` (Tkinter, historical reference implementation).
- Guardian Desktop Platform Shell (Tauri + React, `src/` and `src-tauri/`) as the current UXP direction, connected live to the Python backend over a stdio JSON-RPC bridge (ADR-0019).
- Operational Conversation Workspace with deterministic offline chat, session metadata and transcript export.
- Sentinel AI Execution and Security Platform (`sentinel/`): trust gateway, policy engine (`TrustTierPolicy` wired as the production policy engine), audit trail, and provider adapters for OpenAI, Gemini and a local Ollama fallback, with health-aware orchestration and failover to a local echo provider.
- Guardian Orb knowledge-graph rendering: the Guardian Orb visual presence renders a live graph built from the repository's own tracked markdown and WikiLinks (`jarvis/interfaces/knowledge_graph.py`), Phase 1 of the Guardian Experience Architecture.
- Memory and Data Storage Architecture specification ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]) approved; no persistent memory implementation exists yet (`jarvis/memory/` remains a stub).
- Python package structure.
- Root `Jarvis` lifecycle object.
- `JarvisState` lifecycle enumeration.
- Guardian Runtime Foundation with lifecycle ownership, service status snapshots and bounded observability interfaces.
- Package-level public API.
- GIA-BOOT Proof of Concept readiness interfaces.
- Automated tests for lifecycle, provider, policy, orchestration and stdio-bridge behaviour (254 tests, `jarvis/tests/` and `scripts/tests/`).
- Packaging configuration using package discovery.

Current JARVIS architecture direction includes:

- JARVIS Platform as the runtime operating platform.
- Guardian as the trusted digital companion / AI entity.
- Sentinel as the trust gateway before Platform Services.
- User Experience Platform (UXP) as the current presentation-layer architecture term.
- Provider Architecture for capability-based provider selection.
- Agent Framework for specialist capabilities serving Guardian.
- Device independence and portable restore as architecture requirements.

The canonical Guardian identity and cognitive architecture is recorded in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]. ESR-0008 architecture closure is recorded in [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]], ESR-0009 closure / ESR-0010 handover are recorded in [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] and [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]], ESR-0011 implementation-readiness closure is recorded in [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]], ESR-0012 Implementation Phase Initiation closure is recorded in [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]], and ESR-0013 Guardian Platform Foundation closure review is recorded in [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]].

---

# Repository Structure

```text
aiems/
  History/
    Full Chat/
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
  gia/
  guardian/
  gui/
  interfaces/
  memory/
  platform/
  services/
  shared/
  tests/
sentinel/
scripts/
  tests/
src/
src-tauri/
research/
  HABEI-0001/
```

`jarvis/` is the Python backend and legacy Tkinter shell. `sentinel/` is the AI execution and trust boundary (provider adapters, policy, audit). `src/` and `src-tauri/` are the Tauri + React Guardian Desktop Platform Shell (current UXP direction). `scripts/` holds repository tooling, including the AIEMS Exchange Bridge (`aiems_bridge.py`) used for Claude&harr;Codex review handovers.

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
| History Records | Repository-preserved session chat history and full chat evidence used for WP0 continuity review |

Key engineering artefacts include:

| Artefact | Purpose |
|----------|---------|
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Human-AI collaboration context |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | AI Engineering Playbook |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Closure review package for Guardian Platform Foundation implementation |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] | Closed engineering session report for Implementation Phase Initiation, GIA-BOOT Proof of Concept and AIEMS Engineering Agent validation |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] | Closed engineering session report for Architecture Validation, Implementation Readiness and ESR-0012 handover |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | Closed engineering session report for ESR-0009 closure and ESR-0010 handover |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Current accepted repository baseline |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture |
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
WP0 - Engineering Ecosystem Synchronisation
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

Operational workflow detail is maintained in [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and current Engineering Session Reports. ESR-0008 introduced Engineering Ecosystem Synchronisation as the current WP0 working practice, explicitly accounting for GitHub, AIEMS, OSE, Obsidian, controlled artefacts, registers, previous ESRs and summaries. WP0 session start follows [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] knowledge tiering: the Current State, Architecture, Active Standards and Current ESR tiers are reviewed at every session start, while AIEMS History and Full Chat artefacts form the Historical Archive tier, searched on demand rather than reviewed exhaustively. README introduces the workflow and directs engineers to the authoritative controlled artefacts.

Repository changes are expected to remain traceable to controlled engineering activities, approved Engineering Implementation Packages and approved governance artefacts.

---

# Repository Validation

Run lightweight repository governance validation from the repository root:

```text
python scripts/validate_repository.py
```

For documentation or governance-only packages:

```text
python scripts/validate_repository.py --governance-only
```

This checks WikiLinks, controlled artefact registration, stale programme status references and prohibited source/test changes during governance-only work.

---

# Launching JARVIS

Run the First Light application skeleton from the repository root:

```text
python -m jarvis
```

The current application provides an operational First Light Conversation Workspace with a simple GUI shell, animated orb placeholder, deterministic chat response, service status panel, session metadata, New Conversation, Clear Conversation and user-initiated transcript export. No external AI provider is required.

GUI remains the historical implementation term for the current Tkinter interface. Current architecture uses User Experience Platform (UXP) for future presentation-layer planning.

To run the Guardian Desktop Platform Shell (Tauri + React UXP, live backend bridge), install frontend dependencies with `npm install` and run `npm run tauri dev` from the repository root. This spawns `python -m jarvis --ipc-stdio` as a managed sidecar process; a configured OpenAI/Gemini API key (`OPENAI_API_KEY`/`GEMINI_API_KEY`) or a running local Ollama instance is optional and only changes which Sentinel provider handles conversation requests - a working conversation path exists with no provider configured.

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
| Platform Architecture | In Review | High | [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] defines the platform architecture; [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] defines Guardian identity and cognitive architecture. |
| Sentinel AI Execution and Security Platform | Implemented | High | Trust gateway, `TrustTierPolicy` (production policy engine), audit trail, and OpenAI/Gemini/Ollama provider adapters with failover, reachable live through the UXP-backend bridge. |
| Engineering Ecosystem | In Progress | High | ESR-0008 recognised Obsidian as the human-facing Engineering Knowledge Workspace for OSE while GitHub remains source of truth. |
| JARVIS Development | In Progress | Early/Partial | Operational First Light / Conversation Workspace, Guardian Desktop Platform Shell (Tauri + React) with a live backend bridge, Guardian Orb knowledge-graph rendering, lifecycle object, public API, GIA-BOOT Proof of Concept, Guardian Runtime Foundation, packaging configuration and tests exist. Persistent memory, voice, vision and the agent framework remain not started. |

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

## Phase 2 - JARVIS Architecture Readiness

Status: In progress.

Current focus (see [[PST-0001_PROGRAMME_STATUS|PST-0001]] for full detail):

- Guardian Runtime Foundation has been established and integrated into the JARVIS lifecycle, with the UXP-backend bridge (ADR-0019) live and reachable from the Tauri + React Guardian Desktop Platform Shell.
- Sentinel AI Execution and Security Platform is implemented: trust gateway, `TrustTierPolicy` wired as the production policy engine, audit trail, and OpenAI/Gemini/Ollama provider adapters with health-aware orchestration and failover.
- Guardian Orb knowledge-graph rendering (Guardian Experience Architecture Phase 1) is live, rendering the repository's own tracked markdown and WikiLinks as a graph.
- Memory and Data Storage Architecture ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]) and Sentinel Network Exposure Security Requirements ([[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]]) are approved as specifications; neither has a code implementation yet.
- [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remains the accepted repository baseline.
- Guardian Memory implementation, Provider Framework completion, Conversation Engine expansion, EAC and GDP-0001 implementation remain deferred.
- No engineering session is currently open; ESR-0026 is the latest closed session.

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
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and reload point - the authoritative source for current programme state; this README summarises but does not replace it. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Current accepted repository baseline. |
| [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] | Latest closed engineering session: Ollama Local Fallback Provider (EBG-0075), Memory and Data Storage Architecture (MDS-0001), Sentinel Network Exposure Security Requirements (ADR-0020) - the first session run entirely through the AIEMS Exchange Bridge. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Closure review package for Guardian Platform Foundation implementation and Programme Sponsor closure decision. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture. |
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
| 3.6 | 2 July 2026 | Codex Engineering Implementer | Refreshed README for ESR-0008 closure, RBL-0009, Guardian, Sentinel, UXP and Engineering Ecosystem Synchronisation. |
| 3.7 | 4 July 2026 | Codex Engineering Implementer | Aligned repository status with ESR-0010 closure context and RBL-0010 accepted baseline. |
| 3.8 | 4 July 2026 | Codex Engineering Implementer | Added AIEMS History folder orientation and WP0 session start review guidance for HST artefacts. |
| 3.9 | 4 July 2026 | Codex Engineering Implementer | Added AIEMS Full Chat folder orientation and WP0 session start review guidance for FCH historical evidence. |
| 3.10 | 5 July 2026 | Codex Engineering Implementer | Aligned repository orientation with ESR-0011 closure, implementation readiness and ESR-0012 handover guidance. |
| 3.11 | 5 July 2026 | Codex Engineering Implementer | Extended WP0 session start review guidance to HST-0011 and FCH-0011 ESR-0011 history artefacts. |
| 3.12 | 6 July 2026 | Codex Engineering Implementer | Aligned repository orientation with ESR-0012 closure, GIA-BOOT Proof of Concept completion and retained RBL-0010 baseline status. |
| 3.13 | 6 July 2026 | Codex Engineering Implementer | Extended WP0 session start review guidance to HST-0012 and FCH-0012 ESR-0012 history artefacts. |
| 3.14 | 7 July 2026 | Engineering Agent | Aligned repository orientation with ESR-0013 Guardian Platform Foundation closure review and retained RBL-0010 baseline status. |
| 3.16 | 8 July 2026 | Claude Engineering Implementer | Replaced exhaustive AIEMS History and Full Chat WP0 review requirement with GDE-0001 knowledge tiering, closing out the item flagged as outstanding in ESR-0014A. |
| 3.15 | 7 July 2026 | Engineering Agent | Added ESR-0013 AIEMS History and Full Chat artefacts to WP0 session start review guidance. |
| 3.17 | 18 July 2026 | Claude | Direct Programme Sponsor-requested correction (outside an open ESR): README had drifted 13 sessions stale (last describing ESR-0013 while the repository was at ESR-0026 / RBL-0015 / PST-0001 v2.48). Refreshed Project Status, JARVIS implementation summary, Repository Structure, Capability Roadmap, Phase 2 focus, launch guidance (added Tauri + React Guardian Desktop Platform Shell alongside First Light) and Related Artefacts to match current repository state. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
