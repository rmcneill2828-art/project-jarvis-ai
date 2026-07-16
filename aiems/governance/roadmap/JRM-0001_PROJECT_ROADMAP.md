# JRM-0001 - Project Roadmap

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | JRM-0001 |
| Title | Project Roadmap |
| Version | 1.5 |
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
2. Sequencing is expressed as horizons (Near-term, Mid-term, Longer-term, Not Yet Justified), not fixed ESR numbers or dates. AIEMS sessions are opened ad hoc based on Programme Sponsor availability and priority, not a calendar - committing to "EBG-0012 in ESR-0024" would be false precision.
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
| EBG-0065 - STD-0006 Configuration and Secrets Standard | Discovered at ESR-0021 WP6; named at project bootstrapping but never created. Elevated to Near-term because it is no longer theoretical - JARVIS holds real OpenAI/Gemini API keys and Sentinel credential references today. The longer this stays undocumented, the more implicit practice it has to retroactively capture. |
| EBG-0068 - Engineering Implementation Brief (EIB) artefact type, adopt or drop | Discovered at ESR-0021 WP6. Not a build item - a quick judgement call (confirm EIB was superseded by the EIP convention that followed it, mark Superseded, close). Cheapest possible win in this roadmap; no reason to leave it open. |

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
| EBG-0057 - Claude<->Codex Engineering Bridge | Architecture and cost fully decided (see EBR-0001 note); explicitly requires its own future EIP before implementation. Notably, ESR-0021 is informally already exercising something adjacent to this bridge's Phase 1 intent (Programme Sponsor manually relaying between Claude and ChatGPT/"Codex" via VS Code), without any of the bridge's actual tooling - real-world evidence for whether the manual-relay pattern remains sufficient before investing in automation. |
| EBG-0060 - Direct ChatGPT Execution (DCE) / Repository Execution Agent (REA) | Discovered at ESR-0021 WP6. Conceptually predates and overlaps EBG-0057 immediately above - both are about governed AI repository-write execution paths. Worth a combined judgement when EBG-0057 is next actioned: does the Claude-Codex Bridge architecture already supersede what DCE/REA was reaching for, or does DCE/REA identify a gap the bridge design doesn't cover (e.g. single-AI direct execution outside a two-AI handover model)? |
| EBG-0062 - CPS-0001 Codex Prompt Standard | Discovered at ESR-0021 WP6. Lowest priority of the newly-discovered items per its own backlog note - 20+ sessions of established EIP convention have substantially met the original need even without a named standard. |
| EBG-0064 - ISTL-0001 Engineering Inter-Session Task Register | Discovered at ESR-0021 WP6. Likely substantially satisfied already by PST-0001 Section 8 (Active and Next Planned Work) and EBR-0001 itself - action only if a real gap is confirmed, not by default. Overlaps EBG-0033 above. |
| EBG-0067 - Dropped ADR-0007 topics (JARVIS UI Architecture Strategy; AIEMS Knowledge Architecture) | Discovered at ESR-0021 WP6. The UI-strategy question looks substantively resolved by the later real ADR-0007/ADR-0019 UXP decisions; the knowledge-architecture/relationship-vocabulary question is less clearly resolved elsewhere. Needs a judgement call on whether either is still a live gap before any implementation work, not a build item in itself. **Resolved at ESR-0023 WP1**: split disposition applied - UI Architecture Strategy sub-topic judged Superseded; AIEMS Knowledge Architecture/relationship-vocabulary sub-topic confirmed as a genuine live gap, promoted to Approved Backlog scoped to that remaining sub-topic. No longer Longer-term/Not Yet Justified - re-sequence in a future roadmap refresh. |

---

# 7. Track B - JARVIS Product Capability Roadmap

Governs JARVIS/Guardian/Sentinel product capability. Current state is PST-0001 Section 5's authority; this section sequences what is not yet there.

## 7.1 Near-term

| Item | Rationale |
|------|-----------|
| EBG-0031 - Guardian Architecture Specification | High priority since ESR-0005, blocks meaningful Guardian safety/permission work; Guardian is already user-facing (the live Orb/chat) without this specification formally existing. |
| EBG-0041 - Guardian Identity Architecture Validation | AAM-0001 exists but has never been validated against implementation sequencing, per this item's own text. |
| EBG-0069 - JARVIS_CAPABILITY_READINESS_MATRIX.md Refresh | Discovered at ESR-0021 WP6. Direct precedent already exists and succeeded: EBG-0056 refreshed the sibling PCB-0001 document the same way. Low-risk, well-understood pattern - should not need its own design work, just execution. **Delivered at ESR-0021 WP7**; EBR-0001 remains authoritative for its Complete status. |
| EBG-0070 - Wire a Live Provider into a Production `ProviderOrchestrator` Route | Both providers are live-validated (EBG-0051, and OpenAI since ESR-0015) but neither was wired into default JARVIS/Guardian runtime use - flagged as a candidate in PST-0001 across at least three sessions before this section recommended registering it. **Delivered at ESR-0022 WP1** per [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] v1.0 (Engineering Reviewer and Programme Sponsor approved): `build_default_runtime()` registers a real OpenAI/Gemini provider (configurable via `JARVIS_PRIMARY_PROVIDER`, default `openai` per PEM-001) when its credential is present and non-blank, with `LocalEchoProvider` retained as failover; registered as EBG-0070 in EBR-0001, Complete. |

