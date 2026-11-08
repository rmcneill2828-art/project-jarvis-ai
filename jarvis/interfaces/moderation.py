"""Moderation of a Child or Guest conversation (ESR-0061 WP6b, EIP-ESR0061-006
M1-M6, Section 6.4).

A local classifier, Meta's Llama Guard 3 (`llama-guard3:1b`) on Ollama, checks
a Child's or Guest's message before any model sees it, and the reply before it
is shown. It runs on the processor (`num_gpu` 0), never on the graphics card,
so it can never push the chat model out of the card's memory, with a fixed
4096-token context (left unset, Llama Guard allocates 131,072 tokens). The text
is checked whole, never cut to fit (M1).

**Fail closed (M3):** if the classifier is not installed, not running, too
slow or answers in a way that cannot be read, the turn is treated as unchecked
and blocked with a fixed message. A safety control that vanishes when it
breaks is not one.

**What it is and is not (M2):** Llama Guard classifies hazards (violence,
self-harm, sexual content and so on). It is not tuned to age-appropriateness,
which is what the child-safety prompt layer (S1) is for. Its verdict is
recorded as a category label only, never with the text (D23, M5).
"""

from __future__ import annotations

import json
import re
import unicodedata
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

from jarvis.shared.safe_locations import checked_http_url

DEFAULT_CLASSIFIER_MODEL = "llama-guard3:1b"
CLASSIFIER_NUM_CTX = 4096
# Generous: the first check after start loads the model from disk. The target
# for a warm check is 2 s on the PC (M1), measured in WP6d.
DEFAULT_TIMEOUT_SECONDS = 20.0

# How much text one check may hold. The classifier's context is 4096 tokens and
# must also hold Llama Guard's own instructions (about 600 tokens) and the
# question; 4,000 characters of English is well under 1,500 tokens. Longer text
# is checked in pieces of this size overlapping by 400 characters, so a
# sentence cut at one boundary is whole in the next piece.
PIECE_CHARS = 4_000
PIECE_OVERLAP_CHARS = 400
# The question shown with a reply is context only (it was checked itself as
# input); a Child's or Guest's message is at most 1,000 characters anyway.
QUESTION_CONTEXT_CHARS = 1_000

INPUT = "input"
OUTPUT = "output"

# The roles whose conversations are moderated (M3, M6).
MODERATED_ROLES = frozenset({"Child", "Guest"})

# Llama Guard 3's hazard codes (MLCommons taxonomy), as stored labels. A label
# names a kind of harm; it never carries any of the text that was checked.
CATEGORY_LABELS = {
    "S1": "violent_crimes",
    "S2": "non_violent_crimes",
    "S3": "sex_related_crimes",
    "S4": "child_sexual_exploitation",
    "S5": "defamation",
    "S6": "specialized_advice",
    "S7": "privacy",
    "S8": "intellectual_property",
    "S9": "indiscriminate_weapons",
    "S10": "hate",
    "S11": "self_harm",
    "S12": "sexual_content",
    "S13": "elections",
    "S14": "code_interpreter_abuse",
}
UNSPECIFIED = "unspecified"
UNAVAILABLE = "moderation_unavailable"
SELF_HARM = "self_harm"

# The fixed, non-generated replies (M4). A child reads these, so the exact text
# is the Programme Sponsor's, approved 7 November 2026 with WP6b
# (EIP-ESR0061-006 Section 10D). Change it only with a new approval. No
# category is ever shown.
BLOCKED_GENERAL_TEXT = "I can't help with that one. You could ask a grown-up."
BLOCKED_SELF_HARM_TEXT = (
    "That sounds like something to talk about with someone you trust, like a parent, a carer or a teacher. "
    "If you want to talk to someone right now, you can call Childline for free on 0800 1111. "
    "If you or someone else is in danger, tell a grown-up straight away or call 999."
)
UNAVAILABLE_TEXT = "I can't check that it is safe to answer right now, so please ask a grown-up."

# A Guest may be an adult, so a Guest gets a neutral set (Sponsor, 7 Nov 2026).
# Approved with the Child set above.
GUEST_BLOCKED_GENERAL_TEXT = "I can't help with that on this computer."
GUEST_BLOCKED_SELF_HARM_TEXT = (
    "If you're struggling, you don't have to deal with it alone. You can call Samaritans for free, any time, "
    "on 116 123. If you or someone else is in danger, call 999."
)
GUEST_UNAVAILABLE_TEXT = "I can't check that it is safe to answer right now, so I can't reply. Please try again later."

