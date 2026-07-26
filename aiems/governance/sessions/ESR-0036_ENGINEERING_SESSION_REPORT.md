# ESR-0036 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0036 |
| Title | Engineering Session Report |
| Version | 1.3 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0036 |
| Date Opened | 26 July 2026 |
| Date Closed | 26 July 2026 |
| Closure Status | Closed - WP1-WP2 complete, session-wide WP3 Pass (after one fix round), WP4 Establish (RBL-0022 accepted) |

---

# 2. Purpose

This report records the opening and execution of ESR-0036, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0035_ENGINEERING_SESSION_REPORT|ESR-0035]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

**Process note, disclosed rather than silently corrected:** this report was created retroactively, during what became WP2, rather than during WP0B as PBK-0001's Engineering Session Lifecycle specifies. WP0A/WP0B's substantive work (repository synchronisation, objective confirmation, Programme Sponsor approval) was performed in full before WP1 began; only the report artefact itself was created late. Recorded here as a documentation-debt finding against this session's own process, consistent with the Whole-Document Staleness Sweep discipline applied to other artefacts.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0035_ENGINEERING_SESSION_REPORT|ESR-0035]] closed (25 July 2026), [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] the current accepted baseline, working tree clean, pre-commit governance hook active. A recurring documentation-staleness finding was identified (README.md, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] still citing RBL-0020/ESR-0035-open), matching the same pattern already corrected at ESR-0033 WP1 and ESR-0035 WP1. `scripts/session_launcher.py` (EBG-0107) was independently re-verified working, correctly reporting Next WP Candidate and the EBR-0001 Section 5A active-backlog snapshot.

