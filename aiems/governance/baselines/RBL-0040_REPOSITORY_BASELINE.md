# RBL-0040 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0040 |
| Title | ESR-0060 Repository Baseline (Retrospective Review Discharged; Backend Process-Tree Termination) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0060_ENGINEERING_SESSION_REPORT|ESR-0060]] |
| Previous Baseline | [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 1 October 2026 |
| HEAD at baseline creation | `679c7dd` |

---

# 2. Purpose

RBL-0040 records the repository baseline accepted by the Programme Sponsor at ESR-0060 WP4, superseding [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]].

ESR-0060 ran **review-first**, by Programme Sponsor decision. RBL-0039 had been established with eleven Work Packages (ESR-0059 WP4 to WP14) only self-verified, because GitHub Copilot CLI's monthly quota had run out. Its first act, once the quota reset on 1 October 2026, was the owed independent review (EBG-0153). It then fixed the two real defects that review found, and delivered the one open runtime-safety item carried from ESR-0059: process-tree termination for the packaged backend. Every step of the session was genuinely reviewed by Copilot CLI.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - pointer-synced to this baseline; no product-capability content change this session (the work was correctness and runtime safety). |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0060 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation. Neither independent reviewer was available at opening (Copilot quota exhausted; Codex returning `402 deactivated_workspace`), so the Programme Sponsor chose review-first: no implementation before the retrospective review. WP0 verified EIP-ESR0059-001 Section 4G live against the real packaged sidecar and drafted WP2's design; EBG-0154 registered.

**WP1 - EBG-0153 Retrospective Engineering Review**: three genuine scoped Copilot CLI reviews of the committed code `f33286a^..61f1712`, one per batch - WP4-WP6 Conditional Pass, WP7-WP10 Pass, WP11-WP14 Pass. WP5's GIL-reliant thread safety was confirmed for the paths it covers. Findings registered as EBG-0155 (High), EBG-0156 (Medium) and EBG-0157 (Low cluster).

**WP1b - Provider-Selection and Deadline-Health Fixes** ([[EIP-ESR0060-001_PROVIDER_SELECTION_AND_DEADLINE_HEALTH_FIXES|EIP-ESR0060-001]]): added by Programme Sponsor decision. `JARVIS_PRIMARY_PROVIDER` is normalised like the secondary, a blank value means the default (a second defect found while reading the code), and unknown names are warned about (EBG-0155). A deadline expiring inside a provider call is no longer counted as a provider fault (EBG-0156).

**WP2 - Backend Process-Tree Termination** ([[EIP-ESR0060-002_BACKEND_PROCESS_TREE_TERMINATION|EIP-ESR0060-002]], EBG-0154): a Windows job object per backend with `KILL_ON_JOB_CLOSE`, graceful stdin close, a 3-second grace, then forced tree termination, outside the shared-state lock. Design reviewed in three rounds and implementation in two. Implementation found two gaps all design reviews missed: a fourth `windows-sys` feature, and that CI's `rust` job runs on Linux. A `rust-windows` CI job was added by Programme Sponsor decision.

**WP3 - Session-wide verification**: genuine GitHub Copilot CLI review of `cd8c06e..679c7dd` - Pass, plus the Engineering Implementer's fresh re-run of every check (Section 9).

**The Programme Sponsor's determination** (WP4): **establish a new baseline**.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/interfaces/stdio_rpc.py` | Primary-provider name normalised; blank means default; unknown provider names logged as a warning. |
| `sentinel/providers.py`, `sentinel/orchestrator.py` | `DeadlineExceededError`; deadline expiry inside a provider call leaves health and circuit untouched. |
| `src-tauri/src/lib.rs` | `ProcessGuard` (job object plus held process handle), `BackendHandle::shutdown()` replacing `kill()`, bounded reaping, teardown and app exit outside the lock, non-Windows stand-ins; 19 tests plus an ignored live harness. |
| `src-tauri/Cargo.toml` | Direct `windows-sys` 0.60 dependency (already compiled in through Tauri), approved by the Programme Sponsor. |
| `.github/workflows/ci.yml` | `rust-windows` job (`cargo test` on pushes to `main` and on demand); `--tests` on the Linux clippy step; `workflow_dispatch` trigger. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0154 to EBG-0158 registered; EBG-0153 to EBG-0156 closed Completed. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is pointer-synced to RBL-0040. Its capability content is unchanged: this session corrected behaviour (provider selection, provider health, backend shutdown) rather than adding or removing product capabilities.

