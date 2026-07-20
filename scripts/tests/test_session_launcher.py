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
    read_current_state,
    read_high_priority_backlog,
    read_near_term_roadmap,
)

_PST_FIXTURE = """\
# PST-0001 - Programme Status

| Field | Value |
|-------|-------|
| Current Mode | ESR-0030 is the latest closed session. |
| Current Repository Baseline | RBL-0017, accepted at ESR-0029 WP9. |
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
    report = build_report(state, backlog_items, roadmap_items)

    assert "## Current State" in report
    assert "## High-Priority Open Backlog (EBR-0001)" in report
    assert "## Near-Term Roadmap Candidates (JRM-0001)" in report
    assert "EBG-0001" in report
    assert "Open Track A Item" in report


def test_build_report_handles_empty_results() -> None:
    from scripts.session_launcher import CurrentState

    state = CurrentState(current_mode="No session open.", current_baseline="RBL-0017.")
    report = build_report(state, (), ())

    assert "_No High-priority Approved/Candidate Backlog items found._" in report
    assert "_No open Near-term roadmap items found._" in report
