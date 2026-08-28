# PCB-0001 - Product Capability Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PCB-0001 |
| Title | Product Capability Baseline |
| Version | 2.11 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[JARVIS_PRODUCT_ARCHITECTURE]] |
| Approval | Approved by Programme Sponsor |

---

# 2. Purpose

PCB-0001 records the accepted operational product baseline for JARVIS following review of repository evidence during [[ESR-0007_ENGINEERING_SESSION_REPORT]].

This artefact is an acceptance baseline. It does not replace the repository assessment, product architecture, capability readiness matrix or engineering backlog.

---

# 3. Repository Evidence

PCB-0001 was originally based on independently reviewed repository evidence recorded in [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]] and the accepted repository context established by [[RBL-0007_REPOSITORY_BASELINE]].

This refresh (v2.0) is based on repository evidence gathered across ESR-0013 through ESR-0020, principally: [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] (Sentinel foundation, first live OpenAI validation), [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] (Guardian&harr;Sentinel connection, second provider adapter, live UXP-backend bridge), [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] (Gemini hardening), [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] (repository knowledge-graph backend, Guardian Orb live rendering) and [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] (live Gemini validation). It remains subordinate to [[JARVIS_PRODUCT_ARCHITECTURE]], [[JARVIS_CAPABILITY_READINESS_MATRIX]] and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]] as the authoritative sources for architecture, maturity and backlog respectively - this artefact only records the accepted operational snapshot.

The v2.3 refresh ([[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] WP3) incorporates repository evidence from [[ESR-0022_ENGINEERING_SESSION_REPORT|ESR-0022]] (a real provider wired into the default runtime conversation path, EBG-0070 - discovered stale during this refresh and not itself flagged by the triggering review), [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] (Guardian Voice faculty, Phase 6 Increment A, speech output via self-hosted Piper), [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]] (Local Agent Permission Boundary, GAM-0001 Section 8A), [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] (Guardian Persona refined toward its classic JARVIS characterisation) and [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] (Voice faculty wired into the live JSON-RPC bridge and UXP speak button). Prompted by an independent Codex governance/v1.0-readiness gap analysis (`govreview`/`v1_0_gap_analysis`) that flagged PCB-0001 as not refreshed for the live Voice wiring.

Repository validation confirmed that the following evidence artefacts exist:

- [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]]
- [[RBL-0035_REPOSITORY_BASELINE]] (current accepted repository baseline, established at ESR-0055; superseded RBL-0007 through RBL-0034 since PCB-0001 v1.0)
- [[JARVIS_PRODUCT_ARCHITECTURE]]
- [[JARVIS_CAPABILITY_READINESS_MATRIX]]
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]]

PCB-0001 v1.0 (1 July 2026) was the first Product Capability Baseline. It remained unrefreshed through RBL-0008 to RBL-0013 despite substantial intervening delivery, and was flagged materially stale at [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] Section 6 (tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056). This v2.0 refresh addresses that gap.

---

# 4. Accepted Product Baseline

The Programme Sponsor accepts the following as the current operational JARVIS product baseline:

