# EIP-ESR0052-001 - Process/Tooling Currency Cluster (EBG-0122 through EBG-0124)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0052-001 |
| Title | Engineering Implementation Package: WP1 Process/Tooling Currency Cluster |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0052 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0052 WP1: clears the three concrete, low-risk currency-drift findings from [[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]] (EBG-0122, EBG-0123, EBG-0124), following the Programme Sponsor's direction to open ESR-0052 and draft a Work Package informed by that review.

Per PBK-0001's Feature-First Delivery Discipline, this cluster is process/tooling only and does not by itself satisfy "every Engineering Session shall deliver product-moving engineering work" - flagged here plainly rather than silently left implicit. WR-ESR0052-001 Section 7 already recommended pairing this cluster with a product objective (EBG-0115 Kokoro TTS evaluation or EBG-0111 Composio assessment); that pairing is a decision for the Programme Sponsor on a subsequent Work Package, not assumed or pre-drafted by this package.

---

# 3. Repository Context Investigated

* `package-lock.json` / `npm audit` (full): 4 vulnerabilities (1 moderate, 3 high) - `esbuild`/`vite` (moderate, dev-server-only, requires the major Vite bump this package does not scope), `nanoid` (high) and `postcss` (high), both fixable via a plain, non-forced `npm audit fix`.
* `npm audit --omit=dev`: 0 vulnerabilities - confirms the shipped production bundle is unaffected either way.
* `.github/workflows/ci.yml`: `pip-audit` step currently runs with `continue-on-error: true`, per its own code comment "advisory only until an initial findings baseline has been triaged."
* `pip-audit` (local): 1 finding - `pip` 26.1.2 itself, PYSEC-2026-3721, fixed in 26.2. Not a pinned project dependency; the CI runner's own bundled `pip` version is not independently known from this environment.
* No `.github/dependabot.yml` or `.renovate.json` exists anywhere in the repository.
* Existing CI ecosystem boundaries already separated by job (`ci.yml`): Python at repository root (`pyproject.toml`), frontend at repository root (`package.json`), Rust at `src-tauri/` (`Cargo.toml`), plus the workflow files themselves (`.github/workflows/`).

---

# 4. Scope by Item

## 4A. EBG-0122 - Frontend Dependency Vulnerability Remediation

Run `npm audit fix` (non-forced) to update `package-lock.json`, resolving the `nanoid` and `postcss` advisories. Re-run `npm audit` afterward to confirm only the `esbuild`/`vite` moderate finding remains (expected, since clearing it requires the major Vite bump this package explicitly excludes). No `package.json` version-range change unless `npm audit fix` itself requires one to satisfy a transitive constraint - if it does, that shall be disclosed in the completion report rather than silently accepted.

## 4B. EBG-0123 - Dependency-Freshness Automation

New `.github/dependabot.yml`, weekly cadence, four `package-ecosystem` entries mirroring `ci.yml`'s existing per-technology job boundaries: `npm` at `/`, `pip` at `/`, `cargo` at `/src-tauri`, `github-actions` at `/.github/workflows`. No auto-merge configuration - update PRs land for the Programme Sponsor's own review and merge, consistent with this project's standing Git-operations authority model (PBK-0001 Repository Lifecycle and Separation of Duties).

## 4C. EBG-0124 - `pip-audit` CI Gate Hardening

Remove `continue-on-error: true` from `ci.yml`'s `pip-audit` step. The step's surrounding comment ("Advisory only until an initial findings baseline has been triaged") is updated to reflect that the baseline now exists and has been triaged, rather than left describing a now-stale precondition.

---

# 5. Validation

* `npm audit` and `npm audit --omit=dev` re-run after 4A, confirming the expected vulnerability count.
* `npm run build` - confirms the dependency update does not break the production build.
* `python scripts/validate_repository.py` (full mode) after all changes.
* `python -m pytest jarvis/tests sentinel scripts/tests` - no Python production code touched by this WP, so the count should remain unchanged (523 passed, 1 skipped).
* **Disclosed limitation, not resolved by this package**: 4C's actual effect on CI (whether the hosted runner's own `pip` is already patched, or whether the hardened gate now fails a real CI run) can only be confirmed once this change is pushed and a real workflow run completes - noted in EBG-0124's own register entry as well. If it does fail, the recommended response is fixing the underlying finding (e.g. an explicit `pip install --upgrade pip` step before the audit), not silently reverting to `continue-on-error: true`.

---

# 6. Explicitly Excluded

* The React 18 -> 19 upgrade (WR-ESR0052-001 Section 6: real, but needs its own regression-tested Work Package, not this trivial cluster).
* The Vite major-version bump (low urgency, dev-tooling-only exposure per WR-ESR0052-001 Section 2/7).
* Any MCP-based rearchitecture of the existing Agent Framework (WR-ESR0052-001 Section 5/7: needs a scoped design conversation, not a backlog line item).
* Any change to `sentinel/openai_provider.py` or its endpoint choice (WR-ESR0052-001's Chat-Completions-vs-Responses-API finding, recorded in its Independent Second Opinion addendum: worth evaluating, not scoped for action here).
* A local/CI `pip` self-update as a repository change - `pip`'s version is ambient per-environment tooling (the local `.venv` and each CI job's `actions/setup-python` bundle), not a value pinned anywhere in this repository, so there is no file for this package to diff.
* Any Sentinel/security-relevant code path.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0052`/`WP1`). **Verdict: Conditional Pass with correction**, timestamp 2026-08-26T08:46:48Z. Codex independently verified Section 4's scope against the live EBG-0122/0123/0124 register rows (no exceedance found) and re-checked repository context directly where its own environment allowed: `.github/workflows/ci.yml` still carries `pip-audit`'s `continue-on-error: true` with the advisory-baseline comment; `pyproject.toml` has no pinned `pip` and `pip-audit` only in `dev` extras; `package.json` still shows React 18/Vite 5.4.11; no `.github/dependabot.yml`/`.renovate.json` exists; `validate_repository.py` passes with 0 errors. Disclosed limitation: a direct `npm audit` re-run was blocked by Codex's own shell execution policy, so that one specific claim was not independently re-executed (consistent with the same class of disclosed environment limitation in WR-ESR0052-001's own Codex review). Registration consistency (REG-0001, EBR-0001, ESR-0052 versions) confirmed aligned. **Required correction, folded into v0.2 above:** Section 6's `sentinel/openai_provider.py` exclusion line contained a plain-text "Section 10" reference that `validate_repository.py` flags as an unresolved same-document section heading (this document only numbers to Section 8) - a controlled-document hygiene issue, not a scope or design blocker. Reworded to remove the bare section-number reference.

---

# 8. Related Artefacts

* [[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]] - source of all three items in this cluster.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0122 through EBG-0124, all updated by this package.
* [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] - this session's report, WP1.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Feature-First Delivery Discipline (Section 2's disclosure), Repository Lifecycle and Separation of Duties (Section 4B's no-auto-merge rationale).
