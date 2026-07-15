# JARVIS Capability Readiness Matrix

---

# Document Control

| Field | Value |
|-------|-------|
| Title | JARVIS Capability Readiness Matrix |
| Version | 2.0 |
| Status | Maintained |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Last Refreshed | ESR-0021 WP7 (15 July 2026) |

---

# 1. Purpose

This matrix provides a single engineering view of current JARVIS capability maturity.

It supports product capability prioritisation without approving implementation by itself. Approved package selection remains governed through [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], sequencing guidance in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]], and the active Engineering Session.

---

# 2. Capability Readiness

| Capability | Vision | Architecture | Implementation | Testing | Overall Readiness |
|------------|--------|--------------|----------------|---------|-------------------|
| Conversation | Complete | Complete | Implemented | Implemented | Implemented (Foundation) |
| Intelligence | Complete | Draft | Partial (bounded runtime, no full cognition) | Partial | Planned |
| Memory | Complete | Partial | Not Started | Not Started | Planned |
| Voice | Complete | Partial | Not Started | Not Started | Planned |
| Vision | Complete | Partial | Not Started | Not Started | Planned |
| Guardian | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| Sentinel | Complete | Complete | Implemented | Implemented | Implemented (Foundation) |
| Platform Services | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| User Experience Platform | Complete | Complete | Implemented (Foundation) | Implemented | Implemented (Foundation) |
| Home Automation | Complete | Planned | Not Started | Not Started | Planned |
| Productivity | Complete | Planned | Not Started | Not Started | Planned |
| Engineering Agent (JARVIS-internal specialist agent) | Complete | Partial | Proof of Concept only (GIA-BOOT) | Not Started | Planned |
| Knowledge | Complete | Complete | Implemented (Phase 1-2 of 4) | Implemented | Partial |
| Multi-device | Complete | Planned | Not Started | Not Started | Planned |
| Provider Architecture | Complete | Complete | Implemented (live-validated, unwired from production runtime) | Implemented | Implemented (Foundation) |

---

# 3. Overall Programme Capability Summary

JARVIS has moved well past the early executable foundation this matrix described at ESR-0009. Guardian, Sentinel, Platform Services, the User Experience Platform, Knowledge and Provider Architecture are all now genuinely implemented at foundation scope, not merely architecture-validated:

- **Guardian** has a running runtime foundation (ESR-0013), connected through Sentinel for real conversation (ESR-0017 WP2), reachable through a live, interactive UXP (ESR-0017 WP9), with its own visual presence rendering the live repository knowledge graph (ESR-0019) plus surfaced metrics/cluster panels (ESR-0021 WP4).
- **Sentinel** has a working trust gateway, provider abstraction, audit, policy and trust-tier model, with both OpenAI and Gemini live-validated as real external providers (real billed calls, real generated responses).
- **User Experience Platform** is live and interactive (Tauri + React, real backend bridge), not a disconnected static shell - matching PST-0001's own "Live, Foundation Scope" characterisation.
- **Knowledge** has a real backend graph builder and live-rendered Guardian Orb (Phase 1 complete, Phase 2 partially delivered).
- **Provider Architecture** has two live-validated adapters, though neither is wired into a default/production runtime route yet - a distinct, not-yet-authorised implementation decision (see JRM-0001 Track B Near-term).

**Memory, Voice, Vision, Home Automation, Productivity, Multi-device and a JARVIS-internal specialist Engineering Agent remain not implemented**, consistent with PST-0001's "Outstanding Observations" - these are deliberately deferred, not overlooked. "Intelligence" (full Guardian cognition, beyond the current bounded runtime foundation) also remains architecturally Draft only, per AAM-0001.

JARVIS implementation maturity is now foundation-level-and-live across its core platform capabilities, with product-depth capabilities (memory, voice, vision, automation, multi-device) still ahead.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture source for capability intent and hierarchy. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture context for JARVIS as flagship implementation. |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Current accepted repository baseline. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Sibling document (Product Capability Baseline) refreshed via the same pattern at ESR-0020 (EBG-0056) - this refresh follows that precedent. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture source; still Draft, underlying the Intelligence row's Planned status. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register for candidate package selection; this refresh closes EBG-0069. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Forward-looking sequencing artefact; the Not Started/Planned rows above correspond to items sequenced there. |

---

# 4. Refresh History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0 | 15 July 2026 | Claude Engineering Implementer | Refreshed at ESR-0021 WP7, closing EBG-0069: corrected 13 sessions of staleness (dated to ESR-0009/RBL-0009). Guardian, Sentinel, Platform Services, User Experience Platform, Knowledge and Provider Architecture all updated from "Not Started"/"Planned" to reflect genuine foundation-scope implementation, each cross-checked against PST-0001 Section 5 and this session's own delivered evidence. Memory, Voice, Vision, Home Automation, Productivity, Multi-device and the JARVIS-internal Engineering Agent confirmed still Not Started - deliberately deferred, not newly discovered gaps. Added a Document Control block and this Refresh History section, neither of which existed before, so future staleness is at least version-trackable. **Observation, not actioned by this refresh**: this document has never been registered in REG-0001 as a controlled artefact (no artefact ID, unlike its sibling PCB-0001) - flagged for a separate Programme Sponsor decision on whether to register it formally. |
| 1.0 | Undated (ESR-0009 era) | Programme Sponsor & Chief Engineering Advisor | Initial matrix created to support ESR-0009 readiness following RBL-0009. |
