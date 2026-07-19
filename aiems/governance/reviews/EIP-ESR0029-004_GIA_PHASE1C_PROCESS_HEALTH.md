# EIP-ESR0029-004 - Guardian Instrumentation Agent (GIA) Phase 1c: Process Health

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0029-004 |
| Artefact ID | EIP-ESR0029-004 |
| Title | Guardian Instrumentation Agent (GIA) Phase 1c: Process Health |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0083) |
| Intended Session | ESR-0029 |
| Effective Date | 19 July 2026 |

---

# 2. Purpose

Extend GIA's local resource observability (WP3/WP4, `EIP-ESR0029-002`/`003`) with the next item from EBG-0083's Phase 1 scope: process health. Scoped specifically and narrowly to **the JARVIS backend's own process** (self-observation via `psutil.Process(os.getpid())`) - unambiguous, directly analogous to the existing CPU/Memory/Disk pattern, no new design question about which external services "count."

`Local engineering environment state` (EBG-0083's other remaining Phase 1 item - e.g. whether VS Code/Obsidian/GitHub Desktop are running) is explicitly **not** scoped here. It is a genuinely different kind of check (detecting other applications' processes, not self-observation) that needs its own design conversation about which tools matter and why, rather than being bundled into this small slice.

---

# 3. Related Backlog Item

`EBG-0083` (`EBR-0001`), Complete (Phase 1a/1b). This package delivers the next slice: Process health (self), from ESR-0011 Section 10's "Initial GIA implementation should prioritise: CPU state, Memory state, Storage state, **Process and service health**, Local engineering environment state, Event/state publication."

---

# 4. Repository Context and Investigation Findings

## 4.1 Extends, does not replace, WP3/WP4's architecture

Same pattern as WP4's Storage-state extension: `GiaSnapshot`, `ResourceReader`, `PsutilResourceReader`, `LocalResourceObserver`, and the single `gia.status` RPC method are all retained; this package adds one new field group (process) and one new protocol method, not new architecture.

## 4.2 What "process health" means for this slice