## 7.2 Mid-term

| Item | Rationale |
|------|-----------|
| EBG-0017 - JARVIS Product Requirements and Capability Backlog | High priority, foundational for everything else in this track, but the programme has functioned without it for 20+ sessions by using EBR-0001 and PST-0001 together - not urgent, but overdue. |
| EBG-0019 - Memory and Data Storage Architecture | Blocks persistent memory, which remains explicitly deferred (PST-0001 Section 10) - sequence architecture-first per this item's own stated rationale. |
| EBG-0020 - Guardian, Family Safety and Emergency Controls | Depends conceptually on EBG-0031 (Guardian Architecture) landing first. |
| EBG-0042 - Agent Framework Architecture | ADR-0011 exists; this item defines specialist agent contracts building on it. Relevant once GIA moves past Proof of Concept. |
| EBG-0045 / EBG-0049 - Cost and Strategic Value Framework / Cost-Aware Provider Routing | Explicitly overlapping, already cross-referenced in EBR-0001 - action together, not separately. Directly relevant once the Near-term production-provider-wiring item above happens, since that is where cost first becomes a live concern rather than a research question. |

## 7.3 Longer-term / Not Yet Justified

| Item | Rationale |
|------|-----------|
| EBG-0021 - Local Agent Permission Boundary | No local agent implementation exists yet to bound - premature until one is planned. |
| EBG-0022 - JARVIS AIEMS Knowledge Capability | Interesting, not blocking anything currently planned. |
| EBG-0023 - Backup, Recovery and Data Protection | Gated on EBG-0019 (memory architecture) existing first - nothing significant to back up yet beyond the repository itself. |
| EBG-0024 - JARVIS Cost Strategy | Substantially overlaps EBG-0045/EBG-0049 above; likely mergeable once one of the three is actioned. |
| EBG-0025 - Home Assistant / Smart Home Integration Assessment | No dependency currently forces this; purely additive future scope. |
| EBG-0029 - Product Growth Philosophy | Documentation-only, no urgency. |
| EBG-0046 - Device Independence and Restore Architecture | Large scope, no current trigger. |
| EBG-0047 - Sentinel Gate of Durin Architecture Specification | Extends EBG-0030 (already Completed); worth revisiting once trust-tier work (ESR-0016) sees further use, not before. |
| EBG-0048 - Guardian HITL Governance Specification | Extends EBG-0031 - sequence after it, not before or in parallel. |

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
| EBG-0050 remaining scope: streaming notifications | Explicitly kept open under EBG-0050 rather than closed outright; natural next increment now that a production provider is wired in (EBG-0070, delivered ESR-0022 WP1), since streaming matters most once real conversational latency exists. |
| EBG-0073 - UXP Duplicate Monitoring Elements Tidy-up | Discovered directly by the Programme Sponsor viewing the live app after EBG-0072 shipped: `SystemHealthPanel` and `DiagnosticsPanel` now visibly duplicate Guardian/Sentinel/Providers rows. Low-risk consolidation, no new backend work needed - a natural quick follow-on to EBG-0072 rather than a standalone design effort. |

## 8.3 Mid-term

| Item | Rationale |
|------|-----------|
| EBG-0055 Phase 1.5 / next continuation - true 3D rendering and live animation of the Orb | Explicitly deferred by Programme Sponsor decision at ESR-0019 ("doesn't have to be perfect first time"); a future EIP should clarify whether this becomes explicit Phase 1.5 scope or folds into Phase 3, per EBG-0055's own note. |
| EBG-0050 remaining scope: production sidecar packaging (`tauri-plugin-shell`) | Only matters once the UXP moves toward actual distribution rather than dev-mode use; not urgent while still in active development. |
| Real-Time Activity feed (mock-up panel) | No backend event/activity log exists yet - this is new backend work, not a UXP-only increment, and should be scoped as such rather than attempted as a "quick" UXP session. |

## 8.4 Longer-term / Blocked

