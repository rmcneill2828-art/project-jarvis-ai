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
| **Scorecard status** | **Accepted (Programme Sponsor, 8 July 2026)** | Not yet run | Not yet run | Not yet run |
| Findings raised / accepted / rejected / false positive | 10 / 10 / 0 / 0 * | | | |
| Average defect discovery weight | 3.0 * | | | |
| Repeat issue prevention | Yes * | | | |
| Documentation-only handoff successful | N/A (not the designated Cold Start session) * | | ✓/✗ (verified) | |
| Lead scope discipline | Met * | | | |
| Reviewer role discipline | Met * | | | |
| Evidence responsiveness | Met * | | | |
| Signal-to-noise (Observations excluded) | High * | | | |
| Better converged solution achieved | Yes * | | | |
| Repository impact (multi-tag A/C/G/P/D) | A / C / G / D * | | | |
| Sponsor arbitration required | Low * | | | |

\* ESR-0015 figures originated as the Engineering Implementer's (Claude's) draft self-assessment, carried over from [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] Section 18. The Engineering Reviewer (ChatGPT) independently confirmed these figures as accurate, and the Programme Sponsor accepted the score on 8 July 2026. **This is now the final ESR-0015 trial record.**

---

## 7. Decision Point (ESR-0018)

At the close of ESR-0018, the Programme Sponsor reviews four completed scorecards and decides, based on the evidence recorded above, whether to:

- Adopt the Lead/Reviewer rotation as standing AIEMS practice, or
- Reject it and continue with prior working methods, or
- Adopt a modified version informed by what the trial actually showed.

Any of these three outcomes is a legitimate, evidence-based conclusion. None is a "failure" of the trial itself - the trial succeeds by producing evidence, not by producing a particular answer.

---

## 8. Change Log (measurement instrument only, per Section 4)

| Date | Change | Justification | Sessions affected |
|---|---|---|---|
| - | - | - | - |

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

*Not yet run.*

### ESR-0017

*Not yet run. Cold Start Validation Session - see Section 3.4.*

### ESR-0018

*Not yet run.*
