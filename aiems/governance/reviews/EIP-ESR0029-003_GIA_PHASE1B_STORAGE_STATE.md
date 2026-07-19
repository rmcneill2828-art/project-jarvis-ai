# EIP-ESR0029-003 - Guardian Instrumentation Agent (GIA) Phase 1b: Storage State

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0029-003 |
| Artefact ID | EIP-ESR0029-003 |
| Title | Guardian Instrumentation Agent (GIA) Phase 1b: Storage State |
| Version | 1.1 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0083) |
| Intended Session | ESR-0029 |
| Effective Date | 19 July 2026 |

---

# 2. Purpose

Extend GIA's local resource observability (`EIP-ESR0029-002`, ESR-0029 WP3) with the next item from EBG-0083's own Phase 1 scope: real storage/disk state. This is a small, additive extension of the existing `GiaSnapshot`/`LocalResourceObserver`/`gia.status` machinery, not new architecture - the same pattern proven at WP3, applied to one more `psutil` reading.

Process/service health and local engineering-environment state (EBG-0083's remaining Phase 1 items) are explicitly out of scope here, left for a further package once this slice lands - each phase stays a small, separately-approved increment, per this project's established discipline.

---

# 3. Related Backlog Item

`EBG-0083` (`EBR-0001`), Complete (Phase 1a). This package delivers the next slice: Storage state, from ESR-0011 Section 10's "Initial GIA implementation should prioritise: CPU state, Memory state, **Storage state**, Process and service health, Local engineering environment state, Event/state publication."

---

# 4. Repository Context and Investigation Findings

## 4.1 Extends, does not replace, WP3's architecture

`jarvis/gia/observability.py`'s `GiaSnapshot` (frozen dataclass), `ResourceReader` protocol, `PsutilResourceReader`, and `LocalResourceObserver` are all retained; this package adds one new field group (disk) to the existing snapshot and one new protocol method (`disk_usage`), rather than introducing a second observer class or a second RPC method. `gia.status` remains the single method; its response gains three new fields.

## 4.2 Which path to measure

Confirmed directly on the Programme Sponsor's machine: `os.path.abspath(os.sep)` resolves to `I:\` (the drive the repository and JARVIS installation actually live on), and `psutil.disk_usage()` against it returns real figures (28.7% used, 430.5GB used of 1500.3GB total, at time of investigation). This is the cross-platform-safe way to identify "the local machine's storage state" without hardcoding a Windows drive letter or assuming a POSIX root exists - `os.sep` resolves to `/` on POSIX (a real, meaningful root) and to the current working directory's drive root on Windows (a real, meaningful drive, not an arbitrary guess).

## 4.3 Honest failure behaviour, matching WP3's precedent

A failed `disk_usage` read must raise a real exception through the existing JSON-RPC error path, exactly as CPU/memory failures already do - never a fabricated value.

## 4.4 No test infrastructure change needed

The existing injectable `ResourceReader` protocol and fake-reader test pattern from `jarvis/tests/test_gia_observability.py` extends directly - add a `disk_usage` method to the existing fakes, no new test infrastructure required. The same applies to `jarvis/tests/test_stdio_rpc.py`'s fake-observer pattern for RPC serialization tests (an Engineering Reviewer finding from WP3 that must not regress here: RPC tests assert exact serialization from a deterministic fake, never real host state).

---

# 5. Scope

This package authorises a future implementation to:

1. Extend `GiaSnapshot` with `disk_percent: float`, `disk_used_gb: float`, `disk_total_gb: float`.
2. Extend `ResourceReader` (and `PsutilResourceReader`) with a `disk_usage(path: str) -> DiskUsage`-shaped method, reading the path identified in Section 4.2.
3. Extend `LocalResourceObserver.snapshot()` to call it and populate the new fields, propagating real failures exactly as CPU/memory do today.
4. Extend `gia.status`'s response with `diskPercent`, `diskUsedGb`, `diskTotalGb`.
5. Extend the existing fake reader(s) in `jarvis/tests/test_gia_observability.py` with disk figures; add/extend RPC tests in `jarvis/tests/test_stdio_rpc.py` asserting the new fields serialize correctly from a deterministic fake snapshot (not real host state, per Section 4.4).
6. Record delivery against `EBG-0083` in `EBR-0001`.

---

# 6. Authorised Files

1. `jarvis/gia/observability.py`
2. `jarvis/interfaces/stdio_rpc.py`
3. `jarvis/tests/test_gia_observability.py`
4. `jarvis/tests/test_stdio_rpc.py`
5. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
6. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No frontend (`src/`) files, no change to `jarvis/gia/bootstrap.py`, no new dependency (`psutil` is already present).

---

# 7. Implementation Requirements

1. `GiaSnapshot` remains a frozen dataclass - add fields, do not restructure existing ones.
2. The measured path must be derived the same way as Section 4.2 (`os.path.abspath(os.sep)`), not hardcoded to a specific drive letter.
3. RPC tests must assert exact serialization from an injected fake snapshot (WP3's Engineering Reviewer finding must not regress) - a separate, clearly-labelled test may additionally confirm the real default wiring still works, matching WP3's own pattern.
4. No change to `gia.status`'s existing `cpuPercent`/`memoryPercent`/`memoryUsedMb`/`memoryTotalMb`/`capturedAt` fields or their behaviour.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Process/service health or local engineering-environment state (EBG-0083's remaining Phase 1 items) - future package.
2. GIA Phases 2-4.
3. Any frontend/UXP change.
4. Any change to `jarvis/gia/bootstrap.py`.
5. Any change to `run()`'s startup sequence (the disclosed method-level-only independence limitation from WP3 remains unchanged and unfixed here).

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification (a real `gia.status` call returning plausible disk figures from the actual host, via the same in-memory-stream technique WP3 used) must occur before the package is reported complete.

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

No new dependency. Risk: disk-usage semantics can differ slightly across platforms (e.g. network-mounted drives) - out of scope to handle exhaustively; live verification against the Programme Sponsor's actual machine is the relevant proof, matching WP3's own precedent.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083, Phase 1b delivered by this package. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | WP3's foundation, extended (not replaced) by this package. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Addressed a Medium finding from the Engineering Reviewer (Codex) on the v1.0 implementation review: EBR-0001's EBG-0083 row retained its original WP3-era "Scope of this item" wording ("explicitly deferring Storage state... to a later phase"), directly contradicting the new WP4 delivery note appended immediately after it in the same row. Corrected to explicitly distinguish the original WP3 scope statement from Storage state's actual WP4 delivery, leaving only Process/service health, Local engineering-environment state and Phases 2-4 described as not yet delivered. |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: ff4ea7afcd120cd4d97fc3e29a166032062f97c7`, 19 July 2026 12:10:59Z). All Scope items delivered exactly as designed: `GiaSnapshot` extended with `disk_percent`/`disk_used_gb`/`disk_total_gb`; `ResourceReader`/`PsutilResourceReader` gained `disk_usage(path)`; `LocalResourceObserver.snapshot()` reads it via `STORAGE_PATH = os.path.abspath(os.sep)`; `gia.status` response extended with `diskPercent`/`diskUsedGb`/`diskTotalGb`. WP3's must-not-regress requirement held: all RPC tests continue to assert exact camelCase serialization from a deterministic fake `GiaSnapshot`. 2 new/extended observer tests, existing fake constructions across both test files extended with disk fields, 294 tests total (was 293), all passing. Live-verified via the same real production code path as WP3 (in-memory streams, no OS pipe) - genuine figures returned (28.7% used, ~401GB/1397GB). No new dependency, no frontend change, `jarvis/gia/bootstrap.py` untouched, `run()` startup sequence untouched. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP4, extending WP3's GIA observability with Storage state. Confirmed the cross-platform path-selection approach directly against the Programme Sponsor's machine (real figures: 28.7% used, 430.5GB/1500.3GB). Not yet Engineering Reviewer or Programme Sponsor reviewed. |
