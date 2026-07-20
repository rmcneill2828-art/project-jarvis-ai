# EIP-ESR0031-001 - AIEMS Session-Opening Launcher

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0031-001 |
| Artefact ID | EIP-ESR0031-001 |
| Title | AIEMS Session-Opening Launcher |
| Version | 0.1 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0096's brainstorm thread, registered by this package as a new item) |
| Intended Session | ESR-0031 |
| Effective Date | Pending approval |

---

# 2. Purpose

WP0A session-opening synchronisation (PBK-0001) requires reviewing PST-0001's Current Mode/Baseline, the latest closed Engineering Session Report, and EBR-0001's open high-priority backlog before a new session's objective can be confirmed at WP0B. Today this is entirely manual reading. This session's own WP0 demonstrated the cost of that manually-maintained state directly: three separate rounds were needed to find and fix stale "current state" claims scattered across PST-0001, MDS-0001 and PCB-0001 that a human (or an AI reading quickly) could easily miss.

This package implements a small, read-only reporting script that gathers the same evidence PBK-0001's WP0A/WP0B checklist already requires a human to gather by hand, and presents it as a single report - reducing session-opening overhead without changing who decides the session's objective.

---

# 3. Objective

Given the current repository state, produce a single report surfacing: PST-0001's current mode/baseline in one place, EBR-0001's open High-priority backlog items, and JRM-0001's Near-term roadmap candidates not yet marked Resolved/Complete/Delivered - so a WP0B objective discussion starts from a ready-made summary rather than three separate manual document reads.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `scripts/validate_repository.py` | Already has `parse_register_rows()`, `extract_document_version()` and `find_registered_file()` helpers, built for REG-0001's table shape specifically. This package reuses `find_registered_file` where useful but writes its own parser for EBR-0001 and JRM-0001, whose table shapes differ from REG-0001's. |
| `scripts/bump_version.py` | Already exists and already solves the version-bump-consistency problem this session's brainstorm nearly recommended rebuilding - not touched by this package, cited here only to avoid future duplicate effort. |
| PST-0001 Section "Current Mode" / "Current Repository Baseline" rows | Free-form prose cells in a Document Control-style table (not the REG-0001 register table shape) - this package reads them as opaque text, does not attempt to structurally parse their content. |
| EBR-0001's backlog table | Columns: EBG-ID, Title, Source, Status, Priority, Owner, Description (confirmed against the live file - seven columns, EBG-ID column may contain a WikiLink). |
| JRM-0001's Near-term sections | Three separate tables (Track A Section 6.1, Track B Section 7.1, Track C Section 8.2), each `| Item | Rationale |` - resolved items are annotated inline (e.g. "**Resolved at ESR-0023 WP1**") rather than removed from the table, so a naive "list every row" approach would surface already-closed items as if still open (as seen throughout this session's own JRM-0001 reading). |

---

# 5. Scope

This package authorises a future implementation to:

1. Create `scripts/session_launcher.py`:
   - `read_current_state(pst_path: Path) -> CurrentState` - a frozen dataclass with `current_mode: str`, `current_baseline: str` fields, extracted via regex against PST-0001's `| Current Mode | ... |` and `| Current Repository Baseline | ... |` rows. Raises a clear error (not a silent empty result) if either row is not found, so a future PST-0001 restructuring is caught rather than silently producing an empty report.
   - `read_high_priority_backlog(ebr_path: Path) -> tuple[BacklogItem, ...]` - a frozen dataclass (`id`, `title`, `status`, `priority`, `description`) per row, parsing EBR-0001's table directly (its own parser, not a reuse of `parse_register_rows` - different column shape). Filters to `priority == "High"` and `status` in `{"Approved Backlog", "Candidate Backlog"}`.
   - `read_near_term_roadmap(jrm_path: Path) -> tuple[RoadmapItem, ...]` - a frozen dataclass (`track`, `item`, `rationale`) per row from JRM-0001's three Near-term tables (Sections 6.1, 7.1, 8.2, matched by heading text, not hardcoded line numbers, since section numbers have shifted before). Filters out rows whose `rationale` text contains any of `"Resolved"`, `"Complete"`, `"Delivered"`, `"Closed"`, `"Superseded"` (case-insensitive) - a heuristic, disclosed as such (Section 8), not a guarantee.
   - `build_report(current_state, backlog_items, roadmap_items) -> str` - a plain Markdown report with three headed sections in that order, printed to stdout by default.
