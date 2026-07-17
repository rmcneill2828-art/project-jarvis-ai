# ESR-0025 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0025 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0025 |
| Date Opened | 17 July 2026 |
| Date Closed | 17 July 2026 |
| Closure Status | Closed - WP1 complete, session-wide WP6 Pass, WP7 RBL-0015 retained. EIP-ESR0025-002 (Ollama Local Fallback Provider) remains Draft, carried forward unimplemented to a future session. |

---

# 2. Purpose

This report records the opening and execution of ESR-0025, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

---

# 3. Scope

ESR-0025 opened following [[ESR-0024_ENGINEERING_SESSION_REPORT|ESR-0024]]'s closure, resolving a JRM-0001-flagged overlap between EBG-0060 and EBG-0057 before implementing the AIEMS Exchange Bridge (WP1). Once WP1 landed and was hardened across three post-implementation Engineering Reviewer rounds, the Programme Sponsor directed a series of further items: a live investigation into using Ollama as PEM-001's already-decided local fallback provider (producing a draft EIP, EIP-ESR0025-002, not yet implemented), a double-click desktop launcher for the JARVIS/Guardian Tauri shell, and backlog registration of two Sponsor-raised concerns (Sentinel network-exposure hardening, UXP placeholder-row reconciliation). The session closed with its session-wide WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance, both against the full session diff.

---

# 4. Engineering Authority

ESR-0025 opening was authorised by Programme Sponsor instruction on 17 July 2026, following repository synchronisation confirming [[ESR-0024_ENGINEERING_SESSION_REPORT|ESR-0024]] was formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

