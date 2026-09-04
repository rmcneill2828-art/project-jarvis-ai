# Project JARVIS AI

> **Review Twice. Build Once. Improve for Everyone.**

Supporting principle:

> **Assume Nothing. Verify Everything.**

---

# Project Status

| Item | Status |
|------|--------|
| Project | Project JARVIS AI |
| Current Phase | No session currently open. [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] closed (4 September 2026) / four Work Packages delivered: EBG-0085 esbuild/vite security upgrade (WP1), EBG-0058 accretion re-check (WP2), EBG-0046 DRA-0001 architecture (WP3), JRM-0001 staleness fix (WP4), plus a Pass session-wide WP6 and a WP7 Establish determination (RBL-0036) |
| Repository Status | Operational |
| Engineering Framework | AIEMS v1.0 in development |
| Product Implementation | Operational First Light (Tkinter) / Guardian Desktop Platform Shell (Tauri + React, live UXP-backend bridge, packaged as a distributable installer since ESR-0032) |
| Current Engineering Focus | No session is currently open. [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] is the latest closed session, with [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] (established at ESR-0056 WP7) as the current repository baseline - a Vite/esbuild dev-server security fix plus DRA-0001, a new Platform Services architecture model (Draft) covering device bootstrap, registry, sync protocol and progressive restore. See [[PST-0001_PROGRAMME_STATUS|PST-0001]] for the current authoritative programme-state snapshot. |

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
- Guardian Orb knowledge-graph rendering: the Guardian Orb visual presence renders a live graph built from the repository's own tracked markdown and WikiLinks (`jarvis/interfaces/knowledge_graph.py`), Phase 1 of the Guardian Experience Architecture. Phase 2 (cluster illumination, ESR-0051) is also live: real, observed backend RPC activity (`jarvis/interfaces/activity_tracker.py`) now illuminates the corresponding cluster in both the Orb and the Active Clusters panel.
- Memory and Data Storage Architecture specification ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]) approved; its Personal Memory tier is implemented (`jarvis/memory/`, a real consent-gated SQLite store, ESR-0027) and wired into live conversation via the Guardian Cognitive Core (ESR-0039). Session and Shared-Family tiers remain not started.
- Guardian Voice faculty, Phase 6, both increments: Sentinel-gated speech output (Increment A, self-hosted TTS, `sentinel/kokoro_provider.py`, ESR-0044/wired ESR-0053) and speech input (Increment B, self-hosted `faster-whisper` STT, `sentinel/whisper_provider.py`, push-to-talk mic button gated on real-time capability detection, ESR-0047). Both wired into the live JSON-RPC bridge (`guardian.speak`/`guardian.transcribe`) and the Guardian Desktop Platform Shell. **Guardian's production voice is now Kokoro** (`bm_george` primary, `bf_isabella` automatic runtime fallback, ESR-0053) - a materially more natural, expressive voice than the original Piper adapter (`sentinel/piper_provider.py`, ESR-0044), selected via a real Programme Sponsor listening comparison and replacing Piper outright in production; `piper_provider.py` remains intact and tested, unregistered from production rather than deleted. Vision remains not started.
- Local Agent Permission Boundary defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A): the policy boundary a future Local Agent/Action faculty implementation must obey. Architecture only - no local-agent code exists yet (ESR-0041).
- User Identity and Profile Foundation (`jarvis/identity/`): local, unauthenticated profile create/list/select, role-tagged against GAM-0001 Section 8.1's four household roles, reachable through a real UXP profile picker replacing the previous static placeholder (ESR-0046). Credentialed authentication, memory scoping by profile and enforcement of the roles' differing authority remain not implemented.
- Python package structure.
- Root `Jarvis` lifecycle object.
- `JarvisState` lifecycle enumeration.
- Guardian Runtime Foundation with lifecycle ownership, service status snapshots and bounded observability interfaces.
- Package-level public API.
- GIA-BOOT Proof of Concept readiness interfaces.
- Automated tests for lifecycle, provider, policy, orchestration, stdio-bridge, memory, cognitive-core, voice and identity behaviour (485 tests plus 1 correctly-skipped test, `jarvis/tests/` and `scripts/tests/`).
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
| [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] | Current accepted repository baseline |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Engineering backlog register |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Controlled Artefact Standard |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] | Engineering Documentation Standard |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Software / Python Engineering Standard |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Validation and Quality Assurance Standard |
| [[STD-0006_CONFIGURATION_AND_SECRETS_STANDARD|STD-0006]] | Configuration and Secrets Standard |
| [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] | v1.0 Readiness Scorecard |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Launch Gap Backlog |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Guardian Authority and Boundary Model - Section 8.1's Household Role Model, now operationally implemented by `jarvis/identity/`. |

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
| Platform Architecture | In Review | High | [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] defines the platform architecture, including an Agent Framework subsection (ESR-0048) - a specialist-agent contract shape gated through the mandatory Sentinel `TrustTierPolicy` wiring, now implemented as real code (ESR-0049) and invokable live through the UXP (ESR-0050): GIA's read-only observability wired as the first live specialist agent; [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] defines Guardian identity and cognitive architecture. |
| Sentinel AI Execution and Security Platform | Implemented | High | Trust gateway, `TrustTierPolicy` (production policy engine), audit trail, and OpenAI/Gemini/Ollama provider adapters with failover, reachable live through the UXP-backend bridge. |
| Engineering Ecosystem | In Progress | High | ESR-0008 recognised Obsidian as the human-facing Engineering Knowledge Workspace for OSE while GitHub remains source of truth. |
| JARVIS Development | In Progress | Early/Partial | Operational First Light / Conversation Workspace, Guardian Desktop Platform Shell (Tauri + React) with a live backend bridge, Guardian Orb knowledge-graph rendering, lifecycle object, public API, GIA-BOOT Proof of Concept, Guardian Runtime Foundation, packaging configuration and tests exist. Guardian Cognitive Core (memory/history-informed reasoning), Personal Memory tier, Voice Phase 6 (both speech output and speech input increments) and User Identity and Profile Foundation (`jarvis/identity/`, local unauthenticated profile create/list/select) are implemented; the Local Agent Permission Boundary is defined (GAM-0001 Section 8A). The Agent Framework now has its first real, live specialist agent (`jarvis/agents/`, GIA read-only observability, Sentinel-gated, reachable via `guardian.agent.*` RPC methods, ESR-0049), now invokable live through the UXP via a new `AgentFrameworkPanel` (ESR-0050). Credentialed authentication, memory scoping by profile, role-authority enforcement, the wider Action faculty (local device/system control), Vision and Session/Shared-Family memory remain not started. |

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
- Guardian Orb knowledge-graph rendering (Guardian Experience Architecture Phase 1) is live, rendering the repository's own tracked markdown and WikiLinks as a graph on a Canvas 2D surface (migrated from SVG at ESR-0029). Phase 2 (cluster illumination, ESR-0051) is also live - real, observed backend RPC activity illuminates the corresponding cluster in both the Orb and the Active Clusters panel; Phases 3 (agent-traversal animation) and 4 (Guardian reasoning connection) remain not started.
- Memory and Data Storage Architecture ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]) is approved and its Personal Memory tier is implemented (`jarvis/memory/`, ESR-0027) and wired into live conversation via the Guardian Cognitive Core (ESR-0039); Sentinel Network Exposure Security Requirements ([[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]]) remains an approved specification with no network-facing interface built yet.
- GIA (Guardian Instrumentation Agent) Phase 1 local resource observability (CPU/memory/storage/process health/engineering-environment presence) is implemented and live-verified (ESR-0029). Phase 3 (engineering instrumentation) is now complete in full - git state (ESR-0054); repository health and register state (ESR-0055) - the first concrete steps of a staged path toward JARVIS/Guardian/Sentinel self-awareness: `gia.engineeringStatus` and the `gia-engineering` specialist agent give JARVIS real read access to its own repository git state (branch, uncommitted files, last commit), validation health (error/warning counts) and controlled-artefact register state (current baseline, latest registered session and its status).
- Guardian's Voice faculty, Phase 6, both increments are now implemented and live-verified: speech output (Increment A, self-hosted TTS wired into the UXP's speak button at ESR-0044; production provider is now Kokoro, `bm_george`/`bf_isabella` fallback, replacing Piper at ESR-0053) and speech input (Increment B, self-hosted `faster-whisper` STT, push-to-talk mic button gated on real-time capability detection, ESR-0047); the Local Agent Permission Boundary is defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, ESR-0041) - the prerequisite gate for the still-unimplemented Action faculty. Guardian's Persona has also been refined toward its classic characterisation (ESR-0043), and configuration/secrets practice is now formalised in [[STD-0006_CONFIGURATION_AND_SECRETS_STANDARD|STD-0006]] (ESR-0045).
- User Identity and Profile Foundation (`jarvis/identity/`) is implemented and live-verified (ESR-0046) - local, unauthenticated profile create/list/select, role-tagged against GAM-0001 Section 8.1's four household roles, reachable through a real UXP profile picker. Credentialed authentication, memory scoping by profile and enforcement of the roles' differing authority remain not implemented, deliberately deferred to later work.
- [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] is the current accepted repository baseline, established at ESR-0056 (esbuild/vite Security Upgrade; DRA-0001 Device Bootstrap and Restore Architecture, a new Platform Services model, Draft, covering device bootstrap/registry/sync-protocol/progressive-restore requirements ADR-0012 anticipated and MDS-0001 explicitly deferred).
- Agent Framework Phase 3 (EBG-0119) is implemented (ESR-0049), building real code against the contract [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] scoped at ESR-0048: `jarvis/agents/` (`SpecialistAgent` contract), GIA's read-only observability wired as the first live specialist agent through the mandatory shared Sentinel gate, classified `ROUTINE_INTERACTION`. Agent Framework UXP Wiring (EBG-0120, ESR-0050) makes it invokable live through the UXP - two new Tauri commands, a live capability-sidebar row, a new `AgentFrameworkPanel`. `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remains untouched - no local-device-control agent implemented, wired, or authorised.
- Sentinel's real trust-gateway/platform-entry-validation pattern is now properly documented (ESR-0050, EBG-0047): [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] registered as a controlled artefact for the first time, corrected a factual error (wrong production trust-policy default), and gained a new Sentinel Gate of Durin subsection.
- Session/Shared-Family memory tiers, credentialed profile authentication, role-authority enforcement, the wider Action faculty (local device/system control), Vision, Provider Framework completion, Conversation Engine expansion, EAC and GDP-0001 implementation, and GIA Phase 2 and 4 remain deferred.
- No session is currently open; [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] is the latest closed session.

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
| [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] | Current accepted repository baseline, established at ESR-0056 (esbuild/vite Security Upgrade; DRA-0001 Device Bootstrap and Restore Architecture). |
| [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] | Latest closed engineering session (four Work Packages), opened at the Programme Sponsor's direct request following an instruction to read PBK-0001. WP1 closed EBG-0085 (esbuild/vite dev-server vulnerability upgrade); WP2 re-verified EBG-0058 (already Complete) and fixed JRM-0001 staleness; WP3 created [[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]] (Draft), narrowing EBG-0046's scope to the genuine gap once MDS-0001's coverage was accounted for; WP4 fixed a second JRM-0001 staleness cluster (REG-0001 HST/FCH gap, already resolved since ESR-0028). Session-wide WP6 genuine background Codex review - Pass, no blocking findings. WP7 Establish - RBL-0036 accepted. |
| [[ESR-0055_ENGINEERING_SESSION_REPORT|ESR-0055]] | One Work Package, opened at the Programme Sponsor's direct request following an explicit instruction to read PBK-0001 (initially mislabelled ESR-0054, corrected once flagged as already closed). WP1 resolved the remainder of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0083 Phase 3 per [[EIP-ESR0055-001_GIA_PHASE3BC_REPOSITORY_HEALTH_AND_REGISTER_STATE|EIP-ESR0055-001]] - `gia.engineeringStatus` and `gia-engineering` extended with repository validation health and register-state fields, completing EBG-0083 Phase 3 in full. Session-wide WP6 genuine background Codex review - Pass, no corrective findings. WP7 Establish - RBL-0035 accepted; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0054_ENGINEERING_SESSION_REPORT|ESR-0054]] | Two Work Packages, opened at the Programme Sponsor's direct request following an explicit instruction to read PBK-0001. WP1 closed [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0038 (Formal AIEMS Standards Review) `Complete` - a relevance check found no new standard warranted, the underlying need already met organically by other artefacts. WP2 resolved the first slice of EBG-0083 Phase 3 per [[EIP-ESR0054-002_GIA_PHASE3A_GIT_STATE_OBSERVABILITY|EIP-ESR0054-002]] - a new `gia.engineeringStatus` RPC method and `gia-engineering` specialist agent, the first concrete step of a staged path toward JARVIS/Guardian/Sentinel self-awareness and future engineering assistance discussed with the Programme Sponsor. Session-wide WP6 genuine background Codex review - Pass, no findings. WP7 Establish - RBL-0034 accepted; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0053_ENGINEERING_SESSION_REPORT|ESR-0053]] | Two Work Packages, opened at the Programme Sponsor's direct request. WP1 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0106 per [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] - retired EBR-0001 Section 5A's hand-maintained, twice-stale-drifted snapshot in favour of an on-demand Priority-grouped view generated by `scripts/session_launcher.py`; WP2 resolved EBG-0125 per [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]] - a real live UK-voice comparison, Programme Sponsor selected `bm_george`/`bf_isabella` fallback, Kokoro wired into production replacing Piper outright, live-verified against the real engine. Session-wide WP6 genuine background Codex review - Pass, no findings. WP7 Establish - RBL-0033 accepted; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] | Three Work Packages, opened at the Programme Sponsor's direct request for a technology/code/AI-practice review ([[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]], Codex cross-reviewed, plus a reconciled ad hoc second opinion). WP1 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0122 through EBG-0124 (process/tooling currency cluster) per [[EIP-ESR0052-001_PROCESS_TOOLING_CURRENCY_CLUSTER|EIP-ESR0052-001]]; WP2 investigated and Deferred EBG-0111 (Composio - self-hosted-first/no-discretionary-budget conflict, verified via web search); WP3 resolved EBG-0115 (Kokoro TTS) per [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] - a genuine live comparison, Programme Sponsor preferred Kokoro over Piper, EBG-0125 registered for follow-on production wiring with a British voice (delivered at ESR-0053). Session-wide WP6 genuine background Codex review - Conditional Pass with correction (a review-request diff-boundary mistake, no actual scope creep). WP7 Retain - RBL-0032 unchanged; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] | Two Work Packages, opened after a ~2-week gap at the Programme Sponsor's request for a full project review ([[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]], Codex cross-reviewed). WP1 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0090 through EBG-0096 (process/tooling backlog cluster) per [[EIP-ESR0051-001_PROCESS_TOOLING_BACKLOG_CLUSTER|EIP-ESR0051-001]] - a real Claude↔Codex automated review round trip proven end to end, streamlined Sponsor approval, installer/status-check/auto-start scripts; WP2 resolved EBG-0121 (Guardian Orb Phase 2: Cluster Illumination) per [[EIP-ESR0051-002_GUARDIAN_ORB_PHASE2_CLUSTER_ILLUMINATION|EIP-ESR0051-002]] - real backend RPC activity now illuminates the Orb and Active Clusters panel. Session-wide WP6 genuine background Codex review - Pass, no blocking findings. WP7 Establish - RBL-0032 accepted; retained for lineage, no longer the latest closed session. |
| [[ESR-0050_ENGINEERING_SESSION_REPORT|ESR-0050]] | Three Work Packages: WP1 PCB-0001/Capability Matrix content refresh for Agent Framework Phase 3; WP2 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0120 (Agent Framework UXP Wiring) per [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]] - `gia-observability` now invokable live through the UXP; WP3 resolved EBG-0047 (Sentinel Gate of Durin Architecture Specification) per [[EIP-ESR0050-002_CURRENT_ARCHITECTURE_REFRESH_AND_GATE_OF_DURIN_DETAIL|EIP-ESR0050-002]] - CURRENT_ARCHITECTURE.md registered as a controlled artefact for the first time. Session-wide WP6 genuine background Codex review - Pass, no findings. WP7 Establish - RBL-0031 accepted; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] | Two Work Packages: WP1 Documentation Debt Discipline fix (COC-0001's stale baseline reference); WP2 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0119 (Agent Framework Phase 3: First Specialist Agent Implementation) per [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] - real `jarvis/agents/` module, GIA wired as the first live `ROUTINE_INTERACTION` specialist agent, two new `guardian.agent.*` RPC methods. Session-wide WP6 genuine background Codex review - Pass, no findings. WP7 Establish - RBL-0030 accepted; retained for lineage, no longer the latest closed session or latest baseline. |
| [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] | Two Work Packages: WP1 Documentation Debt Discipline sync, following ESR-0047 WP4's handover; WP2 resolved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0042 (Agent Framework Architecture) per [[EIP-ESR0048-001_AGENT_FRAMEWORK_ARCHITECTURE_SCOPE|EIP-ESR0048-001]] - new [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] "Agent Framework" subsection, architecture only. Session-wide WP6 genuine background Codex review - Pass, no findings. WP7 Retain - RBL-0029 unchanged; retained for lineage, no longer the latest closed session. |
| [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] | Four Work Packages plus a WP6-caught fix round: WP1 Documentation Debt Discipline; WP2 EBG-0118 investigated (inconclusive, remains open); WP3 EBG-0117 (Voice Faculty Increment B, Speech Input) resolved per [[EIP-ESR0047-001_VOICE_PHASE6_INCREMENT_B_SPEECH_INPUT_SCOPE|EIP-ESR0047-001]] - self-hosted `faster-whisper` STT, push-to-talk mic button; WP4 Repository Engineering Health Review (advisory). Session-wide WP6 caught a real mic-button capability-gating defect on first pass (Fail), fixed directly, re-reviewed Pass with no findings. WP7 Establish - RBL-0029 accepted. Both LGB-0001 Must-Ship items now resolved; retained for lineage, no longer the latest closed session. |
| [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] | One Work Package: WP1 EBG-0116 (User Identity and Profile Foundation) resolved per [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] - `jarvis/identity/` module, four new `profile.*` RPC methods, real UXP profile picker. Session-wide WP6 performed directly (EBG-0118, local Codex CLI tooling stall), WP7 Establish - RBL-0028 (superseded by RBL-0029 at ESR-0047); retained for lineage, no longer the latest closed session. |
| [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] | Five Work Packages: EBG-0065 (STD-0006 Configuration and Secrets Standard) resolved at WP1; a Documentation Debt Discipline sweep of this README and PST-0001 at WP2; PCB-0001 refreshed at WP3; RSC-0001 (v1.0 Readiness Scorecard) created at WP4; LGB-0001 (Launch Gap Backlog) created at WP5, registering EBG-0116/EBG-0117 (both now resolved). Session-wide WP6 Pass, WP7 Retain - RBL-0027 retained (superseded by RBL-0028, then RBL-0029); retained for lineage, no longer the latest closed session. |
| [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] | EBG-0114 (Guardian Voice faculty wired into the live JSON-RPC bridge, Tauri bridge and UXP speak button) delivered and live-verified across all three layers; retained for lineage. |
| [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] | Guardian Persona refined toward its classic JARVIS characterisation, recorded in AAM-0001. |
| [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]] | EBG-0021 (Local Agent Permission Boundary) resolved via a new GAM-0001 Section 8A - defines the boundary a future Local Agent/Action faculty implementation must obey. Architecture/policy-definition only, no code changed; retained for lineage. |
| [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] | Guardian's first Voice faculty capability (EBG-0112 Increment A, speech output only via self-hosted Piper local TTS) delivered and live-verified; retained for lineage. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Closure review package for Guardian Platform Foundation implementation and Programme Sponsor closure decision. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source for selecting future engineering packages. |
| [[STD-0006_CONFIGURATION_AND_SECRETS_STANDARD|STD-0006]] | Configuration and Secrets Standard - formalises environment-variable-only credential supply and the agent-accessible/Sponsor-only token boundary. |
| [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] | v1.0 Readiness Scorecard - pass/fail assessment of JARVIS against the eight MLP 0.1 items. |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Launch Gap Backlog - splits RSC-0001's scored gaps into Must-Ship vs Defer. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Authoritative JARVIS product architecture. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability maturity and prioritisation support. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 3.39 | 4 September 2026 | Claude Engineering Implementer | ESR-0056 formally closed. RBL-0036 established (esbuild/vite Security Upgrade; DRA-0001 Device Bootstrap and Restore Architecture, a genuine new backend/architecture artefact), superseding RBL-0035. Top Project Status table, GIA-adjacent bullets, Related Artefacts table (new ESR-0056 row, ESR-0055 row reworded to lineage-only) and "latest closed session"/"no session currently open" references updated. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.38 | 28 August 2026 | Claude Engineering Implementer | ESR-0055 formally closed. RBL-0035 established (GIA Phase 3b/3c: Repository Health and Register State Observability, completing EBG-0083 Phase 3 in full - a genuine new backend capability), superseding RBL-0034. Top Project Status table, GIA/GIA-Phase bullets (Repository Structure summary and Phase 2 Current Roadmap focus), Related Artefacts table (new ESR-0055 row, ESR-0054 row reworded to lineage-only) and "latest closed session"/"no session currently open" references updated. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.37 | 28 August 2026 | Claude Engineering Implementer | ESR-0054 formally closed. RBL-0034 established (EBG-0038 Relevance Check; GIA Phase 3a Git State Observability - JARVIS's first real read access to its own repository git state, a genuine new backend capability), superseding RBL-0033. Top Project Status table, GIA/GIA-Phase bullets (Repository Structure summary and Phase 2 Current Roadmap focus), Related Artefacts table (new ESR-0054 row) and "latest closed session"/"no session currently open" references updated. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.36 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 formally closed. RBL-0033 established (Active Backlog View Generation; Kokoro Production Voice Wiring - Guardian's production speech provider changed from Piper to Kokoro, a genuine live product-capability change), superseding RBL-0032. Top Project Status table, Guardian Voice bullets (both instances - Repository Structure summary and Phase 2 Current Roadmap focus), Related Artefacts table (new ESR-0053 row) and two stale "latest closed session"/"no session currently open" references (Phase 2 focus, found stale since ESR-0052's own closure predated this edit) updated. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.35 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 formally closed. Top Project Status table, Guardian Voice bullet (new `sentinel/kokoro_provider.py` adapter noted, not yet wired into production) and Related Artefacts table updated to reflect no session currently open, RBL-0032 retained (not superseded - this session's real code changes do not change live product behaviour). No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.34 | 22 August 2026 | Claude Engineering Implementer | ESR-0051 formally closed. Top Project Status table, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect no session currently open, RBL-0032 current. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.33 | 22 August 2026 | Claude Engineering Implementer | ESR-0051 WP7: RBL-0032 established (Process/Tooling Backlog Cluster; Guardian Orb Phase 2 Cluster Illumination - a genuine live product-capability change), superseding RBL-0031. Top Project Status table, JARVIS Development/Guardian Experience bullets, Related Artefacts table (new ESR-0051 row) updated to reflect ESR-0051 open (WP1/WP2 complete, session-wide WP6 Pass, WP7 Establish) and RBL-0032 current. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.32 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 formally closed. Top Project Status table, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect no session currently open, RBL-0031 current. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.31 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP7: RBL-0031 established (Agent Framework UXP Wiring; Sentinel Gate of Durin Architecture Specification - a genuine live product-capability change), superseding RBL-0030. Top Project Status table, JARVIS Development/Platform Architecture bullets, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect ESR-0050 open (WP1-WP3 complete, session-wide WP6 Pass, WP7 Establish) and RBL-0031 current - including the new ESR-0050 Related Artefacts row and the stale "no UXP surface for it yet" claim (superseded by WP2's own delivery within this same session). No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.30 | 5 August 2026 | Claude Engineering Implementer | ESR-0049 formally closed. Top Project Status table, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect no session currently open, RBL-0030 current. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.29 | 5 August 2026 | Claude Engineering Implementer | ESR-0049 WP7: RBL-0030 established (Agent Framework Phase 3, First Specialist Agent - a genuine live product-capability change), superseding RBL-0029. Top Project Status table, JARVIS Development/Platform Architecture bullets, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect ESR-0049 open (WP1-WP2 complete, session-wide WP6 Pass, WP7 Establish) and RBL-0030 current. Whole-Document Staleness Sweep on Edit (PBK-0001): the "no session currently open" claim, stale since ESR-0049 opened, corrected in the same pass rather than deferred. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.28 | 4 August 2026 | Claude Engineering Implementer | ESR-0048 formally closed. Two Work Packages: WP1 Documentation Debt Discipline sync (following ESR-0047 WP4's handover); WP2 EBG-0042 (Agent Framework Architecture) resolved - new MOD-0001 "Agent Framework" subsection, architecture only, no agent implemented. Session-wide WP6 (genuine background Codex review of the full session diff) Pass, no findings. WP7 Retain RBL-0029 - documentation/architecture-only session, no code touched. Top Project Status table, JARVIS Development/Platform Architecture bullets, Capability Roadmap Phase 2 focus and Related Artefacts table updated to reflect no session currently open, RBL-0029 retained. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
| 3.27 | 4 August 2026 | Claude Engineering Implementer | ESR-0047 formally closed. Four Work Packages: WP1 Documentation Debt Discipline; WP2 EBG-0118 investigated (inconclusive); WP3 EBG-0117 (Voice Faculty Increment B, Speech Input) resolved; WP4 Repository Engineering Health Review (advisory). Session-wide WP6 caught a real mic-button capability-gating defect on first pass, fixed, re-reviewed Pass. WP7 Establish RBL-0029, superseding RBL-0028. Top Project Status table, JARVIS Development/implementation bullets, Capability Roadmap table, Key Engineering Artefacts and Related Artefacts tables and Phase 2 Current Roadmap focus updated to reflect no session currently open, RBL-0029 current. Automated-test count updated 453 to 485 passed/1 skipped. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.26 | 31 July 2026 | Claude Engineering Implementer | ESR-0046 formally closed (Programme Sponsor direction, concerned about a Codex CLI tooling stall disrupting the post-commit review step - EBG-0118). Session-wide WP6 (performed directly, Codex unavailable) and WP7 (Establish RBL-0028, superseding RBL-0027) complete. Top Project Status table, JARVIS Development bullets, Key Engineering Artefacts and Related Artefacts tables and Phase 2 Current Roadmap focus updated to reflect no session currently open, RBL-0028 current. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.25 | 31 July 2026 | Claude Engineering Implementer | ESR-0046 WP1: resolved EBG-0116 (User Identity and Profile Foundation) per [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] - new `jarvis/identity/` module, four new `profile.*` RPC methods, real UXP profile picker replacing the static "Robert" placeholder. Top Project Status table, JARVIS implementation bullets, Capability Roadmap table, Key Engineering Artefacts table (added GAM-0001), Related Artefacts table (added ESR-0046) and Phase 2 Current Roadmap focus updated to reflect ESR-0046 open, WP1 complete. Automated-test count updated 424 to 453 passed/1 skipped. No governance artefact content changed beyond this session's own delivery; PST-0001 remains the authoritative source this README summarises. |
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
| 3.18 | 19 July 2026 | Claude Engineering Implementer | ESR-0030 WP0A post-commit fix (Codex finding): the top Project Status table had been corrected to ESR-0029/RBL-0017 but Current Focus and Related Artefacts still described ESR-0026/RBL-0015 as current, and Current Focus's memory/GIA bullets were separately stale (Personal Memory implemented at ESR-0027, GIA Phase 1 implemented at ESR-0029, neither reflected). All corrected to the current ESR-0029/RBL-0017 state. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.17 | 18 July 2026 | Claude | Direct Programme Sponsor-requested correction (outside an open ESR): README had drifted 13 sessions stale (last describing ESR-0013 while the repository was at ESR-0026 / RBL-0015 / PST-0001 v2.48). Refreshed Project Status, JARVIS implementation summary, Repository Structure, Capability Roadmap, Phase 2 focus, launch guidance (added Tauri + React Guardian Desktop Platform Shell alongside First Light) and Related Artefacts to match current repository state. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.19 | 25 July 2026 | Claude Engineering Implementer | ESR-0033 WP1 (Documentation Debt Discipline): corrected stale ESR-0029/RBL-0017 references (top Project Status table, Current Roadmap Phase 2 bullets, Related Artefacts, and a further missed RBL-0010 reference in the Key Engineering Artefacts table - Codex pre-implementation review finding, addressed) to ESR-0032/RBL-0019, and updated the "no session currently open" claims to reflect ESR-0033 now open - three sessions and two accepted baselines stale, found during ESR-0033 WP0A repository synchronisation. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.21 | 26 July 2026 | Claude Engineering Implementer | ESR-0036 WP2 (Documentation Debt Discipline, deferred to the last engineering Work Package before session closure by Programme Sponsor direction rather than run first): corrected stale ESR-0034/RBL-0020 references (top Project Status table, Current Roadmap Phase 2 bullets, Related Artefacts, Key Engineering Artefacts table) to ESR-0035/RBL-0021, and updated the "ESR-0035 currently open" claims to reflect ESR-0036 now open. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.20 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP1 (Documentation Debt Discipline): corrected stale ESR-0032/RBL-0019 references (top Project Status table, Current Roadmap Phase 2 bullets, Related Artefacts, Key Engineering Artefacts table) to ESR-0034/RBL-0020, and updated the "ESR-0033 currently open" claims to reflect ESR-0035 now open - two sessions and one accepted baseline stale, found during ESR-0035 WP0A repository synchronisation. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.22 | 30 July 2026 | Claude Engineering Implementer | Direct Programme Sponsor-requested correction (outside an open ESR, following ESR-0041 closure). Whole-document staleness sweep (PBK-0001): README had drifted 5 sessions/4 baselines stale (last describing ESR-0036 open / RBL-0021, while the repository was at ESR-0041 closed / RBL-0025) - top Project Status table, Related Artefacts and Key Engineering Artefacts table corrected. Also caught and corrected staleness predating this drift: the automated-test count (254, stale since well before ESR-0027) corrected to 418 passed/1 skipped; the "persistent memory, voice... not started" JARVIS Development/implementation claims (stale since ESR-0027's Personal Memory and ESR-0040's Voice Increment A) corrected to reflect Guardian Cognitive Core, Personal Memory and Voice Phase 6 Increment A as implemented, and the new Local Agent Permission Boundary (GAM-0001 Section 8A, ESR-0041) as defined. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.24 | 30 July 2026 | Claude Engineering Implementer | ESR-0045 formally closed (five Work Packages: STD-0006, documentation debt sweep, PCB-0001 refresh, RSC-0001 v1.0 Readiness Scorecard, LGB-0001 Launch Gap Backlog; session-wide WP6 Pass, WP7 Retain RBL-0027). Top Project Status table, JARVIS Development capability bullets, Key Engineering Artefacts table (added RSC-0001/LGB-0001), Related Artefacts table and Phase 2 Current Roadmap focus updated to reflect no session currently open. No governance artefact content changed; PST-0001 remains the authoritative source this README summarises. |
| 3.23 | 30 July 2026 | Claude Engineering Implementer | ESR-0045 WP2 (Documentation Debt Discipline sweep), prompted by an independent Codex governance/v1.0-readiness gap analysis (`govreview`/`v1_0_gap_analysis`) found in the AIEMS Exchange Bridge inbox, which flagged README and PST-0001 as out of sync with the repository's actual current session/baseline. README had drifted 4 sessions/2 baselines stale (last describing ESR-0041 closed / RBL-0025, while the repository was at ESR-0045 open / RBL-0027) - top Project Status table, JARVIS Development capability bullets, automated-test count (418 -> 424 passed/1 skipped, reverified live), Key Engineering Artefacts table (added STD-0004 and STD-0006, both previously missing), Phase 2 Current Roadmap focus and Related Artefacts table all corrected. PST-0001 (3.17 to 3.18) and REG-0001 (3.436 to 3.437) were corrected in the same Work Package - PST-0001 remains the authoritative source this README summarises. |
