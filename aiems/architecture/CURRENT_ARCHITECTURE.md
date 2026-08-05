# AIEMS Current Architecture

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | CURRENT_ARCHITECTURE |
| Title | AIEMS Current Architecture |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Review Frequency | At significant Sentinel/Guardian architectural change |

---

## Status

Refreshed at ESR-0050 WP3, per [[EIP-ESR0050-002_CURRENT_ARCHITECTURE_REFRESH_AND_GATE_OF_DURIN_DETAIL|EIP-ESR0050-002]], resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0047. This is this document's first registration as a controlled artefact (previously an informal snapshot with no Document Control block or version field, despite five other controlled artefacts - AAM-0001, MOD-0001, SAM-0001, UAM-0001, GAM-0001 - already treating it as authoritative for Sentinel's implemented scope).

Corrects a stale self-description: this document's Status previously claimed "close of Engineering Session ESR-0014," but its last substantive content edit was actually ESR-0016 WP2A (commit `d6eb854`, the Sentinel trust-tier model update) - 34 sessions before this refresh, not 36. Both figures were wrong; this refresh is the first update since.

This document remains the authoritative architecture snapshot for Sentinel and Guardian's implemented scope. It reflects real, evidenced implementation only - not aspiration or planned work, which remains the responsibility of [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (forward sequencing) and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (backlog).

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
- Guardian Orb visual presence.

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

### Faculties Delivered Since ESR-0014

The responsibilities above were role definitions from the start; what has changed is how much of Guardian is now real, evidenced implementation rather than foundation-only:

- **Guardian Cognitive Core, Phase 1** (ESR-0039): composes persona, retained Personal Memory and bounded recent history before every provider call.
- **Personal Memory** (ESR-0027 WP1, EBG-0080): consent-gated, `PersonalMemoryStore`/`PersonalMemoryService`, wired into `GuardianRuntime`.
- **Guardian Orb** (ESR-0019 WP2 onward): renders the live repository knowledge graph, no longer the placeholder animation this document's earlier revision described as "future."
- **Identity and Profiles** (ESR-0046): local, unauthenticated profile create/list/select, role-tagged against GAM-0001 Section 8.1's household roles.
- **Voice, both directions** (ESR-0040/ESR-0044 speech output; ESR-0047 speech input): self-hosted Piper/`faster-whisper`, Sentinel-gated.
- **Agent Framework** (ESR-0049/ESR-0050): a real, Sentinel-gated first specialist agent (`gia-observability`), now reachable through the live UXP.

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

Implemented during ESR-0016 WP1:

- Sentinel trust-tier policy model.
- Trust tiers: `ROUTINE`, `SENSITIVE`, `RESTRICTED`.
- Classification categories: `ROUTINE_INTERACTION`, `HUMAN_APPROVAL_REQUIRED`, `UNSUPPORTED_HIGH_RISK`, `EMERGENCY_CONTROL`, `LOCAL_AGENT_ACTION`.
- Decision outcomes: `ALLOW` for routine interaction, `REVIEW` for human approval, and `DENY` for unsupported high-risk, emergency-control and local-agent-action categories.
- Conservative classification precedence: unsupported high risk, then emergency control, then local-agent action, then human approval, then routine interaction.
- Deny-category requests cannot be softened to `REVIEW` by also setting human approval.

