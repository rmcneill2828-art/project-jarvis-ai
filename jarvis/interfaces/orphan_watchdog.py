"""Ends the backend when the process that started it is gone (ESR-0061 WP2b,
EBG-0162, EIP-ESR0061-002 Section 6.3).

On Windows a job object ends a backend whose host was killed (EBG-0154). Unix
has no equivalent: a host `SIGKILL` leaves the backend running, and a *busy*
backend never sees stdin close because its read loop is not running. The host
therefore passes its own PID in `JARVIS_HOST_PID`, and a daemon thread here
checks every second that it still exists.

The host's PID is watched, not `getppid()`: in the packaged onefile sidecar the
backend's parent is PyInstaller's bootloader, not the host. Ending this process
makes the bootloader see its child exit, clean its `_MEI*` directory and exit.

POSIX only. On Windows signal 0 is `CTRL_C_EVENT`, so `os.kill(pid, 0)` sends
a Ctrl+C to a console process group instead of testing for existence; the
watchdog does nothing there.
"""

from __future__ import annotations

import logging
import os
import threading
from collections.abc import Callable, Mapping

logger = logging.getLogger(__name__)

HOST_PID_ENV = "JARVIS_HOST_PID"
POLL_SECONDS = 1.0
ORPHAN_EXIT_CODE = 1


def host_is_alive(pid: int) -> bool:
    """True if a process with this PID exists. POSIX only (see module note)."""

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by someone else
    return True


def start_orphan_watchdog(
    environ: Mapping[str, str] | None = None,
    *,
    poll_seconds: float = POLL_SECONDS,
    alive: Callable[[int], bool] = host_is_alive,
    exit_process: Callable[[int], None] = os._exit,
    posix: bool | None = None,
) -> threading.Thread | None:
    """Start the watchdog thread; returns it, or None when it does not apply
    (Windows, no `JARVIS_HOST_PID`, or a value that is not a usable PID)."""

    env = os.environ if environ is None else environ
    if not (os.name == "posix" if posix is None else posix):
        return None
    raw = env.get(HOST_PID_ENV, "").strip()
    if not raw:
        return None
    try:
        host_pid = int(raw)
    except ValueError:
        logger.warning("%s is not a number; the orphan watchdog is off.", HOST_PID_ENV)
        return None
    if host_pid <= 1:
        logger.warning("%s=%s is not a usable PID; the orphan watchdog is off.", HOST_PID_ENV, raw)
        return None

    def watch() -> None:
        stop = threading.Event()
        while not stop.wait(poll_seconds):
            if not alive(host_pid):
                logger.warning("JARVIS host process %s is gone; backend exiting.", host_pid)
                logging.shutdown()
                exit_process(ORPHAN_EXIT_CODE)
                return

    thread = threading.Thread(target=watch, name="orphan-watchdog", daemon=True)
    thread.start()
    return thread