# The child-safety prompt layer (S1), appended to the approved persona for a
# Child profile only, because the classifier does not judge age-appropriateness
# (M2). It changes what the approved persona says to a child, so its exact text
# was approved by the Programme Sponsor (7 November 2026, WP6b) and is recorded
# in AAM-0001 0.10 (EIP-ESR0061-006 6.5).
CHILD_SAFETY_LAYER = (
    "You are talking with a child. Use short, kind, simple words. If a question is about something unsuitable "
    "for a child, or about hurting someone or themselves, say you can't help with that and suggest they ask a "
    "trusted grown-up. Never pretend to be a person. Never ask for their full name, address, school or phone "
    "number, and if they offer them, tell them to keep them private."
)
# The approved persona calls the person "Sir"; a child is called by their first
# name instead (Sponsor, 7 Nov 2026). The name goes only to the local model: a
# question sent to Claude gets the nameless line, so a child's name never
# leaves the computer through this layer.
CHILD_NAME_LINE = "Call them {name}, not Sir."
CHILD_NO_NAME_LINE = "Do not call them Sir."
CHILD_NAME_MAX_CHARS = 40
# The first name only: the first word of the display name, and only if it is
# letters (a hyphen or apostrophe may join letters, as in Anne-Marie or
# O'Neill). One word cannot carry an instruction into the persona the way a
# 40-character phrase could (WP6b post-commit review, Low L1; WP6d).
_FIRST_NAME = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")


def child_first_name(name: str | None) -> str | None:
    """The child's first name as the persona may use it, or None."""

    # Composed form first, so "Zoë" typed as "Zoe" plus a combining mark is
    # still one word of letters (WP6d review, Low).
    words = unicodedata.normalize("NFC", name or "").split()
    if not words:
        return None
    first = words[0]
    if len(first) > CHILD_NAME_MAX_CHARS or _FIRST_NAME.fullmatch(first) is None:
        return None
    return first


def child_safety_layer(name: str | None) -> str:
    """The S1 layer, naming the child by their first name when it is one."""

    first = child_first_name(name)
    line = CHILD_NAME_LINE.format(name=first) if first else CHILD_NO_NAME_LINE
    return f"{CHILD_SAFETY_LAYER} {line}"


@dataclass(frozen=True)
class ModerationVerdict:
    """Allowed, or blocked with a category label. `checked` is False when the
    classifier could not give a verdict (then `allowed` is always False)."""

    allowed: bool
    category: str | None = None
    checked: bool = True

    @property
    def unavailable(self) -> bool:
        return not self.checked


ALLOW = ModerationVerdict(allowed=True)
UNCHECKED = ModerationVerdict(allowed=False, category=UNAVAILABLE, checked=False)


def blocked_text(verdict: ModerationVerdict, role: str | None = "Child") -> str:
    """The fixed reply for a blocked turn (M4): the Child set, or the neutral
    set for a Guest."""

    guest = role == "Guest"
    if verdict.unavailable:
        return GUEST_UNAVAILABLE_TEXT if guest else UNAVAILABLE_TEXT
    if verdict.category == SELF_HARM:
        return GUEST_BLOCKED_SELF_HARM_TEXT if guest else BLOCKED_SELF_HARM_TEXT
    return GUEST_BLOCKED_GENERAL_TEXT if guest else BLOCKED_GENERAL_TEXT


def split_for_checking(text: str) -> list[str]:
    """`text` whole if it fits one check, else overlapping pieces that cover
    every character (WP6b review M-1)."""

    step = PIECE_CHARS - PIECE_OVERLAP_CHARS
    pieces = []
    start = 0
    while True:
        pieces.append(text[start : start + PIECE_CHARS])
        if start + PIECE_CHARS >= len(text):
            return pieces
        start += step