---

# 7. Architecture Outcomes

- The host now owns the backend's whole process tree on Windows. A busy, hung or orphaned backend can no longer outlive teardown, app exit or a killed host: a normal close stays graceful, and everything else is bounded at about 3 seconds.
- Provider health reflects real faults only: running out of turn time no longer opens a provider's circuit.
- A provider-configuration typo is visible in the backend log instead of silently routing everything to local Ollama.
- The Windows-only runtime code is tested in CI on Windows, not only compiled out on Linux.

---

# 8. Scope Boundaries

- no `LOCAL_AGENT_ACTION` boundary change - `sentinel/policy.py` untouched all session;
- no change to the Python backend's drain-on-EOF contract (ESR-0059 WP5) - the host bounds how long it waits instead;
- no Unix process-group handling - no non-Windows build is shipped;
- the spawn-to-adopt gap (EIP-ESR0060-002 Section 4G) recorded, not closed - suspended spawning considered and deferred;
- no credentialed authentication and no code signing (EBG-0146, Deferred) - unchanged from RBL-0039.

---

# 9. Verification

- 6 session commits (`cd8c06e..679c7dd`, 14 files), every one gated through the real Sponsor Approval Service via `submit-response`, each against an approval recorded at its parent commit.
- CI on `main`: every session run green on all jobs, including the new `rust-windows` job on both of its runs - all seven Windows job-object tests passing on a GitHub-hosted runner.
- pytest 759 passed/1 skipped (751 at RBL-0039), with the full suite writing no files into a fake home directory; Playwright 26/26; cargo test 19 passed/1 ignored (8 at RBL-0039), clippy `--tests` and fmt clean on Windows and Linux; ruff clean; validator 0 errors/333 warnings, unchanged; `sync_product_version.py --check` agrees; `npm run build` clean; pip-audit clean in a fresh virtual environment.
- Engineering Reviewer coverage: genuine GitHub Copilot CLI review at every step - retrospective (3 batches), design, implementation, CI change, post-commit and session-wide. In two passes (WP2 post-commit, WP3 session-wide) the reviewer's tool permissions refused its validation commands, so the Engineering Implementer re-ran them; disclosed in ESR-0060.
- Live checks on a freshly rebuilt packaged build: normal close graceful in 826 ms; a busy packaged backend's whole tree ended at 3.0 s; a force-killed host's tree gone in 96 ms.

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. **EBG-0158 - before merging Dependabot's `tauri-plugin-shell` 2.3.5 to 2.4.0 bump** (and its `tauri` 2.12.0 bump): re-verify that dropping `CommandChild` still closes the backend's stdin, which WP2's graceful path relies on. A regression would not leak processes (the forced path still bounds shutdown at about 3 seconds), but every close would become forced.
5. **EBG-0157** - the low-severity hardening cluster from the retrospective review and WP2, including the deadline-capped network timeout design (item 6), the spawn-to-attach PID-reuse race and the manual "Not Responding" check during exit.
6. **Accepted risk, by Programme Sponsor decision**: the `rust-windows` CI job does not run on pull requests, so a Windows regression in the process-tree code surfaces only after merging to `main`.
7. **Single-reviewer risk**: Codex CLI still returns `402 deactivated_workspace`, so GitHub Copilot CLI's monthly quota remains the only independent review path.
8. EBG-0149, EBG-0150, EBG-0151 (Low), EBG-0130 (v1.0 release-gate contradiction), EBG-0110, EBG-0050's residual and EBG-0128 carried forward unchanged.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0060_ENGINEERING_SESSION_REPORT|ESR-0060]] | Session this baseline is drawn from. |
| [[EIP-ESR0060-001_PROVIDER_SELECTION_AND_DEADLINE_HEALTH_FIXES|EIP-ESR0060-001]] | WP1b implementation package. |
| [[EIP-ESR0060-002_BACKEND_PROCESS_TREE_TERMINATION|EIP-ESR0060-002]] | WP2 implementation package. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0154 to EBG-0158 registered; the session's closures recorded. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline, pointer-synced this session. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 October 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0039, on the Programme Sponsor's direction to close ESR-0060 with a new baseline: the retrospective independent review RBL-0039 owed was discharged, the two real defects it found were fixed, and the backend process tree is now bounded on every teardown path - every step genuinely reviewed. |
