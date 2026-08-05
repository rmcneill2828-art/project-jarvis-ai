"""`GiaObservabilityAgent`: the first real `SpecialistAgent`.

Wraps `jarvis.gia.observability.LocalResourceObserver`'s existing
read-only local resource snapshot (CPU/memory/disk/process health,
`psutil`-backed since ESR-0012/ESR-0029) as a `SpecialistAgent`. Classifies
`ROUTINE_INTERACTION` under MOD-0001's Agent Framework rule - it only
reads and reports local state, touching no local device or system state,
exactly the "observation is not control" distinction
`aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` Section
8A.1 already draws for GIA. This agent never approaches
`TrustCategory.LOCAL_AGENT_ACTION`.

A second, pre-existing, ungated `gia.status` JSON-RPC method
(`jarvis/interfaces/stdio_rpc.py`) already exposes the same underlying
snapshot directly - unaffected by this module, since GIA observation does
not go through Sentinel's request path at all per GAM-0001 8A.1. This
agent is an additional, Sentinel-gated path demonstrating the Agent
Framework contract against a real capability, not a replacement.
"""

from jarvis.agents.contracts import AgentRequest, AgentResult
from jarvis.gia.observability import LocalResourceObserver

STATUS_REPORTED = "reported"


class GiaObservabilityAgent:
    """Specialist agent reporting GIA's real local resource snapshot."""

    name = "gia-observability"

    def __init__(self, observer: LocalResourceObserver) -> None:
        # Constructor-injected, not constructed internally - matches every
        # existing provider's dependency-injection pattern (Engineering
        # Reviewer design-review requirement on EIP-ESR0049-001), keeping
        # this agent unit-testable with a fake observer.
        self._observer = observer

    def execute(self, request: AgentRequest) -> AgentResult:
        """Return GIA's current local resource snapshot as an `AgentResult`.

        `request` is accepted for contract conformance; this agent takes
        no parameters and reports the same snapshot regardless of task
        text, matching `LocalResourceObserver.snapshot()`'s own
        no-arguments shape.
        """

        snapshot = self._observer.snapshot()
        payload = {
            "cpuPercent": str(snapshot.cpu_percent),
            "memoryPercent": str(snapshot.memory_percent),
            "memoryUsedMb": str(snapshot.memory_used_mb),
            "memoryTotalMb": str(snapshot.memory_total_mb),
            "diskPercent": str(snapshot.disk_percent),
            "diskUsedGb": str(snapshot.disk_used_gb),
            "diskTotalGb": str(snapshot.disk_total_gb),
            "processStatus": snapshot.process_status,
            "processUptimeSeconds": str(snapshot.process_uptime_seconds),
            "processCpuPercent": str(snapshot.process_cpu_percent),
            "processMemoryMb": str(snapshot.process_memory_mb),
            "capturedAt": snapshot.captured_at.isoformat(),
        }
        return AgentResult(status=STATUS_REPORTED, payload=payload)
