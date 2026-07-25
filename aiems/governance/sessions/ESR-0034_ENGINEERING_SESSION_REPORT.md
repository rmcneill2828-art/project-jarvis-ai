# ESR-0034 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0034 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0034 |
| Date Opened | 25 July 2026 |
| Date Closed | 25 July 2026 |
| Closure Status | Closed - WP1-WP3 complete, session-wide WP4 Pass, WP5 Retain (RBL-0020 remains current) |

---

# 2. Purpose

This report records the opening and execution of ESR-0034, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0033, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service (ADR-0022) with no manual relay anywhere - the ninth consecutive session run this way. Unlike prior sessions' code-implementation focus, ESR-0034 was entirely Programme Sponsor-directed backlog governance and roadmap sequencing: a large batch of Candidate-to-Approved Backlog promotions, one separately-reviewed higher-stakes promotion, and a full rewrite of the project roadmap's product-capability track into an explicit dependency-chain model.

---

# 3. Scope

ESR-0034 opened directly from a Programme Sponsor request following a conversational discussion of JARVIS/Guardian's current capability gaps (itself following ESR-0033's closure): promote two specific Candidate Backlog items whose original parking conditions had since been satisfied, and separately review a third for possible promotion.

**WP1** promoted EBG-0023 (JARVIS Backup, Recovery and Data Protection Guidance) and EBG-0065 (STD-0006 Configuration and Secrets Standard) to Approved Backlog, then - on Programme Sponsor direction - expanded to a full 21-item batch, applying the same test (does the item's own EBR-0001 Notes text state a reason it must remain Candidate?) to every other Candidate Backlog item not already known to be genuinely blocked: EBG-0022, 0025, 0029, 0038, 0040, 0046, 0052, 0054, 0061, 0066, 0081 (Question 1 only), 0090-0096 and 0106. Two Codex review rounds, both findings fixed (EBG-0065's wording overstated "real credentials existing" - corrected to credential references/credential-gated live routes; PST-0001's Current Mode row left stale after the batch expanded from 2 to 21 items).

**WP2** reviewed EBG-0021 (JARVIS Local Agent Permission Boundary) separately from WP1's batch, on the Engineering Implementer's own flag that it differs in kind from routine curation - it is itself the root gate for the Action faculty (per EBG-0041's recommended sequencing) and touches GAM-0001 trust-boundary territory. Promoted to Approved Backlog with that distinction explicitly recorded, not folded into WP1's batch. Codex review found PST-0001 Section 4A still claimed "no session currently open," contradicting Section 3's already-updated state; fixed and reconfirmed.

**WP3** rewrote JRM-0001's Track B (JARVIS Product Capability Roadmap) from stale Near/Mid/Longer-term horizon buckets (last touched 18 July, v1.16 - still listing EBG-0019/Memory as pending despite EBG-0080's real Personal Memory tier having shipped at ESR-0027) into an explicit 8-phase dependency-chain model directly answering the Programme Sponsor's own question: what is the logical path to a working version? Phase 1 (Guardian Cognitive Core, flagged as having no backlog item yet authorising its build) through Phase 8 (Home Assistant/Smart Home, EBG-0025), plus Cross-Cutting Constraints and a Parallel-not-gating subsection. Codex's first review round caught four real defects: a `scripts/session_launcher.py` parser regression from renaming a heading the script hard-codes a lookup against; four already-Complete items (EBG-0017/0024/0045/0049) wrongly carried into the new "still open" table; a horizon-vs-phase principle inconsistency in Section 4/10; and three further stale Track C rows the same review exposed (streaming notifications, sidecar packaging, GIA status). All four fixed and independently reconfirmed, including a live `session_launcher.py` re-run.

Session-wide **WP4** (Independent Repository Verification) and **WP5** (Repository Baseline Determination) closed the session: WP4 reached Pass (with one disclosed, pre-existing environmental limitation in Codex's own sandbox, not a defect in this session's work); WP5 retained [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] rather than establishing a new baseline - both independent views agreeing this session's entirely governance/register/roadmap-only content does not change what RBL-0020 already describes about the repository.

---

# 4. Engineering Authority

ESR-0034 opening was authorised by direct Programme Sponsor instruction on 25 July 2026, immediately following ESR-0033's closure the same day and confirming [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Curate the engineering backlog register to reflect genuinely current conditions (promoting items whose stated blockers have been resolved, or which were simply never reviewed rather than actually blocked), and rewrite the project roadmap's product-capability track so it states an honest, dependency-ordered path from current state to a functioning JARVIS/Guardian - rather than the stale, un-sequenced horizon buckets it had drifted into.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | Promote EBG-0023, EBG-0065, then a further 19 Candidate Backlog items to Approved Backlog | Complete |
| WP2 | Separately review and promote EBG-0021 | Complete |
| WP3 | Rewrite JRM-0001 Track B as an 8-phase dependency-chain roadmap | Complete |
| WP4 | Session-wide Independent Repository Verification | Complete - Pass |
| WP5 | Session-wide Repository Baseline Determination | Complete - Retain RBL-0020 |

---

# 7. WP1 - Backlog Promotion Batch (21 Items)

Promoted EBG-0023 and EBG-0065 first, each on the basis of a specific resolved prerequisite (EBG-0023: EBG-0019/MDS-0001 Complete; EBG-0065: real credential references and credential-gated live routes now exist). On Programme Sponsor direction, expanded to review every other Candidate Backlog item not already known to carry a genuine blocker, applying one consistent test throughout: does the item's own Notes text state a reason it must remain Candidate? Nineteen further items passed this test and were promoted: EBG-0022, 0025, 0029, 0038, 0040, 0046, 0052, 0054, 0061, 0066, 0081 (Question 1 only, Question 2 already delivered), 0090, 0091, 0092, 0093, 0094, 0095, 0096, 0106. EBG-0021 (reviewed separately, WP2) and EBG-0042/0047/0059/0085 (each carrying genuine stated blocking language) were deliberately left untouched.

Two Codex review rounds: the first found EBG-0065's promotion wording overstated "real credentials existing in the codebase" when the actual repository evidence is credential references and environment-variable gates, not committed secret values - corrected. The second, run against the full 21-item batch, found PST-0001's Current Mode row still described only the original 2-item promotion after the batch expanded to 21 - corrected and reconfirmed.

- Commit SHA: `a92b64e`
- `python -m pytest`: 374 passed plus 1 skip (unchanged - no code touched). `python scripts/validate_repository.py` (full mode): 0 errors, 155 warnings.

---

# 8. WP2 - EBG-0021 Promotion (Separate Review)

Reviewed EBG-0021 (JARVIS Local Agent Permission Boundary) on its own, distinct from WP1's batch, on the Engineering Implementer's explicit flag that it differs in character from the routine tooling/process items promoted there: it is itself the prerequisite gate for the Action faculty (per EBG-0041's recommended implementation sequencing - wiring, then Memory, then Voice/Vision, then Action) and touches GAM-0001 trust-boundary territory. Promoted to Approved Backlog with this distinction recorded in EBR-0001 itself, flagged as warranting its own dedicated future session rather than incidental treatment.

Codex review confirmed the promotion itself was valid (no blocking language in EBG-0021's own Notes) and the version chain consistent, but found PST-0001 Section 4A still claimed "no session currently open" - a staleness left over from WP1 that had gone unnoticed since only Section 3 (Current Mode/Phase/Objective) had been updated there. Fixed and independently reconfirmed.

- Commit SHA: `b4732fa`
- `python -m pytest`: 374 passed plus 1 skip. `python scripts/validate_repository.py` (full mode): 0 errors, 155 warnings.

---

# 9. WP3 - JRM-0001 Track B Rewrite (8-Phase Roadmap)

Following a conversational discussion answering the Programme Sponsor's question "what are the blockers to a full functioning version," then "does this roll the themes in as well" (identifying two genuine gaps in the first draft - EBG-0025 Home Assistant, and EBG-0065/EBG-0081 as cross-cutting constraints rather than phases), the Programme Sponsor directed this analysis be written into JRM-0001 formally.

Rewrote Track B (JARVIS Product Capability Roadmap, Section 7) from stale Near/Mid/Longer-term horizon buckets into an explicit dependency-chain model: **Phase 1** Guardian Cognitive Core (flagged - no backlog item yet authorises this build, the single most consequential gap in the roadmap); **Phase 2** EBG-0021; **Phase 3** Action faculty implementation (also flagged - no backlog item yet); **Phase 4** Memory expansion plus EBG-0023; **Phase 5** Knowledge Graph Phases 2-4; **Phase 6** Voice/Vision (also flagged); **Phase 7** EBG-0046; **Phase 8** EBG-0025. Added Cross-Cutting Constraints (EBG-0065, EBG-0081 Question 1) and a Parallel-not-gating subsection for items that mature alongside the chain without blocking or being blocked by it.

Codex's first review round found four real defects: (1) High - the heading rename (`## 7.1 Near-term` to `## 7.1 Foundation (Delivered)`) broke `scripts/session_launcher.py`'s hard-coded Track B parser, reproduced live as an actual `SessionLauncherError`; (2) High - four already-Complete items (EBG-0017, 0024, 0045, 0049) were wrongly carried forward from the old text into the new "still open, parallel" table; (3) Medium - Section 4's roadmap principles and the Section 10 maintenance text still described sequencing purely in horizon terms, now inconsistent with Track B's new phase model; (4) Medium - the same review exposed three further stale Track C rows (streaming notifications and sidecar packaging both actually delivered; GIA described as still Proof-of-Concept-only when Phase 1 is Complete). All four fixed within the WP - the launcher regression by restoring a literal `## 7.1 Near-term` heading and renumbering the rest, verified by an actual `session_launcher.py` re-run rather than by inspection alone. A second Codex pass independently reconfirmed all four fixes.

- Commit SHA: `75d1242`
- `python -m pytest`: 374 passed plus 1 skip (unchanged - no code touched). `python scripts/validate_repository.py` (full mode): 0 errors, 157 warnings.

---

# 10. Session-Wide WP4 - Independent Repository Verification

**Handover preparation**: an [[ESR-0034_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0034 WP4 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session content range (`25ad603`..`75d1242`) across all three Work Packages.

**Pass, one disclosed environmental limitation, no blocking findings**: Codex independently confirmed `git diff --stat 25ad603..75d1242` matches the handover's claimed 4 files/101 insertions/66 deletions exactly, that only `EBR-0001`/`REG-0001`/`JRM-0001`/`PST-0001` were touched with no `sentinel/`, `jarvis/`, `src/`, `src-tauri/` or `.github/workflows/` file anywhere in the diff, and confirmed `validate_repository.py`'s exact figures plus a live, clean `session_launcher.py` re-run (direct evidence the WP3 regression fix holds). Codex's own read-only sandbox could not independently reproduce `python -m pytest` - a known, previously-documented limitation (pytest cannot create its own temp/cache files under Codex's `-s read-only` mode, first disclosed during EBG-0096's own testing in a prior session), not a defect introduced here; its own partial run found zero actual test-assertion failures, and the Engineering Implementer's own direct run outside that sandbox confirmed 374 passed/1 skipped. Codex independently converged with the handover's own baseline recommendation: retain RBL-0020, no new baseline.

- Commit SHA: pending (handover committed as part of session closure)
- `python -m pytest`: 374 passed plus 1 skip. `python scripts/validate_repository.py` (full mode): 0 errors, 157 warnings.

---

# 11. Session-Wide WP5 - Repository Baseline Determination (RBL-0020 Retained)

**Both independent WP4 views recommended retaining the current baseline** rather than establishing a new one: this session's entire content was governance-artefact curation (backlog promotions, a roadmap rewrite) with no runtime, test, CI, dependency, security, or distribution-surface change - unlike ESR-0033's combination of governance work with a live product change and material security hardening. The Programme Sponsor's determination: **retain** - [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] remains the current accepted repository baseline, no new baseline established.

- Commit SHA: pending (recorded as part of session closure)
- `python -m pytest`: 374 passed plus 1 skip throughout. `python scripts/validate_repository.py` (full mode): 0 errors, 157 warnings (stable).

---

# 12. Governance Process Notes

One real scope expansion occurred at each of WP1 and WP3, both flagged plainly by the Engineering Implementer before proceeding rather than silently absorbed - consistent with the standing scope-creep-flagging practice EBG-0092 (itself promoted at WP1) exists to formalise: WP1 grew from a 2-item promotion to a 21-item batch on explicit Programme Sponsor direction; WP3 grew from a conversational roadmap discussion into a formal controlled-artefact rewrite, also on explicit direction.

No environment gaps or lost background processes occurred this session, unlike ESR-0033. The one tooling limitation encountered (Codex's read-only sandbox cannot reproduce `pytest`, Section 10) was already known and disclosed from a prior session, not newly discovered here.

Every Work Package in this session followed the full cycle without exception: draft, Codex read-only review (relayed via `return-findings` under standing per-session Sponsor approval), a fix round wherever findings existed (WP1, WP2 and WP3 all had at least one genuine finding), a second Codex confirmation pass, Sponsor approval via the real deployed Sponsor Approval Service, `submit-response`, then commit.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | 22 items promoted from Candidate to Approved Backlog this session (WP1: 21, WP2: 1). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B rewritten in full at WP3 - now the authoritative dependency-ordered path to a working version. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0034_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0034 WP4 Handover]] | Session-wide Independent Repository Verification and Baseline Determination record, Section 10/11. |
| [[ESR-0033_ENGINEERING_SESSION_REPORT|ESR-0033]] | Prior closed session this one continues from. |
| [[RBL-0020_REPOSITORY_BASELINE|RBL-0020]] | Repository baseline retained at Section 11 - no new baseline established this session. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 25 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP1 (21-item backlog promotion batch, two Codex fix rounds), WP2 (EBG-0021 promoted separately given its Action-faculty/GAM-0001 significance, one Codex fix round), WP3 (JRM-0001 Track B rewritten as an 8-phase dependency-chain roadmap, four Codex-caught findings fixed including a real session_launcher.py regression), and session-wide WP4 (Independent Repository Verification, Pass, one disclosed pre-existing environmental limitation) and WP5 (Repository Baseline Determination, RBL-0020 retained). Ninth session run entirely through the AIEMS Exchange Bridge and the deployed Sponsor Approval Service with no manual relay. Status Open to Closed. |
