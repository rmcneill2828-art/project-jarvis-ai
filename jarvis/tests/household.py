"""Test helper: set up a household the way the app now requires (ESR-0061 WP6a).

Since WP6a, a profile after the first can only be added by an Administrator
with a PIN set, and leaving a Child or Guest profile (or a fresh start) for an
Adult or Administrator needs the PIN. Tests that only want "a profile with
role X, signed in" use `join_household`, which does it the real way: the
first profile is an Administrator, a PIN is set, the Administrator adds the
member, and the member is selected with the PIN. `switch_to` passes the PIN on
every switch; it is ignored where the rule does not need it.
"""

from __future__ import annotations

import json
from typing import Any

TEST_PIN = "246810"
HOUSEHOLD_ADMIN_NAME = "Household admin"


def rpc(server, method: str, **params: Any) -> dict[str, Any]:
    """Call one method; return its result, failing the test on an error."""

    reply = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))
    assert "error" not in reply, f"{method} failed: {reply['error']}"
    return reply["result"]


def _administrator_id(server) -> str | None:
    for profile in rpc(server, "profile.list")["profiles"]:
        if profile["role"] == "Administrator":
            return profile["id"]
    return None


def switch_to(server, profile_id: str) -> dict[str, Any]:
    """Select a profile, giving the PIN in case the rule asks for it."""

    return rpc(server, "profile.select", profileId=profile_id, pin=TEST_PIN)


def ensure_administrator_with_pin(server, name: str = HOUSEHOLD_ADMIN_NAME) -> str:
    """The household's Administrator, signed in, with `TEST_PIN` set; created
    as the first profile when the household is empty."""

    admin_id = _administrator_id(server)
    if admin_id is None:
        admin_id = rpc(server, "profile.create", displayName=name, role="Administrator")["id"]
    switch_to(server, admin_id)
    if not rpc(server, "pin.status")["set"]:
        rpc(server, "pin.set", pin=TEST_PIN)
    return admin_id


def join_household(server, name: str, role: str) -> str:
    """Add a profile with `role` and sign in as it; return its id. The very
    first Administrator asked for becomes the household's Administrator
    itself, so a test asking for one Administrator gets exactly one."""

    if role == "Administrator" and _administrator_id(server) is None:
        return ensure_administrator_with_pin(server, name)
    ensure_administrator_with_pin(server)
    created = rpc(server, "profile.create", displayName=name, role=role)["id"]
    switch_to(server, created)
    return created
