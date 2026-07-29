"""Guardian Cognitive Core: composes persona, retained memory and bounded
conversation history into a single system-prompt string (EBG-0108 Phase 1,
EIP-ESR0039-001).

Deliberately folds everything into the existing `ConversationRequest.persona`
/ `ProviderRequest.system_prompt` channel rather than changing either
dataclass or any provider adapter - `ProviderRequest` is single-turn only and
shared by every adapter (OpenAI, Gemini, Ollama, LocalEcho); restructuring
that shared contract is out of scope for this first increment
(EIP-ESR0039-001 Section 8).
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from jarvis.memory.store import PersonalMemoryRecord

DEFAULT_HISTORY_LIMIT = 6

_MEMORY_SECTION_HEADING = "Retained Memory:"
_HISTORY_SECTION_HEADING = "Recent Conversation:"


class GuardianCognitiveCore:
    """Composes each conversation turn's system-prompt text and tracks
    bounded, in-process conversation history.

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

    def compose(self, persona: str, memory_records: Iterable[PersonalMemoryRecord] = ()) -> str:
        """Compose the full system-prompt text for the next turn.

        Persona text is prepended unchanged - never reworded (AAM-0001 v0.4
        persona text is Programme Sponsor-approved verbatim). The memory and
        history sections are omitted entirely, not rendered empty, when
        there is nothing to include, so a fresh runtime with no retained
        memory and no prior exchanges composes byte-identical text to
        persona-only behaviour.
        """

        sections = [persona]

        memory_section = self._render_memory_section(memory_records)
        if memory_section is not None:
            sections.append(memory_section)

        history_section = self._render_history_section()
        if history_section is not None:
            sections.append(history_section)

        return "\n\n".join(sections)

    def record_exchange(self, user_message: str, response_message: str) -> None:
        """Record a semantically successful exchange into bounded history.

        Callers must only invoke this for exchanges that are not one of
        GuardianRuntime's boundary-error responses or
        SentinelGatedConversationProvider's Sentinel-denial/provider-failure
        responses (EIP-ESR0039-001 Implementation Requirement 6) - this
        method has no way to distinguish those from a genuine model reply
        and trusts the caller's own exclusion check.
        """

        self._history.append((user_message, response_message))

    def _render_memory_section(self, memory_records: Iterable[PersonalMemoryRecord]) -> str | None:
        contents = [record.content for record in memory_records]
        if not contents:
            return None
        lines = [_MEMORY_SECTION_HEADING, *[f"- {content}" for content in contents]]
        return "\n".join(lines)

    def _render_history_section(self) -> str | None:
        if not self._history:
            return None
        lines = [_HISTORY_SECTION_HEADING]
        for user_message, response_message in self._history:
            lines.append(f"User: {user_message}")
            lines.append(f"Guardian: {response_message}")
        return "\n".join(lines)
