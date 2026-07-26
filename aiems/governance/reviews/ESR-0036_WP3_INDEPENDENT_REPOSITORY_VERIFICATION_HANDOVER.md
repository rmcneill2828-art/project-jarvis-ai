# ESR-0036 WP3 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0036-WP3 |
| Title | Independent Repository Verification Handover |
| Version | 0.4 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0036 (closed; session report authored incrementally across this session rather than at closure) |
| Effective Date | 26 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0036's session-wide record for WP3 Independent Repository Verification. ESR-0036 ran two Work Packages: WP1 (EBG-0108 first increment - static Guardian persona injection, a real product code change) and WP2 (consolidated documentation staleness fix - README, COC-0001, PBK-0001, PST-0001, plus retroactive creation of this session's own report). WP3 confirms the current repository state matches the claims made across both Work Packages, that Codex-caught defects were genuinely fixed rather than only claimed fixed, and that no unauthorised scope drift occurred. Submitted to Codex via the AIEMS Exchange Bridge for genuine independent verification, continuing the practice used throughout ESR-0025 through ESR-0035 (the eleventh consecutive session run this way).

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| ESR-0036 session start point | `6cf2aeb` (ESR-0035 formal closure commit) |
| ESR-0036's content endpoint (at drafting) | `26dfc55` - the last commit of WP1/WP2 content, and the range this handover's figures describe |
| This handover's own commit | Necessarily lands after `26dfc55`, since the handover is committed once drafted - the same structural point every prior session's verification handover has run into. |
| `origin/main` | Pushed at every commit this session (`d72a8ba`, `4667374`, `26dfc55`) - WP1 touched `jarvis/`, `sentinel/` and their test suites, all CI-relevant. |
| Prior accepted baseline | `RBL-0021` |

---

## 4. ESR-0036 Commits in Scope

