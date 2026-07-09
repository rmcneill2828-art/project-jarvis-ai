# ESR-0017 WP4 - Engineering Review Package

**Status:** Working Report - not a controlled artefact (per PBK-0001 Working Report Lifecycle), not registered in REG-0001.

---

# 1. Purpose

This package hands ESR-0017 WP4 (the five-session backlog progression roadmap) to the Engineering Reviewer (ChatGPT) for independent review, per the EE-0001 Lead/Reviewer trial. WP1, WP2 and WP3 have all already been reviewed and closed - this is the fourth and final Work Package of ESR-0017.

Unlike WP1-3, WP4 produces no code and no controlled artefact - it is a planning/analysis product, structured against PBK-0001's existing Backlog Progression Analysis framework (`aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`, "Repository Engineering Health Review Guidance" section), applied here at the Programme Sponsor's explicit request rather than at session closure where that framework normally lives.

---

# 2. Session Context

ESR-0017 is open, with four Programme-Sponsor-approved Work Packages, all now complete:

1. **WP1** (reviewed, closed) - UXP&harr;Backend Integration Architecture Decision -> ADR-0019.
2. **WP2** (reviewed, closed) - Connect Guardian Runtime through Sentinel.
3. **WP3** (reviewed, closed) - Gemini provider adapter.
4. **WP4** (this package) - Five-session backlog progression roadmap.

Two new candidate backlog items were created during WP1-3, both already folded with Reviewer input: EBG-0050 (UXP-Backend Bridge Implementation) and EBG-0051 (Gemini Provider Production Readiness).

---

# 3. Methodology

Per PBK-0001's Backlog Progression Analysis guidance, each recommended activity below states: Backlog item reference, Priority, Engineering benefit, Estimated effort, Dependencies, Recommended Engineering Session, Rationale. The analysis considered dependencies between backlog items, engineering sequencing, repository readiness, risk, benefit and Backlog Acceleration Opportunities (grouping related items to reduce repeated verification/re-context-loading cost), per PBK-0001's stated criteria.

**Per PBK-0001: "All handover, backlog progression and JARVIS readiness recommendations are advisory only. The Programme Sponsor determines engineering priorities. No Engineering Implementation Package shall be created or executed from Repository Engineering Health Review recommendations without Programme Sponsor approval."** Nothing below is authorised implementation scope.

The window is framed as **ESR-0017 (this session, recorded as actuals) through ESR-0021** (5 sessions total), matching the scope already recorded in ESR-0017's own session report.

---

# 4. ESR-0017 (this session - actuals, not a recommendation)

| WP | Outcome |
|---|---|
| WP1 | ADR-0019 approved (Tauri sidecar + duplex stdio JSON-RPC), v1.1 after Reviewer revision. New candidate backlog: EBG-0050. |
| WP2 | `GuardianRuntime` connected to Sentinel via optional `conversation_provider`, zero regressions, 8 new tests. |
| WP3 | `GeminiProvider` implemented, unwired by default, 11 new tests. New candidate backlog: EBG-0051. |

One process observation worth carrying forward: WP1-3 were originally implemented back-to-back before the Programme Sponsor introduced per-WP review pauses mid-session. All three were still reviewed individually once the correction was made, so no work reached this roadmap unreviewed - but the correction itself is worth noting for the EE-0001 trial record (Section 5.6, Reviewer role discipline / Section 5.11, Sponsor arbitration), separate from this package's own scope.

---

# 5. ESR-0018 (ChatGPT leads, per frozen EE-0001 rotation - also the trial's decision-point session)

**Revised after ESR-0017 WP9 (see Section 16 addendum): EBG-0050 (both phases) was delivered in ESR-0017 itself, ahead of this roadmap's original schedule. The row below is retained for the historical planning record; it is no longer open work.**

