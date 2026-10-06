"""Errors whose message is written for the person using JARVIS (ESR-0061
WP2a, EBG-0157 item 2).

`StdioRpcServer.handle_line()` returns a `ClientFacingError`'s message to the
UI unchanged - the UI shows it - and for **any other** exception returns only
a fixed sentence naming the exception type, logging the detail locally. So an
internal message can never reach the screen by accident, and a user-facing
error raised without one of these classes fails safe: the person sees the
generic sentence, never internal detail.

Each concrete class also subclasses the builtin it replaces, so existing
callers that catch `TypeError`, `ValueError`, `KeyError`, `PermissionError`
or `RuntimeError` behave exactly as before.
"""

from __future__ import annotations


class ClientFacingError(Exception):
    """Marker: this exception's message is safe and meant to be shown."""


class ClientFacingTypeError(ClientFacingError, TypeError):
    pass


class ClientFacingValueError(ClientFacingError, ValueError):
    pass


class ClientFacingKeyError(ClientFacingError, KeyError):
    pass


class ClientFacingPermissionError(ClientFacingError, PermissionError):
    pass


class ClientFacingRuntimeError(ClientFacingError, RuntimeError):
    pass


def public_type_name(exc: BaseException) -> str:
    """The type name a reply shows. The `ClientFacing*` wrappers above report
    the builtin they stand in for (`TypeError` for `ClientFacingTypeError`), so
    the text the UI shows is unchanged; any other client-facing class, such as
    `RepositoryUnavailableError`, keeps its own name."""

    if type(exc).__module__ == __name__:
        for cls in type(exc).__mro__:
            if cls.__module__ == "builtins":
                return cls.__name__
    return type(exc).__name__
