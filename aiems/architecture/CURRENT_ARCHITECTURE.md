# AIEMS Current Architecture

## Status

Current architecture at the close of Engineering Session ESR-0014.

This document is the authoritative architecture snapshot for the next engineering session. It reflects implemented work and approved architectural decisions up to ESR-0014 closure.

## Platform Overview

AIEMS is structured around a clear separation between cognition and trusted execution.

```text
                         AIEMS
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
    Guardian                              Sentinel
 Cognition Engine          AI Execution & Security Platform
```

## Core Architectural Principle

Guardian expresses intent. Sentinel governs execution.

Guardian decides what should be done.

Sentinel decides whether execution is permitted, where it should occur, how it should be executed, and whether it is safe.

## Guardian

Guardian is the cognition engine.

### Responsibilities

- Reasoning.
- Planning.
- Conversation.
- Goal management.
- Memory utilisation.
- User-facing cognition.
- Future Guardian Orb interaction.

### Non-Responsibilities

Guardian should not own:

- Provider-specific logic.
- API credentials.
- Security policy enforcement.
- Execution routing.
- Retry and failover.
- Provider health decisions.
- Secrets management.
- Compliance controls.

Those responsibilities belong to Sentinel.

## Sentinel

Sentinel is the AI Execution & Security Platform for AIEMS.

### Current Implemented Capabilities

Implemented by the close of ESR-0014:

- Standalone top-level `sentinel` package.
- Sentinel Core trust boundary.
- Sentinel request, decision and response model.
- Execution provider abstraction.
- Provider registry.
- Local deterministic provider.
- Provider configuration model.
- Credential reference abstraction.
- Retry policy model.
- Provider configuration registry.
- Provider orchestrator.
- Provider health model.
- Capability routing.
- Automatic failover.
- Execution history.

### Future Platform Capabilities

Planned Sentinel workstreams:

- Cyber security.
- Identity and authentication.
- Secrets management.
- Policy and compliance.
- Telemetry and observability.
- Audit and forensics.
- Secure execution and sandboxing.
- Provider lifecycle management.
- Capability registry.

## Runtime Architecture

```text
                         Guardian
                    Cognition Engine
                              │
                              ▼
                  Intent / Capability Request
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │              Sentinel                │
        │   AI Execution & Security Platform   │
        │                                      │
        │  ┌────────────────────────────────┐  │
        │  │ Trust Boundary                 │  │
        │  │ Provider Orchestrator          │  │
        │  │ Provider Configuration         │  │
        │  │ Health Monitor                 │  │
        │  │ Routing Engine                 │  │
        │  │ Retry & Failover               │  │
        │  │ Execution History              │  │
        │  └────────────────────────────────┘  │
        └──────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Direct Providers  Gateway Providers  Local Providers
```

## Provider Ecosystem Architecture

Sentinel supports three provider categories.

### Direct Providers

Foundation model or platform providers accessed directly.

Examples:

- OpenAI.
- Anthropic.
- Google Gemini.
- Azure OpenAI.
- Mistral.
- Cohere.

### Gateway Providers

Aggregation providers exposing multiple model families through a unified API.

Examples:

- AIMLAPI.
- OpenRouter.
- Together AI.
- Groq.

Gateway providers are evaluated as execution gateways rather than model owners.

### Local Providers

Local or self-hosted execution paths for resilience and degraded operation.

Examples:

- Ollama.
- llama.cpp.
- LM Studio.
- vLLM.

## Resilience Model

Sentinel owns resilience.

```text
Capability Request
        │
        ▼
Sentinel Orchestrator
        │
        ├── Check trust decision
        ├── Resolve capability route
        ├── Evaluate provider health
        ├── Execute primary provider
        ├── Fail over if required
        └── Record execution history
```

No single provider should be a single point of failure.

## Security Positioning

Cyber security is a future Sentinel workstream, not a separate bolt-on subsystem.

Security capabilities will be added to Sentinel because Sentinel already governs execution.

Future examples:

- Permission checks.
- Secrets access governance.
- Malware scanning integration.
- Sandbox enforcement.
- Identity provider integration.
- Audit trail generation.
- Risk-based execution policy.

## Key Architecture Decisions Reflected

- Sentinel is a standalone top-level package.
- JARVIS/Guardian may depend on Sentinel.
- Sentinel must remain product-agnostic and must not depend on Guardian/JARVIS.
- Guardian expresses intent and capability needs.
- Sentinel owns trusted execution, provider orchestration and security governance.
- Provider selection is evidence-driven through PEM-001.
- Sentinel is formally positioned by ADR-0018 as the AI Execution & Security Platform.

## ESR-0015 Starting Architecture

ESR-0015 should start from this architecture and proceed implementation-first.

Expected ESR-0015 focus:

1. Complete PEM-001 provider scoring.
2. Approve initial provider ecosystem.
3. Implement first external provider adapter.
4. Implement a secondary execution path.
5. Validate live Sentinel failover.
6. Connect Guardian through Sentinel.
7. Deliver Guardian's first interactive conversation.
