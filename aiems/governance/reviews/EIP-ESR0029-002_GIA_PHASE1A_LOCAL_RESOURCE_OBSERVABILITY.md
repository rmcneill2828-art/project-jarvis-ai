# EIP-ESR0029-002 - Guardian Instrumentation Agent (GIA) Phase 1a: Local Resource Observability

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0029-002 |
| Artefact ID | EIP-ESR0029-002 |
| Title | Guardian Instrumentation Agent (GIA) Phase 1a: Local Resource Observability |
| Version | 1.1 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0083) |
| Intended Session | ESR-0029 |
| Effective Date | 19 July 2026 |

---

# 2. Purpose

Deliver the first real slice of the Guardian Instrumentation Agent (GIA): a new, minimal, honest local-resource observability capability - real CPU and memory state, read from the actual host machine and published via a new read-only JSON-RPC method - following the Programme Sponsor's direction to pursue GIA next after ESR-0029 WP1/WP2's resource-interaction research and Guardian Orb performance work.

This is deliberately the smallest defensible slice of EBG-0083's scope, not the whole of GIA. Storage state, process/service health, local engineering-environment state (EBG-0083's remaining Phase 1 items) and Phases 2-4 (platform/engineering/external instrumentation) are explicitly out of scope, left for future EIPs once this foundation is proven.

---

# 3. Related Backlog Item

`EBG-0083` (`EBR-0001`), Approved Backlog. Grounded in ESR-0010's original GIA naming and ESR-0011's authoritative closure-report definition (Section 10): "GIA should be treated as the platform observability layer... Initial GIA implementation should prioritise: CPU state, Memory state, Storage state, Process and service health, Local engineering environment state, Event/state publication... GIA shall observe and publish state. It shall not become a policy engine, decision-maker or owner of platform state."

---

# 4. Repository Context and Investigation Findings

## 4.1 GIA has never been implemented as observability - only a differently-scoped Proof of Concept exists

`jarvis/gia/bootstrap.py` (`GiaBootstrap`, `EngineeringRequest`, `EngineeringReadinessContext`, `ReadinessState`) was built at ESR-0012 WP3 as "GIA-BOOT," a Proof of Concept exploring whether an *engineering request* (a Work Package) has minimum readiness (a non-empty identifier, objective and scope) before proceeding. Confirmed directly by reading the module: it contains no CPU, memory or any platform-state observation at all - it is a request-validation gate, unrelated to the observability capability ESR-0011 actually defined. ESR-0012's own closure report is explicit that "GIA-BOOT is accepted as a Proof of Concept only. Further GIA implementation remains deferred until separately approved." This package does not touch, extend or reuse that module - the real observability capability is new code in a new file.

## 4.2 No existing dependency reads real system resource state

Confirmed directly: `psutil` (or any comparable system-metrics library) is not installed (`ModuleNotFoundError` on import) and not listed in any requirements file. Python's standard library has no cross-platform CPU-percentage/memory-usage API (`os.getloadavg()` is Unix-only and measures load average, not CPU percentage, and has no memory equivalent at all). `psutil` is the standard, actively-maintained, MIT-licensed, cross-platform (Windows/macOS/Linux) library for exactly this need - free, no new recurring cost, consistent with this project's no-discretionary-spend posture (that posture concerns money, not open-source dependencies; `d3-force`, `Path2D` and every existing Python/JS library already in this repository are the same kind of free dependency). Adding it is a genuine new dependency, disclosed here for Engineering Reviewer/Programme Sponsor visibility rather than added silently.

## 4.3 Where this plugs into the existing architecture

`jarvis/interfaces/stdio_rpc.py`'s `StdioRpcServer` dispatches JSON-RPC methods through a simple `self._methods` dict (`guardian.converse`, `platform.status`, `knowledge.graph`, `memory.propose/approve/deny/list`). A new `gia.status` method follows the exact same pattern. Unlike `platform.status` (which reports `GuardianRuntime`'s own lifecycle/service state) or `memory.*` (which requires a connected `PersonalMemoryService`), `gia.status`'s own handler code is deliberately **not** routed through `GuardianRuntime` at all: it calls a new, standalone `jarvis/gia/observability.py` module directly, with no dependency on `GuardianRuntime`, `SentinelTrustGateway` or any conversation/memory boundary - reading real host state does not require trust-gating any more than reading the graph topology in `knowledge.graph` does.

