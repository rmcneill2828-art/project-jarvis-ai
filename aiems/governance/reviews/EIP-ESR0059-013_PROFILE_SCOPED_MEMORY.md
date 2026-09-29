# EIP-ESR0059-013 - Profile-Scoped Memory

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-013 |
| Title | Engineering Implementation Package: WP13 Profile-Scoped Memory |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP13 |

---

# 2. Purpose

Implements ESR-0059 WP13: the memory-isolation half of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0132. The role-enforcement half follows as its own Work Package, by the Programme Sponsor's decision.

Every household profile shared one pool of Personal Memory and one conversation history, so one member's retained memories and recent conversation reached every other member's turns - including a Child's.

**Programme Sponsor's decisions** (29 September 2026, "go with your recommendations"):

1. Memories saved before profiles existed become **shared household notes**, visible to every profile; only an Administrator can delete them.
2. With **no profile selected**, saving a memory is refused ("select a profile first"), and conversation uses household notes only.
3. **Two Work Packages**: memory isolation now (this one), role enforcement next.

---

# 3. Repository Context Investigated

* `jarvis/memory/store.py` - no owner column; WP12's migration mechanism makes adding one safe.
* `GuardianRuntime` held one `GuardianCognitiveCore`, so conversation history was shared across profiles too.
* ESR-0046 deliberately kept the runtime unaware of profiles; `StdioRpcServer` already holds the identity service and knows the active profile.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.2 - personal memory is private to the individual.
* Memory backups contain memories but not profiles (a separate database), so profile ids in a backup need not exist on the installation it is restored to.

---

# 4. Scope

## 4A. Storage

* Memory schema migration 2 (the first real use of WP12): `personal_memory.profile_id`, NULL meaning a shared household note. Existing memories therefore become household notes (decision 1).
* `list_visible(profile_id)` / `count_visible(profile_id)`: a profile's own memories plus household notes; household notes only with no profile. `get(record_id)`.
* Backups export `profile_id`; restores accept it and treat its absence (pre-WP13 backups) as a household note.

## 4B. Service and runtime

* A proposal carries its profile to approval. `delete()`: a profile may delete only its own memories; a household note only an Administrator (decision 1). **Another profile's memory is reported exactly like a missing one**, so its existence is never revealed.
* `GuardianRuntime` keeps **one Cognitive Core per profile**, so recent conversation is also isolated, and passes only the visible memories into each turn.

## 4C. RPC and UXP

* The RPC layer resolves the active profile and passes it down for `guardian.converse`, `memory.propose`, `memory.list`, `memory.status` and `memory.delete` (with an Administrator flag from the profile's role). `memory.propose` without a selected profile is refused (decision 2). `memory.list` includes `profileId`.
* **Restore - a gap found during implementation, not by review**: restoring onto another installation would leave every memory owned by a profile that does not exist there, visible to nobody. Such memories now go to the profile performing the restore - kept private, never turned into household notes - and the result reports how many (`reassignedToActiveProfile`). A restore therefore needs a selected profile, like saving does.
* Memory Management panel: household notes are labelled "(Household)".

## 4D. Tests

* New `jarvis/tests/test_profile_scoped_memory.py` (10): per-profile visibility; conversation carries only the active profile's memories and history; own-memory delete; another profile's memory indistinguishable from a missing one, even for an Administrator; household-note delete Administrator-only; saving without a profile refused over RPC; two profiles isolated over RPC; restore reassigns unknown owners to the restoring profile; restore without a profile refused; a pre-WP13 backup restores as household notes.
* Existing tests updated for the new rules (memories now owned by a profile; stores now at schema version 2; RPC memory tests select a profile first).

## 4E. Explicitly out of scope

* **Role enforcement** - who may approve a memory proposal (a Child or Guest cannot satisfy a `REVIEW` escalation under GAM-0001 Section 8.1), Guest access to household notes, Administrator-only backup/restore. Next Work Package.
* Credentialed authentication - profiles remain unauthenticated, so this is isolation between cooperating household members, not a security boundary against someone who selects another profile.
* Moving a memory between profiles, or into or out of the household.

## 4F. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: every memory read path the product reaches goes through `list_visible`/`count_visible` - conversation, list and status - while `list_all` remains only for backup; the profile id always comes from the identity service on the backend, never from the UXP request, so the frontend cannot ask for another profile's memories; the delete path checks ownership before existence is revealed; per-profile Cognitive Cores are created lazily and only on the single slow-lane worker (WP5), so no new cross-thread state; the restore reassignment runs in one store transaction. **Disclosed limitation**: profiles are unauthenticated, so this isolates cooperating household members rather than defending against someone deliberately selecting another profile - credentialed authentication remains out of scope.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`, `npm run build`, `npx playwright test`; the full suite against a fake home directory creates no files there.

## 5A. Live check - performed against the real backend process

With a recording stand-in for Ollama: saving without a profile was refused; Alice (Adult) and Ben (Child) each saved a memory and chatted; Ben's memory list showed only his own memory; the model received only Alice's memory on her turn and only Ben's on his, with none of Alice's conversation on Ben's turn. A copy of the real memory store upgraded to schema version 2 with the new `profile_id` column.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* No profile's memories or conversation reach another profile's turns or lists.
* Pre-existing memories remain available to everyone, as household notes.
* Nothing becomes invisible to everyone after a restore.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4F (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP13 draft, implementing the Programme Sponsor's three decisions. Memory schema migration 2 (`profile_id`), per-profile visibility and deletion rules, per-profile conversation history, RPC resolution of the active profile, restore reassignment of unknown owners (a gap found during implementation), household label in the UXP. pytest 739 passed/1 skipped, Playwright 26/26, ruff/build/validator clean, no fake-home files. Live-checked through the real backend. Not yet reviewed, approved or committed. |
