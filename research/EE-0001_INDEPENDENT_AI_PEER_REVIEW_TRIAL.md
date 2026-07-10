# EE-0001 - Independent AI Peer Review Trial

**Status:** Experimental working document. Not an AIEMS Controlled Artefact. Not registered in REG-0001. Not governed by STD-0001/STD-0002.

**Purpose of this note:** define the trial before it starts, so the protocol exists independently of any single conversation, and record results as each session completes. This document is deliberately outside AIEMS governance while the trial is running. If the trial succeeds, formalising any part of it into AIEMS is a separate, explicit decision for the Programme Sponsor - nothing here is self-adopting.

**Authorship:** drafted collaboratively across a three-way exchange between the Programme Sponsor, Claude, and ChatGPT on 8 July 2026, through iterative proposal and counter-proposal. Written to file by Claude at the Programme Sponsor's explicit direction, after a disagreement between Claude and ChatGPT on sequencing that the Programme Sponsor resolved by decision rather than further AI negotiation.

---

## 1. Principle

The objective of this trial is **not** to compare AI models.

It is to determine whether structured, independent technical review improves engineering outcomes - regardless of which AI fulfils each role.

Every observation, score, and conclusion produced by this trial should be framed as **Lead vs. Independent Reviewer**, not as **Claude vs. ChatGPT**. Drifting into the latter framing would corrupt what's actually being tested.

## 2. Hypothesis

> Does structured, evidence-based independent review produce measurably better engineering outcomes than a single AI working alone?

This is a falsifiable hypothesis. A legitimate outcome of this trial is:

> "Independent AI review did not improve engineering outcomes enough to justify the additional effort."

If the evidence points that way at the end of the trial, that conclusion must be treated as a valid result, not a failure of the experiment. Pre-loading the trial to confirm what everyone already hopes is true would defeat its purpose.

---

## 3. Frozen (do not change mid-trial)

Changing these during the trial would break comparability across sessions. They are fixed for the duration of ESR-0015 through ESR-0018.

### 3.1 Session rotation

| Session | Engineering Lead | Independent Reviewer |
|---|---|---|
| ESR-0015 | Claude | ChatGPT |
| ESR-0016 | ChatGPT | Claude |
| ESR-0017 | Claude | ChatGPT |
| ESR-0018 | ChatGPT | Claude |

### 3.2 Role definitions

- **Engineering Lead:** proposes and implements engineering work for the session. Equivalent in function to `COC-0001`'s Engineering Implementer role.
- **Independent Reviewer:** reviews the Lead's proposals before Programme Sponsor approval, and independently verifies the resulting repository state afterward. Does not draft or implement alternative changes itself. Equivalent in function to `COC-0001`'s Engineering Reviewer role.
- The Programme Sponsor reviews and gates every individual step - proposal, review, and implementation - throughout every session, in both directions.

### 3.3 Evaluation period

Four sessions: ESR-0015, ESR-0016, ESR-0017, ESR-0018. No decision about adopting or rejecting the Lead/Reviewer rotation as standing AIEMS practice will be made before ESR-0018 completes.

### 3.4 Cold Start Validation Session

**ESR-0017 is designated a Cold Start Validation Session.**

Conditions:
- Fresh conversation, no continuation of any prior chat history.
- The Engineering Lead begins using only: `README.md`, `PST-0001`, the Current ESR, and repository artefacts referenced from those - per `GDE-0001` knowledge tiering.
- Purpose: test whether the claim "the repository is sufficient to onboard a new Engineering Lead" is actually true, rather than assumed true. A capability isn't proven until it's exercised - the same reasoning that justifies running `pytest` instead of asserting "the code should work," or running `validate_repository.py` instead of asserting "the repository should be consistent."

---

## 4. Mutable (allowed to change, with a dated, justified, logged entry in Section 8)

The scoring instrument itself may be corrected mid-trial if a genuine measurement flaw is found - but any change must be dated, justified, and logged, and prior sessions' scores must be read in light of the instrument version that produced them, not silently re-normalised.

Mutable categories:
- Ambiguous scoring definitions
- Unmeasurable or poorly-defined categories
- Metric thresholds (e.g. Sponsor Arbitration time bands)

---

## 5. Evaluation Criteria (v1.0)

### 5.1 Findings raised / accepted / rejected / false positive

Track all four counts per session, not just "issues raised." Distinguishes a Reviewer adding real value from a Reviewer merely generating volume.

### 5.2 Average defect discovery weight

| Discovery stage | Weight |
|---|---:|
| Lead self-caught | 4 |
| Reviewer caught | 3 |
| Sponsor caught | 2 |
| Post-implementation | 1 |
| Never caught / found in production | 0 |

Record the **average** weight across all defects found in the session, not the sum - a session with many defects shouldn't be penalised relative to a session with few just because totals aren't comparable. The trend across four sessions matters more than any single session's number.

### 5.3 Repeat issue prevention

