"""Application bootstrap for JARVIS OS First Light."""

import logging
import sys

from jarvis.config import APP_CONFIG
from jarvis.core import Jarvis
from jarvis.gui import JarvisApp


def configure_logging() -> None:
    """Configure simple application logging."""

    logging.basicConfig(
        level=APP_CONFIG.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    """Launch JARVIS OS.

    ``--ipc-stdio`` launches the JSON-RPC-over-stdio bridge (ADR-0019, ESR-0017
    WP9) instead of the Tkinter First Light GUI - the mode a Tauri sidecar
    process spawns to reach Guardian/Sentinel.
    """

    if "--ipc-stdio" in sys.argv[1:]:
        from jarvis.interfaces.stdio_rpc import run as run_stdio_rpc

        configure_logging()
        run_stdio_rpc()
        return

    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting %s.", APP_CONFIG.app_name)

    jarvis = Jarvis()
    jarvis.start()

    try:
        app = JarvisApp(jarvis)
        app.run()
    finally:
        jarvis.stop()
        logger.info("Shut down %s.", APP_CONFIG.app_name)
