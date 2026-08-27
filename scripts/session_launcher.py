"""AIEMS Session-Opening Launcher (EIP-ESR0031-001, extended EBG-0107, EBG-0106).

Read-only reporting script gathering PST-0001's current state (including
its Next Work Package Candidate row), EBR-0001's open High-priority
backlog and mechanically-generated Active Backlog View, and JRM-0001's
Near-term roadmap candidates into one report, for WP0B objective
discussion. Never writes, stages, commits or pushes anything - the
Programme Sponsor still decides the session objective; this only reduces
the manual reading required to get there.

EBG-0107 (ESR-0033 WP5): the two additions below - Next Work Package
Candidate and an active-backlog view - were the exact gap that made this
script show nothing useful for WP0B selection even after PST-0001 and
EBR-0001 had already been updated to name real candidates.

EBG-0106 (ESR-0053 WP1): the active-backlog view is now generated
directly from Section 5's own Status/Priority columns (`read_open_backlog`
grouped by `generate_active_backlog_view`), not parsed from a hand-
maintained EBR-0001 Section 5A snapshot table - that table drifted stale
twice (most recently, still listing items resolved at ESR-0052) despite
its own "do not edit in place" warning, and has been retired in favour of
this on-demand generation. There is no longer a Section 5A table shape to
read; Section 5 is this script's only EBR-0001 source now.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_PST_PATH = REPO_ROOT / "aiems/governance/status/PST-0001_PROGRAMME_STATUS.md"
DEFAULT_EBR_PATH = REPO_ROOT / "aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md"
DEFAULT_JRM_PATH = REPO_ROOT / "aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md"

_RESOLVED_MARKERS = ("resolved", "complete", "delivered", "closed", "superseded")
_OPEN_BACKLOG_STATUSES = ("Approved Backlog", "Candidate Backlog")
_PRIORITY_ORDER = ("High", "Medium", "Low")

_TRACK_HEADINGS = {
    "Track A": re.compile(r"(?m)^##\s*6\.1\s+Near-term\s*$"),
    "Track B": re.compile(r"(?m)^##\s*7\.1\s+Near-term\s*$"),
    "Track C": re.compile(r"(?m)^##\s*8\.2\s+Near-term\s*$"),
}
_SECTION_END_PATTERN = re.compile(r"(?m)^(?:---\s*$|##\s)")
_WIKILINK_PATTERN = re.compile(r"^\[\[[^\]|]+(?:\|([^\]]+))?\]\]$")
_EBG_ID_PATTERN = re.compile(r"^EBG-\d{4}$")


class SessionLauncherError(Exception):
    """Raised when required repository structure cannot be found - never guessed past."""


@dataclass(frozen=True)
class CurrentState:
    current_mode: str
    current_baseline: str
    next_wp_candidate: str


@dataclass(frozen=True)
class BacklogItem:
    id: str
    title: str
    status: str
    priority: str
    description: str


@dataclass(frozen=True)
class RoadmapItem:
    track: str
    item: str
    rationale: str


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _strip_wikilink(cell: str) -> str:
    match = _WIKILINK_PATTERN.match(cell.strip())
    if match:
        return match.group(1) or cell.strip()
    return cell.strip()


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row on '|', treating [[...]] WikiLinks as atomic.

    A WikiLink's own separator (`[[Target|Display]]`) is a literal '|'
    character that must not be treated as a column boundary - naively
    splitting on every '|' fractures the row and shifts every later column
    whenever a WikiLink with display text appears in any cell, not just the
    first one.
    """

    stripped = line.strip()
    stripped = stripped.removeprefix("|")
    stripped = stripped.removesuffix("|")

    cells: list[str] = []
    current: list[str] = []
    depth = 0
    i = 0
    while i < len(stripped):
        if stripped[i : i + 2] == "[[":
            depth += 1
            current.append("[[")
            i += 2
            continue
        if stripped[i : i + 2] == "]]":
            depth = max(0, depth - 1)
            current.append("]]")
            i += 2
            continue
        char = stripped[i]
        if char == "|" and depth == 0:
            cells.append("".join(current).strip())
            current = []
            i += 1
            continue
        current.append(char)
        i += 1
    cells.append("".join(current).strip())
    return cells


