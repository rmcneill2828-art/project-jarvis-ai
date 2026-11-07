"""ESR-0061 WP6d: the Child's first-use explanation (EIP-ESR0061-006 D1), the
Administrator's safety summary (6.7) and the command-line tool that adds an
Administrator to a household with none (WP6a post-commit review, Low L1)."""

from __future__ import annotations

import sqlite3

import pytest

from jarvis.identity.store import ProfileRecord, ProfileStore, utc_now
from jarvis.tests.test_child_consent import _ConsentNetwork, _household
from jarvis.tests.test_escalation_rpc import _error_text
from jarvis.tools import add_administrator as tool


@pytest.fixture
def network(monkeypatch):
    fake = _ConsentNetwork()
    monkeypatch.setattr("urllib.request.urlopen", fake.urlopen)
    return fake


# --- the first-use explanation (D1) ---------------------------------------------------------------------------------


def test_a_child_must_see_the_explanation_once(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    client.select(child)
    status = client.result("disclosure.status")
    assert status == {"required": True, "acknowledged": False, "acknowledgedAt": None}

    acknowledged = client.result("disclosure.acknowledge")
    assert acknowledged["required"] is False and acknowledged["acknowledged"] is True
    first_time = acknowledged["acknowledgedAt"]
    # A second acknowledgement keeps the first time.
    assert client.result("disclosure.acknowledge")["acknowledgedAt"] == first_time
    assert client.result("disclosure.status")["required"] is False


def test_only_a_child_is_shown_the_explanation_and_only_a_child_acknowledges_it(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    client.select(admin)
    assert client.result("disclosure.status")["required"] is False
    assert "Only a Child profile" in _error_text(client.call("disclosure.acknowledge"))
    # The Administrator's attempt did not acknowledge it for the child.
    client.select(child)
    assert client.result("disclosure.status")["required"] is True


def test_the_explanation_is_per_child(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    second = client.result("profile.create", displayName="Ellie", role="Child")["id"]
    client.select(child)
    client.result("disclosure.acknowledge")
    client.select(second)
    assert client.result("disclosure.status")["required"] is True
    del admin


def test_the_explanation_does_not_gate_moderation(tmp_path, monkeypatch, network):
    """A disclosure, not a safety control: an unacknowledged child is still
    moderated, and an unsafe message still blocked."""

    client, _admin, child = _household(tmp_path, monkeypatch)
    client.select(child)
    network.classifier = "unsafe\nS1"
    reply = client.ask("something unsafe")
    assert reply["blocked"] is True


def test_erasing_a_child_deletes_its_acknowledgement(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    client.select(child)
    client.result("disclosure.acknowledge")
    client.select(admin)
    client.result("profile.erase", profileId=child, confirmName="Sam")
    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        assert connection.execute("SELECT COUNT(*) FROM child_disclosures").fetchone()[0] == 0


# --- the Administrator's safety summary (6.7) -----------------------------------------------------------------------


def test_the_safety_summary_counts_stopped_turns_without_any_text(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    guest = client.result("profile.create", displayName="Visitor", role="Guest")["id"]
    client.select(child)
    network.classifier = "unsafe\nS1"
    client.ask("first secret sentence")
    client.ask("second secret sentence")
    network.classifier = "unsafe\nS11"
    client.ask("third secret sentence")

    client.select(admin)
    summary = client.result("safety.summary")["profiles"]
    by_id = {entry["profileId"]: entry for entry in summary}
    # Child and Guest profiles only: the two moderated roles.
    assert set(by_id) == {child, guest}
    assert by_id[guest]["events"] == []
    events = by_id[child]["events"]
    assert {(event["category"], event["direction"], event["count"]) for event in events} == {
        ("violent_crimes", "input", 2),
        ("self_harm", "input", 1),
    }
    assert all(len(event["day"]) == 10 for event in events)
    assert "secret" not in str(summary)


def test_only_an_administrator_sees_the_safety_summary(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    adult = client.result("profile.create", displayName="Jo", role="Adult")["id"]
    for profile in (child, adult):
        client.select(profile)
        assert "Only an Administrator" in _error_text(client.call("safety.summary"))


# --- adding an Administrator to a household with none (WP6a Low L1) -------------------------------------------------


def _store_with(tmp_path, *roles):
    path = tmp_path / "identity.db"
    store = ProfileStore(path)
    for index, role in enumerate(roles):
        store.create(ProfileRecord(id=f"p{index}", display_name=f"P{index}", role=role, created_at=utc_now()))
    return path, store


def test_the_tool_adds_an_administrator_when_there_is_none(tmp_path):
    path, store = _store_with(tmp_path, "Adult", "Child")
    record = tool.add_administrator(path, "  Robert   McNeill ")
    assert record.role == "Administrator" and record.display_name == "Robert McNeill"
    assert [profile.role for profile in store.list_all()].count("Administrator") == 1


def test_the_tool_refuses_when_there_is_already_an_administrator(tmp_path):
    path, store = _store_with(tmp_path, "Administrator", "Child")
    with pytest.raises(tool.AdministratorExistsError):
        tool.add_administrator(path, "Someone")
    assert len(store.list_all()) == 2


def test_the_tool_refuses_an_empty_name_and_a_missing_household(tmp_path):
    path, _store = _store_with(tmp_path, "Adult")
    with pytest.raises(ValueError, match="empty"):
        tool.add_administrator(path, "   ")
    with pytest.raises(ValueError, match="No JARVIS household"):
        tool.add_administrator(tmp_path / "missing.db", "Robert")
    assert not (tmp_path / "missing.db").exists()


def test_the_tool_main_reports_both_outcomes(tmp_path, monkeypatch, capsys):
    path, _store = _store_with(tmp_path, "Adult")
    monkeypatch.setattr(tool, "identity_db_path", lambda: path)
    assert tool.main(["Robert"]) == 0
    assert "set the Administrator PIN" in capsys.readouterr().out
    assert tool.main(["Another"]) == 1
    assert "already has an Administrator" in capsys.readouterr().out


def test_turns_with_nobody_signed_in_are_one_more_entry_in_the_summary(tmp_path, monkeypatch, network):
    """Review Low: events with no profile (moderated as a Guest) were never
    shown. They are one entry with no profile id, only when there are any."""

    client, admin, _child = _household(tmp_path, monkeypatch)
    client.select(admin)
    assert all(entry["profileId"] is not None for entry in client.result("safety.summary")["profiles"])
    client.server._identity_service.safety_events.record(None, "hate", "input")
    summary = client.result("safety.summary")["profiles"]
    unsigned = [entry for entry in summary if entry["profileId"] is None]
    assert len(unsigned) == 1
    assert unsigned[0]["events"][0]["category"] == "hate" and unsigned[0]["events"][0]["count"] == 1


def test_the_tool_checks_and_adds_in_one_transaction(tmp_path):
    """Review Low: a second run after the first finds the Administrator."""

    path, store = _store_with(tmp_path, "Adult")
    tool.add_administrator(path, "First")
    with pytest.raises(tool.AdministratorExistsError):
        tool.add_administrator(path, "Second")
    assert [profile.display_name for profile in store.list_all() if profile.role == "Administrator"] == ["First"]


# --- the per-profile export holds the WP6 records (session-wide review, Medium M1) ----------------------------------


def test_a_childs_export_holds_its_household_safety_records_but_no_words(tmp_path, monkeypatch, network):
    import json
    from pathlib import Path

    client, admin, child = _household(tmp_path, monkeypatch)
    client.select(admin)
    client.result("consent.record", profileId=child)
    client.select(child)
    client.result("consent.acknowledge")
    client.result("disclosure.acknowledge")
    network.classifier = "unsafe\nS1"
    client.ask("a secret unsafe sentence")
    client.select(admin)
    client.result("consent.revoke", profileId=child)

    reply = client.result("profile.export", profileId=child, directory=str(tmp_path / "out"))
    portable = json.loads(Path(reply["jsonPath"]).read_text(encoding="utf-8"))
    safety = portable["householdSafety"]
    assert [(event["category"], event["direction"]) for event in safety["safetyEvents"]] == [("violent_crimes", "input")]
    assert len(safety["claudeConsents"]) == 1
    consent = safety["claudeConsents"][0]
    assert consent["recordedBy"] == "Robert" and consent["acknowledgedAt"] and consent["revokedAt"]
    assert safety["explanationAcknowledgedAt"] is not None
    markdown = Path(reply["markdownPath"]).read_text(encoding="utf-8")
    assert "## Household safety" in markdown and "violent crimes" in markdown
    assert "secret" not in markdown and "secret" not in json.dumps(portable)
