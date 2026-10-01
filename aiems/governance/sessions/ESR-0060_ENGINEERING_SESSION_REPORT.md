# ESR-0060 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0060 |
| Title | Engineering Session Report |
| Version | 0.3 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0060 |
| Date Opened | 30 September 2026 |
| Date Closed | - |
| Closure Status | Open |

---

# 2. Purpose

This report records the opening of ESR-0060, at the Programme Sponsor's direct request ("start next ESR"), following ESR-0059's formal closure and the establishment of [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]].

The session runs **review-first**, by Programme Sponsor decision: no independent Engineering Reviewer was available at opening (Section 3, WP0A), so the session's first Work Package is the retrospective GitHub Copilot CLI review owed under EBG-0153, run once Copilot's monthly quota resets on 1 October 2026, and no implementation is made until that review has run. Until then, work is limited to session opening and design drafting.

WP0A/WP0B session initialisation followed PBK-0001 and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

**WP0A - Repository Synchronisation (Complete):** Working tree clean at session open. HEAD `cd8c06e` (ESR-0059 WP16), in sync with `origin/main`; that commit's CI run (36601728449) green on all jobs. Repository baseline confirmed as [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] (accepted ESR-0059 WP16). Pre-commit governance hook confirmed active (`core.hooksPath` = `scripts/hooks`). Full Python suite confirmed green at open: 751 passed, 1 skipped. `scripts/session_launcher.py` run for WP0B: PST-0001's Next Work Package Candidate lists EBG-0153, process-tree termination for the packaged backend (EIP-ESR0059-001 Section 4G), EBG-0149 to EBG-0151, and EBG-0130.

**Reviewer availability probed at open - neither independent reviewer is available:**

* **GitHub Copilot CLI** (permanent Engineering Reviewer since ESR-0058): `copilot -p "Reply with the single word OK." -s --deny-tool='write'` still returns "You have exceeded your monthly quota". The Programme Sponsor confirmed the quota resets on 1 October 2026 (the 1st of each month).
* **Codex CLI** (considered as a same-day substitute): `codex exec -s read-only` fails with `402 Payment Required`, auth error code `deactivated_workspace` - the ChatGPT workspace behind it is no longer active. This is new: Codex was last used successfully at ESR-0047. Out-of-repository account state; not investigated further without Programme Sponsor direction. It means EBG-0153's single-reviewer risk currently has no fallback at all.

**WP0B - Engineering Session Initialisation (Complete):** ESR-0059 confirmed formally Closed. ESR-0060 opened as the next session identifier. `~/.current_session` updated to `ESR-0060`. Objective set by Programme Sponsor decision among presented options - **"Open now, review-first"**: WP1 is the EBG-0153 retrospective Copilot review of ESR-0059 WP4 to WP14 once the quota resets; WP2 is process-tree termination for the packaged backend, design-reviewed by Copilot before any implementation. Today's work is limited to opening the session and drafting WP2's design.

**WP1 - EBG-0153 Retrospective Engineering Review (Complete):** GitHub Copilot CLI quota confirmed reset on 1 October 2026 (one-line probe returned "OK"). Routed through the real bridge (`init`/`submit-to-review` for `ESR-0060`/`WP1`, 46-file scope = the committed code diff `f33286a^..61f1712`, governance documents excluded). Review-only: no code change proposed. Run as three genuine scoped Copilot CLI invocations (`--allow-tool='shell(git:*)' --allow-tool='shell(python:*)' --deny-tool='write'`), one per batch, each briefed to test every ESR-0059 self-review claim against the code rather than accept it, and each recording its own `return-findings` entry - all three independently verified against the transcript (`sender: reviewer`, `repository_ref: 5fbfff9...`).

* **Batch A, WP4-WP6 - Conditional Pass.** WP5's GIL-reliant thread-safety claim **holds** for the paths it covers: every stdout write (main thread, slow lane, heartbeat) is under one `_write_lock`, so JSON lines cannot interleave; per-profile Cognitive Cores are touched only by the single slow-lane worker; health-map reads racing worker writes are benign one-step-stale reads. Retry backoff never sleeps past the deadline; a non-ALLOW Sentinel decision raises before any provider is touched; transient-status classification matches across all three adapters. **Finding 1 (High), reproduced live by the reviewer**: `JARVIS_PRIMARY_PROVIDER` is matched case-sensitively - `Gemini` with a valid key registers only `ollama`, silently, with no log line. Registered EBG-0155. **Finding 2 (Medium), reproduced by the reviewer and confirmed by the Engineering Implementer in code**: a deadline that expires inside a provider's own `remaining_timeout()` raises a plain `RuntimeError`, which `execute()` treats as a genuine fault - the provider is marked DEGRADED and its circuit opened for 30 seconds, contrary to EIP-ESR0059-005/006. Registered EBG-0156. Findings 3-5 (concurrent SQLite access with no `busy_timeout`; an unguarded fast-lane write failure; no automated real-thread test) registered in EBG-0157. On finding 3 the Engineering Implementer disagrees with the reviewer's Medium rating: memory writes are short single transactions and Python's 5-second default lock wait applies, so it is hardening, not a live defect.
* **Batch B, WP7-WP10 - Pass.** Strict user/assistant alternation for OpenAI and Gemini; persona-only system prompts; every text-accepting RPC limited before any runtime call, with the UXP limit matching; no conversation or memory content on any audit or log path (every `AuditEvent` traced); rotation under one lock; nothing logged to stdout; a revoked memory is absent from the very next turn. Re-ran the full suite: 751 passed, 1 skipped; ruff clean; validator 0 errors. Two Low findings (raw `str(exc)` in RPC error replies and in persisted provider-failure audit reasons - safe today only by adapter discipline) registered in EBG-0157.
* **Batch C, WP11-WP14 - Pass.** Exactly three subprocess call sites, all list-form with closed stdin; the frozen executable is never re-invoked as an interpreter; a newer-than-code database is refused untouched and five concurrent first-opens migrate correctly (both verified with throwaway scripts); every memory handler takes the profile from the identity service, never from parameters; another profile's memory is indistinguishable from a missing one. One Low finding (the 100 pending-proposal cap is shared across profiles) registered in EBG-0157.