def _find_row_second_cell(text: str, label: str) -> str | None:
    """Return the WikiLink-safe second cell of a `| label | ... |` row.

    Unlike a plain `\\|\\s*(.+?)\\s*\\|\\s*$` regex - correct only for
    strictly two-column rows - this handles rows with a third (or later)
    column, such as Section 8's `| Item | Notes | Status |` table, by
    locating the full row line first and then splitting it with the same
    WikiLink-aware splitter `read_high_priority_backlog` already relies on,
    rather than letting a greedy end-anchored capture swallow every column
    after the label into one string.
    """

    row_match = re.search(rf"(?m)^\|\s*{re.escape(label)}\s*\|.*\|\s*$", text)
    if row_match is None:
        return None
    cells = _split_table_row(row_match.group(0))
    return cells[1] if len(cells) > 1 else None


def read_current_state(pst_path: Path) -> CurrentState:
    """Extract PST-0001's Current Mode, Current Repository Baseline and
    Next Work Package Candidate rows."""

    text = pst_path.read_text(encoding="utf-8", errors="replace")
    current_mode = _find_row_second_cell(text, "Current Mode")
    current_baseline = _find_row_second_cell(text, "Current Repository Baseline")
    next_wp_candidate = _find_row_second_cell(text, "Next Work Package Candidate")

    missing = []
    if current_mode is None:
        missing.append("Current Mode")
    if current_baseline is None:
        missing.append("Current Repository Baseline")
    if next_wp_candidate is None:
        missing.append("Next Work Package Candidate")
    if missing:
        raise SessionLauncherError(
            f"Could not find {' and '.join(missing)} row(s) in {_display_path(pst_path)} - "
            "refusing to produce a partial report."
        )

    return CurrentState(
        current_mode=current_mode,
        current_baseline=current_baseline,
        next_wp_candidate=next_wp_candidate,
    )


def read_open_backlog(ebr_path: Path, priority: str | None = None) -> tuple[BacklogItem, ...]:
    """Return EBR-0001 Section 5 rows with Status Approved/Candidate Backlog.

    `priority`, if given, filters to that single Priority value (e.g. "High").
    Left as `None`, every open row is returned regardless of Priority - the
    basis for `generate_active_backlog_view()` (EBG-0106).
    """

    text = ebr_path.read_text(encoding="utf-8", errors="replace")
    items: list[BacklogItem] = []
    found_any_row = False

    for line in text.splitlines():
        if not line.startswith("| EBG-") and not line.startswith("| [[EBG-"):
            continue
        cells = _split_table_row(line)
        if len(cells) < 7:
            continue
        item_id = _strip_wikilink(cells[0])
        if not _EBG_ID_PATTERN.match(item_id):
            continue  # The header row ("| EBG-ID | ...") also starts with "| EBG-" but is not a data row.
        found_any_row = True
        title, status, item_priority, description = cells[1], cells[3], cells[4], cells[6]
        if status not in _OPEN_BACKLOG_STATUSES:
            continue
        if priority is not None and item_priority != priority:
            continue
        items.append(
            BacklogItem(id=item_id, title=title, status=status, priority=item_priority, description=description)
        )

    if not found_any_row:
        raise SessionLauncherError(
            f"No EBG- rows found in {_display_path(ebr_path)} - refusing to produce a partial report."
        )

    return tuple(items)


def read_high_priority_backlog(ebr_path: Path) -> tuple[BacklogItem, ...]:
    """Return EBR-0001 rows with Priority High and Status Approved/Candidate Backlog.

    A thin, backward-compatible wrapper over `read_open_backlog()`.
    """

    return read_open_backlog(ebr_path, priority="High")


def generate_active_backlog_view(items: tuple[BacklogItem, ...]) -> tuple[tuple[str, tuple[BacklogItem, ...]], ...]:
    """Group open backlog items by Priority, High -> Medium -> Low (EBG-0106).

    Mechanically derived from `read_open_backlog()`'s own Status/Priority
    fields - not a second, hand-maintained view. Replaces the retired
    EBR-0001 Section 5A theme-grouped snapshot, which drifted stale twice
    despite its own "do not edit in place" warning. Section 5 carries no
    `Theme` column, so thematic grouping is not reproduced here - only
    Priority, which is genuinely present on every row. A `Priority` value
    outside the standard three is grouped last, under "Other", rather than
    silently dropped.
    """

    by_priority: dict[str, list[BacklogItem]] = {priority: [] for priority in _PRIORITY_ORDER}
    other: list[BacklogItem] = []
    for item in items:
        if item.priority in by_priority:
            by_priority[item.priority].append(item)
        else:
            other.append(item)

    groups = [(priority, tuple(by_priority[priority])) for priority in _PRIORITY_ORDER if by_priority[priority]]
    if other:
        groups.append(("Other", tuple(other)))
    return tuple(groups)


