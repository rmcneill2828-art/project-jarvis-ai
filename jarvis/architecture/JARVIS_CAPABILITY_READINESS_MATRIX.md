# JARVIS Capability Readiness Matrix

---

# Document Control

| Field | Value |
|-------|-------|
| Title | JARVIS Capability Readiness Matrix |
| Artefact ID | JARVIS_CAPABILITY_READINESS_MATRIX |
| Version | 2.6 |
| Status | Maintained |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Last Refreshed | ESR-0050 WP1 (5 August 2026) |

---

# 1. Purpose

This matrix provides a single engineering view of current JARVIS capability maturity.

It supports product capability prioritisation without approving implementation by itself. Approved package selection remains governed through [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], sequencing guidance in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]], and the active Engineering Session.

---

# 2. Capability Readiness

| Capability | Vision | Architecture | Implementation | Testing | Overall Readiness |
|------------|--------|--------------|----------------|---------|-------------------|
| Conversation | Complete | Complete | Implemented | Implemented | Implemented (Foundation) |
| Intelligence | Complete | Draft | Phase 1 implemented (Guardian Cognitive Core composes persona/memory/history each turn, `jarvis/guardian/cognitive_core.py`) - ESR-0039 | Implemented | Implemented (Phase 1) |
| Memory | Complete | Partial | Personal Memory foundation implemented (`PersonalMemoryStore`/`PersonalMemoryService`, consent-gated, wired into `GuardianRuntime`) - ESR-0027 WP1 | Implemented (unit-tested: `test_memory_store.py`, `test_memory_service.py`) | Implemented (Foundation) |
| Identity | Complete | Partial | Local, unauthenticated profile create/list/select implemented (`jarvis/identity/`), role-tagged against GAM-0001 Section 8.1's four household roles - ESR-0046 | Implemented (unit- and RPC-tested) | Implemented (Foundation) |
| Voice | Complete | Partial | Both increments implemented: speech output (self-hosted Piper, ESR-0040/ESR-0044) and speech input (self-hosted `faster-whisper`, push-to-talk, ESR-0047) | Implemented (unit-, RPC- and Playwright-tested) | Implemented (Foundation) |
| Vision | Complete | Partial | Not Started | Not Started | Planned |
| Guardian | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| Sentinel | Complete | Complete | Implemented | Implemented | Implemented (Foundation) |
| Platform Services | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| User Experience Platform | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| Home Automation | Complete | Planned | Not Started | Not Started | Planned |
| Productivity | Complete | Planned | Not Started | Not Started | Planned |
| Agent Framework (specialist agents serving Guardian) | Complete | Complete | GIA's read-only local-resource observability wired as the first live specialist agent (`jarvis/agents/`, `GiaObservabilityAgent`), Sentinel-gated `ROUTINE_INTERACTION`, reachable via `guardian.agent.*` RPC - ESR-0049, EBG-0119. No UXP surface yet; `LOCAL_AGENT_ACTION` (the Action faculty) remains a hard `DENY`, not implemented. | Implemented (unit- and RPC-tested, 27 new tests) | Implemented (Foundation) |
| Knowledge | Complete | Complete | Implemented (Phase 1-2 of 4) | Implemented | Partial |
| Multi-device | Complete | Planned | Not Started | Not Started | Planned |
| Provider Architecture | Complete | Complete | Implemented (live-validated, wired into production runtime per EBG-0070) | Implemented | Implemented (Foundation) |

---

# 3. Overall Programme Capability Summary

JARVIS has moved well past the early executable foundation this matrix described at ESR-0009. Guardian, Sentinel, Platform Services, the User Experience Platform, Knowledge and Provider Architecture are all now genuinely implemented at foundation scope, not merely architecture-validated:

