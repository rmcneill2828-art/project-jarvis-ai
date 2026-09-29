# EIP-ESR0059-014 - Household Role Enforcement for Memory

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-014 |
| Title | Engineering Implementation Package: WP14 Household Role Enforcement for Memory |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP14 |

---

# 2. Purpose

Implements ESR-0059 WP14: the role-enforcement half of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0132, following WP13's memory isolation, as the Programme Sponsor decided (two Work Packages).

[[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's household roles - Administrator, Adult, Child, Guest - were labels only: any profile could approve a memory proposal, a Guest saw every shared household note, and anyone could back up or restore every profile's memories.

---

# 3. Repository Context Investigated

* GAM-0001 Section 8.1: Adult may approve `REVIEW`-classified actions; a Child cannot satisfy a `REVIEW` escalation; a Guest has "no access to family-shared memory or approval capability"; the Administrator holds full household authority.
* `PersonalMemoryService.propose()` requires a Sentinel `REVIEW` outcome, so approving a proposal is exactly satisfying a `REVIEW` escalation.
* `memory.backup` exports, and `memory.restore` replaces, every profile's memories (WP13).
* `StdioRpcServer` knows the active profile and its role (WP13); the runtime deliberately does not.

---

# 4. Scope

## 4A. Rules, enforced at the RPC boundary

| Action | Allowed roles |
|---|---|
| Approve a memory proposal (`memory.approve`) | Administrator, Adult |
| Decline a proposal (`memory.deny`) | Any - it stores nothing |
| See shared household notes (list, count, conversation) | Administrator, Adult, Child - not Guest |
| Back up memory (`memory.backup`) | Administrator |
| Restore memory (`memory.restore`) | Administrator |
| Delete own memory / household note | unchanged from WP13 (own: any; household: Administrator) |

With no profile selected, approval, backup and restore are refused ("Select a profile first."). Refusals are `PermissionError`s naming the rule.

## 4B. Plumbing

* `include_household` flag through store, service and runtime (`list_visible`, `count_visible`, `converse`, `list_memory`, `memory_status`), defaulting to the WP13 behaviour. The store builds its visibility clause from fixed SQL fragments only; the profile id is always a bound parameter.

## 4C. Documentation

README, PCB-0001 (2.17 to 2.18) and the JARVIS Capability Readiness Matrix (2.17 to 2.18) now record role enforcement for memory, and that credentialed authentication and role authority beyond memory remain open.

## 4D. Tests

New `jarvis/tests/test_household_roles.py` (12): Child and Guest cannot approve (and nothing is stored); Administrator and Adult can; approval with no profile refused; a Child can decline; a Guest sees no household notes in list or count; a Guest's conversation never carries household notes while an Adult's does; Adult, Child and Guest cannot back up or restore (and nothing is written); an Administrator can back up. Existing tests updated to the role each scenario needs.

## 4E. Explicitly out of scope

* GAM-0001 Section 8.2's child-safe content boundary, and role authority over anything beyond memory (agents, the future Action faculty).
* An Adult approving another member's pending proposal from the UXP - there is no proposal UI yet.
* Credentialed authentication: profiles remain unauthenticated, so these rules separate cooperating household members and are not a security boundary.

## 4F. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: every role check reads the active profile from the backend's identity service, never from request parameters, so the UXP cannot claim a role; each check runs before any store change, and the tests confirm nothing is written on refusal; the only dynamic SQL is a choice between two fixed fragments; Guest exclusion covers all three read paths (list, count, conversation). Deliberate choice, disclosed: declining a proposal is not restricted, since it stores nothing. No change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`, `npx playwright test`; the suite creates no files in a fake home.
* **Live check against the real backend process**: a Child approving its own memory was refused; an Adult's approval succeeded; an Adult's backup was refused; an Administrator's succeeded; a Guest's memory list was empty.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* Only Administrator and Adult profiles can approve saving a memory.
* A Guest never sees or is prompted with household notes.
* Only an Administrator can back up or restore memory.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4F (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP14 draft. GAM-0001 Section 8.1 roles enforced for memory: approval Administrator/Adult only, Guests excluded from household notes, backup/restore Administrator-only; declining open to all. pytest 751 passed/1 skipped, Playwright 26/26, ruff/validator clean, no fake-home files. Live-checked through the real backend. Not yet reviewed, approved or committed. |
