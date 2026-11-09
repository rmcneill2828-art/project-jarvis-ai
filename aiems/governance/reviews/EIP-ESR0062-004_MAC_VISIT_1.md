# EIP-ESR0062-004 - Mac Visit 1: Plan and Checklist

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0062-004 |
| Title | Engineering Implementation Package: WP4 Mac Visit 1 - Preparation, On-Visit Checks and Measurements on the Household Mac |
| Version | 0.3 |
| Status | Design approved; P1 (version 0.2.0) built; awaiting Programme Sponsor approval, then the v0.2.0 release (P2) |
| Session | ESR-0062 |
| Work Package | WP4 |
| Risk class | Standard (a verification visit; the only code change is a version number). Copilot for design; the results are recorded, and any defect found becomes its own backlog item and Work Package. |

---

# 2. Purpose

Everything macOS-specific in JARVIS has so far been proven only on GitHub's macOS runners. Mac visit 1, about **21 November 2026**, is the first time it runs on the household Mac, the computer of the household's Child-role user. This plan says what must be ready before the visit, what is checked and measured there, in what order, how each result is decided and recorded, and what is cleaned up afterwards, so the visit is done once and done fully.

It closes or advances:

* **EBG-0162** (macOS platform support): the real-Mac checks ESR-0061 carried (process-group stop, `_MEI` clean-up, `.dmg` and Gatekeeper, microphone, Keychain, file dialog, WKWebView, GIA names). Completed if they pass.
* **EBG-0167** (voice provisioning): download, speaking and the microphone in WKWebView. Completed if they pass.
* The **measurements** ESR-0061 carried: chat model and classifier latency and memory (EIP-ESR0061-003; EIP-ESR0061-006 M1's targets), the Orb's processor use (EIP-ESR0061-004 W3), plus voice timings (new with WP3).
* The two **manual checks** WP2 and WP3 deferred: the 15-minute idle lock, and voice in the app.

---

# 3. Context Investigated

| Item | Finding |
|---|---|
| **No Mac installer exists** | The only release is `v0.1.0` (24 July 2026), from before macOS support. `release.yml`'s `release-macos` job builds the `.dmg`, but only on a version tag that equals `VERSION` (0.1.0, already tagged), and **it has never run on a tag**. Each release job publishes its own files to the release, so one job can publish while the other fails. The CI `rust-macos` job builds an app bundle but does not keep it. |
| What a tag now also runs | Both release jobs run the voice self-check and, for the first time, **the real voice round trip** (WP3 V11) on Windows and on Apple Silicon. A tag is the only way that check runs. |
| Version files | `sync_product_version.py` updates `VERSION`'s four build files (`pyproject.toml`, `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`) but **not the lock files** (`package-lock.json`, `src-tauri/Cargo.lock`), which carry the package's own version. |
| The app | Installed as **`/Applications/JARVIS Guardian Shell.app`** (`productName`); the backend is `Contents/MacOS/jarvis-backend`. The path has spaces. |
| The Mac | ESR-0061 Section 6A: a **new Mac** replaces the M1 Pro, about 21 November. Its chip, memory and macOS version are not yet recorded; the model recommendation for 16 GB unified memory (Qwen3.5 4B) is a prediction until measured. |
| Signing | Ad-hoc signed, not notarised (go-live decision D15): the first launch needs **System Settings, Privacy & Security, Open Anyway**, which appears only for a file carrying the download quarantine flag. Minimum macOS 13.0. |
| Measurement tools | `scripts/measure_ollama.py`; `scripts/measure_moderation.py`, which needs the **private moderation sentence set**. The set measured at ESR-0061 WP6d was lost; its replacement has **not been measured on the PC**, so there is no baseline to compare the Mac with. `scripts/setup-dev-environment.sh` installs Node and Rust, builds and runs the full test suite: far more than measuring needs. |
| Targets on record | Classifier (EIP-ESR0061-006 M1): median **message check at most 3 s on the Mac** (2 s on the PC); the PC met it for messages (median 0.69 s) but **missed it for replies** (median 2.68 s, accepted by the Programme Sponsor). Orb (EIP-ESR0061-004 W3): **idle under 5 percent total CPU**; active states at least 50 frames a second. |
| Who uses the Mac | The household's Child-role user (15). Claude for a Child stays **off** until the "Children and privacy" page is published; nothing in this visit changes that. The visit's test data lives in the Child's own Mac account and must not stay there. |

---

# 4. Scope

## 4.1 Before the visit (P)

| # | Step | Detail |
|---|---|---|
| **P1** | Version 0.2.0 | `sync_product_version.py 0.2.0`; then the lock files' own version lines, with `npm install --package-lock-only` and `cargo update --workspace` (which touches only this project's crates); `--check` agrees. Committed through the gate with the WP3 completion records. |
| **P2** | Release | The Programme Sponsor pushes, then tags and pushes **`v0.2.0`**. Both release jobs must be green; the voice round-trip lines ("Whisper heard: ...") are read from both logs and recorded, and both checksums noted. **If either job fails:** the release and tag are deleted (`gh release delete v0.2.0 --cleanup-tag`, the Programme Sponsor's action) so no half-published release is left; the fault is registered and fixed in its own Work Package; then tagged again. Done at least a week before the visit (D-1). |
| **P3** | Classifier baseline on the PC | `measure_moderation.py` with the **replacement** sentence set on the PC, the same way as M2, so the Mac has a like-for-like comparison. Its SHA-256 is recorded with the results (the hash only, never the content or where it is kept). |
| **P4** | What the Programme Sponsor brings | The **Mac's administrator password** (Gatekeeper, the Python install); the household's Administrator PIN; the Programme Sponsor's non-production Claude key for C8; the sentence set **on a USB stick only**, with a master copy kept off the Mac (the last set was lost) (D-3); about 3 hours. |

## 4.2 At the visit: checks (C)

Each check records **pass / fail / not run**, with what was seen. Downloads go first so they run during the rest.

| # | Check | How | Pass when |
|---|---|---|---|
| **C1** | The Mac | Apple menu, About This Mac; in Terminal `sysctl -n machdep.cpu.brand_string`, `sysctl -n hw.memsize`, `sw_vers`; and whether iCloud "Desktop and Documents" is on | Chip, memory, macOS version and the iCloud setting recorded |
| **C2** | Install and Gatekeeper | **Download** the `.dmg` on the Mac from the release page (so it carries the quarantine flag); `shasum -a 256` it against the release checksum; drag to Applications; first launch; System Settings "Open Anyway" | Checksum matches; JARVIS opens after one "Open Anyway"; no warning on the next launch |
| **C3** | First run | The first-run flow as a new household would see it: the household's real Administrator profile and PIN, the Child's profile | Completes without a developer step. These two profiles are the household's own and stay. Observations go to go-live WP9; WP9 is not claimed here |
| **C4** | WKWebView look | Every view, light and dark mode, window narrow and wide | Matches the PC; each difference listed with a screenshot (no screenshot showing the sentence set's location) |
| **C5** | Ollama | Install Ollama from its download page; AI models: status, the recommendation, **download and use** the recommended model and the safety checker | Recommendation shown; both download and are used. Start these, and C6's downloads, then carry on |
| **C6** | Voice and the microphone (EBG-0167) | AI models, Voice: download Speaking and Listening. Then speak a reply. Then the microphone **for the first time**: the one-time macOS prompt appears - record its wording and allow it - and speak a question. Then turn JARVIS off in System Settings, Privacy & Security, Microphone, and try again; then back on | Both voices download and come on without a restart; the prompt names JARVIS and shows the `NSMicrophoneUsageDescription` text; the reply is heard; the question appears in the composer; with access off, the honest note is shown, not a hang |
| **C7** | Keychain | As the Administrator, Settings: save the Claude key; quit and reopen; then **remove** it | The key survives a restart; Keychain Access shows the JARVIS entry while saved and none after removal |
| **C8** | File dialogs (WP2 F1) | In a test folder **outside** Documents and Desktop (`~/JARVIS-visit-test`, so iCloud never syncs it): export a profile, back up memory, restore from that backup; then choose `/Library` and `~/Library/LaunchAgents` | Ordinary folders work; the system folders are refused with "JARVIS does not use system folders" |
| **C9** | Child experience | Sign in as the Child: an ordinary question, moderated; no household notes; no Claude offer; Settings shows no Claude consent | As on the PC; Claude for a Child is off, before and after the visit |
| **C10** | Idle lock (WP2) | As the Administrator with a PIN, the display kept awake (`caffeinate -d` in Terminal), JARVIS untouched for 15 minutes - run during M1 | Signed out between **15 and 16 minutes** (the backend checks every 5 s, the screen every 30 s), "Signed out after 15 minutes without use", the PIN asked to return |
| **C11** | Process stop (`killpg`) | Three ways, each followed by `pgrep -fl jarvis-backend` after 10 seconds: **quit** normally; **SIGTERM** (`pgrep -fl "JARVIS Guardian Shell"` for the app's id, then `kill -TERM <id>`); **Force Quit** in Activity Monitor | No `jarvis-backend` process left after any of the three |
| **C12** | `_MEI` clean-up | `ls -d "$TMPDIR"_MEI*` before launch, while running, and after each stop in C11 | None left after a normal quit or SIGTERM; any left after Force Quit is recorded (a known PyInstaller limit if so) |
| **C13** | GIA names | System view: what GIA reports for tools on macOS | The honest "not observable" off Windows (EIP-ESR0061-002 6.7); no wrong process names |
| **C14** | Packaged voice from Terminal | `"/Applications/JARVIS Guardian Shell.app/Contents/MacOS/jarvis-backend" --voice-self-check`, then the same with `--voice-round-trip ~/.jarvis/models` (after C6), each run with `time` | Self-check passes; the round trip hears the sentence |

## 4.3 At the visit: measurements (M)

Thresholds are the recorded targets where one exists; otherwise the figure is recorded for the first time and judged against the PC.

| # | Measurement | How | Judged by |
|---|---|---|---|
| **M1** | Chat model | `measure_ollama.py --models <list> --guard <the safety checker> --runs 3`, the list from C1's memory: 16 GB, `qwen3.5:4b qwen3.5:2b`; 24 GB or more, add `qwen3.5:9b` | The 4B recommendation **stands** if it and the safety checker both stay loaded and a warm short answer takes no more than the PC's median (3.8 s) plus half; otherwise R3 |
| **M2** | Classifier | `measure_moderation.py`, exactly as P3 on the PC | **Message check median at most 3 s** (M1's Mac target); the **reply check** is recorded beside the PC's (2.68 s, already accepted as missing 2 s), and a Mac figure over 3 s goes to the Programme Sponsor, as on the PC |
| **M3** | Orb | Activity Monitor, the packaged app on the conversation view: one minute idle, then one while speaking; % CPU of JARVIS and its web content process together | **Idle under 5 percent total CPU** (W3); frame rate cannot be read in the packaged app, so smoothness is judged by eye and recorded |
| **M4** | Voice timings | C14's times; in the app, from pressing speak to sound on a two-sentence reply, and from stopping the microphone to the text | First figures; recorded beside the PC's |
| **M5** | Start-up | From launch to the conversation view, and to voice `on` | First figures |

**Measurement set-up (D-2):** a **minimal** environment, not `setup-dev-environment.sh`: Python 3.12 (python.org installer), the repository cloned to a mode-700 folder outside Desktop, Documents and iCloud (`~/jarvis-measure`), a venv and `pip install -e .` only. The sentence set is copied from the USB stick into that folder. Before starting, Spotlight is told to skip the folder (System Settings, Spotlight, Search Privacy) and zsh history is paused for the session (`unset HISTFILE`), so neither records the location.

## 4.4 After the visit

| # | Step |
|---|---|
| **R0** | **Clean-up on the Mac, checked off before leaving:** the sentence set deleted from `~/jarvis-measure` and the Bin emptied; `~/jarvis-measure` deleted; Python left only if the household wants it (otherwise removed); `~/JARVIS-visit-test` deleted; the Claude key removed (C7) and Keychain Access showing no JARVIS entry; test conversations and test memory removed; the Spotlight exclusion removed with the folder; Claude for a Child confirmed off. The household's real profiles and the downloaded models stay. |
| **R1** | Results recorded in this EIP (a results section added after the visit) and the ESR-0062 WP4 row: every C and M with its outcome. **Evidence is redacted**: no command, output or screenshot that shows the sentence set's content or location. |
| **R2** | EBG-0162 and EBG-0167 marked Completed if their checks passed; every failure registered as its own EBG with a proposed WP, none fixed silently. |
| **R3** | `ollama_models.py`'s recommendation for Apple Silicon changed only through its own WP if M1 shows the 4B model does not fit. |

## 4.5 Programme Sponsor decisions

| # | Question | Recommendation |
|---|---|---|
| **D-1** | Where the Mac installer comes from | **A real release, `v0.2.0`**, at least a week before the visit: it is what a household would install, it runs the real voice round trip on both platforms for the first time, and it needs only a version number. If a release job fails, the release and tag are deleted and redone (P2). The alternative - keeping the CI build's app bundle as an artifact - needs a workflow change and gives an unsigned zip nobody else would use. |
| **D-2** | Measurement tools on the household Mac | **A minimal, temporary environment for M1 and M2 only**, as set out under 4.3, removed in R0. The alternative is to skip M1 and M2, which leaves the 3-second target and the 4B recommendation unmeasured. |
| **D-3** | The private sentence set | **USB stick only** (not AirDrop, which lands in Downloads, indexed and visible to the Child), used from the mode-700 folder, deleted with the Bin emptied at the end; a master copy kept off the Mac. Never iCloud, OneDrive or the repository. |

---

# 4A. Commit Contents

| Area | Files |
|---|---|
| P1 | `VERSION`, `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`, `package-lock.json`, `src-tauri/Cargo.lock` (version lines only) |
| Records | This EIP; ESR-0062; PST-0001; REG-0001; the WP3 completion records (EIP-ESR0062-003 0.5, ESR-0062 0.5, PST-0001 3.50, EBR-0001 1.238), which ride with this commit. After the visit, a second records-only commit: the results, EBR-0001 dispositions |

No product code changes in WP4. Defects the visit finds are fixed in their own Work Packages.

---

# 5. Evidence Pack

The release jobs' logs (voice round trip on both platforms, checksums); P3's PC baseline; the visit's results table (added to this EIP after the visit), with redacted screenshots for C4 and anything that fails; the measurement scripts' output; `pgrep` and `ls` output for C11 and C12; the R0 clean-up list, checked off.

---

# 6. Explicitly Out of Scope

* Go-live WP9 (clean-machine first run): C3's observations feed it; it is not done here.
* Notarisation and a paid Apple Developer account (D15).
* Turning on Claude for a Child (waits for the "Children and privacy" page, WP5).
* The Claude Console checks carried from EIP-ESR0061-003 (spend limit, a live refusal, an HTTP 529): they need the Programme Sponsor's Console, not the Mac.
* Fixing anything found: each finding becomes its own backlog item.
* GPU or Metal tuning for Ollama or Whisper beyond recording what M1 and M4 show.

---

# 7. Validation Requirements

1. The `v0.2.0` release exists with a Windows installer and a `.dmg`, each with a checksum, and both release jobs' voice round trips passed.
2. P3's PC baseline exists before M2 is run.
3. Every C and M item has an outcome recorded (pass, fail with what was seen, or not run with why).
4. No private sentence or its location is written into the repository or shown in evidence; the Mac holds no copy after R0.
5. R0 is checked off in full; Claude for a Child is off before and after.
6. EBG-0162 and EBG-0167 are closed only on passing checks; every failure has an EBG.

---

# 8. Questions for the Engineering Reviewer

1. Is anything carried for the real Mac missing from C and M?
2. Is each pass condition specific enough to decide on the day?
3. Is a version bump to 0.2.0 and a real release the right way to get the Mac installer (D-1)?
4. Is the sentence set's handling (D-2, D-3) sound?
5. Anything rated Medium or higher.

---

# 9. Review Record

**Design review, Copilot CLI (bridge `ESR-0062`/`WP4`, 8 November 2026, `sender: reviewer`): Conditional Pass**, no High, six Medium. It confirmed `release.yml`, `sync_product_version.py` and the `.dmg` job work as D-1 assumes. Each finding and what v0.2 does:

| Finding | Rating | Disposition in v0.2 |
|---|---|---|
| M1: the bundle is `JARVIS Guardian Shell.app`, not `JARVIS.app`; the path has spaces | Medium | **Accepted**: Section 3 and C14 use the quoted real path |
| M2: the sentence set - AirDrop lands in indexed, visible Downloads; a mode-700 folder outside Desktop, Documents and iCloud; Spotlight, Time Machine, zsh history; redact evidence; keep a master copy (the last was lost) | Medium | **Accepted**: D-3 (USB only, master copy off the Mac), the measurement set-up under 4.3 (mode 700, Spotlight skipped, `unset HISTFILE`; Time Machine is covered by deleting the folder the same day), R0, R1's redaction rule |
| M3: no baseline for the replacement set; which figure meets 3 s; the reply check already missed on the PC | Medium | **Accepted**: P3 measures the replacement set on the PC first; M2 judges the message check against 3 s and reports the reply check beside the PC's |
| M4: `setup-dev-environment.sh` installs Node and Rust and builds; P3 omitted the administrator password | Medium | **Accepted**: a minimal Python environment (4.3); the password in P4 |
| M5: `release-macos` has never run on a tag; no recovery for a half-published release; the lock files are not synced; a `.dmg` copied by USB may lack the quarantine flag | Medium | **Accepted**: P1 (lock files), P2 (delete release and tag on failure, a week's margin), C2 (download on the Mac) |
| M6: test data in the Child's account (a Claude key, exports, profiles); iCloud-synced Documents; Claude for a Child off before and after | Medium | **Accepted**: C8 in a non-synced test folder, C1 records the iCloud setting, R0 clean-up list, C9 and R0 confirm Claude for a Child off |
| Low: no thresholds for M1 to M5; the Orb target from W3; M1's model list should follow C1 | Low | **Accepted**: the "Judged by" column; M3 uses W3's 5 percent; M1's list from C1 |
| Low: C6 and C7 both depend on the one-time microphone prompt | Low | **Accepted**: merged into C6 (record the first prompt, then deny through System Settings) |
| Low: the idle lock needs a tolerance and an awake display | Low | **Accepted**: C10 (15 to 16 minutes, `caffeinate -d`) |
| Low: add a SIGTERM case | Low | **Accepted**: C11 |
| Info: the Console checks belong under Out of Scope | Info | **Accepted**: Section 6 |

---

# 11. Preparation (v0.3)

**Design approved** by the Programme Sponsor, 9 November 2026 (direct chat: "Approved"), on v0.2, with the Section 4.5 recommendations as the decisions: **D-1** a real `v0.2.0` release; **D-2** a minimal, temporary measuring environment; **D-3** the sentence set on a USB stick only, master copy off the Mac. The new Mac's chip and memory are **not yet known**; C1 records them on the day and M1's model list follows (16 GB: 4B and 2B; 24 GB or more: add 9B).

| Step | Record |
|---|---|
| P1 | `sync_product_version.py 0.2.0` updated `VERSION`, `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`; `npm install --package-lock-only` and `cargo update --workspace` changed only the project's own version line in `package-lock.json` (two lines) and `src-tauri/Cargo.lock` (one line), no dependency; `--check` agrees; the script tests (224 passed) and `cargo check` pass. Line endings kept LF |
| Implementation review | **Copilot Pass** and **Antigravity Pass** (bridge `ESR-0062`/`WP4`): only version lines changed, no dependency moved, the tag check will accept `v0.2.0`, the WP3 completion records match the facts. Both noted REG-0001's history order (3.846 above 3.845), which is the newest-first convention: no change |
| P2 | After the Programme Sponsor's approval, this commit and its push: the Programme Sponsor tags and pushes `v0.2.0` |
| P3 | The PC baseline with the replacement sentence set: to run on the PC before the visit (it needs the set, which the Programme Sponsor holds) |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 9 November 2026 | Claude Engineering Implementer | Design approved (D-1 to D-3 as recommended); P1 built: version 0.2.0 in VERSION, the four build files and the two lock files' own version lines (Section 11). |
| 0.2 | 8 November 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot), six Mediums accepted: the real app path; the sentence set's handling (USB only, mode-700 folder, Spotlight and history, redaction, master copy); a PC baseline for the replacement set first (P3); a minimal measuring environment; release recovery, lock files and downloading the `.dmg` on the Mac; test data cleaned from the Child's account (R0). Lows accepted: thresholds, the merged microphone check, the idle-lock tolerance, a SIGTERM case; the Console checks out of scope. Checks renumbered C1 to C14. |
| 0.1 | 8 November 2026 | Claude Engineering Implementer | Drafted at ESR-0062 WP4: preparation (a `v0.2.0` release for the Mac installer, which also runs WP3's real voice round trip), 15 on-visit checks, 5 measurements, recording rules; three decisions for the Programme Sponsor (installer source, measurement tools on the household Mac, the private sentence set). |
