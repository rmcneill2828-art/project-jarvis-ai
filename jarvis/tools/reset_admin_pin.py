"""Remove a forgotten Administrator PIN (ESR-0061 WP6a, EIP-ESR0061-006 P5).

    python -m jarvis.tools.reset_admin_pin

There is no reset inside the app: that would be a way round the PIN for the
very person it exists to stop. This is run on the computer by someone who can
already open its files. It removes the PIN, says so on the console, and
leaves a notice in the identity database that the next Administrator sign-in shows ("the PIN
was reset on (date)"), so a reset is never silent.

What it does not protect against, stated plainly: anyone who can run a command
as the household's operating-system user can run this, including a child on a
shared, unlocked account. The PIN is a control inside the app, not a defence
against the operating-system account; the notice is how a reset is noticed.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from jarvis.identity.admin_pin import AdminPin
from jarvis.identity.store import ProfileStore

logger = logging.getLogger(__name__)


def identity_db_path() -> Path:
    """The identity database the backend uses, read from the backend's own
    settings (`stdio_rpc.py`) so the two can never point at different files."""

    from jarvis.interfaces import (
        stdio_rpc,
    )

    override = os.environ.get(stdio_rpc.IDENTITY_DB_PATH_ENV_VAR)
    return Path(override) if override else stdio_rpc.DEFAULT_IDENTITY_DB_PATH


def reset(db_path: Path) -> bool:
    """Remove the PIN; return whether there was one."""

    if not db_path.exists():
        return False
    return AdminPin(ProfileStore(db_path)).reset()


def main(argv: list[str] | None = None) -> int:
    del argv  # no options: one action, nothing to configure
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    db_path = identity_db_path()
    if reset(db_path):
        logger.warning("The Administrator PIN was removed (%s).", db_path)
        print(
            "The Administrator PIN has been removed. The next Administrator to sign in will be told it was reset.\n"
            "Set a new PIN in JARVIS under Settings."
        )
    else:
        print("No Administrator PIN was set, so nothing was changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
