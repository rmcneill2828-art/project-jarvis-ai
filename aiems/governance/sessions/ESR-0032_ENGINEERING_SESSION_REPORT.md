# ESR-0032 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0032 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0032 |
| Date Opened | 21 July 2026 |
| Date Closed | 24 July 2026 |
| Closure Status | Closed - WP0-WP3 complete, session-wide WP4 Pass, WP5 Accept (RBL-0019 established) |

---

# 2. Purpose

This report records the opening and execution of ESR-0032, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0031, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service (ADR-0022) with no manual relay anywhere - the seventh consecutive session run this way. Unlike ESR-0031's process/product pairing, this session pursued a single theme, **Theme 1 - Deployment Alpha**, in full: all three of its items (EBG-0102, EBG-0103, EBG-0104) in one session, per the Programme Sponsor's own explicit choice at WP0B to pursue the entire theme rather than a smaller slice. This is the first session in this project's history to make the product genuinely distributable, CI-gated, and releasable end to end - proven via a real installed Windows package, a real green GitHub Actions run across all four CI jobs, and a real published `v0.1.0` GitHub Release.

---

# 3. Scope

ESR-0032 opened with WP0/WP0B: the Programme Sponsor selected Theme 1 - Deployment Alpha from EBR-0001 Section 5A's active-backlog snapshot, choosing to pursue all three items (EBG-0102, EBG-0103, EBG-0104) in this session rather than a smaller MVP slice or a CI-first ordering - an explicit sizing/risk decision presented via `AskUserQuestion` and confirmed by the Programme Sponsor.

**WP1** (EBG-0102, Guardian Desktop Distribution Foundation) packaged the Python backend as a standalone PyInstaller sidecar spawned via `tauri-plugin-shell`, producing a real Windows installer, live-verified with zero regression to dev mode.

**WP2** (EBG-0103, CI Build Gate Hardening) added real Rust and Playwright CI jobs and tightened `frontend-build`'s advisory `npm audit` into a genuine hard gate. Real Linux (WSL Ubuntu) verification, performed before writing the CI job rather than trusting a first real run alone, found and fixed three genuine cross-platform bugs. A further fix round then resolved a real, pre-existing ruff-version-drift CI failure discovered only by checking the actual GitHub Actions run after the push - itself a direct product of this WP's own purpose, a CI gate that is actually checked and trusted.

**WP3** (EBG-0104, Release Automation and Version Synchronisation) added a single-source-of-truth `VERSION` file, a cross-file version-sync tool, a blocking CI version-equality gate, and a tag-triggered release workflow - live-verified via a real `v0.1.0` tag push (this repository's first-ever public GitHub Release), which found and fixed a genuine `GITHUB_TOKEN` permissions gap that no amount of structural review would have surfaced.

Session-wide WP4 (Independent Repository Verification) and WP5 (Repository Baseline Acceptance) closed the session: WP4 reached Pass, Codex independently confirming the exact diff-stat figures and that no `sentinel/` trust-boundary or Sponsor Approval Service token-handling behaviour changed beyond mechanical fixes; WP5 established a new baseline, [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]], superseding RBL-0018 - both independent views agreeing this session delivered a genuinely distributable, tested, and releasable product for the first time.

---

# 4. Engineering Authority