EBG-0153 closed Completed. **Programme Sponsor decision (option (a), direct chat instruction)**: close WP1, and fix the High finding as a separate Work Package before WP2. Read as taking the recommendation in full, so WP1b covers EBG-0156 as well as EBG-0155. This adds a Work Package to the session plan, recorded as an explicit Programme Sponsor scope change. Single-reviewer risk unchanged: Codex remains unavailable.

**WP1b - Provider-Selection and Deadline-Health Fixes (Not started):** EBG-0155 and EBG-0156, through the standing design-review, Programme Sponsor approval, `submit-response` and post-commit-review template.

**WP2 - Backend Process-Tree Termination (Drafted - design only):** [[EIP-ESR0060-002_BACKEND_PROCESS_TREE_TERMINATION|EIP-ESR0060-002]] drafted (v0.1). No code changed. EBG-0154 registered in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (Candidate Backlog, Medium). **Programme Sponsor approved the new direct `windows-sys` dependency** (EIP Section 4F) via direct chat instruction ("Approved"). This approves the dependency only; implementation still waits for the design review, and EIP-ESR0060-002 is synced to v0.2.

**Real finding made while investigating, before drafting** - EIP-ESR0059-001 Section 4G recorded that terminating the backend's direct child might not reach the real interpreter, "not verified". Verified on this machine today against the real packaged sidecar (`src-tauri/binaries/jarvis-backend-x86_64-pc-windows-msvc.exe`, built 29 September 2026 at ESR-0059 WP11):

* The onefile sidecar runs as a bootloader plus a child process. Killing only the bootloader, with stdin held open, **leaves the child - the real backend - running**.
* But `CommandChild::kill()` consumes the handle, which also drops its stdin writer. Killing the bootloader *and* closing stdin ended an idle backend in 58 ms; closing stdin alone ended bootloader and child cleanly in 637 ms ("Guardian runtime foundation stopped" logged).
* The dev path (`python` resolving to the repository's `.venv` launcher) did **not** orphan: the launcher's child ended with it.
* So the real exposure is narrower than 4G implied: `serve_forever()` deliberately drains every in-flight and queued slow request on stdin EOF (ESR-0059 WP5, "a request accepted is always answered"), each bounded by the 100-second per-turn deadline, and a fast-lane handler blocks EOF handling entirely while it runs. A backend torn down while busy - the malformed-output, connection and write-failure teardown paths, often exactly when it is misbehaving - keeps running on the same SQLite stores until that work ends, while `call_backend()` spawns a replacement beside it. A genuinely hung backend is never ended.

Recorded as EBG-0154 rather than overstated: this is not "every app close leaks a backend".

---

# 4. Engineering Authority

ESR-0060 opening was authorised by direct Programme Sponsor instruction on 30 September 2026, following ESR-0059's formal closure.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Review-first: discharge EBG-0153's retrospective independent review of ESR-0059 WP4 to WP14 as soon as GitHub Copilot CLI's quota resets, fix what it finds that matters (WP1b), then deliver backend process-tree termination (EBG-0154) through the standing design-review, Programme Sponsor approval, `submit-response` and post-commit-review template, with a genuine independent reviewer at every step.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | EBG-0153 retrospective Copilot CLI review of ESR-0059 WP4 to WP14 | Complete - A Conditional Pass, B Pass, C Pass; EBG-0155 to EBG-0157 registered |
| WP1b | Provider-selection case fix and deadline-health fix (EBG-0155, EBG-0156) | Not started - added by Programme Sponsor decision |
| WP2 | Backend process-tree termination (EBG-0154) | Drafted (EIP-ESR0060-002 v0.2, design only; dependency approved) - awaiting design review after WP1b |
| Candidate | EBG-0149, EBG-0150, EBG-0151, EBG-0157 (Low); EBG-0130 (Programme Sponsor judgement) | Not started |

---

# 7. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 1 October 2026 | Claude Engineering Implementer | WP1 complete: EBG-0153 retrospective review of ESR-0059 WP4-WP14 ran as three genuine scoped Copilot CLI reviews through the bridge (A Conditional Pass, B Pass, C Pass); WP5's GIL-reliant thread safety confirmed; EBG-0155 to EBG-0157 registered. Programme Sponsor decision (a): WP1b added before WP2 to fix EBG-0155 and EBG-0156. |
| 0.2 | 30 September 2026 | Claude Engineering Implementer | Programme Sponsor approved the new direct windows-sys dependency for WP2 (EIP-ESR0060-002 Section 4F), via direct chat instruction ("Approved"). Dependency only; implementation still waits for the design review. EIP-ESR0060-002 synced to v0.2. |
| 0.1 | 30 September 2026 | Claude Engineering Implementer | ESR-0060 opened. WP0A/WP0B complete. Neither independent reviewer available (Copilot CLI quota exhausted until 1 October 2026; Codex CLI workspace deactivated). Objective set by Programme Sponsor decision: review-first. WP2 design drafted per EIP-ESR0060-002 v0.1 after verifying EIP-ESR0059-001 Section 4G live; EBG-0154 registered. No code changed. |
