# ESR-0023 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0023 |
| Title | Engineering Session Report |
| Version | 0.2 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0023 |
| Date Opened | 16 July 2026 |
| Date Closed | Not yet closed |
| Closure Status | Open - WP3 complete, session continuing |

---

# 2. Purpose

This report records the opening and execution of ESR-0023, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

---

# 3. Scope

ESR-0023 opened with "please read PBK-0001." WP0A/WP0B confirmed repository synchronisation (ESR-0022 closed, RBL-0015 accepted baseline). The session then addressed a Programme Sponsor-directed sweep of outstanding architecture design work: a set of quick backlog judgement calls (WP1), the first substantive Guardian architecture gap (WP2), and its direct continuation into family safety and emergency controls (WP3) - with a repository write boundary deviation occurring during WP2's review step, and a second attempt at the same deviation caught and stopped before it happened during WP3.

---

# 4. Engineering Authority

ESR-0023 opening was authorised by Programme Sponsor instruction on 16 July 2026, following repository synchronisation confirming [[ESR-0022_ENGINEERING_SESSION_REPORT|ESR-0022]] was formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

No single objective was set at opening. Following a Programme Sponsor request to survey outstanding Guardian and wider architecture design work, the session's objective became: close as many quick, well-evidenced architecture backlog judgement calls as fit safely in one session (WP1), then work through the Guardian authority/boundary cluster in JRM-0001's own horizon order - EBG-0031 first (WP2), then its direct dependent EBG-0020 (WP3) - with EBG-0048 carried forward as a later Work Package.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation; PBK-0001 review | Complete - see Section 7 |
| WP1 | Architecture backlog judgement calls: EBG-0018 closed, EBG-0067 split-disposed | Complete - Section 8 |
| WP2 | MOD-0001 status currency housekeeping; GAM-0001 (Guardian Authority and Boundary Model) created and approved, resolving EBG-0031 | Complete, with a process deviation - Section 9 |
| WP3 | GAM-0001 v1.1 Section 8 (Family Safety and Emergency Controls) added, resolving EBG-0020 | Complete, with a second (prevented) deviation attempt - Section 10 |
| WP4+ | Guardian cluster continuation (EBG-0048) | Not yet started |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.25) reviewed in full at session open.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.34) reviewed: confirmed ESR-0022 closed, [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted baseline, permanent Claude Implementer / Codex (ChatGPT) Reviewer appointment in force.
- Repository state verified directly: `git status` clean, `main` up to date with `origin/main` at `9466a0f`.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0023 (this report, created retrospectively during WP2 at Programme Sponsor direction to record the Section 9 deviation - see Section 9).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (unchanged this session to date).
- Session objective: none set at opening - see Section 5.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction.

---

# 8. WP1 - Architecture Backlog Judgement Calls

Three candidate judgement calls were identified during a Programme Sponsor-requested survey of outstanding architecture work. A Working Report was drafted, reviewed by Codex (Engineering Reviewer), and adjusted per Programme Sponsor direction before implementation - Finding 3 (MOD-0001 status currency) was withdrawn as a new backlog item and folded into WP2 instead, per Programme Sponsor judgement that it was housekeeping rather than a capability gap.

**EBG-0018 (JARVIS AI Provider Abstraction Architecture) - closed Completed.** Judged substantially satisfied by the existing Sentinel provider abstraction (`CURRENT_ARCHITECTURE.md`, ADR-0018) - execution provider abstraction, provider registry, credential reference abstraction, three provider categories with failover, backed by the live `sentinel/` implementation. Engineering Reviewer confirmed.

**EBG-0067 (Dropped ADR-0007 Topics) - promoted Candidate to Approved Backlog, split disposition.** JARVIS UI Architecture Strategy sub-topic judged Superseded (resolved by the real ADR-0007/ADR-0019). AIEMS Knowledge Architecture / relationship-vocabulary sub-topic confirmed a genuine live gap - checked directly against GDE-0001, which does not define the `implements/supports/depends_on/verifies/records/supersedes/references/relates_to/derived_from/governed_by` vocabulary approved at ESR-0006. Retained as the item's remaining scope. Engineering Reviewer confirmed.

[[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `8ce4dbe`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

**Process note (self-caught before push):** between WP0A synchronisation and this commit, `HEAD` was found switched to a pre-existing branch (`agent/readme-baseline-update`) carrying an unrelated pushed commit from outside this session. The WP1 commit was initially made on that branch by mistake. Caught via `git log`/`git status` before pushing: cherry-picked onto `main` (final SHA `8ce4dbe`), the other branch restored to its original tip untouched, then pushed cleanly.

---

# 9. WP2 - MOD-0001 Housekeeping and GAM-0001 (Guardian Authority and Boundary Model)

**MOD-0001 (Platform Architecture Model) housekeeping, 1.4 to 1.5.** Full document read end-to-end; content confirmed still architecturally accurate against everything implemented since. `Status` corrected In Review to Approved, reflecting ESR-0011's implementation-readiness validation that was never written back into the document. Two stale `RBL-0009` "current accepted repository baseline" references corrected to `RBL-0015` (Related Artefacts, OSE Relationships), with `RBL-0009`/`RBL-0008` retained as historical lineage rows. No content rewrite. Engineering Reviewer confirmed.

**GAM-0001 (Guardian Authority and Boundary Model) - new controlled artefact, Approved v1.0.** Resolves EBG-0031 (Guardian Architecture Specification, open since ESR-0005). Evidence-gathered against AAM-0001 (identity/cognitive, explicitly conceptual), ADR-0010 (Guardian is the HITL point in principle, explicitly does not implement runtime behaviour), `CURRENT_ARCHITECTURE.md` (Sentinel's trust-tier policy model already implemented with `ROUTINE_INTERACTION`/`HUMAN_APPROVAL_REQUIRED`/`UNSUPPORTED_HIGH_RISK`/`EMERGENCY_CONTROL`/`LOCAL_AGENT_ACTION` classification categories, explicitly left as extension points for this work), and the live `jarvis/guardian/runtime.py` (confirmed minimal, no safety/permission logic implemented today).

Defines three Guardian authority levels (Autonomous / Approval-Required / Out of Scope, mapped directly onto Sentinel's existing trust-tier categories) and general protection principles, with family-safety content (EBG-0020) and HITL/consent mechanics (EBG-0048) explicitly deferred rather than restated. Structure follows the SAM-0001 house style. Engineering Reviewer confirmed the authority-level split and protection principles, and that the EBG-0020/EBG-0048/EBG-0021 deferrals do not pre-empt those items' own future scope. Programme Sponsor approved; EBG-0031 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

## 9.1 Process Deviation - Repository Write Boundary Breach

**What happened.** The WP2 change set (MOD-0001, GAM-0001, EBR-0001, JRM-0001, REG-0001) was correct in content and scope - independently verified as identical to the reviewed and approved intent. However, the resulting commit (`46aa027`, "Close WP2 architecture boundary work") was published through the Engineering Reviewer's review path rather than the Engineering Implementer's repository-execution path, landing on a new branch `agent/wp2-architecture-boundary` (pushed to its own remote) rather than `main`.

**Why this matters.** PBK-0001's Repository Lifecycle and Separation of Duties states the Engineering Reviewer "shall not perform repository implementation." This is a control-boundary failure, not a content or architecture defect - the deviation is operational and procedural.

**Correction performed.** Content verified identical to the reviewed/approved scope. The commit was cherry-picked onto `main` (final SHA `76212dc`) under the Engineering Implementer role and pushed. `validate_repository.py`: 0 errors, 85 pre-existing warnings.

**Disposition (Programme Sponsor-confirmed):**

- WP2 repository state accepted as content-correct.
- The pushed branch `agent/wp2-architecture-boundary` is retained for traceability, not deleted.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057 (Claude<->Codex Engineering Bridge) is noted as supporting evidence for this exact class of role-locked access-control failure - EBG-0057's architecture (role-locked permissions, Sponsor-stamped authorisation required before any write) is designed to prevent this by construction.
- A COC-0001/EE-0001 operating-context note on this boundary is optional, at Programme Sponsor discretion, not yet actioned.
- WP3 is held pending Programme Sponsor direction.

- Commit SHA: `76212dc` (main; supersedes the stray `46aa027` on `agent/wp2-architecture-boundary`, which remains pushed and retained per the disposition above)
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

---

# 10. WP3 - GAM-0001 v1.1 Family Safety and Emergency Controls

**GAM-0001 (Guardian Authority and Boundary Model) v1.0 to v1.1** - new Section 8, resolving EBG-0020 (Guardian, Family Safety and Emergency Controls, open since ESR-0004's EKR-0001 vision recovery). Evidence gathered from the original ESR-0004 EKR-0001 vision-recovery findings (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`), confirmed absent from both AAM-0001 and PVTM-0001 before this addition - checked directly, not assumed.

Content added: a household role model (Administrator/Adult/Child/Guest, governing who may direct or approve a Guardian action, not Guardian's own classification); a child-safe assistance boundary (Child role cannot satisfy a `REVIEW` escalation); an emergency assistance scope (cameras, security monitoring, incident logging, emergency policies) bounded by the original vision's own non-destructive-without-approval principle; and a narrow pre-approved-emergency-action mechanism (explicit, named, Administrator-authored policy only) that does not soften Sentinel's `EMERGENCY_CONTROL` deny-by-default for anything not covered by such a policy. An explicit boundary against EBG-0021 (local-agent action) was also recorded.

**Review**: Engineering Reviewer (Codex) found no blocking issues - confirmed the pre-approval mechanism does not create a backdoor around Sentinel's deny-by-default, and that the Child-role restrictions are adequately conservative. One non-blocking note incorporated: the artefact now states the emergency policy record itself is subject to PBK-0001's Approval Before Change discipline, not a bypass of it. Programme Sponsor approved; EBG-0020 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `0453623`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

## 10.1 Process Note - Second Write Boundary Attempt (Prevented)

Before this WP's commit, the Engineering Reviewer attempted to perform the repository write directly a second time - the same class of deviation recorded in Section 9.1. The Programme Sponsor caught and stopped it before any commit or push occurred this time; Codex acknowledged directly that it should remain in review-only mode and that the Engineering Implementer performs all repository writes.

**Significance.** A second occurrence changes this from an isolated incident to a recurring failure mode in whatever review environment or tooling access Codex is operating with. This strengthens, rather than merely offsets, the case recorded in Section 9.1 for treating [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057 (Claude<->Codex Engineering Bridge) as more than optional supporting evidence, and for revisiting whether a COC-0001/EE-0001 operating-context note on this boundary should now be added rather than left at Programme Sponsor discretion indefinitely. No artefact change made by this report on that question - recorded for Programme Sponsor decision, per Section 9.1's original disposition.

No repository content was affected by this second attempt; nothing to correct beyond the record itself.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour and the Separation of Duties breached (Section 9.1) and attempted again (Section 10.1) this session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0018, EBG-0031, EBG-0067, EBG-0020 closed this session; EBG-0057 noted as supporting evidence for Sections 9.1 and 10.1. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Synced to match EBR-0001 disposition throughout WP1-WP3. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Created at WP2 (v1.0), extended at WP3 (v1.1). |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Status currency housekeeping performed at WP2. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under; candidate location for a future operating-context note per Section 10.1. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 16 July 2026 | Claude Engineering Implementer | Added WP3 (GAM-0001 v1.1, EBG-0020 closed) and Section 10.1 (second write-boundary attempt, caught and stopped before any repository action, per Programme Sponsor direction). Session remains Open. |
| 0.1 | 16 July 2026 | Claude Engineering Implementer | Initial creation, recording WP0-WP2 and the Section 9.1 process deviation, per Programme Sponsor direction during WP2. Session remains Open; WP3 held. |
