"""Standalone entry point for the PyInstaller-packaged Guardian sidecar.

Unlike ``jarvis.app.main()`` (which also supports the legacy Tkinter
First Light GUI via an unconditional ``from jarvis.gui import
JarvisApp`` at module load time), this entry point always runs the
stdio JSON-RPC bridge - the only mode a Tauri sidecar process ever
needs (EIP-ESR0032-001). Kept as a separate script so the packaged
sidecar never has to bundle Tkinter for a headless backend.
"""

import logging

from jarvis.config import APP_CONFIG
from jarvis.interfaces.stdio_rpc import run as run_stdio_rpc


def main() -> None:
    logging.basicConfig(
        level=APP_CONFIG.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run_stdio_rpc()


if __name__ == "__main__":
    main()
