"""Tests for scripts/aiems_bridge.py (EBG-0057, EIP-ESR0025-001; sponsor
approval moved to a remote service per ADR-0022/EIP-ESR0030-001).

No test invokes a real claude/codex CLI process or the real automated test
suite recursively - capture_repository_ref, capture_evidence and
run_preflight are monkeypatched to fast, deterministic fakes throughout.
fetch_latest_decision is monkeypatched away for cmd_submit_response's own
tests (below), so no test starts a real Sponsor Approval Service for those
(that live integration is covered by test_sponsor_approval_service.py
instead) - but fetch_latest_decision's own JSON-parsing/malformed-response
logic is exercised directly, with only urllib.request.urlopen mocked, in
the dedicated section near the bottom of this file.
"""

from __future__ import annotations

import json

import pytest

from scripts.aiems_bridge import (
    BridgeError,
    EvidenceResult,
    Handover,
    PreflightResult,
    RemoteDecision,
    cmd_init,
    cmd_return_findings,
    cmd_submit_response,
    cmd_submit_to_review,
    exchange_root,
    fetch_latest_decision,
    parse_handover,
    read_transcript,
)
from scripts.aiems_bridge import run_preflight as _real_run_preflight


@pytest.fixture(autouse=True)
def _fast_preflight(monkeypatch):
    monkeypatch.setattr("scripts.aiems_bridge.run_preflight", lambda: PreflightResult(ok=True, details="ok"))


@pytest.fixture
def _fake_head(monkeypatch):
    """Returns a mutable holder so tests can change the 'current HEAD' and
    validation outcome mid-test."""

    state = {"ref": "aaaaaaa", "evidence_passed": True}
    monkeypatch.setattr("scripts.aiems_bridge.capture_repository_ref", lambda repo_root: state["ref"])
    monkeypatch.setattr(
        "scripts.aiems_bridge.capture_evidence",
        lambda repo_root: EvidenceResult(
            passed=state["evidence_passed"],
            text=f"VALIDATION: {'PASSED' if state['evidence_passed'] else 'FAILED'}\nevidence-stub",
        ),
    )
    return state


@pytest.fixture
def _fake_decision(monkeypatch):
    """Returns a mutable holder so tests can change what the Sponsor
    Approval Service would return for fetch_latest_decision, without a
    real running service (that integration is covered separately in
    test_sponsor_approval_service.py)."""

    state = {"decision": None}
    monkeypatch.setattr(
        "scripts.aiems_bridge.fetch_latest_decision",
        lambda session, work_package: state["decision"],
    )
    return state


def test_handover_render_parse_round_trip():
    handover = Handover(
        session="ESR-0025",
        work_package="WP1",
        type="submit-to-review",
        sender="claude",
        recipient="codex",
        repository_ref="deadbeef",
        files_in_scope=("a.py", "b.py"),
        programme_sponsor_authorisation=None,
        timestamp="2026-07-17T00:00:00Z",
        message="please review",
        evidence="pytest ok",
    )

    parsed = parse_handover(handover.render())

    assert parsed == handover


def test_handover_render_parse_round_trip_with_authorisation_and_no_evidence():
    """programme_sponsor_authorisation and the "sponsor-decision" type
    string remain parseable even though no current command writes them -
    historical transcripts from before ADR-0022/EIP-ESR0030-001 still
    contain entries shaped exactly like this, and parse_handover must keep
    reading them correctly."""

    handover = Handover(
        session="ESR-0025",
        work_package="WP1",
        type="sponsor-decision",
        sender="programme_sponsor",
        recipient="n/a",
        repository_ref="deadbeef",
        files_in_scope=(),
        programme_sponsor_authorisation=True,
        timestamp="2026-07-17T00:00:00Z",
        message="approved",
    )

    parsed = parse_handover(handover.render())

    assert parsed == handover


def test_init_creates_layout_and_empty_transcript(tmp_path):
    cmd_init(tmp_path, "ESR-0025", "WP1")

    root = exchange_root(tmp_path)
    for sub in ("claude/inbox", "claude/outbox", "codex/inbox", "codex/outbox", "transcript", ".locks"):
        assert (root / sub).is_dir()
    assert (root / "transcript" / "ESR-0025-WP1.md").exists()


def test_init_refuses_to_overwrite_existing_work_package(tmp_path):
    cmd_init(tmp_path, "ESR-0025", "WP1")

    with pytest.raises(BridgeError):
        cmd_init(tmp_path, "ESR-0025", "WP1")


