"""Tests for scripts/session_launcher.py (EIP-ESR0031-001).

Uses small fixture files matching each artefact's real table shape rather
than the live repository documents, so these tests stay stable regardless
of how PST-0001/EBR-0001/JRM-0001 themselves evolve.
"""

from __future__ import annotations

import pytest

from scripts.session_launcher import (
    SessionLauncherError,
    build_report,
    generate_active_backlog_view,
    read_current_state,
    read_high_priority_backlog,
    read_near_term_roadmap,
    read_open_backlog,
)

_PST_FIXTURE = """\
# PST-0001 - Programme Status

| Field | Value |
|-------|-------|
| Current Mode | ESR-0030 is the latest closed session. |
| Current Repository Baseline | RBL-0017, accepted at ESR-0029 WP9. |

# 8. Active and Next Planned Work

| Item | Notes | Status |
|------|-------|--------|
| Next Work Package Candidate | Theme 7 cleanup, see [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5A - the pipe inside this WikiLink must not shift the Status column into this cell. | Not yet selected |
"""

_PST_FIXTURE_MISSING_BASELINE = """\
# PST-0001 - Programme Status

| Field | Value |
|-------|-------|
| Current Mode | ESR-0030 is the latest closed session. |
"""

_EBR_FIXTURE = """\
# EBR-0001 - Engineering Backlog Register

| EBG-ID | Title | Source | Status | Priority | Owner | Description |
|--------|-------|--------|--------|----------|-------|--------------|
| EBG-0001 | High Approved Item | Source A | Approved Backlog | High | Programme Sponsor | Should be included. |
| EBG-0002 | High Candidate Item | Source B | Candidate Backlog | High | Programme Sponsor | Should also be included. |
| EBG-0003 | Medium Item | Source C | Candidate Backlog | Medium | Programme Sponsor | Should be excluded (not High). |
| EBG-0004 | Completed High Item | Source D | Complete | High | Programme Sponsor | Should be excluded (not open). |
| EBG-0005 | WikiLinked Description | Source E | Approved Backlog | High | Programme Sponsor | See [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] for detail - the pipe inside this WikiLink must not shift later columns. |
"""

_EBR_FIXTURE_NO_ROWS = """\
# EBR-0001 - Engineering Backlog Register

| EBG-ID | Title | Source | Status | Priority | Owner | Description |
|--------|-------|--------|--------|----------|-------|--------------|
"""

_JRM_FIXTURE = """\
# JRM-0001 - Project Roadmap

# 6. Track A - AIEMS Process Roadmap

## 6.1 Near-term

| Item | Rationale |
|------|-----------|
| Open Track A Item | Still genuinely open, no resolution marker. |
| Resolved Track A Item | **Resolved at ESR-0020 WP1** - should be excluded. |

## 6.2 Mid-term

| Item | Rationale |
|------|-----------|
| Mid-term Item | Should never appear - wrong track/horizon entirely. |

---

# 7. Track B - JARVIS Product Capability Roadmap

## 7.1 Near-term

| Item | Rationale |
|------|-----------|
| Open Track B Item | Still open. |

---

# 8. Track C - UXP Evolution Roadmap

## 8.1 Delivered

| Item | Rationale |
|------|-----------|
| Delivered Item | Should never appear - wrong section entirely. |

## 8.2 Near-term

| Item | Rationale |
|------|-----------|
| Open Track C Item | Still open. |

---
"""

_EBR_FIXTURE_MIXED_PRIORITY = """\
# EBR-0001 - Engineering Backlog Register

| EBG-ID | Title | Source | Status | Priority | Owner | Description |
|--------|-------|--------|--------|----------|-------|--------------|
| EBG-0001 | Low Item | Source A | Approved Backlog | Low | Programme Sponsor | Should land in the Low group. |
| EBG-0002 | Unusual Priority Item | Source B | Candidate Backlog | Critical | Programme Sponsor | No standard-priority group - should land in Other, not be dropped. |
"""

_JRM_FIXTURE_MISSING_TRACK = """\
# JRM-0001 - Project Roadmap

# 6. Track A - AIEMS Process Roadmap

## 6.1 Near-term

| Item | Rationale |
|------|-----------|
| Open Track A Item | Still open. |
"""


