"""A readable and a portable export of one profile's own data (ESR-0061 WP5c,
EIP-ESR0061-005 6.5, decision X1).

Two files in the folder the person chose: a Markdown summary to read and a JSON
file to keep. Contents: the profile record, that profile's OWN notes, each
with when it was agreed, and what household safety keeps about it (ESR-0061
WP6: safety events as kind, side and time, never text; Claude consents; when
the first-use explanation was acknowledged; added at the session-wide review,
Medium M1, schema version 2). Never other profiles' data, never shared household
notes (they are not the profile's), never any key, and no filename taken from
the profile's name.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

SCHEMA_VERSION = 2

_NO_SAFETY = {"safetyEvents": [], "claudeConsents": [], "explanationAcknowledgedAt": None}


def write_profile_export(
    profile, notes, directory: Path, *, safety: dict | None = None, now: datetime | None = None
) -> tuple[Path, Path]:
    """Write the two files and return their paths (Markdown, JSON).

    `profile` has id, display_name, role, created_at and share_memory_with_cloud;
    `notes` is a sequence of (record, agreed_at) where record has id, content and
    created_at. `safety` is `ProfileService.household_safety_record`.
    """

    safety = safety or _NO_SAFETY

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
        "householdSafety": {
            "safetyEvents": list(safety["safetyEvents"]),
            "claudeConsents": list(safety["claudeConsents"]),
            "explanationAcknowledgedAt": safety["explanationAcknowledgedAt"],
        },
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
    lines.extend(_safety_lines(safety))
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path, json_path


def _safety_lines(safety: dict) -> list[str]:
    events = safety["safetyEvents"]
    consents = safety["claudeConsents"]
    acknowledged = safety["explanationAcknowledgedAt"]
    lines = ["", "## Household safety", ""]
    if not events and not consents and acknowledged is None:
        lines.append("Nothing is kept about this profile by household safety.")
        return lines
    lines.append(f"Times the safety check stopped something ({len(events)}). The words are never kept.")
    for event in events:
        side = "their message" if event["direction"] == "input" else "JARVIS's reply"
        lines.append(f"- {event['at']}: {event['category'].replace('_', ' ')}, in {side}.")
    lines.extend(["", f"Permission to ask Claude ({len(consents)})."])
    for consent in consents:
        state = f"turned off {consent['revokedAt']}" if consent["revokedAt"] else "on"
        understood = consent["acknowledgedAt"] or "not yet"
        lines.append(
            f"- Allowed {consent['recordedAt']} by {consent['recordedBy']}; understood {understood}; {state}."
        )
    lines.extend(["", f"First-use explanation understood: {acknowledged or 'not yet'}."])
    return lines
