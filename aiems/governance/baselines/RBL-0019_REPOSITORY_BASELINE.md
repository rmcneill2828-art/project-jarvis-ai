# RBL-0019 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0019 |
| Title | ESR-0032 Repository Baseline (Deployment Alpha - Guardian Desktop Distribution, CI Build Gate Hardening, Release Automation) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0032 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 24 July 2026 |
| HEAD at baseline creation | `721fc06` |

---

# 2. Purpose

RBL-0019 records the repository baseline accepted by the Programme Sponsor at ESR-0032 WP5, superseding [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]]. ESR-0032 delivered Theme 1 - Deployment Alpha in full: all three items (EBG-0102 Guardian Desktop Distribution Foundation, EBG-0103 CI Build Gate Hardening, EBG-0104 Release Automation and Version Synchronisation) Complete in a single session, per the Programme Sponsor's own explicit choice at WP0B to pursue the entire theme rather than a smaller slice. This is the first time the product has been genuinely distributable, CI-gated, and releasable end to end - not merely built on a development machine - proven via a real installed Windows package, a real green GitHub Actions run across all four CI jobs, and a real published `v0.1.0` GitHub Release. Both independent WP4 views (Engineering Implementer and Engineering Reviewer) converged on this being baseline-worthy.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; the deployment/release-engineering capabilities delivered are build/distribution-pipeline improvements, not new user-facing UXP capabilities, so no PCB-0001 update was in scope |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0032 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0032_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP4 handover]] recorded two independently-reached views (Sections 9-10), both recommending a new baseline rather than retaining RBL-0018.

**Engineering Implementer's view**: this session delivered three genuine, live-verified capabilities that materially change what the product can do and how trustworthy its own delivery pipeline is - a real installable Windows package with a working sidecar-backed backend (WP1), a CI pipeline that actually builds/tests/gates the complete desktop product including a real Playwright acceptance suite (WP2), and a real, live-published first GitHub Release with automated cross-file version synchronisation (WP3). This is the first time the product has been genuinely distributable and releasable end to end, not merely built on a development machine.