| Item | Priority | Benefit | Effort | Dependencies | Recommended Session |
|---|---|---|---|---|---|
| ~~EBG-0050, Phase 1 only: JSON-RPC message schema + new `python -m jarvis --ipc-stdio`-style headless entry point (no Rust/Tauri work)~~ **Completed early, ESR-0017 WP9.** | High | Unblocks the whole UXP-visible milestone; schema-first is the highest-leverage, lowest-risk slice - settle the contract before writing Rust against it | Medium | ADR-0019 (done) | ~~ESR-0018~~ Delivered ESR-0017 |
| EBG-0051: Gemini production readiness - richer response parsing (safety-blocked responses, empty `parts`, tool/structured output) + Sponsor-run live smoke test | Medium | Clears real, scoped technical debt before Gemini is ever routed to; smoke test is short and Sponsor-run, proportionate to pair alongside the schema work | Low-Medium (+ Sponsor time for the smoke test) | `GeminiProvider` (done, ESR-0017 WP3) | ESR-0018 |

**Not recommended for ESR-0018:** ~~EBG-0050 Phase 2~~ (moot - delivered early alongside Phase 1 at ESR-0017 WP9). ESR-0018 remains appropriately light per the original reasoning below, now carrying only EBG-0051 alongside the EE-0001 decision point.

---

# 6. ESR-0019

**Revised after ESR-0017 WP9: with EBG-0050 already delivered, this session has open capacity for the next product-visible UXP increment - EBG-0055 (Knowledge Graph Phase 1) is recommended to fill it, per the Programme Sponsor's direction that this proceed organically in line with planned Work Packages rather than as a separate initiative.**

| Item | Priority | Benefit | Effort | Dependencies | Recommended Session |
|---|---|---|---|---|---|
| ~~EBG-0050, Phase 2: `src-tauri/src/lib.rs` sidecar command + message forwarding; replace `src/platformStatus.js`'s hardcoded state with live data~~ **Completed early, ESR-0017 WP9** (both phases delivered in one session rather than split across ESR-0018/ESR-0019) | High | The single largest product-visible milestone in this window - delivers `CURRENT_ARCHITECTURE.md` roadmap item 7 ("Deliver Guardian's first interactive conversation") through the real, approved UXP for the first time. Closes the "backend built since ESR-0014, nobody can see it" pattern this whole trial started from. | High (first Rust/Tauri sidecar work in the project) | ~~ESR-0018's schema + Python entry point must land first~~ | ~~ESR-0019~~ Delivered ESR-0017 |
| EBG-0055: Knowledge Graph Phase 1 - static live graph (repository WikiLinks parsed into nodes/edges, new JSON-RPC method, first-pass 2D rendering) | High | Next demonstrable UXP-progress increment per PBK-0001's Feature-First Delivery Discipline, now that the bridge it depends on exists; recovers and begins building toward the Guardian Orb design direction (UAM-0001 Section 8.1) the Programme Sponsor confirmed at ESR-0017 | Medium (parsing/backend) + Medium-High (graph rendering is new frontend surface) | ADR-0019 bridge (done, ESR-0017 WP9) | ESR-0018 or ESR-0019 |

---

# 6.1. Decision Gate - End of ESR-0019

