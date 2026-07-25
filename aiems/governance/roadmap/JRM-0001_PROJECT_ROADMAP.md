# JRM-0001 - Project Roadmap

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | JRM-0001 |
| Title | Project Roadmap |
| Version | 1.20 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | CHR-0001 |
| Created During | ESR-0021 WP5 |

---

# 2. Purpose

JRM-0001 is the forward-looking sequencing artefact for Project JARVIS AI. It answers a question no existing controlled artefact answers on its own: given everything already identified, in roughly what order should it happen, and why.

It closes three backlog items that have sat unactioned since early in the programme, each asking for a version of this same thing:

* EBG-0012 - Establish AIEMS roadmap and release planning artefact (Approved Backlog, ESR-0002).
* EBG-0027 - JRM-0001 JARVIS Product Roadmap (Candidate Backlog, ESR-0005) - this artefact takes the reserved `JRM-0001` identifier, broadened from a JARVIS-only scope to the unified roadmap the Programme Sponsor directed at ESR-0021 WP5.
* EBG-0028 - UXP Evolution Roadmap (Candidate Backlog, ESR-0005/ESR-0008/ESR-0010).

Per PBK-0001's Feature-First Delivery Discipline ("Minimise Controlled Artefact Creation"), these three are consolidated into one artefact with three tracks rather than three separate documents that would restate the same sequencing logic from three angles - the exact failure mode EBG-0058 already identifies elsewhere in PBK-0001.

---

# 3. Relationship to Other Artefacts

JRM-0001 owns sequencing and phasing. It does not own backlog item detail, current programme state, or vision-to-implementation traceability - those remain the responsibility of the artefacts below, per the Repository Documentation Principle (every controlled artefact has one primary responsibility).

| Artefact | What it owns | How JRM-0001 uses it |
|----------|---------------|----------------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Full detail, status and disposition of every backlog item (EBG-####). | JRM-0001 references EBG IDs and summarises sequencing rationale only. EBR-0001 remains authoritative for what each item actually means. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme state - what is implemented, what session is active, current baseline. | JRM-0001's Section 5 Capability Roadmap table is the current-state snapshot this roadmap sequences forward from. JRM-0001 does not duplicate it. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Backward traceability - how implemented capability traces back to product vision. | Complementary, opposite direction: PVTM-0001 explains why something that exists, exists; JRM-0001 explains what doesn't exist yet, and in what order it should. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture, including the Section 8.1 Guardian Orb phased design. | Track C (UXP Evolution) sequences against UAM-0001's existing phase definitions rather than redefining them. |
| [[CHR-0001_PLATFORM_CHARTER|CHR-0001]] | Platform charter and programme-level authority. | JRM-0001 is registered as a child of CHR-0001, matching EBR-0001's own parent. |

---

# 4. Roadmap Principles

1. JRM-0001 is advisory. It does not itself authorise implementation - matching EBR-0001's own Section 3 principle. No Engineering Implementation Package may cite JRM-0001 alone as authorisation; Programme Sponsor approval remains required as normal.
2. Sequencing is expressed as horizons (Near-term, Mid-term, Longer-term, Not Yet Justified) for Track A and Track C, or as an explicit numbered dependency-chain (Track B, since ESR-0034 WP3 - see Section 7.3) where a genuine build order exists rather than an independent priority ranking. Neither form commits to fixed ESR numbers or dates. AIEMS sessions are opened ad hoc based on Programme Sponsor availability and priority, not a calendar - committing to "EBG-0012 in ESR-0024" would be false precision.
3. JRM-0001 references backlog items by ID and states sequencing rationale only. It does not restate EBR-0001 content. Where an EBG item's own note already contains phased detail (for example EBG-0028's four-phase Guardian Orb roadmap), JRM-0001 points to it rather than duplicating it.
4. JRM-0001 is reviewed at engineering session transition, alongside EBR-0001, per Continuous Repository Synchronisation. It is expected to need frequent revision in its early versions, the same way PVTM-0001 has remained Draft/iterating since ESR-0008.
5. Every Engineering Session Report should note, at closure, whether that session's delivered work moves JRM-0001's near-term horizon forward - this is how the roadmap stays connected to actual per-session backlog selection rather than becoming a document nobody consults.

---

# 5. Backlog Alignment Findings (ESR-0021 WP5 Audit)

Building this roadmap required auditing the full backlog register for currency. Two stale entries were found, unrelated to the roadmap items themselves but surfaced by the same evidence-gathering pass:

