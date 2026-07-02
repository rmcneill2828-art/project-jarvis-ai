# JARVIS Product Architecture

---

# 1. Document Control

| Field | Value |
|------|-------|
| Document ID | JARVIS-PRODUCT-ARCHITECTURE |
| Title | JARVIS Product Architecture |
| Version | 1.3 |
| Status | Approved Product Architecture |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Product | JARVIS OS |
| Framework | Project JARVIS AI |
| Classification | Internal |
| Effective Date | 29 June 2026 |

---

# 2. Vision Statement

JARVIS OS is a modular, family-friendly AI Operating System designed to provide personalised intelligent assistance across multiple devices while remaining secure, extensible and human-controlled.

JARVIS OS is the flagship product of Project JARVIS AI.

AIEMS governs engineering. JARVIS OS is the product that demonstrates those engineering principles through practical, useful and enjoyable capability. The platform-level architecture context is recorded in [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].

The product vision is to create a trusted AI companion for everyday family life: helpful in conversation, useful for household tasks, respectful of privacy, safe for children, and capable of growing into a broader intelligent operating environment over time.

JARVIS exists to make capable AI assistance feel understandable, calm and useful in ordinary life. It should help the family ask questions, learn, create, organise, troubleshoot and safely interact with connected technology without requiring the user to understand the engineering behind it.

The long-term product intent is not only to build a chat interface. JARVIS OS should become a trusted family AI operating environment: present across devices, aware of user context where permission allows, respectful of boundaries, transparent about its limits and extensible without becoming uncontrolled.

---

# 3. Product Objectives

JARVIS OS shall be designed to support the following product objectives:

- Cross-platform operation.
- Windows-first delivery.
- Family-first experience.
- Voice-first interaction.
- Privacy by Design.
- Security by Design.
- Modular Architecture.
- Cloud Optional operation.
- Offline capability where practical.
- Human approval for high-risk actions.

These objectives define the product direction. They do not mandate a specific implementation sequence unless later approved through engineering work.

---

# 4. Product Design Principles

JARVIS OS shall follow these product design principles:

- Modular First.
- API First.
- Service Independence.
- Event Driven.
- Fail Gracefully.
- Document as We Build.
- Review Twice. Build Once. Improve for Everyone.
- Every feature must provide genuine family value.

The product should feel useful before it feels complex. Each capability should make daily life easier, safer, more creative or more enjoyable.

JARVIS OS shall also follow these recovered product principles:

- Product before process: governance exists to support the product, not obscure it.
- Human authority: people remain in control of identity, permissions, memory, integrations and high-risk actions.
- Technology independence: JARVIS shall not be tied permanently to a single AI provider, device platform or integration technology.
- Trust through transparency: JARVIS should explain what it can do, what it cannot do and when a capability is unavailable.
- Calm interaction: JARVIS should avoid noisy, alarming or manipulative behaviour.
- Design intent preservation: important product intent shall be recorded before implementation details obscure why a feature exists.

---

# 5. Minimum Lovable Product (MLP)

Version 0.1 shall provide the first Minimum Lovable Product.

The objective of MLP 0.1 is:

> A useful JARVIS that can be enjoyed every day.

MLP 0.1 shall include:

- GUI Dashboard.
- Chat Interface.
- Text Responses.
- Animated Avatar / Orb.
- Basic Voice Input.
- Basic Conversation Memory.
- User Profiles.
- Service Status Dashboard.

The MLP should establish the emotional and practical product foundation: JARVIS should feel present, responsive, understandable and safe, even before advanced automation or external integrations are introduced.

## Product Personality and Behaviour

JARVIS should behave like a calm, capable and trustworthy assistant.

Expected behaviour:

- Clear rather than clever.
- Helpful without pretending to know more than it does.
- Polite and steady under uncertainty.
- Transparent when a service, provider or device capability is unavailable.
- Respectful of family context and individual privacy.
- Careful around children, sensitive information and high-risk actions.
- Willing to ask for human approval rather than guessing.

