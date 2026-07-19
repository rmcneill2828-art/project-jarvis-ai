# ESR-0029 WP8 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0029-WP8 |
| Title | Independent Repository Verification Handover |
| Version | 0.1 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0029 (open; no session report artefact yet - authored later per the practice established at ESR-0022 through ESR-0028) |
| Effective Date | 19 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0029's session-wide record for WP8 Independent Repository Verification. WP8 should confirm that the current repository state matches the claims made across all seven of ESR-0029's Work Packages, that disclosed scope boundaries and defects are accurately characterised, and that no unauthorised scope drift occurred. Submitted to Codex via the AIEMS Exchange Bridge for genuine independent verification, continuing the same real-cycle practice used throughout WP1-WP7.

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Local `HEAD` | `8530604` |
| `origin/main` | `8530604` (pushed, confirmed matching) |
| Working tree | Committed tree clean at `8530604`; working tree has only this untracked WP8 handover document itself |
| Prior accepted baseline | `RBL-0016` |
| ESR-0029 session start point | `1df2802` (ESR-0028's closing commit) |

---

## 4. ESR-0029 Commits in Scope

| Commit | Summary |
|---|---|
| `541e6c1` | WP1: registered EBG-0082 (Cross-Module Resource Interaction Research) - real external research (VS Code Extension Host, Electron/Tauri, Home Assistant, Mycroft) mapped against JARVIS's actual architecture, following a Medium finding fix (a stale claim about a GitHub issue's status, corrected after direct re-verification). |
| `c5a8340` | WP2: migrated `GuardianOrbGraph.jsx` from SVG to Canvas 2D, per ADR-0021. Includes a genuine performance defect found and fixed during the WP's own live verification (see Section 6). |
| `ff4ea7a` | WP3: implemented GIA Phase 1a (CPU/memory local resource observability), per EIP-ESR0029-002. |
| `bac6ba9` | WP4: extended GIA with Phase 1b (Storage state), per EIP-ESR0029-003. |
| `770d292` | WP5: approved ADR-0022 (Sponsor Approval Service architecture decision) - decision only, no code. |
| `e0ae3e3` | WP6: extended GIA with Phase 1c (Process health, self-observation only), per EIP-ESR0029-004. |
| `8530604` | WP7: extended GIA with Phase 1d (Local engineering-environment state), per EIP-ESR0029-005, closing EBG-0083 Phase 1 in full. |

---

## 5. Authorised / Explained Working Set

The full ESR-0029 diff since `1df2802` (19 files changed, 1,883 insertions, 203 deletions):

**WP1 (research, no code):**
1. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - EBG-0082 registered (research delivered, no implementation authorised).

**WP2 (Guardian Orb Canvas 2D migration):**
2. `src/GuardianOrbGraph.jsx` - migrated from SVG DOM rendering to a single Canvas 2D surface; static glow/gradient node treatment; edge depth-banding via `Path2D`; clip scoped to node-drawing pass only (edges proven mathematically safe within the boundary); manual hit-testing; `ResizeObserver`/`devicePixelRatio` responsive sizing.
3. `src/styles.css` - now-dead SVG-element selectors removed.
4. `aiems/governance/reviews/EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION.md` - new, Approved-implemented v1.2.
5. `aiems/governance/decisions/ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE.md` - implementation recorded (Approved to Approved-implemented).

**WP3/WP4/WP6/WP7 (GIA Phase 1a-1d, EBG-0083):**
6. `jarvis/gia/observability.py` - new module: `GiaSnapshot` (frozen dataclass), `ResourceReader` protocol, `PsutilResourceReader`, `LocalResourceObserver`, `ENGINEERING_TOOLS` constant.
7. `jarvis/interfaces/stdio_rpc.py` - new `gia.status` JSON-RPC method, injectable `gia_observer` constructor parameter on `StdioRpcServer`.
8. `jarvis/gia/__init__.py`, `jarvis/__init__.py` - `GiaSnapshot`/`LocalResourceObserver` re-exported, matching the existing GIA-BOOT export convention.
9. `pyproject.toml` - `psutil` added as a new dependency.
10. `jarvis/tests/test_gia_observability.py` - new test file.
11. `jarvis/tests/test_stdio_rpc.py` - extended with `gia.status` coverage.
12. `aiems/governance/reviews/EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY.md` - new, Approved-implemented v1.1.
13. `aiems/governance/reviews/EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE.md` - new, Approved-implemented v1.1.
14. `aiems/governance/reviews/EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH.md` - new, Approved-implemented v1.0.
15. `aiems/governance/reviews/EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE.md` - new, Approved-implemented v1.0.

