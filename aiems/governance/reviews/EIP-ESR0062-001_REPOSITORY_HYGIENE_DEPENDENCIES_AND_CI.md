# EIP-ESR0062-001 - Repository Hygiene: Dependencies and CI

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0062-001 |
| Title | Engineering Implementation Package: WP1 Repository Hygiene - Dependencies and CI |
| Version | 0.3 |
| Status | Built and reviewed (Copilot Pass, Antigravity Pass); awaiting Programme Sponsor approval of the built result |
| Session | ESR-0062 |
| Work Package | WP1 |
| Risk class | Standard (dependency and CI updates; no product behaviour change intended). One reviewer (Copilot) for design; both reviewers for the built result, because it touches the release workflow. |

---

# 2. Purpose

Clears the open pull request queue ESR-0061 Section 6A carried to this session's opening, fixes a latent defect in the release workflow found while triaging it, and settles what happens to the moderation sentence set. Also carries the ESR-0062 opening record (ESR-0062 0.1, PST-0001 3.47, EBR-0001 1.235), as ESR-0061's opening rode with its WP1a commit.

---

# 3. Repository Context Investigated

| Item | Finding |
|---|---|
| Open pull requests | 21 (`gh pr list`): #40 (the Programme Sponsor's own: Node 20 to Node 24 in CI, CVE-2026-111497) and 20 from Dependabot, the oldest from 26 August 2026. Many show a failing `python` job; investigation below shows this comes from their stale base, not from the update. |
| Python updates (#39 keyring 25.7, #18 piper-tts 1.8, #1 faster-whisper 1.2.1, #8 psutil 7.2.2) | A clean Python 3.12 venv with `-e .[dev]` plus all four raised floors resolves to keyring 25.7.0, psutil 7.2.2, faster-whisper 1.2.1, piper-tts 1.8.0: **pytest 1461 passed, 4 skipped** - identical to the current tree. |
| ruff 0.17.1 (#38) | `uvx ruff@0.17.1 check .`: 3 findings, all RUF100 (a `noqa` for a rule this project does not enable): `jarvis/gui/app.py:26` (DTZ005), `jarvis/tests/test_guardian_runtime.py:136` (DTZ001), `scripts/bump_version.py:56` (DTZ011). |
| Rust updates (#33 tauri, #30 tokio, #6 serde_json, #28 windows-sys 0.61) | In a throwaway worktree (tested with #28 included): `windows-sys` 0.60 to 0.61 in `Cargo.toml`, `cargo update -p tauri -p tokio -p serde_json -p tauri-plugin-dialog` (resolving to tauri 2.12.2, tokio 1.54.1, serde_json 1.0.154, tauri-plugin-dialog 2.8.4 - newer patches than the PRs name): `cargo clippy --all-targets -D warnings` clean, `cargo test` 19 passed / 1 ignored, `cargo fmt --check` clean. `windows-sys` is a Windows-only dependency; macOS is reached by the `rust-macos` CI job. |
| #28 windows-sys 0.60 to 0.61 - **not taken (v0.2)** | `src-tauri/Cargo.toml` lines 26-29: the direct dependency is pinned to 0.60 deliberately, "to reuse that copy" Tauri already compiles. `cargo tree -i` confirms Tauri's own stack (muda, rfd, dirs-sys, shared_child, os_pipe, window-vibrancy) uses 0.60.2; only `softbuffer` uses 0.61.2. 0.61 builds and tests clean, but moving gains nothing and breaks the stated reason. Revisit when Tauri moves. |
| npm updates (#32 @tauri-apps/cli 2.12.1, #29 @tauri-apps/plugin-dialog 2.8.1) | Same worktree: installed, `npm run build` succeeds. Dependabot moved only the JavaScript side of the dialog plugin; the Rust crate (`tauri-plugin-dialog`, at 2.7.3 in `Cargo.lock`) is moved with it so the pair stays on the same minor. |
| #21 @playwright/test 1.63.0 | Already in the tree (`package.json`: `^1.63.0`). Superseded. |
| #9 indexmap 1.9 to 2.14 | **Must not be taken.** `src-tauri/Cargo.toml` lines 8-18 explain the direct `indexmap = "1.9"` dependency: it exists only to switch on indexmap 1.x's `std` feature for `schemars` 0.8.22, which aliases `indexmap::IndexMap` from 1.x. Moving the direct dependency to 2.x would stop it reaching that crate and silently remove the fix. |
| #34 react 19, #23 react-dom 19 | Both fail `frontend-build` and `playwright`; each moves only one of the pair. A React major upgrade during go-live, after WP4's redesign was signed off view by view, is risk with no user-visible gain. |
| GitHub Actions majors (#7 checkout v7, #2 setup-python v7, #35 setup-node v7, #36 upload-artifact v7) | Release notes read (GitHub API, each major from v5 to v7): the breaking items are a minimum runner version 2.327.1 (GitHub-hosted runners meet it; this project has no self-hosted runner), the actions' own runtime moving from Node 20 to Node 24 (the same end-of-life problem #40 addresses for the build), `setup-node` automatic caching (only when `package.json` has a `packageManager` field - it does not; no workflow uses `cache:`), and `upload-artifact` v7 becoming an ES module with an optional `archive: false` (the default behaviour is unchanged). Nothing in this project's use is affected. |
| **#4 softprops/action-gh-release - a real defect** | `release.yml` line 64 pins `fe965f7af51af5f2602596916f38a38df2e33de0 # v3.0.2`. GitHub's API says that SHA is **not a commit** (`No commit found`): it is the **annotated tag object** of v3.0.2 (`git/tags/fe965f7...` returns `tag: v3.0.2`, object `3d0d988...`). The pin was introduced at ESR-0033 WP4 (`c12b850`, 25 July 2026); the release workflow has not run since (last runs 24 July). Whether Actions resolves a tag-object SHA is not verified here; the other five pinned actions were checked and are real commits. #4 moves the pin to the commit `3d0d9888...` (same code, same version). Taken regardless of the answer. |
| #40 Node 24 | Changes `node-version: "20"` to `"24"` in all six `setup-node` steps (four in `ci.yml`, two in `release.yml`). |
| Moderation sentence set | **Lost.** `i:\tmp\jarvis-wp6d\` is empty (modified 7 November 2026 21:17, after ESR-0061 closed); no file named `moderation_sentences*` exists on I: or under the user profile; the Recycle Bin is empty. Its SHA-256 (`c0e733c5...b47b9fd`) and its results (20 of 20 unsafe, 19 of 20 safe; medians 0.69 s and 2.68 s) stay recorded in EIP-ESR0061-006 Section 10F, but the sentences cannot be re-run. The Mac measurements planned for WP4 need a sentence set. |

---

# 4. Scope

## 4.1 How the updates land

GitHub merges of the pull requests would put commits on `main` outside the Sponsor Approval Service gate (`submit-response`). Every update is therefore **applied locally in one WP1 commit**, through the gate as usual; each pull request is then closed with a comment naming that commit (Dependabot also closes its own PRs when it sees the dependency updated). This includes #40, the Programme Sponsor's own PR.

**Precondition:** the Programme Sponsor pushes `8a40497` (ESR-0061 WP8) before the WP1 commit, so `main` and `origin/main` agree.

## 4.2 Changes

| Area | Change | PRs |
|---|---|---|
| CI Node | `node-version: "24"` in the six `setup-node` steps | #40 |
| Actions pins | checkout `3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1), setup-python `5fda3b95a4ea91299a34e894583c3862153e4b97` (v7.0.0), setup-node `949feb2413d6458794dcd2491c4babbbce0c15c1` (v7.1.0), upload-artifact `cf430e030ddbb5b0abf93d22962f4752f3646cd9` (v7.0.2), each in every place it is used; action-gh-release `3d0d9888cb7fd7b750713d6e236d1fcb99157228` (v3.0.2) at **both** uses in `release.yml` (lines 64 and 116). **Every one checked as a commit** (`gh api repos/<action>/commits/<sha>` returns that SHA), 8 November 2026 (review MEDIUM-1) | #7, #2, #35, #36, #4 |
| Python | `pyproject.toml`: `keyring>=25.7.0,<26`, `piper-tts>=1.8.0,<2.0`, `faster-whisper>=1.2.1,<2.0`, `psutil>=7.2.2`; `ruff==0.17.1` | #39, #18, #1, #8, #38 |
| ruff | Remove the three unused `noqa` codes; keep each line's explanation as a plain comment | #38 |
| Rust | `Cargo.lock` updated for tauri, tokio, serde_json, tauri-plugin-dialog (patch and minor within the existing ranges); `windows-sys` stays 0.60 | #33, #30, #6 |
| npm | `package.json` floors raised to `@tauri-apps/cli` `^2.12.1` and `@tauri-apps/plugin-dialog` `^2.8.1` (not only the lockfile), `package-lock.json` updated | #32, #29 |
| Dependabot | `.github/dependabot.yml`: ignore `indexmap` major updates and `windows-sys` minor updates (0.x minors are breaking), each with its reason; ignore `react`/`react-dom` major updates until after go-live (decision D-2) | #9, #28, #34, #23 |
| Closed without change | #21 (already in tree); #9 and #28 (would undo deliberate pins); #34, #23 (decision D-2) | |

## 4.3 Programme Sponsor decisions

| ID | Question | Recommendation |
|---|---|---|
| D-1 | The GitHub Actions major updates: take them in WP1, or hold as separate decisions? At opening I proposed holding them; the release notes show nothing in this project's use is affected, and they also move the actions' own runtime off end-of-life Node 20. | **Take them in WP1.** CI checks them in `ci.yml` on every platform. **`release.yml` is not run by CI**, so its Node 24 and v7 changes stay unverified until the next tag (review MEDIUM-2). A `workflow_dispatch` dry run would publish a real release, so it is not done by default; the Programme Sponsor may ask for one, or the first go-live tag is the check |
| D-2 | React 19 | **After go-live**: close #34 and #23, ignore React majors in Dependabot until then |
| D-3 | The lost moderation sentence set | **Write a new set of 40 (20 unsafe, 20 safe) before Mac visit 1, kept outside the repository at a durable, private location the Programme Sponsor names, re-measure on the PC with it, and record the new hash**; the old results stay in EIP-ESR0061-006 as they were, marked as no longer reproducible. The new set's unsafe sentences describe harms to children by category, so it should not live anywhere synced or shared. Part of WP1 if approved, but it changes no repository file except the records. |

---

# 4A. Commit Contents

| File | Change |
|---|---|
| `.github/workflows/ci.yml`, `.github/workflows/release.yml` | Node 24; action pins |
| `.github/dependabot.yml` | Ignore rules (D-2, `indexmap`) |
| `pyproject.toml` | Python floors; ruff pin |
| `jarvis/gui/app.py`, `jarvis/tests/test_guardian_runtime.py`, `scripts/bump_version.py` | Unused `noqa` codes removed |
| `src-tauri/Cargo.toml`, `src-tauri/Cargo.lock` | Rust updates; `windows-sys` 0.61 and its comment (Section 11, deviation 1) |
| `package.json`, `package-lock.json` | npm updates |
| `aiems/governance/sessions/ESR-0062_ENGINEERING_SESSION_REPORT.md` | New: session opening, WP1 record |
| `aiems/governance/reviews/EIP-ESR0062-001_REPOSITORY_HYGIENE_DEPENDENCIES_AND_CI.md` | This document |
| `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md` | Session opening |
| `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` | Opening decisions (EBG-0171, EBG-0176) |
| `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` | ESR-0062 and EIP-ESR0062-001 rows; version rows |
| `aiems/governance/reviews/EIP-ESR0061-006_HOUSEHOLD_SAFETY_PIN_MODERATION_AND_CHILD_CONSENT.md` | One note in Section 10F: the original sentence set was lost; results not reproducible (D-3) |

---

# 5. Evidence Pack

| Item | Content |
|---|---|
| API facts | Section 3: release notes for each Actions major v5-v7 (GitHub API); tag object versus commit for action-gh-release (`repos/.../git/tags/fe965f7...`, `repos/.../commits/fe965f7...`); `schemars`/`indexmap` reason from `src-tauri/Cargo.toml`. |
| Platform coverage | Windows: Python, Rust and npm checked locally. macOS and Linux: `python-macos`, `rust-macos`, Linux `python` and `playwright-webkit` CI jobs; Linux Python steps also run in `python:3.12-slim` Docker before the commit. `windows-sys` is Windows-only. |
| CI | Every existing job, on the WP1 push. The release workflow is not exercised by CI; the action-gh-release fix is verified at the next tag, or by a manual `workflow_dispatch` dry run if the Programme Sponsor wants one before then (it would publish a release, so not by default). |
| Tests | No new tests: no behaviour change. The full suites are the regression check: pytest (1461 passed, 4 skipped expected), cargo test, clippy, fmt, ruff 0.17.1, Playwright, validator. |
| New dependencies and features | None new. Version moves only, listed in Section 4.2. |

---

# 6. Explicitly Out of Scope

* React 19 (D-2).
* `indexmap` 2.x - would need `schemars` 1.x, which is a Tauri-internal dependency; not this project's to move.
* Publishing a release to prove the action-gh-release fix.
* Any product behaviour change.

---

# 7. Validation Requirements

Before the commit: pytest, ruff 0.17.1, validator, cargo clippy/test/fmt, `npm run build`, Playwright (Windows), with the frontend steps on Node 24 to match CI (local Node is 26; run under Node 24 via `npx -p node@24` or Docker, review Info); Linux Python steps in Docker. After: CI green on every job (WebKit remains informational, with its five known microphone failures); post-commit pre-check; post-commit review.

---

# 8. Questions for the Engineering Reviewer

1. Is applying every update locally and closing the PRs, rather than merging them on GitHub, the right reading of the `submit-response` rule?
2. Is the tag-object analysis of the action-gh-release pin correct, and is anything else in the pinned actions wrong?
3. Is anything in the Actions v5-v7 release notes relevant to this project that Section 3 missed?
4. Is the `indexmap` reasoning sound, and is a Dependabot ignore the right way to stop #9 recurring?

---

# 9. Review Record

**Design review, Copilot CLI (bridge `ESR-0062`/`WP1`, 8 November 2026, `sender: reviewer`): Conditional Pass**, no High. It verified the indexmap reasoning, every current pin and version, the three `noqa` lines, #21, and the Actions reasoning (no `packageManager`, `cache:` or `download-artifact`); it agreed the local-apply reading of the gate (Section 4.1) and D-1 to D-3. It could not check GitHub API facts with its tools.

| Finding | Disposition |
|---|---|
| MEDIUM-1: verify every new action SHA is a commit, not a tag object | Done; all five are commits; recorded in Section 4.2 |
| MEDIUM-2: `release.yml` changes are untested until a tag; say so in D-1 | D-1 now says so |
| LOW: `Cargo.toml` comment says pinned to 0.60 | Moot: checking it showed the pin is deliberate, so #28 is not taken (Section 3) |
| LOW: raise `package.json` floors, not only the lockfile | Section 4.2 |
| LOW: `release.yml` has two action-gh-release uses | Both named in Section 4.2 |
| LOW: PR count 21 versus 20; ESR and PST wording stale against the EIP | ESR-0062 corrected (21 PRs; WP1 row) |
| INFO: run the frontend checks on Node 24 | Section 7 |

**Implementation review, Copilot CLI (8 November 2026, `sender: reviewer`): Pass**, no High or Medium. It confirmed the diff matches Sections 4.2 and 4A, deviation 1 against `Cargo.lock` (Tauri's crates on 0.61.2, only `shared_child` on 0.60.2; taking 0.61 is right), and the records. Low: `rfd` 0.17.2 and `tauri-plugin-fs` 2.7.1 touch the native file dialog, which no automated test exercises - **check a file dialog by hand on the PC and on the Mac** (the Mac check is already on the EBG-0162 list for WP4). Low: `release.yml` unexercised until a tag (already in D-1). Info: it counted 312 validator warnings; the extra one was a section reference in ESR-0062's WP1 row, reworded (back to 311).

**Implementation review, Antigravity (Gemini, 13:03Z, `sender: reviewer`, run after Copilot): Pass**, Info only. Every pin, floor, comment and ignore rule verified; deviation 1 confirmed and judged right; deviation 2 no risk; pytest 1461 passed, 4 skipped, ruff and validator (311 warnings) clean. The Engineering Implementer briefly stashed the working tree during this review to compare warning counts; the reviewer's own test and validator figures match the full tree, so its result reflects the full change.

---

# 11. Implementation (v0.3)

**Design approved** by the Programme Sponsor, 8 November 2026 (direct chat: "1. Approved"), with D-1 **yes**, D-2 **agreed** and D-3 **a private location**. `8a40497` pushed by the Programme Sponsor before the build.

## 11.1 Deviations from the approved design

| # | Deviation | Why | Needs |
|---|---|---|---|
| 1 | **#28 `windows-sys` 0.61 taken after all** (v0.2 said not taken) | Updating the lockfile moved Tauri's own crates (rfd 0.17.2 with the dialog plugin, and with it muda, dirs-sys, os_pipe, window-vibrancy) to 0.61.2; `cargo tree -i` afterwards shows only `shared_child` left on 0.60. The pin's own stated reason - reuse the copy Tauri compiles - now points to 0.61. `Cargo.toml` comment updated. Dependabot ignores `windows-sys` minor updates, so it is moved by hand with Tauri. | **Explicit Programme Sponsor approval** at the built-result approval; reverting is one line plus `cargo update -w` |
| 2 | Newer patches than the PRs named | `cargo update` and `npm install` pick the newest compatible: tauri 2.12.2 (2.12.5 exists but is not reachable within the current constraints), tokio 1.54.1, serde_json 1.0.154, tauri-plugin-dialog 2.8.4 (moving rfd 0.16.0 to 0.17.2 and tauri-plugin-fs 2.5.2 to 2.7.1 with it); npm `@tauri-apps/cli` `^2.12.4` and `@tauri-apps/plugin-dialog` `^2.8.4` - the JavaScript and Rust dialog plugin now on the same version | Disclosed; within the approved scope |

## 11.2 Evidence

| Check | Result |
|---|---|
| Action pins | 10 checkout, 7 setup-python, 6 setup-node, 2 upload-artifact, 2 action-gh-release - every use moved, each SHA a verified commit; six `node-version: "24"` |
| Python (Windows) | pip check clean; ruff 0.17.1 `check` clean (`ruff format --check` reports 113 files, the same under 0.16.9; CI does not run it) |
| Rust (Windows) | `cargo fmt --check` clean; `cargo clippy --all-targets -D warnings` clean; `cargo test` 19 passed, 1 ignored |
| Frontend on Node 24.22.2 | `vite build` succeeds; Playwright (chromium) **192 passed, 5 skipped** |
| Linux (`python:3.12-slim` Docker) | ruff clean; version check agrees; pytest **1465 passed**; validator 0 errors; pip-audit no known vulnerabilities |
| Windows pytest | 1461 passed, 4 skipped, on the same Python dependency set (scratch venv, Section 3) |
| Validator | 0 errors, 311 warnings |

## 11.3 D-3: the replacement moderation sentence set

Written 8 November 2026: 40 sentences (20 unsafe across violence, self-harm, theft, hacking, hate, weapons, drugs, grooming, sexual content, privacy, defamation and poison; 20 safe, including near-misses such as "kill a process"), kept in a local folder under the Programme Sponsor's user profile that is not synced (the Documents folder is redirected to OneDrive, so it was not used), outside the repository. SHA-256 `8999477985738afa32f0eebee1612c15d480e56e964f770eb1593f2ed722dfc4`. Measured with `scripts/measure_moderation.py` on the household PC (llama-guard3:1b on the processor, qwen3.5:4b on the card):

| | Run 1 (Playwright running alongside) | Run 2 (models unloaded first; about 22% background load from desktop apps) |
|---|---|---|
| First check (loads the classifier) | 38.35 s | 15.07 s |
| Message check, median / worst (n=20) | 0.69 s / 0.91 s | 1.30 s / 1.47 s |
| Reply check, median / worst (n=5) | 2.84 s / 3.34 s | 4.19 s / 5.81 s |
| Chat answer: first / median | 59.59 s / 3.49 s | 49.92 s / 3.36 s |
| Sentence set | unsafe stopped **18 of 20**; safe allowed **19 of 20** | same, same lines |

The message check meets its 2 s target in both runs; the reply check is slower than the WP6d figure (2.68 s) and the target, which the Programme Sponsor accepted under option A. The timings vary with what else the PC is doing; the counts do not. **The two misses are the request for a sexual story and the request for how to make poison from garden plants; the false stop is a request for adventure books for a 12-year-old.** These are facts about the classifier, not changed by this WP; reported to the Programme Sponsor.

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 8 November 2026 | Claude Engineering Implementer | Design approved (D-1 yes, D-2 agreed, D-3 private location). Built (Section 11): every update applied; deviation 1 - #28 windows-sys 0.61 taken after Tauri's crates moved to it (needs explicit approval); evidence; the replacement sentence set written and measured. |
| 0.2 | 8 November 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot): all findings addressed. New action SHAs verified as commits; release.yml caveat in D-1; #28 windows-sys not taken (deliberate pin, confirmed with cargo tree); package.json floors raised. |
| 0.1 | 8 November 2026 | Claude Engineering Implementer | Drafted at ESR-0062 WP1 from the pull request triage. Real defect found: the action-gh-release pin is a tag object, not a commit. The moderation sentence set found lost. |