def _is_resolved(rationale: str) -> bool:
    lowered = rationale.lower()
    return any(marker in lowered for marker in _RESOLVED_MARKERS)


def read_near_term_roadmap(jrm_path: Path) -> tuple[RoadmapItem, ...]:
    """Return open (non-resolved) rows from JRM-0001's three Near-term tables."""

    text = jrm_path.read_text(encoding="utf-8", errors="replace")
    items: list[RoadmapItem] = []
    missing_tracks: list[str] = []

    for track_name, heading_pattern in _TRACK_HEADINGS.items():
        heading_match = heading_pattern.search(text)
        if heading_match is None:
            missing_tracks.append(track_name)
            continue

        remainder = text[heading_match.end():]
        section_end_match = _SECTION_END_PATTERN.search(remainder)
        section_text = remainder[: section_end_match.start()] if section_end_match else remainder

        for line in section_text.splitlines():
            if not line.startswith("| ") or line.startswith(("|---", "|-")):
                continue
            cells = _split_table_row(line)
            if len(cells) < 2 or cells[0] == "Item":
                continue
            item_name = _strip_wikilink(cells[0])
            rationale = cells[1]
            if _is_resolved(rationale):
                continue
            items.append(RoadmapItem(track=track_name, item=item_name, rationale=rationale))

    if missing_tracks:
        raise SessionLauncherError(
            f"Could not find Near-term heading(s) for: {', '.join(missing_tracks)} in "
            f"{_display_path(jrm_path)} - refusing to produce a partial report."
        )

    return tuple(items)


def build_report(
    current_state: CurrentState,
    backlog_items: tuple[BacklogItem, ...],
    roadmap_items: tuple[RoadmapItem, ...],
    active_backlog_view: tuple[tuple[str, tuple[BacklogItem, ...]], ...],
) -> str:
    lines = ["# Session-Opening Report", ""]

    lines.append("## Current State")
    lines.append("")
    lines.append(f"**Current Mode:** {current_state.current_mode}")
    lines.append("")
    lines.append(f"**Current Repository Baseline:** {current_state.current_baseline}")
    lines.append("")
    lines.append(f"**Next Work Package Candidate:** {current_state.next_wp_candidate}")
    lines.append("")

    lines.append("## High-Priority Open Backlog (EBR-0001)")
    lines.append("")
    if backlog_items:
        for item in backlog_items:
            lines.append(f"- **{item.id}** ({item.status}): {item.title} - {item.description}")
    else:
        lines.append("_No High-priority Approved/Candidate Backlog items found._")
    lines.append("")

    lines.append("## Near-Term Roadmap Candidates (JRM-0001)")
    lines.append("")
    if roadmap_items:
        for item in roadmap_items:
            lines.append(f"- **[{item.track}] {item.item}**: {item.rationale}")
    else:
        lines.append("_No open Near-term roadmap items found._")
    lines.append("")

    lines.append("## Active Backlog View (mechanically generated from EBR-0001 Section 5 - EBG-0106)")
    lines.append("")
    if active_backlog_view:
        for priority, items in active_backlog_view:
            lines.append(f"### {priority}")
            lines.append("")
            for item in items:
                lines.append(f"- **{item.id}** ({item.status}): {item.title} - {item.description}")
            lines.append("")
    else:
        lines.append("_No open Approved/Candidate Backlog items found in EBR-0001 Section 5._")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None, help="Write the report to this path instead of stdout")
    parser.add_argument("--pst-path", type=Path, default=DEFAULT_PST_PATH)
    parser.add_argument("--ebr-path", type=Path, default=DEFAULT_EBR_PATH)
    parser.add_argument("--jrm-path", type=Path, default=DEFAULT_JRM_PATH)
    args = parser.parse_args()

    try:
        current_state = read_current_state(args.pst_path)
        backlog_items = read_high_priority_backlog(args.ebr_path)
        roadmap_items = read_near_term_roadmap(args.jrm_path)
        active_backlog_view = generate_active_backlog_view(read_open_backlog(args.ebr_path))
        report = build_report(current_state, backlog_items, roadmap_items, active_backlog_view)
    except SessionLauncherError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
