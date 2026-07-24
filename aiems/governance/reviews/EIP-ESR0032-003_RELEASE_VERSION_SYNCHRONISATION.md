# EIP-ESR0032-003 - Release Automation and Version Synchronisation (EBG-0104)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0032-003 |
| Title | Release Automation and Version Synchronisation |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Engineering Session | ESR-0032 |
| Closes | EBG-0104 (Candidate Backlog, High) |

---

# 2. Purpose

Closes EBG-0104: `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml` and `src-tauri/tauri.conf.json` each carry their own independent version field (all currently `0.1.0`), with no mechanism preventing the four from drifting apart, and no automated release workflow of any kind exists.

---

# 3. Objective

Choose one authoritative version source, provide a single command that updates all four build files together from it, add a CI check that fails if any of the four drift from each other, and add a tag-triggered release workflow that builds the desktop installer, generates SHA-256 checksums, and publishes both as a GitHub Release artifact.

---

# 4. Repository Context

- Confirmed directly: all four files currently read `0.1.0` (`pyproject.toml:3`, `package.json:3`, `src-tauri/Cargo.toml:3`, `src-tauri/tauri.conf.json:4`). No test, script, or CI step currently checks they agree.
- `scripts/bump_version.py` already exists as this repository's version-bump precedent, but it is scoped entirely to **controlled governance artefacts** registered in REG-0001 (EIPs, ADRs, etc.) - it reads/writes a `**Version:**` badge plus a Document Control table row, and maintains REG-0001's own tracking row for that artefact. None of that machinery applies to product build files, which have no REG-0001 row, no badge, and no Version History table - a new, separate tool is needed, not an extension of `bump_version.py`.
- `.github/workflows/ci.yml` (per EIP-ESR0032-002, this session's WP2) currently runs on every push/PR to `main` - no tag-triggered workflow exists.
- No GitHub Release has ever been created in this repository (confirmed: `gh release list` returns nothing) - this WP would be the first.
- WP1 (EIP-ESR0032-001) already produced a real installer once, manually, via `npm run tauri build` (`JARVIS Guardian Shell_0.1.0_x64-setup.exe`) - this WP automates that same build, not a new build mechanism.

---

# 5. Scope

**In scope:**

1. A new repo-root `VERSION` file (plain text, single line, e.g. `0.1.0`) as the single authoritative source - chosen over designating one of the four existing files as "primary" because each of those four is itself a tool-specific manifest (npm, Cargo, Python packaging, Tauri config) with its own unrelated fields; a dedicated file avoids implying any one tool's config format has special authority over the others.
2. `scripts/sync_product_version.py` (new): reads `VERSION`, writes the matching version string into `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml`, and `src-tauri/tauri.conf.json`. Takes the new version as a CLI argument (updates `VERSION` itself first, then propagates), mirroring `bump_version.py`'s "refuse to guess, error clearly" style rather than silently proceeding on an unexpected existing value.
3. A `version-sync` check added to `.github/workflows/ci.yml`'s existing `python` job (or a new lightweight job - decided during implementation based on which is clearer): reads all five version fields (`VERSION` plus the four build files) and fails the build if any disagree.
4. A tag-triggered `release.yml` workflow: on push of a `v*` tag, runs `npm run tauri build` (Windows, matching this repository's actual current target - `src-tauri/tauri.conf.json`'s `bundle.targets` is `["nsis"]`, Windows-only, no Linux/macOS bundle target configured, so a multi-OS release matrix is not yet meaningful and is out of scope here), computes the installer's SHA-256 checksum, and publishes both the installer and a `.sha256` checksum file as a GitHub Release's attached assets via `softprops/action-gh-release` (a widely-used, actively maintained action - avoids hand-rolling the GitHub Releases API against `gh release create`/`gh release upload` from within a workflow).

**Out of scope (explicitly deferred, not silently dropped):**

- Code signing the installer - a separate, larger undertaking (certificate acquisition/cost) already disclosed as out of scope by EIP-ESR0032-001 and not reopened here.
- A multi-OS release matrix (Linux/macOS bundles) - `tauri.conf.json` does not configure bundle targets for either today; adding them is a product-packaging decision independent of this WP's version-sync purpose.
- Automatic changelog generation - no changelog convention exists yet in this repository; a future EBG, not invented here.
- Actually cutting a real, public release this session as this EIP's own verification evidence - explicitly flagged in Section 10 (Validation) as a decision for the Programme Sponsor, since it is the first GitHub Release this repository would ever have and visible outside the repository's commit history.

---

# 6. Authorised Files

- `VERSION` (new)
- `scripts/sync_product_version.py` (new)
- `scripts/tests/test_sync_product_version.py` (new)
- `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json` (version fields only, via the new script - confirming it works, not hand-edited)
- `.github/workflows/ci.yml` (new version-equality check)
- `.github/workflows/release.yml` (new)

No other files may be modified without a further approved package.

---

# 7. Implementation Requirements

1. `sync_product_version.py` shall refuse to run (no files written) if any target file's existing version field cannot be parsed, rather than guessing or skipping it silently - matching `bump_version.py`'s own established error-handling convention in this repository.
2. The CI version-equality check shall be a real blocking gate, not advisory - unlike `pip-audit`/`npm audit`, there is no pre-existing drift to triage (all four agree today), so no grace-period carve-out is warranted.
3. `release.yml` shall only run on `v*` tag pushes, never on ordinary commits to `main` - it must not fire on every push the way `ci.yml` does.
4. The release workflow shall compute the SHA-256 checksum from the actual built installer artifact within the same job run, not a value entered by hand.

---

# 8. Explicit Exclusions

- No code signing.
- No multi-OS bundle targets.
- No changelog automation.
- No real tag push / public GitHub Release performed as part of this WP's own implementation without a separate, explicit Programme Sponsor decision (Section 10).

---

# 9. Constraints

- `softprops/action-gh-release` is a third-party GitHub Action (not an official `actions/*` one) - a reasonable, extremely widely-adopted choice (used across large open-source projects) for this exact purpose, but disclosed as a new external dependency in the CI supply chain, consistent with this repository's practice of disclosing rather than silently accepting new third-party trust.
- The release workflow can only be verified structurally (`act`-style local dry runs are not reliable for artifact-upload steps) until a real tag is pushed - Section 10 addresses how this WP's verification bar is set given that constraint.

---

# 10. Validation

- `python scripts/sync_product_version.py 0.1.1` run locally, confirming all four build files update correctly and `VERSION` itself updates; then reverted back to `0.1.0` before commit (this WP does not itself decide to bump the product's real version).
- New unit tests for `sync_product_version.py` covering: successful sync, refusal on an unparseable existing field, refusal on a no-op version.
- `python -m pytest` and `python scripts/validate_repository.py` both clean (neither should be affected by this WP).
- The new CI version-equality check verified locally by deliberately drifting one file and confirming the check script exits non-zero, then reverting.
- **Live-verified, not merely structurally reviewed**: the Programme Sponsor explicitly authorised pushing a real `v0.1.0` tag. The first attempt (commit bfee19a) built the installer and computed its checksum successfully but failed at the final publish step - `softprops/action-gh-release` returned "Resource not accessible by integration" because this repository's default `GITHUB_TOKEN` workflow permission is read-only (confirmed via `gh api repos/.../actions/permissions/workflow`) and the workflow never requested `contents: write`. Fixed with a job-level `permissions: contents: write` block (commit 42c7e82, Codex-reviewed, no findings) scoped to only this workflow rather than changing the repository-wide default. The `v0.1.0` tag was moved to the fixed commit and re-pushed (the first attempt never published a release, so nothing was overwritten) - the second run passed every step, and `gh release view v0.1.0` confirms a real, non-draft, non-prerelease GitHub Release with both `JARVIS Guardian Shell_0.1.0_x64-setup.exe` and its `.sha256` checksum attached.

---

# 11. Risks and Dependencies

- **Untested release workflow risk**: per Section 10, `release.yml` may not be live-verified this session if the Programme Sponsor prefers not to cut a real tag yet - disclosed upfront rather than silently assumed correct.
- **No dependency on WP1 or WP2** - self-contained, touches a disjoint file set (only `tauri.conf.json`'s version field overlaps with WP1/WP2's own changes, and only its value, not structure).
- **`softprops/action-gh-release` version pinning**: pinned to a specific tagged release (not `@main`) to avoid an unreviewed upstream change silently altering release behaviour.

---

# 12. Approval Request

Requesting Programme Sponsor approval to proceed with implementation as scoped above, following Engineering Reviewer review of this draft. Separately requesting explicit direction on whether to push a real `v0.1.0` tag as this WP's own live verification of `release.yml`, per Section 10.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0104 (High, Candidate Backlog), closed by this package. |
| [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] | WP1, same session - produced the installer this WP's release workflow now automates the build of. |
| [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]] | WP2, same session - `ci.yml`'s existing structure this WP extends with a new check and a new sibling workflow file. |
| [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] | Current accepted repository baseline this work builds on. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 July 2026 | Claude Engineering Implementer | Approved and implemented (commit bfee19a); fix round (commit 42c7e82) added job-level `contents: write` permissions after a real `v0.1.0` tag push found `release.yml`'s build succeeding but `softprops/action-gh-release` failing to publish due to this repository's read-only default `GITHUB_TOKEN` permission. Live-verified end to end, not merely structurally reviewed: a real GitHub Release now exists at `v0.1.0` with the installer and its SHA-256 checksum attached. Closes EBG-0104. |
| 0.1 | 24 July 2026 | Claude Engineering Implementer | Initial draft, closing EBG-0104. Scoped to a repo-root `VERSION` file as the single authoritative source, a new `sync_product_version.py` script, a blocking CI version-equality check, and a tag-triggered `release.yml` building the installer and publishing SHA-256 checksums via `softprops/action-gh-release`. Explicitly flags that actually pushing a real release tag is a separate Programme Sponsor decision, not assumed as part of this WP's own verification. |