JARVIS should feel present, but not intrusive. Animation, voice and visual feedback should support understanding rather than distract from the task.

## User Experience Philosophy

The JARVIS experience should make system state visible.

The GUI should help users understand:

- what JARVIS heard or received;
- what JARVIS is doing;
- which services are online, offline or unavailable;
- whether a response is local, provider-backed or limited by unavailable capability;
- when human approval is required.

The avatar or orb is a presence indicator, not decoration only. Its animation should communicate calm availability, thinking, degraded service or attention where useful.

The dashboard should grow into a family operations surface showing useful status, service health, shared context and safe shortcuts. It should not become a noisy control panel.

Multi-device interaction should preserve continuity while respecting device permissions. Windows-first delivery remains the initial priority, but phone, tablet, wearable and future device experiences should feel like extensions of the same JARVIS identity.

---

# 6. High Level Architecture

JARVIS OS is composed of a user experience layer, a conversation layer, a core engine and independent supporting services.

ESR-0008 clarifies the current architectural terminology:

- Project JARVIS AI is the engineering programme.
- JARVIS Platform is the runtime operating platform.
- Guardian is the trusted digital companion / AI entity hosted by the JARVIS Platform.
- Sentinel is the trust gateway before Platform Services.
- User Experience Platform (UXP) is the current architectural term for the presentation layer.

Historical GUI references remain valid where they describe earlier implementation or user-interface work. Current architecture uses UXP. UXP visualises state and interaction; it does not own business logic or system state.

```text
                    GUI
                     |
              Conversation Layer
                     |
             JARVIS Core Engine
                     |
     +---------------+---------------+---------------+
     |               |               |               |
   Memory          Voice           Vision        Internet
     |
 Family Profiles
     |
 Security
     |
 Plugin Framework
```

All services shall communicate through documented APIs.

Failure of one service shall not stop the Core. JARVIS OS shall degrade gracefully, report service status clearly and continue operating with available capabilities wherever practical.

Sentinel asks whether an input can be trusted before it reaches Platform Services. Guardian asks whether an action should happen and governs consent, policy, privacy, approval, memory retention and human-in-the-loop decisions.

Specialist agents provide domain capability to Guardian. Engineering Assistant is treated as an Engineering Agent / specialist agent, not a separate AI identity.

Obsidian is part of the Engineering Ecosystem as the human-facing Engineering Knowledge Workspace for OSE. It is not part of the JARVIS runtime platform. GitHub remains the source of truth.

## Capability Hierarchy

JARVIS capabilities shall be organised as a hierarchy so future implementation remains understandable.

```text
JARVIS OS
|
+-- Experience
|   +-- GUI
|   +-- Avatar / Orb
|   +-- Conversation
|   +-- Dashboard
|
+-- Intelligence
|   +-- Conversation Orchestration
|   +-- AI Provider Abstraction
|   +-- Planning
|   +-- Learning Support
|
+-- Knowledge and Memory
|   +-- Session Memory
|   +-- Personal Memory
|   +-- Shared Family Memory
|   +-- AIEMS Knowledge Capability
|
+-- Interaction Services
|   +-- Voice
|   +-- Vision
|   +-- Internet
|   +-- Local Agent
|
+-- Protection
|   +-- Guardian
|   +-- Permissions
|   +-- Human Approval
|   +-- Audit Logging
|
+-- Extensibility
    +-- Plugin Manager
    +-- Smart Home
    +-- Engineering Assistance
    +-- Future Device Integrations
```

Capability relationships shall remain explicit. Memory supports intelligence. Guardian constrains high-risk actions. The GUI exposes service state. Provider abstraction protects the product from long-term dependency on any single AI provider. Capability readiness is tracked in [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].

---

# 7. Core Services

## JARVIS Core

Purpose: Provide the central product engine for conversation coordination, service orchestration and product behaviour.

Responsibilities:

- Coordinate user requests.
- Route work to appropriate services.
- Maintain core lifecycle state.
- Preserve safe operating boundaries.
- Provide the stable centre of the product experience.

Future Expansion:

- Multi-agent coordination.
- Advanced planning.
- Context-aware orchestration.
- Provider selection across local and cloud AI capabilities.
- AIEMS knowledge explanation.

## JARVIS Memory

Purpose: Provide personal, family and session memory in a way that supports useful assistance while preserving privacy boundaries.

Responsibilities:

- Maintain basic conversation memory.
- Support user profile context.
- Separate personal and shared family memories.
- Provide memory status to the product experience.

Future Expansion:

- Long-term family knowledge.
- Memory review and editing.
- Consent-aware memory controls.
- Context retrieval across devices.
- Repository-backed engineering knowledge where approved.

## JARVIS Voice

Purpose: Provide voice input and future speech output for natural interaction.

Responsibilities:

- Capture basic voice input.
- Convert user speech into product requests.
- Support voice-first interaction patterns.
- Report voice service availability.

Future Expansion:

- Speech synthesis.
- Speaker recognition.
- Wake word support.
- Multi-language support.

## JARVIS Vision

Purpose: Provide future visual understanding capabilities for documents, images, camera input and environment context.

Responsibilities:

- Support future visual interpretation.
- Report vision service status.
- Preserve security and permission boundaries around camera or image use.

Future Expansion:

- Document understanding.
- Camera monitoring.
- Object and scene recognition.
- Family-safe visual assistance.

## JARVIS Guardian

Purpose: Provide product safety, security, permissions and human approval controls.

Responsibilities:

- Enforce permission levels.
- Support high-risk action approval.
- Maintain safety boundaries.
- Support audit logging.
- Protect child and guest profiles.

Future Expansion:

- Risk-based action controls.
- Cyber monitoring.
- Policy-aware automation.
- Family safety reporting.
- Pre-approved emergency action framework.
- Parental oversight controls.

## JARVIS Internet

Purpose: Provide controlled internet-enabled assistance when network access is available and approved.

Responsibilities:

- Support internet-backed answers and tasks.
- Respect cloud optional operation.
- Report network-dependent capability status.
- Preserve user approval for higher-risk actions.

Future Expansion:

- Web research.
- Online service integrations.
- Safe browsing assistance.
- Provider-specific internet tools.

## JARVIS Local Agent

Purpose: Provide local device assistance for approved desktop and system-level tasks.

Responsibilities:

- Support Windows-first local capability.
- Report local agent availability.
- Respect permission and approval boundaries.
- Keep local automation separate from the Core.

Future Expansion:

- Cross-platform local agents.
- Device health checks.
- Local file assistance.
- Family IT support automation.
- Strict local permission boundaries.

## JARVIS Plugin Manager

Purpose: Provide an extensible product capability model through controlled plugins.

Responsibilities:

- Track available plugins.
- Enable modular expansion.
- Preserve service boundaries.
- Support safe capability discovery.

Future Expansion:

- Plugin marketplace.
- Family-approved plugins.
- Third-party integrations.
- Capability sandboxing.

## JARVIS Service Monitor

Purpose: Provide visibility of product service health and availability.

Responsibilities:

- Track service status.
- Surface degraded capability.
- Support the Service Status Dashboard.
- Help users understand what JARVIS can currently do.

Future Expansion:

- Health history.
- Service restart guidance.
- Diagnostics.
- Operational notifications.

## JARVIS GUI

Purpose: Provide the primary visual experience for JARVIS OS.

Responsibilities:

- Provide the dashboard.
- Provide the chat interface.
- Display the animated avatar or orb.
- Present user profiles and service status.
- Make JARVIS feel approachable and family-friendly.

Future Expansion:

- Multi-device UI.
- Family dashboard.
- Accessibility modes.
- Smart home and device views.

---

# 8. Family Experience

JARVIS OS is family-first. It shall support different user types with appropriate privacy, capability and safety boundaries.

| User Type | Product Intent |
|-----------|----------------|
| Administrator | Manages household settings, permissions, integrations and high-risk approvals. |
| Adult | Uses JARVIS for personal assistance, family coordination, creativity, learning and IT support. |
| Child | Uses JARVIS through age-appropriate boundaries, educational support and safe creative assistance. |
| Guest | Receives limited temporary access without personal or family memory exposure. |

