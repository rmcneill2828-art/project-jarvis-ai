# ESR-0060 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0060 |
| Title | Engineering Session Report |
| Version | 0.2 |
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

**WP1 - EBG-0153 Retrospective Engineering Review (Not started):** blocked on the Copilot CLI quota reset (1 October 2026). Scope per EBG-0153: genuine scoped Copilot CLI review of ESR-0059 WP4 (`f33286a`) to WP14 (`61f1712`), with WP5's reliance on CPython's GIL for thread safety called out as the point most worth an independent look, and the case-sensitivity mismatch between `JARVIS_PRIMARY_PROVIDER` and `JARVIS_SECONDARY_PROVIDER`.

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

Review-first: discharge EBG-0153's retrospective independent review of ESR-0059 WP4 to WP14 as soon as GitHub Copilot CLI's quota resets, then deliver backend process-tree termination (EBG-0154) through the standing design-review, Programme Sponsor approval, `submit-response` and post-commit-review template, with a genuine independent reviewer at every step.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | EBG-0153 retrospective Copilot CLI review of ESR-0059 WP4 to WP14 | Not started - blocked on Copilot quota reset, 1 October 2026 |
| WP2 | Backend process-tree termination (EBG-0154) | Drafted (EIP-ESR0060-002 v0.2, design only; dependency approved) - awaiting design review after WP1 |
| Candidate | EBG-0149, EBG-0150, EBG-0151 (Low); EBG-0130 (Programme Sponsor judgement) | Not started |

---

# 7. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 30 September 2026 | Claude Engineering Implementer | Programme Sponsor approved the new direct windows-sys dependency for WP2 (EIP-ESR0060-002 Section 4F), via direct chat instruction ("Approved"). Dependency only; implementation still waits for the design review. EIP-ESR0060-002 synced to v0.2. |
| 0.1 | 30 September 2026 | Claude Engineering Implementer | ESR-0060 opened. WP0A/WP0B complete. Neither independent reviewer available (Copilot CLI quota exhausted until 1 October 2026; Codex CLI workspace deactivated). Objective set by Programme Sponsor decision: review-first. WP2 design drafted per EIP-ESR0060-002 v0.1 after verifying EIP-ESR0059-001 Section 4G live; EBG-0154 registered. No code changed. |
