# LGB-0001 - Launch Gap Backlog

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | LGB-0001 |
| Title | Launch Gap Backlog |
| Version | 1.3 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] |
| Approval | Approved by Programme Sponsor |

---

# 2. Purpose

LGB-0001 resolves the second of the triggering Codex `govreview`/`v1_0_gap_analysis` finding's three recommended next actions: "a prioritised launch-gap backlog split into must-ship vs defer." Its first ((1) v1.0 readiness scorecard) was addressed at [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] WP4 ([[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]]); its third ((3) repo cleanup) was addressed at WP2.

This artefact takes RSC-0001's scored gaps (the 2 Fail and 1 Partial MLP 0.1 items) and RSC-0001 Section 5's beyond-MLP-0.1 gaps, and splits them into **Must-Ship** (blocks the MLP 0.1 / v1.0 launch itself) versus **Defer** (a later MLP phase, or an enhancement beyond MLP 0.1's own minimum bar). It does not itself approve, schedule or authorise implementation of any item - that remains for [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] backlog promotion and a future Engineering Session, per PBK-0001's Engineering Scope Control (report observations separately from implementation).

---

# 3. Method

An item is **Must-Ship** only if [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 (MLP 0.1) itself explicitly requires it and RSC-0001 scored it Fail, or Partial at less than a basic working level. Everything else - including gaps the triggering review separately named - is **Defer**, because MLP 0.1's own text does not require it; deferring it is not scope-cutting, it is honouring MLP 0.1's own boundary rather than expanding this artefact's criteria beyond what RSC-0001 already established.

---

# 4. Must-Ship (Blocks Version 1.0)

Reconciled with [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] 2.0 at ESR-0061 WP1b (EBG-0130), so the two artefacts give one answer. **RSC-0001 holds the scores; this section lists the blocking gaps.** Version 1.0 = MLP 0.1, released on Windows and macOS (Programme Sponsor decisions D1-D2, D12).

| Gap | RSC-0001 2.0 | Backlog | Go-live WP |
|-----|--------------|---------|------------|
| No macOS build | Section 4A Fail; every Section 4 item Fail on macOS | EBG-0162 | WP2 |
| No working provider on a fresh install | Text Responses Fail | EBG-0163, EBG-0165 | WP3, WP5 |
| Orb fails without a repository | Animated Avatar / Orb Fail | EBG-0164 | WP4 |
| Dashboard, chat and status breach capability honesty and layout | Three items Partial | EBG-0164 | WP4 |
| Voice not provisioned | Basic Voice Input Fail | EBG-0167 | WP7 |
| Child role not safe | Section 4A Fail | EBG-0166 | WP6 |
| Data rights | Section 4A Fail | EBG-0165 | WP5 |
| User and parents' documentation, "Children and privacy" page | Section 4A Fail | EBG-0168 | WP8 |

The two items this section listed before version 1.3 (EBG-0116 User Identity, EBG-0117 Speech Input) remain resolved: both were delivered at ESR-0046 and ESR-0047, and both still score Pass in a development checkout. Speech input fails on a fresh install only because its models are not provisioned, which is the new EBG-0167.

---

# 5. Defer (Beyond MLP 0.1 - Later Phases or Enhancements)

| Gap | MLP Phase / Nature | Backlog Status |
|-----|---------------------|-----------------|
| Guardian Orb Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) | Enhancement beyond MLP 0.1's basic-animation bar ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8) | Not yet registered as its own EBG - confirmed by search; a candidate for a future backlog curation pass, not registered by this WP to keep scope to genuine launch-blockers. |
| Family Profiles (Administrator/Adult/Child/Guest differentiation) | MLP 0.3 | Subsumed by EBG-0116 above once that item is actioned; no separate registration needed yet. |
| Session and Shared Family memory tiers | MLP 0.4 | Not yet registered as its own EBG ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3 specify the architecture only). |
| Local Agent (device assistance) | MLP 0.5 | EBR-0001 EBG-0042 (Agent Framework Architecture, Candidate Backlog, High) and the permission boundary ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, EBG-0021, Completed) already exist; no implementation EBG registered yet. |
| Controlled internet-assisted capability | MLP 0.6 | EBR-0001 EBG-0025 (Home Assistant and Smart Home Integration Assessment, Approved Backlog, Medium) partially overlaps; broader internet-assisted capability is not separately tracked. |
| Vision | MLP 0.7 | Covered by EBG-0112's own text as a future Increment C, not yet split into its own item (same pattern EBG-0117 above just resolved for Increment B). |
| Expanded permission/safety/audit/approval controls; full HITL live wiring; network-facing Guardian/Sentinel interface | MLP 0.8 | Specifications exist and are Complete (GAM-0001 Section 9/EBG-0048, [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]]/EBG-0076); live implementation depends on EBG-0116 (user identity) above for genuine multi-user enforcement, and is not itself separately tracked as an implementation EBG. |

