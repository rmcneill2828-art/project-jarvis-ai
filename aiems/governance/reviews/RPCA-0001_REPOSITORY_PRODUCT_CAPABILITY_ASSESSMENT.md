# RPCA-0001 - Repository Product Capability Assessment

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RPCA-0001 |
| Title | Repository Product Capability Assessment |
| Version | 1.0 |
| Status | Implementation Complete |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] |
| Repository Baseline | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Classification | Internal |
| Date | 1 July 2026 |

---

# 2. Purpose

RPCA-0001 establishes what JARVIS can currently do based on executable repository evidence.

This assessment supports future creation of PCB-0001 Product Capability Baseline by distinguishing implemented, tested, operationally validated, planned and missing capability.

---

# 3. Scope

This assessment reviews:

1. Current branch and HEAD commit.
2. JARVIS executable entry points.
3. GUI capability.
4. Conversation capability.
5. Provider capability.
6. Session tracking.
7. Transcript model.
8. Transcript export.
9. Service status and health reporting.
10. Tests.
11. Documentation alignment.
12. Gaps between product architecture and implementation.

Executable repository evidence is treated as authoritative. ESR history and controlled documentation are treated as supporting evidence.

---

# 4. Repository Baseline Reviewed

| Item | Evidence |
|------|----------|
| Branch reviewed | `main` |
| HEAD commit before implementation | `b3d3d12964160cd78a221737d8a298b5327dd4e5` |
| Accepted baseline context | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Active engineering session | [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] |
| Programme context | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Product architecture context | [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] |
| Capability maturity context | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] |

Files reviewed for executable evidence:

- `README.md`
- `pyproject.toml`
- `jarvis/__main__.py`
- `jarvis/app.py`
- `jarvis/__init__.py`
- `jarvis/core/jarvis.py`
- `jarvis/gui/app.py`
- `jarvis/interfaces/conversation.py`
- `jarvis/services/model.py`
- `jarvis/services/status.py`
- `jarvis/tests/test_jarvis.py`
- `jarvis/tests/test_public_api.py`
- `jarvis/tests/test_conversation.py`

Files reviewed for documentation alignment:

- `aiems/governance/baselines/RBL-0007_REPOSITORY_BASELINE.md`
- `aiems/governance/sessions/ESR-0007_ENGINEERING_SESSION_REPORT.md`
- `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
- `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
- `aiems/standards/STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD.md`
- `aiems/standards/STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD.md`
- `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md`
- `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`

---

# 5. Executive Summary

JARVIS currently has an implemented and tested First Light / Conversation Workspace foundation.

The repository supports launching JARVIS through `python -m jarvis` and through the packaged `jarvis` console script declared in `pyproject.toml`. The executable path starts the root `Jarvis` lifecycle object, opens a Tkinter GUI, displays an animated orb, provides a conversation text interface, exposes service status, records in-memory conversation exchanges and supports user-initiated transcript export to Markdown or plain text.

The current conversation capability is deterministic and local. It is not an external AI provider integration. Provider capability exists as a lightweight protocol and orchestrator pattern with one implemented provider named `deterministic-local`.

Service status reporting is implemented and tested at a static product-service level. Service health and capability declarations exist in the service model and tests, but runtime health checks, diagnostics, restart guidance and historical monitoring are not implemented.

The product architecture in [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] is broader than the current implementation. The current implementation partially satisfies the GUI, chat, text response, avatar/orb, session memory, transcript and service status foundation. Voice, vision, long-term memory, family profiles, Guardian, local agent, internet capability, plugin management and multi-device capability remain planned or missing.

No rebuild of delivered First Light capability is recommended. The appropriate next work is extension, validation and hardening of the existing foundation through approved work packages tracked against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].

---

# 6. Verified Product Capabilities

