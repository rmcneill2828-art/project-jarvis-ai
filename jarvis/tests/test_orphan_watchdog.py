"""Tests for the orphan watchdog (ESR-0061 WP2b, EIP-ESR0061-002 Section 6.3)."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time

import pytest

from jarvis.interfaces import orphan_watchdog as ow

posix_only = pytest.mark.skipif(os.name != "posix", reason="the watchdog is POSIX-only")


def test_does_nothing_without_a_host_pid():
    assert ow.start_orphan_watchdog({}, posix=True) is None
    assert ow.start_orphan_watchdog({ow.HOST_PID_ENV: "  "}, posix=True) is None


def test_does_nothing_on_windows_even_with_a_host_pid():
    # Signal 0 is CTRL_C_EVENT on Windows: os.kill(pid, 0) would send a Ctrl+C.
    assert ow.start_orphan_watchdog({ow.HOST_PID_ENV: "1234"}, posix=False) is None


@pytest.mark.parametrize("value", ["abc", "0", "1", "-5"])
def test_ignores_an_unusable_pid(value):
    assert ow.start_orphan_watchdog({ow.HOST_PID_ENV: value}, posix=True) is None


def test_exits_once_the_host_is_gone_and_not_before():
    exited = threading.Event()
    codes: list[int] = []
    answers = iter([True, True, False])

    def exit_process(code: int) -> None:
        codes.append(code)
        exited.set()

    thread = ow.start_orphan_watchdog(
        {ow.HOST_PID_ENV: "4242"},
        poll_seconds=0.01,
        alive=lambda pid: next(answers),
        exit_process=exit_process,
        posix=True,
    )

    assert thread is not None and thread.daemon
    assert exited.wait(5)
    assert codes == [ow.ORPHAN_EXIT_CODE]


def test_keeps_running_while_the_host_is_alive():
    calls: list[int] = []
    exited = threading.Event()

    def alive(pid: int) -> bool:
        calls.append(pid)
        return True

    ow.start_orphan_watchdog(
        {ow.HOST_PID_ENV: "4242"},
        poll_seconds=0.01,
        alive=alive,
        exit_process=lambda code: exited.set(),
        posix=True,
    )
    time.sleep(0.2)

    assert len(calls) > 3 and calls[0] == 4242
    assert not exited.is_set()


@posix_only
def test_host_is_alive_sees_this_process_and_a_dead_one():
    assert ow.host_is_alive(os.getpid())
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    child.wait()
    assert not ow.host_is_alive(child.pid)


@posix_only
def test_a_real_backend_process_ends_when_its_real_host_is_killed():
    host = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    backend_code = (
        "import time; from jarvis.interfaces.orphan_watchdog import start_orphan_watchdog; "
        "start_orphan_watchdog(poll_seconds=0.05); time.sleep(60)"
    )
    backend = subprocess.Popen(
        [sys.executable, "-c", backend_code],
        env={**os.environ, ow.HOST_PID_ENV: str(host.pid)},
    )
    try:
        time.sleep(0.5)
        assert backend.poll() is None, "backend must run while its host is alive"
        host.kill()
        host.wait()
        assert backend.wait(timeout=10) == ow.ORPHAN_EXIT_CODE
    finally:
        for process in (host, backend):
            if process.poll() is None:
                process.kill()
                process.wait()
