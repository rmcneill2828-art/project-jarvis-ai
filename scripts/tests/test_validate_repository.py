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
    parse_register_rows,
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


# --- ESR-0061 WP1c R7: register parsing and REG-0001 sync -------------------

_REG_ROWS = textwrap.dedent(
    """\
    # REG-0001

    | Artefact ID | Artefact Type | Title | Version | Status | Owner | Parent | Repository Location |
    |---|---|---|---|---|---|---|---|
    | ADR-0001 | ADR | One | 1.0 | Approved | PS | CHR-0001 | `aiems/governance/decisions/` |
    | EIP-ESR0061-001 | Engineering Implementation Package | Example | 0.7 | Draft | PS | EBR-0001 | `aiems/governance/reviews/` |
    | JARVIS_PRODUCT_ARCHITECTURE | Product Architecture | Product | 1.4 | Approved | PS | EBG-0017 | `jarvis/architecture/` |
    | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Repository Baseline | Old | 1.0 | Accepted | PS | CHR-0001 | `aiems/governance/baselines/` |
    | ESR-0005-RELOAD | Session Reload Snapshot | Reload | 1.0 | Superseded | PS | ESR-0005 | `aiems/governance/status/` |

    # Version History

    | Version | Date | Author | Summary |
    |---|---|---|---|
    | 3.1 | 1 July 2026 | Someone | Registered EIP-ESR0061-001 and more text here. |
    """
)


def test_parse_register_rows_accepts_every_id_shape_in_use(tmp_path):
    register = tmp_path / "REG.md"
    register.write_text(_REG_ROWS, encoding="utf-8")

    ids = [row["id"] for row in parse_register_rows(register)]

    assert ids == ["ADR-0001", "EIP-ESR0061-001", "JARVIS_PRODUCT_ARCHITECTURE", "RBL-0007", "ESR-0005-RELOAD"]


def test_parse_register_rows_handles_a_piped_wikilink_in_the_id_cell(tmp_path):
    register = tmp_path / "REG.md"
    register.write_text(_REG_ROWS, encoding="utf-8")

    row = next(r for r in parse_register_rows(register) if r["id"] == "RBL-0007")

    assert row["version"] == "1.0"
    assert row["status"] == "Accepted"
    assert row["location"] == "aiems/governance/baselines/"


def test_parse_register_rows_skips_version_history_rows(tmp_path):
    register = tmp_path / "REG.md"
    register.write_text(_REG_ROWS, encoding="utf-8")

    assert not any(row["id"].startswith("3.") for row in parse_register_rows(register))


