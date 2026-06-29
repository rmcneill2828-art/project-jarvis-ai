"""Application settings for JARVIS OS."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Static application configuration."""

    app_name: str = "JARVIS OS"
    window_title: str = "JARVIS OS - First Light"
    log_level: int = 20


APP_CONFIG = AppConfig()
