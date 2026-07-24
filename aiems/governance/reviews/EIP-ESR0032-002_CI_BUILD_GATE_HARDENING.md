# EIP-ESR0032-002 - CI Build Gate Hardening (EBG-0103)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0032-002 |
| Title | CI Build Gate Hardening |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Engineering Session | ESR-0032 |
| Closes | EBG-0103 (Candidate Backlog, High) |

---

# 2. Purpose

Closes EBG-0103: CI currently builds neither Rust nor the full desktop product, and `frontend-build`'s `continue-on-error` is set at the job level (covering even the `npm run build` compile step itself, not just the advisory `npm audit` step). Both are real gaps independently verified against `.github/workflows/ci.yml` by two external reviews and both AI reviewers this session.

---

# 3. Objective

Add a real Rust CI job (build, clippy, fmt check, test); narrow `frontend-build`'s `continue-on-error` to only its `npm audit` step, matching the precedent already established for the Python job's `pip-audit` step; and, per Programme Sponsor direction to expand this WP's scope, add a genuine committed Playwright acceptance suite (previously an unused dependency with zero committed tests in this repository's history) and wire it into CI as an enforced check.

---

# 4. Repository Context

- `.github/workflows/ci.yml` runs on `ubuntu-latest`. The existing `python` job is a real gate (`pytest`, `validate_repository.py` block the pipeline; only `pip-audit` is advisory). The existing `frontend-build` job has `continue-on-error: true` at the job level - confirmed directly, this covers the `npm run build` step itself, not only `npm audit`.
- No Rust/Tauri build step exists in CI at all - confirmed directly, no `cargo`/`rustc` invocation anywhere in the workflow file.
- Local verification performed on this (Windows) development machine ahead of drafting this EIP: `cargo clippy --manifest-path src-tauri/Cargo.toml` is completely clean (zero warnings, including on this session's own WP1 restructuring) - no pre-existing lint backlog to triage, unlike `pip-audit`'s precedent. `cargo fmt --check` initially found 15 formatting diffs across all 3 source files (`build.rs`, `lib.rs`, `main.rs`) - this codebase had never been run through `rustfmt`; applied directly ahead of this EIP (a mechanical, safe, zero-behaviour-change reformat), now clean.
- **Update: the Linux build was, in fact, locally verified** - the Programme Sponsor pointed out a WSL Ubuntu 26.04 installation exists on this machine, previously unused for this purpose. Installed the documented system packages (`build-essential`, `curl`, `wget`, `file`, `libssl-dev`, `libgtk-3-dev`, `librsvg2-dev`, `libwebkit2gtk-4.1-dev`, `libayatana-appindicator3-dev`, `patchelf`) plus a Rust toolchain, and ran a real `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test` against this exact repository under WSL. This surfaced three genuine, real bugs, all fixed and re-verified before this EIP's implementation:
  1. **`schemars` 0.8.22 / `indexmap` 1.9.x incompatibility**: `tauri-build`/`tauri-utils`/`tauri-plugin` pull in `schemars` for Linux/dbus capability-schema generation (a code path Windows never exercises, explaining why WP1's Windows build never hit this). `schemars` 0.8.22 requests `indexmap`'s `serde-1` feature but never `std`; `indexmap` 1.9.x has no default features at all, so without `std`, `indexmap`'s own `#[cfg(has_std)]` split compiles `IndexMap<K, V, S>` with no default for `S`, breaking `schemars`'s `type Map<K, V> = indexmap::IndexMap<K, V>;` alias (`error[E0107]`). Fixed by adding an explicit `indexmap = { version = "1.9", features = ["std"] }` to `[build-dependencies]`, forcing the feature on via Cargo's feature unification - re-verified compiling clean on Linux afterward.
  2. **`scripts/build_backend_sidecar.py` was Windows-only**: hardcoded a `.exe` suffix when locating PyInstaller's own output and naming the copied Tauri sidecar, but PyInstaller (and Tauri's own `externalBin` convention) produce no extension at all on Linux/macOS. Fixed by branching the suffix on whether `"windows"` appears in the target triple; also switched `shutil.copyfile` to `shutil.copy`, since the former silently drops the source file's executable permission bit (would have produced a sidecar Tauri could find but not execute). Re-verified: a real Linux sidecar built, executed directly with a genuine `platform.status` round-trip, and consumed successfully by a full Linux `cargo build`.
  3. **Missing PNG icon**: only `icons/icon.ico` (Windows-only format, and only a single 32x32 size embedded) existed; Tauri's `generate_context!()` macro fails outright on any platform without a PNG present. Regenerated the full icon set via `npx tauri icon`, removing the iOS/Android/Windows-Store assets it also generates (out of scope - no mobile targets exist), keeping only `32x32.png`/`128x128.png`/`128x128@2x.png`/`icon.icns`/`icon.ico`, and updated `tauri.conf.json`'s `bundle.icon` array accordingly. **Disclosed, not fixed by this WP**: the only available source is a 32x32 icon, upscaled by Tauri's own tool - functionally sufficient for CI/bundling to succeed, but a proper high-resolution source icon is a separate, future design task, not addressed here.
  After all three fixes, a full `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test` passed cleanly on real Ubuntu 26.04 under WSL - genuine local verification, not merely "the first real CI run will tell us." The real GitHub Actions run after this WP's push remains a further confirmation (a genuinely clean environment, vs. this WSL install), but is no longer the *sole* verification evidence for the Linux path.
- `playwright` (`^1.61.1`, bare automation library) is a `package.json` devDependency; `@playwright/test` (the test-runner/assertion package) is not yet installed. No `.spec.*` file or `playwright.config.*` exists anywhere in this repository's git history - confirmed directly, zero prior commits.
- Real DOM structure confirmed by direct source read of `src/App.jsx`: the chat input has placeholder `"Ask Guardian anything..."`, the submit button `aria-label="Send"`, the System Health panel has class `system-health-panel`. `invoke()` calls exactly three commands: `platform_status`, `knowledge_graph`, `send_message`.
- The Tauri IPC mocking mechanism this repository's own prior ad hoc Playwright checks used (per EBG-0072/EBG-0073's delivery notes) is confirmed by direct source read of `node_modules/@tauri-apps/api/core.js`: `invoke(cmd, args, options)` calls `window.__TAURI_INTERNALS__.invoke(cmd, args, options)` directly - a real committed suite can inject an equivalent mock via Playwright's `page.addInitScript()`, matching the same mechanism.

