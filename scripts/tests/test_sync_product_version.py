"""Regression tests for scripts/sync_product_version.py (EIP-ESR0032-003)."""

from __future__ import annotations

from scripts import sync_product_version
from scripts.sync_product_version import VersionSyncError, check_synced, plan_sync

PYPROJECT = 'version = "0.1.0"\nname = "jarvis"\n'
PACKAGE_JSON = '{\n  "name": "x",\n  "version": "0.1.0",\n  "private": true\n}\n'
CARGO_TOML = '[package]\nversion = "0.1.0"\nedition = "2021"\n'
TAURI_CONF = '{\n  "$schema": "s",\n  "version": "0.1.0",\n  "identifier": "x"\n}\n'


def _setup(tmp_path, monkeypatch, version="0.1.0"):
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (tmp_path / "package.json").write_text(PACKAGE_JSON, encoding="utf-8")
    src_tauri = tmp_path / "src-tauri"
    src_tauri.mkdir()
    (src_tauri / "Cargo.toml").write_text(CARGO_TOML, encoding="utf-8")
    (src_tauri / "tauri.conf.json").write_text(TAURI_CONF, encoding="utf-8")

    version_file = tmp_path / "VERSION"
    version_file.write_text(version + "\n", encoding="utf-8")

    monkeypatch.setattr(sync_product_version, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sync_product_version, "VERSION_FILE", version_file)


def test_plan_sync_updates_all_four_files_and_version(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")

    edits = plan_sync("0.2.0")

    assert len(edits) == 5
    for edit in edits:
        edit.path.write_text(edit.text, encoding="utf-8")

    assert (tmp_path / "VERSION").read_text(encoding="utf-8").strip() == "0.2.0"
    assert 'version = "0.2.0"' in (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert '"version": "0.2.0"' in (tmp_path / "package.json").read_text(encoding="utf-8")
    assert 'version = "0.2.0"' in (tmp_path / "src-tauri" / "Cargo.toml").read_text(encoding="utf-8")
    assert '"version": "0.2.0"' in (tmp_path / "src-tauri" / "tauri.conf.json").read_text(encoding="utf-8")
    # Untouched fields must survive - this is a targeted single-line edit,
    # not a rewrite of the whole file.
    assert '"identifier": "x"' in (tmp_path / "src-tauri" / "tauri.conf.json").read_text(encoding="utf-8")


def test_plan_sync_rejects_noop_version(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")

    try:
        plan_sync("0.1.0")
    except VersionSyncError as exc:
        assert "Already at version" in str(exc)
    else:
        raise AssertionError("Expected a no-op version to be rejected.")


def test_plan_sync_rejects_non_semver_string(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")

    try:
        plan_sync("v1")
    except VersionSyncError as exc:
        assert "not a plain X.Y.Z version" in str(exc)
    else:
        raise AssertionError("Expected a non-X.Y.Z version string to be rejected.")


def test_plan_sync_rejects_missing_target_file(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")
    (tmp_path / "package.json").unlink()

    try:
        plan_sync("0.2.0")
    except VersionSyncError as exc:
        assert "package.json" in str(exc)
    else:
        raise AssertionError("Expected a missing target file to be rejected, not silently skipped.")


def test_plan_sync_rejects_unparseable_version_field(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")
    (tmp_path / "src-tauri" / "Cargo.toml").write_text("[package]\nedition = \"2021\"\n", encoding="utf-8")

    try:
        plan_sync("0.2.0")
    except VersionSyncError as exc:
        assert "Cargo.toml" in str(exc)
    else:
        raise AssertionError("Expected a missing version field to be rejected, not silently skipped.")


def test_check_synced_reports_no_mismatches_when_all_agree(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")

    assert check_synced() == []


def test_check_synced_reports_drifted_file(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")
    (tmp_path / "package.json").write_text(
        PACKAGE_JSON.replace("0.1.0", "0.1.1"), encoding="utf-8"
    )

    mismatches = check_synced()

    assert len(mismatches) == 1
    assert "package.json" in mismatches[0]
    assert "0.1.1" in mismatches[0]


def test_check_synced_reports_missing_version_file(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, version="0.1.0")
    (tmp_path / "VERSION").unlink()

    mismatches = check_synced()

    assert len(mismatches) == 1
    assert "missing or empty" in mismatches[0]