def test_read_current_state_extracts_both_rows(tmp_path) -> None:
    pst_path = tmp_path / "PST-0001.md"
    pst_path.write_text(_PST_FIXTURE, encoding="utf-8")

    state = read_current_state(pst_path)

    assert state.current_mode == "ESR-0030 is the latest closed session."
    assert state.current_baseline == "RBL-0017, accepted at ESR-0029 WP9."


def test_read_current_state_extracts_next_wp_candidate_from_three_column_row(tmp_path) -> None:
    """EBG-0107 (ESR-0033 WP5): Next Work Package Candidate lives in a
    3-column Section 8 row (Item | Notes | Status), not the 2-column
    Section 3 rows - a naive end-anchored regex would swallow the trailing
    Status column into the same capture. Also regresses the WikiLink-pipe
    column-shift bug this script's own live smoke test previously found."""

    pst_path = tmp_path / "PST-0001.md"
    pst_path.write_text(_PST_FIXTURE, encoding="utf-8")

    state = read_current_state(pst_path)

    assert state.next_wp_candidate == (
        "Theme 7 cleanup, see [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5A - "
        "the pipe inside this WikiLink must not shift the Status column into this cell."
    )
    assert "Not yet selected" not in state.next_wp_candidate


def test_read_current_state_raises_on_missing_row(tmp_path) -> None:
    pst_path = tmp_path / "PST-0001.md"
    pst_path.write_text(_PST_FIXTURE_MISSING_BASELINE, encoding="utf-8")

    with pytest.raises(SessionLauncherError, match="Current Repository Baseline"):
        read_current_state(pst_path)


def test_read_high_priority_backlog_filters_correctly(tmp_path) -> None:
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    items = read_high_priority_backlog(ebr_path)
    ids = [item.id for item in items]

    assert "EBG-0001" in ids
    assert "EBG-0002" in ids
    assert "EBG-0003" not in ids  # Medium priority, excluded
    assert "EBG-0004" not in ids  # Complete, excluded
    assert "EBG-0005" in ids


def test_read_high_priority_backlog_wikilink_pipe_does_not_shift_columns(tmp_path) -> None:
    """Regression test: a WikiLink with display text inside the Description
    cell contains a literal '|' that must not be treated as a column
    separator - naive line.split("|") corrupted every row after the first
    one containing such a link, silently dropping valid High-priority items
    rather than crashing (found during this package's own live smoke test).
    """

    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    items = {item.id: item for item in read_high_priority_backlog(ebr_path)}

    assert "EBG-0005" in items
    item = items["EBG-0005"]
    assert item.status == "Approved Backlog"
    assert item.priority == "High"
    assert "the pipe inside this WikiLink must not shift later columns." in item.description


def test_read_high_priority_backlog_raises_on_no_rows(tmp_path) -> None:
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE_NO_ROWS, encoding="utf-8")

    with pytest.raises(SessionLauncherError, match="No EBG- rows found"):
        read_high_priority_backlog(ebr_path)


def test_read_near_term_roadmap_filters_resolved_items(tmp_path) -> None:
    jrm_path = tmp_path / "JRM-0001.md"
    jrm_path.write_text(_JRM_FIXTURE, encoding="utf-8")

    items = read_near_term_roadmap(jrm_path)
    names = [item.item for item in items]

    assert "Open Track A Item" in names
    assert "Resolved Track A Item" not in names
    assert "Mid-term Item" not in names
    assert "Open Track B Item" in names
    assert "Delivered Item" not in names
    assert "Open Track C Item" in names


def test_read_near_term_roadmap_raises_on_missing_track(tmp_path) -> None:
    jrm_path = tmp_path / "JRM-0001.md"
    jrm_path.write_text(_JRM_FIXTURE_MISSING_TRACK, encoding="utf-8")

    with pytest.raises(SessionLauncherError, match="Track B, Track C"):
        read_near_term_roadmap(jrm_path)


