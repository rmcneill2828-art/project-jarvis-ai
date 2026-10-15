"""The operating system's credential store, behind one small interface.

ESR-0061 WP5a (EIP-ESR0061-005 6.1, decision K1). The Claude API key a person
types into the app is kept in the Windows Credential Manager or the macOS
Keychain through the `keyring` package. Nothing else in the code imports
`keyring`, so a secret has exactly one route in and one route out.

Rules this module keeps (STD-0006):

* A value is never logged, never put in an exception message, and never
  returned by anything but `get`. Failures raise `SecretStoreError` with a
  fixed message.
* No usable store means `available` is False and every operation refuses; it
  never falls back to a file (decision K2).
* The platform backend is chosen explicitly rather than by entry-point
  discovery, which a one-file PyInstaller build cannot be relied on to carry.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, Protocol

logger = logging.getLogger(__name__)

SERVICE_NAME = "jarvis-guardian"

# Backends that exist so that keyring "works" without storing anything.
_INERT_BACKEND_MODULES = frozenset({"keyring.backends.fail", "keyring.backends.null"})


class SecretStoreError(RuntimeError):
    """The store could not do what was asked. The message never holds a value."""


class _Backend(Protocol):
    def get_password(self, service: str, username: str) -> str | None: ...

    def set_password(self, service: str, username: str, password: str) -> None: ...

    def delete_password(self, service: str, username: str) -> None: ...


def _platform_backend() -> Any | None:
    """The operating system's own keyring backend, or None if there is none."""

    try:
        if sys.platform == "win32":
            from keyring.backends.Windows import WinVaultKeyring

            return WinVaultKeyring()
        if sys.platform == "darwin":
            from keyring.backends.macOS import Keyring

            return Keyring()
        import keyring

        return keyring.get_keyring()
    except Exception:  # noqa: BLE001 - any import or construction failure means "no store"
        logger.warning("No operating system credential store could be loaded.")
        return None


def _is_usable(backend: Any | None) -> bool:
    if backend is None:
        return False
    module = type(backend).__module__
    if module in _INERT_BACKEND_MODULES:
        return False
    # keyring marks a backend it cannot use with a non-positive priority.
    priority = getattr(backend, "priority", 1)
    try:
        return float(priority) > 0
    except (TypeError, ValueError):
        return True


class SecretStore:
    """Get, set and delete named secrets for this application."""

    def __init__(self, backend: _Backend | None = None, *, service: str = SERVICE_NAME, use_platform: bool = True):
        """`backend` is injectable for tests. With none given, the platform's
        own is used when `use_platform` is true; an `unavailable()` store sets
        it false and has no backend at all."""

        if backend is None and use_platform:
            backend = _platform_backend()
        self._backend = backend if _is_usable(backend) else None
        self._service = service

    @classmethod
    def unavailable(cls) -> SecretStore:
        """A store that holds nothing and never touches the host's credentials
        (what tests and a machine without a secure store use)."""

        return cls(use_platform=False)

    @property
    def available(self) -> bool:
        return self._backend is not None

    def get(self, name: str) -> str | None:
        if self._backend is None:
            return None
        try:
            value = self._backend.get_password(self._service, name)
        except Exception as exc:  # noqa: BLE001
            raise SecretStoreError("The credential store could not be read.") from _drop(exc)
        return value if isinstance(value, str) and value.strip() else None

    def set(self, name: str, value: str) -> None:
        if self._backend is None:
            raise SecretStoreError("This computer has no secure credential store.")
        if not isinstance(value, str) or not value.strip():
            raise SecretStoreError("A secret must not be empty.")
        try:
            self._backend.set_password(self._service, name, value)
        except Exception as exc:  # noqa: BLE001
            raise SecretStoreError("The credential store could not be written.") from _drop(exc)

    def delete(self, name: str) -> None:
        """Remove a secret; removing one that is not there is not an error."""

        if self._backend is None:
            return
        try:
            self._backend.delete_password(self._service, name)
        except Exception as exc:  # noqa: BLE001
            if type(exc).__name__ == "PasswordDeleteError":
                return
            raise SecretStoreError("The credential store could not be changed.") from _drop(exc)


def _drop(exc: BaseException) -> None:
    """Chain nothing: a backend's own message or traceback could hold the value
    (`raise ... from None` semantics, written as a value so the call sites read
    as one line). The exception type is logged, never its text."""

    logger.warning("Credential store operation failed (%s).", type(exc).__name__)


__all__ = ["SERVICE_NAME", "SecretStore", "SecretStoreError"]