Family experience shall include:

- Personal memories.
- Shared family memories.
- Privacy boundaries.
- Educational support.
- Creative assistance.
- IT assistance.
- Shared family dashboard.

JARVIS OS should help a household work better together without flattening individual privacy. Personal memories belong to the person. Shared family memories belong to the household context.

---

# 9. Security Architecture

JARVIS OS shall be secure by design and human-controlled.

Initial security architecture shall include:

- Face Recognition.
- Phone Authentication.
- Password fallback.
- Permission Levels.
- Audit Logging.
- Human Approval.
- Safe AI behaviour.

Security controls shall protect family members, reduce accidental harm and ensure higher-risk actions remain under human control.

Permission levels shall determine what users can see, request and approve. Audit logging shall support review of important actions without exposing unnecessary private content.

---

# 10. Product Roadmap

JARVIS OS shall evolve through vertical increments that deliver visible family value early.

| Phase | Product Focus |
|-------|---------------|
| MLP 0.1 | GUI dashboard, chat, text responses, animated avatar/orb, basic voice input, basic memory, user profiles and service status. |
| MLP 0.2 Voice | Improve voice input and introduce richer voice interaction. |
| MLP 0.3 Family Profiles | Expand administrator, adult, child and guest profile behaviour. |
| MLP 0.4 Memory | Improve personal memory, shared family memory and memory controls. |
| MLP 0.5 Local Agent | Introduce Windows-first local device assistance. |
| MLP 0.6 Internet | Add controlled internet-assisted capability. |
| MLP 0.7 Vision | Add visual understanding foundations. |
| MLP 0.8 Guardian | Expand permission, safety, audit and approval controls. |
| Version 1.0 | Family AI Operating System. |

Roadmap phases describe product direction. Each implementation package shall still be separately approved through AIEMS and selected against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] where appropriate.

---

# 11. Future Vision

Future JARVIS OS capability may include:

- Smart Home.
- Home Assistant integration assessment.
- Cyber Monitoring.
- Camera Monitoring.
- Robotics.
- Wearables.
- Vehicle Integration.
- Multiple AI Providers.
- Agent Collaboration.
- AIEMS Knowledge Capability.
- Engineering Assistance.
- Backup and Recovery Assistance.

Future capabilities shall remain modular, secure, privacy-aware and subject to human approval where risk requires it.

---

# 12. Engineering Principles

JARVIS OS engineering shall follow these principles:

- Everything must justify its existence.
- Governance exists to enable delivery.
- Review Twice. Build Once. Improve for Everyone.
- Build vertically.
- Deliver value early.
- Protect user privacy.
- Remain modular.
- Product before process.
- Feature-first delivery.
- Engineer for maintainable cost.
- Preserve design intent before implementation detail.

The product should grow through small, validated increments that make JARVIS more useful while preserving trust.

Engineering economics matter. JARVIS should prefer simple, maintainable, low-cost solutions until complexity is justified by product value, safety or scalability.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture model that JARVIS implements as flagship product. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability maturity view supporting package selection. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture aligned during ESR-0008. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Engineering session that recorded JARVIS Platform, UXP, Sentinel and Guardian architecture outcomes. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and ESR-0009 readiness position. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Closed session that established ESR-0008 readiness and product engineering context. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register containing JARVIS product engineering candidates. |

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial JARVIS OS product architecture blueprint created. |
| 1.1 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Promoted recovered product vision, behaviour, user experience, capability hierarchy and engineering intent into the product architecture. |
| 1.3 | 2 July 2026 | Codex Engineering Implementer | Aligned related artefact context with ESR-0009 readiness and RBL-0009 handover. |
| 1.2 | 2 July 2026 | Codex Engineering Implementer | Aligned product architecture with ESR-0008 JARVIS Platform, Guardian identity, Sentinel, UXP, Agent Framework and Obsidian/OSE terminology. |