def test_read_open_backlog_returns_every_open_priority(tmp_path) -> None:
    """EBG-0106: with no `priority` filter, every open row is returned
    regardless of Priority - not just High, unlike `read_high_priority_backlog`."""

    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    items = read_open_backlog(ebr_path)
    ids = [item.id for item in items]

    assert "EBG-0001" in ids  # High, Approved Backlog
    assert "EBG-0002" in ids  # High, Candidate Backlog
    assert "EBG-0003" in ids  # Medium - included here, unlike read_high_priority_backlog
    assert "EBG-0004" not in ids  # Complete - excluded regardless of priority
    assert "EBG-0005" in ids


def test_read_open_backlog_filters_by_given_priority(tmp_path) -> None:
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    items = read_open_backlog(ebr_path, priority="Medium")

    assert [item.id for item in items] == ["EBG-0003"]


def test_read_high_priority_backlog_is_a_read_open_backlog_wrapper(tmp_path) -> None:
    """Backward-compatibility check (Codex Finding 1, EIP-ESR0053-001 v0.2):
    read_high_priority_backlog's own behaviour is unchanged by the refactor."""

    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    assert read_high_priority_backlog(ebr_path) == read_open_backlog(ebr_path, priority="High")


def test_generate_active_backlog_view_groups_by_priority_in_order(tmp_path) -> None:
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")

    view = generate_active_backlog_view(read_open_backlog(ebr_path))
    groups = dict(view)

    assert [priority for priority, _ in view] == ["High", "Medium"]  # order preserved, Low omitted (empty)
    assert {item.id for item in groups["High"]} == {"EBG-0001", "EBG-0002", "EBG-0005"}
    assert {item.id for item in groups["Medium"]} == {"EBG-0003"}


def test_generate_active_backlog_view_omits_empty_priority_groups(tmp_path) -> None:
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE_MIXED_PRIORITY, encoding="utf-8")

    view = generate_active_backlog_view(read_open_backlog(ebr_path, priority="Low"))

    assert [priority for priority, _ in view] == ["Low"]


def test_generate_active_backlog_view_groups_unrecognised_priority_as_other(tmp_path) -> None:
    """A Priority value outside the standard three must not be silently
    dropped - it is grouped last, under "Other"."""

    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE_MIXED_PRIORITY, encoding="utf-8")

    view = generate_active_backlog_view(read_open_backlog(ebr_path))
    groups = dict(view)

    assert [priority for priority, _ in view] == ["Low", "Other"]
    assert [item.id for item in groups["Other"]] == ["EBG-0002"]


def test_build_report_includes_all_sections(tmp_path) -> None:
    pst_path = tmp_path / "PST-0001.md"
    pst_path.write_text(_PST_FIXTURE, encoding="utf-8")
    ebr_path = tmp_path / "EBR-0001.md"
    ebr_path.write_text(_EBR_FIXTURE, encoding="utf-8")
    jrm_path = tmp_path / "JRM-0001.md"
    jrm_path.write_text(_JRM_FIXTURE, encoding="utf-8")

    state = read_current_state(pst_path)
    backlog_items = read_high_priority_backlog(ebr_path)
    roadmap_items = read_near_term_roadmap(jrm_path)
    active_backlog_view = generate_active_backlog_view(read_open_backlog(ebr_path))
    report = build_report(state, backlog_items, roadmap_items, active_backlog_view)

    assert "## Current State" in report
    assert "## High-Priority Open Backlog (EBR-0001)" in report
    assert "## Near-Term Roadmap Candidates (JRM-0001)" in report
    assert "## Active Backlog View (mechanically generated from EBR-0001 Section 5 - EBG-0106)" in report
    assert "**Next Work Package Candidate:**" in report
    assert "EBG-0001" in report
    assert "Open Track A Item" in report
    assert "### High" in report
    assert "### Medium" in report
    assert "EBG-0003" in report


def test_build_report_handles_empty_results() -> None:
    from scripts.session_launcher import CurrentState

    state = CurrentState(
        current_mode="No session open.",
        current_baseline="RBL-0017.",
        next_wp_candidate="Not yet determined.",
    )
    report = build_report(state, (), (), ())

    assert "_No High-priority Approved/Candidate Backlog items found._" in report
    assert "_No open Near-term roadmap items found._" in report
    assert "_No open Approved/Candidate Backlog items found in EBR-0001 Section 5._" in report