def test_find_registered_file_resolves_a_compound_id(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    status_dir = tmp_path / "aiems/governance/status"
    status_dir.mkdir(parents=True)
    target = status_dir / "ESR-0005_ENGINEERING_SESSION_RELOAD.md"
    target.write_text("x", encoding="utf-8")
    (status_dir / "ESR-0005_ENGINEERING_SESSION_REPORT.md").write_text("y", encoding="utf-8")

    assert validator.find_registered_file("ESR-0005-RELOAD", "aiems/governance/status/") == target


def _write_controlled(tmp_path, doc_status: str | None, reg_status: str = "Approved"):
    register_dir = tmp_path / "aiems/governance/registers"
    register_dir.mkdir(parents=True)
    (register_dir / "REG-0001_CONTROLLED_ARTEFACT_REGISTER.md").write_text(
        textwrap.dedent(
            f"""\
            | Artefact ID | Artefact Type | Title | Version | Status | Owner | Parent | Repository Location |
            |---|---|---|---|---|---|---|---|
            | ADR-0001 | ADR | One | 1.0 | {reg_status} | PS | CHR-0001 | `aiems/governance/decisions/` |
            """
        ),
        encoding="utf-8",
    )
    decisions = tmp_path / "aiems/governance/decisions"
    decisions.mkdir(parents=True)
    status_row = f"| Status | {doc_status} |\n" if doc_status is not None else ""
    (decisions / "ADR-0001_ONE.md").write_text(
        f"# ADR-0001\n\n| Field | Value |\n|---|---|\n| Version | 1.0 |\n{status_row}", encoding="utf-8"
    )


def test_check_controlled_register_flags_a_status_mismatch(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    _write_controlled(tmp_path, doc_status="Superseded", reg_status="Approved")
    result = ValidationResult(errors=[], warnings=[])

    validator.check_controlled_register(result)

    assert any("ADR-0001 status mismatch" in error for error in result.errors)


def test_check_controlled_register_passes_matching_status(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    _write_controlled(tmp_path, doc_status="Approved", reg_status="Approved")
    result = ValidationResult(errors=[], warnings=[])

    validator.check_controlled_register(result)

    assert result.errors == []


def test_check_controlled_register_warns_when_document_has_no_status(tmp_path, monkeypatch):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    _write_controlled(tmp_path, doc_status=None)
    result = ValidationResult(errors=[], warnings=[])

    validator.check_controlled_register(result)

    assert result.errors == []
    assert any("no parseable document status" in warning for warning in result.warnings)


# --- ESR-0061 WP1c R10: section-reference warnings ---------------------------

_UAM = "# UAM-0001 - Example\n\n# 8. Orb\n\n## 8.1 Graph\n\n## 8.2 States\n"
_JRM = "# JRM-0001 - Roadmap\n\n## 7.1 Near-term\n\n## 7.3 Path\n"


def _section_warnings(tmp_path, monkeypatch, body: str) -> list[str]:
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validator, "HISTORICAL_ARCHIVE_DIR", tmp_path / "aiems" / "History")
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "UAM-0001_EXAMPLE.md").write_text(_UAM, encoding="utf-8")
    (docs / "JRM-0001_ROADMAP.md").write_text(_JRM, encoding="utf-8")
    (docs / "DOC-0001_TEST.md").write_text("# DOC-0001\n\n# 1. Intro\n\n" + body + "\n", encoding="utf-8")
    result = ValidationResult(errors=[], warnings=[])
    validator.check_section_references(result)
    return [w for w in result.warnings if "DOC-0001_TEST" in w]


def test_section_ref_resolves_artefact_in_an_earlier_table_cell(tmp_path, monkeypatch):
    body = "| [[UAM-0001_EXAMPLE|UAM-0001]] | Section 8.1 is the design direction |"
    assert _section_warnings(tmp_path, monkeypatch, body) == []


def test_section_ref_resolves_through_a_short_qualifier(tmp_path, monkeypatch):
    body = "See JRM-0001 Track B Section 7.1 and UAM-0001's own Section 8.2 for detail."
    assert _section_warnings(tmp_path, monkeypatch, body) == []


def test_section_ref_follow_on_inherits_the_previous_referent(tmp_path, monkeypatch):
    body = "[[UAM-0001_EXAMPLE|UAM-0001]] Section 8.1 (the graph) and Section 8.2 (the states) changed."
    assert _section_warnings(tmp_path, monkeypatch, body) == []


def test_section_ref_checks_every_number_in_a_list(tmp_path, monkeypatch):
    ok = _section_warnings(tmp_path, monkeypatch, "UAM-0001 Sections 8.1, 8.2 and 8 are amended.")
    assert ok == []
    bad = _section_warnings(tmp_path, monkeypatch, "UAM-0001 Sections 8.1, 8.9 and 8 are amended.")
    assert len(bad) == 1 and "Section 8.9" in bad[0]


def test_section_ref_skips_version_history_tables(tmp_path, monkeypatch):
    body = "# 9. Version History\n\n| Version | Summary |\n|---|---|\n| 1.1 | Fixed Section 42 wording. |"
    assert _section_warnings(tmp_path, monkeypatch, body) == []


def test_section_ref_guard_broken_own_reference_still_warns(tmp_path, monkeypatch):
    warnings = _section_warnings(tmp_path, monkeypatch, "As Section 5 explains, this is wrong.")
    assert len(warnings) == 1 and "Section 5" in warnings[0]


def test_section_ref_guard_missing_section_in_resolved_artefact_still_warns(tmp_path, monkeypatch):
    warnings = _section_warnings(tmp_path, monkeypatch, "JRM-0001 Track B Section 7.9 is the plan.")
    assert len(warnings) == 1 and "JRM-0001_ROADMAP" in warnings[0]


def test_section_ref_guard_inheritance_stops_at_sentence_end(tmp_path, monkeypatch):
    body = "UAM-0001 Section 8.1 changed. Section 4 of this document is unaffected."
    warnings = _section_warnings(tmp_path, monkeypatch, body)
    assert len(warnings) == 1 and "Section 4" in warnings[0] and "this document" in warnings[0]


# --- ESR-0061 WP1c R4: single-source current baseline ------------------------


def _baseline_claim_result(tmp_path, monkeypatch, files: dict[str, str]):
    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validator, "HISTORICAL_ARCHIVE_DIR", tmp_path / "aiems" / "History")
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    result = ValidationResult(errors=[], warnings=[])
    validator.check_current_baseline_claims(result)
    return result


