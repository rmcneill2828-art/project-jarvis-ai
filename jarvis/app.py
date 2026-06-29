"""Application bootstrap for JARVIS OS First Light."""

import logging

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
    """Launch JARVIS OS."""

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