def parse_verdict(content: object) -> ModerationVerdict:
    """Read Llama Guard's answer: "safe", or "unsafe" then category codes.

    Strict, because the text under test is written by the person being
    protected and may try to steer the classifier: only a first line that is
    exactly "safe" allows the turn. "unsafe" blocks it (by its first listed
    category, self-harm first if present). Anything else - empty, a refusal,
    extra prose - cannot be read and fails closed.
    """

    if not isinstance(content, str):
        return UNCHECKED
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    if not lines:
        return UNCHECKED
    first = lines[0].lower()
    if first == "safe":
        return ALLOW
    if first != "unsafe":
        return UNCHECKED
    codes = re.findall(r"\bS(\d{1,2})\b", " ".join(lines[1:2]))
    labels = [CATEGORY_LABELS.get(f"S{code}", UNSPECIFIED) for code in codes]
    if SELF_HARM in labels:
        return ModerationVerdict(allowed=False, category=SELF_HARM)
    return ModerationVerdict(allowed=False, category=labels[0] if labels else UNSPECIFIED)


Transport = Callable[[str, bytes, float], bytes]


def _default_transport(url: str, body: bytes, timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


class ModerationService:
    """The classifier over Ollama's `/api/chat`."""

    def __init__(
        self,
        endpoint: str,
        model: str = DEFAULT_CLASSIFIER_MODEL,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        transport: Transport | None = None,
    ) -> None:
        # Only http:// or https:// (ESR-0062 WP2, F3): urllib would open file://.
        self._endpoint = checked_http_url(endpoint).rstrip("/")
        self._model = model
        self._timeout = timeout_seconds
        self._transport = transport or _default_transport

    @property
    def model(self) -> str:
        return self._model

    def _ask(self, messages: list[dict[str, str]]) -> ModerationVerdict:
        body = json.dumps(
            {
                "model": self._model,
                "messages": messages,
                "stream": False,
                # On the processor, a fixed context, and a short deterministic answer.
                "options": {"num_gpu": 0, "num_ctx": CLASSIFIER_NUM_CTX, "temperature": 0, "num_predict": 16},
            }
        ).encode("utf-8")
        try:
            raw = self._transport(f"{self._endpoint}/api/chat", body, self._timeout)
            payload = json.loads(raw)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError):
            # Not installed, not running, too slow, or not JSON: unchecked.
            return UNCHECKED
        if not isinstance(payload, dict) or payload.get("error"):
            return UNCHECKED
        message = payload.get("message")
        return parse_verdict(message.get("content") if isinstance(message, dict) else None)

    def _check_pieces(self, text: str, ask: Callable[[str], ModerationVerdict]) -> ModerationVerdict:
        """Check `text` whole if it fits, else in overlapping pieces that each
        fit, so nothing is ever cut off unchecked (WP6b review, Copilot Medium
        M-1: a long reply could overflow the classifier's context, which Ollama
        silently shortens). Any piece that cannot be checked fails the whole
        closed; any unsafe piece blocks it, self-harm first."""

        verdicts = [ask(piece) for piece in split_for_checking(text)]
        if any(verdict.unavailable for verdict in verdicts):
            return UNCHECKED
        unsafe = [verdict for verdict in verdicts if not verdict.allowed]
        if not unsafe:
            return ALLOW
        return next((verdict for verdict in unsafe if verdict.category == SELF_HARM), unsafe[0])

    def check_input(self, text: str) -> ModerationVerdict:
        """A person's message, before any model is called."""

        if not text.strip():
            return ALLOW
        return self._check_pieces(text, lambda piece: self._ask([{"role": "user", "content": piece}]))

    def check_output(self, question: str, reply: str) -> ModerationVerdict:
        """A model's reply, judged as the answer to `question`, before it is shown."""

        if not reply.strip():
            return ALLOW
        asked = question[:QUESTION_CONTEXT_CHARS]
        return self._check_pieces(
            reply,
            lambda piece: self._ask([{"role": "user", "content": asked}, {"role": "assistant", "content": piece}]),
        )


__all__ = [
    "BLOCKED_GENERAL_TEXT",
    "BLOCKED_SELF_HARM_TEXT",
    "CATEGORY_LABELS",
    "CHILD_SAFETY_LAYER",
    "DEFAULT_CLASSIFIER_MODEL",
    "GUEST_BLOCKED_GENERAL_TEXT",
    "GUEST_BLOCKED_SELF_HARM_TEXT",
    "GUEST_UNAVAILABLE_TEXT",
    "INPUT",
    "MODERATED_ROLES",
    "OUTPUT",
    "UNAVAILABLE_TEXT",
    "UNCHECKED",
    "ModerationService",
    "ModerationVerdict",
    "blocked_text",
    "child_safety_layer",
    "parse_verdict",
]