**WP5 (Sponsor Approval Service decision, ADR-0022):**
16. `aiems/governance/decisions/ADR-0022_SPONSOR_APPROVAL_SERVICE.md` - new, Approved v1.1. Decision only - no implementation.

**Governance (session-wide, all WPs):**
17. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - registers all five new EIPs, ADR-0022, EBG-0082/0083/0084; version-aligns every touched artefact throughout.
18. `aiems/governance/registers/REG-0002_ADR_REGISTER.md` - registers ADR-0022, records ADR-0021's implementation.

No files outside this set were touched. No `sentinel/` (trust boundary/policy) code was modified anywhere in the session. `jarvis/` **was** modified this session, unlike ESR-0028 - `jarvis/gia/observability.py` (new), `jarvis/interfaces/stdio_rpc.py`, `jarvis/gia/__init__.py`, `jarvis/__init__.py` are all real backend Python code, not documentation, delivering GIA's first real observability capability. `jarvis/gia/bootstrap.py` (the pre-existing, unrelated GIA-BOOT Proof of Concept) was explicitly not touched at any point, confirmed directly in every WP3/4/6/7 review.

---

## 6. Session Observations

1. **All seven Work Packages completed the full real review cycle** via the AIEMS Exchange Bridge - draft, `submit-to-review`, Codex's `return-findings`, `sponsor-decision`, implementation, commit, a second `submit-to-review` of the committed diff, and a final `return-findings` confirmation. No manual relay anywhere.
2. **WP1 was research-only** (no code touched): real external research (not confined to this repository) into whether JARVIS's modular architecture is missing an established cross-module resource-governance pattern. One Medium finding (a stale claim that a VS Code GitHub issue was "open, unresolved" when it was actually closed as not planned) was caught, directly re-verified via `WebFetch`, and corrected before Programme Sponsor approval.
3. **WP2 (Canvas migration) is this session's largest single product-code change, and the one requiring the most significant mid-flight correction**: the approved design was implemented, but live verification (Chrome DevTools Protocol TaskDuration against the real 200-node/1,745-edge graph) found the initial implementation measured *more* expensive than the SVG baseline it was meant to improve on (~27-29% of one core vs. ~9%) - the opposite of the migration's purpose. Root-caused via a CDP ablation study to Canvas's circular clip combined with per-edge stroke calls specifically, not edge count or the clip alone. Fixed by batching edges into depth-banded `Path2D` objects and recognising edges are mathematically guaranteed within the circular boundary (a disk is convex), scoping the clip to only the node/glow-drawing pass. Final result: plain Canvas ~4.46%, Canvas with glow ~6.26%, both below the SVG baseline - confirmed independently by the Programme Sponsor's own real Windows Task Manager check (JARVIS Guardian Shell: 1.4% CPU, 1.0% GPU, Power Usage "Low", a categorical change from the SVG-era's sustained "Very high"). A further post-implementation Engineering Reviewer finding (a hit-testing order bug - the lookup array wasn't built in actual paint order, so overlapping-node tooltips could report the wrong node) was found and fixed before the post-commit review closed clean.
4. **WP3/WP4/WP6/WP7 (GIA Phase 1, EBG-0083) were delivered as four small, separately-approved slices** (CPU/memory, storage, process health, engineering-tool presence), each an additive extension of the same `GiaSnapshot`/`LocalResourceObserver`/`gia.status` architecture with no new dependency beyond WP3's initial `psutil` addition - matching this project's established small/evidence-led/staged delivery discipline. Two genuine defects were found and fixed across this sequence: WP3's first RPC tests called the real host instead of a deterministic fake snapshot, leaving the serialization path unproven (fixed via a new injectable `gia_observer` parameter, carried forward without regression through WP4/WP6/WP7); and WP3's initial design overstated GIA's independence from `GuardianRuntime` as a present resilience guarantee, when `run()`'s existing startup sequence still gates all RPC methods behind `GuardianRuntime` constructing successfully (narrowed to an accurate method-level-only claim, disclosed as a real, unfixed limitation). WP7's tool-name evidence was verified directly against the Programme Sponsor's real machine (`tasklist`), not assumed - ChatGPT Desktop's real process name (`ChatGPT Classic.exe`) differs from the obvious guess (`ChatGPT.exe`).
5. **WP5 (ADR-0022) is decision-only**, following the Programme Sponsor's own proposal to replace the AIEMS Exchange Bridge's file-based `sponsor-decision` command with a remote, agent-read-only approval service. The Engineering Implementer's review did not accept the proposal's own framing - it independently confirmed the self-approval gap directly against the real `scripts/aiems_bridge.py` code, and separately surfaced a gap the proposal's code sketch alone would not have closed: `cmd_submit_response` already correctly implements the approval and drift checks, but was never actually the practiced gate for any commit this session - every Work Package went through reading the local transcript directly and running `git commit` via Bash. This was recorded as a binding operational-practice requirement in the decision itself (Decision item 7), not left as an implied consequence.
6. **A recurring pattern of self-found stale cross-references inside `EBR-0001`'s own dense backlog entries**, caught by the Engineering Reviewer at WP4 and WP7: a WP3-era "scope of this item" sentence describing Storage state as still deferred was left uncorrected after WP4 actually delivered it, directly contradicting the delivery note appended immediately after it in the same row. Both instances were fixed the same session, and the second instance's fix explicitly re-verified there were no further stale mentions by grepping the full row - a disclosed, evidence-based correction, not a guess.
7. **A submission-timing artefact was found and clarified at WP3's fix round**: REG-0001 briefly reported stale version numbers relative to a v1.1 update still in flight when Codex's review of the v1.0 submission actually ran - a timing quirk of two overlapping submissions, not a content error in the final file state, confirmed by direct re-inspection before resubmission.
8. **This session's product-facing change (WP2's Canvas migration) is comparable in kind to ESR-0028's WP4 rotation work, but this session also adds a genuinely new backend capability** (GIA, a new Python module, a new dependency, a new RPC method) that ESR-0028 did not have an equivalent of - `jarvis/` code was modified this session where it was not at ESR-0028.