**This is method-level independence only, not process-level resilience, and this package does not claim otherwise.** Engineering Reviewer finding (v0.1 review): `run()`'s current bootstrap sequence (`jarvis/interfaces/stdio_rpc.py` lines ~319-326) always calls `build_default_runtime()` - which constructs *and starts* `GuardianRuntime` - before `StdioRpcServer` is even created, so no JSON-RPC method, `gia.status` included, is reachable at all if that construction/start step fails. ESR-0011's resilience framing ("if Guardian fails, GIA continues observing") is a real, worthwhile future property, but achieving it would mean redesigning `run()`'s startup sequence itself (serving `gia.status` even when `GuardianRuntime` construction fails) - a separate, larger piece of engineering than this package's deliberately minimal scope, not authorised or attempted here. What this package actually delivers: `gia.status`'s handler is architecturally decoupled at the code level (no runtime/gateway/service-boundary dependency in its own call graph) so that a future, separately-scoped startup-resilience package has a clean method to build on - not a present guarantee that GIA survives a Guardian startup failure today.

## 4.4 Honest failure behaviour

Per the established no-mock-fallback rule (ESR-0017 WP9) and `platform.status`'s own honest connecting/unavailable states: if `psutil` cannot read a value (an unsupported platform, a transient OS error), the method must raise a real error surfaced to the caller, not fabricate a plausible-looking number. The frontend already has a working pattern for this (`knowledgeGraphError`/`platformError` state in `App.jsx`) that a future UI consumer would reuse - not itself part of this backend-only package.

## 4.5 CPU percentage requires a real sampling interval, not a single instantaneous read

`psutil.cpu_percent()` measures usage *between two calls* - called with no prior baseline in the same process, it returns a meaningless `0.0` on first invocation. A short blocking sample (`psutil.cpu_percent(interval=0.2)`) gives a real, honest, immediate reading at the cost of a brief (≤0.2s) synchronous delay on that one RPC call - an accepted, disclosed tradeoff for a status-check method, not a hot path.

## 4.6 No test infrastructure precedent for a new backend module

Following the established pattern for every other backend capability added this project (`sentinel/ollama_provider.py`, `jarvis/memory/`), this package adds real `pytest` unit tests for the new module and its RPC wiring, using an injectable interface (not monkeypatching `psutil` globals) so tests do not depend on the actual host machine's live CPU/memory values.

---

# 5. Scope

This package authorises a future implementation to:

1. Add `psutil` as a new Python dependency (`requirements.txt` or equivalent), disclosed per Section 4.2.
2. Create `jarvis/gia/observability.py`: a `GiaSnapshot` dataclass (`cpu_percent: float`, `memory_percent: float`, `memory_used_mb: float`, `memory_total_mb: float`, `captured_at: datetime`) and a `LocalResourceObserver` class with a `snapshot()` method reading real values via `psutil`, injectable (constructor-accepts a reader dependency) so tests can substitute a fake without touching the real OS.
3. Add a new `"gia.status": self._gia_status` entry to `StdioRpcServer._methods` in `jarvis/interfaces/stdio_rpc.py`, calling `LocalResourceObserver.snapshot()` directly (not via `GuardianRuntime`), returning `{"cpuPercent": ..., "memoryPercent": ..., "memoryUsedMb": ..., "memoryTotalMb": ..., "capturedAt": ...}`.
4. Propagate a real error (not a fabricated/zeroed snapshot) if the underlying read fails, matching the no-mock-fallback rule.
5. Add unit tests for `LocalResourceObserver` (using an injected fake reader, not the real host) and for `gia.status`'s RPC wiring (confirming the method is registered and returns the expected shape from a fake snapshot).
6. Record delivery against `EBG-0083` in `EBR-0001`, disclosing explicitly that Storage state, Process/service health, Local engineering-environment state and Phases 2-4 remain not delivered.

---

# 6. Authorised Files

