# RSC-0001 - v1.0 Readiness Scorecard

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RSC-0001 |
| Title | v1.0 Readiness Scorecard |
| Version | 1.1 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 (Minimum Lovable Product) |
| Approval | Approved by Programme Sponsor |

---

# 2. Purpose

RSC-0001 records a pass/fail-per-capability assessment of JARVIS against the Minimum Lovable Product (MLP 0.1) defined in [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 - the artefact's own stated definition of what "a useful JARVIS that can be enjoyed every day" requires.

This artefact exists because no single controlled artefact previously answered, in one place and against one explicit release-criteria definition, "is JARVIS at v1.0 yet?" [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational baseline and its constraints; [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] tracks per-capability maturity across the full product vision, not specifically MLP 0.1. Neither is structured as a scorecard against explicit release criteria.

This artefact was created following an independent Codex governance/v1.0-readiness gap analysis (`govreview`/`v1_0_gap_analysis`, delivered to the AIEMS Exchange Bridge inbox outside any open engineering session), whose first recommendation was exactly this: "a single explicit v1.0 release-criteria artefact." [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] WP2 and WP3 addressed that review's other findings (documentation staleness, PCB-0001 refresh) first, per the Programme Sponsor's direction; this WP4 addresses the scorecard recommendation.

RSC-0001 does not itself approve, prioritise or schedule any implementation. It records an assessment only. Future engineering priorities remain governed by [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]].

---

# 3. Scoring Method

Each MLP 0.1 item is scored against the live repository (code, tests and controlled artefacts), not against architecture intent or backlog specification-completion alone - a specification being "Complete" (e.g. a GAM-0001 section, an ADR) is not treated as equivalent to the capability itself being implemented and reachable through the live running product.

| Score | Meaning |
|-------|---------|
| **Pass** | Implemented, reachable through the live running product (UXP and/or First Light), and live-verified at least once. |
| **Partial** | Implemented at foundation level only, or reachable but materially incomplete against the MLP item's own description. |
| **Fail** | Not implemented; architecture/specification may exist, but no working code path exists. |

---

# 4. MLP 0.1 Scorecard

Per [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5, MLP 0.1 "shall include" the following eight items.

| MLP 0.1 Item | Score | Evidence |
|--------------|-------|----------|
| GUI Dashboard | **Pass** | Guardian Desktop Platform Shell (Tauri + React, `src/`, `src-tauri/`) is live, packaged as a distributable installer since ESR-0032; capability/diagnostics panels derive from live `platform.status` data. |
| Chat Interface | **Pass** | Live conversation workspace reachable through both the Tkinter First Light shell and the UXP; the UXP chat input calls the real backend over a duplex stdio JSON-RPC bridge (`python -m jarvis --ipc-stdio`, [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]]), not a static mock-up. |
| Text Responses | **Pass** | `GuardianRuntime.converse()` returns real generated or deterministic-fallback text through the same live path as Chat Interface; a real external provider (OpenAI or Gemini) is wired into the default path when credentialed (EBG-0070, ESR-0022), with Ollama and a deterministic local provider as further fallbacks. |
| Animated Avatar / Orb | **Partial** | The Guardian Orb is Guardian's visual presence ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8) and renders the live repository knowledge graph as a 2D force-directed, circle-confined visualisation, genuinely animating today via a continuous `requestAnimationFrame` rotation loop (`src/GuardianOrbGraph.jsx`'s `drawFrame`/`rotateNode`, ESR-0019 WP2) - not a static placeholder. The MLP's "animated" qualifier is therefore met at a basic level; true 3D rendering and knowledge-graph Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) remain not implemented, which is why this is Partial rather than Pass. |
| Basic Voice Input | **Pass** | Push-to-talk microphone capture is implemented (Voice faculty Phase 6 Increment B, `sentinel/whisper_provider.py`/`jarvis/interfaces/voice.py`, EBG-0117, [[EIP-ESR0047-001_VOICE_PHASE6_INCREMENT_B_SPEECH_INPUT_SCOPE|EIP-ESR0047-001]], ESR-0047), Sentinel-gated exactly like the existing speech-output path and reachable through the live UXP's mic button (conditionally rendered on real-time capability detection). Live-verified: Guardian's own Piper-synthesized speech was transcribed back by Guardian's own Whisper path via the real `guardian.transcribe` RPC, exact text match. No wake-word/continuous listening, speaker identification or role enforcement - deliberately out of MLP 0.1's "basic" bar. |
| Basic Conversation Memory | **Pass** | Personal Memory is implemented at foundation level, consent-gated (`jarvis/memory/`, ESR-0027 WP1) and wired into live conversation via the Guardian Cognitive Core, which composes persona, retained Personal Memory and bounded recent conversation history before each provider call (`jarvis/guardian/runtime.py`, ESR-0039). This satisfies the MLP's "basic" qualifier; Session and Shared-Family memory tiers ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3) are a later-phase capability, not part of MLP 0.1's own stated scope. |
| User Profiles | **Pass** | Local, unauthenticated profile create/list/select is implemented (`jarvis/identity/`, EBG-0116, [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]], ESR-0046), role-tagged against [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's four household roles and reachable through a real UXP profile picker replacing the previous static placeholder. Credentialed authentication, memory scoping by profile and enforcement of the roles' differing authority remain not implemented - deliberately deferred, disclosed follow-on work beyond MLP 0.1's "basic" bar. |
| Service Status Dashboard | **Pass** | `platform.status` JSON-RPC method exposes a live service/health model consumed by the UXP's diagnostics panels, not the original lightweight model alone. |

**Score: 7 Pass, 1 Partial, 0 Fail (of 8 MLP 0.1 items).**

---

# 5. Beyond MLP 0.1: Related Gaps Identified by the Triggering Review

The independent Codex `govreview` finding that prompted this artefact also named gaps beyond MLP 0.1's own scope - these belong to later MLP phases ([[JARVIS_PRODUCT_ARCHITECTURE]] Section 10, Product Roadmap: MLP 0.2 through 0.8) and are recorded here for completeness, not scored against MLP 0.1 criteria they were never part of:

| Gap | MLP Phase | Status |
|-----|-----------|--------|
| Richer voice interaction beyond basic push-to-talk input | MLP 0.2 Voice | Basic input now Pass (see above); richer interaction (continuous listening, multi-language, speaker identification) remains not started. |
| Family profile behaviour (Administrator/Adult/Child/Guest differentiation) | MLP 0.3 Family Profiles | User identity/profile plumbing now exists (EBG-0116), but role-authority enforcement against Sentinel/`TrustTierPolicy` remains not implemented - the actual differentiation this MLP phase describes is still not started. |
| Session and Shared Family memory tiers | MLP 0.4 Memory | Not started ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3 specify the architecture; no implementation exists). |
| Local device assistance (Local Agent) | MLP 0.5 Local Agent | Not started - the permission boundary is defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, EBG-0021, ESR-0041), but no Local Agent module exists under `jarvis/`; `Sentinel`'s `TrustCategory.LOCAL_AGENT_ACTION` remains `DENY` for every request today. |
| Controlled internet-assisted capability | MLP 0.6 Internet | Not started. |
| Visual understanding (Vision) | MLP 0.7 Vision | Not started - deferred alongside speech input for the same Household Role Model reason (EBG-0112). |
| Expanded permission, safety, audit and approval controls; full HITL live wiring | MLP 0.8 Guardian | Partially specified, not fully live - GAM-0001's authority model, family-safety principles (EBG-0020) and HITL governance mechanics (EBG-0048) are all approved specifications, but a network-facing Guardian/Sentinel interface does not exist yet ([[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] remains an approved specification with no implementation), and the family-safety/consent mechanics they specify are not wired into a live multi-user flow (there being no user-identity plumbing to wire them into yet). |

