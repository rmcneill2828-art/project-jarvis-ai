"""AIEMS Session-Opening Launcher (EIP-ESR0031-001).

Read-only reporting script gathering PST-0001's current state, EBR-0001's
open High-priority backlog, and JRM-0001's Near-term roadmap candidates
into one report, for WP0B objective discussion. Never writes, stages,
commits or pushes anything - the Programme Sponsor still decides the
session objective; this only reduces the manual reading required to get
there.
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


class SessionLauncherError(Exception):
    """Raised when required repository structure cannot be found - never guessed past."""


@dataclass(frozen=True)
class CurrentState:
    current_mode: str
    current_baseline: str


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
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

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


def read_current_state(pst_path: Path) -> CurrentState:
    """Extract PST-0001's Current Mode and Current Repository Baseline rows."""

    text = pst_path.read_text(encoding="utf-8", errors="replace")
    mode_match = re.search(r"(?m)^\|\s*Current Mode\s*\|\s*(.+?)\s*\|\s*$", text)
    baseline_match = re.search(r"(?m)^\|\s*Current Repository Baseline\s*\|\s*(.+?)\s*\|\s*$", text)

    missing = []
    if mode_match is None:
        missing.append("Current Mode")
    if baseline_match is None:
        missing.append("Current Repository Baseline")
    if missing:
        raise SessionLauncherError(
            f"Could not find {' and '.join(missing)} row(s) in {_display_path(pst_path)} - "
            "refusing to produce a partial report."
        )

    return CurrentState(
        current_mode=mode_match.group(1).strip(),
        current_baseline=baseline_match.group(1).strip(),
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
            if not line.startswith("| ") or line.startswith("|---") or line.startswith("|-"):
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
) -> str:
    lines = ["# Session-Opening Report", ""]

    lines.append("## Current State")
    lines.append("")
    lines.append(f"**Current Mode:** {current_state.current_mode}")
    lines.append("")
    lines.append(f"**Current Repository Baseline:** {current_state.current_baseline}")
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
        report = build_report(current_state, backlog_items, roadmap_items)
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
