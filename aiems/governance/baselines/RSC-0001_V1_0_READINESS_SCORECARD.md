# RSC-0001 - v1.0 Readiness Scorecard

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RSC-0001 |
| Title | v1.0 Readiness Scorecard |
| Version | 1.0 |
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
| Basic Voice Input | **Fail** | No speech input / microphone capture / speech-to-text code path exists anywhere under `jarvis/` or `sentinel/` today. Guardian's Voice faculty (Phase 6 Increment A, ESR-0040, wired into the live UXP at ESR-0044) is speech **output** only; speech input is explicitly deferred as a distinct future increment (EBG-0112) because, unlike output-only voice, it engages [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's Household Role Model. |
| Basic Conversation Memory | **Pass** | Personal Memory is implemented at foundation level, consent-gated (`jarvis/memory/`, ESR-0027 WP1) and wired into live conversation via the Guardian Cognitive Core, which composes persona, retained Personal Memory and bounded recent conversation history before each provider call (`jarvis/guardian/runtime.py`, ESR-0039). This satisfies the MLP's "basic" qualifier; Session and Shared-Family memory tiers ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3) are a later-phase capability, not part of MLP 0.1's own stated scope. |
| User Profiles | **Fail** | No user identification, login or profile-switching code path exists anywhere under `jarvis/` today. [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 defines a Household Role Model (Administrator/Adult/Child/Guest) but explicitly states it does not implement authentication or enforcement - it defines roles and their authority, nothing more. Guardian's current persona addresses a single user by a configured preferred name, explicitly disclosed as a single-user stopgap (ESR-0043), not a profiles system. |
| Service Status Dashboard | **Pass** | `platform.status` JSON-RPC method exposes a live service/health model consumed by the UXP's diagnostics panels, not the original lightweight model alone. |

**Score: 5 Pass, 1 Partial, 2 Fail (of 8 MLP 0.1 items).**

---

# 5. Beyond MLP 0.1: Related Gaps Identified by the Triggering Review

The independent Codex `govreview` finding that prompted this artefact also named gaps beyond MLP 0.1's own scope - these belong to later MLP phases ([[JARVIS_PRODUCT_ARCHITECTURE]] Section 10, Product Roadmap: MLP 0.2 through 0.8) and are recorded here for completeness, not scored against MLP 0.1 criteria they were never part of:

| Gap | MLP Phase | Status |
|-----|-----------|--------|
| Richer voice interaction, speech input | MLP 0.2 Voice | Not started (see Basic Voice Input above). |
| Family profile behaviour (Administrator/Adult/Child/Guest differentiation) | MLP 0.3 Family Profiles | Not started - blocked on the same user-identity plumbing gap as User Profiles above ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1). |
| Session and Shared Family memory tiers | MLP 0.4 Memory | Not started ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3 specify the architecture; no implementation exists). |
| Local device assistance (Local Agent) | MLP 0.5 Local Agent | Not started - the permission boundary is defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, EBG-0021, ESR-0041), but no Local Agent module exists under `jarvis/`; `Sentinel`'s `TrustCategory.LOCAL_AGENT_ACTION` remains `DENY` for every request today. |
| Controlled internet-assisted capability | MLP 0.6 Internet | Not started. |
| Visual understanding (Vision) | MLP 0.7 Vision | Not started - deferred alongside speech input for the same Household Role Model reason (EBG-0112). |
| Expanded permission, safety, audit and approval controls; full HITL live wiring | MLP 0.8 Guardian | Partially specified, not fully live - GAM-0001's authority model, family-safety principles (EBG-0020) and HITL governance mechanics (EBG-0048) are all approved specifications, but a network-facing Guardian/Sentinel interface does not exist yet ([[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] remains an approved specification with no implementation), and the family-safety/consent mechanics they specify are not wired into a live multi-user flow (there being no user-identity plumbing to wire them into yet). |

---

# 6. Interpretation

JARVIS is **not yet at v1.0** if v1.0 is defined as MLP 0.1 fully delivered: 2 of 8 MLP 0.1 items (Basic Voice Input, User Profiles) have no implementation at all, and a third (Animated Avatar/Orb) is only partially met.

The 5 Pass items represent genuine, live-verified capability, not aspirational claims - each cites a specific code path and, where applicable, a live-verification record in its originating Engineering Session Report. The gap is concentrated, not diffuse: Basic Voice Input and User Profiles both trace back to the same underlying prerequisite - user identity/profile plumbing does not exist, which is also why Family Profiles (MLP 0.3) and the full HITL/family-safety wiring (MLP 0.8) remain blocked. Closing that one prerequisite would very likely unblock more than one currently-failing item at once.

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

---

# 9. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial RSC-0001 created at ESR-0045 WP4, per the Programme Sponsor's selection of the triggering Codex governance review's first recommendation (a single explicit v1.0 release-criteria artefact). Scored all 8 MLP 0.1 items against live repository evidence: 5 Pass, 1 Partial (Animated Avatar/Orb), 2 Fail (Basic Voice Input, User Profiles). Recorded beyond-MLP-0.1 gaps for completeness. |