* **EBG-0003** (Lifecycle review of COC-0001) and **EBG-0004** (Lifecycle review of PBK-0001) both still show `Approved Backlog` status in EBR-0001's Section 5 table, despite COC-0001 and PBK-0001 both having been promoted from Draft to Approved at ESR-0020 - repeatedly documented as "EBG-0004 resolved" in PST-0001, EIP-ESR0020-001 and the ESR-0020 session report itself, but never reflected in the backlog register's own Status column. Corrected to `Completed` as part of this WP, per EBR-0001's own Section 12 maintenance trigger ("when the Programme Sponsor directs a backlog review" - this roadmap construction is exactly that).
* **EBG-0018** (JARVIS AI Provider Abstraction Architecture, Candidate Backlog since ESR-0004) appears substantially satisfied by the Sentinel provider abstraction now implemented (`sentinel/` provider registry, capability resolution, OpenAI/Gemini/local adapters, live-validated per PST-0001 Section 5). Not marked Completed by this WP - the original request was an architecture-definition activity distinct from the implementation that followed it, and closing it is a Programme Sponsor judgement call, not an automatic inference. Flagged here as a Near-term candidate for that judgement (Section 6.2). **Resolved at ESR-0023 WP1**: closed as Completed in EBR-0001, Engineering Reviewer confirmed.

---

# 6. Track A - AIEMS Process Roadmap

Governs AIEMS itself: standards, workflow, registers, roles. Sourced from EBR-0001's Approved Backlog and process-related Candidate Backlog items.

## 6.1 Near-term

| Item | Rationale |
|------|-----------|
| EBG-0058 - PBK-0001 Clause Consolidation | Already Approved Backlog; directly addresses accretion risk in the document governing every session. Programme Sponsor-raised, highest process-hygiene value of anything currently open. |
| REG-0001 HST/FCH registration gap (unnumbered - see Section 9) | Deferred to an ESR-0021 WP per Programme Sponsor direction (EIP-ESR0021-002 Section 12); small, mechanical, should not linger. |
| EBG-0005 - REG-0001 metadata alignment following P2-004A | Long-approved, low effort, closes a historical gap. |
| EBG-0065 - STD-0006 Configuration and Secrets Standard | Discovered at ESR-0021 WP6; named at project bootstrapping but never created. Elevated to Near-term because it is no longer theoretical - Sentinel's `CredentialReference` mechanism is live-tested and capable of using real OpenAI/Gemini API keys whenever the Programme Sponsor sets them as a temporary environment variable for a session (confirmed no such key is persistently configured anywhere on the Programme Sponsor's machine, per ESR-0027 closure discussion). ESR-0027 also added a real local SQLite personal-memory store, another category of locally-held data this standard should cover. The longer this stays undocumented, the more implicit practice it has to retroactively capture. |
| EBG-0068 - Engineering Implementation Brief (EIB) artefact type, adopt or drop | Discovered at ESR-0021 WP6. Not a build item - a quick judgement call (confirm EIB was superseded by the EIP convention that followed it, mark Superseded, close). Cheapest possible win in this roadmap; no reason to leave it open. |
| EBG-0057 - Claude<->Codex Engineering Bridge | **Resolved at ESR-0025 WP1**: MVP implemented per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2 (v1.0 implemented; three post-implementation Engineering Reviewer findings - path-traversal, unchecked validation exit codes, a TOCTOU race on the authorisation check - addressed across v1.1-v1.2), closed Complete in EBR-0001. `scripts/aiems_bridge.py` - five commands, role-locking enforced as a real code gate. REA remains this item's own future-phase scope, not yet actioned. |

## 6.2 Mid-term

| Item | Rationale |
|------|-----------|
| EBG-0008 - Engineering Implementation Package Standard | Would formalise a pattern (EIP structure) already used consistently for 20+ sessions in practice but never standardised - codifying existing practice rather than inventing new process. |
| EBG-0009 - Engineering Session Standard | Same rationale as EBG-0008, for session lifecycle rather than EIP structure. |
| EBG-0010 - Repository metadata / cross-reference validation rules | Natural precursor to EBG-0014 (validation automation) - sequence before it. |
| EBG-0013 - Engineering Decision Index | Growing ADR/decision count (20+ ADRs) makes this increasingly valuable; not urgent yet. |
| EBG-0018 closure judgement (see Section 5) | Programme Sponsor decision on whether Sentinel's provider abstraction satisfies this item's original architecture-definition intent. **Resolved at ESR-0023 WP1** - closed Completed. |
| EBG-0059 - Engineering Assurance Capability (EAC/EAA/EAR) | Discovered at ESR-0021 WP6. The highest-value item this audit surfaced: a complete, previously-adversarially-reviewed architecture spec for independent process verification, directly addressing the exact failure mode behind ESR-0020's two self-disclosed process deviations (a human had to catch them). Not Near-term only because it is a substantial build (WP4.1-4.7 in its own original plan), not a quick fix - but it should not sit as long as it already has. |
| EBG-0061 - Engineering Workspace Standard (EWS-0001) | Discovered at ESR-0021 WP6. Real content already exists from ESR-0010 (tool-responsibility matrix still reflecting operative practice); this is a formalisation pass, not new design work. |
| EBG-0063 - TMP-0002 Engineering Session Chat Summary Template | Discovered at ESR-0021 WP6. Natural companion to EBG-0009 above - action together for one combined session-documentation pass rather than two separate sessions touching the same area. |
| EBG-0066 - AIEMS Maturity Model / Index | Discovered at ESR-0021 WP6; independently proposed twice in early sessions. Complements PBK-0001's existing "JARVIS Development Readiness Assessment" question and EBG-0033 (AIEMS Improvement Register) - consider scoping all three together. |