**Corrected as of this refresh (ESR-0050 WP3)**: this section previously claimed `SimpleApprovalPolicy` remains the production default for `SentinelTrustGateway` - true only for a *bare-constructed* gateway (`sentinel/core.py`'s `SentinelTrustGateway.__init__` still falls back to `SimpleApprovalPolicy()` when no policy engine is passed). It has not been true of the actual **production** runtime path since ESR-0024 WP1 (EBG-0074, Complete): `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` explicitly constructs `SentinelTrustGateway(policy_engine=TrustTierPolicy())`. `TrustTierPolicy` is the real production default; `SimpleApprovalPolicy` is now only the seen-nowhere-in-production fallback for ad hoc/test construction.

Implemented since ESR-0016, previously undocumented here:

- **Audit logging** (`sentinel/audit.py`): every `SentinelTrustGateway.evaluate()` call records an `AuditEvent` (outcome, summary, source, intent, reason) via an injectable `AuditRecorder` (`MemoryAuditRecorder` for tests, `JsonAuditRecorder` for persistence).
- **Self-hosted speech providers**: Piper (text-to-speech, ESR-0040) and `faster-whisper` (speech-to-text, ESR-0047), both Sentinel-gated, credential/path-gated with no auto-download and an honest `not_connected` degrade path.
- **Agent Framework's `SentinelGatedAgentService`** (ESR-0049): every specialist-agent invocation evaluated through the same shared gateway every other capability uses, before executing.
- **Real external-provider wiring**: OpenAI and Gemini both live-validated against their real APIs; one is wired as the default production text-generation route (configurable, credential-gated, EBG-0070 ESR-0022); Ollama registered as a further local fallback (EBG-0075, ESR-0026); `LocalEchoProvider` retained as the final, always-available failover.

The trust-tier model provides extension points for [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (which used them, ESR-0023) and the Agent Framework (which reuses them, ESR-0048/ESR-0049). It does not implement Guardian family-safety behaviour, emergency control execution, automation, or Guardian's wider UI behaviour beyond what is documented above.

### Sentinel Gate of Durin: Trust Gateway and Platform-Entry Validation

Added at ESR-0050 WP3, resolving EBG-0047 ("Extend EBG-0030 with Sentinel trust gateway, trust tiers and platform-entry validation details"). Documents the real, already-implemented pattern [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] decided architecturally at ESR-0008 - this section records its actual implementation, not new architecture.

**The metaphor.** ADR-0009 retains "Speak, friend, and enter" as an architectural metaphor for trusted platform entry - not a literal authentication mechanism. Sentinel sits before Platform Services; everything entering JARVIS passes through Sentinel first.

**The real gate: `SentinelTrustGateway.evaluate()`.** A `SentinelRequest` (source, intent, payload type, optional metadata, timestamp - `sentinel/core.py`) is submitted to the gateway. The gateway delegates the trust decision to its configured `PolicyEngine`, wraps the result in a `SentinelDecision` (outcome, reason, trust boundary, whether human approval is required), returns a `SentinelResponse`, and unconditionally records an `AuditEvent` - every decision is evaluated and audited, with no bypass path.

**Trust-tier classification: `TrustTierPolicy.classify()`.** The production policy engine (see the corrected claim above) classifies each request into a `TrustCategory` using a fixed, conservative precedence - `UNSUPPORTED_HIGH_RISK`, then `EMERGENCY_CONTROL`, then `LOCAL_AGENT_ACTION`, then `HUMAN_APPROVAL_REQUIRED`, then `ROUTINE_INTERACTION` - and maps each category to a `TrustTier` (`RESTRICTED`/`SENSITIVE`/`ROUTINE`) and outcome (`DENY`/`DENY`/`DENY`/`REVIEW`/`ALLOW`). `LOCAL_AGENT_ACTION`'s `DENY` cannot be softened to `REVIEW`, per GAM-0001 Section 8A's hard boundary.

**Platform-entry validation is real and shared, not per-capability.** `build_default_runtime()` constructs exactly one `SentinelTrustGateway` instance and passes that same instance to every capability it wires: conversation (`SentinelGatedConversationProvider`), memory (`PersonalMemoryService`), speech synthesis, speech transcription, and the Agent Framework (`SentinelGatedAgentService`). None of these constructs its own gateway - "one trust boundary, not two," per `EIP-ESR0027-001` Section 4's own framing of the requirement. A future capability wired into the production runtime must reuse this same shared instance, not construct a fresh one, to remain a genuine platform-entry gate rather than a bypassable per-capability check.

### Future Platform Capabilities

Planned Sentinel workstreams:

- Cyber security.
- Identity and authentication (distinct from JARVIS's own local, unauthenticated profile identity, ESR-0046 - this remains a Sentinel-level credentialed-authentication gap).
- Secrets management (STD-0006, ESR-0045, defines the configuration/secrets *standard*; a Sentinel-owned secrets management *capability* implementing it remains future).
- Policy and compliance (beyond the trust-tier classification model already implemented).
- Telemetry and observability.
- Forensic-depth audit analysis (basic audit event recording is implemented, see above; deeper forensic tooling remains future).
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
        │  │ Audit Recorder                 │  │
        │  └────────────────────────────────┘  │
        └──────────────────────────────────────┘
                              │
       ┌───────────────┬─────┴──────┬────────────────┐
       ▼                ▼            ▼                ▼
 Direct Providers  Speech/Transcription  Agent Framework  Memory Service
 Gateway Providers    Providers          (Specialist        (Personal
 Local Providers                          Agents)            Memory)
```

The diagram above extends the original providers-only routing shown at ESR-0014/ESR-0016 to reflect the real capabilities now sharing the same trust boundary: speech/transcription providers, the Agent Framework, and the memory service, alongside the original text-generation provider ecosystem.

## Provider Ecosystem Architecture

Sentinel supports three provider categories.

### Direct Providers

Foundation model or platform providers accessed directly.

**Implemented and live-validated**: OpenAI, Google Gemini.

**Approved in principle (PEM-001), not yet implemented**: Anthropic, Azure OpenAI, Mistral, Cohere.

### Gateway Providers

Aggregation providers exposing multiple model families through a unified API.

Examples (still illustrative only - none implemented):

- AIMLAPI.
- OpenRouter.
- Together AI.
- Groq.

Gateway providers are evaluated as execution gateways rather than model owners.

### Local Providers

Local or self-hosted execution paths for resilience and degraded operation.

**Implemented**: Ollama (EBG-0075, ESR-0026, registered as a local fallback), `LocalEchoProvider` (deterministic, the final failover with no external dependency).

**Still illustrative examples, not implemented**: llama.cpp, LM Studio, vLLM.

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

No single provider should be a single point of failure. Confirmed still accurate against the real `sentinel/orchestrator.py` (`ProviderOrchestrator`, `ProviderRoute`, `ProviderHealth`) at this refresh.

## Security Positioning

Cyber security is a future Sentinel workstream, not a separate bolt-on subsystem.

Security capabilities will be added to Sentinel because Sentinel already governs execution.

Future examples:

- Permission checks.
- Secrets access governance.
- Malware scanning integration.
- Sandbox enforcement.
- Identity provider integration.
- Audit trail generation (basic recording now implemented, see Sentinel's Current Implemented Capabilities above; the broader trail/governance workstream remains future).
- Risk-based execution policy.

## Key Architecture Decisions Reflected

- Sentinel is a standalone top-level package.
- JARVIS/Guardian may depend on Sentinel.
- Sentinel must remain product-agnostic and must not depend on Guardian/JARVIS.
- Guardian expresses intent and capability needs.
- Sentinel owns trusted execution, provider orchestration and security governance.
- Provider selection is evidence-driven through PEM-001.
- Sentinel is formally positioned by [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] as the AI Execution and Security Platform.
- Sentinel is the Gate of Durin ([[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]]) - every capability passes through the same shared trust boundary before executing.
- Specialist agents are capabilities Guardian invokes, never separate identities ([[ADR-0011_AGENT_FRAMEWORK|ADR-0011]]), and are evaluated through the identical Sentinel gate every other capability uses.

## Historical Note: ESR-0015 Starting Architecture

This section previously listed seven forward-looking implementation items as "Expected ESR-0015 focus." All seven were completed, most by approximately ESR-0017: PEM-001 provider scoring, initial provider ecosystem approval, the first external provider adapter, a secondary execution path, live Sentinel failover validation, Guardian connected through Sentinel, and Guardian's first interactive conversation. Retained here as a historical record rather than deleted outright, since several other controlled artefacts (RBL-0012, RBL-0013, ESR-0017's own review packages) cite specific numbered items from that original list as evidence of what they delivered.

Forward-looking sequencing is no longer this document's responsibility. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] are the authoritative sources for what comes next.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sibling Sentinel architecture artefact, positioning-only (explicitly disclaims defining executable policy logic); this document carries the implementation-grounded detail SAM-0001 defers. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Parent platform architecture; treats this document as the authoritative Sentinel-scope snapshot via its own Subsequent Architectural Update note. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity/cognitive architecture; likewise treats this document as authoritative for Sentinel's implemented scope. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian experience architecture; likewise treats this document as authoritative for Sentinel's implemented scope. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | References this document as authoritative for the implemented Sentinel trust-tier mechanism (via its own Related Artefacts table, not a Subsequent-Architectural-Update-style note). |
| [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | The architecture decision this document's Gate of Durin subsection records the real implementation of. |
| [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] | Positioned Sentinel as the AI Execution and Security Platform, broadening it beyond trust-gateway-only. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0047, resolved by this refresh. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Forward-looking sequencing authority, superseding this document's retired "ESR-0015 Starting Architecture" role. |

---

## Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP3, per EIP-ESR0050-002, resolving EBG-0047 (Sentinel Gate of Durin Architecture Specification). First registration as a controlled artefact (Document Control block, version field added). Corrected the stale Status line (claimed close of ESR-0014; last real edit was ESR-0016 WP2A) and one factual error (claimed `SimpleApprovalPolicy` remains the production default; `TrustTierPolicy` has been the real default since ESR-0024 WP1/EBG-0074). Added Guardian's "Faculties Delivered Since ESR-0014" and Sentinel's post-ESR-0016 implemented-capabilities detail (audit logging, speech/transcription providers, Agent Framework gating, real provider wiring). Added the new Sentinel Gate of Durin subsection directly resolving EBG-0047, grounded in `SentinelTrustGateway.evaluate()`, `TrustTierPolicy.classify()` and `build_default_runtime()`'s single shared gateway evidence. Refreshed Provider Ecosystem's implemented-versus-planned distinction. Replaced the long-completed "ESR-0015 Starting Architecture" forward-look with a historical note, redirecting to JRM-0001/EBR-0001. Added Related Artefacts and this Version History section, neither of which existed before. |
| 0.14 | 9 July 2026 | Claude Engineering Reviewer | ESR-0016 WP2A: landed and independently verified (commit `d6eb854`) - added the Sentinel trust-tier policy model (trust tiers, classification categories, decision outcomes, `SimpleApprovalPolicy` as the then-accurate production default, extension points for EBG-0047/EBG-0020/EBG-0021). Informal version marker only - this document carried no real Document Control or version field until the 1.0 refresh above. |