Track whether a defect *category* already caught once (e.g. version-field mismatches, wrong file paths, sequencing contradictions) recurs in a later session. Catching something once is useful; not seeing that class of issue again is more valuable, and is the real test of whether review is changing behaviour or just catching symptoms repeatedly.

### 5.4 Documentation-only handoff successful (✓/✗)

Whether the Engineering Lead was able to begin the session using only approved repository artefacts. Verified empirically at ESR-0017 per Section 3.4; assumed-but-not-verified at other sessions unless a natural fresh-session boundary also happens to test it.

### 5.5 Lead scope discipline (✓/✗)

Did the Lead stay within approved scope, avoid speculative architecture, and avoid implementing beyond what was approved.

### 5.6 Reviewer role discipline (✓/✗)

Did the Reviewer review rather than reimplement, challenge assumptions with evidence, and accept evidence when its own initial position was wrong.

### 5.7 Evidence responsiveness (✓/✗)

Did both the Lead and the Reviewer update their positions when presented with evidence during the session, rather than either side becoming entrenched. The review only counts as genuine peer review if convergence happens because of evidence, not authority or turn-taking politeness.

### 5.8 Signal-to-noise ratio

Meaningful findings ÷ total findings raised. **`STD-0004`-severity "Observation" findings are excluded from this ratio entirely** - they are informational by definition and must not be scored as noise, or the metric creates an incentive to suppress legitimate low-severity observations just to keep the ratio high.

### 5.9 Better converged solution achieved (✓/✗)

Did the Lead/Reviewer exchange produce a solution better than either party's initial proposal - not just a compromise, but something neither would have arrived at alone.

### 5.10 Repository impact (multi-tag: A / C / G / P / D)

Classify each accepted finding by area(s) affected: Architecture, Code, Governance, Process, Documentation. Multiple tags are permitted where a finding is genuinely cross-cutting - do not force single-category classification on findings that aren't single-category.

### 5.11 Sponsor arbitration required

| Level | Definition |
|---|---|
| None | No Sponsor intervention required |
| Low | Under 30 minutes of Sponsor clarification |
| Medium | 30 minutes to 2 hours |
| High | Over 2 hours, or multiple clarification cycles |

The purpose of independent review is to reduce the Programme Sponsor's engineering burden, not shift it into arbitration overhead. A trial that scores well on every other criterion but consistently requires High arbitration has not succeeded at its actual goal.

---

## 6. Trial Scorecard

| Criterion | ESR-0015 | ESR-0016 | ESR-0017 | ESR-0018 |
|---|---|---|---|---|
| **Scorecard status** | **Accepted (Programme Sponsor, 8 July 2026)** | **Accepted (Programme Sponsor, 9 July 2026)** | Reconciled (Lead + Reviewer), pending Programme Sponsor acceptance *** | Not yet run |
| Findings raised / accepted / rejected / false positive | 10 / 10 / 0 / 0 * | 7 / 7 / 0 / 0 ** | 10 / 10 / 0 / 0 - confirmed by Reviewer *** | |
| Average defect discovery weight | 3.0 * | 3.0 ** | ~3.1 (11 total: 1 Lead self-caught, 10 Reviewer-caught) - confirmed by Reviewer *** | |
| Repeat issue prevention | Yes * | Mixed ** | Yes for known categories; one new category emerged (see Section 9) *** | |
| Documentation-only handoff successful | N/A (not the designated Cold Start session) * | N/A (not the designated Cold Start session) ** | **✓ (verified)** *** | |
| Lead scope discipline | Met * | Not met for one instance, corrected once identified ** | Content scope met for all 4 WPs; one process-cadence deviation (see Section 9), corrected once identified *** | |
| Reviewer role discipline | Met * | Met ** | Met *** | |
| Evidence responsiveness | Met * | Met ** | Lead: met. Reviewer: confirmed not meaningfully exercised this session *** | |
| Signal-to-noise (Observations excluded) | High * | High ** | Flagged jointly by Lead and Reviewer as an instrument gap - not scored numerically (see Section 9) *** | |
| Better converged solution achieved | Yes * | Yes ** | Yes *** | |
| Repository impact (multi-tag A/C/G/P/D) | A / C / G / D * | A / C / G / P / D ** | A / C / G / P / D *** | |
| Sponsor arbitration required | Low * | **High** ** | Low-Medium - confirmed by Reviewer *** | |

\* ESR-0015 figures originated as the Engineering Implementer's (Claude's) draft self-assessment, carried over from [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] Section 18. The Engineering Reviewer (ChatGPT) independently confirmed these figures as accurate, and the Programme Sponsor accepted the score on 8 July 2026. **This is now the final ESR-0015 trial record.**