---

# 6. New Backlog Registrations

Two new [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] entries were registered by this Work Package, both genuinely untracked gaps confirmed by direct search before registering (not assumed):

- **EBG-0116** - User Identity and Profile Foundation (Candidate Backlog, High).
- **EBG-0117** - Voice Faculty Increment B: Speech Input (Candidate Backlog, High) - splits Increment B out of EBG-0112 per that item's own explicit invitation to do so once selected.

Neither entry authorises implementation. A future Engineering Implementation Package would still need to be drafted, reviewed and approved for either, per both entries' own registration text.

---

# 7. Interpretation

Two items were originally Must-Ship, sharing no common code dependency on each other. User Identity and Profile Foundation, identified as the higher-leverage item since RSC-0001 flagged it as blocking two further Defer-bucket items (Family Profiles, full HITL live wiring) beyond User Profiles itself, was resolved first, at ESR-0046 WP1. Voice Faculty Increment B (Speech Input) was resolved second, at ESR-0047 WP3 - both Must-Ship items are now delivered.both Must-Ship items are now delivered" would read as contradicting the new Section 4): " Since version 1.3 (ESR-0061 WP1b), Section 4 lists eight Version 1.0 blockers from [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] 2.0's fresh-install scoring; the two items above remain delivered.

---

# 8. Maintenance

LGB-0001 shall be refreshed whenever a Must-Ship item is delivered (moving it out of this backlog) or whenever [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] is refreshed, since both draw on the same scoring.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] | Source of the scored gaps this backlog splits into Must-Ship/Defer. |
| [[JARVIS_PRODUCT_ARCHITECTURE]] | Source of the MLP 0.1 launch criteria defining "Must-Ship." |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog register; hosts EBG-0116 and EBG-0117, newly registered by this artefact. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Source of the Household Role Model and Local Agent Permission Boundary referenced throughout. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Governs sequencing and prioritisation of any future implementation; this artefact does not itself schedule. |
| [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] | Session that created this artefact (WP5), resolving the triggering review's second recommendation. |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 6 October 2026 | Claude Engineering Implementer | ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0130): Must-Ship reconciled with RSC-0001 2.0's fresh-install scoring; eight go-live blockers allocated to WP2-WP8. |
| 1.2 | 4 August 2026 | Claude Engineering Implementer | Per Section 8's own maintenance rule: EBG-0117 (Voice Faculty Increment B, Speech Input) resolved at ESR-0047 WP3 per [[EIP-ESR0047-001_VOICE_PHASE6_INCREMENT_B_SPEECH_INPUT_SCOPE|EIP-ESR0047-001]]. Section 4's Must-Ship row struck through and marked resolved; Section 7's Interpretation updated. Both original Must-Ship items now delivered. |
| 1.1 | 31 July 2026 | Claude Engineering Implementer | Per Section 8's own maintenance rule: EBG-0116 (User Identity and Profile Foundation) resolved at ESR-0046 WP1 per [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]]. Section 4's Must-Ship row struck through and marked resolved; Section 7's Interpretation updated to reflect one of two Must-Ship items now delivered. One Must-Ship item (EBG-0117, Voice Faculty Increment B) remains open. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial LGB-0001 created at ESR-0045 WP5, per the Programme Sponsor's selection of the triggering Codex review's second recommended next action (a prioritised launch-gap backlog split must-ship vs defer). Split RSC-0001's scored gaps into 2 Must-Ship items (both newly registered as EBG-0116/EBG-0117, confirmed genuinely untracked before registering) and 7 Defer items (later MLP phases or beyond-MLP-0.1 enhancements). |
