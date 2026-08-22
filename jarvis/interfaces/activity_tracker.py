"""Real backend RPC-activity tracker for the Guardian Orb's Phase 2 cluster
illumination (EBG-0121, [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]]
Section 8.1: "architectural clusters ... illuminate as the systems they
represent are accessed").

`knowledge_graph.py`'s `_cluster_for` already assigns each repository node a
coarse cluster (top-level directory) as a Phase 1 byproduct. This module maps
each real, dispatched JSON-RPC method (`stdio_rpc.py`'s `_methods` dict) to
the cluster that actually implements it, and records genuinely-observed
dispatch activity - never a simulated or decorative signal, per the
no-mock-fallback rule (ESR-0017 WP9). A method being recorded means that RPC
capability was genuinely dispatched and its handler returned successfully;
it is not a claim that any downstream provider call within that handler
(e.g. an external voice/model provider) itself succeeded.
"""

from __future__ import annotations

import threading
import time

# Cluster mapping mirrors where each method's real implementation lives, not
# merely where its RPC handler happens to be defined in this bridge file -
# voice methods map to "sentinel" because `PiperProvider`/`WhisperProvider`
# actually live there, reached via the Sentinel-gated voice adapters; every
# other method's real implementation lives under `jarvis/`. Must cover every
# key in `StdioRpcServer._methods` exactly - see
# `test_method_clusters_covers_every_dispatched_rpc_method` for the
# coverage test enforcing this (Codex design-review requirement,
# EIP-ESR0051-002).
METHOD_CLUSTERS: dict[str, str] = {
    "guardian.converse": "jarvis",
    "guardian.speak": "sentinel",
    "guardian.transcribe": "sentinel",
    "guardian.agent.list": "jarvis",
    "guardian.agent.invoke": "jarvis",
    "platform.status": "jarvis",
    "knowledge.graph": "jarvis",
    "memory.propose": "jarvis",
    "memory.approve": "jarvis",
    "memory.deny": "jarvis",
    "memory.list": "jarvis",
    "profile.list": "jarvis",
    "profile.create": "jarvis",
    "profile.select": "jarvis",
    "profile.active": "jarvis",
    "gia.status": "jarvis",
}


class ActivityTracker:
    """Tracks "is this cluster active right now", not a history log.

    Two independent interfaces over the same underlying state: `pop_pending`
    (push - `serve_forever` drains newly-recorded events to emit
    notifications) and `recent_clusters` (pull - `knowledge.graph` reports
    the current active set on each fetch). Guards only its own mutable
    state with `_lock`, held solely for the state update itself - never
    across a blocking write to any stream. `StdioRpcServer`'s own
    `_write_lock` is a separate lock for a separate purpose (serialising
    stdout writes); the two must never be acquired nested or held
    simultaneously across a blocking call (Codex design-review requirement,
    EIP-ESR0051-002).
    """

    def __init__(self, clock=time.monotonic) -> None:
        self._clock = clock
        self._lock = threading.Lock()
        self._last_seen: dict[str, float] = {}
        self._pending: list[tuple[str, str]] = []

    def record(self, method: str) -> str | None:
        """Record a successfully-dispatched RPC method's activity.

        Returns the cluster it maps to, or None if `method` has no mapping
        (never raises - an unmapped method simply does not illuminate
        anything, rather than breaking the request it was recorded from).
        """

        cluster = METHOD_CLUSTERS.get(method)
        if cluster is None:
            return None
        with self._lock:
            self._last_seen[cluster] = self._clock()
            self._pending.append((method, cluster))
        return cluster

    def pop_pending(self) -> list[tuple[str, str]]:
        """Drain and return `(method, cluster)` pairs recorded since the last
        call - the push-channel interface `serve_forever` consumes to decide
        which `knowledge.cluster_activity` notifications to emit."""

        with self._lock:
            pending, self._pending = self._pending, []
        return pending

    def recent_clusters(self, window_seconds: float = 30.0) -> list[str]:
        """Sorted list of clusters with activity within the last
        `window_seconds` - the pull interface `knowledge.graph` consumes so
        a UXP session that mounts mid-activity is not shown a falsely-idle
        Orb."""

        with self._lock:
            now = self._clock()
            return sorted(cluster for cluster, seen in self._last_seen.items() if now - seen <= window_seconds)