---

## 7. Validation Evidence

Re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 295 passed |
| `python scripts/validate_repository.py` (full, not governance-only) | 0 errors, 129 warnings |
| `npm run build` | Clean |
| `git diff --check 1df2802..8530604` | Clean - no whitespace issues in the full session range. |
| `git status` | Committed tree clean on `main` at `8530604`, matching `origin/main`; working tree has only this untracked WP8 handover document. |

The 129 warnings are the session's stable baseline (126 pre-existing plus 3 new, disclosed, accepted cross-document "Section N.M" false positives introduced by this session's own EIP/EBR prose, matching the same accepted false-positive class as every prior session) - no new *validate_repository.py errors* were introduced by any WP's final committed state.

---

## 8. Scope Check

- No `sentinel/` (trust boundary/policy classification) code was touched anywhere in the session.
- `jarvis/` code **was** modified this session (`jarvis/gia/observability.py` new, `jarvis/interfaces/stdio_rpc.py`, `jarvis/gia/__init__.py`, `jarvis/__init__.py`) - real backend code delivering GIA's first observability capability, confirmed distinct from and non-modifying of the pre-existing `jarvis/gia/bootstrap.py` (GIA-BOOT) at every WP.
- `src/` (UXP) was touched only in WP2, fully disclosed, live-verified (both CDP-based and the Programme Sponsor's own real hardware check), confirmed by Codex with no outstanding findings after two fix rounds.
- WP5 (ADR-0022) touches zero code, consistent with its explicit decision-only scope.
- A new dependency (`psutil`) was added at WP3, disclosed prominently in the EIP and delivery notes, not added silently.
- The working tree is clean and pushed; this handover document is the sole untracked file, being this review's own subject.

---

## 9. WP9 Baseline Recommendation

**Engineering Implementer's independent view:** cut a new baseline, `RBL-0017`.

Rationale: this session changed the running product in two materially significant ways. First, the Guardian Orb's entire rendering engine was replaced (SVG to Canvas 2D) - a user-visible change in how the flagship UXP element is drawn, directly comparable in kind to ESR-0028's WP4 rotation work that triggered `RBL-0016`. Second, and unlike ESR-0028, this session delivered a genuinely new backend capability: GIA's first real observability slice, a new Python module, a new third-party dependency, and a new JSON-RPC method exposed to the running application - none of which existed at `RBL-0016`. Both changes are real, live-verified (Canvas migration via CDP measurement and the Programme Sponsor's own Task Manager check; GIA via direct `gia.status` calls returning genuine host data) product capability changes, not governance churn or documentation-only work. This matches, and arguably exceeds in scope, the substance that warranted `RBL-0016`'s own cut.

**Engineering Reviewer's independent view (Codex):** cut a new baseline, `RBL-0017`. Recorded verbatim in the bridge return (`ESR-0029-WP8`, `20260719T151934Z-return-findings.md`): "ESR-0029 materially changed the running product in two baseline-worthy ways: the Guardian Orb rendering engine moved from SVG DOM to Canvas 2D with live performance/hardware verification, and GIA introduced the first real backend observability capability via a new psutil-backed Python module, dependency, JSON-RPC method, and live-verified host/resource/tool telemetry. This is more than governance churn and at least comparable in substance to the prior RBL-0016 trigger." Both independent views converge.

