# EIP-ESR0051-002 - Guardian Orb Phase 2: Cluster Illumination

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0051-002 |
| Title | Engineering Implementation Package: Guardian Orb Phase 2 Cluster Illumination |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0051 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0051 WP2: EBG-0121, resolving [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1's Phase 2 ("architectural clusters illuminate as the systems they represent are accessed") - the gap `src/GuardianOrbGraph.jsx`'s own code comment already names ("access-triggered cluster illumination, which needs real backend activity signal this component does not have").

---

# 3. Repository Context Investigated

* `jarvis/interfaces/knowledge_graph.py`: Phase 1 already computes a coarse `cluster` field per node (`_cluster_for`, top-level repository directory), explicitly deferring "the real cluster-illumination semantics" to Phase 2.
* `jarvis/interfaces/stdio_rpc.py`: `_methods` dict maps **16** RPC method names to handlers (corrected from this draft's original miscount of 15 - Codex design-review finding); `handle_line` dispatches one request per line, returning a response dict; `serve_forever`'s loop already runs a background `_heartbeat_loop` thread emitting a `system.heartbeat` JSON-RPC notification (no `id` key) via `_write_line` under a shared write lock (EIP-ESR0031-002) - the existing push-notification precedent this package extends, not replaces.
* `src/App.jsx`: already listens for `jarvis://notification` events (`listen("jarvis://notification", ...)`), currently only handling `system.heartbeat`; `knowledge_graph`/`platform_status` are one-time mount fetches via `invoke(...)`.
* `src/GuardianOrbGraph.jsx`: Canvas 2D rendering, `colorForCluster`/`computeClusterOrder` shared with `KnowledgeGraphPanels.jsx` so both use identical cluster order/colour; per-node `depthAlpha`/glow-sprite draw already exists (Section 4.3-equivalent).
* `src/KnowledgeGraphPanels.jsx`: `ActiveClustersPanel` renders one `.cluster-row` per cluster (swatch, name, static live node count) - real but static, no access-driven state yet.
* `src/styles.css`: `.cluster-row`/`.cluster-swatch`/`.cluster-name`/`.cluster-count` exist; `@keyframes mic-recording-pulse` is an existing pulse-animation precedent to mirror stylistically.
* `jarvis/tests/test_stdio_rpc.py`: `test_heartbeat_loop_emits_notification_with_no_id_key` and `test_serve_forever_still_processes_requests_correctly_with_heartbeat_thread_running` are the direct test precedents for the new notification's own tests.

---

# 4. Scope

## 4A. Backend - `jarvis/interfaces/activity_tracker.py` (new)

New `ActivityTracker` class: a static `METHOD_CLUSTERS: dict[str, str]` maps each of the **16** real RPC method names (all of `_methods`'s current keys, including `gia.status` - Codex design-review finding: this draft's v0.1 undercounted the method total and must not silently omit any handler from the mapping) to the repository cluster that actually implements it (mirroring `_cluster_for`'s directory-based clustering by the real underlying module - e.g. `guardian.speak`/`guardian.transcribe` map to `"sentinel"`, since that is where `PiperProvider`/`WhisperProvider` actually live, not `"jarvis"` merely because the RPC handler is defined in `stdio_rpc.py`, reached via the Sentinel-gated voice adapters - honest as "this RPC capability was genuinely accessed," not a claim that the downstream provider call itself succeeded; the remaining 14 methods map to `"jarvis"`, the real location of every other handler's underlying implementation).

* `record(method: str) -> str | None`: looks up the cluster for a dispatched method, records it as currently-active with the current monotonic time, queues it for the next pending-notification pop, and returns the cluster (or `None` for an unmapped method). Guards its own mutable state with a lock, held only while updating that state - never while writing to `out_stream` (Codex design-review requirement: `ActivityTracker`'s lock and `StdioRpcServer`'s existing `_write_lock` are separate locks serving different data, and must never be held simultaneously across a blocking write).
* `pop_pending() -> list[tuple[str, str]]`: drains and returns queued `(method, cluster)` pairs since last call - the push-channel interface `serve_forever` consumes.
* `recent_clusters(window_seconds: float = 30.0) -> list[str]`: sorted list of clusters with activity within the window - the pull interface `knowledge.graph` consumes for its initial/one-time-fetch state.

Injectable clock (`time.monotonic` default) for deterministic tests, mirroring `gia_observer`'s injectability pattern. A dedicated test asserts `METHOD_CLUSTERS`'s key set exactly equals `StdioRpcServer(...)._methods`'s key set, so a future new RPC method cannot silently go unmapped (Codex design-review requirement).

## 4B. Backend - `jarvis/interfaces/stdio_rpc.py`

* `StdioRpcServer.__init__` gains an injectable `activity_tracker: ActivityTracker | None = None` parameter (defaulting to a real `ActivityTracker()`), mirroring `gia_observer`/`identity_service`'s existing injectability pattern.
* `handle_line`: after `result = handler(params)` succeeds (before returning the response), calls `self._activity_tracker.record(method)`. Only successful dispatches are recorded - an errored or malformed request did not genuinely exercise that cluster's real capability.
* `_knowledge_graph`: response gains `"active_clusters": self._activity_tracker.recent_clusters()` - real data only, computed from genuinely recorded activity, never a placeholder list.
* `serve_forever`'s main loop: after writing each response, calls `self._activity_tracker.pop_pending()` and, for each `(method, cluster)` pair, writes a new `knowledge.cluster_activity` notification (no `id` key, same `_write_line`/write-lock pattern as `system.heartbeat`) with `params: {"cluster": cluster, "method": method, "timestamp": <UTC ISO>}`.

## 4C. Frontend - `src/App.jsx`

* The existing `jarvis://notification` listener gains a second branch: `event.payload?.method === "knowledge.cluster_activity"` updates a new `activeClusters` state (a `Map<cluster, lastActiveAtMs>`), setting/refreshing the entry for `event.payload.params.cluster` to `Date.now()`.
* A lightweight prune (via the existing shared `animationScheduler` subscription pattern already used by `GuardianOrbGraph`, or a simple `setInterval`) removes entries older than a fixed `CLUSTER_ACTIVE_WINDOW_MS` (10 seconds) so illumination fades rather than sticking on forever.
* `knowledgeGraph.active_clusters` (the pull field from the initial mount fetch) seeds `activeClusters` on load, so a cluster active in the moments just before the UXP opened is not shown as falsely idle.
* `activeClusters` (as a plain array of currently-active cluster names) is passed down as a new prop to both `GuardianOrbGraph` and `ActiveClustersPanel`.

## 4D. Frontend - `src/GuardianOrbGraph.jsx`

* Gains an `activeClusters` prop (array, default `[]`).
* In the per-node draw pass (Section 4.3-equivalent), a node whose `cluster` is in `activeClusters` receives a modest additional glow-alpha boost (a fixed increment, not a second sprite pass, to avoid adding meaningful per-frame cost to the already carefully-tuned draw loop) - real, observable illumination, not a new decorative animation loop.

## 4E. Frontend - `src/KnowledgeGraphPanels.jsx`

* `ActiveClustersPanel` gains an `activeClusters` prop (array, default `[]`); a `.cluster-row` whose cluster is in the array gains an `is-active` class.

## 4F. `src/styles.css`

* New `.cluster-row.is-active` rule: a subtle pulsing box-shadow/border-colour animation (new `@keyframes cluster-active-pulse`, mirroring `@keyframes mic-recording-pulse`'s existing style), using the cluster's own swatch colour where feasible, otherwise the existing accent colour.

---

# 5. Explicitly Excluded

* Phase 3 (agent-traversal animation, blocked on deeper GIA telemetry per `GuardianOrbGraph.jsx`'s own disclosed scope) and Phase 4 (Guardian reasoning connection) - both remain separate, later, out-of-scope phases.
* Any change to which RPC methods exist, their params/return shape (beyond `knowledge.graph`'s additive `active_clusters` field), or any Sentinel/security-relevant code path.
* Any change to `_cluster_for`'s Phase 1 clustering logic itself - `METHOD_CLUSTERS` is a new, separate mapping (RPC method to cluster), not a modification of the existing file-to-cluster mapping.
* Any per-request activity history/audit log - only "is this cluster active right now" is tracked, nothing persisted, nothing exposed beyond the current active-cluster set.

---

# 6. Validation

* `python -m pytest jarvis/tests sentinel scripts/tests` - new tests, per Codex design review: `ActivityTracker` `record`/`pop_pending`/`recent_clusters` windowing; `METHOD_CLUSTERS`'s key set exactly equals `_methods`'s key set (mapping-coverage test); `stdio_rpc.py`'s new `knowledge.cluster_activity` notification (mirroring `test_heartbeat_loop_emits_notification_with_no_id_key`'s pattern: no `id` key, correct method/params shape); a concurrent-write/interleaving test alongside the existing heartbeat thread; `_knowledge_graph`'s new `active_clusters` pull field.
* `npm run build` clean.
* `npx playwright test tests/e2e/app.spec.js` - existing tests unchanged; new test(s) covering the `knowledge.cluster_activity` notification driving `is-active` on the correct `ActiveClustersPanel` row.
* `python scripts/validate_repository.py` (full mode) - 0 errors.
* Live smoke check: performed against the real `python -m jarvis --ipc-stdio` backend process (not mocked) - a real `platform.status` call produced a genuine `knowledge.cluster_activity` notification (`cluster: "jarvis"`), and the subsequent `knowledge.graph` call's response correctly reported `active_clusters: ["jarvis"]`.
* **Disclosed test-coverage limitation**: the new Playwright e2e tests exercise the pull-interface seed path (`knowledge_graph`'s `active_clusters` field driving `ActiveClustersPanel`'s `is-active` class on mount) - this suite has no existing mock for `@tauri-apps/api/event`'s `listen()` at all (`system.heartbeat` is likewise untested at this layer), so the live push-notification path (`knowledge.cluster_activity` arriving mid-session) is covered by the backend `stdio_rpc.py` tests and the standalone live smoke check above, not by a browser-level e2e test. Disclosed rather than silently assumed covered.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0051`/`WP2`). **Verdict: Approve with one required correction**, timestamp 2026-08-22T13:11:11Z. Codex independently re-verified every Section 3 context claim against the real files, confirmed the METHOD_CLUSTERS mapping approach is honest and defensible (sentinel for voice, jarvis for the rest, understood as "capability genuinely accessed" not "downstream execution succeeded"), confirmed extending the heartbeat notification pattern is architecturally sound (the existing `_write_line` lock already prevents interleaving), and confirmed no Phase 3/4 dependency and no Sentinel/security code touched. The required correction - this draft's v0.1 undercounted `_methods` as 15 methods instead of the real 16, risking `gia.status` being silently left unmapped - is folded into Section 4A above, along with Codex's locking guidance (`ActivityTracker`'s own lock must never be held across a blocking write) and the required mapping-coverage/interleaving tests (Section 6).

---

# 8. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0121, this package's target item.
* [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1 - the design direction this package implements Phase 2 of.
* [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] - this session's report, WP2.
* EIP-ESR0031-002 (Streaming Notifications MVP) - the existing push-notification precedent this package extends.
