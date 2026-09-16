# RBL-0038 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0038 |
| Title | ESR-0058 Repository Baseline (Engineering Reviewer Succession; BRD-0001 Recovery; Home Assistant Agent; Playwright Reliability Fix; Memory Management UXP) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0058_ENGINEERING_SESSION_REPORT|ESR-0058]] |
| Previous Baseline | [[RBL-0037_REPOSITORY_BASELINE|RBL-0037]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 16 September 2026 |
| HEAD at baseline creation | `505e8f1` |

---

# 2. Purpose

RBL-0038 records the repository baseline accepted by the Programme Sponsor at ESR-0058 WP8, superseding [[RBL-0037_REPOSITORY_BASELINE|RBL-0037]]. ESR-0058 opened at the Programme Sponsor's direct request to resolve EBG-0126 - the Engineering Reviewer role left permanently unfilled at RBL-0037's own acceptance, after ChatGPT/Codex was found retired on cost grounds. Unlike ESR-0057, this session both resolved that gap and then used the resolution throughout: every one of WP2 through WP7 was genuinely design-reviewed and post-commit-reviewed by GitHub Copilot CLI, the newly-appointed permanent Engineering Reviewer, via the AIEMS Exchange Bridge's real submit-to-review/return-findings flow - restoring the dual-AI verification rigour RBL-0037 explicitly flagged as absent.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0037_REPOSITORY_BASELINE|RBL-0037]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session; the Home Assistant agent and Memory Management UXP capabilities are not yet reflected there, flagged as a documentation-staleness item for a future session's Documentation Debt sync (itself now tracked as EBG-0134). |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0058 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation. Objective set by direct Programme Sponsor instruction: resolve EBG-0126.

**WP1 (Technical Feasibility Test)**: a scoped, non-blanket `copilot -p ... --allow-tool=...` invocation confirmed no `Create Unsafe Agents` classifier block - resolving EBG-0126's own open technical question in favour of GitHub Copilot CLI, where a same-purpose Antigravity CLI invocation had been blocked twice at ESR-0057.

**WP2 (Engineering Reviewer Re-appointment)**: [[EIP-ESR0058-001_ENGINEERING_REVIEWER_REAPPOINTMENT|EIP-ESR0058-001]] - COC-0001 rewritten (ChatGPT/Codex's tenure recorded and closed, 10 July 2026 to 14 September 2026; GitHub Copilot CLI appointed 16 September 2026); `scripts/aiems_bridge.py`'s `codex`-hardcoded reviewer identity generalised to a role-based `"reviewer"` (configurable via `AIEMS_REVIEWER_TOOL`). The first genuine end-to-end use of the renamed identity, and the first genuine post-commit review under the new standing arrangement.

**WP3 (BRD-0001 Recovery Implementation)**: [[EIP-ESR0058-002_BRD-0001_RECOVERY_IMPLEMENTATION|EIP-ESR0058-002]] - delivers BRD-0001 Section 6's recovery expectations in full (`import_snapshot()`, `restore_backup()`, `restore_memory()`, new `memory.restore` RPC method), completing both halves of EBG-0023's original scope (export at ESR-0057 WP2, recovery now). A real gap caught during implementation, not by review: `import_snapshot()` initially rejected `export_snapshot()`'s own tuple output.

**WP4 (Home Assistant State Query Agent)**: [[EIP-ESR0058-003_HOME_ASSISTANT_STATE_QUERY_AGENT|EIP-ESR0058-003]] - the third specialist agent (`home-assistant-state-query`, `ROUTINE_INTERACTION`), resolving EBG-0127. A real finding caught while updating documentation: MOD-0001 explicitly named Home Assistant as an example of an agent *not yet* authorised, directly contradicted by this delivery, corrected in the same edit.

**WP5 (Playwright E2E Reliability, EBG-0129)**: [[EIP-ESR0058-004_PLAYWRIGHT_E2E_RELIABILITY|EIP-ESR0058-004]] - resolves a reproduced parallel-worker cold-start race (12 failed/6 passed at default parallelism vs 17 passed/1 failed sequentially). The gap analysis's own literal recommendation (production build plus preview server) was tried first and **reverted, disclosed rather than silently dropped**: it broke `animationScheduler.spec.js`'s deliberate raw-source-import design. The actual fix - a `globalSetup` hook performing one sequential warm-up navigation before parallel workers start - was verified via repeated real `npx playwright test` runs (18/18, later 23/23 including WP6's new tests, across multiple runs), not a single lucky pass.

**WP6 (Memory Management UXP Surface, EBG-0131)**: [[EIP-ESR0058-005_MEMORY_MANAGEMENT_UXP_SURFACE|EIP-ESR0058-005]] - closes BRD-0001's own disclosed "RPC-only, no UXP surface" gap. New `memory.status` RPC method (record count only, never content), Tauri commands, and `src/MemoryManagementPanel.jsx` - a native folder-picker for backup, native file-picker for restore, with an explicit inline confirmation before any non-empty store is overwritten, mirroring rather than working around the backend's "recovery never runs silently" guarantee. New dependency: `tauri-plugin-dialog`.

**Session-wide WP7 (Independent Repository Verification)**: covering the full session range `c8999c8..HEAD` (10 commits, 36 files, 2115 insertions/80 deletions). A **genuine GitHub Copilot CLI review was available and used** - unlike ESR-0057's disclosed self-verification substitution. Independently confirmed commit/file counts, re-ran `pytest` (587 passed/1 skipped) and `validate_repository.py` (0 errors/333 warnings), confirmed `sentinel/policy.py`'s `LOCAL_AGENT_ACTION` boundary untouched all session. **Real finding**: EBR-0001's own EBG-0126 row was still "Candidate Backlog" despite the underlying WP1/WP2 work being genuinely done - fixed immediately. **Verdict: Conditional Pass**, the one finding fixed before closure.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with the Engineering Implementer's and Reviewer's own advisory - a permanent Engineering Reviewer succession, two real product capabilities (Home Assistant agent, Memory Management UXP), and a genuine test-infrastructure reliability fix, matching the Establish threshold applied at RBL-0035 through RBL-0037.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Engineering Reviewer section rewritten - ChatGPT/Codex's tenure recorded and closed; GitHub Copilot CLI appointed as the new permanent holder (WP2). |
| `scripts/aiems_bridge.py`, `scripts/tests/test_aiems_bridge.py` | Reviewer identity generalised from hardcoded `codex` to role-based `reviewer`, configurable via `AIEMS_REVIEWER_TOOL` (WP2). |
| `jarvis/memory/store.py`, `jarvis/memory/service.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py` | New Personal Memory recovery capability - `import_snapshot()`, `restore_backup()`, `restore_memory()`, new `memory.restore` RPC method (WP3); new `memory.status` RPC method and its full store/service/runtime chain (WP6). |
| `jarvis/agents/home_assistant_agent.py` (new) | `HomeAssistantClient`, `HomeAssistantStateQueryAgent` - the third specialist agent, resolving EBG-0127 (WP4). |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Stale "Home Assistant not yet authorised" claim corrected to record all three specialist agents delivered (WP4). |
| `tests/e2e/global-setup.js` (new), `playwright.config.js` | Cold-start parallel-worker race root-caused and fixed via a pre-worker warm-up navigation, resolving EBG-0129 (WP5). |
| `src/MemoryManagementPanel.jsx` (new), `src-tauri/src/lib.rs`, `src-tauri/Cargo.toml` | Memory Management UXP surface - native folder/file pickers, overwrite-confirmation flow, new `tauri-plugin-dialog` dependency, resolving EBG-0131 (WP6). |
| [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] | Section 8A (recovery, WP3) and Section 8B (UXP surface, WP6) added; Sections 8/8A's stale "no UXP surface" exclusions corrected. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0126, EBG-0023, EBG-0127, EBG-0129, EBG-0131 closed Complete; EBG-0130, EBG-0132, EBG-0133, EBG-0134 registered from the Programme Sponsor-requested GitHub Copilot CLI gap analysis (Candidate Backlog, no implementation authorised). |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session - the Home Assistant read-only agent and Memory Management UXP surface (both real, tested, live-wired capabilities) are not yet reflected there. EBG-0134 (Capability-Tracking Refresh Cadence), registered this session from the gap analysis, now formally tracks this recurring gap rather than leaving it an ad hoc flag at each baseline.

---

# 7. Architecture Outcomes

- The Engineering Reviewer role is filled again for the first time since RBL-0037's own acceptance - GitHub Copilot CLI, verified genuinely working across every Work Package this session (design review, post-commit review, and a full session-wide review), not merely appointed on paper.
- Personal Memory's backup/recovery lifecycle (BRD-0001) is now complete end-to-end: export (ESR-0057), recovery (this session's WP3), and a real UXP surface (this session's WP6) - no longer RPC-only.
- The Agent Framework now has three specialist agents (`gia-observability`, `gia-engineering`, `home-assistant-state-query`), all `ROUTINE_INTERACTION`-classified; `sentinel/policy.py`'s `LOCAL_AGENT_ACTION` boundary remains completely untouched, confirmed by a zero-line diff across the full session.
- The Playwright E2E harness's parallel-worker race is genuinely fixed, not papered over - the first-tried literal fix (production build/preview) was found to conflict with an existing, intentional test design and was reverted rather than accepted for its surface-level success.
- A Programme Sponsor-requested GitHub Copilot CLI gap analysis, deliberately excluding this session's own work for an unbiased read, surfaced six real findings (two P0, three P1, one P2) - one (Playwright reliability) and one (Memory Management UXP) resolved this same session; the other four (release-gate contradiction, profile-based enforcement, packaged-app CI proof, capability-tracking cadence) registered as Candidate Backlog.
- **Self-caught process error, disclosed rather than hidden**: `Edit`'s `replace_all: true` on a bare version-number string corrupted an unrelated historical version-history row twice this session (EBR-0001, at both WP6 and WP7) - each caught immediately via `git diff` and fixed before proceeding, never reaching a commit. The recurrence (a mistake this project's own history had already named once before) is recorded here as a standing discipline gap, not resolved by this session's fixes alone.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no `LOCAL_AGENT_ACTION` boundary change - Track B Phase 3 (EBG-0128) remains a separate, unstarted security-and-policy programme;
- no device *control* of any kind via the Home Assistant agent - read-only state query only;
- no encryption at rest for Personal Memory backup files - disclosed open gap in BRD-0001, carried forward unchanged;
- no Session or Shared-Family Memory tier coverage, no profile-based memory/authority enforcement - EBG-0132 registered but not scoped or implemented;
- no v1.0 release-gate decision - EBG-0130's RSC-0001/LGB-0001 contradiction remains open, a Programme Sponsor judgement call not made this session;
- no native packaged-app CI integration proof - EBG-0133 registered but not built; Playwright continues to drive a mocked-IPC Vite dev server, not a bundled Tauri binary.

---

# 9. Verification

Repository validation performed across ESR-0058's Work Packages and at WP7/WP8:

- Git working tree was clean throughout; the session's content (`c8999c8..HEAD`, 12 commits including WP7's own and this baseline's closure) pushed to `origin/main`.
- 587 Python tests passing plus 1 correctly-skipped test by session close (up from 561 at RBL-0037's acceptance).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count moved 332→333 across the session (net +1, a pre-existing false-positive-class cross-reference warning unrelated to this session's own files).
- `npx playwright test`: 23/23 passing (up from 18 at RBL-0037), confirmed clean across multiple consecutive runs at default parallelism - the specific property EBG-0129 existed to restore.
- `cargo build`/`test`/`clippy --all-targets -- -D warnings`/`fmt --check` (matching CI exactly): all clean.
- **Genuine GitHub Copilot CLI design and post-commit review obtained for every Work Package WP2 through WP6**, plus a genuine session-wide review at WP7 - the first ESR since EE-0001's Section 7 appointment (10 July 2026) to both lose and then fully restore independent-AI-review coverage within the same session.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`submit-response`), including a genuine drift-refusal-and-retry episode at WP6's closure record (a fresh Sponsor decision required at the moved HEAD).
- Session-wide WP7 (genuine GitHub Copilot CLI review): Conditional Pass, one real finding (EBG-0126's register row) fixed before closure.
- The Programme Sponsor's own WP8 determination: establish a new baseline rather than retain RBL-0037 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0037_REPOSITORY_BASELINE|RBL-0037]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. **EBG-0130 (v1.0 Release Gate Contradiction)** - the highest-priority open item this baseline carries forward: RSC-0001 and LGB-0001 give contradictory v1.0 readiness signals, and this is a Programme Sponsor judgement call, not a build item.
5. EBG-0132 (Profile-Based Memory and Authority Enforcement) - Candidate Backlog, no implementation authorised yet.
6. EBG-0133 (Native Packaged-App CI Integration Proof) - Candidate Backlog, no implementation authorised yet.
7. EBG-0134 (Capability-Tracking Refresh Cadence) - a documentation-debt item, not yet actioned; PCB-0001/Capability Matrix content refresh for this session's two new capabilities remains outstanding.
8. EBG-0128 (Local Agent Action Faculty) - remains Candidate Backlog, `LOCAL_AGENT_ACTION` still unconditional `DENY`.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0037_REPOSITORY_BASELINE|RBL-0037]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0058_ENGINEERING_SESSION_REPORT|ESR-0058]] | Session this baseline is drawn from. |
| [[EIP-ESR0058-001_ENGINEERING_REVIEWER_REAPPOINTMENT|EIP-ESR0058-001]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[EIP-ESR0058-002_BRD-0001_RECOVERY_IMPLEMENTATION|EIP-ESR0058-002]] | Approved Engineering Implementation Package WP3's deliverables were built against. |
| [[EIP-ESR0058-003_HOME_ASSISTANT_STATE_QUERY_AGENT|EIP-ESR0058-003]] | Approved Engineering Implementation Package WP4's deliverables were built against. |
| [[EIP-ESR0058-004_PLAYWRIGHT_E2E_RELIABILITY|EIP-ESR0058-004]] | Approved Engineering Implementation Package WP5's deliverables were built against. |
| [[EIP-ESR0058-005_MEMORY_MANAGEMENT_UXP_SURFACE|EIP-ESR0058-005]] | Approved Engineering Implementation Package WP6's deliverables were built against. |
| [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] | Sections 8A/8B added this session, completing the backup/recovery/UXP lifecycle. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0126, EBG-0023, EBG-0127, EBG-0129, EBG-0131 closed Complete; EBG-0130, EBG-0132, EBG-0133, EBG-0134 registered. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync via EBG-0134. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0037. The Programme Sponsor's explicit WP8 decision to cut a new baseline agrees with both the Engineering Implementer's and the newly-restored Engineering Reviewer's own advisory: a permanent Engineering Reviewer succession (GitHub Copilot CLI, verified genuinely working throughout this session including a full session-wide review), two real product capabilities (Home Assistant read-only agent; Memory Management backup/restore UXP), and a genuine test-infrastructure reliability fix (Playwright's parallel-worker race root-caused and fixed) together warrant a new baseline, matching the Establish threshold applied at RBL-0035 through RBL-0037. |