| Baseline Area | Accepted Position |
|---------------|-------------------|
| First Light foundation | JARVIS has an executable First Light foundation (`python -m jarvis`), unchanged since v1.0. |
| Conversation Workspace | JARVIS provides an operational conversation workspace, reachable through both the legacy Tkinter First Light shell and the live Tauri+React User Experience Platform (UXP). The UXP chat input calls the real backend via a duplex stdio JSON-RPC bridge (`python -m jarvis --ipc-stdio`), not a static mock-up ([[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]], ESR-0017 WP9). A real external provider (OpenAI or Gemini) is wired into this default path when credentialed, with Ollama and the deterministic local provider as further fallbacks (see Section 6). |
| User Experience Platform (UXP) | The Tauri+React UXP is live, not a disconnected shell: capability/diagnostics panels derive from live `platform.status` data, and the Guardian Orb renders the live repository knowledge graph (148+ nodes, 1200+ edges) as a 2D force-directed, circle-confined visualisation with a deterministic hemisphere depth projection (ESR-0019 WP2, [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1 Phase 1). The Tkinter GUI remains the separate, still-functional legacy First Light shell (animated orb placeholder, conversation controls, service status), not superseded by the UXP. True 3D rendering, live animation and knowledge-graph Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) are not implemented. |
| Sentinel (AI Execution and Security Platform) | Implemented under `sentinel/`: trust boundary primitives, provider abstraction/registry, health-aware provider orchestration with automatic failover, audit logging, policy and a trust-tier policy model ([[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]], [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]]). Reachable through the live UXP via `GuardianRuntime.converse()` (ESR-0017 WP2). |
| Provider abstraction framework | A real provider (OpenAI or Gemini, configurable via `JARVIS_PRIMARY_PROVIDER`, default OpenAI per PEM-001) **is wired into JARVIS/Guardian's default runtime conversation path** (EBG-0070, Complete, ESR-0022 WP1), credential-gated and blank-value-safe - absent a configured credential, the path degrades honestly rather than failing. A local Ollama adapter is also registered unconditionally as a further fallback (EBG-0075, ESR-0026), with the deterministic `LocalEchoProvider` retained as the final failover. Both OpenAI and Gemini remain independently live-validated against their real APIs (OpenAI: ESR-0015 WP5; Gemini: hardened ESR-0018, live-validated ESR-0020 WP3). |
| Guardian | Guardian Runtime Foundation is implemented with lifecycle ownership, service status snapshots and bounded observability, connected to Sentinel (`GuardianRuntime.converse()`, ESR-0017 WP2) and reachable through the live UXP. Guardian's Persona has been refined toward its classic JARVIS characterisation - precise/economical phrasing, dry wit, mild reasoned pushback, "Sir"/preferred-name addressing (ESR-0043, [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]). This remains foundation-level Guardian capability, not the full HITL governance, family-safety or emergency-control model AAM-0001 describes (see Section 6). |
| Voice faculty | Guardian's Voice faculty, Phase 6, is implemented for both directions. Speech output (Increment A) uses a self-hosted Piper local-TTS provider (`sentinel/piper_provider.py`, credential/path-gated, no API key or recurring cost - ESR-0040), wired into the live JSON-RPC bridge (`guardian.speak`) and the UXP's speak button (ESR-0044). Speech input (Increment B) uses a self-hosted `faster-whisper` STT provider (`sentinel/whisper_provider.py`, ESR-0047), wired into the live JSON-RPC bridge (`guardian.transcribe`) and a push-to-talk UXP mic button, conditionally rendered on real-time capability detection (`platform.status`'s `transcriptionAvailable` field). Live-verified end to end: Guardian's own Piper-synthesized speech transcribed back by Guardian's own Whisper path, exact text match. No wake-word/continuous listening, speaker identification or role enforcement (see Section 6). |
| User Identity and Profiles | Local, unauthenticated profile create/list/select is implemented (`jarvis/identity/`, ESR-0046), role-tagged against [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's four household roles and reachable through a real UXP profile picker. Credentialed authentication, memory scoping by profile and enforcement of the roles' differing authority remain not implemented (see Section 6). |
| Repository Knowledge Graph | Implemented: `jarvis/interfaces/knowledge_graph.py` parses git-tracked Markdown WikiLinks into a node/edge graph, exposed via the `knowledge.graph` JSON-RPC method (ESR-0019 WP2, EBG-0055 Phase 1). |
| Agent Framework | Implemented at foundation level: `jarvis/agents/` defines the `SpecialistAgent`/`AgentRequest`/`AgentResult` contract; GIA's existing read-only local-resource observability (`LocalResourceObserver`) is wired as the first live specialist agent (`GiaObservabilityAgent`), evaluated through the same shared Sentinel `TrustTierPolicy` gateway every other capability uses and classified `ROUTINE_INTERACTION`, reachable via `guardian.agent.list`/`guardian.agent.invoke` JSON-RPC methods (ESR-0049, EBG-0119). `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` hard `DENY` remains completely untouched - no local-device-control agent is implemented, wired or authorised. No UXP surface exists for invoking it yet. |
| Session lifecycle | JARVIS tracks current-session metadata and supports new conversation and clear conversation behaviour. |
| Transcript export | JARVIS supports user-initiated transcript export in Markdown and plain-text formats, on the Tkinter First Light shell. |
| Health/status model | JARVIS exposes a service status and health model consumed live by the UXP (`platform.status`), in addition to the original lightweight model. |
| Repository governance integration | JARVIS product capability is governed through AIEMS repository evidence, controlled architecture, baseline and backlog artefacts. |

This accepted baseline shall be used as the reference point for future JARVIS product engineering unless superseded by a later accepted Product Capability Baseline.

---

# 5. Capability Maturity

The authoritative capability maturity assessment is maintained within [[JARVIS_CAPABILITY_READINESS_MATRIX]].

PCB-0001 does not duplicate the matrix. Future maturity changes shall be assessed through the authoritative matrix and accepted through appropriate AIEMS baseline or review activity.

---

# 6. Current Constraints

The accepted product baseline includes the following constraints:

- A real external AI provider (OpenAI or Gemini) is wired into JARVIS/Guardian's default runtime conversation path (EBG-0070, ESR-0022), with Ollama and the deterministic local provider as further fallbacks - no provider selection is required for a basic working conversation, only for choosing which external provider is primary.
- Persistent memory: Personal Memory (MDS-0001 Section 6.2) is implemented at foundation level, consent-gated, delivered at ESR-0027 WP1 (EBG-0080); Session Memory (Section 6.1) and Shared Family Memory (Section 6.3) are not yet implemented.
- Voice capability is implemented for both speech output (Phase 6 Increment A, self-hosted Piper, ESR-0040/ESR-0044) and basic speech input (Increment B, self-hosted `faster-whisper`, ESR-0047); no wake-word/continuous listening, multi-language support or speaker identification.
- User identity is implemented at foundation level (local, unauthenticated profile create/list/select, ESR-0046); no credentialed authentication, memory scoping by profile, or enforcement of GAM-0001 Section 8.1's role authority.
- Vision capability is not implemented.
- Guardian capability is implemented only at the foundation level (runtime lifecycle, Sentinel connection, UXP reachability, live knowledge-graph Orb, refined persona) - the full HITL governance, consent/policy, family-safety and pre-approved emergency-action model ([[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], EBG-0031, EBG-0048) is not implemented.
- The Agent Framework has one implemented specialist agent (GIA read-only observability, `ROUTINE_INTERACTION`, ESR-0049) but no UXP surface for invoking it yet. Local-device-control agent capability (the Action faculty) is not implemented. The Local Agent Permission Boundary is defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, ESR-0041) - the policy boundary a future Local Agent/Action faculty implementation must obey - but `LOCAL_AGENT_ACTION` remains a hard `DENY` with no implementation approaching it.
- Internet-backed assistance is not implemented.
- Runtime service health checks are live (`platform.status` feeds the UXP) but remain observational - no active diagnostics, alerting or automated remediation.
- Knowledge-graph Orb rendering is 2D with a depth illusion, not true 3D; live animation and Phases 2-4 (cluster illumination, agent-traversal, Guardian reasoning connection) are not implemented.
- Production sidecar packaging, streaming notifications and a full crash-restart policy for the UXP-backend bridge are not implemented (development-mode process spawning only).

These constraints are accepted baseline limitations. They are not defects in PCB-0001 and shall not be treated as implementation authority.

---

# 7. Future Engineering Direction

Future implementation priorities are governed by [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]].

PCB-0001 does not select, approve or reprioritise backlog items. Future product capability changes shall proceed only through approved engineering work packages or other Programme Sponsor authority.

---

# 8. Operational Acceptance Statement

PCB-0001 v1.0 was accepted by the Programme Sponsor as the operational product baseline for JARVIS following ESR-0007 repository product capability assessment.

**PCB-0001 v2.0 was accepted by the Programme Sponsor on 13 July 2026**, at [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] WP4 closure, following the Engineering Implementer's refresh (addressing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056) and the Engineering Reviewer's review (no material overstatement found, judged conservative if anything).

Acceptance records the current operational foundation and its known constraints. It does not approve expansion beyond the accepted baseline.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]] | Repository product capability evidence supporting this baseline. |
| [[RBL-0007_REPOSITORY_BASELINE]] | Repository baseline context for ESR-0007 product engineering. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT]] | Engineering session context for PCB-0001 creation. |
| [[JARVIS_PRODUCT_ARCHITECTURE]] | Product architecture defining intended JARVIS direction and capability relationships. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX]] | Authoritative capability maturity assessment. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]] | Governed source for future engineering priorities and candidate work. |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.11 | 28 August 2026 | Claude Engineering Implementer | ESR-0055 WP7: corrected the Section 3 current-baseline reference from RBL-0034 to RBL-0035, established at ESR-0055 WP7 (GIA Phase 3b/3c: Repository Health and Register State Observability, completing EBG-0083 Phase 3 in full). Pointer fix only - WP1's own new GIA capability is not yet reflected in this baseline's content, remains open for a future refresh (now two sessions of GIA capability, Phase 3a and 3b/3c, both unreflected here). |
| 2.10 | 28 August 2026 | Claude Engineering Implementer | ESR-0054 WP7: corrected the Section 3 current-baseline reference from RBL-0033 to RBL-0034, established at ESR-0054 WP7 (EBG-0038 Relevance Check; GIA Phase 3a Git State Observability). Pointer fix only - WP2's own new GIA capability is not yet reflected in this baseline's content, remains open for a future refresh. |
| 2.9 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP7: corrected the Section 3 current-baseline reference from RBL-0032 to RBL-0033, established at ESR-0053 WP7 (Active Backlog View Generation; Kokoro Production Voice Wiring). Pointer fix only - WP2's own Kokoro production-voice delivery is not yet reflected in this baseline's content, remains open for a future refresh. |
| 2.8 | 22 August 2026 | Claude Engineering Implementer | ESR-0051 WP7: corrected the Section 3 current-baseline reference from RBL-0031 to RBL-0032, established at ESR-0051 WP7 (Process/Tooling Backlog Cluster; Guardian Orb Phase 2 Cluster Illumination). Pointer fix only - WP2's own Guardian Orb Phase 2 delivery is not yet reflected in this baseline's content, remains open for a future refresh. |
| 2.7 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP7: corrected the Section 3 current-baseline reference from RBL-0030 to RBL-0031, established at ESR-0050 WP7 (Agent Framework UXP Wiring; Sentinel Gate of Durin Architecture Specification). Pointer fix only - WP2's own Agent Framework UXP Wiring delivery is not yet reflected in this baseline's content, remains open for a future refresh. |
| 2.6 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 WP1 (content refresh disclosed as deferred at ESR-0049 WP7): Section 4 gains a new Agent Framework row - `jarvis/agents/` contract, GIA's read-only observability wired as the first live `ROUTINE_INTERACTION` specialist agent, reachable via `guardian.agent.*` RPC, no UXP surface yet. Section 6's "Local agent capability is not implemented" constraint reworded to distinguish the now-implemented Agent Framework (one read-only specialist agent) from the still-untouched `LOCAL_AGENT_ACTION`/Action faculty hard `DENY` boundary. |
| 2.5 | 5 August 2026 | Claude Engineering Implementer | ESR-0049 WP7: corrected the Section 3 current-baseline reference from RBL-0029 to RBL-0030, established at ESR-0049 WP7 (Agent Framework Phase 3, First Specialist Agent). Pointer fix only - the new Agent Framework capability itself is not yet reflected in this baseline's content, remains open for a future refresh. |
| 2.4 | 4 August 2026 | Claude Engineering Implementer | ESR-0048 WP1 (Documentation Debt Discipline): refreshed for ESR-0046 (User Identity and Profile Foundation, `jarvis/identity/`) and ESR-0047 (Voice faculty Increment B, speech input, self-hosted `faster-whisper`). Section 4 gains a new User Identity and Profiles row; Voice faculty row updated to cover both directions. Section 6 constraints updated. Section 3's current-baseline reference corrected RBL-0027 to RBL-0029. |
| 2.3 | 30 July 2026 | Claude Engineering Implementer | ESR-0045 WP3: refreshed for ESR-0040 (Voice faculty, speech output, self-hosted Piper), ESR-0041 (Local Agent Permission Boundary, GAM-0001 Section 8A), ESR-0043 (Guardian Persona refinement) and ESR-0044 (Voice faculty wired into the live JSON-RPC bridge and UXP speak button) - prompted by an independent Codex governance/v1.0-readiness gap analysis flagging PCB-0001 as not refreshed for the live Voice wiring. Also caught and corrected staleness the triggering review itself missed: Section 4's Provider abstraction framework row and Section 6's first constraint both still claimed no external provider was wired into the default runtime conversation path, despite EBG-0070 (ESR-0022) having wired one over a month earlier - corrected, and Ollama's fallback registration (EBG-0075, ESR-0026) added. Removed a duplicate "Local agent capability is not implemented" bullet, merged into the GAM-0001 Section 8A constraint. |
| 2.2 | 20 July 2026 | Claude Engineering Implementer | ESR-0031 WP0 repository synchronisation: corrected Section 6's blanket "Persistent memory is not implemented" constraint, stale since ESR-0027 WP1 delivered Personal Memory (EBG-0080) - now correctly distinguishes the implemented Personal tier from the still-unbuilt Session and Shared Family tiers. |
| 2.1 | 13 July 2026 | Claude Engineering Implementer | Status In Review to Accepted - the Programme Sponsor accepted the v2.0 refresh at ESR-0020 WP4 closure, following Engineering Reviewer review (no material overstatement, judged conservative). |
| 2.0 | 13 July 2026 | Claude Engineering Implementer | Refreshed to reflect current repository evidence (ESR-0013 through ESR-0020), addressing EBG-0056 (flagged materially stale at RBL-0013): Sentinel/Guardian foundation, live Tauri+React UXP with real backend bridge and knowledge-graph Orb, two live-validated external provider adapters (neither wired into the default runtime path), refreshed constraints. Status set to In Review pending Programme Sponsor acceptance. |
| 1.0 | 1 July 2026 | Codex Engineering Implementer | Initial Product Capability Baseline created following RPCA-0001 repository product capability assessment. |
