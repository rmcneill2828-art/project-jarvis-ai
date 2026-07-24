# EIP-ESR0032-001 - Guardian Desktop Distribution Foundation (EBG-0102)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0032-001 |
| Title | Guardian Desktop Distribution Foundation |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Engineering Session | ESR-0032 |
| Closes | EBG-0102 (Candidate Backlog, Critical) |

---

# 2. Purpose

Closes EBG-0102: package the Python backend as a real Tauri sidecar executable, enable Tauri bundling, and produce a genuine installable Windows artifact - the deployment blocker both external gap-analysis reviews (21 July 2026) and both AI reviewers independently ranked as the single largest constraint on Guardian actually being distributable, as distinct from architecturally complete.

---

# 3. Objective

Replace the current dev-mode-only backend spawn (`std::process::Command::new("python")`, requiring a full local Python/repository checkout - `src-tauri/src/lib.rs`'s own header comment already discloses this) with a bundled, standalone sidecar executable for release builds, enable `bundle.active`, and produce a real Windows installer via `npm run tauri build`. **Codex pre-implementation review finding (addressed):** this WP verifies the bundled sidecar path launches and can hold a basic conversation *on this development machine* - it does not itself establish "without any development toolchain present," since no clean-machine (no-toolchain) test is performed (Section 5/8). That broader claim remains for a future WP once a genuinely clean test environment is available.

---

# 4. Repository Context

- `src-tauri/tauri.conf.json`: `bundle.active` is currently `false`; no `externalBin` sidecar is configured. Verified directly.
- `src-tauri/src/lib.rs`: `spawn_backend()` calls `Command::new("python").args(["-m", "jarvis", "--ipc-stdio"])` unconditionally - this only works when Python and the repository checkout are present on the running machine, confirmed by the function's own header comment.
- `src-tauri/Cargo.toml`: no `tauri-plugin-shell` dependency exists yet. `package.json` has no `@tauri-apps/plugin-shell` either. Both must be added.
- No PyInstaller (or equivalent) dependency exists in `pyproject.toml` today - confirmed directly (`pip show pyinstaller` found nothing).
- Neither `makensis` (NSIS) nor `candle` (WiX) is present on this machine's `PATH` - confirmed directly. Tauri's bundler has historically been able to auto-fetch NSIS on first Windows build when missing; this must be verified live during implementation, not assumed.
- EBG-0050's own remaining scope already named this exact gap ("production sidecar bundling/packaging... still dev-mode `std::process::Command` only") and was promoted into this dedicated item (EBG-0102) at ESR-0031 WP4's closure follow-on.
- No prior EIP or session has touched Tauri bundling configuration; this is genuinely new ground for this repository.

---

# 5. Scope

**In scope:**

1. Package `jarvis/`'s existing `python -m jarvis --ipc-stdio` entry point as a standalone executable using PyInstaller (added as a new `pyproject.toml` dev dependency, disclosed).
2. Add `tauri-plugin-shell` (Cargo) and `@tauri-apps/plugin-shell` (npm) dependencies.
3. Configure `tauri.conf.json`'s `bundle.externalBin` to register the packaged executable as a sidecar, and grant the corresponding Tauri v2 shell-execute capability/permission for that specific sidecar only (not a general shell-execute grant).
4. Restructure `spawn_backend()` in `src-tauri/src/lib.rs` to branch on build type: `cfg!(debug_assertions)` (true for `tauri dev`) keeps the existing raw `std::process::Command` path unchanged, so day-to-day development is unaffected; a release build instead spawns the bundled sidecar via `tauri-plugin-shell`'s `Command::sidecar()` API.
5. Adapt the existing line-based reader/notification-dispatch logic (`run_reader()`, the pending-call map) to whichever I/O shape `tauri-plugin-shell`'s sidecar `Command` actually exposes (its spawned-process event stream, not a raw `std::process::Child` handle) - the exact adaptation is an implementation-time detail to resolve, not pre-specified here, but existing request/response and notification semantics (EIP-ESR0031-002) must be preserved for both code paths.
6. Enable `bundle.active = true`; set an explicit Windows target (`nsis`, the more commonly auto-available Tauri v2 default) rather than `"all"`.
7. Produce a real installer via `npm run tauri build` and install/run it (or at minimum run the produced executable directly) on this machine, confirming the packaged app launches and can complete a basic `send_message`/`platform_status` round-trip using the bundled sidecar, not the dev-mode Python spawn.

**Out of scope (explicitly deferred, not silently dropped):**

- Clean-machine (separate VM, no dev toolchain) acceptance testing - no such VM is available in this environment this session; disclosed as a real gap, not fabricated as tested. A future WP/session should perform this once a Sponsor-provided clean VM is available.
- Code signing, checksums, release manifest, tag-driven CI release pipeline - EBG-0104's own scope, a separate WP this session.
- CI building/testing the Rust/Tauri side at all - EBG-0103's own scope, a separate WP this session.
- Non-Windows targets (macOS/Linux bundling) - this repository and its development environment are Windows-only today; no cross-platform claim is made or tested.
- Upgrade/rollback/uninstall behaviour verification - a later Theme 1 concern (WP-D5-equivalent), not this foundation.

---

# 6. Authorised Files

- `pyproject.toml` (new PyInstaller dev dependency, a build/packaging script or `pyproject.toml` entry if PyInstaller needs a spec file)
- A new PyInstaller spec file or build script (exact path to be determined during implementation, e.g. `scripts/build_backend_sidecar.py` or `jarvis.spec`)
- `src-tauri/Cargo.toml` (new `tauri-plugin-shell` dependency)
- `package.json` (new `@tauri-apps/plugin-shell` dependency)
- `src-tauri/tauri.conf.json` (`bundle.active`, `bundle.targets`, `bundle.externalBin`, shell-execute capability/permission scoped to the sidecar)
- `src-tauri/src/lib.rs` (`spawn_backend()` restructuring, dev/release branch)
- `src-tauri/capabilities/*` (new or modified capability file granting the scoped sidecar-execute permission, per Tauri v2's permission model - exact filename to be confirmed during implementation)
- `jarvis/tests/test_stdio_rpc.py` and/or new Rust-side tests, if the restructuring introduces new testable units
- `.gitignore` (excluding PyInstaller's `build/`/`dist/` output directories and the compiled sidecar binary itself from version control, if not already covered)

No other files may be modified without a further approved package.

---

# 7. Implementation Requirements

1. The dev-mode (`cfg!(debug_assertions)` true) code path shall remain functionally unchanged from its current behaviour - `npm run tauri dev` must continue to work exactly as it does today, with no new build step required for ordinary development iteration.
2. The release-mode sidecar path shall preserve all existing request/response and notification semantics established by EIP-ESR0031-002 (JSON-RPC 2.0 envelope, `id`-key presence distinguishing response from notification, connection-level teardown on an unparsable line) - the I/O transport changes, the protocol handling does not.
3. The sidecar's granted Tauri v2 capability shall be scoped to executing that one named sidecar binary only, not a general shell-execute permission - preserving the CSP/capability-minimisation posture already established for this shell (locked-down CSP, `object-src 'none'`, `base-uri 'none'`).
4. The PyInstaller-packaged executable shall be built from the same `jarvis/` source the dev-mode path runs - no behavioural fork between the two beyond the packaging mechanism itself.
5. A real `npm run tauri build` shall be run and its output installer artifact actually installed or executed directly - "the config looks right" is not sufficient evidence; the packaged executable's own conversation round-trip must be observed running, per PBK-0001's Operational Verification Before Reporting.
6. **Codex pre-implementation review finding (addressed):** the dev/release branch is keyed on Cargo's build profile (`cfg!(debug_assertions)`), not on whether the sidecar binary happens to exist - a debug-profile packaged build (if one is ever produced) still takes the raw `python -m jarvis` path, and a release-profile run always takes the sidecar path regardless of whether a local Python install is also present. This coupling shall be stated in the restructured `spawn_backend()`'s own comments, not left implicit.
7. **Codex pre-implementation review finding (addressed):** the release-mode sidecar path shall provide equivalent best-effort process termination on app exit to the current `backend.child.kill()` behaviour - `tauri-plugin-shell`'s sidecar `CommandChild` exposes its own kill/termination mechanism, which the exit handler shall call for the sidecar path exactly as the existing handler does for the dev-mode `Child`.

---

# 8. Explicit Exclusions

- No clean-machine VM test is performed or claimed.
- No code signing is applied to the produced installer.
- No CI changes are made (EBG-0103's own scope).
- No release automation, checksums or version-sync tooling is added (EBG-0104's own scope).
- No non-Windows target is built or tested.

---

# 9. Constraints

- PyInstaller is not currently installed; its addition and first successful build are real, disclosed implementation risk, not assumed to work first try (native dependencies such as `psutil` sometimes need explicit PyInstaller hidden-import handling).
- Neither NSIS nor WiX is currently on this machine's `PATH`; Tauri's bundler's ability to auto-fetch NSIS must be verified live, not assumed - if it cannot, this constraint blocks installer generation entirely and must be reported honestly, not worked around by relaxing scope silently.
- `tauri-plugin-shell`'s sidecar `Command` API is event/callback-based, not a synchronous `std::process::Child` - adapting the existing reader-thread design will require genuine design work during implementation, not a mechanical find-replace.

---

# 10. Validation

- `cargo build` (dev profile) unchanged, confirming the debug-mode path compiles.
- `npm run tauri dev` live-smoke-tested exactly as in prior sessions, confirming zero regression to the development experience.
- `npm run tauri build` run for real, producing an actual installer artifact.
- The produced installer (or the built executable directly) run on this machine, with a real `send_message`/`platform_status` round-trip observed against the bundled sidecar - screenshots or equivalent direct observation, not inferred success.
- `python -m pytest` and `python scripts/validate_repository.py` both run clean.
- Any new Rust-side logic covered by tests where practical; PyInstaller packaging itself is not unit-testable and relies on the live build/run verification above.

---

# 11. Risks and Dependencies

- **Toolchain risk**: PyInstaller and NSIS/WiX availability are unconfirmed until actually exercised - this WP's own biggest technical unknown, disclosed upfront rather than discovered mid-implementation and then hidden.
- **Runtime environment risk (Codex pre-implementation review finding, addressed)**: the current dev-mode spawn deliberately sets `current_dir(repo_root)` so `python -m jarvis` can resolve source and any relative data/config paths against the repository checkout. A PyInstaller-packaged executable has no repository checkout around it at all - its working directory, bundled resource paths, and any config/database file paths `jarvis/` resolves relative to its own location or cwd must be re-verified against the packaged executable specifically, not assumed to behave identically to the dev-mode invocation. This is real implementation-time investigation, not a known-safe assumption.
- **Architectural risk**: adapting `run_reader()`'s synchronous line-based design to `tauri-plugin-shell`'s async event model is real design work with more than one reasonable approach; the EIP intentionally does not pre-decide the exact shape, leaving it to be resolved (and reviewed) during implementation.
- **Dependency**: EBG-0103 (CI) and EBG-0104 (release automation) are separate WPs this session but share this WP's territory (`tauri.conf.json`, `Cargo.toml`, `package.json`) - sequencing this WP first avoids the other two WPs touching files this one is actively restructuring.
- **No external dependency on EBG-0103/0104's own completion** - this WP is self-contained and can close independently.

---

# 12. Approval Request

Requesting Programme Sponsor approval to proceed with implementation as scoped above, following Engineering Reviewer review of this draft.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0102 (Critical, Candidate Backlog), closed by this package. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0050, whose remaining sidecar-packaging scope this item promoted and supersedes. |
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | Original UXP-backend bridge architecture this package extends for production packaging. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Operational Verification Before Reporting governs this package's validation approach. |
| [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] | Current accepted repository baseline this work builds on. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 July 2026 | Claude Engineering Implementer | Approved and implemented. `scripts/jarvis_backend_entry.py` and `scripts/build_backend_sidecar.py` (new) package the backend via PyInstaller; `spawn_backend()` restructured into a `BackendHandle` enum (`Dev`/`Sidecar`) branching on `cfg!(debug_assertions)`, sharing JSON-RPC dispatch logic via a new `dispatch_line()` function; `tauri-plugin-shell`/`@tauri-apps/plugin-shell` added; scoped `shell:allow-execute` capability; `bundle.active` enabled with `nsis` target. Live-verified: a real `npm run tauri build` produced an actual installer (NSIS auto-fetched live); the release executable's System Health panel populated with genuine sidecar-backed data; graceful exit confirmed zero orphaned processes (both the PyInstaller onefile bootloader and its child terminated); dev mode independently re-verified with zero regression (still spawns raw `python -m jarvis --ipc-stdio`). Closes EBG-0102. |
| 0.2 | 24 July 2026 | Claude Engineering Implementer | Pre-implementation fix round (Codex-caught, four non-blocking findings): tightened Section 3's "without any development toolchain present" overclaim to "verified on this machine"; disclosed the `cfg!(debug_assertions)` profile-coupling behaviour explicitly (Implementation Requirement 6); added an equivalent-sidecar-termination-on-exit requirement (Implementation Requirement 7); added the PyInstaller runtime-environment/cwd/data-path risk to Section 11. No blocking finding on the core approach (PyInstaller sidecar via tauri-plugin-shell, scoped capability, bundle.active, Windows nsis target, preserving EIP-ESR0031-002 semantics) - confirmed internally consistent with the current starting state. |
| 0.1 | 21 July 2026 | Claude Engineering Implementer | Initial draft, closing EBG-0102. Scoped to sidecar packaging (PyInstaller), tauri-plugin-shell wiring, bundle enablement and a real installer build/run - explicitly excluding clean-machine VM testing, code signing, CI and release-automation scope (EBG-0103/EBG-0104, separate WPs this session). |