| Commit | Summary |
|---|---|
| `d72a8ba` | WP1: EBG-0108 first increment - static Guardian persona injection, threaded through `GuardianRuntimeConfig` -> `ConversationRequest` -> `ProviderRequest.system_prompt` -> OpenAI/Gemini/Ollama adapters. Persona text formally adopted into AAM-0001 v0.4 (recovered from ESR-0004's "EKR-0001 Task 2" JARVIS character draft, Sponsor-approved verbatim). Codex design review Pass (findings folded in); post-commit review Pass. |
| `4667374` | WP2: consolidated documentation staleness fix - README.md, COC-0001, PBK-0001 corrected from stale RBL-0020/ESR-0035-open to RBL-0021/ESR-0036-open; new ESR-0036 session report created retroactively; PST-0001/REG-0001 updated. Codex design review: initial Fail (2 findings - stale README row, inconsistent wording), both fixed, fix-round Pass. |
| `26dfc55` | WP2 post-commit fix: post-commit review of `4667374` found 3 further current-facing RBL-0020 references in PST-0001 that a targeted (not whole-document) sweep had missed. Fixed as a new commit, not an amend. Codex confirmed Pass. |

---

## 5. Authorised / Explained Working Set

The full ESR-0036 session-content diff, `6cf2aeb`..`26dfc55` (20 files changed, 315 insertions, 47 deletions):

**WP1 (EBG-0108 first increment):** `jarvis/guardian/config.py` (new `DEFAULT_GUARDIAN_PERSONA` constant, `persona` field), `jarvis/guardian/runtime.py` (`converse()` threads persona), `jarvis/interfaces/conversation.py` (`ConversationRequest.persona`), `jarvis/interfaces/sentinel_conversation.py` (threads persona into `ProviderRequest.system_prompt`), `sentinel/providers.py` (`ProviderRequest.system_prompt`), `sentinel/openai_provider.py`/`gemini_provider.py`/`ollama_provider.py` (conditional system-prompt injection via each provider's native mechanism), five test files (positive coverage per layer), `AAM-0001` (new Guardian Persona section, 0.3 to 0.4), `REG-0001` (tracking rows/version).

**WP2 (documentation staleness fix):** `README.md`, `COC-0001`, `PBK-0001` (RBL-0020/ESR-0035-open corrected to RBL-0021/ESR-0036-open, Whole-Document Staleness Sweep applied); `ESR-0036_ENGINEERING_SESSION_REPORT.md` (new); `PST-0001` (Sections 3/4A updated for ESR-0036 opening and WP1 completion, plus 3 further current-facing RBL-0020 references found post-commit and fixed in `26dfc55`); `REG-0001` (tracking rows/version for PBK-0001, COC-0001, PST-0001, ESR-0036's own registration).

**REG-0001** was updated at every version bump across both Work Packages (AAM-0001 to 0.4, PBK-0001 to 1.34, COC-0001 to 1.16, PST-0001 to 2.98, ESR-0036 registered at 1.0), each an additive Version History row plus the corresponding self-row/badge update.

---

## 6. Session Observations

1. **This session's WP1 is the first EBG-0108 (Guardian Cognitive Core) implementation work of any kind** - AAM-0001 remained architecture-only since ESR-0008; this is the first code touching the actual conversation path toward that architecture, deliberately scoped to the smallest honest slice (static persona only, no memory wiring or reasoning loop).
2. **A deliberate, Sponsor-directed departure from PBK-0001's Documentation-Debt Priority discipline**: the Programme Sponsor chose EBG-0108 as WP1 ahead of the accumulated documentation staleness the discipline would normally address first, reasoning that one consolidated documentation pass at the end (capturing both the pre-existing staleness and WP1's own new state) is more efficient than two separate passes. Flagged plainly in the session report rather than silently followed as if it were the default.
3. **The persona content itself traces to a previously-dropped thread**: a Programme Sponsor recollection led to a Codex-run historical-archive search finding "EKR-0001 Task 2" (ESR-0004, `FCH-0004`) - a full character draft for JARVIS, predating the Guardian identity split, that was never promoted into a backlog item alongside its siblings. Formally adopted now into AAM-0001, closing that specific gap.
4. **Two genuine defects were caught by Codex across the two Work Packages, both fixed and independently reconfirmed**: WP1's design review found the persona should be a named constant rather than an inline literal (folded in before commit); WP2's post-commit review found a whole-document-sweep miss (3 further stale RBL-0020 references in PST-0001, fixed in a follow-on commit rather than an amend).
5. **Every Codex review this session ran in `-s read-only` sandbox mode**, per the standing EBG-0096 precedent - Codex's own sandbox cannot write the bridge's lock file directly, so findings were relayed into the bridge by the Engineering Implementer verbatim on Codex's behalf, under explicit per-instance Programme Sponsor approval for each relay act (eight such relays this session, never silently, never without approval).
6. **Programme Sponsor approval for both Work Packages was independently verified against the real Sponsor Approval Service decision database** (not merely asserted in chat) before either `submit-response` call proceeded - a deliberate practice this session, not previously called out as a distinct step in prior sessions' reports.

---

## 7. Validation Evidence

Re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 381 passed, 1 skipped (was 374 before WP1; unchanged since - WP2 touched no code) |
| `python scripts/validate_repository.py` (full, not governance-only) | 0 errors, 172 warnings, after one real fix (see below) |
| `git status` | Clean working tree at `26dfc55` plus this handover's own drafting |
| Real GitHub Actions CI | Green at every commit this session (`d72a8ba`, `4667374`, `26dfc55`, `f5acf51`) - `gh run list`/`gh run view` confirmed all 4 jobs (`python`, `rust`, `playwright`, `frontend-build`) passed for `d72a8ba`, the one commit touching CI-relevant `jarvis/`/`sentinel/` Python code. **Disclosed process gap**: this check was omitted from the session's validation evidence until the Programme Sponsor asked whether a verification step was missing, after WP4 had already closed - every check above this row was run at the time; this one was not, despite being standard practice in every prior session's own report (e.g. ESR-0035 Section 7). Checked retroactively, result clean, no corrective commit needed beyond recording it here. |

**Codex's independent WP3 verification pass caught a genuine defect this handover's own first draft did not disclose**: `ESR-0036_ENGINEERING_SESSION_REPORT.md` had been bumped to v1.1 (recording WP2's completion) but `REG-0001`'s tracking row still read 1.0 - `validate_repository.py` correctly failed with `ESR-0036 version mismatch: REG-0001=1.0 file=1.1`, contradicting this section's original 0-errors claim. Fixed by aligning REG-0001's ESR-0036 row and version/changelog (3.370 to 3.371); re-validated clean (0 errors, 172 warnings, confirmed above).

The warning count is unchanged from ESR-0035's closing figure (172) - all confirmed to be the same known false-positive class (cross-document "Section N.N" prose references), not a new class of problem; this session's version-history additions did not move the count, unlike most prior sessions, since no new "Section N.N"-style cross-reference prose was added this time.

**Second disclosed process gap, also raised by the Programme Sponsor post-closure**: PBK-0001's Repository Lifecycle names "Programme Sponsor validates the completed work" as a distinct step from Engineering Reviewer verification and automated testing - and this had not happened either. WP1's own validation to that point was entirely mocked unit tests (`ProviderRequest`/`ConversationRequest` fixtures) and Codex's diff review; nobody had actually run the live product and observed the persona reach a real conversation. Performed retroactively: Ollama (installed but not running) was started at the Programme Sponsor's direction, `qwen3.5:2b` (already pulled, matching `DEFAULT_OLLAMA_MODEL`) served as the real provider (no cloud API key configured, so Ollama - not `LocalEchoProvider` - was first in the routing order), the Guardian Desktop Platform Shell was launched via `npm run tauri dev`, and the Programme Sponsor personally sent a message and confirmed Guardian's real response reflected the new persona. One genuine, expected observation: a long pause before each response, caused by `qwen3.5` being a reasoning-capable model (an internal "thinking" pass before the visible answer, per `sentinel/ollama_provider.py`'s own docstring) running on local CPU with no GPU acceleration - unrelated to the persona-injection change itself, and within the 90-second timeout the Ollama provider configuration already accounts for. Both the dev server and Ollama were stopped afterward at the Programme Sponsor's direction (dev server via `TaskStop`, Ollama via `taskkill` on both its tray and server processes, confirmed clean via `tasklist`).

---

## 8. Scope Check

- WP1 touched `jarvis/guardian/`, `jarvis/interfaces/`, `jarvis/tests/`, `sentinel/` (provider adapters and their tests), plus `AAM-0001` and `REG-0001`. WP2 touched only governance artefacts (`README.md`, `COC-0001`, `PBK-0001`, `PST-0001`, `REG-0001`, `ESR-0036`'s own report).
- No `src/`, `src-tauri/`, `.github/workflows/`, or `jarvis/memory/` file was touched at all this session.
- No new third-party dependencies introduced.
- Both Work Packages went through the same cycle: draft, Codex read-only review (relayed via `return-findings` under explicit per-instance Sponsor approval), fix round where findings existed, a second Codex confirmation pass where a fix round occurred, Programme Sponsor approval independently verified against the real Sponsor Approval Service database, `submit-response`, then commit. WP2 additionally needed a second post-commit fix round (Section 4, `26dfc55`) after Codex's first post-commit review caught a genuine miss - disclosed here, not smoothed over.
- Working tree was clean and at `26dfc55` at the point this handover was drafted, with the handover document itself the sole new file at that moment, prior to being committed as its own follow-on commit (Section 3).

---

## 9. WP4 Baseline Recommendation

**Engineering Implementer's independent view:** establish a new baseline - do not retain `RBL-0021`.

Rationale: WP1 delivered a genuine, live-verified product code change - the first implementation work of any kind against EBG-0108 (Guardian Cognitive Core), touching `jarvis/guardian/`, `jarvis/interfaces/` and all three live Sentinel provider adapters, backed by 7 new automated tests. This is the same category of change that justified RBL-0021 itself at ESR-0035 WP5 (that session's WP3 UXP animation-scheduler change): a real, functionally-verified change to shipped conversation behaviour (every live provider call now carries a persona) and its test coverage, not pure governance churn. WP2's documentation fix, while itself requiring two follow-on commits to get fully clean, touched no product code and would not alone warrant a new baseline - but WP1 already does.

---

## 10. WP3 Verification Result

**Pass, after one fix round - no remaining blocking findings.** Codex independently confirmed `git diff --stat 6cf2aeb..26dfc55` matches Section 5's claimed 20 files/315 insertions/47 deletions exactly, and `git diff --name-status` confirms no `src/`, `src-tauri/`, `.github/workflows/`, or `jarvis/memory/` file was touched. First pass found a genuine defect: `ESR-0036_ENGINEERING_SESSION_REPORT.md` had been bumped to v1.1 (recording WP2's completion) while `REG-0001`'s tracking row still read 1.0 - `validate_repository.py` correctly failed on this, contradicting this handover's original 0-errors claim. Fixed (REG-0001 aligned to 1.1, version/changelog updated); Codex's fix-round pass independently re-ran `validate_repository.py` itself (sandbox allowed it this time) and confirmed clean (0 errors, 172 warnings). Codex's own sandbox could not run `python -m pytest` (temp-directory restriction, disclosed environmental limitation consistent with prior sessions). **Codex independently converges with Section 9: establish a new baseline** - "the session includes real product behavior changes in the Guardian conversation path and Sentinel provider request plumbing, with tests added across affected layers. That is baseline-worthy; the documentation-only WP2 would not be enough on its own."

---

## 11. WP4 Baseline Acceptance Result

**Establish a new baseline - [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] supersedes `RBL-0021`.** The Programme Sponsor determined at ESR-0036 WP4 to establish a new baseline, agreeing with both independent views in Sections 9-10: WP1's real Guardian persona-injection change (new module wiring, a live conversation-path refactor, and new automated test coverage) marks a meaningfully different repository state than pure documentation correction, warranting a new baseline for future sessions to synchronise against.

---

## 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108's first implementation increment delivered this session. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian Persona section added (0.3 to 0.4), WP1. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for every version bump this session. |
| [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] | Current accepted repository baseline, established at Section 11's WP4 acceptance, superseding RBL-0021. |
| [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] | Prior accepted repository baseline, superseded by RBL-0022. |
| [[ESR-0035_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0035 WP4 Handover]] | Precedent handover this document follows the structure of. |
| [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] | Parent session report, authored incrementally across WP1-WP2 rather than at closure. |

---

## 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.4 | 26 July 2026 | Claude Engineering Implementer | Added the missing Programme Sponsor validation record to Section 7 - a live run of the Guardian Desktop Platform Shell against a real Ollama provider, with the Programme Sponsor personally confirming Guardian's response reflected the new persona. A second distinct process gap the Programme Sponsor raised post-closure, separate from the CI gap. |
| 0.3 | 26 July 2026 | Claude Engineering Implementer | Added the missing real GitHub Actions CI verification to Section 7, after the Programme Sponsor asked whether a verification step had been missed post-closure. Checked retroactively via `gh run list`/`gh run view`: green at every commit this session, all 4 jobs passing for `d72a8ba` (the CI-relevant one). Disclosed as a process gap in the check itself, not just an added data point. |
| 0.2 | 26 July 2026 | Claude Engineering Implementer | Recorded the Programme Sponsor's WP4 determination: establish a new baseline - RBL-0022 supersedes RBL-0021, agreeing with both independent WP3 views. |
| 0.1 | 26 July 2026 | Claude Engineering Implementer | Drafted ESR-0036 WP3 Independent Repository Verification handover, covering the full session diff (`6cf2aeb`..`26dfc55`) across two Work Packages (WP1 EBG-0108 first increment, WP2 documentation staleness fix). Records repository state, authorised working set, six session observations, validation evidence, and an independent baseline view (establish a new baseline, superseding RBL-0021). Submitted to the Engineering Reviewer via the AIEMS Exchange Bridge for genuine independent verification. |
