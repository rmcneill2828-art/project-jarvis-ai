"""Regression tests for scripts/validate_repository.py staleness checks."""

from __future__ import annotations

import textwrap

from scripts.validate_repository import (
    ValidationResult,
    check_stale_status_references,
    extract_current_esr_reference,
    latest_accepted_baseline,
)


def test_extract_current_esr_reference_reads_current_mode_row():
    text = "| Current Mode | [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] closed. |"
    assert extract_current_esr_reference(text) == "ESR-0014"


def test_extract_current_esr_reference_ignores_negated_mentions_elsewhere():
    text = textwrap.dedent(
        """
        | Current Mode | [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] closure review prepared. |

        PST-0001 does not create ESR-0014.
        """
    )
    assert extract_current_esr_reference(text) == "ESR-0013"


def test_extract_current_esr_reference_handles_addendum_letter_suffix():
    text = "| Current Mode | [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] closed. |"
    assert extract_current_esr_reference(text) == "ESR-0014"


def test_check_stale_status_references_flags_current_mode_pointing_at_old_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    sessions_dir = tmp_path / "aiems/governance/sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "ESR-0013_ENGINEERING_SESSION_REPORT.md").write_text("ESR-0013", encoding="utf-8")
    (sessions_dir / "ESR-0014_ENGINEERING_SESSION_REPORT.md").write_text("ESR-0014", encoding="utf-8")

    status_dir = tmp_path / "aiems/governance/status"
    status_dir.mkdir(parents=True)
    status_path = status_dir / "PST-0001_PROGRAMME_STATUS.md"
    status_path.write_text(
        textwrap.dedent(
            """
            | Current Mode | [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] closure review prepared. |

            This does not create ESR-0014.
            """
        ),
        encoding="utf-8",
    )

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    result = ValidationResult(errors=[], warnings=[])
    check_stale_status_references(result)

    assert any("Current Mode references ESR-0013" in error for error in result.errors)


def test_latest_accepted_baseline_ignores_draft_status(tmp_path):
    baselines_dir = tmp_path / "aiems/governance/baselines"
    baselines_dir.mkdir(parents=True)
    (baselines_dir / "RBL-0010_REPOSITORY_BASELINE.md").write_text(
        "| Status | Accepted |", encoding="utf-8"
    )
    (baselines_dir / "RBL-0011_REPOSITORY_BASELINE.md").write_text(
        "| Status | Draft |", encoding="utf-8"
    )

    assert latest_accepted_baseline(baselines_dir) == "RBL-0010"


def test_latest_accepted_baseline_returns_none_when_nothing_accepted(tmp_path):
    baselines_dir = tmp_path / "aiems/governance/baselines"
    baselines_dir.mkdir(parents=True)
    (baselines_dir / "RBL-0001_REPOSITORY_BASELINE.md").write_text(
        "| Status | Draft |", encoding="utf-8"
    )

    assert latest_accepted_baseline(baselines_dir) is None


def test_check_stale_status_references_does_not_flag_draft_baseline_as_current(tmp_path, monkeypatch):
    """Regression test: drafting a recommended-but-unaccepted baseline must not
    itself trigger a staleness error against the still-current accepted one."""

    monkeypatch.chdir(tmp_path)

    baselines_dir = tmp_path / "aiems/governance/baselines"
    baselines_dir.mkdir(parents=True)
    (baselines_dir / "RBL-0010_REPOSITORY_BASELINE.md").write_text(
        "| Status | Accepted |", encoding="utf-8"
    )
    (baselines_dir / "RBL-0011_REPOSITORY_BASELINE.md").write_text(
        "| Status | Draft |", encoding="utf-8"
    )

    status_dir = tmp_path / "aiems/governance/status"
    status_dir.mkdir(parents=True)
    status_path = status_dir / "PST-0001_PROGRAMME_STATUS.md"
    status_path.write_text(
        textwrap.dedent(
            """
            | Current Repository Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] remains current; RBL-0011 recommended. |
            """
        ),
        encoding="utf-8",
    )

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    result = ValidationResult(errors=[], warnings=[])
    check_stale_status_references(result)

    assert result.errors == []


def test_check_stale_status_references_passes_when_current_mode_matches_latest_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    sessions_dir = tmp_path / "aiems/governance/sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "ESR-0013_ENGINEERING_SESSION_REPORT.md").write_text("ESR-0013", encoding="utf-8")
    (sessions_dir / "ESR-0014_ENGINEERING_SESSION_REPORT.md").write_text("ESR-0014", encoding="utf-8")

    status_dir = tmp_path / "aiems/governance/status"
    status_dir.mkdir(parents=True)
    status_path = status_dir / "PST-0001_PROGRAMME_STATUS.md"
    status_path.write_text(
        "| Current Mode | [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] closed. |",
        encoding="utf-8",
    )

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    result = ValidationResult(errors=[], warnings=[])
    check_stale_status_references(result)

    assert result.errors == []