---

# 6. Interpretation

JARVIS is **not yet at v1.0** if v1.0 is defined as MLP 0.1 fully delivered, but the gap has narrowed materially since this scorecard's original scoring: both items that scored Fail (Basic Voice Input, User Profiles) are now Pass, resolved at ESR-0047 and ESR-0046 respectively. Only one item, Animated Avatar/Orb, remains short of full Pass - genuinely animating today but not yet 3D or connected to the Guardian Orb knowledge-graph vision's later phases.

The 7 Pass items represent genuine, live-verified capability, not aspirational claims - each cites a specific code path and a live-verification record in its originating Engineering Session Report. The prerequisite this scorecard originally identified (user identity/profile plumbing) has been closed, which is also what unblocked Basic Voice Input's own delivery and now leaves the path clear for Family Profiles (MLP 0.3) and full HITL/family-safety wiring (MLP 0.8), neither of which is itself complete yet - both remain gated on role-authority enforcement, which EBG-0116/EBG-0117 deliberately did not implement.

This artefact does not recommend implementation order - that remains for a future Work Package or Engineering Session, informed by [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]'s existing phase sequencing and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]'s backlog.

---

# 7. Maintenance

RSC-0001 shall be refreshed whenever a Work Package changes the score of any MLP 0.1 item, and reviewed at minimum whenever [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is refreshed, since both draw on the same live repository evidence.

---

# 8. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE]] | Source of the MLP 0.1 release criteria this scorecard assesses against. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product baseline and constraints; shares much of the same underlying evidence. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Broader per-capability maturity tracking across the full product vision, not specifically MLP 0.1; not yet refreshed for ESR-0040/0041/0043/0044 (a pre-existing, separately tracked staleness). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Source of the Household Role Model and Local Agent Permission Boundary referenced in the User Profiles and beyond-MLP-0.1 rows. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Governed source for future engineering priorities; this artefact does not itself prioritise. |
| [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] | Session that created this artefact (WP4), triggered by an independent Codex governance/v1.0-readiness gap analysis. |
| [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] | Delivered EBG-0116 (User Profiles), the first of this scorecard's two Fail items, now Pass. |
| [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] | Delivered EBG-0117 (Basic Voice Input), the second of this scorecard's two Fail items, now Pass. |

---

# 9. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 4 August 2026 | Claude Engineering Implementer | ESR-0048 WP1 (Documentation Debt Discipline), per this artefact's own Section 7 maintenance rule: refreshed both Fail items to Pass - Basic Voice Input (EBG-0117, ESR-0047) and User Profiles (EBG-0116, ESR-0046). Score corrected from 5 Pass/1 Partial/2 Fail to 7 Pass/1 Partial/0 Fail. Section 5's Voice/Family Profiles rows and Section 6's Interpretation updated accordingly. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial RSC-0001 created at ESR-0045 WP4, per the Programme Sponsor's selection of the triggering Codex governance review's first recommendation (a single explicit v1.0 release-criteria artefact). Scored all 8 MLP 0.1 items against live repository evidence: 5 Pass, 1 Partial (Animated Avatar/Orb), 2 Fail (Basic Voice Input, User Profiles). Recorded beyond-MLP-0.1 gaps for completeness. |