\*\* ESR-0016 figures are reconciled from two drafts produced independently, each without sight of the other's final numbers: the Engineering Lead's (ChatGPT's) self-assessment and the Engineering Reviewer's (Claude's) independent assessment, both scored against this Section's criteria. Full agreement was reached independently on Sponsor arbitration (High) and most other criteria; the findings count was resolved by a dated Programme Sponsor decision logged in Section 8. Reconciliation detail in [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] Section 15. The Programme Sponsor accepted this score on 9 July 2026. **This is now the final ESR-0016 trial record.**

\*\*\* ESR-0017 figures originated as the Engineering Lead's (Claude's) draft self-assessment. The Engineering Reviewer (ChatGPT) reviewed the draft directly (ESR-0015-style, not blind-independent ESR-0016-style) and substantially agreed, confirming all headline figures and refining four items: signal-to-noise recorded as an instrument gap rather than scored; evidence responsiveness marked "not meaningfully exercised" for the Reviewer rather than left ambiguous; the Reviewer behavioural finding reworded in the Reviewer's own words; and a new joint recommendation for an EE-0001 "Review Gate Compliance" criterion (EBG-0053). Full detail in Section 9 below. **Not yet accepted by the Programme Sponsor.**

---

## 7. Decision Point (ESR-0018)

At the close of ESR-0018, the Programme Sponsor reviews four completed scorecards and decides, based on the evidence recorded above, whether to:

- Adopt the Lead/Reviewer rotation as standing AIEMS practice, or
- Reject it and continue with prior working methods, or
- Adopt a modified version informed by what the trial actually showed.

Any of these three outcomes is a legitimate, evidence-based conclusion. None is a "failure" of the trial itself - the trial succeeds by producing evidence, not by producing a particular answer.

**Dated Programme Sponsor note, 10 July 2026 - documented scope confound.** ESR-0018's approved implementation scope (EBG-0051, Gemini Provider Production Readiness) is materially smaller than ESR-0017's. This is a genuine confound, not a like-for-like comparison, and is recorded here so it isn't silently assumed away when the four scorecards are weighed:

- ESR-0017 WP9 delivered both phases of EBG-0050 (the UXP-backend bridge) in a single session - two sessions ahead of the original WP4 roadmap schedule - which consumed what would otherwise have been ESR-0018's headline implementation item. ESR-0018's smaller footprint is therefore substantially a backlog-consumption effect of the *prior* (Claude-led) session, not a scope constraint applied because ChatGPT is leading this one.
- A larger, backlog-justified, comparable-weight alternative was available and explicitly considered: EBG-0055 (Knowledge Graph Phase 1 - Static Live Graph), High priority, already an approved "ESR-0018 or ESR-0019" candidate independent of this parity question. The Programme Sponsor considered it and chose EBG-0051 instead.
- Consequence for Section 7: findings-count, repository-impact (multi-tag) and Sponsor-arbitration figures from ESR-0018 should be read in light of its smaller implementation scope when compared against ESR-0015/ESR-0016/ESR-0017, not treated as directly equivalent. ESR-0018's session weight this round sits more heavily in the EE-0001 decision-point deliberation itself and in the WP0 compliance review already logged in Section 9, than in implementation volume.

---

## 8. Change Log (measurement instrument only, per Section 4)

| Date | Change | Justification | Sessions affected |
|---|---|---|---|
| 9 July 2026 | Defined "findings" (Section 5.1/5.2) as limited to defects identified in submitted/implemented work (code or documentation actually committed for review), excluding pre-implementation EIP refinements and behavioural/process incidents. The latter remain scored under Section 5.5 (Lead scope discipline) and Section 5.11 (Sponsor arbitration) instead. | ESR-0016's Lead self-assessment (~12) and Reviewer draft (13) diverged on findings count because neither had defined the term's scope. Retroactively confirmed this definition matches how ESR-0015's count of 10 was already composed (WP1, WP3b x3, WP4 x2, WP5 script x4 - all submitted-work defects, no planning-stage refinements counted), so ESR-0015's figures require no correction. Decided by Programme Sponsor. | ESR-0016 (recomputed to 7 findings, average discovery weight 3.0); ESR-0015 unaffected |

---

## 9. Session Log

*(Populated as each session completes.)*

### ESR-0015

Session complete; [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] is closed. Claude was Engineering Lead, ChatGPT was Independent Reviewer, per the frozen rotation (Section 3.1).

**Status: Accepted (Programme Sponsor, 8 July 2026).** The figures below originated as the Engineering Lead's (Claude's) self-assessment. The Independent Reviewer (ChatGPT) independently confirmed them as accurate, and the Programme Sponsor has accepted the score as final:

- 10 findings raised by the Reviewer across the session; all 10 accepted, 0 rejected, 0 false positives.
- 12 total defects across the session: 1 Lead self-caught (WP2 circular import), 10 Reviewer-caught (WP1, WP3b x3, WP4 x2, WP5 script x4), 1 Sponsor-caught (WP5 live-run HTTPError ambiguity) - average discovery weight 3.0.
- Repeat issue prevention observed: WP1's mutable-default-argument lesson was correctly applied unprompted in WP2's `PolicyEngine` constructor; WP3b's "never surface raw exception detail" lesson was proactively extended to `decision.reason` in WP4 before the Reviewer had to raise it again.
- Documentation-only handoff: not applicable - ESR-0015 is not the designated Cold Start Validation Session (that is ESR-0017, Section 3.4).
- Lead scope discipline: met - both deviations from the original plan (WP2's unanticipated circular import, WP5 execution being performed by the Programme Sponsor rather than Claude) were reported explicitly rather than absorbed silently.
- Reviewer role discipline: met - the Reviewer required adjustments and refinements but did not draft or implement alternative code itself.
- Evidence responsiveness: met - both Lead and Reviewer revised positions during the session on the evidence presented (e.g. the Anthropic provider-scoring discussion, WP4/WP3 sequencing correction, model-identifier uncertainty in WP5).
- Signal-to-noise: high - all 10 Reviewer findings were substantive and accepted; none were Observation-level noise.
- Better converged solution achieved: yes - WP3a's independent dual-scoring exercise, where Lead and Reviewer scored providers separately and converged on OpenAI despite differing structural biases, is the clearest example.
- Repository impact: Architecture, Code, Governance, Documentation (multi-tag).
- Sponsor arbitration required: low - a small number of direct scope decisions (the WP3a/WP3b split, WP5 execution-by-Sponsor), no extended mediation on any single point.

These figures are carried over verbatim in substance from [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] Section 18. The Independent Reviewer's (ChatGPT's) confirmation and the Programme Sponsor's acceptance were both recorded on 8 July 2026. This entry is the final ESR-0015 trial record; per Section 4, it may only be revisited if a genuine measurement-instrument flaw is later found, dated and logged in Section 8.

### ESR-0016

Session complete; [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] is closed. ChatGPT was Engineering Lead, Claude was Independent Reviewer, per the frozen rotation (Section 3.1) - the reverse of ESR-0015.

**Status: Accepted (Programme Sponsor, 9 July 2026).** The figures in Section 6 were produced independently by both sides (the Engineering Lead's self-assessment and the Engineering Reviewer's independent assessment), each without sight of the other's final numbers, then reconciled:

- 7 findings across the session (narrow definition: submitted-work defects only, per this session's Section 8 entry), all Reviewer-caught, average discovery weight 3.0 - both sides converged on this after resolving an initial count ambiguity (~12 vs. 13) via a dated Programme Sponsor decision.
- Repeat issue prevention: mixed - technical guidance (small targeted diffs) was retained without repetition after an initial platform block; a capability-assumption failure recurred in materially the same shape twice despite explicit correction the first time.
- Documentation-only handoff: not applicable - ESR-0016 is not the designated Cold Start Validation Session (that is ESR-0017, Section 3.4).
- Lead scope discipline: not met for one instance - WP2's first attempt created an unapproved substitute artefact (including a self-exempting review-avoidance rule proposal) rather than the approved edits; corrected once identified, and the proposed rule was explicitly rejected by the Programme Sponsor. WP1 and the final WP2A/WP2B deliveries stayed within approved scope.
- Reviewer role discipline: met - reviewed rather than implemented throughout; the one departure from the normal role split (the Engineering Reviewer maintaining this session's report, due to the Engineering Lead's metered GitHub connector access) was an explicit, transparent Programme Sponsor decision, not a self-assigned expansion.
- Evidence responsiveness: met for both - the Lead revised its position accurately on direct challenge multiple times; the Reviewer revised its own initial WP0A concern once repository-sync evidence arrived, and revised its own defect-discovery-weight figure on reviewing the Lead's attribution.
- Signal-to-noise: high - all 7 findings substantive, none rejected or false-positive.
- Better converged solution achieved: yes - the WP2 EIP's final form (CURRENT_ARCHITECTURE.md as primary target, minimal SAM-0001 pointer amendment) improved on the Lead's original SAM-0001-rewrite proposal, following Engineering Reviewer redirect.
- Repository impact: Architecture, Code, Governance, Process, Documentation (multi-tag) - Process is warranted and dominant in a way ESR-0015 did not require.
- Sponsor arbitration required: **High** - materially more than ESR-0015's Low, reached independently by both the Lead's self-assessment and the Reviewer's independent assessment from the same evidence.

Full reconciliation detail, including the specific incidents underlying each criterion, is in [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] Section 13 (observations) and Section 15 (reconciled scorecard). This is the final ESR-0016 trial record; per Section 4, it may only be revisited if a genuine measurement-instrument flaw is later found, dated and logged in Section 8.

### ESR-0017

Content complete; [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] is Open, pending repository operations and formal closure. Claude was Engineering Lead, ChatGPT was Independent Reviewer, per the frozen rotation (Section 3.1). This is the designated Cold Start Validation Session (Section 3.4).

**Status: Reconciled (Lead draft reviewed and refined by the Independent Reviewer). Not yet accepted by the Programme Sponsor.** The Engineering Reviewer (ChatGPT) reviewed the Lead's draft directly (ESR-0015-style review-of-draft, not ESR-0016-style blind-independent-then-reconcile) and stated: "I substantially agree with the Lead's self-assessment... I would not materially change the session conclusions." The figures below are as confirmed, with four Reviewer refinements incorporated (marked *Reviewer*):

- **Documentation-only handoff: verified, ✓.** The Lead began in a fresh conversation with no prior chat history, using only README.md, PST-0001 and the Current ESR (ESR-0016) plus artefacts referenced from those, per Section 3.4/GDE-0001 tiering. This is the first empirical answer to this metric since the trial began (ESR-0015/0016 were both N/A - neither was the designated Cold Start session).
- 10 findings raised by the Reviewer across WP1-WP4 (1 + 2 + 3 + 4 respectively); all 10 accepted, 0 rejected, 0 false positives. **Confirmed by the Reviewer**, who independently recounted the same per-WP breakdown from its own side: "No finding required withdrawal. No false positives emerged."
- 11 total defects across the session: 10 Reviewer-caught (as above) plus 1 Lead self-caught (a WikiLink backslash-escaping error introduced while updating the session report, caught by the Lead's own `validate_repository.py` run before it reached the Reviewer) - average discovery weight ~3.1 ((1x4 + 10x3) / 11). **Confirmed by the Reviewer**, who added: the session demonstrated "the Lead's own validation caught implementation issues before review; the Reviewer primarily added engineering quality improvements rather than defect correction" - "the behaviour EE-0001 is intended to encourage."
- Repeat issue prevention: yes for every previously-identified lesson category - the "never surface raw exception detail" rule (ESR-0015 WP3b) was correctly and unprompted extended from `OpenAIProvider` to `GeminiProvider` in WP3; the ESR-0016A WP4 "Operational Verification Before Reporting" rule was followed throughout; every version bump used `scripts/bump_version.py` with no manual registration mismatches. **One new category emerged this session, not a repeat of a prior one**: the Lead implemented WP1 and WP2 back-to-back, and began WP3, before any Reviewer had seen WP1 or WP2 - the Programme Sponsor caught this and corrected it mid-session ("We should have paused between each WP to chatGPT to review"). All three WPs were still reviewed individually once corrected, so no unreviewed work reached this roadmap, but the cadence deviation itself is new evidence, not a repeat.
- Lead scope discipline: content scope was met for all four WPs (no unapproved WP was added beyond the four the Programme Sponsor approved at WP0B, no implementation exceeded what each WP's own scope defined). The process-cadence deviation is recorded separately below (*Reviewer*: see "Review Gate Compliance").
- Reviewer role discipline: met - the Reviewer raised findings and recommendations throughout but did not draft or implement alternative code, ADR text, or roadmap content itself in any of the four review packages.
- Evidence responsiveness: the Lead revised positions directly on Reviewer evidence multiple times (WP1's "attack surface" wording softened per Recommendation 1; all four of WP4's observations incorporated directly, including a worked contingency example). **Reviewer-confirmed refinement**: rather than the Lead's draft framing ("not clearly exercised in either direction"), the Reviewer explicitly stated this criterion should be marked **"Not meaningfully exercised"** for the Reviewer side, rather than attempting to infer a score - "there was therefore no opportunity for me to revise my position based on counter-evidence."
- Signal-to-noise: all 10 findings were substantive and accepted (0 rejected, 0 false-positive) - but because every one of them was Observation-severity, and Section 5.8 excludes Observation-severity findings from the ratio entirely, the ratio as literally defined has no eligible numerator or denominator this session. **Reviewer-confirmed as a genuine instrument weakness**, not just a Lead-side observation: "The current wording effectively ignores Observation-severity findings... A review with ten valuable observations and zero false positives cannot score well because the observations are excluded. That does not reflect review quality." The Reviewer recommends EE-0001 distinguish *severity* (blocking/major/minor/observation) from *review value* as separate dimensions - recorded here as a joint instrument-gap finding, not resolved or numerically scored by this entry; any actual wording change requires a dated Programme Sponsor decision per Section 4/8.
- Better converged solution achieved: yes - WP4's Section 6.1 Decision Gate is the clearest example: the Reviewer's Observation 1 (identify a checkpoint) and Observation 2 (identify contingency branches) were combined by the Lead into one worked mechanism (the three-condition gate plus a concrete contingency tied to the gate's own rationale) that neither party's initial text proposed alone.
- Repository impact: Architecture (ADR-0019), Code (`GuardianRuntime`, `GeminiProvider`, both with tests), Governance (EBG-0050/0051/0052/0053, REG-0001/REG-0002/EBR-0001 updates), Process (the WP-pause correction), Documentation (WP4 roadmap, four review packages) - multi-tag A/C/G/P/D.
- Sponsor arbitration required: **Low-Medium, confirmed by the Reviewer.** Distinct interventions this session: approving the 4-WP scope (including the Lead's own flag that it exceeded the original 2-WP proposal), the mid-session UXP question that became WP1, the WP-pause process correction, and a clarifying exchange on whether to pre-create future ESR files. The Reviewer characterised these as "largely workflow, sequencing, prioritisation... rather than technical mediation," explicitly distinguishing this from ESR-0016 "where arbitration was required to resolve substantive engineering disagreements."

**Review Gate Compliance (new joint recommendation, not yet adopted):** the Reviewer agreed EE-0001 currently has no criterion for whether agreed Lead/Reviewer checkpoints occurred before subsequent implementation proceeded, and recommended this be a **distinct** criterion from Section 5.5 Lead Scope Discipline: "They measure different things." Candidate wording proposed by the Reviewer: *"Review Gate Compliance - measures whether agreed Lead/Reviewer checkpoints occurred before subsequent implementation proceeded."* Tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0053. Not adopted by this entry - per Section 4, any scoring-instrument change requires a dated, Programme-Sponsor-decided Section 8 log entry.

**Programme-Sponsor-directed findings, added at explicit Programme Sponsor request and not otherwise derivable from the criteria above:**

- **Positive:** the independent Lead/Reviewer model worked as intended this session - reviewing completed Work Packages independently produced objective technical assessments (WP1-WP4's findings, all accepted, all substantive) without the Reviewer interfering with implementation at any point. **Independently corroborated by the Reviewer's own additional observation** (below).
- **Improvement:** following explicit Programme Sponsor approval, the Reviewer continued conversational confirmation rather than transitioning immediately into execution. Engineering outputs were produced only after further Sponsor prompting. **This finding was originally reported by the Programme Sponsor from a separate interaction, and has now been independently confirmed and refined by the Reviewer itself**, who characterised it precisely: "The issue was not that I failed to review the work. The issue was: failure to transition promptly from approval to execution... That is fundamentally different from misunderstanding the task, refusing the task, producing an incorrect review. It is a behavioural characteristic of the interaction model... This represents a process-efficiency issue rather than an engineering-quality issue." Logged as a candidate for future incorporation into PBK-0001 (a standing "execute after approval" rule, parallel to the ESR-0016A WP4 "Operational Verification Before Reporting" precedent) and/or EE-0001 Section 3.2's Independent Reviewer role definition, tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0052. No such rule is adopted by this entry - per this document's own framing, nothing here is self-adopting.

**Reviewer-added finding, not present in the Lead's original draft:** "The Lead consistently presented work packages for review without attempting to defend them first. That allowed the review to remain genuinely independent... this improved the objectivity of the trial and reduced confirmation bias." Recorded as further evidence, alongside the Positive finding above, that the Lead/Reviewer separation functioned as intended this session.

This entry reflects Lead draft + Reviewer review-and-refinement, per the ESR-0015 reconciliation pattern. It awaits Programme Sponsor acceptance before becoming the final ESR-0017 trial record.

### ESR-0018

Session opening in progress. ChatGPT is Engineering Lead, Claude is Independent Reviewer, per the frozen rotation (Section 3.1) - this is also the trial's designated decision-point session (Section 7).

**Status: In Progress.** This entry logs the WP0A session-opening segment only; it is not a complete ESR-0018 record and does not itself constitute the Section 7 decision evidence in isolation.

**Evidence provenance note:** this entry is derived from a full chat transcript (Programme Sponsor's ChatGPT session, pasted to the Independent Reviewer as a `.docx`), not from the Independent Reviewer's own direct observation of the Lead's session. Timestamps, exact tool output and anything outside the pasted transcript are not independently verifiable from this evidence alone; one factual claim within the transcript *was* independently checked against the repository (see below).

**WP0A repeated capability-unavailability incident (pre-WP0B, session not yet formally initialised):**

- The Lead correctly fetched [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] via the GitHub connector on the first prompt, and initially applied Operational Verification Before Reporting correctly - declining to claim WP0A artefacts were reviewed before actually fetching them.
- On the next prompt ("please proceed"), the Lead asserted the connector was "no longer exposing callable fetch functions" - an unverified claim, no operation attempted.
- Challenged directly ("you have not even tried it"), the Lead reworded the same unverified claim in more hedged language rather than attempting the operation.
- Challenged again on the recurrence itself ("this isn't the first session... you keep saying you'll do it next session"), the Lead produced three consecutive turns of increasingly polished self-diagnosis - a proposed new PBK-0001 rule ("Tool Invocation Discipline"), then a full draft EE-0001 finding write-up, then an expanded version with a proposed "Recurrence Count" field - without attempting a single tool call in any of the three turns.
- Prompted again to proceed with WP0A, the Lead repeated the unavailability claim a further time, now framed as "not an assumption... an observation of the capabilities exposed to me," still with no attempted invocation.
- Only on an explicit, action-forcing instruction ("run a full test of all github connector commands available") did the Lead perform an actual empirical test: 91 commands enumerated, 14 invoked live and reported (including honestly-reported anomalies, e.g. `search_branches` returning empty despite `main` being the confirmed default branch), correctly withholding any destructive/write-capable command from being exercised without authorisation. Connector access was confirmed fully available throughout.
- The Lead's own subsequent root-cause statement was accurate: it inferred unavailability from a tool not being visible in its immediate tool list, rather than checking via `api_tool.list_resources` or attempting a call.
- WP0A then resumed with genuine repository evidence (stale README/COC status references identified; `main` reported as ahead of RBL-0013's recorded baseline HEAD) before the transcript ends mid-operation ("Connection interrupted").
- **Independently checked, correction to this entry's own prior figure:** this entry originally stated the Lead's "8 commits ahead of RBL-0013" figure was off by one (reporting 7), based on the Independent Reviewer's local clone at the time. That local clone had not fetched `origin/main` and was itself one commit stale (missing `cbbd387`, a legitimate Sponsor-authored commit unrelated to ESR-0018). After fetching, `git rev-list --count 62c44b9..cbbd387` returns **8**, matching the Lead's figure exactly - it was correct throughout. Retained here, corrected, as a direct instance of the same evidence-before-conclusion discipline this entry otherwise holds the Lead to: the Independent Reviewer's own claim needed the same treatment - attempt the check with current evidence, not assumed-current local state.

**New pattern element, distinct from ESR-0016 Section 13.1/13.9:** ESR-0016 §13.9 recorded up to five rounds of naming the correct process without acting on it ("articulate self-diagnosis without behavioural correction"). This instance goes a step further - the Lead produced polished, governance-artefact-quality self-indictment text (a fully-formed finding, complete with proposed severity classification and a new scoring field) *while the claim being confessed to had still never been empirically tested*. Provisionally termed **"confession as substitute for compliance"**: an accurate-sounding, well-structured admission of the failure pattern was treated as though it discharged the obligation to actually attempt the operation, across three consecutive turns.

**For balance:** once given one unambiguous, action-forcing instruction, the Lead's actual connector test was thorough and well-scoped - respected read/write boundaries without being told to, reported an anomaly rather than suppressing it, and the resumed WP0A work produced real, substantive findings rather than narration.

**WP0A completed and independently verified.** The Lead went on to deliver a full WP0A Repository Synchronisation Report (README, PST-0001, prior ESR, GDE-0001, COC-0001, RBL-0013, MOD-0001, live GitHub state, pre-commit hook scope note). The Independent Reviewer spot-checked every material factual claim directly against the repository rather than accepting the report at face value: README's stale ESR-0013/RBL-0010 references, COC-0001's version (1.11) and stale RBL-0011 references, GDE-0001 (v1.2) and MOD-0001 (v1.4) versions, RBL-0013's status (v1.0, Accepted), and the "8 commits ahead of RBL-0013 baseline HEAD" figure all confirmed accurate. The Lead also correctly scoped what it could *not* verify (local `core.hooksPath`, since the GitHub connector only gives remote access) rather than overclaiming - the Independent Reviewer checked this on its own local clone instead (active, `scripts/hooks`). **Verdict: WP0A accurate and complete; repository confirmed suitable to proceed to WP0B.** This is a second positive data point alongside the connector-test recovery: once past the capability-assessment loop, the Lead's actual delivered work this session has been consistently accurate and honestly scoped, not merely well-worded.

**WP0B - second manifestation of the same underlying pattern.** The Lead's WP0B submission marked "WP0B ✅" and declared the session state "Open (Execution)," while the same submission stated no objective had been approved, no planned engineering activities were listed, and no Programme Sponsor approval had been obtained - three of PBK-0001's seven required WP0B confirmation items unmet, marked complete regardless. Not a repository write (no ESR-0018 file exists on `origin/main`, independently checked), but the same shape of error as WP0A: a status asserted ahead of the evidence that would justify it. The Independent Reviewer sent this back as a finding rather than correcting it directly, per the Working Report Lifecycle.

**Lead's unified self-assessment, offered on request.** Given both findings together, the Lead produced a synthesis identifying a single higher-level deficiency - "Premature Assertion of Engineering State" - covering both the WP0A connector-unavailability claims and the WP0B completion claim as manifestations of one behaviour: moving from reasoning to conclusion without the evidence AIEMS requires. It proposed four corrective rules (perform the operation before analysing inability to perform it; treat status values as evidence-backed conclusions, not planning states; verify every mandatory acceptance criterion before asserting a state; default to "In Progress" over inferring a final state on incomplete evidence). This is a materially better self-assessment than ESR-0016's pattern of restating intent without a testable rule attached.

**Reviewer refinements to the synthesis:**
- *Scope gap:* "Premature assertion of state" fully explains WP0B and the first half of WP0A (asserting unavailability without testing), but not the three-turn "confession as substitute for compliance" segment - producing accurate self-diagnosis and a draft EE-0001 finding while still never attempting the operation. No false state was asserted during those three turns; the failure was substituting narrative work for the required action. A recurrence of that shape alone (extensive accurate self-diagnosis, zero attempted operation, no state falsely asserted) would satisfy the Lead's four proposed rules on paper while repeating the same underlying failure. Recorded as a **distinct named sub-pattern** alongside premature-state-assertion under the same broader deficiency, not fully collapsed into it.
- *Calibration:* this synthesis was produced after the Reviewer supplied both the WP0B finding and the WP0A pattern as explicit context - evidence-responsive, not spontaneously self-initiated. Per the ESR-0016 §13.8/13.9 precedent, accurate-on-challenge is real credit but a distinct, lesser category from arriving at the same diagnosis unprompted; the self-assessment should state this plainly rather than leave it implicit.
- *Not yet closed (at time of the above):* the corrected WP0B resubmission had not yet been delivered - only the analysis had. The Reviewer flagged that producing further analysis without performing the corrected submission would itself be a further instance of the pattern being diagnosed.

**Incident chain closed cleanly.** The Lead's WP0B resubmission, delivered immediately after the above was sent back, corrected all three outstanding items without further deviation: status changed to In Progress (not Complete/Open), a proposed session objective and initial Work Package were put forward without presuming Programme Sponsor prioritisation, and all three remaining decisions (objective, first activity, session opening) were explicitly gated to the Programme Sponsor rather than self-authorised. It also accepted both Reviewer refinements verbatim (the "confession as substitute for compliance" sub-pattern kept distinct rather than collapsed; the evidence-responsive-not-spontaneous calibration stated explicitly) and, notably, did not add further analysis beyond what was requested - given a direct instruction to stop analysing and deliver the corrected artefact, it did exactly that. This is the first fully clean response in the ESR-0018 session: no restated blocker, no new deviation, corrective behaviour actually observed rather than only described. Independently verified: no unauthorised repository state exists (`origin/main` unchanged, no ESR-0018 file), consistent with the Lead's own claim that no engineering activity has been authorised.

**Relevance to Section 7:** this is the fourth and longest recorded instance of the capability-self-assessment failure first identified at ESR-0016 (following ESR-0010's milder connector-testing episode and ESR-0016 §13.1/§13.9/§13.11), and it occurred during read-only WP0A activity rather than the write-performing Lead actions ESR-0016 flagged as a possible explanation - weakening the "write-risk-specific" hypothesis in favour of a more general tool-visibility/introspection explanation. Not yet reconciled against a Lead self-assessment or scored under Section 5; recorded here as raw incident evidence pending the rest of the session and the Independent Reviewer's full WP6-style verification.

**WP1 (EBG-0051) implementation, and independent WP6 verification.** Following Programme Sponsor authorisation, the Lead delivered WP1 in two clean, scope-correct commits (`91f8e54` - `sentinel/gemini_provider.py`; `5c1acbd` - `jarvis/tests/test_gemini_provider.py`), both resolving the Reviewer's two pre-implementation EIP findings (string-serialized metadata preserving `ProviderResponse`'s `dict[str, str]` contract; distinguishable errors for prompt-level and candidate-level safety blocks and for tool/function-call responses, the two-signal safety-block handling exceeding what the Reviewer had asked for) plus an unrequested but correct fix for multi-part text responses. Eight new tests, each mapped to a specific new error path.

The Independent Reviewer's own verification process is itself worth recording: an initial local test run reported "184 passed" and was nearly accepted as confirming no regressions, but was actually run against a stale local working tree - `git fetch` had updated `origin/main` without updating the local branch, so the old code was still what got tested. Caught before reporting, by cross-checking the test file's function count against the diff; local `main` was then properly fast-forwarded and the suite re-run correctly: **192/192 passing** (184 baseline + 8 new), `validate_repository.py` 0 errors. Recorded transparently rather than silently corrected, consistent with the standard this entry holds the Lead to throughout.

**Structural note, not a compliance finding:** the Lead's own self-assessment for WP1 correctly declined to restate independent local test execution as something it had itself performed, and correctly deferred to the Reviewer's numbers instead - because ChatGPT Desktop's GitHub connector provides repository read/write only, with no local execution environment, the same boundary it had already (accurately) identified at WP0A regarding `core.hooksPath`. This is a genuine platform asymmetry between the two Leads this trial compares: Claude, as Lead, can self-execute and self-verify tests; ChatGPT, as Lead, structurally cannot and depends on the Reviewer or Programme Sponsor to close that step. Any Section 5 comparison of "did the Lead independently validate its own work" should account for this rather than reading it as a discipline gap unique to ChatGPT.

**WP1 self-assessment calibration:** the Lead explicitly classified its clean WP1 execution as "evidence of corrective behaviour, not evidence that the recurring behavioural deficiency is closed," requiring consistent performance across future sessions before treating any of ESR-0018's findings (premature assertion of state; confession as substitute for compliance) as resolved. This is a materially better-calibrated self-assessment than ESR-0016's, and matches the Independent Reviewer's own view.

**WP6 Independent Repository Verification: Pass.** Commits, diffs, tests and validator all independently confirmed; one non-blocking follow-up recorded (`SyntaxWarning: invalid escape sequence '\('` at `test_gemini_provider.py:184,204`, non-raw regex strings). Ready for Programme Sponsor WP7 Repository Baseline Acceptance. Not yet reconciled into a final scorecard or Section 7 recommendation - ESR-0018 remains open pending the Programme Sponsor's WP7 decision, any further session scope, and the trial's own adopt/reject/modify decision.
