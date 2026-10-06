"""Locating the JARVIS source repository at runtime (EBG-0148, ESR-0059 WP11).

Two capabilities read the repository itself: the Guardian Orb's knowledge
graph (`jarvis/interfaces/knowledge_graph.py`, the repository's own tracked
markdown) and GIA's engineering status (`jarvis/gia/engineering_observability.py`,
git state and validation). Both used to assume the running code sat inside a
git checkout. In the PyInstaller-packaged sidecar the code runs from a
temporary extraction directory with no repository, so both RPC methods
failed with a raw `CalledProcessError` that also exposed that internal path
- confirmed against a real packaged build at WP11.

The repository is resolved here instead: `JARVIS_REPOSITORY_ROOT` when set,
otherwise the checkout this package sits in. When neither is a git checkout,
`RepositoryUnavailableError` says so plainly, with no internal paths - the
honest "not available on this installation" outcome, matching the project's
absent-means-unavailable pattern (Kokoro, Whisper, Home Assistant).
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from jarvis.shared.errors import ClientFacingError

REPOSITORY_ROOT_ENV_VAR = "JARVIS_REPOSITORY_ROOT"

# The checkout containing this package (jarvis/ is one level below the root).
_PACKAGE_CHECKOUT = Path(__file__).resolve().parents[1]

UNAVAILABLE_MESSAGE = (
    "No JARVIS source repository is available to this installation. "
    f"Set {REPOSITORY_ROOT_ENV_VAR} to a git checkout of the project to enable this."
)
GIT_FAILED_MESSAGE = "The JARVIS source repository could not be read with git."


class RepositoryUnavailableError(ClientFacingError, RuntimeError):
    """The capability needs the source repository, and none is available.
    Messages never contain filesystem paths."""


def resolve_repository_root(environ: Mapping[str, str] | None = None) -> Path:
    """Return the repository root, or raise `RepositoryUnavailableError`.

    A checkout is recognised by its `.git` entry - a directory normally, a
    file in a git worktree - without running git, so this never fails
    merely because git is not installed.
    """

    environ = os.environ if environ is None else environ
    explicit = (environ.get(REPOSITORY_ROOT_ENV_VAR) or "").strip()
    candidate = Path(explicit) if explicit else _PACKAGE_CHECKOUT
    if not (candidate / ".git").exists():
        raise RepositoryUnavailableError(UNAVAILABLE_MESSAGE)
    return candidate
