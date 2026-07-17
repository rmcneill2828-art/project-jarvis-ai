"""Tests for scripts/aiems_bridge.py (EBG-0057, EIP-ESR0025-001).

No test invokes a real claude/codex CLI process or the real automated test
suite recursively - capture_repository_ref, capture_evidence and
run_preflight are monkeypatched to fast, deterministic fakes throughout.
"""

from __future__ import annotations

import pytest

from scripts.aiems_bridge import (
    BridgeError,
    EvidenceResult,
    Handover,
    PreflightResult,
    cmd_init,
    cmd_return_findings,
    cmd_sponsor_decision,
    cmd_submit_response,
    cmd_submit_to_review,
    exchange_root,
    find_latest_sponsor_decision,
    parse_handover,
    read_transcript,
)


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


def test_submit_response_refused_without_any_sponsor_decision(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")

    with pytest.raises(BridgeError, match="no approving sponsor-decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_refused_after_rejection(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looked fine at the time")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "reject", "changed my mind")

    with pytest.raises(BridgeError, match="no approving sponsor-decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")


def test_submit_response_succeeds_after_approval_with_matching_ref(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looks good")

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert handover.type == "submit-response"
    assert any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_refused_when_validation_failed(tmp_path, _fake_head):
    """Engineering Reviewer Medium finding, addressed: a failing pytest/
    validate_repository.py run must hard-block submit-response, not merely
    be attached as evidence for a handover that still looks successful."""

    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looks good")

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


def test_submit_response_refused_when_repository_has_drifted_since_approval(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looks good")

    _fake_head["ref"] = "bbbbbbb"  # an unrelated commit landed after approval

    with pytest.raises(BridgeError, match="drifted since sponsor-decision"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert not any((exchange_root(tmp_path) / "claude" / "outbox").glob("*submit-response*"))


def test_submit_response_succeeds_after_fresh_sponsor_decision_clears_drift(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looks good")

    _fake_head["ref"] = "bbbbbbb"
    with pytest.raises(BridgeError, match="drifted"):
        cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    # A fresh sponsor-decision against the new HEAD clears the drift.
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "re-approved at new HEAD")

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")
    assert handover.type == "submit-response"


def test_submit_response_holds_lock_across_evidence_capture_against_concurrent_sponsor_decision(
    tmp_path, monkeypatch
):
    """Engineering Reviewer Medium finding (TOCTOU), addressed: the read of
    the approving sponsor-decision, the drift check and evidence capture all
    happen inside the same lock acquisition as the final write, so a
    concurrent same-WP action attempted mid-flight (here, during evidence
    capture - the slowest step) must fail against the lock rather than race
    in and silently change the approval state submit-response already read."""

    monkeypatch.setattr("scripts.aiems_bridge.capture_repository_ref", lambda repo_root: "aaaaaaa")

    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "looks good")

    concurrent_attempt = {}

    def _evidence_with_concurrent_race(repo_root):
        try:
            cmd_sponsor_decision(repo_root, "ESR-0025", "WP1", "reject", "racing in mid-flight")
            concurrent_attempt["blocked"] = False
        except BridgeError:
            concurrent_attempt["blocked"] = True
        return EvidenceResult(passed=True, text="VALIDATION: PASSED\nstub")

    monkeypatch.setattr("scripts.aiems_bridge.capture_evidence", _evidence_with_concurrent_race)

    handover = cmd_submit_response(tmp_path, "ESR-0025", "WP1", "implemented")

    assert concurrent_attempt["blocked"] is True, "concurrent sponsor-decision was not blocked by the lock"
    assert handover.type == "submit-response"

    handovers = read_transcript(tmp_path, "ESR-0025", "WP1")
    assert all(h.message != "racing in mid-flight" for h in handovers), (
        "the racing sponsor-decision must never have been recorded"
    )


def test_sponsor_decision_written_only_to_transcript_never_inbox_or_outbox(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    before = {p for p in tmp_path.rglob("*") if p.is_file()}

    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "fine")

    after = {p for p in tmp_path.rglob("*") if p.is_file()}
    new_files = after - before

    root = exchange_root(tmp_path)
    for path in new_files:
        assert (root / "transcript") in path.parents, f"unexpected non-transcript write: {path}"
        for role in ("claude", "codex"):
            for box in ("inbox", "outbox"):
                assert (root / role / box) not in path.parents


def test_find_latest_sponsor_decision_returns_most_recent():
    older = Handover(
        session="ESR-0025", work_package="WP1", type="sponsor-decision", sender="programme_sponsor",
        recipient="n/a", repository_ref="a", files_in_scope=(), programme_sponsor_authorisation=True,
        timestamp="2026-07-17T00:00:00Z", message="first",
    )
    newer = Handover(
        session="ESR-0025", work_package="WP1", type="sponsor-decision", sender="programme_sponsor",
        recipient="n/a", repository_ref="b", files_in_scope=(), programme_sponsor_authorisation=False,
        timestamp="2026-07-17T01:00:00Z", message="second",
    )

    assert find_latest_sponsor_decision([older, newer]) == newer
    assert find_latest_sponsor_decision([newer, older]) == older  # list order, not timestamp, is authoritative
    assert find_latest_sponsor_decision([]) is None


def test_read_transcript_round_trips_multiple_handovers(tmp_path, _fake_head):
    cmd_init(tmp_path, "ESR-0025", "WP1")
    cmd_submit_to_review(tmp_path, "ESR-0025", "WP1", ["a.py"], "please review")
    cmd_return_findings(tmp_path, "ESR-0025", "WP1", "looks fine")
    cmd_sponsor_decision(tmp_path, "ESR-0025", "WP1", "approve", "go ahead")

    handovers = read_transcript(tmp_path, "ESR-0025", "WP1")

    assert [h.type for h in handovers] == ["submit-to-review", "return-findings", "sponsor-decision"]


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