- **Guardian** has a running runtime foundation (ESR-0013), connected through Sentinel for real conversation (ESR-0017 WP2), reachable through a live, interactive UXP (ESR-0017 WP9), with its own visual presence rendering the live repository knowledge graph (ESR-0019) plus surfaced metrics/cluster panels (ESR-0021 WP4).
- **Sentinel** has a working trust gateway, provider abstraction, audit, policy and trust-tier model, with both OpenAI and Gemini live-validated as real external providers (real billed calls, real generated responses).
- **User Experience Platform** is live and interactive (Tauri + React, real backend bridge), not a disconnected static shell - matching PST-0001's own "Live, Foundation Scope" characterisation.
- **Knowledge** has a real backend graph builder and live-rendered Guardian Orb (Phase 1 complete, Phase 2 partially delivered).
- **Provider Architecture** has two live-validated adapters, and one is now wired into the default production runtime conversation path (EBG-0070, Complete, ESR-0022 WP1) - `LocalEchoProvider` remains the failover.
- **Memory** has a Personal Memory foundation (`PersonalMemoryStore`/`PersonalMemoryService`), consent-gated and wired into `GuardianRuntime`, delivered at ESR-0027 WP1. Session and Shared Family memory remain not implemented.
- **Intelligence** moved from Draft/Planned to Implemented (Phase 1): the Guardian Cognitive Core now composes persona, retained Personal Memory and bounded recent history before every provider call, delivered at ESR-0039. Full cognition beyond this remains architecturally Draft, per AAM-0001.
- **Identity** is newly implemented at foundation level: local, unauthenticated profile create/list/select, role-tagged against GAM-0001 Section 8.1's four household roles, delivered at ESR-0046. Credentialed authentication, memory scoping by profile and role-authority enforcement remain not implemented.
- **Voice** is now implemented at foundation level for both directions: speech output (ESR-0040/ESR-0044) and speech input (ESR-0047), both self-hosted, Sentinel-gated and reachable through the live UXP.
- **Agent Framework** moved from Proof of Concept (GIA-BOOT) to Implemented (Foundation): GIA's read-only local-resource observability is now a real, Sentinel-gated `ROUTINE_INTERACTION` specialist agent, reachable via `guardian.agent.*` RPC (ESR-0049, EBG-0119). It has no UXP surface yet, and `LOCAL_AGENT_ACTION` (the Action faculty, local device/system control) remains a hard `DENY` under GAM-0001 Section 8A - not implemented, not approached.

**Vision, Home Automation, Productivity and Multi-device remain not implemented**, consistent with PST-0001's "Outstanding Observations" - these are deliberately deferred, not overlooked.

JARVIS implementation maturity is now foundation-level-and-live across its core platform capabilities plus Memory, Intelligence Phase 1, Identity, Voice and the Agent Framework, with product-depth capabilities (vision, automation, multi-device, and Session/Shared Family memory) still ahead.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture source for capability intent and hierarchy. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture context for JARVIS as flagship implementation. |
| [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]] | Current accepted repository baseline. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Sibling document (Product Capability Baseline) refreshed via the same pattern at ESR-0020 (EBG-0056) - this refresh follows that precedent. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture source; still Draft, underlying the Intelligence row's Planned status. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register for candidate package selection; the v2.0 refresh closed EBG-0069, this v2.1 refresh closes EBG-0017. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Forward-looking sequencing artefact; the Not Started/Planned rows above correspond to items sequenced there. |

---

