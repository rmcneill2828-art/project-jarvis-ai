"""Tests for jarvis/gui/app.py's pure helper functions.

Deliberately does not instantiate JarvisApp itself - that requires a real
Tkinter root window, which this suite avoids for CI portability. Only the
extracted, dependency-free `_transcript_filename()` helper is exercised.
"""

from __future__ import annotations

import re

from jarvis.gui.app import _transcript_filename
from jarvis.interfaces.conversation import TRANSCRIPT_FORMAT_MARKDOWN, TRANSCRIPT_FORMAT_TEXT

_FILENAME_PATTERN = re.compile(r"^jarvis_transcript_\d{8}_\d{6}\d{6}(\.md|\.txt)$")


def test_transcript_filename_uses_markdown_extension() -> None:
    name = _transcript_filename(TRANSCRIPT_FORMAT_MARKDOWN)

    assert name.endswith(".md")
    assert _FILENAME_PATTERN.match(name)


def test_transcript_filename_uses_text_extension() -> None:
    name = _transcript_filename(TRANSCRIPT_FORMAT_TEXT)

    assert name.endswith(".txt")
    assert _FILENAME_PATTERN.match(name)


def test_transcript_filename_has_microsecond_resolution() -> None:
    """EBG-0105 (ESR-0033 WP6): two exports triggered within the same
    wall-clock second must not collide - the timestamp component now
    carries 6 digits of sub-second (microsecond) resolution, not just
    the prior second-level %Y%m%d_%H%M%S."""

    name = _transcript_filename(TRANSCRIPT_FORMAT_MARKDOWN)
    timestamp = name.removeprefix("jarvis_transcript_").removesuffix(".md")

    # %Y%m%d_%H%M%S%f -> 8 + 1 + 6 + 6 = 21 characters.
    assert len(timestamp) == 21
    assert timestamp[8] == "_"