*(Added per ChatGPT Engineering Reviewer's WP4 Observation 1. Updated per the Section 16 addendum: two of three conditions are already satisfied ahead of schedule.)*

Before ESR-0020 begins Guardian governance work, the Programme Sponsor has a natural checkpoint to confirm all three of the following actually hold, not just that a session closed:

1. ~~The IPC bridge is complete (EBG-0050 Phase 2 delivered).~~ **Satisfied - ESR-0017 WP9.**
2. ~~Guardian is genuinely interactive through the real UXP (not just through tests - a Sponsor-observable conversation, the way ESR-0015 WP5 was for OpenAI).~~ **Satisfied - ESR-0017 WP9, verified via a real windowed Tauri session with a live Guardian round trip, not just tests.**
3. Gemini is validated (EBG-0051's live smoke test has actually run, not just been scheduled). **Still outstanding.**

**Contingency** *(per Observation 2)*: if EBG-0051's smoke test slips, ESR-0020's Guardian governance work (EBG-0041, EBG-0031) should be deferred accordingly rather than started early - the entire rationale for sequencing them after the bridge and validated providers is that Guardian being fully wired makes the spec work concrete rather than speculative (Section 7); starting that work before this gate is satisfied would undercut its own stated justification. This is offered as a worked example of the contingency-branch pattern the Reviewer recommended future roadmap analyses adopt more generally.

---

# 7. ESR-0020

| Item | Priority | Benefit | Effort | Dependencies | Recommended Session |
|---|---|---|---|---|---|
| EBG-0041: Guardian Identity Architecture Validation | High | Guardian is fully connected end-to-end (Sentinel since ESR-0017 WP2, UXP since ESR-0019) for the first time by this point - validating identity/cognition sequencing is now concrete, not speculative | Medium (spec/validation, not implementation) | Most valuable once Guardian is fully wired (post ESR-0019); gated on Section 6.1 | ESR-0020 |
| EBG-0031: Guardian Architecture Specification | High | Define safety/permission/approval boundaries before any deeper Guardian implementation - "define before implement" (Principle 1), flagged High priority since ESR-0005 and never actioned | Medium | Pairs naturally with EBG-0041; gated on Section 6.1 | ESR-0020 |
| *(secondary, only if capacity allows)* EBG-0049: Cost-Aware Provider Routing | High (but secondary here) | Two real external providers exist by this point (OpenAI, Gemini) - routing decisions become meaningful rather than speculative | Medium | Both providers wired (ESR-0017 WP3, plus EBG-0051's smoke test) | ESR-0020, if it doesn't crowd out EBG-0041/EBG-0031 |

**Scope-management note** *(per Observation 3, not required now)*: ESR-0020 may become documentation-heavy if EBG-0031 and EBG-0041 both expand substantially during drafting. If that happens, split them across ESR-0020 and a follow-on session rather than compromising review quality/thoroughness to force both into one session.

---

# 8. ESR-0021

| Item | Priority | Benefit | Effort | Dependencies | Recommended Session |
|---|---|---|---|---|---|
| EBG-0048: Guardian HITL Governance Specification | High | Extends EBG-0031 with consent/policy/privacy/approval/memory-retention governance | Medium | EBG-0031 (ESR-0020) | ESR-0021 |
| EBG-0042: Agent Framework Architecture | High | Defines specialist agent contracts (including the Engineering Agent already in informal use) while preserving Guardian as the singular user-facing identity | Medium | None blocking | ESR-0021 |
| Revisit EBG-0047: Sentinel Gate of Durin Architecture Specification | High | Left Candidate at ESR-0016 specifically because "trust tiers and platform-entry validation are not confidently satisfied by the current Sentinel Core implementation." By ESR-0021 a real platform-entry point exists (the JSON-RPC bridge, ESR-0019) to validate against, which didn't exist at ESR-0016 | Medium (reassessment, possibly spec update) | EBG-0050 Phase 2 (ESR-0019) | ESR-0021 |

---

# 9. Backlog Acceleration Opportunities

- ~~**EBG-0050's two-phase split** (schema/Python in ESR-0018, Rust/frontend in ESR-0019) keeps both halves tightly sequenced back-to-back while avoiding one oversized, high-risk session.~~ **Overtaken by events (see Section 16): both phases were delivered in a single session (ESR-0017 WP9) without the risk this reasoning anticipated.** Retained for the historical record of the original planning rationale.
- **EBG-0031 -> EBG-0041 -> EBG-0048** form one continuous Guardian governance thread across ESR-0020/ESR-0021 - grouping them close together reduces re-context-loading cost between sessions, consistent with PBK-0001's Backlog Acceleration criterion.

---

# 10. Flagged, Not Sequenced: Aging Governance Backlog

`EBG-0003` through `EBG-0014` and `EBG-0032` through `EBG-0038` remain Approved/Candidate Backlog since ESR-0001-ESR-0006 - untouched since implementation-first work took over from ESR-0012 onward. None are included in this 5-session sequence. Flagged as an observation only: worth a future Programme Sponsor decision on whether they're still wanted, superseded by the project's implementation-first shift, or genuinely still pending. Not a WP4 recommendation to act on them now.

**Revisit trigger** *(per ChatGPT Engineering Reviewer's WP4 Observation 4, agreeing this should stay consciously deferred rather than forgotten)*: this flag should be re-raised explicitly at ESR-0021 closure (the end of this 5-session window) or at the ESR-0018 EE-0001 decision point, whichever comes first - not left to be rediscovered incidentally by a future session the way it was found here.

---

# 11. What to Review

Please assess, independently:

1. **Sequencing logic** - does Guardian identity/architecture spec work (ESR-0020) really belong *after* the UXP bridge (ESR-0019), or should it run earlier/in parallel? The Lead's reasoning is that Guardian being fully wired end-to-end makes the spec work concrete rather than speculative - is that reasoning sound, or does it just delay already-overdue spec work (High priority since ESR-0005) for a plausible-sounding reason?
2. **EBG-0050 split** - is splitting into two sessions the right call, or is this over-cautious given the codebase's demonstrated ability to do larger sessions (ESR-0015/0016 each delivered substantial work)?
3. **ESR-0018 load** - is it appropriate for ESR-0018 to carry two Work Packages (schema+Python entry point, Gemini hardening) while also being the EE-0001 decision-point session, or should ESR-0018 be kept to a single WP given the trial's own Section 5.11 arbitration-overhead metric?
4. **Priority ordering** - is Guardian governance work (EBG-0031/0041/0048, ESR-0020/0021) correctly prioritised ahead of the aging governance backlog (Section 10)?
5. **EBG-0047 timing** - is "wait until a real platform-entry point exists" (ESR-0021, post-bridge) sound reasoning, or should Gate of Durin work happen earlier, in parallel with the bridge itself?
6. **Missing items** - is anything currently in EBR-0001 that should be in this 5-session window but isn't (e.g. EBG-0027 JRM-0001 JARVIS Product Roadmap, EBG-0045 Cost and Strategic Value Framework)?

---

# 12. Validation Performed

- This WP produced no code and no controlled artefact - there is nothing to `pytest`.
- `python scripts/validate_repository.py`: no new errors or warnings attributable to this package (it references EBG-IDs and ESR numbers as plain text, not WikiLinks, to avoid the adjacency-heuristic false-positive class already documented in prior WP packages).
- Every backlog item cited (EBG-0003 through EBG-0051) was cross-checked against the current `EBR-0001` table content at time of writing, not recalled from memory.

---

# 13. Explicit Non-Claims

- This does not approve, schedule, or authorise any of ESR-0018 through ESR-0021 as active sessions - only ESR-0017 is open.
- This does not create or modify any EBR-0001 entries - all cited backlog items are pre-existing (EBG-0050/EBG-0051 were created during WP1/WP3, not by WP4).
- This does not bind the EE-0001 Lead/Reviewer rotation - ESR-0018 (ChatGPT Lead) is fixed by EE-0001 Section 3.1 regardless of what this roadmap recommends for its content.
- This is not a full Repository Engineering Health Review - it does not include Backlog Validation counts, Engineering Handover, or the JARVIS Development Readiness Assessment PBK-0001 mandates for a full Health Review; it is scoped to exactly what was requested, the five-session progression roadmap.

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| ESR-0017 | Parent session report; WP4 is its final Work Package. |
| ESR-0017 WP1/WP2/WP3 Review Packages | Prior Work Packages this roadmap builds on (EBG-0050, EBG-0051 origins). |
| EE-0001 | Lead/Reviewer trial; ESR-0018's rotation and decision-point status are fixed inputs to this roadmap, not recommendations. |
| EBR-0001 | Authoritative backlog source for every item cited above, including EBG-0055 added by the Section 16 revision. |
| PBK-0001 | Source of the Backlog Progression Analysis methodology this package follows. |
| UAM-0001 | Source of the Guardian Orb design direction EBG-0055 (ESR-0019) begins building toward. |

---

# 15. Reviewer Findings and Disposition

ChatGPT Engineering Reviewer returned: **0 Blocking, 0 Major, 4 Minor Observations**.

| # | Observation | Disposition |
|---|---|---|
| 1 | Identify an explicit decision gate at the end of ESR-0019 (bridge complete, Guardian interactive, Gemini validated) before entering Guardian governance work | **Accepted and incorporated.** New Section 6.1, Decision Gate - End of ESR-0019, added with all three named conditions. |
| 2 | The roadmap assumes every session succeeds; future analyses would benefit from contingency branches (e.g. "if EBG-0050 Phase 2 slips, defer EBG-0041") | **Accepted and incorporated.** The exact example given is now in Section 6.1 as a worked contingency, tied explicitly to why the ESR-0020 sequencing is justified in the first place. |
| 3 | ESR-0020 may become documentation-heavy; if EBG-0031/EBG-0041 expand substantially, split rather than compromise review quality. Not required now | **Accepted and incorporated** as a scope-management note under Section 7 (ESR-0020), for whichever Lead runs that session to apply if it becomes relevant - not acted on further now, per the Reviewer's own framing. |
| 4 | The aging governance backlog should stay visible - agreed it shouldn't interrupt current trajectory, but should be consciously deferred, not forgotten | **Accepted and strengthened.** Section 10 now has an explicit revisit trigger (ESR-0021 closure or the ESR-0018 EE-0001 decision point, whichever comes first) rather than sitting as an undated footnote. |

WP4 is now considered reviewed and closed, pending Programme Sponsor acceptance of this disposition. This closes out all four Work Packages of ESR-0017.

---

# 16. Post-Review Addendum - Roadmap Revised After ESR-0017 WP9

*(Added after WP4's review and closure above, once WP9 - not yet defined when WP4 was reviewed - was implemented later in the same session.)*

WP9 delivered EBG-0050 (both Phase 1 and Phase 2) in ESR-0017 itself, two sessions ahead of the schedule this roadmap set. Sections 5, 6 and 6.1 above have been updated in place (strikethrough marking superseded content, historical reasoning retained rather than deleted) rather than left to silently contradict what actually happened.

This freed real capacity in ESR-0018/ESR-0019 that did not exist when WP4 was reviewed. The Programme Sponsor asked whether the Guardian Orb knowledge-graph design direction (recovered from FCH-0010 and incorporated into UAM-0001 Sections 8.1/8.2/8.3 later in ESR-0017) could be built "organically in line with planned WPs" rather than as a separate initiative. Section 6 now recommends EBG-0055 (Knowledge Graph Phase 1 - Static Live Graph, newly added to EBR-0001) fill that freed capacity in ESR-0018 or ESR-0019, consistent with PBK-0001's Feature-First Delivery Discipline (every session makes demonstrable UXP progress) and the "UXP grows with the work, not ahead of it" principle UAM-0001 Section 7.1 traces back to ESR-0010.

**This addendum is a Lead-side update, not independently re-reviewed by the Engineering Reviewer.** The original WP4 disposition (Section 15) reflects ChatGPT's actual review of the original roadmap; this addendum was added afterward by the Engineering Lead alone. Per the per-Work-Package review discipline this session has otherwise followed throughout, the Programme Sponsor should decide whether this revision needs its own Reviewer pass before EBG-0055 is treated as an accepted part of the roadmap, or whether Lead-side updates that only strike through already-completed items and add one new candidate item (still requiring separate Programme Sponsor authorisation before implementation, per Section 3's standing caveat) can stand without a further review cycle.

No implementation is authorised by this addendum, consistent with Section 13's Explicit Non-Claims.