@pytest.mark.parametrize(
    "session,work_package",
    [
        ("../../escape", "WP1"),
        ("ESR-0025", "../../escape"),
        ("ESR/0025", "WP1"),
        ("ESR-0025", "WP1/../../etc"),
        ("ESR-0025", "WP1\\..\\..\\escape"),
        ("", "WP1"),
    ],
)
def test_init_rejects_path_traversal_in_identifiers(tmp_path, session, work_package):
    """Engineering Reviewer High finding, addressed: session/work_package fed
    unsanitised into transcript/lock paths could otherwise escape
    .aiems-exchange/ entirely."""

    with pytest.raises(BridgeError):
        cmd_init(tmp_path, session, work_package)

    # No file should have been written anywhere, in or outside .aiems-exchange/.
    assert not any(p for p in tmp_path.rglob("*") if p.is_file())


def test_return_findings_rejects_path_traversal_in_identifiers(tmp_path, _fake_head):
    """Same protection must hold for return-findings specifically, since
    that is Codex's only command and the one this property matters most
    for."""

    cmd_init(tmp_path, "ESR-0025", "WP1")
    before = {p for p in tmp_path.rglob("*") if p.is_file()}

    with pytest.raises(BridgeError):
        cmd_return_findings(tmp_path, "ESR-0025", "../../escape", "looks fine")

    after = {p for p in tmp_path.rglob("*") if p.is_file()}
    assert after == before


def test_return_findings_writes_only_inside_exchange_directory(tmp_path, _fake_head):
    """Structural test for Constraint 1: return-findings takes no file-path
    argument, so every file it touches must resolve under .aiems-exchange/."""

    cmd_init(tmp_path, "ESR-0025", "WP1")
    before = {p for p in tmp_path.rglob("*") if p.is_file()}

    cmd_return_findings(tmp_path, "ESR-0025", "WP1", "looks fine")

    after = {p for p in tmp_path.rglob("*") if p.is_file()}
    new_files = after - before
    assert new_files, "expected return-findings to write at least one file"
    exchange = exchange_root(tmp_path)
    assert all(exchange in path.parents for path in new_files)


def test_submit_response_refused_without_any_sponsor_decision(tmp_path, _fake_head, _fake_decision):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")

    with pytest.raises(BridgeError, match="no approving decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_refused_after_rejection(tmp_path, _fake_head, _fake_decision):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    _fake_decision["decision"] = RemoteDecision(
        decision="reject", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="changed my mind"
    )

    with pytest.raises(BridgeError, match="no approving decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")


def test_submit_response_succeeds_after_approval_with_matching_ref(tmp_path, _fake_head, _fake_decision):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="looks good"
    )

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert handover.type == "submit-response"
    assert any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_refused_when_validation_failed(tmp_path, _fake_head, _fake_decision):
    """Engineering Reviewer Medium finding, addressed: a failing pytest/
    validate_repository.py run must hard-block submit-response, not merely
    be attached as evidence for a handover that still looks successful."""

    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="looks good"
    )

    _fake_head["evidence_passed"] = False

    with pytest.raises(BridgeError, match="validation failed"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_to_review_not_blocked_by_failing_validation_but_marks_it(tmp_path, _fake_head):
    """submit-to-review stays non-blocking (submitting known-broken WIP for
    review is legitimate) but the evidence text must make failure
    unmissable."""

    cmd_init(tmp_path, "ESR-0025", "WP1")
    _fake_head["evidence_passed"] = False

    handover = cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review, tests are red")

    assert handover.evidence is not None
    assert handover.evidence.startswith("VALIDATION: FAILED")


def test_submit_response_refused_when_repository_has_drifted_since_approval(tmp_path, _fake_head, _fake_decision):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="looks good"
    )

    _fake_head["ref"] = "bbbbbbb"  # an unrelated commit landed after approval

    with pytest.raises(BridgeError, match="drifted since the approved decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_succeeds_after_fresh_sponsor_decision_clears_drift(tmp_path, _fake_head, _fake_decision):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="looks good"
    )

    _fake_head["ref"] = "bbbbbbb"
    with pytest.raises(BridgeError, match="drifted"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    # A fresh decision recorded against the new HEAD clears the drift.
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="bbbbbbb", timestamp="2026-07-19T01:00:00Z", note="re-approved at new HEAD"
    )

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")
    assert handover.type == "submit-response"


