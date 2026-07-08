# ADR-0018 — Sentinel as AI Execution & Security Platform

## Status

Approved.

## Engineering Session

ESR-0014

## Decision Type

Core AIEMS Platform Architecture

## Decision

Sentinel is designated as the AI Execution & Security Platform for AIEMS.

Sentinel is no longer considered solely a trust gateway or AI provider interface. It is the execution governance platform responsible for secure, resilient and policy-driven execution of AI capabilities across AIEMS.

## Official Mission Statement

Sentinel is the AI Execution & Security Platform for AIEMS, providing trusted execution, cyber security, AI orchestration, policy enforcement, resilience and operational governance for AI systems.

## Context

During ESR-0014, Sentinel evolved from a planned trust boundary into a standalone top-level package with implemented execution capabilities:

- Sentinel Core trust boundary.
- Provider abstraction.
- Provider registry.
- Local deterministic provider.
- Provider configuration model.
- Credential references.
- Retry policy model.
- Provider configuration registry.
- Provider orchestrator.
- Health-aware routing.
- Automatic failover.
- Execution history.

The implementation work demonstrated that Sentinel's role is broader than AI provider selection. Sentinel is the correct architectural location for execution governance, cyber security, trust enforcement, provider orchestration, resilience, policy, audit and future operational controls.

## Guardian / Sentinel Responsibility Boundary

### Guardian

Guardian is the cognition engine.

Guardian is responsible for:

- Cognition.
- Reasoning.
- Planning.
- Conversation.
- Goal management.
- Memory utilisation.

Guardian decides what should be done.

### Sentinel

Sentinel is the AI Execution & Security Platform.

Sentinel is responsible for:

- Trusted execution.
- AI provider orchestration.
- Capability routing.
- Provider configuration.
- Health monitoring.
- Retry and failover.
- Execution history.
- Execution governance.
- Cyber security.
- Policy enforcement.
- Identity and secrets integration.
- Audit and telemetry.
- Compliance support.

Sentinel decides whether execution is permitted, where it should occur, how it should be executed, and whether it is safe.

## Consequences

### Positive

- Guardian remains focused on cognition and does not become coupled to provider, security or execution concerns.
- Sentinel becomes reusable across future AIEMS AI systems, not just Guardian/JARVIS.
- AI orchestration becomes one capability within a broader execution and security platform.
- Future cyber security, identity, secrets, audit and compliance capabilities have a natural architectural home.
- Provider resilience, health monitoring and failover remain outside Guardian.
- Direct providers, gateway providers and local providers can be integrated without changing Guardian.

### Trade-offs

- Sentinel becomes a larger platform surface and will need clear modular boundaries.
- Future Sentinel work should be organised into explicit workstreams to avoid uncontrolled growth.
- Security and execution governance must be designed carefully to avoid over-coupling unrelated capabilities.

## Long-Term Sentinel Workstreams

```text
Sentinel
│
├── Core Foundation                     ✅ ESR-0014
├── AI Provider Ecosystem               🚧 ESR-0015+
├── Cyber Security                      📋 Future
├── Identity & Authentication           📋 Future
├── Secrets Management                  📋 Future
├── Policy & Compliance                 📋 Future
├── Telemetry & Observability           📋 Future
├── Audit & Forensics                   📋 Future
├── Secure Execution & Sandboxing       📋 Future
└── Future AIEMS Services               📋 Future
```

## Architectural Principle

Guardian expresses intent. Sentinel governs execution.

## Decision Outcome

Approved during ESR-0014 closure.

This ADR supersedes any prior interpretation of Sentinel as only a trust gateway. Sentinel remains a trust boundary, but its broader platform role is now AI Execution & Security Platform for AIEMS.
