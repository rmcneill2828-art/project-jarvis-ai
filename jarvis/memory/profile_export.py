"""A readable and a portable export of one profile's own data (ESR-0061 WP5c,
EIP-ESR0061-005 6.5, decision X1).

Two files in the folder the person chose: a Markdown summary to read and a JSON
file to keep. Contents: the profile record and that profile's OWN notes, each
with when it was agreed. Never other profiles' data, never shared household
notes (they are not the profile's), never any key, and no filename taken from
the profile's name.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

SCHEMA_VERSION = 1


def write_profile_export(profile, notes, directory: Path, *, now: datetime | None = None) -> tuple[Path, Path]:
    """Write the two files and return their paths (Markdown, JSON).

    `profile` has id, display_name, role, created_at and share_memory_with_cloud;
    `notes` is a sequence of (record, agreed_at) where record has id, content and
    created_at.
    """

    moment = (now or datetime.now(UTC)).astimezone(UTC)
    stamp = moment.strftime("%Y%m%d-%H%M%S")
    directory.mkdir(parents=True, exist_ok=True)
    markdown_path = directory / f"jarvis-profile-export-{stamp}.md"
    json_path = directory / f"jarvis-profile-export-{stamp}.json"

    portable = {
        "schemaVersion": SCHEMA_VERSION,
        "exportedAt": moment.isoformat(),
        "profile": {
            "displayName": profile.display_name,
            "role": profile.role,
            "createdAt": profile.created_at.isoformat(),
            "shareNotesWithClaude": bool(profile.share_memory_with_cloud),
        },
        "notes": [
            {
                "text": record.content,
                "savedAt": record.created_at.isoformat(),
                "agreedAt": agreed_at.isoformat() if agreed_at is not None else None,
            }
            for record, agreed_at in notes
        ],
    }
    json_path.write_text(json.dumps(portable, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# JARVIS data for {profile.display_name}",
        "",
        f"Exported {moment.strftime('%d %B %Y, %H:%M')} UTC.",
        "",
        (
            "This file lists what JARVIS keeps about this profile on this computer. "
            "It does not include other profiles, notes shared by the household, or any key."
        ),
        "",
        "## Profile",
        "",
        f"- Name: {profile.display_name}",
        f"- Role: {profile.role}",
        f"- Created: {profile.created_at.strftime('%d %B %Y')}",
        f"- Notes may be sent to Claude with a question: {'yes' if profile.share_memory_with_cloud else 'no'}",
        "",
        f"## Saved notes ({len(notes)})",
        "",
    ]
    if not notes:
        lines.append("No notes are saved for this profile.")
    for index, (record, agreed_at) in enumerate(notes, start=1):
        agreed = agreed_at.strftime("%d %B %Y") if agreed_at is not None else "not recorded"
        lines.append(f"{index}. {record.content}")
        lines.append(f"   - Saved {record.created_at.strftime('%d %B %Y')}; agreed {agreed}.")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path, json_path
