# PEM-001 — AI Provider Evaluation Matrix

## Status

Draft for ESR-0014 engineering decision support.

## Purpose

Select the initial AI provider ecosystem for Project JARVIS AI using an AIEMS-aligned evaluation method.

The goal is not to choose a single model vendor. The goal is to define a resilient provider ecosystem that Sentinel can orchestrate without coupling Guardian to any provider.

## Architectural Context

ESR-0014 established Sentinel as a standalone trust and execution platform with:

- Sentinel Core trust boundary.
- Provider abstraction.
- Provider configuration.
- Local provider.
- Provider orchestrator.
- Health-aware routing.
- Failover.
- Execution history.

Guardian expresses intent and required capability. Sentinel determines execution.

```text
Guardian
    │
    ▼
Sentinel AI Orchestrator
    │
    ├── Direct Providers
    ├── Gateway Providers
    └── Local Providers
```

## Provider Ecosystem Categories

### 1. Direct Foundation Model Providers

These providers own and operate foundation models directly.

Candidate examples:

- OpenAI
- Anthropic
- Google Gemini
- Mistral
- Cohere
- Azure OpenAI

### 2. Gateway / Aggregation Providers

These providers expose multiple underlying model families through a unified API.

Candidate examples:

- AIMLAPI
- OpenRouter
- Together AI
- Groq

Gateway providers should not be treated as equivalent to foundation model providers. They are execution gateways that may provide vendor flexibility, faster experimentation and broader model access, but they also introduce another operational dependency.

### 3. Local / Offline Providers

These provide local or self-hosted execution.

Candidate examples:

- Ollama
- llama.cpp
- LM Studio
- vLLM

Local providers are important for resilience and graceful degradation. They may not match frontier-model capability, but they can keep core Guardian functionality available when cloud providers are unavailable.

## Evaluation Criteria

| Criterion | Weight | Description |
|---|---:|---|
| Capability Coverage | 20% | Text, reasoning, tool calling, structured output, vision, audio, embeddings and future multimodal support. |
| Reliability | 15% | Provider uptime, operational maturity, rate limits and production readiness. |
| Resilience Fit | 15% | Suitability for primary, secondary, gateway or local fallback roles. |
| SDK / API Maturity | 10% | Documentation, SDK quality, API stability and implementation effort. |
| Cost | 10% | Pricing predictability and suitability for iterative development. |
| Latency | 10% | Suitability for interactive Guardian experiences. |
| Privacy / Data Handling | 10% | Data retention, enterprise controls, locality and policy compatibility. |
| Vendor Independence | 10% | Ability to avoid single-provider lock-in and support Sentinel routing flexibility. |

## Initial Qualitative Assessment

| Candidate | Category | Strengths | Risks / Unknowns | Likely Role |
|---|---|---|---|---|
| OpenAI | Direct | Strong general capability, mature API ecosystem, multimodal/tool trajectory. | Cloud dependency, vendor concentration, cost management. | Primary candidate. |
| Anthropic | Direct | Strong reasoning, coding and agentic capability; useful diversity from OpenAI. | Separate API surface, provider-specific policy and availability considerations. | Secondary cloud candidate. |
| Google Gemini | Direct | Strong multimodal and Google ecosystem fit. | API evolution and capability consistency require assessment. | Vision/multimodal candidate. |
| Azure OpenAI | Direct/Enterprise Channel | Enterprise controls, Azure integration, possible governance advantages. | Azure setup complexity and dependency on Microsoft/Azure account model. | Enterprise/managed deployment candidate. |
| AIMLAPI | Gateway | Unified access to many models; useful for evaluation and experimentation. | Gateway dependency, feature parity and reliability need validation. | Gateway candidate. |
| OpenRouter | Gateway | Broad model marketplace and routing flexibility. | External routing dependency and production reliability need validation. | Gateway candidate. |
| Together AI | Gateway/Hosted Open Models | Strong open-model access. | Model-specific capability variation. | Research/fallback candidate. |
| Groq | Gateway/Inference | Low-latency inference profile. | Model catalogue and capability breadth need validation. | Performance-tier candidate. |
| Ollama | Local | Offline fallback, simple local development, vendor independence. | Local hardware limits and lower capability than frontier cloud models. | Local fallback candidate. |
| llama.cpp | Local | Lightweight local runtime and strong portability. | More engineering effort than Ollama. | Embedded/local fallback candidate. |

## Recommended Provider Roles to Evaluate

| Role | Description | Candidate Set |
|---|---|---|
| Primary Cloud Provider | Default high-capability provider for Guardian cognition. | OpenAI, Anthropic, Gemini, Azure OpenAI |
| Secondary Cloud Provider | Independent fallback cloud provider. | Anthropic, OpenAI, Gemini |
| Gateway Provider | Unified model access for experimentation and optional routing flexibility. | AIMLAPI, OpenRouter, Together AI |
| Local Fallback Provider | Offline or degraded-mode provider. | Ollama, llama.cpp |
| Specialist Provider | Capability-specific provider for vision, embeddings, speech or high-speed inference. | Gemini, OpenAI, Groq, Cohere, specialist APIs |

## Resilience Principles

1. No single AI provider should become a single point of failure.
2. Guardian must not contain provider-specific logic.
3. Sentinel should route by capability, policy and health.
4. Gateway providers should augment resilience, not replace direct-provider resilience.
5. Local fallback should exist for degraded operation even if quality is reduced.
6. Provider choice should be revisitable as the AI ecosystem changes.

## Proposed Initial Ecosystem Direction

This is a draft recommendation pending further evidence:

| Role | Draft Direction |
|---|---|
| Primary | OpenAI or Anthropic, selected after scoring. |
| Secondary | The strongest independent alternative to the primary. |
| Gateway | AIMLAPI or OpenRouter for evaluation and optional routing flexibility. |
| Local Fallback | Ollama first, with llama.cpp as a later extraction path. |
| Vision / Multimodal | Evaluate OpenAI and Gemini directly. |
| Embeddings | Evaluate separately; do not assume same provider as chat/reasoning. |

## Implementation Implications

The next implementation should not hard-code OpenAI as the only provider. Instead:

1. Add provider role metadata to Sentinel configuration.
2. Extend the orchestrator to support named routing strategies.
3. Implement one direct provider adapter selected by PEM-001.
4. Implement one gateway or local provider adapter for resilience validation.
5. Demonstrate failover through Sentinel before exposing Guardian's first visible conversation flow.

## Open Questions

- Should the first external provider be direct or gateway-based?
- Should local fallback be required before Guardian is made visible?
- Should embeddings be evaluated independently from conversation providers?
- How should provider scoring be represented in Sentinel configuration?
- Should provider health be manual initially or derived from runtime telemetry?

## Decision Required

Before implementing the first external provider adapter, approve the evaluation outcome for:

1. Primary provider.
2. Secondary provider.
3. Gateway candidate.
4. Local fallback path.
5. First adapter to implement.

## Current Recommendation

Proceed with evidence gathering and scoring against the PEM-001 matrix before coding a vendor-specific external provider adapter.

PEM-001 keeps provider choice aligned with the Sentinel orchestration architecture and avoids binding Guardian to a single AI vendor.
