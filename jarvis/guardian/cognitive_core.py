"""Guardian Cognitive Core: bounded conversation history and the retained
memory each conversation turn carries (EBG-0108 Phase 1, EIP-ESR0039-001).

EIP-ESR0039-001's first increment folded persona, retained memory and
history into one system-prompt string, deliberately deferring any change to
the shared single-turn `ProviderRequest` contract (its Section 8). ESR-0059
WP7 (EBG-0142) made that change: rendering user-authored text into the
system prompt gave it system-level authority on every later turn - a
prompt-injection path. The core now supplies history and memory as data,
and each provider adapter places them outside the system role: earlier
turns in their own user/assistant roles, retained memory as a clearly
delimited block of notes in the current user message. The system prompt
carries only the approved persona, verbatim (AAM-0001 v0.4).
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from jarvis.memory.store import PersonalMemoryRecord

DEFAULT_HISTORY_LIMIT = 6

# Prompt budgets (EBG-0143, ESR-0059 WP8). Each history entry is truncated
# to HISTORY_ENTRY_CHAR_LIMIT; retained memory notes are kept, newest first,
# up to MEMORY_NOTES_CHAR_BUDGET in total. With the RPC boundary's 4000-
# character message limit and the persona, a worst-case turn still leaves
# roughly 400 tokens of Ollama's 4096-token context for the reply, at a
# conservative 3.5 characters per token - rather than being silently
# truncated from the start. The bound is an estimate, checked by a test.
HISTORY_ENTRY_CHAR_LIMIT = 400
MEMORY_NOTES_CHAR_BUDGET = 1_500
TRUNCATION_MARKER = " [truncated]"


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - len(TRUNCATION_MARKER)] + TRUNCATION_MARKER


class GuardianCognitiveCore:
    """Tracks bounded, in-process conversation history and turns retained
    memory records into the notes each turn carries.

    History is held only in memory, scoped to the running process, exactly
    like the rest of GuardianRuntime's current state (GuardianRuntimeState,
    diagnostics) - no persistence, lost on restart.
    """

    def __init__(self, history_limit: int = DEFAULT_HISTORY_LIMIT) -> None:
        if history_limit < 1:
            msg = "Guardian Cognitive Core history_limit must be at least 1."
            raise ValueError(msg)
        self._history_limit = history_limit
        self._history: deque[tuple[str, str]] = deque(maxlen=history_limit)

    def history(self) -> tuple[tuple[str, str], ...]:
        """Return recorded (user message, Guardian reply) exchanges, oldest
        first - at most `history_limit` of them."""

        return tuple(
            (_truncate(user_message, HISTORY_ENTRY_CHAR_LIMIT), _truncate(reply, HISTORY_ENTRY_CHAR_LIMIT))
            for user_message, reply in self._history
        )

    @staticmethod
    def memory_notes(memory_records: Iterable[PersonalMemoryRecord]) -> tuple[str, ...]:
        """Return retained memory as plain notes, in stored order, within
        MEMORY_NOTES_CHAR_BUDGET (EBG-0143): the newest notes are kept first,
        so once memory outgrows the budget the oldest are left out of the
        turn - never truncated mid-note. The provider adapters frame the
        notes as data rather than instructions."""

        contents = [record.content for record in memory_records]
        kept: list[str] = []
        used = 0
        for content in reversed(contents):
            if used + len(content) > MEMORY_NOTES_CHAR_BUDGET:
                break
            kept.append(content)
            used += len(content)
        return tuple(reversed(kept))

    def record_exchange(self, user_message: str, response_message: str) -> None:
        """Record a semantically successful exchange into bounded history.

        Callers must only invoke this for genuine model replies -
        `GuardianRuntime.converse()` decides that from
        `ConversationResponse.is_model_reply` (EIP-ESR0039-001
        Implementation Requirement 6; EBG-0141). This method has no way to
        tell a model reply from any other text and trusts the caller.
        """

        self._history.append((user_message, response_message))