_LIVE_COC = "aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md"


def test_current_baseline_claim_in_a_live_artefact_is_an_error(tmp_path, monkeypatch):
    result = _baseline_claim_result(
        tmp_path, monkeypatch, {_LIVE_COC: "* [[RBL-0040_X|RBL-0040]] records the current accepted repository baseline.\n"}
    )
    assert len(result.errors) == 1 and "COC-0001" in result.errors[0]


def test_current_baseline_claim_in_a_frozen_artefact_is_a_warning(tmp_path, monkeypatch):
    result = _baseline_claim_result(
        tmp_path,
        monkeypatch,
        {"aiems/governance/decisions/ADR-0001_X.md": "| [[RBL-0009_X|RBL-0009]] | Current accepted repository baseline. |\n"},
    )
    assert result.errors == []
    assert len(result.warnings) == 1 and "ADR-0001" in result.warnings[0]


def test_pointer_to_pst0001_is_not_a_claim(tmp_path, monkeypatch):
    result = _baseline_claim_result(
        tmp_path,
        monkeypatch,
        {_LIVE_COC: "| [[RBL-0040_X|RBL-0040]] | Accepted at ESR-0060; the current baseline is recorded in PST-0001. |\n"},
    )
    assert result.errors == [] and result.warnings == []


def test_baseline_claims_ignore_records_and_version_history(tmp_path, monkeypatch):
    result = _baseline_claim_result(
        tmp_path,
        monkeypatch,
        {
            "aiems/governance/sessions/ESR-0010_X.md": "RBL-0009 is the current accepted repository baseline.\n",
            "aiems/governance/status/PST-0001_PROGRAMME_STATUS.md": "| Current Repository Baseline | [[RBL-0040_X|RBL-0040]] |\n",
            "aiems/models/MOD-0001_X.md": "# 9. Version History\n\n| 1.2 | 1 July | A | Current accepted repository baseline set to RBL-0009. |\n",
        },
    )
    assert result.errors == [] and result.warnings == []


def test_find_registered_file_prefers_the_exact_id_over_a_suffixed_one(tmp_path, monkeypatch):
    """CI run 37448647822 (Linux): `ESR-0007*.md` also matches the addendum
    `ESR-0007A_...`, and Linux sorts it first ("A" < "_") while Windows does
    not, so ESR-0007's row was compared with its addendum."""

    import scripts.validate_repository as validator

    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    sessions = tmp_path / "aiems/governance/sessions"
    sessions.mkdir(parents=True)
    report = sessions / "ESR-0007_ENGINEERING_SESSION_REPORT.md"
    addendum = sessions / "ESR-0007A_POST_CLOSURE_ENGINEERING_ADDENDUM.md"
    report.write_text("r", encoding="utf-8")
    addendum.write_text("a", encoding="utf-8")
    monkeypatch.setattr(validator.Path, "glob", lambda self, pattern: iter([addendum, report]))

    assert validator.find_registered_file("ESR-0007", "aiems/governance/sessions/") == report
    assert validator.find_registered_file("ESR-0007A", "aiems/governance/sessions/") == addendum
