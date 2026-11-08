"""Checks on locations a caller supplies (ESR-0062 WP2, EIP-ESR0062-002 F1, F3).

`checked_user_path` guards the export, backup and restore RPCs: the screens
pass a path chosen in the native file dialog, but the backend must not take
any string as given (WR-ESR0061-002 F1). `checked_http_url` guards every
configured service address, because `urllib` would otherwise open `file://`
(F3). A refusal names the reason, never the path or the address, which may
hold a user name or password.
"""

from __future__ import annotations

import ntpath
import os
import socket
import sys
import urllib.parse
from collections.abc import Mapping
from pathlib import Path

from jarvis.shared.errors import ClientFacingValueError

SYSTEM_LOCATION_MESSAGE = "JARVIS does not use system folders for this. Choose another location."


# -- Service addresses (F3) ---------------------------------------------------


def checked_http_url(url: str) -> str:
    """Return `url` if it is an http:// or https:// address with a host name;
    raise ValueError otherwise (the message never repeats the address)."""

    try:
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname
    except ValueError:
        hostname = None
        parsed = None
    if parsed is None or parsed.scheme.lower() not in {"http", "https"} or not hostname:
        msg = "The address must start with http:// or https:// and name a host."
        raise ValueError(msg)
    return url


# -- Caller-supplied paths (F1) -----------------------------------------------


def system_locations(platform: str, environ: Mapping[str, str], home: Path) -> list[str]:
    """The folders JARVIS never reads from or writes to for a caller."""

    if platform == "win32":
        system_drive = environ.get("SystemDrive", "C:")
        roaming = environ.get("APPDATA", str(home / "AppData" / "Roaming"))
        return [
            environ.get("SystemRoot", system_drive + "\\Windows"),
            environ.get("ProgramFiles", system_drive + "\\Program Files"),
            environ.get("ProgramFiles(x86)", system_drive + "\\Program Files (x86)"),
            environ.get("ProgramW6432", system_drive + "\\Program Files"),
            environ.get("ProgramData", system_drive + "\\ProgramData"),
            # The whole per-user Start Menu, which holds the Startup folder.
            roaming + "\\Microsoft\\Windows\\Start Menu",
        ]
    if platform == "darwin":
        return [
            "/System",
            "/Library",
            "/Applications",
            "/usr",
            "/bin",
            "/sbin",
            "/etc",
            "/private/etc",
            "/private/var/db",
            str(home / "Library" / "LaunchAgents"),
        ]
    return ["/etc", "/usr", "/bin", "/sbin", "/boot", "/proc", "/sys", str(home / ".config" / "autostart")]


def _fold(path: str, platform: str) -> str:
    if platform == "win32":
        # ntpath, not os.path: Windows rules on whatever computer runs the check.
        return ntpath.normcase(path).rstrip("\\")
    if platform == "darwin":
        return path.casefold().rstrip("/")
    return path.rstrip("/")


def is_inside(path: str, roots: list[str], platform: str) -> bool:
    """Whether `path` is one of `roots` or inside one, compared the way the
    platform's file system does (case-insensitive on Windows and macOS)."""

    separator = "\\" if platform == "win32" else "/"
    folded = _fold(path, platform)
    for root in roots:
        folded_root = _fold(root, platform)
        if folded_root and (folded == folded_root or folded.startswith(folded_root + separator)):
            return True
    return False


def _strip_extended_prefix(path: str) -> str:
    """`os.path.realpath` may return an extended-length form on Windows; read
    it as the ordinary path it names before testing it."""

    if path.startswith("\\\\?\\UNC\\"):
        return "\\\\" + path[len("\\\\?\\UNC\\") :]
    if path.startswith("\\\\?\\"):
        return path[len("\\\\?\\") :]
    return path


def is_device_or_local_share(path: str, platform: str) -> bool:
    """A Windows device or extended-length path, or a network path back to
    this computer (which would reach its administrative shares)."""

    if platform != "win32":
        return False
    normal = path.replace("/", "\\")
    if normal.startswith(("\\\\?\\", "\\\\.\\")):
        return True
    if normal.startswith("\\\\"):
        host = normal[2:].split("\\", 1)[0].casefold()
        local_names = {"localhost", "127.0.0.1", "::1", "0:0:0:0:0:0:0:1", socket.gethostname().casefold()}
        return host in local_names or host.startswith("127.")
    return False


def checked_user_path(raw: str, *, kind: str) -> Path:
    """Return `raw` as a Path if it is a safe location a caller may use.

    `kind` is "directory" (export, backup) or "file" (restore). The path must
    be absolute, must exist as that kind, must not itself be a link or
    junction, must not be a device path or a network path back to this
    computer, and neither it nor what it resolves to may be inside a system
    location. Raises ClientFacingValueError naming the reason, never the path.
    """

    if kind not in {"directory", "file"}:
        msg = f"Unknown kind {kind!r}."
        raise ValueError(msg)
    if "\x00" in raw:
        msg = "That location is not valid."
        raise ClientFacingValueError(msg)
    platform = sys.platform
    path = Path(raw)
    if not path.is_absolute():
        msg = "Choose a full location, not a relative one."
        raise ClientFacingValueError(msg)
    if is_device_or_local_share(raw, platform):
        msg = "That location cannot be used. Choose a folder on this computer or another one."
        raise ClientFacingValueError(msg)
    try:
        exists = path.is_dir() if kind == "directory" else path.is_file()
        if not exists:
            msg = "That folder does not exist." if kind == "directory" else "That file does not exist."
            raise ClientFacingValueError(msg)
        if os.path.islink(path) or os.path.isjunction(path):
            msg = "A link cannot be used here. Choose the folder or file itself."
            raise ClientFacingValueError(msg)
        resolved = _strip_extended_prefix(os.path.realpath(path))
    except (OSError, ValueError) as exc:
        if isinstance(exc, ClientFacingValueError):
            raise
        msg = "That location cannot be used."
        raise ClientFacingValueError(msg) from exc
    if is_device_or_local_share(resolved, platform):
        msg = "That location cannot be used. Choose a folder on this computer or another one."
        raise ClientFacingValueError(msg)
    roots = system_locations(platform, os.environ, Path.home())
    if is_inside(str(path), roots, platform) or is_inside(resolved, roots, platform):
        raise ClientFacingValueError(SYSTEM_LOCATION_MESSAGE)
    return path