The session objective at opening was **EBG-0057** (Claude<->Codex Engineering Bridge), following the Programme Sponsor's post-ESR-0024 decision to run it as a separate AIEMS/engineering-tooling workstream outside JRM-0001's JARVIS/Guardian product tracks - the session's first delivery from JRM-0001 Track A rather than Track B. Before implementation, a flagged overlap with EBG-0060 (Direct Code Execution / Repository Execution Agent) was resolved: EBG-0060's DCE component marked Superseded (citing ESR-0023's write-boundary incidents as direct empirical evidence against single-AI direct execution), its REA component folded into EBG-0057's own future-phase scope.

No further formal objective was set at opening. Once WP1 closed, the Programme Sponsor directed several further activities conversationally rather than through a second named Work Package: a live Ollama investigation (producing a draft EIP, not yet actioned), a desktop launcher build, and two backlog registrations. These are recorded in Section 9 rather than as a separate numbered WP, since none followed the propose-review-approve-implement lifecycle a WP implies - the launcher was built and verified directly at the Programme Sponsor's request, and the backlog items explicitly authorise no implementation.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation | Complete - see Section 7 |
| WP1 | Resolved the EBG-0060/EBG-0057 overlap; implemented the Claude<->Codex Engineering Bridge (EBG-0057) | Complete - Section 8 |
| Session Activities | Ollama local-fallback investigation (EIP-ESR0025-002 drafted, not implemented), JARVIS/Guardian desktop launcher (EBG-0078, Completed), two backlog registrations (EBG-0076, EBG-0077) | Recorded - Section 9 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass / Accept, RBL-0015 retained - Section 10 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] reviewed at session open.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] reviewed: confirmed ESR-0024 closed, [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted baseline, permanent Claude Implementer / Codex (ChatGPT) Reviewer appointment in force.
- Repository state verified directly: `git status` clean, `main` at `a06afca` (ESR-0024's closing commit).

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0025 (this report, authored at closure per the practice established at ESR-0022/ESR-0023/ESR-0024).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (retained throughout, confirmed again at this session's own WP7).
- Session objective: EBG-0057, following the Programme Sponsor's post-ESR-0024 decision - see Section 5.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction and subsequent objective confirmation.

---

# 8. WP1 - EBG-0060/EBG-0057 Overlap Resolution and Claude<->Codex Engineering Bridge

**Overlap resolution (`fdb82f7`).** EBG-0060's Direct Code Execution (DCE) component was marked Superseded, citing ESR-0023's write-boundary incidents as direct empirical evidence against single-AI direct execution without a review gate. Its Repository Execution Agent (REA) component was folded into EBG-0057's own future-phase scope rather than retained as a competing backlog item. EBG-0057 was elevated to Near-term in JRM-0001.

**Bridge implementation (`128fdfb`).** A Working Report / Engineering Implementation Package ([[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]]) was drafted, reviewed by Codex, and hardened across three post-implementation review rounds before this report's closure:

- **v0.1 to v0.2 (pre-implementation, two findings):** `sponsor-decision` had no canonical storage location (resolved: transcript-only, no separate inbox/outbox); repository drift since Sponsor approval was only warned about (resolved: `submit-response` hard-refuses on any mismatch against the approving decision's recorded state).
- **First post-implementation review (High + Medium):** unsanitised `session`/`work_package` identifiers could escape `.aiems-exchange/` via path-traversal (fixed via `_validate_identifier` inside `_wp_key()`); `submit-to-review`/`submit-response` did not check `pytest`/`validate_repository.py` exit codes, so a failing run could look successful (fixed: `submit-response` hard-refuses on validation failure, `submit-to-review` stays non-blocking but its evidence carries an unmissable `VALIDATION: PASSED`/`FAILED` marker).
- **Second post-implementation review (Medium, TOCTOU):** `submit-response`'s authorisation/drift checks, preflight and evidence capture all ran *before* the Work Package lock was acquired, only locking for the final write - a concurrent `sponsor-decision` could land in that window and the response would still proceed on stale approval. Fixed by moving the entire read-check-evidence-write sequence inside the lock, proven by a test injecting a concurrent decision during evidence capture.

`scripts/aiems_bridge.py` implements all five commands (`init`, `submit-to-review`, `return-findings`, `sponsor-decision`, `submit-response`) with role-locking enforced as a real code gate rather than only a documented convention: `return-findings` has no code path capable of writing outside `.aiems-exchange/` (no file-path argument exists to exploit it), and `submit-response` refuses before any file write unless the transcript's most recent `sponsor-decision` approves and the current repository HEAD matches the exact state that decision approved. 25 new tests (237 total, was 212).

**Disclosed limitation.** `scripts/aiems_bridge.py submit-to-review`'s preflight hard-requires both `claude` and `codex` CLI binaries on `PATH`; neither exists on the Engineering Implementer's machine (confirmed via `which`). The tool's design assumed a local-CLI-based exchange that does not match this project's actual Codex-review pattern (manual relay between chat sessions). A live dry run and smoke check confirmed the authorisation-refusal, approval-success, preflight-refusal and path-traversal-refusal paths for real, but the full successful cycle has not been exercised end-to-end in this environment - disclosed as an honest gap, not asserted as tested. Not actioned this session; a candidate for future backlog registration.

**Review**: Engineering Reviewer (Codex) approved v1.0 initially, then reviewed each of the two further post-implementation diffs with no unresolved findings after v1.1 and v1.2. Programme Sponsor approved implementation throughout. EBG-0057 closed Complete in EBR-0001.

- Commit SHAs: `fdb82f7`, `128fdfb`
- `python -m pytest`: 237 passed (was 212). `python scripts/validate_repository.py`: 0 errors, 104 pre-existing warnings.

---

# 9. Session Activities Beyond WP1

Following WP1's closure, the Programme Sponsor directed several further items conversationally (`b803996`), none following the propose-review-approve-implement lifecycle a formal Work Package implies:

**Ollama local fallback investigation.** The Programme Sponsor asked whether Ollama was intended for local conversation with API providers reserved for deeper reasoning; conversational discussion clarified the actual intended role per PEM-001's Decision Outcome (ESR-0015 WP3a) is resilience fallback, not complexity-based routing (the latter remains EBG-0045/EBG-0049's separate, deferred territory). A live investigation confirmed Ollama installed and running on the Programme Sponsor's machine, models correctly migrated to `I:\Ollama Models`, and the real `/api/generate` response shape (including a `thinking` field on reasoning-capable models that must not leak into visible content). This produced **EBG-0075** (Approved Backlog) and a draft **[[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]]** (v0.1, Draft) - scoped in full but **not implemented, not fully technically reviewed, and not approved**. It remains open for a future session.

A related performance question was also resolved during this investigation: Ollama's cold-start latency (~64s) was confirmed disk-bound (a raw sequential read benchmark against `I:\`'s HDD measured 79.8 MB/s, mathematically explaining the observed `load_duration` almost exactly), while warm generation was confirmed genuinely GPU-accelerated (RTX 4060 utilisation rising to 33-38%, ~6.7GB VRAM, 39 tokens/sec) - correcting the Engineering Implementer's own earlier incorrect CPU-bound hypothesis, disclosed directly to the Programme Sponsor at the time.

**JARVIS/Guardian desktop launcher.** At the Programme Sponsor's request for a way to start JARVIS/Guardian without the command line, `scripts/start-jarvis.bat` was built and verified live end-to-end (window opened, chat round-trip confirmed) - a dev-mode double-click launcher running the same `npm run tauri dev` path this session's earlier work validated. A copy was placed on the Programme Sponsor's desktop. Recorded as **EBG-0078** (Completed), mirroring the EBG-0054 precedent of documenting already-delivered dev tooling rather than folding it into an unrelated EIP. The Programme Sponsor separately confirmed a real installer-style packaged `.exe` is out of scope until closer to a live/update-only phase; that gap remains tracked under EBG-0050.

**Backlog registrations.** Two further Sponsor-raised concerns were registered without authorising implementation: **EBG-0076** (Sentinel Network Exposure Security Hardening, High priority - no authentication, rate limiting or TLS exists anywhere in Sentinel or the RPC layer today, and no network-facing interface exists at all; the Programme Sponsor directed this be addressed "sooner rather than later"), and **EBG-0077** (UXP Static Placeholder Row Reconciliation Against Reference Mock-up, Medium priority - extending EBG-0073's explicitly-left-open question, tied to preparing the UXP ahead of a planned future Guardian self-awareness/introspection capability).

**Engineering Reviewer findings on this batch, both addressed:** a scope-leak question on whether `scripts/start-jarvis.bat` needed EIP-ESR0025-002 authorisation (resolved: unrelated to the Ollama EIP, addressed separately via EBG-0078); and a malformed EBR-0001 version-history row (two unrelated entries had been merged into one table row with a stray `|`, splitting into proper rows).

- Commit SHA: `b803996`
- `python -m pytest`: 237 passed. `python scripts/validate_repository.py`: 0 errors, 104 pre-existing warnings.

---

# 10. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0025_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0025 WP6 Independent Repository Verification handover]] was prepared covering the full session diff (`a06afca`..`b803996`), widened from an initial draft that covered only WP1's bridge diff before the session's further work existed.

**Session-wide WP6 (Independent Repository Verification)**: the Engineering Reviewer's own local sandbox/shell failed twice during this step; rather than claim a verification it could not perform, Codex disclosed the failure and, once handed the full commit diff directly (shell-free), independently confirmed HEAD/`origin/main` both at `b803996`, the 10-file diff scope, the fixed EBR-0001 version-history row, and EIP-ESR0025-002's Draft/unimplemented characterisation. One wording finding was raised (the handover overstated the working tree as unconditionally clean without qualifying its own untracked status) and addressed. **Pass.**

**Session-wide WP7 (Repository Baseline Acceptance): [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline.** Both independent views converged: the Engineering Reviewer's and the Engineering Implementer's own, each reasoning that this session's diff (bridge tooling, backlog registration, an unimplemented EIP draft) does not touch `jarvis/`, `sentinel/` or `src/` and so does not change the product runtime baseline. Programme Sponsor's own determination, informed by both: **Accept - retain RBL-0015**.

- Commit SHA: `b5213b7`
- `python -m pytest`: 237 passed. `python scripts/validate_repository.py`: 0 errors, 104 pre-existing warnings.

---

# 11. Carried Forward, Not Actioned This Session

- **EIP-ESR0025-002 (Ollama Local Fallback Provider)** remains Draft v0.1. Its technical scope has not yet received a full Engineering Reviewer pass (only two incidental governance findings on adjacent material were raised and addressed) and it is not Programme Sponsor-approved. No implementation has occurred. A clear candidate objective for a future session.
- **EBG-0076** (Sentinel network exposure hardening) and **EBG-0077** (UXP placeholder-row reconciliation) are Approved Backlog only - no implementation authorised.
- The `aiems_bridge.py` preflight's hard dependency on local `claude`/`codex` CLI binaries (Section 8) is disclosed but not yet itself backlogged as a fix - a candidate for a future session if the Programme Sponsor wants the bridge genuinely usable end-to-end rather than falling back to manual relay.

---

# 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0057 closed Complete; EBG-0075, EBG-0076, EBG-0077 added as Approved Backlog; EBG-0078 added Completed. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | EBG-0057 annotated resolved (Track A). |
| [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] | Approved and implemented package for WP1, v1.2. |
| [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] | Draft v0.1, carried forward unimplemented - see Section 11. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0025_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0025 WP6 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.5, Section 10. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Retained as the current accepted repository baseline at Section 10. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Decision Outcome grounding the Ollama investigation and EIP-ESR0025-002. |

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per the practice established at ESR-0022/ESR-0023/ESR-0024. Records WP0-WP1, session activities beyond WP1 (Ollama investigation/EIP-ESR0025-002 draft, desktop launcher, two backlog registrations), the session-wide WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (Accept, RBL-0015 retained). Status Open to Closed. |
