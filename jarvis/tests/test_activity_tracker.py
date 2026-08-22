"""Tests for the Guardian Orb Phase 2 activity tracker (EBG-0121,
EIP-ESR0051-002)."""

from jarvis.interfaces.activity_tracker import METHOD_CLUSTERS, ActivityTracker
from jarvis.interfaces.stdio_rpc import StdioRpcServer


class _FakeClock:
    """Deterministic monotonic-style clock: advances only when told to."""

    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now


def test_record_returns_mapped_cluster_and_marks_it_active():
    tracker = ActivityTracker(clock=_FakeClock())

    cluster = tracker.record("guardian.speak")

    assert cluster == "sentinel"
    assert tracker.recent_clusters() == ["sentinel"]


def test_record_returns_none_for_unmapped_method_and_records_nothing():
    tracker = ActivityTracker(clock=_FakeClock())

    cluster = tracker.record("not.a.real.method")

    assert cluster is None
    assert tracker.recent_clusters() == []
    assert tracker.pop_pending() == []


def test_pop_pending_drains_and_returns_recorded_events_once():
    tracker = ActivityTracker(clock=_FakeClock())

    tracker.record("guardian.converse")
    tracker.record("guardian.speak")

    first = tracker.pop_pending()
    second = tracker.pop_pending()

    assert first == [("guardian.converse", "jarvis"), ("guardian.speak", "sentinel")]
    assert second == []


def test_recent_clusters_excludes_activity_outside_the_window():
    clock = _FakeClock(start=0.0)
    tracker = ActivityTracker(clock=clock)

    tracker.record("guardian.speak")
    clock.now = 31.0  # past the 30s default window

    assert tracker.recent_clusters() == []


def test_recent_clusters_includes_activity_at_exactly_the_window_boundary():
    clock = _FakeClock(start=0.0)
    tracker = ActivityTracker(clock=clock)

    tracker.record("guardian.speak")
    clock.now = 30.0

    assert tracker.recent_clusters(window_seconds=30.0) == ["sentinel"]


def test_recent_clusters_deduplicates_and_sorts_multiple_active_clusters():
    clock = _FakeClock(start=0.0)
    tracker = ActivityTracker(clock=clock)

    tracker.record("guardian.speak")  # sentinel
    tracker.record("guardian.converse")  # jarvis
    tracker.record("guardian.transcribe")  # sentinel again - no duplicate entry

    assert tracker.recent_clusters() == ["jarvis", "sentinel"]


def test_method_clusters_covers_every_dispatched_rpc_method(tmp_path):
    """Codex design-review requirement (EIP-ESR0051-002): a future new RPC
    method must not silently go unmapped. Builds a real StdioRpcServer
    (offline-safe env, matching test_stdio_rpc.py's own _server pattern) and
    asserts METHOD_CLUSTERS' key set is exactly the server's real dispatch
    table, not a hand-maintained count that can drift."""

    from jarvis.guardian.runtime import GuardianRuntime  # noqa: PLC0415 - avoids a module-level import cycle
    from jarvis.interfaces.stdio_rpc import build_default_runtime

    runtime: GuardianRuntime = build_default_runtime(
        environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        }
    )
    server = StdioRpcServer(runtime)

    assert set(METHOD_CLUSTERS.keys()) == set(server._methods.keys())  # noqa: SLF001 - the exact coverage this test exists to enforce
