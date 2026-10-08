"""Smoke test of the packaged backend's process-tree guarantees on macOS/Linux.

ESR-0061 WP2b (EBG-0162, EIP-ESR0061-002 Section 6.5). Runs a built sidecar
(``python scripts/build_backend_sidecar.py`` first) the way the Tauri host does -
as a process-group leader, with ``JARVIS_HOST_PID`` set - and checks, with the
real binary:

1. a ``platform.status`` request gets a real answer;
2. a graceful stop (stdin closed) ends the whole tree and leaves no ``_MEI*``
   directory behind;
3. a force-killed host (the orphan case) ends the busy backend's whole tree
   through the watchdog, again leaving no ``_MEI*`` directory;
4. a group kill (what the host's ``ProcessTree::terminate`` does) ends the tree.

Exit code 0 only if every check passes. POSIX only. All state is isolated in a
temporary directory.

    python scripts/smoke_unix_sidecar.py [--sidecar PATH] [--expect-tree]

``--expect-tree`` additionally requires at least two processes in the group (the
onefile bootloader plus the interpreter it forks); leave it off for a wrapper.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BINARIES = REPO_ROOT / "src-tauri" / "binaries"
STARTUP_TIMEOUT = 90.0
EXIT_TIMEOUT = 20.0


class SmokeError(Exception):
    pass


def find_sidecar() -> Path:
    found = sorted(BINARIES.glob("jarvis-backend-*"))
    if len(found) != 1:
        raise SmokeError(f"expected exactly one sidecar in {BINARIES}, found {[p.name for p in found]}")
    return found[0]


def group_has_members(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except OSError as exc:
        if exc.errno == errno.ESRCH:
            return False
        if exc.errno == errno.EPERM:
            return True
        raise
    return True


def group_size(pgid: int) -> int | None:
    """Processes in the group, or None when `pgrep` is unavailable."""

    if shutil.which("pgrep") is None:
        return None
    result = subprocess.run(["pgrep", "-g", str(pgid)], capture_output=True, text=True, check=False)
    return len([line for line in result.stdout.split() if line.strip()])


def wait_group_gone(proc: subprocess.Popen, timeout: float) -> bool:
    """Waits for the whole group to end, reaping the leader as the host does."""

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        proc.poll()  # reap the leader: a zombie leader keeps its group alive
        if not group_has_members(proc.pid):
            return True
        time.sleep(0.1)
    return False


def leftover_extraction_dirs(tmp: Path) -> list[str]:
    return sorted(p.name for p in tmp.glob("_MEI*"))


class Backend:
    """A sidecar started as the host starts it."""

    def __init__(self, sidecar: Path, state: Path, host_pid: int) -> None:
        self.tmp = state / "tmp"
        self.tmp.mkdir(parents=True, exist_ok=True)
        env = {
            **os.environ,
            "TMPDIR": str(self.tmp),
            "JARVIS_HOST_PID": str(host_pid),
            "JARVIS_MEMORY_DB_PATH": str(state / "memory.db"),
            "JARVIS_IDENTITY_DB_PATH": str(state / "identity.db"),
            "JARVIS_MEMORY_BACKUP_DIR": str(state / "backups"),
            "JARVIS_LOG_DIR": str(state / "logs"),
        }
        self.proc = subprocess.Popen(
            [str(sidecar)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env,
            process_group=0,
            text=True,
        )

    def request(self, method: str) -> dict:
        assert self.proc.stdin is not None and self.proc.stdout is not None
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": {}}) + "\n")
        self.proc.stdin.flush()
        lines: list[str] = []
        reader = threading.Thread(target=lambda: lines.append(self.proc.stdout.readline()), daemon=True)
        reader.start()
        reader.join(STARTUP_TIMEOUT)
        if not lines or not lines[0].strip():
            raise SmokeError(f"no answer to {method} within {STARTUP_TIMEOUT:.0f}s")
        return json.loads(lines[0])

    def cleanup(self) -> None:
        if group_has_members(self.proc.pid):
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except OSError:
                pass
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
    if not ok:
        raise SmokeError(name)


def run(sidecar: Path, expect_tree: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="jarvis-smoke-") as raw:
        root = Path(raw)

        # 1 + 2: answers a request; graceful stop ends the tree and cleans up.
        host = subprocess.Popen(["sleep", "300"])
        backend = Backend(sidecar, root / "graceful", host.pid)
        try:
            reply = backend.request("platform.status")
            check("platform.status answered", "result" in reply, json.dumps(reply)[:120])
            size = group_size(backend.proc.pid)
            if expect_tree:
                check("backend is a tree of at least two processes", size is not None and size >= 2, f"{size}")
            else:
                print(f"[info] group size {size}")
            assert backend.proc.stdin is not None
            backend.proc.stdin.close()
            check("graceful stop ends the whole tree", wait_group_gone(backend.proc, EXIT_TIMEOUT))
            check("graceful stop leaves no _MEI directory", not leftover_extraction_dirs(backend.tmp), str(leftover_extraction_dirs(backend.tmp)))
        finally:
            backend.cleanup()
            host.kill()
            host.wait()

        # 3: host force-killed. This script keeps the backend's stdin open, so no
        # EOF can end it: only the watchdog can, as for a backend too busy to read.
        host = subprocess.Popen(["sleep", "300"])
        backend = Backend(sidecar, root / "orphan", host.pid)
        try:
            backend.request("platform.status")
            # Without this, a backend that had crashed on its own would pass below.
            check("backend is alive before its host is killed", backend.proc.poll() is None and group_has_members(backend.proc.pid))
            host.kill()
            host.wait()
            check("orphaned backend ends its whole tree", wait_group_gone(backend.proc, EXIT_TIMEOUT))
            check("orphaned backend leaves no _MEI directory", not leftover_extraction_dirs(backend.tmp), str(leftover_extraction_dirs(backend.tmp)))
        finally:
            backend.cleanup()
            if host.poll() is None:
                host.kill()
                host.wait()

        # 4: group kill, as the host's forced path does.
        host = subprocess.Popen(["sleep", "300"])
        backend = Backend(sidecar, root / "killpg", host.pid)
        try:
            backend.request("platform.status")
            check("backend is alive before the group kill", backend.proc.poll() is None and group_has_members(backend.proc.pid))
            os.killpg(backend.proc.pid, signal.SIGKILL)
            check("group kill ends the whole tree", wait_group_gone(backend.proc, EXIT_TIMEOUT))
        finally:
            backend.cleanup()
            host.kill()
            host.wait()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sidecar", type=Path, help="path to the built sidecar (default: the one in src-tauri/binaries)")
    parser.add_argument("--expect-tree", action="store_true", help="require two or more processes in the group")
    args = parser.parse_args(argv)
    if os.name != "posix":
        print("POSIX only.", file=sys.stderr)
        return 2
    try:
        run(args.sidecar or find_sidecar(), args.expect_tree)
    except SmokeError as exc:
        print(f"SMOKE FAILED: {exc}", file=sys.stderr)
        return 1
    print("SMOKE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
