"""Standalone entry point for the PyInstaller-packaged Guardian sidecar.

Unlike ``jarvis.app.main()`` (which also supports the legacy Tkinter
First Light GUI via an unconditional ``from jarvis.gui import
JarvisApp`` at module load time), this entry point always runs the
stdio JSON-RPC bridge - the only mode a Tauri sidecar process ever
needs (EIP-ESR0032-001). Kept as a separate script so the packaged
sidecar never has to bundle Tkinter for a headless backend.
"""

import logging
import sys
from pathlib import Path

from jarvis.config import APP_CONFIG
from jarvis.interfaces.stdio_rpc import run as run_stdio_rpc
from jarvis.interfaces.voice_self_check import round_trip as run_voice_round_trip
from jarvis.interfaces.voice_self_check import run as run_voice_self_check

VOICE_SELF_CHECK_FLAG = "--voice-self-check"
VOICE_ROUND_TRIP_FLAG = "--voice-round-trip"


def main() -> None:
    # ESR-0062 WP3 (V10): prove the build carries every part voice needs, then exit.
    if VOICE_SELF_CHECK_FLAG in sys.argv[1:]:
        sys.exit(run_voice_self_check(sys.stdout))
    # V11: with real models in the given folder, speak and hear a sentence, then exit.
    if len(sys.argv) == 3 and sys.argv[1] == VOICE_ROUND_TRIP_FLAG:
        sys.exit(run_voice_round_trip(Path(sys.argv[2]), sys.stdout))
    logging.basicConfig(
        level=APP_CONFIG.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run_stdio_rpc()


if __name__ == "__main__":
    main()
