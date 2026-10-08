"""Tests for scripts/build_backend_sidecar.py naming (ESR-0061 WP2b, EBG-0162).

PyInstaller itself is replaced by a stand-in that writes the file it would
produce, so these check only what the script decides: the Tauri-facing name per
target triple, and that the executable bit survives the copy.
"""

from __future__ import annotations

import os
import stat
import subprocess

import pytest

from scripts import build_backend_sidecar as bbs


def _fake_pyinstaller(monkeypatch, tmp_path, suffix: str):
    output = tmp_path / "binaries"
    monkeypatch.setattr(bbs, "OUTPUT_DIR", output)

    def fake_run(command, cwd=None, check=False):
        dist = tmp_path / "work" / "dist"
        dist.mkdir(parents=True, exist_ok=True)
        built = dist / f"{bbs.SIDECAR_NAME}{suffix}"
        built.write_bytes(b"binary")
        built.chmod(0o755)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(bbs.subprocess, "run", fake_run)
    return output


def test_apple_silicon_sidecar_is_named_for_its_triple_without_a_suffix(monkeypatch, tmp_path):
    output = _fake_pyinstaller(monkeypatch, tmp_path, suffix="")

    path = bbs.build_sidecar("aarch64-apple-darwin", tmp_path / "work")

    assert path == output / "jarvis-backend-aarch64-apple-darwin"
    assert path.read_bytes() == b"binary"


@pytest.mark.skipif(os.name != "posix", reason="permission bits are POSIX")
def test_the_executable_bit_survives_the_copy(monkeypatch, tmp_path):
    _fake_pyinstaller(monkeypatch, tmp_path, suffix="")

    path = bbs.build_sidecar("aarch64-apple-darwin", tmp_path / "work")

    assert path.stat().st_mode & stat.S_IXUSR


def test_windows_sidecar_keeps_its_exe_suffix(monkeypatch, tmp_path):
    output = _fake_pyinstaller(monkeypatch, tmp_path, suffix=".exe")

    path = bbs.build_sidecar("x86_64-pc-windows-msvc", tmp_path / "work")

    assert path == output / "jarvis-backend-x86_64-pc-windows-msvc.exe"


def test_a_missing_build_artefact_is_an_error_not_a_guess(monkeypatch, tmp_path):
    monkeypatch.setattr(bbs, "OUTPUT_DIR", tmp_path / "binaries")
    monkeypatch.setattr(bbs.subprocess, "run", lambda command, cwd=None, check=False: subprocess.CompletedProcess(command, 0))

    with pytest.raises(bbs.BuildError):
        bbs.build_sidecar("aarch64-apple-darwin", tmp_path / "work")
