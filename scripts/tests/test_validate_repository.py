"""Regression tests for scripts/validate_repository.py staleness checks."""

from __future__ import annotations

import textwrap

from scripts.validate_repository import (
    ValidationResult,
    check_stale_status_references,
    check_version_badge_table_consistency,
    extract_badge_version,
    extract_current_esr_reference,
    extract_table_version,
    iter_markdown_files,
    latest_accepted_baseline,
    latest_closed_numbered,
)


def test_iter_markdown_files_excludes_aiems_exchange(tmp_path, monkeypatch):
    """The gitignored .aiems-exchange/ directory embeds prior
    validate_repository.py output as evidence (capture_evidence in
    scripts/aiems_bridge.py) - if scanned, each run re-embeds the previous
    run's warnings, growing without bound (confirmed live: 104 -> 425 -> 1279
    warnings across three evidence captures during ESR-0026 WP1)."""

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    tracked_dir = tmp_path / "aiems/governance/registers"
    tracked_dir.mkdir(parents=True)
    (tracked_dir / "REG-0001_CONTROLLED_ARTEFACT_REGISTER.md").write_text("tracked", encoding="utf-8")

    exchange_dir = tmp_path / ".aiems-exchange/transcript"
    exchange_dir.mkdir(parents=True)
    (exchange_dir / "ESR-0026-WP1.md").write_text("ephemeral", encoding="utf-8")

    files = iter_markdown_files()

    assert any(f.name == "REG-0001_CONTROLLED_ARTEFACT_REGISTER.md" for f in files)
    assert not any(".aiems-exchange" in f.parts for f in files)


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
    (sessions_dir / "ESR-0013_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )
    (sessions_dir / "ESR-0014_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )

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
    (sessions_dir / "ESR-0013_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )
    (sessions_dir / "ESR-0014_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )

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


def test_latest_closed_numbered_ignores_open_status(tmp_path):
    sessions_dir = tmp_path / "aiems/governance/sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "ESR-0016_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )
    (sessions_dir / "ESR-0017_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Open |", encoding="utf-8"
    )

    assert latest_closed_numbered("ESR", sessions_dir) == "ESR-0016"


def test_latest_closed_numbered_returns_none_when_nothing_closed(tmp_path):
    sessions_dir = tmp_path / "aiems/governance/sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "ESR-0017_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Open |", encoding="utf-8"
    )

    assert latest_closed_numbered("ESR", sessions_dir) is None


def test_check_stale_status_references_does_not_flag_open_session_as_stale(tmp_path, monkeypatch):
    """Regression test: an Engineering Session that has just opened (correctly
    Status: Open, not yet Closed) must not itself trigger a staleness error
    against PST-0001, which is required by PBK-0001 WP0B to keep pointing at
    the latest *closed* session until the new one actually closes. Found via
    ESR-0017: this check previously fired the moment the session file
    existed, regardless of its Status."""

    monkeypatch.chdir(tmp_path)

    sessions_dir = tmp_path / "aiems/governance/sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "ESR-0016_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Closed |", encoding="utf-8"
    )
    (sessions_dir / "ESR-0017_ENGINEERING_SESSION_REPORT.md").write_text(
        "| Status | Open |", encoding="utf-8"
    )

    status_dir = tmp_path / "aiems/governance/status"
    status_dir.mkdir(parents=True)
    status_path = status_dir / "PST-0001_PROGRAMME_STATUS.md"
    status_path.write_text(
        "| Current Mode | [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] closed. |",
        encoding="utf-8",
    )

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    result = ValidationResult(errors=[], warnings=[])
    check_stale_status_references(result)

    assert result.errors == []


def test_extract_badge_version_ignores_occurrences_outside_the_header():
    """EBG-0098 fix round (found live against FCH-0000): a bare whole-file
    search false-positived on HST/FCH archives, which embed raw pasted
    transcripts containing many incidental '**Version:**' occurrences (quoted
    content from other documents) far from any real top-of-file badge."""

    lines = ["# FCH-0000 - Full Chat History", "", "| Version | 1.0 |", ""]
    lines += ["filler line"] * 30
    lines.append("**Version:** 0.1 Foundation")
    text = "\n".join(lines)

    assert extract_table_version(text) == "1.0"
    assert extract_badge_version(text) is None


def test_extract_badge_version_finds_a_genuine_header_badge():
    text = "# PST-0001 - Programme Status\n\n**Version:** 2.87\n\n| Version | 2.87 |\n"

    assert extract_badge_version(text) == "2.87"
    assert extract_table_version(text) == "2.87"


def _write_register(register_path, rows):
    header = "| Artefact ID | Type | Title | Version | Status | Owner | Classification | Location |\n"
    header += "|---|---|---|---|---|---|---|---|\n"
    body = "".join(
        f"| {r['id']} | Doc | {r['title']} | {r['version']} | Approved | Owner | Internal | {r['location']} |\n"
        for r in rows
    )
    register_path.parent.mkdir(parents=True, exist_ok=True)
    register_path.write_text(header + body, encoding="utf-8")


def test_check_version_badge_table_consistency_flags_real_drift(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    doc_dir = tmp_path / "aiems/governance/status"
    doc_dir.mkdir(parents=True)
    (doc_dir / "PST-0001_PROGRAMME_STATUS.md").write_text(
        "# PST-0001\n\n**Version:** 2.66\n\n| Version | 2.58 |\n",
        encoding="utf-8",
    )

    register_path = tmp_path / "aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
    _write_register(
        register_path,
        [{"id": "PST-0001", "title": "Programme Status", "version": "2.58", "location": "aiems/governance/status"}],
    )

    result = ValidationResult(errors=[], warnings=[])
    check_version_badge_table_consistency(result)

    assert len(result.errors) == 1
    assert "PST-0001" in result.errors[0]
    assert "badge=2.66" in result.errors[0]
    assert "table=2.58" in result.errors[0]


def test_check_version_badge_table_consistency_passes_when_aligned(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    doc_dir = tmp_path / "aiems/governance/status"
    doc_dir.mkdir(parents=True)
    (doc_dir / "PST-0001_PROGRAMME_STATUS.md").write_text(
        "# PST-0001\n\n**Version:** 2.87\n\n| Version | 2.87 |\n",
        encoding="utf-8",
    )

    register_path = tmp_path / "aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
    _write_register(
        register_path,
        [{"id": "PST-0001", "title": "Programme Status", "version": "2.87", "location": "aiems/governance/status"}],
    )

    result = ValidationResult(errors=[], warnings=[])
    check_version_badge_table_consistency(result)

    assert result.errors == []