---

## 10. WP8 Verification Result

**Pass / no findings.** Engineering Reviewer (Codex) independently verified the submitted session range `1df2802..8530604` directly against repository evidence via the AIEMS Exchange Bridge (`ESR-0029-WP8`, returned `2026-07-19T15:19:34Z`, `repository_ref: 8530604737c659caeca7c7fba39b5be84b9ac77f`):

- Diff stat confirmed to match exactly: 19 files changed, 1,883 insertions, 203 deletions.
- Full file set confirmed to match the authorised/explained working set (Section 5) for every WP.
- `HEAD`/`main`/`origin/main` independently confirmed aligned at `8530604`, with only the WP8 handover itself untracked.
- Scope boundaries independently confirmed to hold: `jarvis/gia/bootstrap.py` and `jarvis/app.py`/`run()` startup untouched across the full session range; no `sentinel/` trust-boundary or policy code touched; `src/` changes confined to the disclosed WP2 Canvas migration; WP5 confirmed decision-only with no Sponsor-service implementation code present.
- Governance alignment independently confirmed coherent at HEAD across ADR-0021, ADR-0022, EIP-ESR0029-001 through -005, EBR-0001 (EBG-0082/0083/0084), and REG-0001/REG-0002.
- Validation evidence independently accepted (submitted pytest 295/295, `validate_repository.py` 0 errors/129 warnings, `npm run build` clean) plus one independently-run check: `git diff --check 1df2802..8530604` confirmed clean.

No drift found between the approved state and the actual repository. No findings raised.

---

## 11. WP9 Baseline Acceptance Result

**Accept - new baseline established.** The Programme Sponsor determined at ESR-0029 WP9 to accept a new baseline, [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]], superseding RBL-0016, agreeing with both independent views in Section 9. Recorded in `RBL-0017_REPOSITORY_BASELINE.md` (v1.0, Accepted), registered in REG-0001 (v3.257 to v3.258), with PST-0001's Current Repository Baseline references updated accordingly (v2.58 to v2.59).

---

## 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] | Approved-implemented package for WP2, v1.2. |
| [[EIP-ESR0029-002_GIA_PHASE1A_LOCAL_RESOURCE_OBSERVABILITY|EIP-ESR0029-002]] | Approved-implemented package for WP3, v1.1. |
| [[EIP-ESR0029-003_GIA_PHASE1B_STORAGE_STATE|EIP-ESR0029-003]] | Approved-implemented package for WP4, v1.1. |
| [[EIP-ESR0029-004_GIA_PHASE1C_PROCESS_HEALTH|EIP-ESR0029-004]] | Approved-implemented package for WP6, v1.0. |
| [[EIP-ESR0029-005_GIA_PHASE1D_ENGINEERING_ENVIRONMENT_STATE|EIP-ESR0029-005]] | Approved-implemented package for WP7, v1.0. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | Approved-implemented decision, implementation delivered at WP2. |
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | Approved decision for WP5, v1.1 - decision only, no implementation. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0082 (research), EBG-0083 (GIA Phase 1, Complete in full), EBG-0084 (Sponsor Approval Service, decision half Complete) all registered/updated this session. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for the session's controlled artefacts. |
| [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] | Prior accepted repository baseline. |
| [[ESR-0028_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0028 WP6 Handover]] | Precedent handover this document follows the structure of. |

---

## 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 19 July 2026 | Claude Engineering Implementer | Recorded the Programme Sponsor's WP9 determination: Accept - new baseline `RBL-0017` established, superseding RBL-0016 (Section 11), following a Codex post-commit review finding that v0.2 still described the acceptance as pending after the accepting commit had already landed. |
| 0.2 | 19 July 2026 | Claude Engineering Implementer | Recorded Engineering Reviewer (Codex) independent verification result: Pass / no findings, no drift found, full convergence with the Engineering Implementer's own view that a new baseline `RBL-0017` is warranted. Awaiting Programme Sponsor WP9 baseline acceptance determination. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Drafted ESR-0029 WP8 Independent Repository Verification handover, covering the full session diff (`1df2802`..`8530604`) across seven Work Packages. Records repository state, authorised working set, session observations (WP2's real performance-defect-found-and-fixed cycle, GIA's four-phase staged delivery with two genuine defects found and fixed, ADR-0022's operational-practice finding), validation evidence, and an independent baseline view (cut new baseline `RBL-0017`, given both a Guardian Orb rendering-engine change comparable to `RBL-0016`'s own trigger and a genuinely new backend capability GIA introduces). Submitted to the Engineering Reviewer via the AIEMS Exchange Bridge for genuine independent verification. |
