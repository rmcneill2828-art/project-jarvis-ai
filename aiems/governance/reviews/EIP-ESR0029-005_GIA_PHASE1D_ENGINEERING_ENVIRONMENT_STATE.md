# EIP-ESR0029-005 - Guardian Instrumentation Agent (GIA) Phase 1d: Local Engineering-Environment State

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0029-005 |
| Artefact ID | EIP-ESR0029-005 |
| Title | Guardian Instrumentation Agent (GIA) Phase 1d: Local Engineering-Environment State |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0083) |
| Intended Session | ESR-0029 |
| Effective Date | 19 July 2026 |

---

# 2. Purpose

Deliver EBG-0083's last remaining Phase 1 item: local engineering-environment state. Scoped to the narrowest honest form of this - **presence detection for a small, fixed, disclosed list of named engineering tools** (is a matching process currently running, yes/no), extending WP3/WP4/WP6's `GiaSnapshot`/`LocalResourceObserver`/`gia.status` pattern rather than introducing new architecture. This closes EBG-0083's Phase 1 entirely; Phases 2-4 remain separate, later work.

---

# 3. Related Backlog Item

`EBG-0083` (`EBR-0001`), Complete (Phase 1a/1b/1c). This package delivers Phase 1's last item: Local engineering environment state, from ESR-0011 Section 10's "Initial GIA implementation should prioritise: CPU state, Memory state, Storage state, Process and service health, **Local engineering environment state**, Event/state publication."

---

# 4. Repository Context and Investigation Findings

## 4.1 A genuinely different kind of check than WP3/WP4/WP6

CPU/Memory/Disk/Process (WP3/WP4/WP6) are all self/host introspection - reading a number about this machine or this process. Local engineering-environment state is different: detecting whether *other, named, external* applications are currently running. This package scopes it as narrowly and unambiguously as CPU/Memory/Disk/Process were: a small, fixed, disclosed set of tool names, boolean presence only - no arbitrary process enumeration exposed, no judgement about what "degradation" means (explicitly out of scope, per Section 8).

## 4.2 Which tools, and their real process names - verified directly, not assumed

ESR-0011's own working discussion (`FCH-0011`) named: GitHub Desktop, VS Code, Obsidian, ChatGPT Desktop. Confirmed directly against the Programme Sponsor's real running machine (`tasklist`) rather than assuming executable names: VS Code's real process name is `Code.exe` (many instances - Electron apps run multiple processes) and ChatGPT Desktop's real process name is **`ChatGPT Classic.exe`, not `ChatGPT.exe`** as would otherwise have been assumed - confirming the value of checking rather than guessing. Obsidian and GitHub Desktop were not running at investigation time (a legitimate, honestly-observable state, not a detection failure) - their expected process names (`Obsidian.exe`, `GitHubDesktop.exe`) are the standard published names for those applications; live verification (Section 9) will confirm detection actually works when at least one of them is open, not merely that "not found" is returned correctly for tools that happen to be closed.

## 4.3 Detection mechanism

`psutil.process_iter(["name"])` enumerates all running processes' names in one pass - a single, bounded, cheap operation (typically well under the existing 0.2s CPU-sampling cost already accepted for this RPC method), not a per-tool separate scan. Each configured tool is matched against one or more candidate process names (handling cases like ChatGPT's, where the real name differs from the obvious guess).

## 4.4 Honest failure behaviour, matching WP3/WP4/WP6's precedent

A failed process-enumeration read must raise a real exception through the existing JSON-RPC error path, exactly as CPU/memory/disk/process failures already do.

## 4.5 No test infrastructure change needed