ESR-0032 opening was authorised by Programme Sponsor instruction on 21 July 2026, following repository synchronisation confirming [[ESR-0031_ENGINEERING_SESSION_REPORT|ESR-0031]] was closed and [[RBL-0018_REPOSITORY_BASELINE|RBL-0018]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

One theme, three items, selected by the Programme Sponsor at WP0B via `AskUserQuestion` from EBR-0001 Section 5A's active-backlog snapshot:

- **WP1** - Guardian Desktop Distribution Foundation (EBG-0102): sidecar packaging, Tauri bundling, a real installer.
- **WP2** - CI Build Gate Hardening (EBG-0103): a real Rust CI job, a real Playwright acceptance suite, a genuinely trustworthy `frontend-build` gate.
- **WP3** - Release Automation and Version Synchronisation (EBG-0104): a single version source of truth, a blocking CI drift check, a real tag-triggered release pipeline.

The Programme Sponsor explicitly chose to pursue all three items in one session ("Everything in Theme 1 this session") over a smaller MVP slice or CI-first ordering, accepting the larger scope/risk tradeoff that choice was flagged as carrying. All three were met by closure.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0/WP0B | Repository synchronisation; session objective selection (Theme 1 - Deployment Alpha, all three items) | Complete - Section 7 |
| WP1 | Guardian Desktop Distribution Foundation implementation per EIP-ESR0032-001 | Complete - Section 8 |
| WP2 | CI Build Gate Hardening implementation per EIP-ESR0032-002, plus a fix round for a real GitHub Actions ruff-drift failure | Complete - Section 9 |
| WP3 | Release Automation and Version Synchronisation implementation per EIP-ESR0032-003, plus a fix round for a real release-permissions bug | Complete - Section 10 |
| Session-wide WP4/WP5 | Independent Repository Verification; Repository Baseline Acceptance (RBL-0019 established) | Complete - Section 11/12 |

---

# 7. WP0/WP0B - Session Initialisation Record

- Repository state verified directly against `origin/main`, confirming ESR-0031 formally closed and RBL-0018 the accepted baseline at session open.
- Session objective selection presented via `AskUserQuestion`: the Programme Sponsor selected Theme 1 - Deployment Alpha, then explicitly chose to pursue all three of its items (EBG-0102, EBG-0103, EBG-0104) in this session rather than a smaller slice - a sizing/risk decision surfaced explicitly, not silently assumed.
- Draft [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] registered for WP1.
- Commit SHA: `b506764`.

---

# 8. WP1 - Guardian Desktop Distribution Foundation (EBG-0102)

Implements [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] v1.0 (Approved-implemented).

**A pre-implementation fix round** addressed four Codex non-blocking findings on the draft: a distributability overclaim in the EIP's own wording, disclosure of the `cfg!(debug_assertions)` build-profile coupling behaviour, an added requirement that release-mode exit cleanly terminate the sidecar's full process tree, and disclosure of a PyInstaller runtime-environment/cwd/data-path risk.

**Delivered**: `scripts/jarvis_backend_entry.py` (new) - a headless stdio-RPC-only entry point, deliberately separate from `jarvis.app.main()` to avoid bundling Tkinter (which `jarvis.app` imports unconditionally for the legacy First Light GUI) into a backend that never needs it. `scripts/build_backend_sidecar.py` (new) - packages that entry point via PyInstaller into Tauri's `externalBin` sidecar naming convention, target triple auto-detected via `rustc -vV`. `src-tauri/src/lib.rs`'s `spawn_backend()` now branches on `cfg!(debug_assertions)`: dev builds keep the original `Command::new("python")` path, release builds spawn the packaged sidecar via `tauri-plugin-shell`'s async `Command::sidecar()` API. A new `BackendHandle` enum (`Dev`/`Sidecar`) and a shared `dispatch_line()` function let both paths reuse identical JSON-RPC dispatch logic. `src-tauri/capabilities/default.json` grants `shell:allow-execute` scoped to exactly one named sidecar, not a general shell-execute permission.

**Live-verified end to end, not assumed**: a real `npm run tauri build` produced an actual installer (`JARVIS Guardian Shell_0.1.0_x64-setup.exe`) - Tauri auto-fetched NSIS live. The release executable was run directly: the System Health panel populated with genuine live sidecar-backed data; process inspection confirmed the sidecar's PyInstaller onefile bootloader+child pair both genuinely running; graceful app close triggered `BackendHandle::kill()`, and process inspection afterward confirmed zero orphaned processes. Dev mode was independently re-verified live afterward with zero regression.

**A post-implementation fix round (Codex-caught)** corrected EBG-0102's own EBR-0001 entry, which cited a stale pre-fix-round EIP version.

- Commit SHAs: `3299ef3` (pre-implementation fix round), `293780a` (implementation), `a938e53` (post-implementation fix round)
- `python -m pytest`: 351 passed. `python scripts/validate_repository.py`: 0 errors, clean.

---

# 9. WP2 - CI Build Gate Hardening (EBG-0103)

Implements [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]] v1.0 (Approved-implemented).

