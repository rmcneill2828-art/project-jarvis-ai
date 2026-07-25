"""AIEMS Session-Opening Launcher (EIP-ESR0031-001, extended EBG-0107).

Read-only reporting script gathering PST-0001's current state (including
its Next Work Package Candidate row), EBR-0001's open High-priority
backlog and Section 5A active-backlog snapshot, and JRM-0001's Near-term
roadmap candidates into one report, for WP0B objective discussion. Never
writes, stages, commits or pushes anything - the Programme Sponsor still
decides the session objective; this only reduces the manual reading
required to get there.

EBG-0107 (ESR-0033 WP5): the two additions below - Next Work Package
Candidate and the Section 5A snapshot - were the exact gap that made
this script show nothing useful for WP0B selection even after PST-0001
and EBR-0001 had already been updated to name real candidates. Reads
Section 5A directly (its 3-column theme tables), not Section 5's own
Status/Priority fields - EBG-0106's own generation-mechanism scope,
which would let this reader be simplified or removed, remains separately
unimplemented.
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

_TRACK_HEADINGS = {
    "Track A": re.compile(r"(?m)^##\s*6\.1\s+Near-term\s*$"),
    "Track B": re.compile(r"(?m)^##\s*7\.1\s+Near-term\s*$"),
    "Track C": re.compile(r"(?m)^##\s*8\.2\s+Near-term\s*$"),
}
_SECTION_END_PATTERN = re.compile(r"(?m)^(?:---\s*$|##\s)")
_WIKILINK_PATTERN = re.compile(r"^\[\[[^\]|]+(?:\|([^\]]+))?\]\]$")
_EBG_ID_PATTERN = re.compile(r"^EBG-\d{4}$")
_SECTION_5A_HEADING_PATTERN = re.compile(r"(?m)^#\s*5A\.\s+Active Backlog View")
_TOP_LEVEL_HEADING_PATTERN = re.compile(r"(?m)^#\s+\d")
_THEME_HEADING_PATTERN = re.compile(r"(?m)^##\s+(Theme\s+\d+\s*-\s*.+?)\s*$")


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


@dataclass(frozen=True)
class ActiveBacklogItem:
    theme: str
    id: str
    priority: str
    item: str


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


def read_high_priority_backlog(ebr_path: Path) -> tuple[BacklogItem, ...]:
    """Return EBR-0001 rows with Priority High and Status Approved/Candidate Backlog."""

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
        title, status, priority, description = cells[1], cells[3], cells[4], cells[6]
        if priority == "High" and status in _OPEN_BACKLOG_STATUSES:
            items.append(
                BacklogItem(id=item_id, title=title, status=status, priority=priority, description=description)
            )

    if not found_any_row:
        raise SessionLauncherError(
            f"No EBG- rows found in {_display_path(ebr_path)} - refusing to produce a partial report."
        )

    return tuple(items)


def read_active_backlog_snapshot(ebr_path: Path) -> tuple[ActiveBacklogItem, ...]:
    """Return EBR-0001 Section 5A's active-backlog snapshot, grouped by theme.

    Reads Section 5A's own 3-column `| ID | Priority | Item |` theme tables
    directly - not Section 5's Status/Priority fields (EBG-0106's own
    separate, still-unimplemented generation-mechanism scope). A theme with
    no open items (e.g. "fully delivered, no open items remain") legitimately
    has no table at all and contributes zero items, not an error.
    """

    text = ebr_path.read_text(encoding="utf-8", errors="replace")
    section_match = _SECTION_5A_HEADING_PATTERN.search(text)
    if section_match is None:
        raise SessionLauncherError(
            f"Could not find Section 5A heading in {_display_path(ebr_path)} - refusing to produce a partial report."
        )

    remainder = text[section_match.end():]
    next_heading_match = _TOP_LEVEL_HEADING_PATTERN.search(remainder)
    section_text = remainder[: next_heading_match.start()] if next_heading_match else remainder

    theme_headings = list(_THEME_HEADING_PATTERN.finditer(section_text))
    if not theme_headings:
        raise SessionLauncherError(
            f"No Theme headings found in Section 5A of {_display_path(ebr_path)} - refusing to produce a partial report."
        )

    items: list[ActiveBacklogItem] = []
    for index, heading_match in enumerate(theme_headings):
        theme_name = heading_match.group(1).strip()
        start = heading_match.end()
        end = theme_headings[index + 1].start() if index + 1 < len(theme_headings) else len(section_text)
        theme_body = section_text[start:end]

        for line in theme_body.splitlines():
            if not line.startswith("|") or line.startswith(("|---", "|-")):
                continue
            cells = _split_table_row(line)
            if len(cells) < 3:
                continue
            item_id = _strip_wikilink(cells[0])
            if not _EBG_ID_PATTERN.match(item_id):
                continue  # Skips the "| ID | Priority | Item |" header row too.
            items.append(ActiveBacklogItem(theme=theme_name, id=item_id, priority=cells[1], item=cells[2]))

    return tuple(items)


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
    active_backlog_items: tuple[ActiveBacklogItem, ...],
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

    lines.append("## Active Backlog Snapshot (EBR-0001 Section 5A)")
    lines.append("")
    if active_backlog_items:
        themes_in_order: list[str] = []
        by_theme: dict[str, list[ActiveBacklogItem]] = {}
        for item in active_backlog_items:
            if item.theme not in by_theme:
                themes_in_order.append(item.theme)
                by_theme[item.theme] = []
            by_theme[item.theme].append(item)
        for theme in themes_in_order:
            lines.append(f"### {theme}")
            lines.append("")
            for item in by_theme[theme]:
                lines.append(f"- **{item.id}** ({item.priority}): {item.item}")
            lines.append("")
    else:
        lines.append("_No active-backlog items found in Section 5A._")
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
        active_backlog_items = read_active_backlog_snapshot(args.ebr_path)
        report = build_report(current_state, backlog_items, roadmap_items, active_backlog_items)
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
