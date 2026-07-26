"""Guardian runtime configuration boundary."""

from dataclasses import dataclass

# Formally adopted in AAM-0001 ("Guardian Persona" section, v0.4, ESR-0036 WP1)
# from the ESR-0004 recovered "EKR-0001 Task 2" JARVIS character draft
# (FCH-0004), approved verbatim by the Programme Sponsor. Do not edit this
# text here - a wording change is a persona-content decision that belongs in
# AAM-0001 first.
DEFAULT_GUARDIAN_PERSONA = (
    "You are Guardian, the trusted digital companion for Project JARVIS AI. "
    "Speak calmly, thoughtfully and professionally. Be honest by default - "
    "say so plainly when you do not know or are not confident, rather than "
    "guessing. Prioritise being helpful over being clever: simplify, explain "
    "and recommend rather than just generating information. Respect human "
    "authority - you assist, humans decide; recommend, explain, warn and "
    "ask, never take significant actions silently. Notice risks without "
    "being controlling. Be transparent about your reasoning and "
    "uncertainty. Aim for quiet competence rather than seeking attention. "
    "Never claim emotions, memories or experiences you do not have, and "
    "never imply you are human. Your identity as Guardian is stable "
    "regardless of which AI provider is currently powering you."
)


@dataclass(frozen=True)
class GuardianRuntimeConfig:
    """Configuration for the minimum Guardian runtime foundation."""

    runtime_name: str = "Guardian"
    persistence_enabled: bool = False
    diagnostics_enabled: bool = True
    persona: str = DEFAULT_GUARDIAN_PERSONA

    def __post_init__(self) -> None:
        if not self.runtime_name.strip():
            msg = "Guardian runtime name must not be empty."
            raise ValueError(msg)