**Real Linux verification, not assumed**: at the Programme Sponsor's suggestion, a previously-unused WSL Ubuntu 26.04 install on this machine was used to actually run the planned CI checks locally before writing the workflow. This found and fixed three genuine bugs: (1) `schemars` 0.8.22 (pulled in transitively for Linux/dbus capability-schema generation, a code path Windows never exercises) requests `indexmap`'s `serde-1` feature but never `std`, and `indexmap` 1.9.x has no default features at all - fixed by forcing `indexmap`'s `std` feature via an explicit `[build-dependencies]` entry; (2) `scripts/build_backend_sidecar.py` was Windows-only (hardcoded `.exe` suffix, and `shutil.copyfile` silently drops the executable permission bit) - fixed with target-triple branching and `shutil.copy`; (3) only a single 32x32 `.ico` existed for the app icon, and Tauri's `generate_context!()` macro fails outright without a PNG present on any platform - the full icon set regenerated via `npx tauri icon`.

**Delivered**: `.github/workflows/ci.yml` gained a `rust` job (`cargo build`/`clippy -D warnings`/`fmt --check`/`test`, all blocking from introduction) and a `playwright` job; `frontend-build`'s `continue-on-error` narrowed from job-level to only its `npm audit` step. `playwright.config.js` and `tests/e2e/app.spec.js` (new, scope expanded per Programme Sponsor direction after confirming Playwright was already used on other of the Programme Sponsor's projects) - two real committed tests mocking Tauri's IPC layer via `page.addInitScript`. Two genuine test-writing mistakes (a CSS-class selector matching both user and Guardian messages; a mocked response returning a bare string when the app expects `{message, provider}`) were found and fixed by actually running the suite.

**A further fix round was required after checking the real GitHub Actions run**, not assumed green from local WSL verification alone: the `python` job failed on `ruff check .` despite everything passing locally - local `ruff` was cached at an older version while CI's unpinned install always fetches latest, which had drifted and enabled several new default rules, surfacing 87 pre-existing violations across the repository, none introduced by this session. 70 auto-fixed mechanically; 17 hand-fixed, including justified `# noqa` comments on deliberate broad-exception catches and the Ollama provider's established `RuntimeError` contract (changing it to `TypeError` would have broken existing tests - a judgment call to preserve behaviour over blindly satisfying a lint rule). `frontend-build`'s `npm audit` was also tightened from advisory to a real `--omit=dev` hard gate, having confirmed the only two findings (vite/esbuild) are dev-only build tooling never shipped in the app.

**A separate governance-process deviation occurred and was self-caught** during this WP's closure: a documentation backfill commit was made directly via `git commit` without first going through `submit-to-review`, breaking standing review discipline. Caught before starting WP3 and retroactively submitted through the full review/approval cycle rather than left uncorrected (Section 14).