def test_submit_response_refused_when_service_unreachable(tmp_path, _fake_head, monkeypatch):
    """ADR-0022 Decision item 4: an unreachable Sponsor Approval Service
    must refuse the response, never fall back to any local approval path."""

    def _unreachable(session, work_package):
        msg = "Sponsor Approval Service unreachable at http://127.0.0.1:1: [Errno 111] Connection refused"
        raise BridgeError(msg)

    monkeypatch.setattr("scripts.aiems_bridge.fetch_latest_decision", _unreachable)

    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")

    with pytest.raises(BridgeError, match="unreachable"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_holds_lock_across_evidence_capture_against_concurrent_invocation(
    tmp_path, monkeypatch, _fake_decision
):
    """Engineering Reviewer Medium finding (TOCTOU), addressed originally
    against the file-based sponsor-decision command this replaced: the
    fetch of the approving decision, the drift check and evidence capture
    all happen inside the same lock acquisition as the final write, so a
    concurrent same-WP bridge operation attempted mid-flight (here, during
    evidence capture - the slowest step) must fail against the lock rather
    than race in."""

    monkeypatch.setattr("scripts.aiems_bridge.capture_repository_ref", lambda repo_root: "aaaaaaa")
    _fake_decision["decision"] = RemoteDecision(
        decision="approve", repository_ref="aaaaaaa", timestamp="2026-07-19T00:00:00Z", note="looks good"
    )

    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")

    concurrent_attempt = {}

    def _evidence_with_concurrent_race(repo_root):
        from scripts.aiems_bridge import work_package_lock

        try:
            with work_package_lock(repo_root, "ESR-0025", "WP1"):
                pass
            concurrent_attempt["blocked"] = False
        except BridgeError:
            concurrent_attempt["blocked"] = True
        return EvidenceResult(passed=True, text="VALIDATION: PASSED\nstub")

    monkeypatch.setattr("scripts.aiems_bridge.capture_evidence", _evidence_with_concurrent_race)

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert concurrent_attempt["blocked"] is True, "concurrent same-WP operation was not blocked by the lock"
    assert handover.type == "submit-response"


def test_read_transcript_round_trips_multiple_handovers(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_return_findings(tmp_path, "ESR-0025", "WP1", "looks fine")

    handovers = read_transcript(tmp_path, "ESR-0025", "WP1")

    assert [h.type for h in handovers] == ["submit-to-review", "return-findings"]


def test_work_package_lock_prevents_concurrent_reentry(tmp_path, _fake_head):
    from scripts.aiems_bridge import work_package_lock

    cmd_init(tmp_path, "ESR-0025", "WP1")
    with work_package_lock(tmp_path, "ESR-0025", "WP1"):
        with pytest.raises(BridgeError):
            with work_package_lock(tmp_path, "ESR-0025", "WP1"):
                pass


def test_preflight_failure_blocks_submit_to_review_before_any_write(tmp_path, monkeypatch, _fake_head):
    monkeypatch.setattr(
        "scripts.aiems_bridge.run_preflight",
        lambda: PreflightResult(ok=False, details="codex: NOT FOUND on PATH"),
    )
    cmd_init(tmp_path, "ESR-0025", "WP1")

    with pytest.raises(BridgeError, match="Preflight failed"):
        cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")

    assert not any((exchange_root(tmp_path) / "codex" / "inbox").glob("*"))


def test_run_preflight_invokes_subprocess_with_shell_true_on_windows(monkeypatch):
    """On Windows, npm installs global CLI tools (claude, codex) as .CMD shim
    files - subprocess.run([...]) without shell=True raises FileNotFoundError
    (WinError 2) even when shutil.which finds the tool, since CreateProcess
    cannot launch a .CMD file directly. Confirmed live: preflight crashed with
    both tools genuinely installed and on PATH until shell=True was added."""
    import sys as _sys

    import scripts.aiems_bridge as bridge

    calls: list[tuple[list[str], bool]] = []

    def _fake_which(tool: str) -> str:
        return f"/fake/{tool}"

    def _fake_run(args, **kwargs):
        calls.append((list(args), kwargs.get("shell", False)))

        class _Result:
            stdout = "ok"
            stderr = ""

        return _Result()

    monkeypatch.setattr(bridge.shutil, "which", _fake_which)
    monkeypatch.setattr(bridge.subprocess, "run", _fake_run)

    # The file's autouse _fast_preflight fixture replaces run_preflight
    # itself with a stub for every test; call the real implementation via
    # the reference captured at import time, before that fixture patches it.
    result = _real_run_preflight()

    assert result.ok is True
    expected_shell = _sys.platform == "win32"
    assert all(shell == expected_shell for _, shell in calls)
    assert ["claude", "--version"] in [args for args, _ in calls]
    assert ["codex", "--version"] in [args for args, _ in calls]
    assert ["codex", "login", "status"] in [args for args, _ in calls]


# --- fetch_latest_decision's own JSON handling, mocking only urlopen ---
# (cmd_submit_response's tests above monkeypatch fetch_latest_decision
# itself, so they never exercise this parsing logic - these tests do.)


class _FakeResponse:
    def __init__(self, payload_bytes: bytes) -> None:
        self._payload_bytes = payload_bytes

    def read(self) -> bytes:
        return self._payload_bytes

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *exc_info: object) -> None:
        return None


def test_fetch_latest_decision_returns_none_for_valid_null_decision(monkeypatch):
    monkeypatch.setenv("AIEMS_AGENT_TOKEN", "agent-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr(
        "scripts.aiems_bridge.urllib.request.urlopen",
        lambda request, timeout: _FakeResponse(
            json.dumps({"decision": None, "repository_ref": None, "timestamp": None, "note": None}).encode()
        ),
    )

    assert fetch_latest_decision("ESR-0030", "WP1") is None


def test_fetch_latest_decision_returns_record_for_a_real_decision(monkeypatch):
    monkeypatch.setenv("AIEMS_AGENT_TOKEN", "agent-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr(
        "scripts.aiems_bridge.urllib.request.urlopen",
        lambda request, timeout: _FakeResponse(
            json.dumps(
                {"decision": "approve", "repository_ref": "deadbeef", "timestamp": "2026-07-19T00:00:00Z", "note": "ok"}
            ).encode()
        ),
    )

    result = fetch_latest_decision("ESR-0030", "WP1")

    assert result == RemoteDecision(
        decision="approve", repository_ref="deadbeef", timestamp="2026-07-19T00:00:00Z", note="ok"
    )


@pytest.mark.parametrize("malformed_payload", [[], "just a string", 42, True])
def test_fetch_latest_decision_raises_on_non_dict_payload(monkeypatch, malformed_payload):
    """Engineering Reviewer Low finding, addressed: a non-dict JSON response
    (e.g. a bare list) must be treated as a malformed service response, not
    silently folded into the same 'no decision recorded' case a genuine
    {"decision": null, ...} reply represents."""

    monkeypatch.setenv("AIEMS_AGENT_TOKEN", "agent-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr(
        "scripts.aiems_bridge.urllib.request.urlopen",
        lambda request, timeout: _FakeResponse(json.dumps(malformed_payload).encode()),
    )

    with pytest.raises(BridgeError, match="malformed response"):
        fetch_latest_decision("ESR-0030", "WP1")


@pytest.mark.parametrize(
    "inconsistent_null_payload",
    [
        {"decision": None, "repository_ref": "deadbeef", "timestamp": None, "note": None},
        {"decision": None, "repository_ref": None, "timestamp": "2026-07-19T00:00:00Z", "note": None},
        {"decision": None, "repository_ref": None, "timestamp": None, "note": "unexpected"},
        {"decision": None},
    ],
)
def test_fetch_latest_decision_raises_on_inconsistent_null_decision_shape(monkeypatch, inconsistent_null_payload):
    """Engineering Reviewer follow-up Low finding, addressed: a dict with
    decision: null must match the service's actual emitted shape exactly
    (every other field also null) to be treated as a genuine absence of
    approval - any other field being non-null (or simply missing) means
    the response doesn't match what sponsor_approval_service.py's do_GET
    actually emits, and must be treated as malformed instead."""

    monkeypatch.setenv("AIEMS_AGENT_TOKEN", "agent-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr(
        "scripts.aiems_bridge.urllib.request.urlopen",
        lambda request, timeout: _FakeResponse(json.dumps(inconsistent_null_payload).encode()),
    )

    with pytest.raises(BridgeError, match="malformed response"):
        fetch_latest_decision("ESR-0030", "WP1")


def test_fetch_latest_decision_raises_on_dict_missing_required_fields(monkeypatch):
    """A decision value present but the record otherwise incomplete (e.g.
    missing repository_ref) must also be treated as malformed, not
    partially trusted."""

    monkeypatch.setenv("AIEMS_AGENT_TOKEN", "agent-secret")
    monkeypatch.setenv("AIEMS_SPONSOR_URL", "http://127.0.0.1:8765")
    monkeypatch.setattr(
        "scripts.aiems_bridge.urllib.request.urlopen",
        lambda request, timeout: _FakeResponse(json.dumps({"decision": "approve"}).encode()),
    )

    with pytest.raises(BridgeError, match="malformed response"):
        fetch_latest_decision("ESR-0030", "WP1")


def test_fetch_latest_decision_raises_when_tokens_or_url_missing(monkeypatch):
    monkeypatch.delenv("AIEMS_AGENT_TOKEN", raising=False)
    monkeypatch.delenv("AIEMS_SPONSOR_URL", raising=False)

    with pytest.raises(BridgeError, match="must both be set"):
        fetch_latest_decision("ESR-0030", "WP1")