The Programme Sponsor directed a deliberate departure from PBK-0001's Documentation-Debt Priority discipline for this session: rather than fixing the documentation staleness first (the discipline's normal default), [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 (Guardian Cognitive Core Implementation, the roadmap's flagged critical-path item) was selected as WP1, with the documentation fix deferred to the last engineering Work Package before session-wide verification and closure - a deliberate efficiency choice (one consolidated documentation pass capturing both the pre-existing staleness and whatever new state WP1 itself creates, rather than two separate passes), not an oversight.

---

# 4. Engineering Authority

ESR-0036 opening was authorised by direct Programme Sponsor instruction on 26 July 2026, immediately following ESR-0035's closure, confirming [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] as the accepted repository baseline at session open.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Deliver EBG-0108's first implementation increment (static persona injection), then correct the accumulated documentation staleness in a single consolidated pass that also captures this session's own new state, before session closure.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0108 first increment: static Guardian persona injection | Complete |
| WP2 | Consolidated documentation staleness fix (README, COC-0001, PBK-0001) plus this session report | Complete |
| WP3 | Session-wide Independent Repository Verification | Complete - Pass (after one fix round) |
| WP4 | Session-wide Repository Baseline Determination | Complete - Establish (RBL-0022) |

---

# 7. WP1 - EBG-0108 First Increment: Guardian Persona Injection

Delivered the first authorised increment of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 (Guardian Cognitive Core Implementation, Approved Backlog, High), against the current architecture gap: `GuardianRuntime.converse()` was a single delegation with no persona, no memory read and no reasoning loop (confirmed by direct codebase research before scoping). This WP closed only the "no persistent persona" portion - static, additive, no memory wiring or reasoning loop, both explicitly deferred to future EBG-0108 increments.

**Persona content provenance:** the Programme Sponsor recalled Guardian's personality having been discussed previously. A targeted search (delegated to Codex as Engineering Reviewer, per the Sponsor's direction to route in-depth research to Codex rather than spend Claude's own effort on it going forward) found "EKR-0001 Task 2: Recovering the Personality & Behaviour of JARVIS", a full 15-point character draft recovered during ESR-0004 ([[FCH-0004_ESR-0004_FULL_CHAT_HISTORY|FCH-0004]], approx. lines 10890-11166) - drafted for JARVIS before the ESR-0008 identity split moved the user-facing personality to Guardian, and the one EKR-0001 recovered item never promoted into an [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] backlog item alongside its siblings (EBG-0017 through EBG-0025). The Programme Sponsor directed this draft be formally adopted now rather than deferred further, and personally reviewed and approved the exact persona wording (a content/tone judgement reserved to the Sponsor, not delegated to either AI role).

**Governance:** [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] (0.3 to 0.4): new "Guardian Persona" section under Canonical Identity Model, formally adopting the Sponsor-approved wording, explicitly disclosing that the original draft's household-role differentiation (children/adults/guests) is deferred - no user-identity plumbing exists in `ConversationRequest` today.

**Implementation:** additive, backward-compatible threading of the approved persona string through `GuardianRuntimeConfig.persona` (new `DEFAULT_GUARDIAN_PERSONA` constant) -> `GuardianRuntime.converse()` -> `ConversationRequest.persona` (new optional field) -> `SentinelGatedConversationProvider.generate()` -> `ProviderRequest.system_prompt` (new optional field) -> each live provider's own native mechanism: OpenAI (leading `system` message), Gemini (`systemInstruction`), Ollama (`system` field) - injected only when truthy. `LocalEchoProvider` untouched. Persona deliberately kept out of Sentinel audit metadata.

Run entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service: a pre-implementation research task and a separate design-review submission to Codex (Pass, with findings - named persona constant instead of an inline literal, decide blank-persona behaviour, add positive test coverage per layer, keep persona out of audit metadata - all folded into the implementation), Programme Sponsor approval verified directly against the Sponsor Approval Service's own decision database (two `approve` records for ESR-0036/WP1 at the correct repository ref, not merely asserted in chat), `submit-response`, commit, push, then post-commit independent re-verification (Pass, no blocking issues).

- Files: `jarvis/guardian/config.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/conversation.py`, `jarvis/interfaces/sentinel_conversation.py`, `sentinel/providers.py`, `sentinel/openai_provider.py`, `sentinel/gemini_provider.py`, `sentinel/ollama_provider.py`, five test files (`test_openai_provider.py`, `test_gemini_provider.py`, `test_ollama_provider.py`, `test_sentinel_conversation.py`, `test_guardian_runtime.py`), [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- `python -m pytest`: 381 passed, 1 skipped (was 374 passed, 1 skipped - 7 new tests, no regressions). `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings - one real REG-0001/AAM-0001 version-tracking mismatch found and fixed during this WP's own validation pass, before commit.
- Commit SHA: `d72a8ba`, pushed (`6cf2aeb..d72a8ba`).
- **Post-commit independent verification**: Codex re-reviewed the actual pushed diff (`git show d72a8ba`) in a fresh read-only pass - **Pass**. Confirmed persona threading matches the approved design exactly, `LocalEchoProvider` untouched, AAM-0001/REG-0001 tracking consistent, touched files exactly within expected scope (no `jarvis/memory/`, `src/`, `src-tauri/`, `.github/workflows/`). One non-blocking observation: no provider-level negative test for a blank `system_prompt` (truthiness-check coverage and Sentinel-layer `None` coverage exist instead) - noted, not a fail.

---

# 7A. WP2 - Consolidated Documentation Staleness Fix

Corrected the recurring RBL-0020/ESR-0035-open staleness pattern (same as ESR-0033 WP1 and ESR-0035 WP1) in README.md, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], applying the Whole-Document Staleness Sweep discipline to each document. Also created this ESR-0036 report retroactively (a disclosed process gap - PBK-0001's Engineering Session Lifecycle specifies the report should be created at WP0B, before WP1) and registered it in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]. Updated [[PST-0001_PROGRAMME_STATUS|PST-0001]] Sections 3/4A for ESR-0036 opening and WP1's completion.

Run entirely through the AIEMS Exchange Bridge and the deployed Sponsor Approval Service, the same pattern as WP1.

- **Initial design review**: Codex found two blocking issues - README's Current Phase row still described stale ESR-0035 content rather than ESR-0036/EBG-0108, and this report's own wording claimed the documentation fix was deferred to "the session's last Work Package," contradicted by WP3/WP4 still Pending. Both fixed (README corrected; wording changed to "the last engineering Work Package before session-wide verification and closure" throughout). Fix-round re-review: **Pass**.
- Commit SHA: `4667374`, pushed (`d72a8ba..4667374`).
- **Post-commit independent verification**: Codex re-reviewed the actual pushed diff (`git show 4667374`) and found a genuine miss - the fix had only swept the PST-0001 sections directly touched (Section 3/4A), not the whole document, leaving 3 current-facing RBL-0020 references elsewhere (Repository Acceptance row, session-start guidance, and the Related Artefacts list, which had no RBL-0021 row at all). Fixed in a new commit (not an amend): `26dfc55`, pushed (`4667374..26dfc55`). Deliberately did not rewrite the surrounding paragraph's separate, older ESR-0028/29/30-era staleness near the session-start guidance - out of this finding's scope. Final post-commit re-review: **Pass**, no further issues.
- `python -m pytest`: 381 passed, 1 skipped throughout (no code touched). `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings throughout.

---

# 8. Governance Process Notes

Two deliberate departures from standing default practice occurred this session, both flagged plainly rather than silently accommodated:

1. **Documentation-Debt Priority deferred, not skipped.** PBK-0001's Documentation-Debt Priority discipline normally puts documentation staleness first at WP0/WP1 selection. The Programme Sponsor directed EBG-0108 be WP1 instead, with the documentation fix moved to the last engineering Work Package before session-wide verification and closure (WP2, ahead of WP3/WP4) - reasoned as consolidating two documentation passes into one, since WP1's own new state would otherwise need a second pass regardless.
2. **Research delegation to Codex.** The Programme Sponsor directed that in-depth/open-ended research (the historical-archive sweep for Guardian's prior personality discussion) be routed to Codex via the AIEMS Exchange Bridge rather than a Claude sub-agent, to conserve Claude's own effort for the engineering itself, given the project's engineering is expected to grow more complex from this session onward.

No environment gaps or lost background processes occurred this session. Every relay of Codex's findings into the bridge (`return-findings`, performed by the Engineering Implementer since Codex's own sandbox cannot write there directly) was preceded by explicit, per-instance Programme Sponsor approval - eight such relays this session across WP1 (research task, design review, post-commit review) and WP2 (design review, fix-round confirmation, post-commit finding, post-commit fix confirmation, final post-commit confirmation) - the last two fix rounds Codex's own real reviews caught, not merely assumed clean.

---

# 8A. Session-Wide WP3 - Independent Repository Verification

**Handover preparation**: an [[ESR-0036_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0036 WP3 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session content range (`6cf2aeb`..`26dfc55`) across both Work Packages.

**Pass, after one fix round - no remaining blocking findings**: Codex independently confirmed `git diff --stat 6cf2aeb..26dfc55` matches the handover's claimed 20 files/315 insertions/47 deletions exactly, and that no `src/`, `src-tauri/`, `.github/workflows/` or `jarvis/memory/` file was touched anywhere in the diff. First pass caught a genuine defect the handover's own first draft had not disclosed: the ESR-0036 report itself had been bumped to v1.1 (recording WP2's completion) while REG-0001's tracking row still read 1.0 - `validate_repository.py` correctly failed on this. Fixed; Codex's fix-round pass independently re-ran `validate_repository.py` itself (its sandbox allowed this that time, unlike `pytest`, which remained blocked by a temp-directory restriction throughout - a disclosed environmental limitation consistent with prior sessions) and confirmed clean. Codex independently converged with the handover's own baseline recommendation: establish a new baseline, superseding RBL-0021.

- `python -m pytest`: 381 passed, 1 skipped. `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings (after the fix above).

---

# 8B. Session-Wide WP4 - Repository Baseline Determination (RBL-0022 Established)

**Both independent WP3 views recommended establishing a new baseline** rather than retaining the current one: WP1 delivered a genuine, live-verified product code change (the first implementation work of any kind against EBG-0108, touching the Guardian conversation path and all three live Sentinel provider adapters, backed by 7 new tests), unlike WP2's documentation-only content. The Programme Sponsor's determination: **establish** - [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] is accepted as the new current repository baseline, superseding [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]].

- `python -m pytest`: 381 passed, 1 skipped throughout. `python scripts/validate_repository.py` (full mode): 0 errors, 172 warnings.

---

# 9. Related Artefacts

* [[ESR-0035_ENGINEERING_SESSION_REPORT|ESR-0035]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Documentation-Debt Priority (deliberately deferred, Section 8) and Feature-First Delivery Discipline, both engaged this session.
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] - Guardian Persona section added (0.3 to 0.4), WP1.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0108, first increment delivered this session.
* [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] - current accepted repository baseline, established at this session's WP4.
* [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] - prior accepted repository baseline, superseded by RBL-0022.
* [[FCH-0004_ESR-0004_FULL_CHAT_HISTORY|FCH-0004]] - source of the recovered persona draft formally adopted this session.
* [[ESR-0036_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0036 WP3 Handover]] - session-wide Independent Repository Verification and Baseline Determination record, Section 8A/8B.

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 26 July 2026 | Claude Engineering Implementer | ESR-0036 formally closed. Session-wide WP3 (Independent Repository Verification: Pass, after one fix round) and WP4 (Repository Baseline Determination: Establish - RBL-0022 accepted, superseding RBL-0021) complete. |
| 1.1 | 26 July 2026 | Claude Engineering Implementer | ESR-0036 WP2 Complete: consolidated documentation staleness fix, across three commits (`4667374`, then a post-commit fix `26dfc55` after Codex caught a whole-document-sweep miss). |
| 1.0 | 26 July 2026 | Claude Engineering Implementer | ESR-0036 opened. WP1 (EBG-0108 first increment - Guardian persona injection) Complete. Report created retroactively during WP2, a disclosed process gap against PBK-0001's own session lifecycle. |
