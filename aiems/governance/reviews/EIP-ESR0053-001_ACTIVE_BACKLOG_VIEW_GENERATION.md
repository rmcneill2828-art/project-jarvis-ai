# EIP-ESR0053-001 - Active Backlog View Generation (EBG-0106)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0053-001 |
| Title | Engineering Implementation Package: WP1 Active Backlog View Generation |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0053 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0053 WP1: resolves EBG-0106 by replacing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5A's hand-maintained "Active Backlog View" snapshot with a view mechanically generated from Section 5's own Status/Priority columns.

Selected per PBK-0001's Documentation-Debt Priority discipline, ahead of new capability work, following a live confirmation during ESR-0053 WP0A that Section 5A is currently stale: it still lists EBG-0115 (Kokoro TTS) and EBG-0111 (Composio) as open Theme 8 items, though both were resolved at [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] WP2/WP3 (Composio Deferred, Kokoro Completed). This is the second observed drift of this same section (the first triggered its ESR-0048 WP1 full regeneration) - direct evidence for EBG-0106's own diagnosis that a hand-maintained second source of truth drifts regardless of the "do not edit in place" warning already present in the section's own header.

---

# 3. Repository Context Investigated

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5A (`aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`): theme-grouped, manually regenerated snapshot, last regenerated 4 August 2026 (ESR-0048 WP1) - now stale again, confirming EBG-0106's own diagnosis rather than a one-off lapse.
* Section 5's own table columns: `| Backlog ID | Title | Source | Status | Priority | Owner | Notes |` - `Status` and `Priority` are the only fields structured enough to group by mechanically; there is no `Theme` column on Section 5 itself, so Section 5A's existing per-item Theme grouping is not derivable without a separate, unauthorised schema change to Section 5.
* `scripts/session_launcher.py` (EIP-ESR0031-001, extended EBG-0107): already has a WikiLink-safe table-row parser (`_split_table_row`), a `read_high_priority_backlog()` reader that filters Section 5 to open (`Approved Backlog`/`Candidate Backlog`) rows of one Priority, and a separate `read_active_backlog_snapshot()` that parses Section 5A's own theme tables - the exact reader whose source data is stale today, and whose own docstring already names EBG-0106 as "the exact gap that made this script show nothing useful" once Section 5A itself falls behind.
* `scripts/tests/test_session_launcher.py`: fixture-based tests covering all of the above readers and `build_report()`, none touching the live repository documents.
* EBG-0106's own [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5 entry: proposes "a smaller, derived active-product-backlog view... mechanically generated from EBR-0001's own Status/Priority fields rather than manually maintained," explicitly naming a script "analogous to `session_launcher.py`, not a new hand-maintained document," and leaves open whether the result should be committed to the repository or generated on demand - that decision is made by this package (Section 4C).
* `git status`: clean; current branch `main`; up to date with `origin/main` as of WP0A.

---

# 4. Scope by Item

## 4A. Generalise the existing reader

`scripts/session_launcher.py`'s `read_high_priority_backlog()` is refactored into `read_open_backlog(ebr_path, priority=None)`, returning every open (`Approved Backlog`/`Candidate Backlog`) Section 5 row, optionally filtered to one `Priority` value. `read_high_priority_backlog()` is retained as a one-line wrapper (`return read_open_backlog(ebr_path, priority="High")`), preserving its current signature and behaviour - this half of the refactor is genuinely backward-compatible for its existing callers and tests. `read_active_backlog_snapshot()` and the `ActiveBacklogItem` dataclass it returns are a separate matter, covered by 4C: they are intentionally, breakingly retired, not preserved - their removal is not "unaffected" by this package, since Section 5A's theme tables (their only source data) are removed in the same change.

## 4B. New mechanical grouping function

A new `generate_active_backlog_view(items)` groups an already-read tuple of open `BacklogItem`s by `Priority`, in `High -> Medium -> Low` order (any other literal `Priority` value present is grouped last, under `Other`, rather than silently dropped). This is the direct mechanical analogue of EBG-0106's own example grouping ("Now/Next/Later"), derived only from data Section 5 already carries - no new column, no manual curation.

## 4C. Retire the hand-maintained snapshot; generate on demand

`read_active_backlog_snapshot()`, the `ActiveBacklogItem` dataclass, and the three Section-5A-specific regex constants are removed - there is no longer a Section 5A table shape for them to parse. `build_report()`'s "Active Backlog Snapshot" section is rebuilt from `generate_active_backlog_view(read_open_backlog(ebr_path))` instead, retitled "Active Backlog View" to match the new mechanism.

