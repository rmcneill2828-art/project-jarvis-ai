"""Standalone entry point for the PyInstaller-packaged Guardian sidecar.

Unlike ``jarvis.app.main()`` (which also supports the legacy Tkinter
First Light GUI via an unconditional ``from jarvis.gui import
JarvisApp`` at module load time), this entry point always runs the
stdio JSON-RPC bridge - the only mode a Tauri sidecar process ever
needs (EIP-ESR0032-001). Kept as a separate script so the packaged
sidecar never has to bundle Tkinter for a headless backend.

ESR-0062 WP5: an installed household has no Python, so the two recovery
tools are also reachable here, with the same trust model as
`python -m jarvis.tools.reset_admin_pin` and `...add_administrator`: run
from a command line on the computer, never from inside the app, and a reset
leaves a notice for the next Administrator.
"""

import logging
import sys
from pathlib import Path

from jarvis.config import APP_CONFIG
from jarvis.interfaces.stdio_rpc import run as run_stdio_rpc
from jarvis.interfaces.voice_self_check import round_trip as run_voice_round_trip
from jarvis.interfaces.voice_self_check import run as run_voice_self_check
from jarvis.tools import add_administrator, reset_admin_pin

VOICE_SELF_CHECK_FLAG = "--voice-self-check"
VOICE_ROUND_TRIP_FLAG = "--voice-round-trip"
RESET_ADMIN_PIN_FLAG = "--reset-admin-pin"
ADD_ADMINISTRATOR_FLAG = "--add-administrator"
RECOVERY_USAGE = (
    "Usage, with JARVIS closed:\n"
    f"  jarvis-backend {RESET_ADMIN_PIN_FLAG}\n"
    f'  jarvis-backend {ADD_ADMINISTRATOR_FLAG} "Name"\n'
    "Nothing was changed."
)


def main() -> None:
    # ESR-0062 WP3 (V10): prove the build carries every part voice needs, then exit.
    if VOICE_SELF_CHECK_FLAG in sys.argv[1:]:
        sys.exit(run_voice_self_check(sys.stdout))
    # V11: with real models in the given folder, speak and hear a sentence, then exit.
    if len(sys.argv) == 3 and sys.argv[1] == VOICE_ROUND_TRIP_FLAG:
        sys.exit(run_voice_round_trip(Path(sys.argv[2]), sys.stdout))
    # WP5: recovery for a forgotten PIN, or a household with no Administrator.
    if sys.argv[1:] == [RESET_ADMIN_PIN_FLAG]:
        sys.exit(reset_admin_pin.main([]))
    if len(sys.argv) == 3 and sys.argv[1] == ADD_ADMINISTRATOR_FLAG:
        sys.exit(add_administrator.main([sys.argv[2]]))
    # A mistyped recovery command explains itself rather than silently
    # starting the backend (WP5 implementation review, Antigravity Low).
    if any(arg in (RESET_ADMIN_PIN_FLAG, ADD_ADMINISTRATOR_FLAG) for arg in sys.argv[1:]):
        print(RECOVERY_USAGE)
        sys.exit(2)
    logging.basicConfig(
        level=APP_CONFIG.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run_stdio_rpc()


if __name__ == "__main__":
    main()
