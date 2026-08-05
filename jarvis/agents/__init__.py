"""Agent Framework: specialist capability agents serving Guardian.

Implements the `SpecialistAgent` contract scoped architecture-only at
ESR-0048 (`aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md`, "Agent
Framework" subsection, EIP-ESR0048-001). This package is the first real
code built against that contract, per EIP-ESR0049-001.

Every specialist agent is invoked only through
`jarvis.interfaces.sentinel_agent.SentinelGatedAgentService`, never
directly - the mandatory Sentinel gate MOD-0001 requires.
"""