| Capability | Status | Evidence | Assessment |
|------------|--------|----------|------------|
| Python package structure | Implemented / Tested | `pyproject.toml`, `jarvis/__init__.py`, `jarvis/tests/test_public_api.py` | Package discovery and public API exports exist. |
| Executable module entry point | Implemented | `jarvis/__main__.py`, `jarvis/app.py` | `python -m jarvis` calls `jarvis.app.main`. |
| Console script entry point | Implemented | `pyproject.toml` | `jarvis = "jarvis.app:main"` is declared. |
| Root lifecycle object | Implemented / Tested | `jarvis/core/jarvis.py`, `jarvis/tests/test_jarvis.py` | `Jarvis` starts, stops and reports `STOPPED` or `RUNNING`. |
| GUI workspace | Implemented | `jarvis/gui/app.py` | Tkinter application with header, orb, conversation panel, controls and service status panel exists. |
| Animated orb | Implemented | `jarvis/gui/app.py` | Canvas oval animation is implemented through `after`. |
| Conversation text input | Implemented | `jarvis/gui/app.py` | Entry field, return binding and send button route messages to `ConversationService`. |
| Deterministic text response | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Non-empty messages return the local default response. |
| Empty message handling | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Empty input receives a distinct listening response and is recorded as an exchange. |
| Provider protocol | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | `ConversationProvider` protocol, orchestrator and deterministic provider exist. |
| External AI provider integration | Missing | Repository evidence | No external provider client, configuration or network-backed generation is implemented. |
| Session tracking | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Session ID, provider name and exchange count are available through metadata. |
| New conversation | Implemented / Tested | `jarvis/gui/app.py`, `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | New session resets transcript and updates metadata. |
| Clear conversation | Implemented / Tested | `jarvis/gui/app.py`, `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Transcript can be cleared while preserving session ID. |
| Transcript model | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Exchanges include sequence number, user message, JARVIS response, provider and UTC timestamp. |
| Transcript snapshot | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Transcript is returned as an immutable tuple snapshot. |
| Transcript export | Implemented / Tested | `jarvis/gui/app.py`, `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Markdown and plain-text exports are supported and unsupported formats raise `ValueError`. |
| Service status display | Implemented / Tested | `jarvis/core/jarvis.py`, `jarvis/gui/app.py`, `jarvis/tests/test_jarvis.py` | Core and Conversation report Online; Memory, Voice, Vision and Internet report unavailable or offline states. |
| Service health model | Implemented / Tested | `jarvis/services/model.py`, `jarvis/services/status.py`, `jarvis/tests/test_jarvis.py` | Service health enum, model and capability checks exist. |
| Runtime health checks | Missing | Repository evidence | No active probes, service diagnostics, health history or recovery workflow exists. |
| Basic conversation memory | Implemented / Tested | `jarvis/interfaces/conversation.py`, `jarvis/tests/test_conversation.py` | Current-session exchange history exists in memory only. |
| Persistent memory | Missing | Repository evidence | No storage-backed memory, user profiles or family memory implementation exists. |
| Operational validation | Operationally validated in ESR history / Requires current-session confirmation | `README.md`, [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Documentation records Conversation Workspace operational validation; this RPCA did not launch the GUI. |

---

# 7. Capability Evidence Table

| Product Area | Implemented | Tested | Operationally Validated | Planned | Missing |
|--------------|-------------|--------|--------------------------|---------|---------|
| Executable launch | `python -m jarvis`; package script declaration | Import and lifecycle tests indirectly support package viability | First Light / Conversation Workspace recorded as operational in [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Packaging hardening | Installer, release packaging, launch diagnostics |
| GUI | Tkinter workspace, orb, conversation controls, export buttons, status panel | No automated GUI tests | Recorded as operational in repository documentation | GUI evolution roadmap in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Accessibility validation, layout tests, richer dashboard |
| Conversation | Local deterministic exchange flow | Unit tests cover response path and metadata | Recorded as operational First Light | Rich conversation orchestration | External AI-backed responses, tool use, planning |
| Provider | Protocol, orchestrator and deterministic provider | Unit tests cover deterministic provider and routing | Not separately operationally validated | Provider abstraction architecture is candidate backlog | External provider adapters, model selection, provider configuration |
| Session tracking | Session ID, provider name, exchange count | Unit tests cover metadata and reset behaviour | Exposed in GUI metadata | Runtime chat archive candidate backlog | Persistent sessions and default archive workflow |
| Transcript model | In-memory exchange dataclass with timestamp and provider | Unit tests cover transcript content and snapshot behaviour | GUI displays conversation; export supported | Archive workflow enhancement is candidate backlog | Persistent transcript repository and retention policy |
| Transcript export | Markdown and text export through service and GUI save dialog | Unit tests cover export format content and invalid format handling | Prototype export artefacts classified in [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | EBG-0026 and EBG-0039 | Default save location, auto naming, runtime archive |
| Service status | Static service status map and GUI status panel | Unit tests cover initial service states and update operation | Status panel is part of Conversation Workspace | Service monitor expansion in architecture | Runtime probes, degradation handling, restart guidance |
| Memory | Current-session transcript memory only | Unit tests cover session transcript | Not validated as persistent memory | Memory and data storage architecture candidate backlog | Long-term memory, profiles, consent controls |
| Voice | Status placeholder only | Status test confirms unavailable state | Not operationally validated | Product architecture MLP capability | Voice input/output implementation |
| Vision | Status placeholder only | Status test confirms unavailable state | Not operationally validated | Product roadmap capability | Visual understanding implementation |
| Internet | Offline placeholder only | Status test confirms offline state | Not operationally validated | Controlled internet capability roadmap | Internet-backed assistance |
| Guardian | Package placeholder only | No tests | Not operationally validated | Guardian architecture candidate backlog | Permissions, safety, audit and approval controls |

---

# 8. Tests and Validation Evidence

The repository contains executable tests under `jarvis/tests`.

Validated test areas:

- Public API exports for `Jarvis`, `JarvisState`, `JarvisService`, `ServiceHealth` and `ServiceStatus`.
- Lifecycle start, stop and initial state.
- Initial service statuses for Core, Conversation, Memory, Voice, Vision and Internet.
- Service status update through `register_service`.
- Service health and capability declarations.
- Deterministic conversation response.
- Empty-message response.
- Provider routing through `ConversationOrchestrator`.
- Conversation exchange metadata and UTC timestamp presence.
- Transcript snapshot behaviour.
- Clear conversation and new conversation behaviours.
- Markdown transcript export.
- Plain-text transcript export.
- Unsupported transcript export format handling.

Validation status:

| Check | Result |
|-------|--------|
| Test suite present | Pass |
| Conversation tests present | Pass |
| Lifecycle tests present | Pass |
| Public API tests present | Pass |
| GUI automated tests present | Not Started |
| External provider tests present | Not Applicable / Missing capability |
| Persistent memory tests present | Not Applicable / Missing capability |
| Runtime health probe tests present | Not Applicable / Missing capability |

Validation standards context is provided by [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] and [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]].

---

# 9. Documentation Alignment

Documentation alignment is broadly consistent with executable evidence.

Aligned documentation:

- `README.md` states that JARVIS can be launched with `python -m jarvis`.
- `README.md` describes an operational First Light Conversation Workspace with deterministic offline chat, session metadata and transcript export.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] records JARVIS development as early and product capabilities as foundation-level.
- [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] identifies Conversation as partial and most other capabilities as planned or not started.
- [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] correctly frames ESR-0007 as a return to product engineering rather than already-approved capability expansion.

Documentation requiring careful interpretation:

- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] describes the intended MLP 0.1 capability set. It should not be read as evidence that all MLP capabilities are implemented.
- Service capability strings in `jarvis/core/jarvis.py` include future-facing names for unavailable services. These are status declarations, not implemented runtime capability.
- `README.md` says "Operational First Light / Conversation Workspace"; this is accurate for the implemented foundation but should not be interpreted as mature conversational AI.

---

# 10. Product Gaps

The following gaps exist between product architecture and implementation.

| Gap | Current State | Required Future Direction |
|-----|---------------|---------------------------|
| AI provider abstraction | Lightweight protocol and deterministic provider only | Define architecture before external provider integration, aligned with [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]. |
| External AI responses | Missing | Add provider-backed generation through approved provider architecture. |
| Persistent memory | Missing | Define memory, storage, privacy and consent boundaries before implementation. |
| Family profiles | Missing | Define user model, permissions and privacy boundaries. |
| Voice | Missing beyond unavailable service status | Implement basic voice input only after architecture and validation scope are approved. |
| Vision | Missing beyond unavailable service status | Treat as future visual understanding capability. |
| Guardian | Missing beyond package placeholder and architecture intent | Define Guardian safety, permission, approval and audit boundaries before implementation. |
| Internet capability | Missing beyond offline service status | Define controlled internet capability, approval boundaries and provider strategy. |
| Local agent | Missing | Define local device control permission boundary before implementation. |
| Plugin manager | Missing | Keep as future extensibility capability until product need justifies it. |
| Runtime health checks | Missing | Extend service status model with active health probes and diagnostics. |
| GUI validation | Manual / historical only | Add GUI-level validation approach appropriate to Tkinter. |
| Transcript archive workflow | Partial export only | Extend existing export rather than rebuild it; address default location and naming through approved backlog work. |

---

# 11. Risks and Observations

| Type | Observation | Impact |
|------|-------------|--------|
| Risk | Architecture breadth may be mistaken for delivered capability. | Product baseline could overstate maturity unless implementation evidence remains authoritative. |
| Risk | Provider protocol exists but external provider architecture is not defined. | Premature provider integration could create avoidable coupling. |
| Risk | Current transcript storage is in memory only. | Sessions are lost unless explicitly exported. |
| Risk | GUI capability lacks automated tests. | Regression confidence for user-facing workflow remains limited. |
| Risk | Service status is static. | Users can see intended availability states, but not active runtime health. |
| Observation | First Light capability should be extended, not rebuilt. | Existing launch, GUI, conversation, session and export foundations provide usable product base. |
| Observation | Documentation already distinguishes early implementation maturity. | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] supports accurate baseline framing. |

---

# 12. Recommended Next Engineering Work

Recommended next work should extend, validate or harden delivered First Light capability.

1. Create PCB-0001 using RPCA-0001 as repository evidence input.
2. Progress transcript archive workflow from existing export capability, aligned with EBG-0026 and EBG-0039 in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].
3. Define JARVIS provider abstraction architecture before adding any external AI provider.
4. Define memory and data storage architecture before implementing persistent or family memory.
5. Add GUI validation appropriate to the Tkinter workspace.
6. Extend service status toward active health checks and diagnostic reporting.
7. Maintain the existing First Light / Conversation Workspace as the foundation for future vertical capability increments.

No recommendation is made to rebuild the existing First Light executable, GUI shell, deterministic conversation path, transcript model or export capability.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Accepted repository baseline context for ESR-0007. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Active engineering session context for product capability assessment. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status and current product engineering position. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product vision and target capability architecture assessed against repository evidence. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Existing capability maturity view compared with executable evidence. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source for recommended future work. |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Software engineering standard relevant to implementation evidence. |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Validation standard relevant to RPCA evidence and checks. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 July 2026 | Codex Engineering Implementer | Initial repository product capability assessment created for ESR-0007 WP1, based on executable repository evidence and OSE verified links. |
