"""Tests for scripts/sponsor_client.py (ADR-0022, EIP-ESR0030-001).

The HTTP call itself is mocked here (real service round-trips are covered
by test_sponsor_approval_service.py) - these tests exercise request
construction, error handling, and the CLI's environment-variable
validation in isolation.
"""

from __future__ import annotations

import json
import urllib.error

import pytest

from scripts.sponsor_client import ClientError, main, submit_decision


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._body = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *exc_info: object) -> None:
        return None


def test_submit_decision_sends_correct_request(monkeypatch):
    captured = {}

    def _fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return _FakeResponse(
            {"session": "ESR-0030", "work_package": "WP1", "decision": "approve",
             "repository_ref": "deadbeef", "timestamp": "2026-07-19T00:00:00Z", "note": "ok"}
        )

    monkeypatch.setattr("scripts.sponsor_client.urllib.request.urlopen", _fake_urlopen)

    result = submit_decision(
        "http://127.0.0.1:8765", "sponsor-secret", "ESR-0030", "WP1", "approve", "deadbeef", "looks good"
    )

    assert captured["url"] == "http://127.0.0.1:8765/decisions"
    assert captured["method"] == "POST"
    assert captured["headers"]["Authorization"] == "Bearer sponsor-secret"
    assert captured["body"] == {
        "session": "ESR-0030",
        "work_package": "WP1",
        "decision": "approve",
        "repository_ref": "deadbeef",
        "note": "looks good",
    }
    assert result["decision"] == "approve"


def test_submit_decision_strips_trailing_slash_from_url(monkeypatch):
    captured = {}

    def _fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        return _FakeResponse({"session": "s", "work_package": "w", "decision": "approve", "repository_ref": "r", "timestamp": "t", "note": ""})

    monkeypatch.setattr("scripts.sponsor_client.urllib.request.urlopen", _fake_urlopen)

    submit_decision("http://127.0.0.1:8765/", "token", "s", "w", "approve", "r", "")

    assert captured["url"] == "http://127.0.0.1:8765/decisions"


def test_submit_decision_raises_client_error_on_http_error(monkeypatch):
    def _fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 403, "Forbidden", None, None)

    monkeypatch.setattr("scripts.sponsor_client.urllib.request.urlopen", _fake_urlopen)
    monkeypatch.setattr(
        urllib.error.HTTPError, "read", lambda self: b'{"error": "forbidden"}', raising=False
    )

    with pytest.raises(ClientError, match="HTTP 403"):
        submit_decision("http://127.0.0.1:8765", "wrong-token", "s", "w", "approve", "r", "")


def test_submit_decision_raises_client_error_on_url_error(monkeypatch):
    def _fake_urlopen(request, timeout):
        raise urllib.error.URLError("Connection refused")

    monkeypatch.setattr("scripts.sponsor_client.urllib.request.urlopen", _fake_urlopen)

    with pytest.raises(ClientError, match="Could not reach"):
        submit_decision("http://127.0.0.1:1", "token", "s", "w", "approve", "r", "")


def test_main_errors_when_sponsor_token_missing(monkeypatch, capsys):
    monkeypatch.delenv("AIEMS_SPONSOR_TOKEN", raising=False)
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")

    exit_code = main(["ESR-0030", "WP1", "--decision", "approve"])

    assert exit_code == 1
    assert "AIEMS_SPONSOR_TOKEN" in capsys.readouterr().err


def test_main_errors_when_sponsor_url_missing(monkeypatch, capsys):
    monkeypatch.setenv("AIEMS_SPONSOR_TOKEN", "sponsor-secret")
    monkeypatch.delenv("AIEMS_SPONSOR_URL", raising=False)

    exit_code = main(["ESR-0030", "WP1", "--decision", "approve"])

    assert exit_code == 1
    assert "AIEMS_SPONSOR_URL" in capsys.readouterr().err


def test_main_succeeds_and_reports_the_recorded_decision(monkeypatch, capsys):
    monkeypatch.setenv("AIEMS_SPONSOR_TOKEN", "sponsor-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr("scripts.sponsor_client.capture_repository_ref", lambda repo_root: "deadbeef")
    monkeypatch.setattr(
        "scripts.sponsor_client.submit_decision",
        lambda *args, **kwargs: {
            "session": "ESR-0030", "work_package": "WP1", "decision": "approve",
            "repository_ref": "deadbeef", "timestamp": "2026-07-19T00:00:00Z", "note": "ok",
        },
    )

    exit_code = main(["ESR-0030", "WP1", "--decision", "approve", "--note", "ok"])

    assert exit_code == 0
    assert "approve" in capsys.readouterr().out


def test_main_reports_client_error_and_exits_nonzero(monkeypatch, capsys):
    monkeypatch.setenv("AIEMS_SPONSOR_TOKEN", "sponsor-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr("scripts.sponsor_client.capture_repository_ref", lambda repo_root: "deadbeef")

    def _raise(*args, **kwargs):
        raise ClientError("Could not reach Sponsor Approval Service at http://127.0.0.1:8765: refused")

    monkeypatch.setattr("scripts.sponsor_client.submit_decision", _raise)

    exit_code = main(["ESR-0030", "WP1", "--decision", "approve"])

    assert exit_code == 1
    assert "Could not reach" in capsys.readouterr().err