# 4. Refresh History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.6 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP7: corrected the Related Artefacts current-baseline reference from RBL-0030 to RBL-0031, established at ESR-0050 WP7 (Agent Framework UXP Wiring; Sentinel Gate of Durin Architecture Specification). Pointer fix only - capability rows not re-audited this pass. |
| 2.5 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP1 (content refresh disclosed as deferred at ESR-0049 WP7): renamed the "Engineering Agent (JARVIS-internal specialist agent)" row to "Agent Framework (specialist agents serving Guardian)" and updated it from Proof of Concept (GIA-BOOT) to Implemented (Foundation) - GIA's read-only observability is now the first live specialist agent, Sentinel-gated `ROUTINE_INTERACTION`, `guardian.agent.*` RPC-reachable (ESR-0049, EBG-0119); no UXP surface yet, `LOCAL_AGENT_ACTION` untouched. Overall Programme Capability Summary updated to match; the stale "JARVIS-internal specialist Engineering Agent remain not implemented" claim removed. |
| 2.4 | 5 August 2026 | Claude Engineering Implementer | ESR-0049 WP7: corrected the Related Artefacts current-baseline reference from RBL-0029 to RBL-0030, established at ESR-0049 WP7 (Agent Framework Phase 3, First Specialist Agent). Pointer fix only - capability rows not re-audited this pass; the new Agent Framework capability is not yet reflected here, remains open for a future content refresh. |
| 2.3 | 4 August 2026 | Claude Engineering Implementer | ESR-0048 WP1 (Documentation Debt Discipline): refreshed for ESR-0039 (Guardian Cognitive Core Phase 1), ESR-0046 (User Identity) and ESR-0047 (Voice Increment B) - flagged stale since ESR-0028 at ESR-0047 WP4's Repository Engineering Health Review. Intelligence row updated Draft/Planned to Implemented (Phase 1); new Identity row added; Voice row updated Not Started to Implemented (Foundation) for both directions. Overall Programme Capability Summary and Related Artefacts (`RBL-0015` to `RBL-0029`) updated to match. |
| 2.2 | 18 July 2026 | Claude Engineering Implementer | Post-commit fix per Engineering Reviewer (Codex) finding on the ESR-0028 WP2 committed diff: the Related Artefacts EBR-0001 relationship note still said "this refresh closes EBG-0069", true of the prior v2.0 refresh but not this one. Corrected to disclose both - the v2.0 refresh closed EBG-0069, this v2.1 (now v2.2) refresh closes EBG-0017. |
| 2.1 | 18 July 2026 | Claude Engineering Implementer | Refreshed at ESR-0028 WP2 per EIP-ESR0028-002, closing EBG-0017: registered this document in REG-0001 for the first time (closing the registration gap disclosed in the v2.0 entry below), and corrected two rows found stale against direct PST-0001 Section 5 evidence. Memory row: Implementation/Testing/Overall Readiness updated from Not Started/Planned to reflect the ESR-0027 WP1 Personal Memory foundation (`PersonalMemoryStore`/`PersonalMemoryService`, consent-gated, unit-tested). Provider Architecture row: removed the now-incorrect "unwired from production runtime" qualifier, reflecting EBG-0070's production wiring at ESR-0022 WP1. Updated the Overall Programme Capability Summary narrative and Related Artefacts (`RBL-0014` to `RBL-0015`) to match, so the refreshed rows no longer contradict the surrounding prose - an inconsistency an Engineering Reviewer pre-implementation review caught in the v0.1 implementation draft before it reached this document. |
| 2.0 | 15 July 2026 | Claude Engineering Implementer | Refreshed at ESR-0021 WP7, closing EBG-0069: corrected 13 sessions of staleness (dated to ESR-0009/RBL-0009). Guardian, Sentinel, Platform Services, User Experience Platform, Knowledge and Provider Architecture all updated from "Not Started"/"Planned" to reflect genuine foundation-scope implementation, each cross-checked against PST-0001 Section 5 and this session's own delivered evidence. Memory, Voice, Vision, Home Automation, Productivity, Multi-device and the JARVIS-internal Engineering Agent confirmed still Not Started - deliberately deferred, not newly discovered gaps. Added a Document Control block and this Refresh History section, neither of which existed before, so future staleness is at least version-trackable. **Observation, not actioned by this refresh**: this document has never been registered in REG-0001 as a controlled artefact (no artefact ID, unlike its sibling PCB-0001) - flagged for a separate Programme Sponsor decision on whether to register it formally. |
| 1.0 | Undated (ESR-0009 era) | Programme Sponsor & Chief Engineering Advisor | Initial matrix created to support ESR-0009 readiness following RBL-0009. |