## 6.3 Longer-term / Not Yet Justified

| Item | Rationale |
|------|-----------|
| EBG-0014 - Repository validation automation | Explicitly gated on EBG-0010 first; premature until that baseline exists. |
| EBG-0011 - AI Roles and Capability Matrix | Valuable once the AI collaborator set stabilises further; currently still evolving (this session's own ChatGPT-via-VS-Code/"Codex" venue question is a live example of that evolution). |
| EBG-0032 - Historical Engineering Register | Nice-to-have; GDE-0001's knowledge tiering already substantially addresses the underlying need (bounded session-start review, Historical Archive on demand). |
| EBG-0033 - AIEMS Improvement Register | Candidate Backlog since ESR-0005, never picked up; EBR-0001 and Section 8 entries in EE-0001 have informally covered this need so far. |
| EBG-0034, EBG-0035, EBG-0036, EBG-0037 - authority/context/verification/classification refinements | All Candidate Backlog since ESR-0005, all reasonable, none blocking current work. Batch for a future dedicated governance-hygiene session rather than one-at-a-time. |
| EBG-0038 - Formal AIEMS Standards Review | Explicitly about validating whether ESR-0006-era working practices (RFEP, RFDP, Continuous Repository Synchronisation, Engineering Ecosystem Synchronisation) deserve formal standard status. Reasonable but not urgent - these practices are functioning as working practices. |
| EBG-0040, EBG-0043, EBG-0044 | Documentation/workflow-guidance items; useful, not blocking. |
| EBG-0052 - Execute After Approval Principle | Candidate since ESR-0017; overlaps conceptually with material EBG-0058 will already touch (Approval Before Change restatements) - resolve together. |
| EBG-0060 - Direct ChatGPT Execution (DCE) / Repository Execution Agent (REA) | Discovered at ESR-0021 WP6. Conceptually predated and overlapped EBG-0057 (moved to Near-term, Section 6.1). **Resolved post-ESR-0024 closure**: DCE (single-AI direct execution) marked Superseded by EBG-0057's two-AI handover architecture - ESR-0023's write-boundary incidents are direct empirical evidence against it. REA (execution-automation agent) folded into EBG-0057's future-phase scope rather than retained as a competing item. No longer Longer-term/Not Yet Justified in the DCE sense; the REA idea now lives inside EBG-0057's own scope. |
| EBG-0062 - CPS-0001 Codex Prompt Standard | Discovered at ESR-0021 WP6. Lowest priority of the newly-discovered items per its own backlog note - 20+ sessions of established EIP convention have substantially met the original need even without a named standard. |
| EBG-0064 - ISTL-0001 Engineering Inter-Session Task Register | Discovered at ESR-0021 WP6. Likely substantially satisfied already by PST-0001 Section 8 (Active and Next Planned Work) and EBR-0001 itself - action only if a real gap is confirmed, not by default. Overlaps EBG-0033 above. |
| EBG-0067 - Dropped ADR-0007 topics (JARVIS UI Architecture Strategy; AIEMS Knowledge Architecture) | Discovered at ESR-0021 WP6. The UI-strategy question looks substantively resolved by the later real ADR-0007/ADR-0019 UXP decisions; the knowledge-architecture/relationship-vocabulary question is less clearly resolved elsewhere. Needs a judgement call on whether either is still a live gap before any implementation work, not a build item in itself. **Resolved at ESR-0023 WP1**: split disposition applied - UI Architecture Strategy sub-topic judged Superseded; AIEMS Knowledge Architecture/relationship-vocabulary sub-topic confirmed as a genuine live gap, promoted to Approved Backlog scoped to that remaining sub-topic. No longer Longer-term/Not Yet Justified - re-sequence in a future roadmap refresh. |

---

# 7. Track B - JARVIS Product Capability Roadmap

Governs JARVIS/Guardian/Sentinel product capability. Current state is PST-0001 Section 5's authority; this section sequences what is not yet there.

**Rewritten at ESR-0034 WP3** (Programme Sponsor-directed), replacing the prior Near/Mid/Longer-term horizon buckets below with an explicit dependency-chain model. The horizon-bucket approach had gone stale relative to real delivery (it still listed EBG-0019/Memory as pending Mid-term work after EBG-0080 had already built the real Personal Memory tier, among other gaps) and, more fundamentally, obscured genuine build *order* - several items are not independently prioritisable, they are strictly sequenced by what they need to exist first. The phase model below states that ordering explicitly. Horizons remain the right tool for Track A (process work has no comparable dependency chain); Track B's product-capability path does not.

## 7.1 Near-term

| Item | Rationale |
|------|-----------|
| Guardian Cognitive Core (Phase 1 of the Path to a Working Version, Section 7.3) | **EBG-0108 registered at ESR-0035 WP2** (Approved Backlog) - AAM-0001 remains Approved as architecture only; no implementation is yet authorised. The single most consequential open item in Track B; a future session should action EBG-0108 via its own Engineering Implementation Package. |

## 7.2 Foundation (Delivered)

Not sequenced further - already landed and not revisited by this roadmap. Sentinel trust gateway with `TrustTierPolicy` wired into the production default (EBG-0074); a live provider wired into the default conversation route with local failover (EBG-0070, EBG-0075); Personal Memory, a real consent-gated SQLite tier (EBG-0080); GIA Phase 1, local resource/engineering-environment observability (EBG-0083 Phase 1 of 4); the UXP-backend bridge including streaming notifications (EBG-0050, EBG-0099); Guardian Desktop distribution, CI and release automation (EBG-0102/0103/0104, Theme 1 in full); GAM-0001's authority/HITL/family-safety model (EBG-0031/0020/0048); JARVIS Product Requirements/Capability Backlog and Cost Strategy/Framework work (EBG-0017, 0024, 0045, 0049, all Complete at ESR-0028 WP2/WP3).

## 7.3 Path to a Working Version - Phased Dependency Chain

Each phase requires the one(s) before it. Phase numbering is sequencing, not priority ranking within a phase.

| Phase | Item(s) | Why it sits here |
|-------|---------|-------------------|
| **1** | Guardian Cognitive Core | **EBG-0108 registered at ESR-0035 WP2** (Approved Backlog) - AAM-0001 remains Approved as architecture only; Guardian today routes messages to a provider with no persistent persona or memory-informed reasoning loop. The single most consequential gap in the whole roadmap - every phase below either extends it or depends on it existing. No implementation is authorised by EBG-0108's registration itself; a future session should action it via its own Engineering Implementation Package. |
| **2** | EBG-0021 - Local Agent Permission Boundary | Promoted to Approved Backlog at ESR-0034 WP2. Must be defined before any action-taking capability exists, per its own text and GAM-0001 - the boundary comes first, not concurrently with or after the capability it constrains. |
| **3** | Action faculty (implementation) | **No backlog item yet builds this either** - EBG-0021 (Phase 2) only defines the boundary. Depends on Phase 1 (something must decide what to act on) and Phase 2 (the constraint it must obey). STD-0006 (EBG-0065, see Section 7.4) should land before this phase ships, not after. |
| **4** | Memory expansion: Session and Shared-Family tiers (extends MDS-0001/EBG-0019 beyond the Personal tier); EBG-0023 - Backup, Recovery and Data Protection | EBG-0023 promoted to Approved Backlog at ESR-0034 WP1, on the basis that its stated prerequisite (EBG-0019/MDS-0001) is Complete - it naturally follows here, since there is little worth backing up beyond the repository itself until this phase lands. |
| **5** | Knowledge Graph Phases 2-4 (EBG-0055) | Phase 3 (agent-traversal animation) is explicitly blocked on GIA telemetry beyond Phase 1 (EBG-0083 Phases 2-4, not yet delivered); Phase 4 (Guardian reasoning connection) additionally depends on Phase 1 above existing. |
| **6** | Voice/Vision | **No backlog item yet registered.** Sits after the cognitive core exists (Phase 1) - otherwise it is just a different input modality into a shell with nothing behind it. EBG-0081 Question 1's shared animation scheduler (Section 7.4) is now delivered (ESR-0035 WP3), so this phase's future animated UI surfaces (e.g. a voice waveform) have a shared clock to register with rather than needing their own. |
| **7** | EBG-0046 - Device Independence and Restore Architecture | Promoted to Approved Backlog at ESR-0034 WP1. ADR-0012's architecture decision is already made; matters most once Phase 4 gives there something meaningfully more state to carry across devices. |
| **8** | EBG-0025 - Home Assistant / Smart Home Integration Assessment | Promoted to Approved Backlog at ESR-0034 WP1. Same shape as Phase 6 - another additive integration once the core (Phases 1-4) exists to integrate with. Not a hard dependency on Phase 6 specifically; the two can proceed in either order once Phase 4 is done. |

## 7.4 Cross-Cutting Constraints

Not phase-gated themselves - apply across whichever phases are in flight when they become relevant.

| Item | Constraint |
|------|------------|
| EBG-0065 - STD-0006 Configuration and Secrets Standard | Promoted to Approved Backlog at ESR-0034 WP1. Becomes materially relevant starting at Phase 3 (an acting agent needs disciplined credential handling) and again at Phase 7 (secrets syncing across devices). Should be actioned before Phase 3 ships, not treated as background debt. |
| EBG-0081 Question 1 - UXP shared animation scheduler | **Delivered at ESR-0035 WP3**: `src/animationScheduler.js` (new) provides a single shared `requestAnimationFrame` loop that `GuardianOrbGraph.jsx` now registers with instead of running its own; the loop starts lazily on first subscriber and stops on last unsubscribe. Question 2 (Canvas migration) was already delivered at ESR-0029 WP2. Both questions now closed - this constraint is satisfied ahead of Phase 6/8 adding new animated UI surfaces (voice waveform, smart-home widgets), which can register with the existing scheduler rather than needing their own. |

## 7.5 Parallel - Not Gated By, and Not Gating, the Phases Above

| Item | Rationale |
|------|-----------|
| EBG-0042 - Agent Framework Architecture | ADR-0011 exists; matures naturally once Phases 1-3 exist to define specialist agent contracts against. Left Candidate Backlog - not confidently ready before then. |
| EBG-0059 - Engineering Assurance Capability (EAC/EAA/EAR) | A complete, previously adversarially-reviewed architecture spec for independent process verification. Unblocks once GIA (Phase 5's prerequisite) matures further - left Candidate Backlog, cross-referenced to EBG-0055 Phase 3's own GIA dependency. |
| EBG-0047 - Sentinel Gate of Durin Architecture Specification | Extends EBG-0030 (Completed). Worth revisiting as trust-tier work (EBG-0074) sees further production use - left Candidate Backlog, not confidently satisfied by the current Sentinel Core implementation as of its last review. |
| EBG-0022 - JARVIS AIEMS Knowledge Capability | Self-referential (JARVIS explaining AIEMS itself), not a phase dependency in either direction. Promoted to Approved Backlog at ESR-0034 WP1; action whenever convenient. |

## 7.6 Explicitly Out of Scope for This Track

EBG-0008, 0011, 0038, 0040, 0061, 0066, 0067 (Track A - AIEMS governance/standards debt); EBG-0090-0096, 0106 (AIEMS engineering-tooling backlog, all promoted at ESR-0034 WP1); EBG-0029 (Product Growth Philosophy, documentation-only); EBG-0052 (Execute After Approval Principle, process discipline); EBG-0054 (Dev-Environment Setup Automation). None of these change whether JARVIS/Guardian functions as a product - they govern the engineering process that builds it, not the product itself. See Track A (Section 6) for the first group.

---

# 8. Track C - UXP Evolution Roadmap

EBG-0028 already carries substantial phased content for the Guardian Orb specifically (Phase 1 static graph, Phase 2 cluster colours/chat UI, Phase 3 agent-traversal animation, Phase 4 Guardian reasoning connection). This section sequences that alongside the rest of the live UXP rather than replacing it.

## 8.1 Delivered

| Phase / Item | Status |
|---|---|
| EBG-0050 - UXP-Backend Bridge (foundation scope) | Completed at ESR-0017 WP9. |
| EBG-0055 Phase 1 - static live knowledge graph as the Orb's visual presence | Completed at ESR-0019 WP2. |
| EBG-0028 Phase 2 (cluster colours surfaced as their own panel) | Substantially delivered at ESR-0021 WP4 (Knowledge Metrics + Active Clusters panels) - the underlying cluster-colour data existed since ESR-0019 but was never surfaced as a panel until this session. Status label on EBG-0055 left unchanged pending a future session's explicit judgement on whether this fully closes Phase 2 (chat UI was already present beforehand). |

## 8.2 Near-term

| Item | Rationale |
|------|-----------|
| System Health panel (using only real fields: Guardian, Sentinel, Providers from `platform.status`) | Directly identified during ESR-0021 WP4 scoping as buildable now without violating the no-mock-fallback rule, deliberately deferred to a future WP rather than bundled into WP4's minor scope. **Delivered at ESR-0022 WP1** per [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] v1.0, paired with EBG-0070 (Track B) in the same package; registered as EBG-0072 in EBR-0001, Complete. |
| EBG-0050 remaining scope: streaming notifications | **Delivered at ESR-0031 WP2** per [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] as EBG-0099 - the UXP-backend bridge's first live-push mechanism, closing this remaining EBG-0050 scope. Corrected here (ESR-0034 WP3) - this row previously described it as still pending. |
| EBG-0073 - UXP Duplicate Monitoring Elements Tidy-up | Discovered directly by the Programme Sponsor viewing the live app after EBG-0072 shipped: `SystemHealthPanel` and `DiagnosticsPanel` now visibly duplicate Guardian/Sentinel/Providers rows. Low-risk consolidation, no new backend work needed - a natural quick follow-on to EBG-0072 rather than a standalone design effort. **Resolved at ESR-0023 WP6**: duplication removed, closed Completed in EBR-0001. |

## 8.3 Mid-term

| Item | Rationale |
|------|-----------|
| EBG-0055 Phase 1.5 / next continuation - true 3D rendering and live animation of the Orb | Explicitly deferred by Programme Sponsor decision at ESR-0019 ("doesn't have to be perfect first time"); a future EIP should clarify whether this becomes explicit Phase 1.5 scope or folds into Phase 3, per EBG-0055's own note. |
| EBG-0050 remaining scope: production sidecar packaging (`tauri-plugin-shell`) | **Delivered at ESR-0032 WP1** as its own promoted item, EBG-0102 (Guardian Desktop Distribution Foundation) - a real PyInstaller sidecar, `tauri-plugin-shell` wiring, and installer build. Corrected here (ESR-0034 WP3) - this row previously described it as not yet urgent/undelivered. |
| Real-Time Activity feed (mock-up panel) | No backend event/activity log exists yet - this is new backend work, not a UXP-only increment, and should be scoped as such rather than attempted as a "quick" UXP session. |

## 8.4 Longer-term / Blocked

| Item | Rationale |
|------|-----------|
| EBG-0055 Phase 3 - agent-traversal animation | Explicitly blocked on GIA telemetry beyond Phase 1. **Corrected here (ESR-0034 WP3)**: GIA is no longer only a Proof of Concept - EBG-0083 Phase 1 (local resource/engineering-environment observability) delivered in full at ESR-0029 WP3/WP4/WP6/WP7. Phases 2-4 (platform, engineering-repository and external instrumentation) remain undelivered; Phase 3 cannot proceed until those land - see Track B Section 7.3 Phase 5. |
| EBG-0055 Phase 4 - Guardian reasoning connection | Depends on Phase 3 and on Guardian Cognitive Architecture (currently Draft, per PST-0001 Section 5) maturing beyond its current bounded-runtime-foundation scope. |

---

# 9. Unnumbered Items Requiring an EBG Identifier

Two items are referenced repeatedly across sessions without ever being assigned their own EBR-0001 entry. This roadmap does not mint them itself - EBR-0001 remains the register's own authority - but flags them so a future session closes the gap:

1. ~~**Wiring a live provider into a production `ProviderOrchestrator` route.**~~ Mentioned as "a candidate future backlog item, not yet raised as its own EBG entry" in PST-0001 across ESR-0018 through ESR-0020. **Registered as EBG-0070 and delivered at ESR-0022 WP1** per EIP-ESR0022-001 v1.0 (see Section 7.1).
2. **REG-0001 HST/FCH registration gap** (HST-0015 through HST-0020, FCH-0020_GPT missing from REG-0001's artefact table despite the files existing). Surfaced at ESR-0021 WP4 (EIP-ESR0021-002 Section 12), deferred to a Work Package at ESR-0021 closure per Programme Sponsor direction. Recommend EBG-0071 if not resolved before session close.

**Note (ESR-0021 WP6):** EBG-0059 and EBG-0060 have since been taken by two of the 11 Candidate Backlog items added during this session's historical HST/FCH audit (Engineering Assurance Capability and the DCE/Repository Execution Agent governance model respectively - see EBR-0001). The recommendations above are renumbered to EBG-0070/0071 accordingly to avoid collision.

---

# 10. Maintenance and Review

JRM-0001 shall be reviewed:

* At every engineering session transition, alongside EBR-0001.
* Whenever a backlog item it references changes status in EBR-0001 (completed, superseded, merged, rejected).
* Whenever the Programme Sponsor directs a roadmap review.

JRM-0001 does not itself authorise implementation. Horizon and phase placement alike are advisory sequencing guidance; the Programme Sponsor determines actual per-session engineering priorities, as EBR-0001 Section 8 (Prioritisation Rules) and PBK-0001's Repository Engineering Health Review Guidance already establish for backlog work generally.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative source for every backlog item this roadmap sequences; closes EBG-0012/0027/0028. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current-state snapshot this roadmap sequences forward from. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Complementary backward-traceability model. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Source of Track C's Guardian Orb phase definitions. |
| [[CHR-0001_PLATFORM_CHARTER|CHR-0001]] | Parent artefact. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers this artefact as a controlled document. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.20 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP3: recorded EBG-0081 Question 1's delivery (UXP shared animation scheduler) in Section 7.4 and the Phase 6 Voice/Vision row of Section 7.3 - both questions of EBG-0081 now closed. |
| 1.19 | 25 July 2026 | Claude Engineering Implementer | ESR-0035 WP2: recorded EBG-0108's registration (Guardian Cognitive Core Implementation, Approved Backlog) against Phase 1 of Track B's dependency chain (Sections 7.1, 7.3) - closes this roadmap's own flagged gap ("no backlog item yet authorises this build"). No implementation authorised; the phase itself remains unactioned pending a future Engineering Implementation Package. |
| 1.18 | 25 July 2026 | Claude Engineering Implementer | ESR-0034 WP3 fix round (Codex-caught, 4 findings): (1) High - restored a literal '## 7.1 Near-term' heading (renumbered 7.1-7.6) so scripts/session_launcher.py's Track B parser doesn't break, verified by running the launcher live; (2) High - removed EBG-0017/0024/0045/0049 from the new Parallel table, all four already Complete, moved into 7.2 Foundation instead; (3) Medium - Section 4 Principle 2 and the Section 10 maintenance line amended to state Track A/C use horizons, Track B uses the new phase model; (4) Medium - fixed three further stale Track C rows exposed by the same review (streaming notifications and sidecar packaging both actually delivered; GIA is Phase 1 Complete, not still Proof-of-Concept-only). |
| 1.17 | 25 July 2026 | Claude Engineering Implementer | ESR-0034 WP3: rewrote Track B (JARVIS Product Capability Roadmap) from stale Near/Mid/Longer-term horizon buckets into an explicit 8-phase dependency-chain model - Phase 1 Guardian Cognitive Core (flagged: no backlog item yet authorises this build) through Phase 8 Home Assistant/Smart Home (EBG-0025). Added Cross-Cutting Constraints (EBG-0065, EBG-0081 Q1) and Parallel-not-gating (EBG-0042, 0059, 0047, 0045/0049, 0024, 0022, 0017) subsections, and an explicit Out-of-Scope note pointing Theme 7/tooling items to Track A. Incorporates ESR-0034 WP1/WP2's 22 promotions and closes the staleness gap since v1.16 (18 July) - EBG-0019/Memory was still listed pending despite EBG-0080's real Personal Memory tier having shipped at ESR-0027. |
| 1.16 | 18 July 2026 | Claude Engineering Implementer | Corrected EBG-0065's rationale: "JARVIS holds real OpenAI/Gemini API keys... today" overstated a persistent fact - confirmed directly (Windows User/Machine environment variables, current shell process) that no such key is persistently configured anywhere on the Programme Sponsor's machine. Reworded to describe the real capability (CredentialReference reads a temporary session-scoped environment variable when the Sponsor sets one) rather than implying standing possession. Also added ESR-0027's real local SQLite personal-memory store as a second category of locally-held data this standard should cover. Raised by the Programme Sponsor after the claim was repeated uncritically in a backlog-grouping summary. |
| 1.15 | 17 July 2026 | Claude Engineering Implementer | Updated Track A's EBG-0057 entry to reference [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2 - a further post-implementation Engineering Reviewer finding (TOCTOU: `submit-response`'s checks ran before the Work Package lock was acquired) addressed. |
| 1.14 | 17 July 2026 | Claude Engineering Implementer | Updated Track A's EBG-0057 entry to reference [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.1 - two post-implementation Engineering Reviewer findings (path-traversal via unsanitised `session`/`work_package`; `submit-to-review`/`submit-response` not checking validation exit codes) addressed. |
| 1.13 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 WP1 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track A's EBG-0057 entry as resolved - `scripts/aiems_bridge.py` MVP implemented per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.0, closed Complete in EBR-0001. |
| 1.12 | 17 July 2026 | Claude Engineering Implementer | Resolved the EBG-0060/EBG-0057 overlap post-ESR-0024 closure (Programme Sponsor-approved): moved EBG-0057 from Track A 6.3 (Longer-term) to 6.1 (Near-term), reflecting the Programme Sponsor's decision to action it next as its own AIEMS/engineering-tooling workstream, separate from Track B's JARVIS/Guardian sequencing. Updated EBG-0060's 6.3 entry to record the resolution: DCE Superseded, REA folded into EBG-0057's future-phase scope. |
| 1.11 | 17 July 2026 | Claude Engineering Implementer | ESR-0024 WP1 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track B's EBG-0074 entry as resolved - `TrustTierPolicy` wired into `build_default_runtime()` per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0, closed Complete in EBR-0001; updated EBG-0019's rationale to reflect EBG-0074 as landed rather than pending. |
| 1.10 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP6 (Engineering Reviewer/Codex reviewed, Programme Sponsor visually confirmed): annotated Track C's EBG-0073 entry as resolved - Guardian/Sentinel/Providers duplication removed, closed Completed in EBR-0001. |
| 1.9 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP5 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track B's EBG-0041 entry as resolved (AAM-0001 approved v0.3, closed Completed in EBR-0001); added EBG-0074 (Wire TrustTierPolicy as Production Default) to Track B Near-term, sequenced ahead of Memory/Voice/Vision/Action per the Engineering Reviewer's explicit recommendation; updated EBG-0019's rationale to reflect it as the next faculty after EBG-0074. |
| 1.8 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP4 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track B's EBG-0048 entry as resolved - GAM-0001 v1.2 Section 9 extended, closing EBG-0048 Completed in EBR-0001. |
| 1.7 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP3 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track B's EBG-0020 entry as resolved - GAM-0001 v1.1 Section 8 added, closing EBG-0020 Completed in EBR-0001. |
| 1.6 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP2 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated Track B's EBG-0031 entry as resolved - GAM-0001 (Guardian Authority and Boundary Model) created and approved v1.0, closing EBG-0031 Completed in EBR-0001 and unblocking EBG-0020/EBG-0048. |
| 1.5 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP1 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated EBG-0018's closure judgement and EBG-0067's Longer-term entry as resolved, matching EBR-0001 v1.46's disposition - EBG-0018 closed Completed; EBG-0067 split, UI Architecture Strategy sub-topic Superseded, Knowledge Architecture/relationship-vocabulary sub-topic promoted to Approved Backlog. |
| 1.4 | 16 July 2026 | Claude Engineering Implementer | Added EBG-0073 (UXP Duplicate Monitoring Elements Tidy-up) to Track C Near-term, discovered by the Programme Sponsor during the live visual check of EBG-0072. |
| 1.3 | 16 July 2026 | Claude Engineering Implementer | Marked Track B's production-provider-wiring item and Track C's System Health panel item Delivered/Complete: implemented per EIP-ESR0022-001 v1.0 (Engineering Reviewer and Programme Sponsor approved), registered EBG-0070/EBG-0072 Complete in EBR-0001. Section 9's first unnumbered item struck through as resolved. ESR-0022 WP1. |
| 1.2 | 16 July 2026 | Claude Engineering Implementer | Following an Engineering Reviewer High finding on EIP-ESR0022-001 v0.1 (a retroactive package cannot be genuinely approved), corrected Track B/Track C entries for EBG-0070/EBG-0072 from `In Progress` to `Approved Backlog`: the earlier implementation was fully reverted, and EIP-ESR0022-001 v0.2 is now a genuine prospective proposal with no code written. |
| 1.1 | 16 July 2026 | Claude Engineering Implementer | Recorded Track B's production-provider-wiring item and Track C's System Health panel item as registered (EBG-0070, EBG-0072), proposed together at ESR-0022 WP1 per this document's own Backlog Acceleration Opportunity pairing. **Corrected same-day**: both were drafted and tested before an Engineering Implementation Package existed for Engineering Reviewer review - reworded throughout from "Delivered/Complete" to "Proposed, pending review" pending [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] review and Programme Sponsor final approval. ESR-0022 WP1. |
| 1.0 | 15 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 15 July 2026.** Status Draft to Approved; version 0.3 to 1.0 marking baseline acceptance. Registering in REG-0001 and closing EBG-0012/EBG-0027/EBG-0028 in EBR-0001 as the same action. ESR-0021 WP5/WP6. |
| 0.3 | 15 July 2026 | Claude Engineering Implementer | Sequenced all 11 EBG-0059-0069 items from the ESR-0021 WP6 historical audit into Tracks A/B: Near-term (EBG-0065, EBG-0068, EBG-0069), Mid-term (EBG-0059, EBG-0061, EBG-0063, EBG-0066), Longer-term (EBG-0060, EBG-0062, EBG-0064, EBG-0067). Flagged EBG-0060/EBG-0057 and EBG-0064/EBG-0033 as overlap pairs needing a combined judgement rather than separate action. Still Draft, not yet Programme Sponsor-reviewed or registered. ESR-0021 WP6. |
| 0.2 | 15 July 2026 | Claude Engineering Implementer | Renumbered Section 9's two recommended EBG identifiers (0059/0060 to 0070/0071) after those numbers were taken by real Candidate Backlog items added during ESR-0021 WP6's historical HST/FCH audit. No other content changed; not yet Programme Sponsor-reviewed or registered. ESR-0021 WP6. |
| 0.1 | 15 July 2026 | Claude Engineering Implementer | Initial draft. Consolidates EBG-0012, EBG-0027 and EBG-0028 into one unified roadmap with AIEMS Process, JARVIS Product and UXP Evolution tracks, per Programme Sponsor direction at ESR-0021 WP5. Surfaced and corrected two stale backlog statuses (EBG-0003, EBG-0004) found during the audit; flagged EBG-0018 for a Programme Sponsor closure judgement; identified two unnumbered recurring items (production provider wiring, REG-0001 HST/FCH gap) for future EBG registration. ESR-0021 WP5. |