Confirmed directly via `psutil.Process(os.getpid())` against this session's own running Python process: `.status()` (e.g. `"running"`), `.create_time()` (used to derive uptime), `.cpu_percent(interval=...)` (this process's own CPU share, distinct from the whole-machine `cpu_percent` WP3 already reports), `.memory_info().rss` (this process's own resident memory, distinct from the whole-machine `memory_used_mb` WP3 already reports), and `.num_threads()`. All real, meaningful, immediately available - no ambiguity about scope, since "the process" means the one JARVIS backend process already running `gia.status`'s own request handler.

## 4.3 Honest failure behaviour, matching WP3/WP4's precedent

A failed process-health read must raise a real exception through the existing JSON-RPC error path, exactly as CPU/memory/disk failures already do.

## 4.4 No test infrastructure change needed

The existing injectable `ResourceReader` protocol and fake-reader pattern extends directly - add a `process_health()` method to the existing fakes. RPC tests continue to assert exact camelCase serialization from a deterministic fake `GiaSnapshot` (WP3's must-not-regress requirement, already carried forward once at WP4 without issue).

---

# 5. Scope

This package authorises a future implementation to:

1. Extend `GiaSnapshot` with `process_status: str`, `process_uptime_seconds: float`, `process_cpu_percent: float`, `process_memory_mb: float`.
2. Extend `ResourceReader` (and `PsutilResourceReader`) with a `process_health() -> ProcessHealth`-shaped method, backed by `psutil.Process(os.getpid())`.
3. Extend `LocalResourceObserver.snapshot()` to call it and populate the new fields, propagating real failures exactly as the existing fields do.
4. Extend `gia.status`'s response with `processStatus`, `processUptimeSeconds`, `processCpuPercent`, `processMemoryMb`.
5. Extend the existing fake reader(s) with process-health figures; extend RPC tests asserting the new fields serialize correctly from a deterministic fake snapshot.
6. Record delivery against `EBG-0083` in `EBR-0001`.

---

# 6. Authorised Files

1. `jarvis/gia/observability.py`
2. `jarvis/interfaces/stdio_rpc.py`
3. `jarvis/tests/test_gia_observability.py`
4. `jarvis/tests/test_stdio_rpc.py`
5. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
6. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No frontend (`src/`) files, no change to `jarvis/gia/bootstrap.py`, no new dependency (`psutil` already present).

---

# 7. Implementation Requirements

1. `GiaSnapshot` remains a frozen dataclass - add fields, do not restructure existing ones.
2. `process_health()` must observe the current process (`os.getpid()`) - never a different, externally-specified PID (that would be a materially different, unscoped capability).
3. RPC tests must assert exact serialization from an injected fake snapshot (WP3's Engineering Reviewer finding must not regress).
4. No change to `gia.status`'s existing `cpuPercent`/`memoryPercent`/`memoryUsedMb`/`memoryTotalMb`/`diskPercent`/`diskUsedGb`/`diskTotalGb`/`capturedAt` fields or their behaviour.
5. Field naming must clearly distinguish this process's own CPU/memory (`processCpuPercent`/`processMemoryMb`) from the whole-machine figures already in the response (`cpuPercent`/`memoryPercent`/`memoryUsedMb`) - no ambiguity between the two scopes in the serialized response.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Local engineering-environment state (VS Code/Obsidian/GitHub Desktop or any other external application/service detection) - EBG-0083's last remaining Phase 1 item, deferred to its own future package given it needs a separate design conversation about which tools matter.
2. Observing or reporting on any process other than the JARVIS backend's own (no arbitrary PID/process-name lookup capability).
3. GIA Phases 2-4.
4. Any frontend/UXP change.
5. Any change to `jarvis/gia/bootstrap.py` or `run()`'s startup sequence.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification (a real `gia.status` call returning plausible process-health figures from the actual running backend, via the same in-memory-stream technique WP3/WP4 used) must occur before the package is reported complete.

---

# 10. Validation

```powershell
python -m pytest
python scripts/validate_repository.py
```

1. All existing and new tests pass.
2. Live verification per Section 9 item 2.
3. `validate_repository.py` 0 errors.

---

# 11. Risks and Dependencies

No new dependency. Risk: `cpu_percent()` on a `psutil.Process` object has the same first-call-returns-zero characteristic as the whole-machine call WP3 already handled (a real sampling interval is required) - handled the same way, not a new risk class.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083, Phase 1c delivered by this package. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | WP3's foundation, extended by this package. |
| [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]] | WP4's precedent for this exact kind of small, additive extension. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: 770d292f6711cb0299f7b9986be8c33eb3947972`, 19 July 2026 13:20:28Z). All Scope items delivered exactly as designed: `GiaSnapshot` extended with `process_status`/`process_uptime_seconds`/`process_cpu_percent`/`process_memory_mb`; `ResourceReader`/`PsutilResourceReader` gained `process_health(interval)` backed by `psutil.Process(os.getpid())`; `LocalResourceObserver.snapshot()` reads it and derives uptime via `time.time() - create_time`; `gia.status` response extended with `processStatus`/`processUptimeSeconds`/`processCpuPercent`/`processMemoryMb`. WP3's must-not-regress requirement held: all RPC tests continue to assert exact camelCase serialization from a deterministic fake `GiaSnapshot`. Existing fake reader/snapshot constructions across both test files extended with process-health fields, 294 tests total (unchanged - existing tests extended, no new test functions added), all passing. Live-verified via the same real production code path as WP3/WP4 (in-memory streams, no OS pipe) - genuine figures returned (status "running", uptime 0.6s, correctly near-zero for a freshly-started process). No new dependency, no frontend change, `jarvis/gia/bootstrap.py` untouched, no external process/service lookup capability introduced, `run()` startup sequence untouched. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP6, extending WP3/WP4's GIA observability with process health, scoped narrowly to the JARVIS backend's own process (self-observation) - confirmed directly against this session's own running Python process via psutil.Process(os.getpid()). Local engineering-environment state (the other remaining Phase 1 item) explicitly excluded, deferred to its own future package. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