1. `jarvis/gia/observability.py` (new)
2. `jarvis/interfaces/stdio_rpc.py`
3. `pyproject.toml` (confirmed at implementation time as where Python dependencies are declared - no `requirements.txt` exists in this repository)
4. `jarvis/tests/test_gia_observability.py` (new)
5. `jarvis/tests/test_stdio_rpc.py` (adding `gia.status` coverage to existing RPC tests)
6. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
7. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
8. `jarvis/gia/__init__.py` and `jarvis/__init__.py` - discovered at implementation time, not in the original list; both already re-export `jarvis/gia/bootstrap.py`'s public classes at their respective package levels, so re-exporting `GiaSnapshot`/`LocalResourceObserver` the same way is a small, consistent extension of that existing convention rather than new authority - disclosed here and in Section 14's delivery entry rather than silently included.

No frontend (`src/`) files are authorised - this is a backend-only capability delivery, per PBK-0001's Feature-First Delivery Discipline allowance (the same precedent as `EBG-0080` Personal Memory: backend capability landed before any UI consumes it). `jarvis/gia/bootstrap.py` and its tests are explicitly **not** authorised for changes - the new observability module is separate, standalone code, not an extension of GIA-BOOT.

---

# 7. Implementation Requirements

1. `LocalResourceObserver` must accept an injectable reader (e.g. a constructor parameter defaulting to a real `psutil`-backed implementation) so unit tests never depend on the actual host machine's live resource state.
2. `gia.status`'s own handler code must not construct or depend on `GuardianRuntime`, `SentinelTrustGateway`, or any memory/conversation boundary - it is independent instrumentation at the code level, per Section 4.3. This is method-level decoupling only; it does not change `run()`'s existing startup sequence, and does not make `gia.status` reachable if `build_default_runtime()` itself fails - that is a separate, unauthorised, future scope.
3. A failed read must raise a real exception surfaced through the existing JSON-RPC error path (matching how other methods in `StdioRpcServer` already propagate `TypeError`/domain errors) - never a zeroed or fabricated snapshot.
4. `psutil.cpu_percent` must be called with a real, disclosed sampling interval (Section 4.5), not a bare `cpu_percent()` call that returns a meaningless first-call value.
5. No changes to `jarvis/gia/bootstrap.py`, `GuardianRuntime`, `SentinelTrustGateway`, or any existing RPC method's behaviour.
6. New dependency addition must be the only dependency change - no incidental version bumps to unrelated packages.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Storage state, process/service health, or local engineering-environment state (EBG-0083's remaining Phase 1 items) - future EIPs.
2. GIA Phases 2-4 (platform instrumentation, engineering instrumentation, external/provider telemetry under Sentinel) - future, separately-scoped work.
3. Any frontend/UXP change to display GIA data - this is backend-only capability delivery.
4. Any change to `jarvis/gia/bootstrap.py` (GIA-BOOT) - separate, untouched Proof of Concept.
5. Any policy, decision-making, or platform-state-ownership behaviour - GIA observes and publishes only, per its own defining constraint (ESR-0011 Section 10).
6. Continuous/background polling or a push-based event stream - `gia.status` is a pull-based, on-demand RPC method matching every other method in `StdioRpcServer` today; a future event-publication mechanism (if genuinely needed) is separate design work.
7. Any redesign of `run()`'s startup sequence to make `gia.status` reachable when `build_default_runtime()`/`GuardianRuntime` construction fails - Section 4.3 discloses this as a real current limitation (method-level independence only, not process-level resilience), not something this package fixes.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification must occur before the package is reported complete: a real call to `gia.status` against the actual running backend (not only unit tests against a fake reader), confirming genuine, plausible CPU/memory figures are returned from the real host.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. New unit tests pass, exercising both a healthy snapshot and a simulated read failure (via the injected fake reader), without depending on real host state.
2. Full existing suite remains passing (no regression).
3. Live verification (Section 9 item 2): a real `gia.status` call against the actual running Python backend returns plausible figures from the real machine.
4. `validate_repository.py` (full mode) passes with 0 errors for the governance-artefact files.

---

# 11. Risks and Dependencies

## Dependencies

New dependency: `psutil`. No other dependency.

## Risks

1. **New third-party dependency, first one added to the Python side in some time.** Mitigated by `psutil`'s maturity (widely used, actively maintained, MIT-licensed) and by confining its use to one new, isolated module (`jarvis/gia/observability.py`) behind an injectable interface, not scattered across the codebase.
2. **Cross-platform behaviour is not identical everywhere `psutil` runs** (e.g. some metrics differ slightly on Windows vs. Linux) - this project's actual deployment target today is the Programme Sponsor's own Windows machine, so live verification against that real environment (Section 9 item 2) is the relevant proof, not exhaustive cross-platform testing.
3. **`cpu_percent`'s blocking sample interval (Section 4.5) adds real latency to that one RPC call** (~0.2s) - disclosed and accepted for a status-check method; a future high-frequency polling use case would need a different, non-blocking design, out of scope here.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083 (this package's parent backlog item), Phase 1a delivered by this package. |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] | Section 10's GIA Outcome is this package's authoritative scope source. |
| `jarvis/gia/bootstrap.py` | The unrelated, pre-existing "GIA-BOOT" Proof of Concept - explicitly not touched by this package. |
| `jarvis/interfaces/stdio_rpc.py` | New `gia.status` method added here, following the existing dispatch pattern. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Addressed a Medium finding from the Engineering Reviewer (Codex) on the v1.0 implementation: the two `gia.status` RPC tests called the real psutil-backed observer via `_server()` instead of a deterministic fake, so the RPC serialization/shape path (Section 5 item 5, Section 4.6) was never actually proven against a known snapshot. Fixed by adding a `gia_observer` constructor parameter to `StdioRpcServer` (defaulting to the real `LocalResourceObserver()`, backwards-compatible), and rewriting the RPC tests: one now injects a fake observer returning a fixed `GiaSnapshot` and asserts the *exact* camelCase-serialized response; a second confirms `gia.status` resolves against a bare, unstarted `GuardianRuntime()` using the same fake-injection pattern; a third, clearly-labelled supplementary test confirms the *default* (no injection) wiring still genuinely uses the real host, distinct from and not a substitute for the EIP's own separate live-verification requirement. 293 tests total (was 292). |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: c5a8340cc9ed24bf60241b0c93b278b842651af4`, 19 July 2026 09:54:31Z). All Scope items delivered: `psutil` added as a new dependency (`pyproject.toml`); `jarvis/gia/observability.py` created (`GiaSnapshot`, `ResourceReader` protocol, `PsutilResourceReader`, `LocalResourceObserver`); `gia.status` added to `StdioRpcServer._methods`, calling the observer directly with no `GuardianRuntime`/`SentinelTrustGateway`/memory dependency in its own handler code; re-exported through `jarvis/gia/__init__.py` and `jarvis/__init__.py` matching the existing GIA-BOOT export convention (a small, disclosed addition beyond the originally-listed Authorised Files, for consistency with that established pattern). 6 new tests: 4 for `LocalResourceObserver` (success, failure propagation, real sampling interval, real default `psutil` reader) using an injected fake so none depend on the actual host; 2 for the RPC wiring (real host data returned, and `gia.status` resolves against a bare unstarted `GuardianRuntime()`). 292 tests total (was 286), all passing. Live-verified via the real production code path (`build_default_runtime()` + `StdioRpcServer.serve_forever()`) using in-memory streams - genuine host figures returned (CPU 6.7%, memory 47.8%/15.6GB/32.7GB at verification time). A raw `python -m jarvis.app --ipc-stdio` invocation through a Git Bash pipe produced no output on this Windows machine; independently confirmed the same is true of the pre-existing `platform.status` method, isolating this to a general shell/stdin-piping quirk unrelated to this package, not a defect. `npm`/frontend unaffected - no `src/` files touched, per Section 6's exclusion. |
| 0.2 | 19 July 2026 | Claude Engineering Implementer | Addressed a Medium finding from the Engineering Reviewer (Codex): Section 4.3/Section 7 item 2 overstated GIA's independence from `GuardianRuntime` as a present process-level resilience guarantee, when `run()`'s existing startup sequence (`build_default_runtime()` constructing and starting `GuardianRuntime` before `StdioRpcServer` exists) means no method, `gia.status` included, is reachable if that construction fails. Narrowed the claim to what this package actually delivers - method-level code decoupling only - and added an explicit exclusion (Section 8 item 7) disclosing that fixing `run()`'s startup resilience is separate, unauthorised future work. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP3, following the Programme Sponsor's direction to pursue GIA next. Investigated the existing (unrelated) GIA-BOOT Proof of Concept, confirmed no system-resource-reading dependency currently exists, and scoped the smallest defensible first slice of EBG-0083: real CPU/memory observation via a new `psutil`-backed module and a new standalone `gia.status` RPC method, independent of `GuardianRuntime`. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