---

# 5. Scope

**In scope:**

1. Add a `rust` job to `.github/workflows/ci.yml`: install Tauri's documented Linux system dependencies, then run `cargo build --manifest-path src-tauri/Cargo.toml`, `cargo clippy --manifest-path src-tauri/Cargo.toml -- -D warnings`, `cargo fmt --manifest-path src-tauri/Cargo.toml --check`, and `cargo test --manifest-path src-tauri/Cargo.toml` (no Rust unit tests exist today; this asserts none silently fail to compile, and covers any added in the future). All four are blocking - clippy and fmt are already genuinely clean locally, so unlike `pip-audit` there is no pre-existing backlog justifying an advisory carve-out.
2. Narrow `frontend-build`'s `continue-on-error` from the job level to only its `npm audit --audit-level=high` step, mirroring the `python` job's existing `pip-audit` pattern exactly. `npm run build` itself becomes a real blocking gate.
3. Add `@playwright/test` as a devDependency; a `playwright.config.js` running against the existing Vite dev server (`npm run dev`, `http://localhost:1420`, matching `tauri.conf.json`'s `devUrl`); a real committed spec file covering: the app launches and renders JARVIS branding with a live-mocked "Operational" System Health state; sending a chat message renders the mocked response in the conversation log. Wire `npx playwright test` into CI as a new `playwright` job (or a step within `frontend-build` - to be decided during implementation based on which keeps the workflow clearest), installing browsers via `npx playwright install --with-deps chromium` (Chromium only, not all three engines, since this is a Chromium-based webview product).

**Out of scope (explicitly deferred, not silently dropped):**

- Testing the actual Tauri-bundled webview (WebKit on Linux/macOS, WebView2 on Windows) - Playwright drives Chromium against the Vite dev server directly, the same mocked-IPC approach already used for this repository's prior ad hoc checks, not a full native-webview end-to-end test. A true native-webview E2E harness remains future scope.
- Release automation, checksums, signing, version synchronisation (EBG-0104, a separate WP this session).
- Any change to `src-tauri/src/lib.rs` or other application logic - this WP is CI/tooling and test-infrastructure only.

---

# 6. Authorised Files

- `.github/workflows/ci.yml`
- `package.json`, `package-lock.json` (new `@playwright/test` devDependency)
- `playwright.config.js` (new)
- A new test directory (e.g. `tests/e2e/`) and at least one real `.spec.js` file within it
- `src-tauri/build.rs`, `src-tauri/src/main.rs`, `src-tauri/src/lib.rs` (already-applied `cargo fmt` reformatting, no logic change)
- `.gitignore` (Playwright's own report/output directories, if not already covered)
- `src-tauri/Cargo.toml`/`Cargo.lock` (the `indexmap` `std`-feature-forcing fix, found during real Linux verification)
- `scripts/build_backend_sidecar.py` (the Windows-only `.exe`-suffix/permission-bit fix, found during real Linux verification)
- `src-tauri/tauri.conf.json` (`bundle.icon` array) and `src-tauri/icons/*` (the missing-PNG fix, found during real Linux verification)

No other files may be modified without a further approved package.

---

# 7. Implementation Requirements

1. The new Rust CI job's clippy and fmt checks shall be blocking from the start, since both are already genuinely clean on this codebase - no advisory grace period is warranted or requested.
2. `frontend-build`'s `continue-on-error` narrowing shall not silently widen scope elsewhere - only the `npm audit` step keeps it; the job's other steps become blocking.
3. The Playwright suite shall mock Tauri's IPC layer (`window.__TAURI_INTERNALS__.invoke`) rather than requiring a live backend or a bundled Tauri binary in CI - consistent with this repository's own prior ad hoc verification approach and appropriate for a CI environment with no display/webview stack.
4. The actual GitHub Actions run following this WP's commit is this EIP's real verification for the Rust CI job on Linux - if it fails on missing system dependencies or any other Linux-specific issue, that shall be fixed and re-verified via a further real CI run, not assumed correct from local Windows verification alone.

---

# 8. Explicit Exclusions

- No native-webview (WebKit/WebView2) end-to-end testing.
- No release automation, signing, or version-sync changes (EBG-0104).
- No change to application runtime logic.

---

# 9. Constraints

- Tauri's Linux build system-dependency list is asserted from Tauri's own published documentation, not independently re-derived - if incomplete or stale for the currently-pinned Tauri version, the first real CI run will surface this directly and it will be fixed as a genuine, disclosed fix-round finding, not silently worked around.
- `cargo test --manifest-path src-tauri/Cargo.toml` will report "0 tests" today (none exist) - this is expected and correct, not a defect; the check's purpose here is to assert the crate under the `#[cfg(test)]` configuration still compiles, catching future test-breaking changes.

---

# 10. Validation

- Local (Windows) `cargo build`/`clippy`/`fmt --check` confirmed clean ahead of this EIP (already performed).
- The real GitHub Actions run triggered by this WP's push - all jobs (`python`, `frontend-build`, `rust`, `playwright`) must show green (or the specific new gates must pass; pre-existing advisory items remain advisory) before this WP is considered verified. Checked via `gh run view` / `gh run list` against the real remote, not assumed.
- `npx playwright test` run locally against the real Vite dev server before commit, confirming both new spec assertions pass.
- `python -m pytest` and `python scripts/validate_repository.py` both run clean (neither should be affected by this WP, but checked per standing practice).

---

# 11. Risks and Dependencies

- **Linux system-dependency risk**: the single largest unknown in this WP - disclosed upfront, resolved by the real CI run rather than assumed.
- **No dependency on WP1 or WP3** - self-contained, though it does touch `src-tauri/` files WP1 also touched (now settled, no conflict).
- **Playwright browser download size/time in CI**: `npx playwright install --with-deps chromium` downloads a real browser binary on every CI run unless cached - acceptable for now, a future optimisation (dependency caching) is not this WP's scope.

---

# 12. Approval Request

Requesting Programme Sponsor approval to proceed with implementation as scoped above, following Engineering Reviewer review of this draft.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0103 (High, Candidate Backlog), closed by this package. |
| [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] | WP1, same session, touches overlapping `src-tauri/` files - sequenced after to avoid conflict. |
| [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] | Current accepted repository baseline this work builds on. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 July 2026 | Claude Engineering Implementer | Approved and implemented. Real Linux verification (WSL Ubuntu 26.04, at the Programme Sponsor's suggestion) found and fixed three genuine bugs before the CI job could even be written accurately: a schemars/indexmap std-feature incompatibility (`[build-dependencies]` fix), a Windows-only bug in `build_backend_sidecar.py` (`.exe`-suffix and lost-executable-bit), and a missing PNG icon (only a 32x32 `.ico` existed). All three fixed and re-verified with a full clean `cargo build`/`clippy -D warnings`/`fmt --check`/`test` on real Ubuntu. `.github/workflows/ci.yml` gained a `rust` job (with Tauri's Linux system dependencies and the sidecar-build step Tauri's own `generate_context!()` macro requires even for a plain `cargo build`) and a `playwright` job; `frontend-build`'s `continue-on-error` narrowed to only `npm audit`. `playwright.config.js` and `tests/e2e/app.spec.js` (new) - two real tests, both passing locally, covering app launch/system-health and a full send-message round-trip; two genuine test-writing mistakes (wrong CSS-class specificity, wrong mocked response shape) found and fixed via actually running the suite, not assumed correct. Closes EBG-0103. |
| 0.1 | 24 July 2026 | Claude Engineering Implementer | Initial draft, closing EBG-0103. Scoped to a new Rust CI job (build/clippy/fmt/test, blocking from the start since both are already clean locally), narrowing frontend-build's continue-on-error to only npm audit, and - per Programme Sponsor direction to expand this WP's scope - a genuine committed Playwright suite wired into CI, since the existing dependency had zero committed tests in this repository's history. |
