"""Tests for scripts/sponsor_approval_service.py (ADR-0022, EIP-ESR0030-001).

Real socket-based tests against the actual ThreadingHTTPServer bound to an
ephemeral localhost port, per this project's live-verification-over-mocks-
alone precedent - the auth/routing/persistence properties this service
exists for are only genuinely proven by real HTTP requests, not by calling
handler methods directly.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request

import pytest

from scripts.sponsor_approval_service import DecisionRecord, DecisionStore, build_server


@pytest.fixture
def _service(tmp_path):
    server = build_server(
        host="127.0.0.1",
        port=0,  # let the OS pick a free port
        db_path=tmp_path / "sponsor_decisions.db",
        agent_token="agent-secret",
        sponsor_token="sponsor-secret",
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    try:
        yield base_url
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _get(base_url: str, session: str, work_package: str, token: str | None) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"{base_url}/decisions/latest?session={session}&work_package={work_package}"
    )
    if token is not None:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def _post(base_url: str, body: dict, token: str | None) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"{base_url}/decisions",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    if token is not None:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_get_returns_null_decision_when_none_recorded(_service):
    status, payload = _get(_service, "ESR-0030", "WP1", "agent-secret")

    assert status == 200
    assert payload == {"decision": None, "repository_ref": None, "timestamp": None, "note": None}


def test_get_requires_bearer_token(_service):
    status, _ = _get(_service, "ESR-0030", "WP1", None)

    assert status == 401


def test_get_rejects_wrong_token(_service):
    status, _ = _get(_service, "ESR-0030", "WP1", "not-the-real-token")

    assert status == 403


def test_get_rejects_sponsor_token_presented_on_the_read_route(_service):
    """The sponsor (write) token must not also work as a read credential -
    the two roles are separate capabilities, not a tiered single secret."""

    status, _ = _get(_service, "ESR-0030", "WP1", "sponsor-secret")

    assert status == 403


def test_post_creates_decision_and_get_returns_it(_service):
    post_status, post_payload = _post(
        _service,
        {
            "session": "ESR-0030",
            "work_package": "WP1",
            "decision": "approve",
            "repository_ref": "deadbeef",
            "note": "looks good",
        },
        "sponsor-secret",
    )

    assert post_status == 201
    assert post_payload["decision"] == "approve"
    assert post_payload["repository_ref"] == "deadbeef"

    get_status, get_payload = _get(_service, "ESR-0030", "WP1", "agent-secret")

    assert get_status == 200
    assert get_payload["decision"] == "approve"
    assert get_payload["repository_ref"] == "deadbeef"
    assert get_payload["note"] == "looks good"


def test_post_requires_sponsor_token(_service):
    status, _ = _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "approve", "repository_ref": "deadbeef", "note": ""},
        None,
    )

    assert status == 401


def test_post_rejects_agent_token_presented_on_the_write_route(_service):
    """Implementation Requirement 2/3: the agent (read) token must never be
    accepted on the write route, even though it is a valid token for this
    service in general."""

    status, _ = _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "approve", "repository_ref": "deadbeef", "note": ""},
        "agent-secret",
    )

    assert status == 403


def test_post_rejects_invalid_decision_value(_service):
    status, _ = _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "maybe", "repository_ref": "deadbeef", "note": ""},
        "sponsor-secret",
    )

    assert status == 400


def test_post_rejects_invalid_session_identifier(_service):
    status, _ = _post(
        _service,
        {
            "session": "../../escape",
            "work_package": "WP1",
            "decision": "approve",
            "repository_ref": "deadbeef",
            "note": "",
        },
        "sponsor-secret",
    )

    assert status == 400


def test_post_rejects_missing_repository_ref(_service):
    status, _ = _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "approve", "repository_ref": "", "note": ""},
        "sponsor-secret",
    )

    assert status == 400


def test_multiple_decisions_get_returns_latest(_service):
    _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "approve", "repository_ref": "first", "note": "1"},
        "sponsor-secret",
    )
    _post(
        _service,
        {"session": "ESR-0030", "work_package": "WP1", "decision": "reject", "repository_ref": "second", "note": "2"},
        "sponsor-secret",
    )

    _, payload = _get(_service, "ESR-0030", "WP1", "agent-secret")

    assert payload["decision"] == "reject"
    assert payload["repository_ref"] == "second"


def test_get_route_never_creates_a_record_regardless_of_repeated_calls(_service):
    """Structural confirmation of Implementation Requirement 3: do_GET has
    no code path reaching store.record - calling GET repeatedly, including
    with the sponsor token, must never change what a subsequent GET with
    the agent token reports."""

    for token in ("agent-secret", "sponsor-secret", "wrong-token", None):
        _get(_service, "ESR-0030", "WP1", token)

    _, payload = _get(_service, "ESR-0030", "WP1", "agent-secret")
    assert payload == {"decision": None, "repository_ref": None, "timestamp": None, "note": None}


def test_decisions_persist_across_store_reopen(tmp_path):
    """ADR-0022 Decision item 5: the database must be durable across
    restarts - reopening the same file as a fresh DecisionStore (simulating
    a service restart) must still see prior decisions, not lose them."""

    db_path = tmp_path / "sponsor_decisions.db"
    first_store = DecisionStore(db_path)
    first_store.record(
        DecisionRecord(
            session="ESR-0030",
            work_package="WP1",
            decision="approve",
            repository_ref="deadbeef",
            note="looks good",
            timestamp="2026-07-19T00:00:00Z",
        )
    )

    reopened_store = DecisionStore(db_path)
    latest = reopened_store.latest("ESR-0030", "WP1")

    assert latest is not None
    assert latest.decision == "approve"
    assert latest.repository_ref == "deadbeef"
