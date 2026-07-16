# ESR-0022 WP6 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0022-WP6 |
| Title | Independent Repository Verification Handover |
| Version | 0.2 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | ESR-0022 |
| Effective Date | 16 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0022 WP1 for WP6 Independent Repository Verification. WP6 should confirm that the repository state on `main` matches the claims made by the pushed commit, that the disclosed process deviation and its correction are accurately characterised, and that no unauthorized scope drift occurred.

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `https://github.com/rmcneill2828-art/project-jarvis-ai.git` |
| Branch | `main` |
| Expected `HEAD` | `e4a04a0` |
| Confirmed | Local `HEAD` and `origin/main` both resolve to `e4a04a0` (`git rev-parse --short HEAD` / `origin/main` after `git fetch origin main`) |
| Prior accepted baseline | `RBL-0014` |

---

## 4. Commits

Single commit since the prior accepted baseline:

| # | SHA | One-line summary |
|---|---|---|
| 1 | `e4a04a0` | ESR-0022 WP1: production provider wiring, System Health panel, sidecar cwd fix. |

---

## 5. Session Observations

1. **Self-disclosed process deviation, corrected before any commit.** An earlier revision of EIP-ESR0022-001 (v0.1) described an implementation that had already been drafted and locally tested before the package existed - a real sequencing failure against PBK-0001's Working Report Lifecycle (Approval Before Change). The Engineering Reviewer correctly declined to approve that retroactively. The implementation was fully reverted (`git restore`) - it was never committed, so no trace of the deviation exists in repository history. EIP-ESR0022-001 was then rewritten as v0.2, a genuine prospective package with no code written, reviewed by the Engineering Reviewer (who also raised a Medium finding on blank-model-env-var handling, incorporated into the design), and approved by both the Engineering Reviewer and the Programme Sponsor before real implementation began. The single commit on `main` (`e4a04a0`) reflects only that approved, post-review implementation.
2. **Scope addition beyond the EIP, separately authorised.** During the Programme Sponsor's live visual verification of the implementation (via `npm run tauri dev`), the Python sidecar failed to start (`No module named jarvis`, repeated). Root-caused directly (confirmed by reproducing the identical failure with cwd manually set to `src-tauri/`): `spawn_backend()` in `src-tauri/src/lib.rs` never anchored the child process's working directory, and `jarvis` is not pip-installed in this environment - it only resolves via the cwd-based `sys.path` entry Python's `-m` flag adds, which requires cwd to be the repository root. Fixed by anchoring to `CARGO_MANIFEST_DIR`'s parent (compile-time constant, not launch-time state), so it no longer depends on where `cargo run`/`tauri dev` was invoked from. This was outside EIP-ESR0022-001's authorised file list (`src-tauri/src/lib.rs` was not one of the 10 authorised files); the Programme Sponsor explicitly authorised this specific fix directly ("Fix it now please as i cant approve the WP without viewing it") rather than through a separate EIP, given its small, mechanical, well-understood nature and that it was blocking the Sponsor's own verification of the approved package.
3. **New backlog item recorded, no implementation.** EBG-0073 (UXP Duplicate Monitoring Elements Tidy-up) was added to EBR-0001 as `Approved Backlog`: the Programme Sponsor observed live that the new `SystemHealthPanel` visibly duplicates `DiagnosticsPanel`'s Guardian/Sentinel/Providers rows. No code changed for this item; it is backlog documentation only, deferred to a future session.
4. **Live verification performed, not just automated tests.** Both the original implementation and the sidecar fix were verified against the real Tauri desktop app (`npm run tauri dev`), not only against pytest/Playwright-mocked checks - the Guardian runtime confirmed starting successfully (`INFO jarvis.guardian.runtime: Guardian runtime foundation started.`) after the fix.

---

## 6. Validation Evidence

Validation re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 209 passed |
| `python scripts/validate_repository.py` (full mode, not `--governance-only` - this session's changes include source code) | Passed, 0 errors, 85 warnings |
| `git diff --check` | Clean |
| `git rev-parse --short HEAD` | `e4a04a0` |
| `git rev-parse --short origin/main` | `e4a04a0` |
| `git status --short` | Clean |

The 85 warnings are the same pre-existing, non-blocking set present at every prior session's closure (unchanged count).

---

## 7. Scope Check

- No changes to `scripts/validate_repository.py`.
- No changes to `PEM-001`, `STD-0006`, or `EBG-0050`'s remaining scope - all explicitly excluded by EIP-ESR0022-001 Section 8.
- `src-tauri/src/lib.rs` was changed outside the EIP's authorised file list, but directly and explicitly authorised by the Programme Sponsor as its own small, separately-scoped fix (Section 5, item 2) - not an unauthorised or silent scope expansion.
- No other files outside the EIP's 10 authorised files plus the `src-tauri/src/lib.rs` fix and the EBG-0073 backlog documentation were modified.

---

## 8. WP7 Baseline Recommendation

This one is less clear-cut than ESR-0020/ESR-0021's "retain, incremental" pattern, and is flagged for the Engineering Reviewer's and Programme Sponsor's own judgement rather than presumed here:

**Case for retaining RBL-0014:** the delivered UXP change (System Health panel) is incremental in the same way ESR-0020/ESR-0021's UXP work was; the backend change is additive/configurable (falls back to `LocalEchoProvider` if no credential is present) rather than a structural architecture change.

**Case for a new baseline:** this is the first session where JARVIS/Guardian's *default* production conversation path can call a real external AI model rather than only the deterministic local echo - arguably a different kind of milestone than a UXP panel addition, closer in kind to ESR-0019's knowledge-graph delivery (which did receive a new baseline, RBL-0014).

No recommendation is asserted either way in this handover; Section 9 below asks the Engineering Reviewer to form an independent view.

**Resolved.** Engineering Reviewer WP6: Pass. Programme Sponsor's own WP7 determination: establish a new baseline, not retain RBL-0014 - RBL-0014 is explicitly the ESR-0019 baseline for the knowledge-graph delivery; this session adds the first default production provider wiring path, changing Guardian's normal runtime behaviour, not just its presentation, a materially new operational capability, made stronger by the combination of a different default execution path plus a new live UXP status surface. Recorded as [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]].

---

## 9. What WP6 Should Produce

WP6 should produce:

1. Confirmation that the repository state on `main` matches the claims made by commit `e4a04a0`.
2. Confirmation that the process-deviation disclosure (Section 5, item 1) is accurately characterised - in particular, that no trace of the reverted retroactive implementation exists in repository history.
3. An independent view on Section 8's open question: retain `RBL-0014` or recommend a new baseline.
4. A recommendation to the Programme Sponsor on WP7 closure.

---

## 10. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] | Approved package this session's implementation follows. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Roadmap used to select this session's WP (Track B/C Near-term Backlog Acceleration Opportunity). |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and workflow context. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register updated for EBG-0070/EBG-0072 (Complete) and EBG-0073 (new). |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for the session's changes. |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Prior accepted baseline. |

---

## 11. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 16 July 2026 | Claude Engineering Implementer | Recorded resolution of Section 8's open baseline question: Engineering Reviewer WP6 Pass; Programme Sponsor WP7 determination to establish a new baseline (RBL-0015) rather than retain RBL-0014, judging production provider wiring a materially new operational capability. RBL-0015 drafted and registered accordingly. |
| 0.1 | 16 July 2026 | Claude Engineering Implementer | Drafted WP6 Independent Repository Verification handover for ESR-0022: records the single commit, validation evidence, disclosed process deviation and its correction, the separately-authorised sidecar fix, and an open (not pre-decided) WP7 baseline question for the Engineering Reviewer. |
