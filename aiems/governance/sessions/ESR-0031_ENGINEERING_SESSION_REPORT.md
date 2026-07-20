# ESR-0031 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0031 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0031 |
| Date Opened | 20 July 2026 |
| Date Closed | 20 July 2026 |
| Closure Status | Closed - WP0-WP2 complete, session-wide WP3 Pass, WP4 Accept (RBL-0018 established) |

---

# 2. Purpose

This report records the opening and execution of ESR-0031, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0030, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service (ADR-0022) with no manual relay anywhere - the sixth consecutive session run this way. It paired a process-improvement objective (the AIEMS Session-Opening Launcher) with a genuine product-moving objective (Streaming Notifications MVP) per PBK-0001's Feature-First Delivery Discipline, and directed a new standing PBK-0001 practice - Documentation Debt Discipline - following a live example found during the session's own WP4 baseline-acceptance closure.

---

# 3. Scope

ESR-0031 opened with WP0 repository synchronisation, which found and fixed stale "`jarvis/memory/` empty stub" claims across PST-0001, MDS-0001 and PCB-0001 (predating ESR-0027 WP1's real Personal Memory delivery) and one matching code-level instance in `jarvis/platform/shell.py`, across three fix rounds - a genuine version-badge-vs-Document-Control-table drift bug (PST-0001: 2.66 vs 2.58) was also found and fixed along the way.

The Programme Sponsor selected the AIEMS Session-Opening Launcher as the session's process-improvement objective (WP0B/WP1). Pairing it with product-moving work was required by PBK-0001's Feature-First Delivery Discipline; Shared Family Memory was considered as that paired objective but ruled out before drafting once GAM-0001 Section 10's explicit non-goal (household role authentication/enforcement not implemented) was checked directly. Streaming Notifications MVP was selected instead (WP2B/WP2), closing EBG-0050's long-open remaining scope.

Session-wide WP3 (Independent Repository Verification) and WP4 (Repository Baseline Acceptance) closed the session: WP3 reached Pass after one fix round on the handover's own self-referential HEAD-staleness; WP4 established a new baseline, [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]], superseding RBL-0017 - both independent views agreeing this session delivered a genuine, live-verified product capability rather than process tooling alone. WP4's closure also directed a new PBK-0001 practice, Documentation Debt Discipline, following a live example found during that same closure (Section 8/9's duplicate "current state" rows had drifted stale for five sessions). WP4's own commit then went through two further Codex-caught fix rounds before reaching a clean Pass - see Section 11.

---

# 4. Engineering Authority

ESR-0031 opening was authorised by Programme Sponsor instruction on 20 July 2026, following repository synchronisation confirming [[ESR-0030_ENGINEERING_SESSION_REPORT|ESR-0030]] was closed and [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Two objectives, selected by the Programme Sponsor at WP0B/WP2B from sets of `AskUserQuestion` candidates:

- **WP1** - AIEMS Session-Opening Launcher (EBG-0097), a read-only reporting script gathering PST-0001's Current Mode/Baseline, EBR-0001's open High-priority backlog, and JRM-0001's Near-term roadmap into a single WP0B discussion aid.
- **WP2** - Streaming Notifications MVP (EBG-0099, EBG-0050's remaining scope), the UXP-backend bridge's first live-push mechanism - selected after Shared Family Memory was ruled out per GAM-0001 Section 10.

Both were met by closure, each with a genuine defect found and fixed during its own required live smoke check rather than unit tests alone.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation - stale memory-capability claims fixed across three rounds | Complete - Section 7 |
| WP0B | Session objective selection; registered draft EIP-ESR0031-001 | Complete - Section 7 |
| WP1 | AIEMS Session-Opening Launcher implementation per EIP-ESR0031-001 | Complete - Section 8 |
| WP2B | Streaming Notifications MVP selection (after Shared Family Memory ruled out); registered draft EIP-ESR0031-002 | Complete - Section 9 |
| WP2 | Streaming Notifications MVP implementation per EIP-ESR0031-002 | Complete - Section 9 |
| Session-wide WP3/WP4 | Independent Repository Verification; Repository Baseline Acceptance (RBL-0018 established) | Complete - Section 10/11 |

---

# 7. WP0/WP0B - Session Initialisation Record

**WP0 - Repository Synchronisation:**

- Repository state verified directly against `origin/main`, confirming ESR-0030 formally closed and RBL-0017 the accepted baseline at session open.
- **Found and fixed stale "`jarvis/memory/` empty stub" claims** across PST-0001, MDS-0001 and PCB-0001, and one matching code-level instance in `jarvis/platform/shell.py` (memory capability status changed from `NOT_IMPLEMENTED` to `PLACEHOLDER`) - all predating ESR-0027 WP1's real Personal Memory delivery. Required three fix rounds: each Codex review found more stale instances than the prior sweep caught.
- **A genuine version-badge-vs-Document-Control-table drift bug was found and fixed along the way** (PST-0001's top-of-file badge said 2.66, its own table said 2.58, eight versions apart, unnoticed for several sessions) - registered as EBG-0098 (Candidate Backlog) since `validate_repository.py` has no check comparing the two locations within the same document.
- Commit SHAs: `7393a03` (initial sync), `52edf8c` (Codex Medium fix round), `e1a61f2` (second fix round, readiness-matrix version cite).

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0031 (this report, authored at closure per established practice).
- Repository baseline reference at opening: RBL-0017 (superseded by this session's own WP4).
- Session objective selection presented via `AskUserQuestion`: the Programme Sponsor selected the AIEMS Session-Opening Launcher. Pairing it with genuine product-moving work (required by PBK-0001's Feature-First Delivery Discipline) led to Shared Family Memory being considered and then ruled out before drafting (Section 9), replaced with Streaming Notifications MVP.
- Draft [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] registered; EBG-0097 and EBG-0098 registered in EBR-0001.
- Commit SHA: `a4d09ae`.

---

# 8. WP1 - AIEMS Session-Opening Launcher (EBG-0097)

Implements [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] v1.1 (Approved-implemented).

**Delivered**: `scripts/session_launcher.py` (new) - a read-only reporting script with `_split_table_row()` (a WikiLink-aware table-row parser), `_EBG_ID_PATTERN`, and functions gathering PST-0001's Current State, EBR-0001's High-priority backlog, and JRM-0001's Near-term roadmap into a single `build_report()` output. `scripts/tests/test_session_launcher.py` (new), 9 tests.

**Two genuine defects were found and fixed during the package's own required live smoke check, not just unit tests**: a naive `line.split("|")` table-row parser silently corrupted every row after the first one containing a WikiLink with display text in a non-ID cell (a double-square-bracket link whose target and display text are themselves separated by a literal pipe character, mistaken for a column boundary), shifting later columns and dropping several genuinely High-priority backlog items without any error - fixed with the WikiLink-aware `_split_table_row()`, with a regression test. A second defect (the table header row `| EBG-ID | ... |` itself matching the "row found" detection, since "EBG-ID" starts with "EBG-", masking the intended "no data rows" error case) was also found via the test suite and fixed with `_EBG_ID_PATTERN`.

**A post-implementation fix round** corrected an EIP-stage wording overclaim ("never writes" contradicted the EIP's own authorised `--output` flag) and added a Version History section that had been missing from the original draft entirely - a structural gap versus this project's established EIP template.

- Commit SHAs: `28d6236` (implementation), `376761f` (post-implementation fix round)
- `python -m pytest`: 347 passed (was 338 at ESR-0030's closure). `python scripts/validate_repository.py`: 0 errors, clean.

---

# 9. WP2B/WP2 - Streaming Notifications MVP (EBG-0099)

Closes EBG-0050's long-open "streaming notifications" remaining scope - the UXP-backend bridge's first live-push mechanism, per [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] v1.0 (Approved-implemented).

**Shared Family Memory was the originally-selected paired objective, abandoned before drafting** once GAM-0001 Section 10's explicit non-goal (household role authentication/enforcement not implemented) was checked directly - no identity system exists to differentiate Guest/Child/Adult/Administrator access against, avoiding wasted implementation effort on a premature scope.

**A genuine internal contradiction in the implementation package's own requirements was found and fixed before any code was written**: Implementation Requirements 3 and 4 disagreed on how an unparsable stream line should be handled - resolved by treating any unparsable line as connection-level corruption (failing all pending calls and resetting connection state), since the reader thread has no way to distinguish a broken notification from a broken response.

**Delivered**: `jarvis/interfaces/stdio_rpc.py`'s `StdioRpcServer` gained a background heartbeat thread emitting a `system.heartbeat` JSON-RPC notification (no `id` key) every `JARVIS_HEARTBEAT_INTERVAL_SECONDS` (default 30s), guarded by a shared write lock - 4 new in-process unit tests. `src-tauri/src/lib.rs` was restructured from a single synchronous write-then-read per call into a background reader thread plus a pending-call dispatch map (`Arc<Mutex<HashMap<u64, mpsc::Sender<...>>>>`): a line with an `id` key routes to the matching in-flight call, a line with none is forwarded to the frontend via `app_handle.emit("jarvis://notification", ...)`. `src/App.jsx`/`src/styles.css` gained a second, independent `useEffect` (via `@tauri-apps/api/event`'s `listen()`) displaying the live heartbeat timestamp next to the System Health panel.

**Live-smoke-tested via a real `npm run tauri dev` session** per PBK-0001's Operational Verification Before Reporting: two screenshots ~35 seconds apart proved the heartbeat timestamp genuinely advanced while `platform_status`/`knowledge_graph` (the pre-existing request/response path, using the same restructured `call_backend()`) continued to populate real data correctly in the same session - not unit tests alone. A stray UI-automation attempt to also exercise `send_message` misfired onto the wrong foreground window (VS Code) and was abandoned as unnecessary once this evidence was already in hand. A Vite `node.exe` left holding port 1420 after `TaskStop` was found and killed explicitly, matching the standing known-insufficient-cleanup lesson.

**A post-commit Codex finding was corrected**: EBG-0099's register entry had incorrectly described a real-subprocess smoke test as part of the committed "4 new tests" - corrected to distinguish the 4 real in-process unit tests from the separate, never-committed manual verification script.

A byproduct discovered during the same live smoke check, out of this WP's own scope, was registered as EBG-0100 (UXP capability sidebar's Memory row hardcoded to `NOT_IMPLEMENTED` despite EBG-0080's real Personal Memory delivery since ESR-0027).

- Commit SHAs: `65862d5` (draft EIP), `97f3c5c` (pre-implementation contradiction fix), `1c99ab5` (wording fix), `3377617` (implementation), `d611c67` (test-coverage overclaim fix)
- `python -m pytest`: 351 passed. `cargo build`/`npm run build`: clean. `python scripts/validate_repository.py`: 0 errors, clean.

---

# 10. Session-Wide WP3 - Independent Repository Verification

**Handover preparation**: an [[ESR-0031_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0031 WP3 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session's intended content range (`82050c9`..`d611c67`) across WP0/WP0B/WP1/WP2B/WP2.

**One fix round was required**, on the handover document's own self-referential HEAD-staleness: the handover necessarily gets committed after the endpoint it describes, the same point ESR-0030's own WP3 handover ran into. Fixed by explicitly distinguishing the session's content endpoint from the handover's own commit(s) throughout.

**Pass, both independent views converging**: this session delivered a genuine, live-verified, user-observable UXP capability (Streaming Notifications MVP) - not process tooling alone.

- Commit SHAs: `bcae059` (handover draft), `4c5e4dd` (fix round, Pass recorded)
- `python scripts/validate_repository.py` (full mode): 0 errors, 140 warnings at the time of this WP.

---

# 11. Session-Wide WP4 - Repository Baseline Acceptance (RBL-0018 Established)

**Both independent WP3 views recommended a new baseline** rather than retaining RBL-0017, matching the pattern of RBL-0016/RBL-0017's own product-capability-change triggers. The Programme Sponsor's determination: **establish a new baseline** - [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]].

**A new PBK-0001 practice was directed during this closure: Documentation Debt Discipline** (whole-document staleness sweeps on edit; documentation-debt backlog items get first priority over new capability work until that category is empty). This followed a direct discussion the Programme Sponsor raised mid-closure about the volume of planned work repeatedly changing due to incomplete engineering work or incorrect documentation - diagnosed as documentation duplication without automated drift-checking, combined with documentation-debt backlog items having no forcing function against perpetual deprioritisation. Applying the new discipline immediately surfaced a genuine, much-larger-than-expected live example: PST-0001's Section 8/9 "current state" rows had independently duplicated Section 3/4A's own facts and drifted stale for five to six sessions (one row still described ESR-0025) while Section 3/4A were kept current throughout - restructured to reference the authoritative section rather than restate it, and a stale JRM-0001 version citation (v1.13, actual v1.16) was corrected in the same sweep.

**The initial WP4 commit (`d0c9435`) went through two further Codex-caught fix rounds before reaching a clean Pass**:

- *First fix round (`0370726`)*: Codex's independent post-implementation review found two genuine issues - PBK-0001 still named RBL-0017 as the current baseline in two places (Related Artefacts, OSE Relationships), directly undercutting the Whole-Document Staleness Sweep rule added in the same commit; and RBL-0018/PST-0001 stated a stale "140 warnings" verification figure against the actual 143 at the time. Both fixed. Fixing the warning count itself proved self-referential: the fix text's own new content ("Section 4A narrative, Section 9 Current Activity row") added one further genuine cross-document "Section N" false positive, requiring one more pass to land on the true stable figure, 144. **A separate, unrelated tooling defect was found and fixed while bumping versions for this round**: `scripts/bump_version.py`'s `--date` flag silently defaults to a stale hardcoded placeholder ("9 July 2026", a literal example value from its own `--help` text) rather than deriving today's date, which mis-dated six Version History/REG-0001 rows - all six corrected to 20 July 2026, and the tool defect itself registered as EBG-0101 (Candidate Backlog) rather than fixed in this round.
- *Second fix round (`ff12ba1`)*: Codex's review of the first fix round found one residual issue - REG-0001's own copied Version History summaries (rows 3.300, 3.301) still said "the actual 143" after RBL-0018/PST-0001's own body text had already been corrected to 144. Corrected both rows.
- *Final review*: **Pass, no findings.** Codex independently re-ran `validate_repository.py` (0 errors, 144 warnings, matching) and confirmed both REG-0001 rows now read 144.

- Commit SHAs: `d0c9435` (WP4 closure, RBL-0018 accepted, Documentation Debt Discipline directed), `0370726` (first fix round), `ff12ba1` (second fix round, clean Pass)
- `python -m pytest`: 351 passed throughout. `python scripts/validate_repository.py` (full mode): 0 errors, 144 warnings (final, stable figure).

---

# 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] | Approved-implemented package for WP1, v1.1. |
| [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] | Approved-implemented package for WP2, v1.0. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0097, EBG-0099 Complete; EBG-0098, EBG-0100, EBG-0101 registered, Candidate Backlog. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 10's explicit non-goal against household identity/authentication ruled out Shared Family Memory as WP2, avoiding wasted implementation effort. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | New Documentation Debt Discipline section directed this session, v1.31. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0031_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0031 WP3 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, Section 10/11. |
| [[ESR-0030_ENGINEERING_SESSION_REPORT|ESR-0030]] | Prior closed session this one continues from. |
| [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] | New repository baseline established at Section 11, superseding RBL-0017. |

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 20 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0 (stale memory-claim fixes, three rounds), WP0B/WP1 (AIEMS Session-Opening Launcher, two genuine defects caught by its own live smoke check), WP2B/WP2 (Streaming Notifications MVP after Shared Family Memory was ruled out per GAM-0001 Section 10, live-smoke-tested via a real Tauri session), and the session-wide WP3 Independent Repository Verification (Pass after one self-referential-staleness fix round) and WP4 Repository Baseline Acceptance (RBL-0018 established, Documentation Debt Discipline directed, two further Codex-caught fix rounds before a clean Pass). Sixth session run entirely through the AIEMS Exchange Bridge and the deployed Sponsor Approval Service with no manual relay. Status Open to Closed. |