**Design decision (EBG-0106's own open question): generated on demand, not committed.** EBR-0001 Section 5A's theme tables are replaced with a short paragraph explaining that the active view is no longer stored here - it is produced fresh by running `python scripts/session_launcher.py`, whose "Active Backlog View" section reads Section 5 directly - and that this section shall not be hand-edited to re-add a static table. This is the only design that removes the second-source-of-truth problem EBG-0106 names rather than relocating it: a committed, periodically-regenerated table would still drift in every session that does not happen to touch it, exactly as Section 5A itself has now drifted twice.

**Disclosed trade-off, not resolved by this package**: Section 5A's existing Theme groupings (e.g. "Theme 5 - Security Hygiene", "Theme 8 - Deferred Product Research") carry real curatorial value beyond raw Priority and are lost by this change, since Section 5 has no `Theme` column for a script to read. Reintroducing thematic grouping would require adding and maintaining a `Theme` column across Section 5's own rows - a materially larger change than this WP's scope, and not authorised here. If the Programme Sponsor wants thematic grouping preserved, that is a separate future backlog item, not silently folded into this one.

## 4D. Update `session_launcher.py`'s own docstring

Lines 11-18's note ("EBG-0106's own generation-mechanism scope... remains separately unimplemented") is corrected to describe the now-implemented mechanism instead of flagging it as an open gap.

## 4E. Close EBG-0106

EBR-0001's own EBG-0106 row (Section 5) is updated: Status `Approved Backlog` to `Completed`, Notes extended with an implementation summary and a pointer to this package. Section 5A's header/date-stamp line is replaced per 4C above.

---

# 5. Validation

* `python -m pytest scripts/tests/test_session_launcher.py` - **behaviour unchanged** for `read_current_state`, `read_near_term_roadmap` and `read_high_priority_backlog` (via its `read_open_backlog` wrapper): their existing test assertions carry over as-is. **Test wiring necessarily changes**, not merely "unchanged": the test module's import list drops `read_active_backlog_snapshot`/`ActiveBacklogItem` (both removed by 4C) and gains `read_open_backlog`/`generate_active_backlog_view`; `test_build_report_includes_all_sections`/`test_build_report_handles_empty_results` are updated for `build_report()`'s new signature (Section 4C); the four `test_read_active_backlog_snapshot_*` tests are removed outright (their subject no longer exists) and replaced with equivalent-intent coverage for `read_open_backlog(priority=None)` and `generate_active_backlog_view()` (priority-grouping order, empty-group omission, unrecognised-priority handling, WikiLink-pipe column safety carried over from the removed tests' fixtures).
* `python -m pytest jarvis/tests sentinel scripts/tests` (full suite) - no production `jarvis/`/`sentinel/`/`src/` code touched; count should be unchanged from ESR-0052's closing 530 passed/1 skipped.
* `python scripts/validate_repository.py` (full mode) - 0 errors expected; confirms no unresolved WikiLinks introduced by Section 5A's rewritten text.
* Live run: `python scripts/session_launcher.py` against the real repository EBR-0001, confirming the "Active Backlog View" section's Priority groups match a manual spot-count of Section 5's current open rows.

**Actual results (deviation disclosed):** `scripts/tests/test_session_launcher.py` - 16 passed (was 14; net +2, not the predicted "unchanged" test wiring - the four removed Section-5A tests were replaced by seven new ones covering `read_open_backlog`/`generate_active_backlog_view`, a net gain rather than a like-for-like swap). Full suite `python -m pytest jarvis/tests sentinel scripts/tests` - **532 passed, 1 skipped** (up from ESR-0052's closing 530/1, matching the +2 above; no production `jarvis/`/`sentinel/`/`src/` code touched). `python scripts/validate_repository.py --governance-only` - 0 errors, 298 warnings (unchanged from pre-implementation, none newly introduced by this package's files). Live `python scripts/session_launcher.py` run against the real repository confirmed the "Active Backlog View" section correctly Priority-groups the real open Section 5 rows (spot-checked against a manual count).

---

# 6. Explicitly Excluded

* Adding a `Theme` column to Section 5 or otherwise preserving thematic grouping (Section 4C's disclosed trade-off) - a separate future backlog item if wanted, not this package's scope.
* Any change to `EBR-0001`'s Section 5 main table content beyond the single EBG-0106 row closure (4E) - no other backlog item's Status/Priority/Notes are touched.
* Any change to `PST-0001`'s Next Work Package Candidate reading logic (`read_current_state()`) or to `read_near_term_roadmap()` - both out of this item's scope.
* Committing a static, periodically-regenerated Section 5A table (rejected design alternative, Section 4C) - the on-demand design is the one implemented.
* Any Sentinel/security-relevant code path; any `src/`/`src-tauri/` change.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0053`/`WP1`). **Verdict: Conditional Pass with corrections**, timestamp 2026-08-27T20:19:33Z. Codex confirmed, via direct repository search, that no production caller of `read_high_priority_backlog`/`read_active_backlog_snapshot` exists outside `scripts/session_launcher.py` and `scripts/tests/test_session_launcher.py`, and independently agreed with all four requested assessments: (1) the on-demand design genuinely removes the second-source-of-truth drift rather than relocating it, since no derived table is committed; (2) the Theme-grouping trade-off is adequately disclosed; (3) the `read_open_backlog` wrapper design is safe for the real visible callers; (4) WikiLink/registration hygiene found acceptable, REG-0001/ESR-0053 entries confirmed consistent. **Required corrections, folded into v0.2 above:** (Finding 1, Medium) Section 4A's original wording risked implying the whole refactor was non-breaking while 4C separately removes `read_active_backlog_snapshot()`/`ActiveBacklogItem` - reworded to state plainly that only the `read_high_priority_backlog` half is backward-compatible, while the Section-5A parser is an intentional breaking retirement. (Finding 2, Low) Section 5's validation wording overclaimed "tests continue passing unchanged" when the test module's own import list and `build_report` tests necessarily change once the removed symbols and rebuilt signature take effect - reworded to distinguish unchanged behavioural expectations from changed test wiring.

---

# 8. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0106 (closed by this package), Section 5A (rewritten by this package).
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Documentation-Debt Priority Until Backlog Cleared, the discipline that selected this WP ahead of new capability work.
* [[ESR-0053_ENGINEERING_SESSION_REPORT|ESR-0053]] - this session's report, WP1.
* `scripts/session_launcher.py` / `scripts/tests/test_session_launcher.py` - the reader/generator this package modifies.
* EBG-0107 (`EBR-0001` Section 5) - the prior `session_launcher.py` fix whose own closure note first named this package's scope as separately unimplemented.