2. `main()`: CLI entry point, `python scripts/session_launcher.py [--output PATH]`. With `--output`, writes the report to the given path instead of stdout. Read-only throughout - no repository file is ever modified by this script.
3. Add `scripts/tests/test_session_launcher.py` covering: current-state extraction against a real PST-0001-shaped fixture, backlog filtering (High/Approved/Candidate included; Medium or Complete excluded), roadmap filtering (an item with "Resolved at ESR-00xx" in its rationale excluded; an open item included), and a missing-row error case for `read_current_state`.
4. Register **EBG-0097** (this package's own backlog entry) in EBR-0001 as `Complete` only once actually implemented, validated and committed, with corresponding REG-0001 update.
5. Separately, and outside this package's own scope, register a new Candidate Backlog item recommending a future addition to `validate_repository.py`: a check comparing an artefact's `**Version:**` badge against its own Document Control table `Version` row for internal drift (the exact PST-0001 2.66-vs-2.58 bug this session found had no automated check catching it, since `extract_document_version()` only ever reads one of the two locations, preferring the table). This package does not implement that check itself - registering the idea is in scope; building it is not.

No other files are authorised to change. No product UXP changes (`src/`, `src-tauri/`) are in scope - this is an engineering-process tool, not a JARVIS/Guardian capability; PBK-0001's Feature-First Delivery Discipline is satisfied by this session's paired WP2 (Shared Family Memory), not by this package.

---

# 6. Authorised Files

1. `scripts/session_launcher.py`
2. `scripts/tests/test_session_launcher.py`
3. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
4. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
5. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. All three read functions must fail loudly (raise a clear, named exception) on a structural mismatch - a missing expected row or heading - rather than returning an empty or partial result silently. A report that quietly omits a whole section because a heading changed is worse than one that visibly errors.
2. `read_near_term_roadmap()`'s resolved-item filter must be applied to the `rationale` text only, never to the `item` name - filtering must not accidentally exclude an item whose *name* happens to contain a filtered word (none currently do, but this must not be assumed to hold forever without the implementation guarding it explicitly).
3. The script must never write, stage, commit or push anything - it is a read-only reporting tool. No `git` operations of any kind.
4. Table parsing must tolerate a WikiLinked EBG-ID/Item cell (an internal cross-reference link wrapped in double square brackets, the same convention `parse_register_rows()` already handles for REG-0001) since EBR-0001 and JRM-0001 both use this convention inline in table cells.
5. The CLI must exit non-zero and print a clear error (not a traceback) on any `BuildReportError`-style failure, matching `bump_version.py`'s existing `main()` error-handling pattern.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any automatic selection or recommendation of a WP0B objective - the report surfaces candidates; the Programme Sponsor still decides, per PBK-0001's existing WP0B requirement ("Programme Sponsor approval before engineering activity begins").
2. Any repository write, git operation, or bridge submission performed by this script itself.
3. Parsing or surfacing Medium/Low-priority backlog items, Mid-term/Longer-term roadmap items, or any EBR-0001/JRM-0001 content beyond what Section 5 specifies - scope is deliberately narrow (High-priority open backlog, Near-term roadmap only) to keep the report short enough to actually read at WP0.
4. Building the version-badge-vs-table drift check named in Section 5 item 5 - that is a separate future backlog item, not part of this package's implementation.
5. Any integration with `codex exec`, the AIEMS Exchange Bridge, or the automated review pattern proven earlier in this session (EBG-0096) - this is a standalone local reporting script, not part of that automation.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. The script shall be runnable standalone (`python scripts/session_launcher.py`) with no required arguments, defaulting to the live repository's own PST-0001/EBR-0001/JRM-0001 paths - matching the zero-configuration expectation of `scripts/validate_repository.py`.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
python scripts/session_launcher.py
```

Validation should confirm:

1. Full pytest suite passes, including the new `test_session_launcher.py` cases.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. Running the script against the actual live repository produces a coherent, readable report - reviewed manually by the Engineering Implementer as part of self-review, not just exercised via unit tests against fixtures.
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

None - this package reads existing controlled artefacts (PST-0001, EBR-0001, JRM-0001) without modifying the process that produces them.

## Risks

1. **Heading/table-shape brittleness.** All three artefacts' current table shapes were confirmed directly against the live files at draft time (Section 4), but none of the three commit to their table shape as a stable contract - a future restructuring of any of them could break this script's parsing. Mitigated by Implementation Requirement 1 (fail loudly, not silently) rather than avoided entirely.
2. **The resolved-item filter is a heuristic, not a guarantee.** A roadmap rationale that describes a genuinely open item using one of the filtered words in an unrelated sense (unlikely given current phrasing conventions, but not structurally impossible) would be incorrectly excluded from the report. Disclosed, not solved, by this package.
3. **This tool reduces reading effort; it does not reduce review effort.** It does not replace WP0A's own synchronisation checklist (README, PST-0001, latest ESR, GDE-0001, PBK-0001, COC-0001) - it summarises three of those items faster, not all of them.

---

# 12. Approval Request

Draft v0.1 - not yet reviewed by the Engineering Reviewer or approved by the Programme Sponsor.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current Mode/Baseline source this package reads. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | High-priority backlog source this package reads; EBG-0097 registered by this package. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Near-term roadmap source this package reads. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | WP0A/WP0B session-opening requirements this package supports without changing. |
