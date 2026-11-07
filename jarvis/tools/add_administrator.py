"""Add an Administrator to a household that has none (ESR-0061 WP6d; WP6a
post-commit review, Low L1).

    python -m jarvis.tools.add_administrator "Name"

A household set up before WP6a may have profiles but no Administrator. Then
nobody can add a profile or set the PIN, because both need an Administrator
signed in, and the first-profile rule only covers an empty household. There
is deliberately no way to do this inside the app: anyone signed in there,
including a child, could use it.

This is run on the computer, by someone who can already open its files, like
`reset_admin_pin`. It adds one Administrator profile **only when the
household has none**, and refuses otherwise, so it can never be used to add a
second Administrator behind the first one's back. The new Administrator then
sets the PIN in Settings.

The same limit as the PIN reset applies, stated plainly: anyone who can run a
command as the household's operating-system user can run this. A household
with no Administrator has no PIN, so this gives nothing the app did not
already leave open.
"""

from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

from jarvis.identity.store import ProfileRecord, ProfileStore, utc_now
from jarvis.tools.reset_admin_pin import identity_db_path


class AdministratorExistsError(Exception):
    """The household already has an Administrator, so nothing was added."""


def add_administrator(db_path: Path, display_name: str) -> ProfileRecord:
    """Add one Administrator profile; refuse if one already exists."""

    name = " ".join(display_name.split())
    if not name:
        msg = "The name must not be empty."
        raise ValueError(msg)
    if not db_path.exists():
        # A new household makes its first Administrator in the app itself.
        msg = "No JARVIS household was found on this computer, so nothing was changed."
        raise ValueError(msg)
    store = ProfileStore(db_path)
    record = ProfileRecord(id=str(uuid.uuid4()), display_name=name, role="Administrator", created_at=utc_now())
    # The check and the insert in one write transaction, so two runs at once
    # cannot both find no Administrator (WP6d review, Low).
    with store.write_transaction() as connection:
        existing = connection.execute("SELECT COUNT(*) FROM profiles WHERE role = 'Administrator'").fetchone()[0]
        if existing:
            msg = "This household already has an Administrator, so nothing was changed."
            raise AdministratorExistsError(msg)
        connection.execute(
            "INSERT INTO profiles (id, display_name, role, created_at, share_memory_with_cloud) VALUES (?, ?, ?, ?, 0)",
            (record.id, record.display_name, record.role, record.created_at.isoformat()),
        )
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m jarvis.tools.add_administrator",
        description="Add an Administrator to a household that has none.",
    )
    parser.add_argument("name", help="the new Administrator's display name")
    args = parser.parse_args(argv)
    try:
        record = add_administrator(identity_db_path(), args.name)
    except (AdministratorExistsError, ValueError) as error:
        print(str(error))
        return 1
    print(
        f"Added {record.display_name} as the household's Administrator.\n"
        "Open JARVIS, choose this profile and set the Administrator PIN in Settings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
