"""Package the JARVIS backend as a Tauri sidecar executable (EIP-ESR0032-001).

Runs PyInstaller against ``scripts/jarvis_backend_entry.py`` (the
headless stdio-RPC-only entry point - see that file's own docstring
for why it is separate from ``jarvis.app.main()``) and places the
result at the path Tauri's ``bundle.externalBin`` sidecar convention
expects: ``src-tauri/binaries/<name>-<target-triple>.exe``.

The target triple is read from ``rustc -vV`` by default (this
machine's host triple) rather than hardcoded, since a build produced
for one triple will not run as a sidecar on another.

This is a build-time tool, not part of the shipped application -
its own output (``src-tauri/binaries/``) is gitignored and
regenerated from source on demand, never committed.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRY_SCRIPT = REPO_ROOT / "scripts" / "jarvis_backend_entry.py"
SIDECAR_NAME = "jarvis-backend"
OUTPUT_DIR = REPO_ROOT / "src-tauri" / "binaries"


class BuildError(Exception):
    """Raised when the sidecar cannot be built - never guessed past."""


def detect_target_triple() -> str:
    """Return this machine's Rust host target triple via ``rustc -vV``."""

    try:
        result = subprocess.run(
            ["rustc", "-vV"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BuildError(f"Could not run 'rustc -vV' to detect the target triple: {exc}") from exc

    for line in result.stdout.splitlines():
        if line.startswith("host:"):
            return line.split(":", 1)[1].strip()

    raise BuildError("'rustc -vV' output did not contain a 'host:' line.")


def build_sidecar(target_triple: str, work_dir: Path) -> Path:
    """Run PyInstaller, returning the path to the produced sidecar executable.

    Tauri's own `externalBin` naming convention only appends `.exe` for
    Windows targets (`-windows-` in the triple) - Linux/macOS sidecars are
    extension-less. PyInstaller follows the same host-platform convention
    for its own output, so both the located build artefact and the copied,
    Tauri-facing sidecar name must branch on this - hardcoding `.exe`
    unconditionally breaks on any non-Windows host (found via a real WSL
    Ubuntu build, EIP-ESR0032-002).
    """

    if not ENTRY_SCRIPT.exists():
        raise BuildError(f"Entry script not found: {ENTRY_SCRIPT}")

    exe_suffix = ".exe" if "windows" in target_triple else ""

    dist_dir = work_dir / "dist"
    build_dir = work_dir / "build"
    spec_dir = work_dir

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        SIDECAR_NAME,
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(build_dir),
        "--specpath",
        str(spec_dir),
        "--noconfirm",
        str(ENTRY_SCRIPT),
    ]

    result = subprocess.run(command, cwd=REPO_ROOT, check=False)
    if result.returncode != 0:
        raise BuildError(f"PyInstaller exited with code {result.returncode}.")

    built_exe = dist_dir / f"{SIDECAR_NAME}{exe_suffix}"
    if not built_exe.exists():
        raise BuildError(f"PyInstaller reported success but {built_exe} does not exist.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target_path = OUTPUT_DIR / f"{SIDECAR_NAME}-{target_triple}{exe_suffix}"
    # shutil.copy (not copyfile) preserves the source file's permission bits -
    # PyInstaller's own output is already executable, and copyfile alone
    # would silently drop that bit on Linux/macOS, breaking Tauri's sidecar
    # spawn with a permission error rather than a clear "not found" one.
    shutil.copy(built_exe, target_path)
    return target_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-triple",
        default=None,
        help="Override the detected Rust target triple (default: this machine's host triple).",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=REPO_ROOT / ".sidecar-build",
        help="Scratch directory for PyInstaller's own build/dist/spec output.",
    )
    args = parser.parse_args()

    try:
        target_triple = args.target_triple or detect_target_triple()
        sidecar_path = build_sidecar(target_triple, args.work_dir)
    except BuildError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Sidecar built: {sidecar_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
