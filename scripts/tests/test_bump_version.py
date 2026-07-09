"""Regression tests for scripts/bump_version.py."""

from __future__ import annotations

import sys

import scripts.bump_version as bump_version
from scripts.bump_version import BumpVersionError, plan_bump

# bump_version.py resolves `validate_repository` via a sys.path.insert() hack
# (so `python scripts/bump_version.py` works when invoked directly, not just
# via `-m`), which loads it as a *separate* module object from
# `scripts.validate_repository` - patching the latter's REPO_ROOT would not
# affect what bump_version.py's own find_registered_file() actually sees.
# Importing scripts.bump_version above guarantees the bare module is already
# in sys.modules by the time we grab it here.
bare_validate_repository = sys.modules["validate_repository"]

REG_HEADER = """\
# REG-0001 - Controlled Artefact Register

**Version:** {version}

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | REG-0001 |
| Title | Controlled Artefact Register |
| Version | {version} |
| Status | In Review |

---

# Controlled Artefact Register

| Artefact ID | Artefact Type | Title | Version | Status | Owner | Parent | Repository Location |
|--------------|---------------|-------|---------|------------|----------------------|----------------|--------------------------------|
| ADR-0099 | Architecture Decision Record | Example Decision | 1.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| REG-0001 | Register | Controlled Artefact Register | {version} | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| {version} | 9 July 2026 | Test Author | Initial. |
"""

ADR_CONTENT = """\
# ADR-0099 - Example Decision

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0099 |
| Title | Example Decision |
| Version | 1.0 |
| Status | Approved |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 9 July 2026 | Test Author | Initial. |
"""


def _setup(tmp_path, monkeypatch, reg_version: str = "3.60"):
    monkeypatch.setattr(bare_validate_repository, "REPO_ROOT", tmp_path)
    register_path = tmp_path / "aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
    register_path.parent.mkdir(parents=True)
    register_path.write_text(REG_HEADER.format(version=reg_version), encoding="utf-8")
    monkeypatch.setattr(bump_version, "REGISTER_PATH", register_path)

    decisions_dir = tmp_path / "aiems/governance/decisions"
    decisions_dir.mkdir(parents=True)
    (decisions_dir / "ADR-0099_EXAMPLE_DECISION.md").write_text(ADR_CONTENT, encoding="utf-8")

    return register_path


def test_bumping_another_artefact_auto_increments_reg0001(tmp_path, monkeypatch):
    register_path = _setup(tmp_path, monkeypatch, reg_version="3.60")

    edits = plan_bump("ADR-0099", "1.1", "Test change.", "Test Author", "9 July 2026")

    paths = {edit.path for edit in edits}
    assert register_path in paths
    assert len(edits) == 2

    reg_edit = next(edit for edit in edits if edit.path == register_path)
    assert "| Version | 3.61 |" in reg_edit.text or "**Version:** 3.61" in reg_edit.text
    assert "Aligned ADR-0099 version (1.0 to 1.1) following: Test change." in reg_edit.text


def test_bumping_reg0001_itself_uses_literal_target_version(tmp_path, monkeypatch):
    """Regression test: bumping REG-0001 as its own tracked artefact must
    apply the literal requested version, not silently discard it in favour
    of an auto-incremented one. Found via ESR-0017: the general two-edit
    path targets the same file twice when artefact_id == "REG-0001", and
    the second (auto-incrementing) write silently overwrote the first,
    producing a Version History entry describing a version transition that
    never actually happened on disk."""

    register_path = _setup(tmp_path, monkeypatch, reg_version="3.71")

    edits = plan_bump("REG-0001", "3.72", "Registered something.", "Test Author", "9 July 2026")

    assert len(edits) == 1
    assert edits[0].path == register_path

    text = edits[0].text
    assert "**Version:** 3.72" in text
    assert "| Version | 3.72 |" in text
    assert "| REG-0001 | Register | Controlled Artefact Register | 3.72 |" in text
    assert "| 3.72 | 9 July 2026 | Test Author | Registered something. |" in text
    # The old bug's telltale sign: a mismatched "Aligned REG-0001 version
    # (X to Y)" sentence where Y didn't match what was actually applied.
    assert "Aligned REG-0001" not in text


def test_bumping_reg0001_itself_does_not_silently_drop_wrong_guess(tmp_path, monkeypatch):
    """Even a 'coincidentally correct' literal target (old + 0.01) must be
    applied via the literal value, not the auto-increment path - otherwise
    a genuinely wrong guess (anything other than old + 0.01) would silently
    apply the auto-incremented value instead of raising or respecting the
    caller's explicit input."""

    register_path = _setup(tmp_path, monkeypatch, reg_version="3.60")

    # A deliberately "wrong" jump (not old + 0.01) must still be honoured
    # literally, not replaced by an auto-incremented 3.61.
    edits = plan_bump("REG-0001", "4.0", "Deliberate large jump.", "Test Author", "9 July 2026")

    assert len(edits) == 1
    text = edits[0].text
    assert "**Version:** 4.0" in text
    assert "| 4.0 | 9 July 2026 | Test Author | Deliberate large jump. |" in text
    assert "3.61" not in text


def test_bumping_reg0001_rejects_noop_version(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, reg_version="3.60")

    try:
        plan_bump("REG-0001", "3.60", "No-op.", "Test Author", "9 July 2026")
    except BumpVersionError as exc:
        assert "already at version" in str(exc)
    else:
        raise AssertionError("Expected a no-op REG-0001 version bump to be rejected.")
