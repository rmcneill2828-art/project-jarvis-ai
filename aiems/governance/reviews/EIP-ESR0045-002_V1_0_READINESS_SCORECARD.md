# EIP-ESR0045-002 - v1.0 Readiness Scorecard

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0045-002 |
| Artefact ID | EIP-ESR0045-002 |
| Title | v1.0 Readiness Scorecard |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | Independent Codex `govreview`/`v1_0_gap_analysis` finding, recommendation 1 |
| Intended Session | ESR-0045 |
| Effective Date | 30 July 2026 |

---

# 2. Purpose

An independent Codex governance/v1.0-readiness gap analysis (`govreview`/`v1_0_gap_analysis`, delivered to the AIEMS Exchange Bridge inbox outside any open engineering session, addressed at ESR-0045 WP2 and WP3) recommended, as its first "missed opportunity": "create a single explicit v1.0 release-criteria artefact." No existing controlled artefact serves this purpose - [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational baseline and its constraints, and [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] tracks per-capability maturity across the whole product vision - neither is structured as a scorecard against an explicit, named release-criteria definition.

[[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 already defines exactly such a release-criteria set: the Minimum Lovable Product (MLP 0.1), an explicit list of eight items the artefact itself states MLP 0.1 "shall include." This package proposes scoring JARVIS against that existing, Programme-Sponsor-approved definition rather than inventing new criteria.

---

# 3. Objective

Create RSC-0001 (v1.0 Readiness Scorecard) as a new controlled artefact: a pass/fail-per-capability assessment of each MLP 0.1 item against live repository evidence (code, tests, live-verification records in Engineering Session Reports), plus a summary of related gaps beyond MLP 0.1 that the triggering review separately named.

---

# 4. Repository Context

Confirmed directly against the live repository before drafting (not assumed):

| MLP 0.1 Item | Verified Against |
|--------------|-------------------|
| GUI Dashboard | `src/`, `src-tauri/` (Guardian Desktop Platform Shell, live, installer since ESR-0032). |
| Chat Interface | `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` and `guardian.converse`, reachable from the UXP over the stdio JSON-RPC bridge (ADR-0019). |
| Text Responses | Same path as Chat Interface; `_build_real_provider()` wires a credential-gated real provider (EBG-0070). |
| Animated Avatar / Orb | `jarvis/interfaces/knowledge_graph.py`, `src/GuardianOrbGraph.jsx` (`drawFrame`/`rotateNode`, continuous `requestAnimationFrame` rotation loop), [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8 - live, genuinely animated knowledge-graph rendering exists; UAM-0001 Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) remain not implemented. |
| Basic Voice Input | Grepped `jarvis/` and `sentinel/` directly - no speech-input/microphone-capture/speech-to-text code path exists anywhere. `jarvis/interfaces/voice.py` and `sentinel/piper_provider.py` are output-only. |
| Basic Conversation Memory | `jarvis/memory/` (`PersonalMemoryStore`/`PersonalMemoryService`, ESR-0027) and `jarvis/guardian/runtime.py`'s composition of persona/memory/bounded history before each provider call (ESR-0039). |
| User Profiles | Grepped `jarvis/` directly for "profile"/"household"/user-identity code - none found. [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 explicitly states it "does not implement login, identification or access control." |
| Service Status Dashboard | `platform.status` JSON-RPC method, live UXP diagnostics panels. |

---

# 5. Scope

This package authorises creating `aiems/governance/baselines/RSC-0001_V1_0_READINESS_SCORECARD.md` as a new controlled artefact (already drafted in full at v1.0, subject to this review), containing:

- A scoring method (Pass/Partial/Fail, defined against live-reachability and live-verification, not specification-completion).
- A scorecard table for all 8 MLP 0.1 items with cited evidence per row.
- A summary table of related gaps beyond MLP 0.1 (Voice input/richer interaction, Family Profiles, Session/Shared-Family memory, Local Agent, Internet, Vision, expanded Guardian/HITL controls), explicitly not scored against MLP 0.1 criteria they were never part of.
- An interpretation section stating the overall result (5 Pass, 1 Partial, 2 Fail) and observing that the two Fail items and the Family Profiles/full-HITL gaps share a common root prerequisite (user identity/profile plumbing does not exist).
- No implementation prioritisation or scheduling - RSC-0001 explicitly defers that to [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]].

REG-0001 registration for RSC-0001 and this EIP. No `jarvis/`, `sentinel/`, `src/`, `src-tauri/` or `scripts/` file is touched - assessment only, no code change.

---

# 6. Risks and Considerations

- **Scoring accuracy risk**: an inaccurate Pass/Fail score would misinform future prioritisation. Mitigated by citing a specific code path or live-verification record for every row, and by Engineering Reviewer (Codex) design review before this artefact is finalised.
- **Staleness risk**: like PCB-0001, this scorecard will drift as capability changes. Mitigated by an explicit Maintenance section directing it be refreshed whenever a Work Package changes an MLP 0.1 item's score.
- **Scope discipline**: this package deliberately does not propose an implementation order or backlog re-prioritisation, honouring PBK-0001's Engineering Scope Control (report observations separately from implementation) and the Programme Sponsor's direction that this WP is assessment, not a launch-gap backlog (a separate, still-open recommendation from the same triggering review).

---

# 7. Approval

Programme Sponsor approval required before RSC-0001 is created as a controlled artefact, verified via `submit-response` against the real Sponsor Approval Service - chat approval alone is not sufficient.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 30 July 2026**, verified via `submit-response` against the real Sponsor Approval Service. RSC-0001 created as scoped. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Fix round after Engineering Reviewer (Codex) design review - v0.1: Fail with one finding (Animated Avatar/Orb row understated Guardian Orb animation: `src/GuardianOrbGraph.jsx`'s `drawFrame`/`rotateNode` run a continuous `requestAnimationFrame` rotation loop today, not "not implemented"). Corrected in both RSC-0001 and this package; row kept Partial (true 3D rendering and UAM-0001 Phases 2-4 remain not implemented). Resubmitted - **Pass**. |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, submitted for Engineering Reviewer (Codex) design review. |
