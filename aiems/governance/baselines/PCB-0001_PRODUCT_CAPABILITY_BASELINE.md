# PCB-0001 - Product Capability Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PCB-0001 |
| Title | Product Capability Baseline |
| Version | 2.1 |
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

Repository validation confirmed that the following evidence artefacts exist:

- [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]]
- [[RBL-0014_REPOSITORY_BASELINE]] (current accepted repository baseline; superseded RBL-0007 through RBL-0013 since PCB-0001 v1.0)
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
| Conversation Workspace | JARVIS provides an operational conversation workspace, reachable through both the legacy Tkinter First Light shell and the live Tauri+React User Experience Platform (UXP). The UXP chat input calls the real backend via a duplex stdio JSON-RPC bridge (`python -m jarvis --ipc-stdio`), not a static mock-up ([[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]], ESR-0017 WP9). The default conversation path remains the deterministic local provider; external providers are not wired into this default path (see Section 6). |
| User Experience Platform (UXP) | The Tauri+React UXP is live, not a disconnected shell: capability/diagnostics panels derive from live `platform.status` data, and the Guardian Orb renders the live repository knowledge graph (148+ nodes, 1200+ edges) as a 2D force-directed, circle-confined visualisation with a deterministic hemisphere depth projection (ESR-0019 WP2, [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1 Phase 1). The Tkinter GUI remains the separate, still-functional legacy First Light shell (animated orb placeholder, conversation controls, service status), not superseded by the UXP. True 3D rendering, live animation and knowledge-graph Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) are not implemented. |
| Sentinel (AI Execution and Security Platform) | Implemented under `sentinel/`: trust boundary primitives, provider abstraction/registry, health-aware provider orchestration with automatic failover, audit logging, policy and a trust-tier policy model ([[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]], [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]]). Reachable through the live UXP via `GuardianRuntime.converse()` (ESR-0017 WP2). |
| Provider abstraction framework | Two external provider adapters are implemented and independently live-validated against their real APIs: OpenAI (validated ESR-0015 WP5) and Google Gemini (hardened ESR-0018; live-validated ESR-0020 WP3 - real generated response received, Policy decision Allow). **Neither is wired into JARVIS/Guardian's default runtime conversation path** - both remain reachable only through dedicated manual validation scripts (`scripts/wp5_first_conversation_demo.py`, `scripts/gemini_provider_smoke_test.py`), not the product's everyday conversation flow. The deterministic local provider remains the only provider in the default path. |
| Guardian | Guardian Runtime Foundation is implemented with lifecycle ownership, service status snapshots and bounded observability, connected to Sentinel (`GuardianRuntime.converse()`, ESR-0017 WP2) and reachable through the live UXP. This is foundation-level Guardian capability, not the full HITL governance, family-safety or emergency-control model described in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] (see Section 6). |
| Repository Knowledge Graph | Implemented: `jarvis/interfaces/knowledge_graph.py` parses git-tracked Markdown WikiLinks into a node/edge graph, exposed via the `knowledge.graph` JSON-RPC method (ESR-0019 WP2, EBG-0055 Phase 1). |
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

- External AI providers (OpenAI, Gemini) are implemented and live-validated but not wired into JARVIS/Guardian's default runtime conversation path - both remain opt-in, manual-script-only.
- Persistent memory is not implemented.
- Voice capability is not implemented.
- Vision capability is not implemented.
- Guardian capability is implemented only at the foundation level (runtime lifecycle, Sentinel connection, UXP reachability, live knowledge-graph Orb) - the full HITL governance, consent/policy, family-safety and pre-approved emergency-action model ([[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], EBG-0031, EBG-0048) is not implemented.
- Local agent capability is not implemented.
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
| 2.1 | 13 July 2026 | Claude Engineering Implementer | Status In Review to Accepted - the Programme Sponsor accepted the v2.0 refresh at ESR-0020 WP4 closure, following Engineering Reviewer review (no material overstatement, judged conservative). |
| 2.0 | 13 July 2026 | Claude Engineering Implementer | Refreshed to reflect current repository evidence (ESR-0013 through ESR-0020), addressing EBG-0056 (flagged materially stale at RBL-0013): Sentinel/Guardian foundation, live Tauri+React UXP with real backend bridge and knowledge-graph Orb, two live-validated external provider adapters (neither wired into the default runtime path), refreshed constraints. Status set to In Review pending Programme Sponsor acceptance. |
| 1.0 | 1 July 2026 | Codex Engineering Implementer | Initial Product Capability Baseline created following RPCA-0001 repository product capability assessment. |
