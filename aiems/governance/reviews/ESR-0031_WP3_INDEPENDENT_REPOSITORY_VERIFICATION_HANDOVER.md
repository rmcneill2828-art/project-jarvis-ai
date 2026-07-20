# ESR-0031 WP3 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0031-WP3 |
| Title | Independent Repository Verification Handover |
| Version | 0.1 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0031 (open; no session report artefact yet - authored later per established practice) |
| Effective Date | 20 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0031's session-wide record for WP3 Independent Repository Verification. WP3 should confirm the current repository state matches the claims made across all of ESR-0031's Work Packages, that disclosed scope boundaries and defects are accurately characterised, and that no unauthorised scope drift occurred. Submitted to Codex via the AIEMS Exchange Bridge for genuine independent verification, continuing the practice used throughout ESR-0025 through ESR-0030 - this session additionally proved a refined review mechanism (`codex exec -s read-only`, Claude relaying findings under explicit Sponsor approval) across every one of its WPs.

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Local `HEAD` | `d611c67` |
| `origin/main` | `d611c67` (pushed, confirmed matching) |
| Working tree | Clean; this handover document itself is the sole untracked file at time of writing |
| Prior accepted baseline | `RBL-0017` |
| ESR-0031 session start point | `82050c9` (ESR-0030 closure's final post-commit fix) |

---

## 4. ESR-0031 Commits in Scope

| Commit | Summary |
|---|---|
| `7393a03` | WP0: repository synchronisation - corrected stale "jarvis/memory/ empty stub" claims across PST-0001/MDS-0001/PCB-0001, predating ESR-0027 WP1's real Personal Memory delivery; also fixed a code-level instance in `jarvis/platform/shell.py`. |
| `52edf8c` | WP0 fix round: addressed two Codex Medium findings - the staleness ran deeper than the first pass caught, five further PST-0001 rows and two further MDS-0001 references still cited stale versions/claims. |
| `e1a61f2` | WP0 second fix round: addressed a Codex Low finding - MDS-0001 still cited the readiness matrix at a stale version. |
| `a4d09ae` | WP0B: registered draft EIP-ESR0031-001 (AIEMS Session-Opening Launcher), EBG-0097, EBG-0098. |
| `28d6236` | WP1: implemented the AIEMS Session-Opening Launcher (`scripts/session_launcher.py`) - two genuine defects found and fixed during its own required live smoke check. |
| `376761f` | WP1 fix round: addressed two Codex post-implementation findings - an EIP wording overclaim ("never writes" contradicting its own authorised `--output` flag) and PST-0001 still saying WP1 was in progress after EBG-0097 was marked Complete in the same commit. |
| `65862d5` | WP2B: registered draft EIP-ESR0031-002 (Streaming Notifications MVP), EBG-0099 - after Shared Family Memory was ruled out as WP2 (GAM-0001 Section 10's explicit non-goal against household identity/authentication enforcement). |
| `97f3c5c` | WP2B fix round: addressed a Codex Medium finding - Implementation Requirements 3 and 4 directly contradicted each other on how to handle an unparsable stream line. |
| `1c99ab5` | WP2B: corrected stale Section 12 wording (Codex non-blocking editorial note). |
| `3377617` | WP2: implemented the Streaming Notifications MVP - Python heartbeat emitter, Rust reader-thread restructuring, React notification listener, live-smoke-tested via a real `npm run tauri dev` session. |
| `d611c67` | WP2 fix round: addressed a Codex Low finding - EBG-0099's row conflated the 4 committed unit tests with a separate, never-committed manual real-subprocess verification script. |

---

## 5. Authorised / Explained Working Set

The full ESR-0031 diff since `82050c9` (16 files changed, 1,353 insertions, 116 deletions):

**WP0 (repository synchronisation, no code except one field fix):**
1. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md` - stale "jarvis/memory/ empty stub" claims corrected across Current Product Capability Baseline, JARVIS Capability Maturity, Current Product Baseline, Repository Health rows; a genuine version-badge-vs-Document-Control-table drift bug found and fixed (2.66 vs 2.58); a missing Version History table header found and fixed.
2. `aiems/models/MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE.md` - Section 5's evidence check and Section 11/12 references to `jarvis/memory/` corrected to reflect the real ESR-0027 WP1 Personal Memory delivery.
3. `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md` - Section 6's blanket "Persistent memory is not implemented" corrected to distinguish the implemented Personal tier.
4. `jarvis/platform/shell.py` - Memory capability status corrected from `NOT_IMPLEMENTED` to `PLACEHOLDER` with an accurate summary.
5. `jarvis/tests/test_guardian_shell.py` - updated to match the corrected capability status.

**WP0B/WP1 (AIEMS Session-Opening Launcher, EBG-0097):**
6. `aiems/governance/reviews/EIP-ESR0031-001_SESSION_OPENING_LAUNCHER.md` (new) - reached v1.1 (Approved-implemented).
7. `scripts/session_launcher.py` (new) - read-only reporting script gathering PST-0001 current state, EBR-0001 high-priority backlog, JRM-0001 near-term roadmap into one report.
8. `scripts/tests/test_session_launcher.py` (new) - 9 tests, including regression tests for two genuine defects (a WikiLink-pipe table-parsing bug, a header-row false-positive) found during the script's own live smoke test.

**WP2B/WP2 (Streaming Notifications MVP, EBG-0099):**
9. `aiems/governance/reviews/EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP.md` (new) - reached v1.0 (Approved-implemented).
10. `jarvis/interfaces/stdio_rpc.py` - `StdioRpcServer` gained a background heartbeat thread emitting `system.heartbeat` JSON-RPC notifications, guarded by a shared write lock.
11. `jarvis/tests/test_stdio_rpc.py` - 4 new in-process unit tests for the heartbeat mechanism.
12. `src-tauri/src/lib.rs` - restructured backend I/O from synchronous write-then-read into a background reader thread plus pending-call dispatch map, distinguishing responses (has `id`) from notifications (no `id`), with connection-level teardown on any unparsable line.
13. `src/App.jsx` - a second, independent `useEffect` listening for `jarvis://notification`, displaying the live heartbeat timestamp.
14. `src/styles.css` - minimal styling for the new heartbeat display element.

**Governance bookkeeping throughout (all WPs):**
15. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - EBG-0097/0098/0099/0100 registered and progressed; reached v1.115.
16. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - version-aligned throughout every commit; reached v3.296.

This is the first session since ESR-0029 to touch `jarvis/` and `src-tauri/`/`src/` product/UXP code, not purely AIEMS tooling or governance documentation - WP2 delivered the UXP's first-ever live-push mechanism, a genuine (if deliberately minimal) new user-observable capability. Zero new third-party dependency in either language - Python uses only `threading`/`datetime` (stdlib), Rust uses only `std::sync`/`std::thread` (stdlib) plus the already-present `tauri`/`serde_json` crates.

---

## 6. Session Observations

1. **WP0 grew substantially larger than its original scope during drafting**, because fixing two stale "jarvis/memory/ empty stub" claims (the original plan) uncovered a genuine, previously-undetected version-drift bug (PST-0001's top banner and Document Control table had silently diverged, 2.66 vs 2.58, unnoticed for several sessions) and a structural defect in the Version History table itself (missing header, stray duplicate). Each was flagged explicitly to the Programme Sponsor before proceeding rather than silently expanding scope.
2. **The same staleness class recurred twice more after the first WP0 commit**, each time caught by Codex rather than a second self-review pass - five further PST-0001 rows citing stale versions on the second round, then MDS-0001's own evidence-check citing a stale readiness-matrix version on the third. An exhaustive whole-file grep sweep (rather than fixing only the cited lines) was adopted from the second round onward, consistent with the same lesson learned repeatedly across ESR-0029/ESR-0030.
3. **A genuinely useful review-automation pattern was proven across every WP this session**: `codex exec -s read-only` (Codex has zero write capability by construction, reporting findings as plain text) with Claude relaying its verbatim findings into the bridge under explicit per-instance Programme Sponsor approval. This replaced an earlier `workspace-write`-mode attempt that depended on a fragile Windows sandbox ACE grant (`SetNamedSecurityInfoW failed: 5`), root-caused during this session's own brainstorming thread to the Programme Sponsor's deliberate `elevated` sandbox setting - a control against Codex misreading pasted directive text as authorisation to act, correctly left in place rather than relaxed.
4. **WP1's own required live smoke check found two genuine defects that unit tests alone would not have caught**: a naive `line.split("|")` table parser silently corrupted every row after the first one containing a WikiLink with display text in a non-ID cell, dropping several genuinely High-priority backlog items from the report with no error at all; and the table header row itself matched the "found a data row" check (since "EBG-ID" starts with "EBG-"), which would have masked the intended "no rows found" error case. Both fixed with regression tests before the smoke check was considered complete.
5. **The originally-selected WP2 objective (Shared Family Memory) was abandoned before drafting began**, once GAM-0001 Section 10's explicit non-goal (household role authentication/enforcement is not implemented) was checked directly - a technically honest implementation could not have differentiated access by household role today. Streaming Notifications MVP was substituted, itself chosen only after confirming its own trigger condition (a production provider wired into the runtime, EBG-0070) had already happened and that no smaller product-moving alternative was being overlooked.
6. **WP2's pre-implementation review found a real internal contradiction before any code was written**: the EIP's own Implementation Requirements 3 and 4 disagreed on how to handle an unparsable stream line - one said log-and-ignore, the other implicitly required a call to fail loudly - a contradiction the reader thread's design genuinely could not resolve on its own (an unparsable line carries no `id` to correlate against anything). Resolved by treating any unparsable line as connection-level corruption, failing every pending call rather than guessing which one it was meant for.
7. **WP2's implementation was live-smoke-tested against the real running application, not just unit tests** - a genuine `npm run tauri dev` session, two screenshots roughly 35 seconds apart, showing the heartbeat timestamp advance from 16:34:18 to 16:35:48 while `platform_status`/`knowledge_graph` (the pre-existing request/response path, sharing the same restructured `call_backend()`) continued to populate real data in the same session, directly evidencing that the Rust I/O restructuring did not silently break existing calls.
8. **A stray UI-automation attempt during that same smoke check misfired onto the wrong foreground window** (VS Code rather than the JARVIS app) and was abandoned once the screenshot evidence already in hand was judged sufficient - disclosed in EBG-0099's own record rather than omitted, though it had no material effect on the result.
9. **A post-implementation review found a genuine governance-accuracy defect, not a code defect**: EBG-0099's own record initially conflated the 4 real committed unit tests with a separate, ad hoc, never-committed manual real-subprocess verification script, describing both as if they were part of the same "4 new tests" claim. Corrected once found.
10. **A new backlog item (EBG-0100) was discovered as a byproduct of the live smoke check itself, not sought out** - the UXP's capability sidebar hardcodes the Memory row as "Not Implemented" regardless of actual backend state, unrelated to and not fixed by this session's own `jarvis/platform/shell.py` correction (a different code path entirely). Registered, not fixed, being out of WP2's own scope.

---

## 7. Validation Evidence

Re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 351 passed |
| `python scripts/validate_repository.py` (full, not governance-only) | 0 errors, 140 warnings |
| `cargo build --manifest-path src-tauri/Cargo.toml` | Clean, no warnings |
| `npm run build` | Clean |
| `git status` | Committed tree clean on `main` at `d611c67`, matching `origin/main`; working tree has only this untracked WP3 handover document. |

The warning count rose from 130 (ESR-0030 closure) to 140 across this session - all confirmed to be the same known false-positive pattern (cross-document "Section N.N" references `validate_repository.py` cannot disambiguate from same-document headings), not a new class of problem.

---

## 8. Scope Check

- `jarvis/`, `src-tauri/`, and `src/` were genuinely touched this session (WP0's `shell.py` fix, WP1's launcher script, WP2's streaming-notifications feature) - a departure from ESR-0030's AIEMS-tooling-only pattern, matching this session's Feature-First Delivery Discipline pairing (a process-tooling WP alongside a genuine product-moving WP).
- Zero new third-party dependency in either language.
- No `sentinel/` trust-boundary code touched.
- No changes to the Sponsor Approval Service, its token handling, or the bridge's core commands beyond what each WP's own EIP explicitly authorised.
- Working tree is clean and pushed; this handover document is the sole untracked file, being this review's own subject.

---

## 9. WP4 Baseline Recommendation

**Engineering Implementer's independent view:** accept a new baseline (`RBL-0018`), superseding `RBL-0017`.

Rationale: unlike ESR-0030 (pure AIEMS process tooling), this session delivered a genuine, live-verified, user-observable UXP capability - the streaming-notifications heartbeat display, the first live-push mechanism the UXP has ever had, proven via a real running application session rather than unit tests alone. This matches the pattern of ESR-0028/ESR-0029's own new-baseline sessions (Guardian Orb rotation, Canvas 2D migration) rather than ESR-0025/ESR-0026/ESR-0027/ESR-0030's retain-baseline pattern. `PCB-0001` and the JARVIS Capability Readiness Matrix both already reflect this session's Memory-status corrections (WP0) as part of the same baseline; the streaming-notifications capability itself is not yet reflected in either and would need its own follow-on refresh, similar to precedent.

**Engineering Reviewer's independent view (Codex):** to be recorded here once WP3 review returns.

---

## 10. WP3 Verification Result

Pending Codex's independent review via the AIEMS Exchange Bridge.

---

## 11. WP4 Baseline Acceptance Result

Pending Programme Sponsor determination.

---

## 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] | Approved-implemented package for WP0B/WP1, v1.1. |
| [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] | Approved-implemented package for WP2B/WP2, v1.0. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0097/0099 Complete this session; EBG-0098/0100 registered, Candidate Backlog. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for the session's controlled artefacts. |
| [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | Prior accepted repository baseline. |
| [[ESR-0030_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0030 WP3 Handover]] | Precedent handover this document follows the structure of. |

---

## 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 20 July 2026 | Claude Engineering Implementer | Drafted ESR-0031 WP3 Independent Repository Verification handover, covering the full session diff (`82050c9`..`d611c67`) across WP0/WP0B/WP1/WP2B/WP2. Records repository state, authorised working set, session observations (staleness recurrence, the proven read-only review-automation pattern, two genuine WP1 defects found via live smoke test, the Shared Family Memory scope reconsideration, WP2's pre-implementation contradiction fix, WP2's own live smoke test, and a governance-accuracy self-correction), validation evidence, and an independent baseline view (accept a new baseline, RBL-0018 - unlike ESR-0030, this session delivered a genuine live-verified UXP capability). Submitted to the Engineering Reviewer via the AIEMS Exchange Bridge for genuine independent verification.