**Engineering Reviewer's (Codex) independent view**: converged - "the range materially changes the product's distributability and release posture with a Tauri sidecar-backed Windows package path, expanded CI gates including Rust and Playwright, VERSION-based synchronization, and tag-triggered release automation; the scope is disclosed and fits Theme 1 Deployment Alpha rather than unrelated UXP drift." Codex independently confirmed the exact diff-stat figures, the file-list accuracy, and that no `sentinel/` trust-boundary or Sponsor Approval Service token-handling behaviour changed beyond mechanical fixes, before reaching this view.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `scripts/jarvis_backend_entry.py`, `scripts/build_backend_sidecar.py` (new) | Headless stdio-RPC entry point packaged via PyInstaller into a standalone sidecar executable, matching Tauri's `externalBin` convention. |
| `src-tauri/src/lib.rs` | New `BackendHandle` enum (`Dev`/`Sidecar`) and shared `dispatch_line()` let both the dev (`Command::new("python")`) and release (`tauri-plugin-shell`'s `Command::sidecar()`) paths share identical JSON-RPC dispatch logic. |
| `tauri-plugin-shell`, `src-tauri/capabilities/default.json` | Scoped `shell:allow-execute` permission for exactly one named sidecar - not a general shell-execute grant. |
| [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] | v1.0, Approved-implemented. Closes EBG-0102. Live-verified: a real `npm run tauri build` installer, System Health populated with genuine sidecar-backed data, zero orphaned processes on graceful exit, zero regression to dev mode. |
| `.github/workflows/ci.yml` | New `rust` job (build/clippy/fmt/test, blocking from introduction) and `playwright` job; `frontend-build`'s `npm audit` tightened to a real `--omit=dev` hard gate with no `continue-on-error`. |
| `playwright.config.js`, `tests/e2e/app.spec.js` (new) | 2 real committed acceptance tests, mocking Tauri's IPC layer via `page.addInitScript`. |
| [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]] | v1.0, Approved-implemented. Closes EBG-0103. Real Linux (WSL Ubuntu) verification found and fixed three genuine cross-platform bugs (`schemars`/`indexmap` build-dependency incompatibility, a Windows-only sidecar-build bug, a missing PNG icon) before the CI job was written. A further fix round resolved a real, pre-existing ruff-version-drift CI failure (unrelated to this session's own changes) discovered by checking the real GitHub Actions run rather than trusting local verification alone. |
| `VERSION` (new), `scripts/sync_product_version.py` (new) | Single authoritative version source, propagated into `pyproject.toml`/`package.json`/`src-tauri/Cargo.toml`/`src-tauri/tauri.conf.json` in one command; 8 new tests. Wired into CI as a blocking `--check` gate. |
| `.github/workflows/release.yml` (new) | Tag-triggered (`v*` only) release workflow: verifies the tag matches `VERSION`, builds the real installer, locates the exact NSIS artifact (fails on zero/multiple matches), computes its SHA-256, publishes via `softprops/action-gh-release` pinned to the immutable `v3.0.2` tag. |
| [[EIP-ESR0032-003_RELEASE_VERSION_SYNCHRONISATION|EIP-ESR0032-003]] | v1.0, Approved-implemented. Closes EBG-0104. **Live-verified, not merely structurally reviewed**: a real `v0.1.0` GitHub Release exists (this repository's first-ever), confirmed via `gh release view v0.1.0` with the installer and its SHA-256 checksum attached. A genuine `GITHUB_TOKEN` permissions bug was found and fixed via the real tag push. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0102, EBG-0103, and EBG-0104 all Complete - all three Theme 1 items delivered in one session. |
| Test suite | 359 tests, up from RBL-0018's 351 - 8 new from `sync_product_version.py`; no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. This session's deliverables are deployment/release-engineering capabilities (installability, CI trustworthiness, release publication) rather than new user-facing UXP capabilities - PCB-0001's own scope (product capability tiers a user or Guardian interaction can exercise) is not affected by this baseline.

---

# 7. Architecture Outcomes

- First genuine end-to-end distribution path for the product: a PyInstaller-packaged Python backend spawned as a Tauri sidecar via `tauri-plugin-shell`, rather than requiring a development Python environment on the target machine.
- First real Rust/Tauri CI build gate - `cargo build`/`clippy -D warnings`/`fmt --check`/`test` all genuinely blocking, discovered and fixed a real cross-platform build-dependency incompatibility (`schemars`/`indexmap`) that would otherwise have silently blocked every future Linux build.
- First real browser-driven acceptance test suite (Playwright), mocking the Tauri IPC boundary to verify the actual React UI renders correctly against real (if mocked) backend responses - not just unit-level Python/Rust tests.
- First genuinely trustworthy CI gate: checking the real GitHub Actions run (not just local verification) after WP2's push caught a real, pre-existing ruff-version-drift failure that had been silently failing since before this session began - a direct product of making the gate actually checked rather than assumed green.
- First automated cross-file version synchronisation and first tag-triggered release automation - a single `VERSION` file propagated across four independent build manifests, and a real, live-verified GitHub Release pipeline producing a checksummed installer artifact.
- A real, previously-unknown GitHub Actions permissions gap (`GITHUB_TOKEN` defaults to read-only) was found and fixed only because a real release tag was actually pushed, rather than the release workflow being merely structurally reviewed and left untested.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0033 artefact is created by this baseline - ESR-0032 remains open pending formal session closure;
- code signing for the Windows installer remains out of scope - a separate, larger undertaking (certificate acquisition/cost), disclosed but not addressed;
- multi-OS bundle targets (Linux/macOS) remain out of scope - only Windows/`nsis` is configured in `tauri.conf.json` today;
- changelog automation remains out of scope - no changelog convention exists yet in this repository;
- `Cargo.lock`/`package-lock.json` are intentionally left for `cargo`/`npm` to regenerate on the next real version bump - derived artifacts, not authoritative version carriers, not hand-synchronised by this baseline's tooling;
- the low-resolution app icon (upscaled from a single 32x32 source, disclosed at WP2) remains a future design task, not addressed by this baseline.

---

# 9. Verification

Repository validation performed during ESR-0032 WP4/WP5:

- Git working tree was clean; the session's intended content range (`077f31b`..`4ec539b`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main` at every commit in the session (confirmed via real GitHub Actions CI runs, not assumed).
- 359/359 tests passing, up from RBL-0018's 351 (8 net-new tests; no regressions).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 149 warnings (consistent with the pre-existing false-positive pattern, not a new class of problem).
- `cargo build --manifest-path src-tauri/Cargo.toml` clean.
- `npm run build` clean.
- `npx playwright test` - 2/2 passing.
- `python scripts/sync_product_version.py --check` - all four build files agree with `VERSION`.
- `git diff --stat 077f31b..4ec539b` independently re-run by the Engineering Reviewer, confirmed to match exactly (70 files, 1,788 insertions, 191 deletions).
- Real GitHub Actions CI green across all four jobs (`python`, `rust`, `playwright`, `frontend-build`) on the final session commit (`721fc06`).
- Real, live-verified GitHub Release at `v0.1.0` - confirmed via `gh release view v0.1.0`: non-draft, non-prerelease, with the installer and its SHA-256 checksum attached.
- The Engineering Reviewer performed WP4 Independent Repository Verification: **Pass, no blocking findings** - independently confirmed the diff-stat figures, file-list accuracy, and that no `sentinel/` trust-boundary or Sponsor Approval Service token-handling behaviour changed beyond mechanical fixes.
- The Programme Sponsor's own WP5 determination: establish a new baseline rather than retain RBL-0018 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0032** - the Engineering Session Report remains to be authored separately, following this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0102/0103/0104 all Complete.
5. [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]], [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]], [[EIP-ESR0032-003_RELEASE_VERSION_SYNCHRONISATION|EIP-ESR0032-003]], and the [[ESR-0032_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP4 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0032_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0032 WP4 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] | Approved-implemented package for the Guardian Desktop Distribution Foundation. |
| [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]] | Approved-implemented package for CI Build Gate Hardening. |
| [[EIP-ESR0032-003_RELEASE_VERSION_SYNCHRONISATION|EIP-ESR0032-003]] | Approved-implemented package this baseline's release automation was implemented against. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not affected by this session's deployment/release-engineering scope. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0102/0103/0104 all Complete. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0018, following the Engineering Reviewer's WP4 Pass and the Programme Sponsor's explicit WP5 decision to cut a new baseline rather than retain RBL-0018: all three Theme 1 - Deployment Alpha items (EBG-0102, EBG-0103, EBG-0104) delivered a genuinely distributable, CI-gated, and releasable product for the first time, agreeing with both independent WP4 baseline views. |