The existing injectable `ResourceReader` protocol and fake-reader pattern extends directly. RPC tests continue to assert exact camelCase serialization from a deterministic fake `GiaSnapshot` (WP3's must-not-regress requirement, already carried forward twice without issue).

---

# 5. Scope

This package authorises a future implementation to:

1. Define a small, disclosed constant mapping tool label to candidate real process name(s) (e.g. `{"vscode": ("Code.exe",), "obsidian": ("Obsidian.exe",), "githubDesktop": ("GitHubDesktop.exe",), "chatgpt": ("ChatGPT.exe", "ChatGPT Classic.exe")}`), confirmed against real evidence per Section 4.2.
2. Extend `ResourceReader` (and `PsutilResourceReader`) with a `running_process_names() -> frozenset[str]` method, backed by `psutil.process_iter(["name"])`.
3. Extend `GiaSnapshot` with `engineering_tools_running: dict[str, bool]` (one entry per configured tool).
4. Extend `LocalResourceObserver.snapshot()` to call `running_process_names()` once and compute presence for each configured tool against it, propagating real failures exactly as the existing fields do.
5. Extend `gia.status`'s response with `engineeringToolsRunning` (an object keyed by camelCase tool name, e.g. `githubDesktop`).
6. Extend the existing fake reader(s) with tool-presence figures; extend RPC tests asserting the new field serializes correctly from a deterministic fake snapshot.
7. Record delivery against `EBG-0083` in `EBR-0001`, closing Phase 1 entirely.

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

1. `GiaSnapshot` remains a frozen dataclass - add one field, do not restructure existing ones.
2. The tool-name mapping must be a module-level constant, disclosed in code comments with its evidence source (Section 4.2), not scattered magic strings.
3. Detection must be presence-only (boolean) - no process metadata (PID, memory, command line, window title) is exposed for these external tools, since that would exceed "is it running" into a different, unscoped capability.
4. RPC tests must assert exact serialization from an injected fake snapshot (WP3's Engineering Reviewer finding must not regress).
5. No change to `gia.status`'s existing fields or their behaviour.
6. Live verification (Section 9) must include at least one tool observed in both states (running and not running) where practically achievable, not only the "not running" state already confirmed during investigation.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any judgement, threshold, or "degradation" classification (e.g. "Obsidian should be open and isn't") - GIA observes and publishes only, per its own defining constraint (ESR-0011 Section 10). A future consumer (Guardian, a UI) may apply judgement; this package does not.
2. Arbitrary process enumeration or lookup by name at request time (e.g. a generic "is process X running" RPC parameter) - only the small, fixed, disclosed tool list from Section 5 item 1.
3. Any process metadata beyond presence (PID, memory, CPU, window title, command line) for the external tools - self-process detail remains WP6's scope (`jarvis` itself), not extended here to other applications.
4. GIA Phases 2-4.
5. Any frontend/UXP change.
6. Any change to `jarvis/gia/bootstrap.py` or `run()`'s startup sequence.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification (a real `gia.status` call returning plausible tool-presence figures from the actual running machine, via the same in-memory-stream technique WP3/WP4/WP6 used) must occur before the package is reported complete, per Implementation Requirement 6.

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

No new dependency. Risks:

1. **Process names can vary by OS/install/version** (confirmed directly at Section 4.2 - ChatGPT's real name differed from the obvious guess) - mitigated by supporting multiple candidate names per tool and by live-verifying against the real machine rather than assuming names are correct.
2. **A tool not currently running is indistinguishable from a tool not installed** - this package reports presence only, honestly, and does not attempt to distinguish "not running" from "not installed" (a materially different, unscoped capability).

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0083, Phase 1d (closing Phase 1 entirely) delivered by this package. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | WP3's foundation, extended by this package. |
| [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]] | WP6's precedent for this exact kind of small, additive extension. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: e0ae3e3c14c6df136dcc8b83141f2faf71538f92`, 19 July 2026 13:54:17Z). All Scope items delivered exactly as designed: `ENGINEERING_TOOLS` constant (vscode/obsidian/githubDesktop/chatgpt, with both `ChatGPT.exe` and `ChatGPT Classic.exe` as candidates); `ResourceReader`/`PsutilResourceReader` gained `running_process_names()` via a single `psutil.process_iter(["name"])` pass; `GiaSnapshot` gained `engineering_tools_running`; `LocalResourceObserver.snapshot()` matches the constant against the running-names set; `gia.status` response gained `engineeringToolsRunning`. WP3's must-not-regress requirement held: RPC tests continue to assert exact camelCase serialization from a deterministic fake `GiaSnapshot`. 1 new test (confirming ChatGPT Desktop matches under either candidate name) plus existing tests extended, 295 tests total (was 294), all passing. Live-verified via the same real production code path as WP3/WP4/WP6 (in-memory streams, no OS pipe) - genuine figures returned matching the independently-confirmed `tasklist` evidence exactly (`vscode`/`chatgpt` true, `obsidian`/`githubDesktop` false), satisfying Implementation Requirement 6's both-states verification. No new dependency, no frontend change, `jarvis/gia/bootstrap.py` untouched, no process metadata beyond presence exposed, `run()` startup sequence untouched. Closes EBG-0083 Phase 1 in full. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP7, extending WP3/WP4/WP6's GIA observability with local engineering-environment state (presence-only detection of a small, fixed, disclosed tool list). Confirmed real process names directly against the Programme Sponsor's running machine rather than assuming them - found ChatGPT Desktop's real process name (`ChatGPT Classic.exe`) differs from the obvious guess. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