| Item | Rationale |
|------|-----------|
| EBG-0055 Phase 3 - agent-traversal animation | Explicitly blocked on GIA telemetry; GIA remains a Proof of Concept with further implementation deferred (PST-0001 Section 10). Cannot proceed until GIA does. |
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

JRM-0001 does not itself authorise implementation. Horizon placement is advisory sequencing guidance; the Programme Sponsor determines actual per-session engineering priorities, as EBR-0001 Section 8 (Prioritisation Rules) and PBK-0001's Repository Engineering Health Review Guidance already establish for backlog work generally.

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
| 1.5 | 16 July 2026 | Claude Engineering Implementer | ESR-0023 WP1 (Engineering Reviewer/Codex reviewed, Programme Sponsor approved): annotated EBG-0018's closure judgement and EBG-0067's Longer-term entry as resolved, matching EBR-0001 v1.46's disposition - EBG-0018 closed Completed; EBG-0067 split, UI Architecture Strategy sub-topic Superseded, Knowledge Architecture/relationship-vocabulary sub-topic promoted to Approved Backlog. |
| 1.4 | 16 July 2026 | Claude Engineering Implementer | Added EBG-0073 (UXP Duplicate Monitoring Elements Tidy-up) to Track C Near-term, discovered by the Programme Sponsor during the live visual check of EBG-0072. |
| 1.3 | 16 July 2026 | Claude Engineering Implementer | Marked Track B's production-provider-wiring item and Track C's System Health panel item Delivered/Complete: implemented per EIP-ESR0022-001 v1.0 (Engineering Reviewer and Programme Sponsor approved), registered EBG-0070/EBG-0072 Complete in EBR-0001. Section 9's first unnumbered item struck through as resolved. ESR-0022 WP1. |
| 1.2 | 16 July 2026 | Claude Engineering Implementer | Following an Engineering Reviewer High finding on EIP-ESR0022-001 v0.1 (a retroactive package cannot be genuinely approved), corrected Track B/Track C entries for EBG-0070/EBG-0072 from `In Progress` to `Approved Backlog`: the earlier implementation was fully reverted, and EIP-ESR0022-001 v0.2 is now a genuine prospective proposal with no code written. |
| 1.1 | 16 July 2026 | Claude Engineering Implementer | Recorded Track B's production-provider-wiring item and Track C's System Health panel item as registered (EBG-0070, EBG-0072), proposed together at ESR-0022 WP1 per this document's own Backlog Acceleration Opportunity pairing. **Corrected same-day**: both were drafted and tested before an Engineering Implementation Package existed for Engineering Reviewer review - reworded throughout from "Delivered/Complete" to "Proposed, pending review" pending [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] review and Programme Sponsor final approval. ESR-0022 WP1. |
| 1.0 | 15 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 15 July 2026.** Status Draft to Approved; version 0.3 to 1.0 marking baseline acceptance. Registering in REG-0001 and closing EBG-0012/EBG-0027/EBG-0028 in EBR-0001 as the same action. ESR-0021 WP5/WP6. |
| 0.3 | 15 July 2026 | Claude Engineering Implementer | Sequenced all 11 EBG-0059-0069 items from the ESR-0021 WP6 historical audit into Tracks A/B: Near-term (EBG-0065, EBG-0068, EBG-0069), Mid-term (EBG-0059, EBG-0061, EBG-0063, EBG-0066), Longer-term (EBG-0060, EBG-0062, EBG-0064, EBG-0067). Flagged EBG-0060/EBG-0057 and EBG-0064/EBG-0033 as overlap pairs needing a combined judgement rather than separate action. Still Draft, not yet Programme Sponsor-reviewed or registered. ESR-0021 WP6. |
| 0.2 | 15 July 2026 | Claude Engineering Implementer | Renumbered Section 9's two recommended EBG identifiers (0059/0060 to 0070/0071) after those numbers were taken by real Candidate Backlog items added during ESR-0021 WP6's historical HST/FCH audit. No other content changed; not yet Programme Sponsor-reviewed or registered. ESR-0021 WP6. |
| 0.1 | 15 July 2026 | Claude Engineering Implementer | Initial draft. Consolidates EBG-0012, EBG-0027 and EBG-0028 into one unified roadmap with AIEMS Process, JARVIS Product and UXP Evolution tracks, per Programme Sponsor direction at ESR-0021 WP5. Surfaced and corrected two stale backlog statuses (EBG-0003, EBG-0004) found during the audit; flagged EBG-0018 for a Programme Sponsor closure judgement; identified two unnumbered recurring items (production provider wiring, REG-0001 HST/FCH gap) for future EBG registration. ESR-0021 WP5. |