- Commit SHAs: `39907a7` (draft EIP), `fc64b84` (implementation), `77c15a8` (ruff/audit fix round), `a04005d` (post-closure documentation backfill)
- `python -m pytest`: 359 passed (was 351 at ESR-0031's closure). Real GitHub Actions CI: all four jobs (`python`, `rust`, `playwright`, `frontend-build`) green on the fix-round commit.

---

# 10. WP3 - Release Automation and Version Synchronisation (EBG-0104)

Implements [[EIP-ESR0032-003_RELEASE_VERSION_SYNCHRONISATION|EIP-ESR0032-003]] v1.0 (Approved-implemented).

**A design decision was surfaced explicitly rather than silently assumed**: the draft EIP proposed a repo-root `VERSION` file as the single authoritative version source, deliberately not designating any of the four existing build files as primary since each is a tool-specific manifest (Python packaging, npm, Cargo, Tauri config) with unrelated fields of its own - Codex's design review agreed this avoids an arbitrary tool preference. The draft also explicitly declined to authorise pushing a real release tag as its own scope, deferring that decision to the Programme Sponsor, who then explicitly authorised it.

**Delivered**: `VERSION` (new) as the single source of truth. `scripts/sync_product_version.py` (new) propagates it into `pyproject.toml`/`package.json`/`src-tauri/Cargo.toml`/`src-tauri/tauri.conf.json` in one command, refusing to guess on an unparseable/missing field or a no-op version - 8 new tests. `python scripts/sync_product_version.py --check` wired into `ci.yml` as a blocking gate. `.github/workflows/release.yml` (new) triggers only on `v*` tag pushes, verifies the tag matches `VERSION`, builds the real installer, locates the exact NSIS artifact (failing on zero or multiple matches, never a broad glob), computes its SHA-256 checksum, and publishes both via `softprops/action-gh-release` pinned to the immutable `v3.0.2` tag (confirmed via the GitHub API, not guessed).

**Live-verified end to end, not merely structurally reviewed**: at the Programme Sponsor's explicit authorisation, a real `v0.1.0` tag was pushed - this repository's first-ever public GitHub Release. The first attempt built the installer and computed its checksum successfully but failed to publish (`softprops/action-gh-release`: "Resource not accessible by integration") because this repository's default `GITHUB_TOKEN` workflow permission is read-only, a genuine bug no amount of structural review would have surfaced. Fixed with a job-level `permissions: contents: write` block, the tag moved to the fixed commit and re-pushed, and the second run passed every step - `gh release view v0.1.0` confirms a real, non-draft, non-prerelease release with the installer and its `.sha256` checksum attached.

- Commit SHAs: `d57e602` (draft EIP), `bfee19a` (implementation), `42c7e82` (permissions fix round), `4ec539b` (governance closure)
- `python -m pytest`: 359 passed. `npx playwright test`: 2 passed. Real GitHub Actions CI: all four jobs green. Real GitHub Release published at `v0.1.0`.

---

# 11. Session-Wide WP4 - Independent Repository Verification

**Handover preparation**: an [[ESR-0032_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0032 WP4 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session's content range (`077f31b`..`4ec539b`) across WP0B/WP1/WP2/WP3.

**Pass, both independent views converging, no fix round required**: Codex independently confirmed `git diff --stat 077f31b..4ec539b` matches the handover's claimed 70 files/1,788 insertions/191 deletions exactly, that the file-list/working-set characterisation is accurate and complete with no extra file found outside the described scope, and - directly checking rather than trusting the claim - that `sentinel/` trust-boundary diffs and Sponsor Approval Service/bridge token-handling diffs are both mechanical only (import modernisation, justified `noqa` comments, explicit `check=False`), with no behavioural change in either. Codex's own recurring CLI sandbox crash prevented it from independently re-confirming the live GitHub Release via `gh` in its own environment - disclosed as a limitation, not treated as a blocking gap, since the Engineering Implementer's own `gh release view v0.1.0` output stands as that specific evidence.

- Commit SHAs: `d7226e1` (handover draft), `721fc06` (verification result recorded)
- `python scripts/validate_repository.py` (full mode): 0 errors, 149 warnings at the time of this WP.

---

# 12. Session-Wide WP5 - Repository Baseline Acceptance (RBL-0019 Established)

**Both independent WP4 views recommended a new baseline** rather than retaining RBL-0018: this session delivered three genuine, live-verified capabilities that materially change what the product can do and how trustworthy its own delivery pipeline is - a real installable Windows package (WP1), a CI pipeline that actually builds/tests/gates the complete desktop product (WP2), and a real, live-published first GitHub Release with automated cross-file version synchronisation (WP3). The Programme Sponsor's determination: **establish a new baseline** - [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]].

**Codex reviewed RBL-0019's own content** against the real session diff and its own WP4 findings, confirming the baseline document accurately describes what was actually delivered, and confirmed REG-0001's new row and PST-0001's Current Repository Baseline/Mode/Phase/Objective updates are internally consistent - Pass, no blocking findings, no fix round required.

- Commit SHA: `8f90b96` (WP5 closure, RBL-0019 accepted)
- `python -m pytest`: 359 passed throughout. `python scripts/validate_repository.py` (full mode): 0 errors, 149 warnings (stable). Real GitHub Actions CI: all four jobs green on the closing commit.

---

# 13. Governance Process Note - Self-Caught Deviation

During WP2's closure, a documentation-backfill commit (`a04005d`) was made directly via `git commit` without first going through `submit-to-review` - a breach of the standing practice that every commit passes through the real Sponsor Approval Service gate. This was caught by the Engineering Implementer before WP3 began, not flagged externally, and was retroactively submitted through the full review/approval cycle rather than left as an unremediated gap. Codex's own review of the retroactive submission noted the process deviation explicitly as a finding while confirming the content itself was accurate.

Separately, this session experienced a recurring, real environment issue: Codex's own `codex exec` CLI sandbox crashed (`windows sandbox: helper_unknown_error: setup refresh had errors`) repeatedly, consistently right after completing a genuine review and attempting to call `return-findings` itself. Each time, Codex's own verbatim, already-formed findings text was submitted on its behalf by the Engineering Implementer, with explicit Programme Sponsor approval obtained before the first instance and the same approved pattern applied consistently thereafter. This is a real, disclosed limitation of this session's tooling, not yet backlogged as its own item.

Five Version History entries (three in REG-0001, one each in EBR-0001 and PST-0001) were also found misattributed to `scripts/bump_version.py`'s default author ("Claude Engineering Reviewer") instead of the role actually performing the bumps ("Claude Engineering Implementer"), after two calls omitted the explicit `--author` flag. Caught and corrected before WP3's closure commit.

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0032-001_GUARDIAN_DESKTOP_DISTRIBUTION_FOUNDATION|EIP-ESR0032-001]] | Approved-implemented package for WP1, v1.0. |
| [[EIP-ESR0032-002_CI_BUILD_GATE_HARDENING|EIP-ESR0032-002]] | Approved-implemented package for WP2, v1.0. |
| [[EIP-ESR0032-003_RELEASE_VERSION_SYNCHRONISATION|EIP-ESR0032-003]] | Approved-implemented package for WP3, v1.0. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0102, EBG-0103, EBG-0104 all Complete. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0032_WP4_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0032 WP4 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, Section 10/11. |
| [[ESR-0031_ENGINEERING_SESSION_REPORT|ESR-0031]] | Prior closed session this one continues from. |
| [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] | New repository baseline established at Section 12, superseding RBL-0018. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0/WP0B (Theme 1 - Deployment Alpha selected in full), WP1 (Guardian Desktop Distribution Foundation, real installer live-verified with zero orphaned processes), WP2 (CI Build Gate Hardening, real Linux verification finding three genuine bugs, plus a fix round for a real GitHub Actions ruff-drift failure), WP3 (Release Automation and Version Synchronisation, live-verified via a real v0.1.0 GitHub Release, plus a fix round for a real GITHUB_TOKEN permissions bug), and the session-wide WP4 Independent Repository Verification (Pass, no fix round) and WP5 Repository Baseline Acceptance (RBL-0019 established, no fix round). Also records a self-caught governance-process deviation, Codex's recurring CLI sandbox crashes, and a self-corrected author-attribution mistake (Section 13). Seventh session run entirely through the AIEMS Exchange Bridge and the deployed Sponsor Approval Service with no manual relay. Status Open to Closed. |
