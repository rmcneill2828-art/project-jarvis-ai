"""`GiaEngineeringAgent`: the second real `SpecialistAgent` (EIP-ESR0054-002;
extended by EIP-ESR0055-001).

Wraps `jarvis.gia.engineering_observability.EngineeringStateObserver`'s
read-only engineering-state snapshot (git state, repository health,
register state) as a `SpecialistAgent`, mirroring
`jarvis.agents.gia_agent.GiaObservabilityAgent`'s own shape exactly.
Classifies `ROUTINE_INTERACTION` under MOD-0001's Agent Framework rule -
it only reads and reports repository state, touching no local device
or system state, exactly the "observation is not control" distinction
`aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` Section
8A.1 already draws for GIA. This agent never approaches
`TrustCategory.LOCAL_AGENT_ACTION`.

A second, pre-existing, ungated `gia.engineeringStatus` JSON-RPC method
(`jarvis/interfaces/stdio_rpc.py`) already exposes the same underlying
snapshot directly - unaffected by this module, since GIA observation does
not go through Sentinel's request path at all per GAM-0001 8A.1. This
agent is an additional, Sentinel-gated path, matching
`GiaObservabilityAgent`'s own precedent for `gia.status`.
"""

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.gia.engineering_observability import EngineeringStateObserver

STATUS_REPORTED = "reported"


class GiaEngineeringAgent:
    """Specialist agent reporting GIA's real engineering (git) state snapshot."""

    name = "gia-engineering"

    def __init__(self, observer: EngineeringStateObserver) -> None:
        # Constructor-injected, not constructed internally - matches every
        # existing provider/agent's dependency-injection pattern, keeping
        # this agent unit-testable with a fake observer.
        self._observer = observer

    def execute(self, request: AgentRequest) -> AgentResult:
        """Return GIA's current engineering (git) state snapshot as an
        `AgentResult`.

        `request` is accepted for contract conformance; this agent takes
        no parameters and reports the same snapshot regardless of task
        text, matching `EngineeringStateObserver.snapshot()`'s own
        no-arguments shape.
        """

        snapshot = self._observer.snapshot()
        payload = {
            "gitBranch": snapshot.git_branch,
            "gitUncommittedFiles": str(snapshot.git_uncommitted_files),
            "gitLastCommitSha": snapshot.git_last_commit_sha,
            "gitLastCommitMessage": snapshot.git_last_commit_message,
            "repositoryValidationErrors": str(snapshot.repository_validation_errors),
            "repositoryValidationWarnings": str(snapshot.repository_validation_warnings),
            "currentRepositoryBaseline": snapshot.current_repository_baseline,
            "latestRegisteredSession": snapshot.latest_registered_session,
            "latestRegisteredSessionStatus": snapshot.latest_registered_session_status,
            "capturedAt": snapshot.captured_at.isoformat(),
        }
        return AgentResult(status=STATUS_REPORTED, payload=payload)
