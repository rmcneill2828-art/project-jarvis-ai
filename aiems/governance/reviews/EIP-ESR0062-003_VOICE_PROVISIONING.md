# EIP-ESR0062-003 - Voice Provisioning on Windows and macOS

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0062-003 |
| Title | Engineering Implementation Package: WP3 Voice Provisioning on Windows and macOS - In-App Voice Download, Packaged Voice, Start-Up Without Voice |
| Version | 0.5 |
| Status | Implemented - committed `56f4080`, CI green, post-commit review Pass (Copilot, Antigravity) |
| Session | ESR-0062 |
| Work Package | WP3 |
| Risk class | Elevated (downloads files from the internet onto the household's computers, and changes what the packaged backend contains). Copilot for design; both reviewers for the built result. |

---

# 2. Purpose

Delivers **EBG-0167** (go-live WP7, [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] decision D4: voice models are downloaded in-app). Today speech output (Kokoro) and speech input (`faster-whisper`) work only in a developer setup where someone has fetched the model files by hand and set two environment variables. An installed JARVIS has no voice at all, on either computer. After this WP a household Adult or Administrator can turn voice on from Settings with one button, on Windows and on the Mac, and it is ready for checking at Mac visit 1 (WP4).

Also folds in **EBG-0179** (registered with this EIP, Section 3): a voice model that fails to load stops the whole backend starting.

---

# 3. Repository Context Investigated

| Item | Finding |
|---|---|
| Wiring | `_build_speech_provider` and `_build_transcription_provider` in `jarvis/interfaces/stdio_rpc.py` build a Sentinel-gated `KokoroProvider` (`bm_george`, fallback `bf_isabella`, `en-gb`) only when `JARVIS_KOKORO_MODEL_PATH` and `JARVIS_KOKORO_VOICES_PATH` are set, and a `WhisperProvider` only when `JARVIS_WHISPER_MODEL_PATH` is set. "No voice model is ever auto-downloaded." Both are built once, inside `build_default_runtime`, and handed to `GuardianRuntime`, which reports `speech_available` / `transcription_available` through `platform.status`. The screen already shows the speak and microphone buttons only when these are true. |
| This PC | `~/.jarvis/models/kokoro/` holds `kokoro-v1.0.onnx` (325,532,387 bytes) and `voices-v1.0.bin` (28,214,398 bytes), but neither variable is set, so voice is off here too. No Whisper model is present. |
| **Packaged backend (tested)** | The Windows sidecar built on 15 October, started with the two Kokoro variables pointing at those files, **fails to start**: `RuntimeError: Kokoro voice model could not be loaded ... (FileNotFoundError)`. The same files load and speak from the source tree (3.7 seconds for load plus a short phrase). Cause: `kokoro_onnx` reads `config.json` beside its own code, `espeakng_loader` loads `espeak-ng.dll` / `.dylib` and `espeak-ng-data/` beside its code, and `faster_whisper` reads `assets/silero_vad_v6.onnx` beside its code; `scripts/build_backend_sidecar.py` collects none of these. |
| **EBG-0179 (new)** | The same test shows the second defect: the load error is not caught, so **the backend exits** and the app has no backend at all. Any damaged or partly downloaded model file would do the same. A voice problem must cost only the voice. |
| Download sources | Kokoro: the `kokoro-onnx` project's GitHub release `model-files-v1.0` (the files already on this PC; sizes match the release exactly). Whisper: Hugging Face `Systran/faster-whisper-base.en` at commit `3d3d5dee26484f91867d81cb899cfcf72b96be6c` (`config.json`, `model.bin` 145,216,508 bytes, `tokenizer.json`, `vocabulary.txt`). SHA-256 of every file is known (Section 4.1, V2). |
| Mac recording format | WKWebView's `MediaRecorder` gives `audio/mp4` (AAC), not WebM. Tested: `faster_whisper.audio.decode_audio` (PyAV) decodes an AAC-in-MP4 clip correctly (1.0 s in, 16,384 samples at 16 kHz out). The screen already passes the recorder's own MIME type. |
| Existing download pattern | `jarvis/interfaces/ollama_setup.py` `PullManager`: one download at a time in a background thread, `ollama.pullProgress` notifications at most every 0.5 s, cancel, a catalog that is the allow-list, Adult or Administrator only (`MODEL_MANAGER_ROLES`). `LocalAiPanel.jsx` in Settings shows it. |
| CI | The `rust-windows` and `rust-macos` jobs, and both release jobs, build the sidecar with `scripts/build_backend_sidecar.py`; `rust-macos` and `release-macos` then run `scripts/smoke_unix_sidecar.py`. None checks voice. |

---

# 4. Scope

## 4.1 Changes

| # | Item | Change |
|---|---|---|
| **V1** | Where voice lives, and when it is trusted | A fixed folder per model under the JARVIS data folder (derived from the existing data-folder logic, the folder that holds `memory/`, i.e. `~/.jarvis/`): `models/kokoro/` (the existing files) and `models/whisper/base.en/`. A model is **trusted** only when every file has been **SHA-256-checked against the catalog**: by the download itself, or - for files the app did not download, such as this PC's existing Kokoro files - by a check run **in the background before the first load** (about 2 s for 350 MB). A trusted model gets a small `verified.json` (each file's size and modification time); a later start trusts it cheaply while size and time still match, and re-checks the hash if either changed (M1). The environment variables still override the folders, for development: an overriding path is hash-checked when it matches a catalog file's size, and otherwise loaded as a developer's own model, as today. |
| **V2** | Catalog | `jarvis/config/voice_models.py`: for each model (Kokoro speech, Whisper base.en listening), each file's **HTTPS address** (the Kokoro GitHub release; Hugging Face pinned **by commit**, never `main`), **size** and **SHA-256**. The catalog is the allow-list: nothing else can be downloaded. |
| **V3** | Download | `jarvis/interfaces/voice_setup.py` `VoiceDownloads`, modelled on `PullManager` (M3): **one download at a time**, checked and set under one lock; a background thread; each file goes to `<catalog name>.part` (file names come **only from the catalog**, never the server) in the model's folder, which must be a real folder, not a link; **HTTPS at every hop** - a redirect handler refuses any non-`https` target and stops after 5 redirects (GitHub and Hugging Face redirect to signed CDN hosts, so the target host is not pinned; the hash is the trust); reading **stops past the catalog size** (`Content-Length` is not trusted); then **size and SHA-256 are checked** and the file is moved into place with `os.replace` (retried briefly on Windows, where antivirus can hold a new file); a mismatch deletes the `.part` and reports "The download was damaged. Try again."; a disk-full or other write error deletes the `.part` and says so; a read timeout ends a stalled download; a free-disk check before starting (size plus 10%). **Cancel** removes the `.part` files; once a file has been verified and moved, cancel no longer undoes it. Leftover `.part` files are removed at start. Notifications `voice.downloadProgress` (`{model, state, receivedBytes, totalBytes}`) at most every 0.5 s and at the end. No file is ever run: these are model data read by ONNX Runtime and CTranslate2; Kokoro's voices file is read with `np.load` with pickles not allowed (NumPy's default, checked). |
| **V4** | Who may download | Adult or Administrator, the same rule as the local model (`MODEL_MANAGER_ROLES`, D-3). A Child or Guest uses voice once it is there, as today. |
| **V5** | Loading in the background, and turning voice on without a restart | Voice is **never loaded inside `build_default_runtime`** (M2): the backend starts, answers at once, and loads each trusted model **in its own background thread** (one failing never holds up the other), reporting `loading` meanwhile. The same path installs a model after a download. `GuardianRuntime` gains `set_speech_provider` / `set_transcription_provider`, each one assignment under a lock (M4); `speak` and `transcribe` read the provider **once** into a local variable, so a swap can never leave a call half on the old provider and half on the new. Downloading over a model that is loaded is refused ("Voice is already on."): only a `missing` or `damaged` model can be downloaded, and a damaged one is never loaded. Speech still passes through Sentinel exactly as now. |
| **V6** | EBG-0179: start-up never fails because of voice | Covered by V5: no voice load happens before the backend answers. A model whose hash does not match is **never loaded**, so a native crash in ONNX Runtime or CTranslate2 from a damaged file cannot happen (M1); it reports `damaged`. A load that raises is left off and logged by exception type only ("Speech output is off: the voice model could not be loaded"). A model not present is logged as "not configured", never with a path. The screen offers a fresh download in both cases. |
| **V7** | RPCs | `voice.status` (each model: `missing` / `checking` / `loading` / `on` / `damaged` / `downloading`, sizes, free disk, whether this person may download), `voice.download {model}`, `voice.cancelDownload`. The role check is **in the backend** (V4); the screen only mirrors it. Excluded from `METHOD_CLUSTERS` the way the Ollama setup methods are. Rust: `voice_status`, `voice_download`, `voice_cancel_download`, registered in `generate_handler!`; the notification passes through like `ollama.pullProgress`. |
| **V8** | Screen | A **Voice** section in `LocalAiPanel.jsx` (Settings): for "Speaking" and "Listening", whether it is on, the download size, a **Download** button (Adult or Administrator only; others see "Ask an adult to turn this on"), progress, Cancel, and "Try again" after a failure. When the download finishes, the screen refreshes `platform.status`, so the speak and microphone buttons appear without a restart. |
| **V9** | Packaged backend | `build_backend_sidecar.py` adds `--collect-data kokoro_onnx`, `--collect-data faster_whisper`, and `--collect-all` for `espeakng_loader`, `phonemizer`, `language_tags`, `segments`, `csvw`, `av`, `ctranslate2`, `onnxruntime` and `tokenizers` (M5), trimmed only where the self-check proves an entry unnecessary. |
| **V10** | Packaged voice self-check | `jarvis_backend_entry.py --voice-self-check`, run **against the built executable** (M5): with no model download, it imports `kokoro_onnx`, `faster_whisper`, `ctranslate2`, `tokenizers` and `av`; reads `kokoro_onnx`'s `config.json`; loads the espeak-ng library and **phonemizes a sample sentence** with its data; **creates an ONNX Runtime session** on Whisper's VAD model; and decodes a small generated AAC-in-MP4 clip through PyAV. One line per part; non-zero exit if any fails. Run in CI after each sidecar build (`rust-windows`, `rust-macos`, both release jobs). |
| **V11** | Real voice in the release jobs | The two release jobs (Windows and macOS) also download both models (cached by their pinned hashes with `actions/cache`), then, with the **built executable**, synthesise one sentence and transcribe that audio back, checking the words return. Not on every push: macOS runner minutes are the limited resource, and the self-check (V10) already catches a missing part on every build (M5, partly accepted). |

## 4.2 Programme Sponsor decisions

| # | Question | Recommendation |
|---|---|---|
| **D-1** | Which Kokoro file | **The full model, 325 MB** (`kokoro-v1.0.onnx`): the one you chose `bm_george` on by ear (EIP-ESR0053-002). The 92 MB `int8` version is smaller but may sound different; worth a listening test later, not now. |
| **D-2** | Which Whisper model | **`base.en`, 145 MB**: quick on both computers, including the 16 GB Mac. `small.en` (484 MB) understands better but is about three times slower on the CPU; it can be added to the catalog later if `base.en` mishears too often. |
| **D-3** | Who may download | **Adult or Administrator**, the same as the local chat model. |

---

# 4A. Commit Contents

| Area | Files |
|---|---|
| V1-V7 | `jarvis/config/voice_models.py` (new), `jarvis/interfaces/voice_setup.py` (new), `jarvis/interfaces/stdio_rpc.py` (default locations, start-up without voice, three RPCs, the notification, installing a provider after download), `jarvis/guardian/runtime.py` (two setters under a lock), `jarvis/interfaces/activity_tracker.py` (exclusions) |
| V7 | `src-tauri/src/lib.rs` (three commands) |
| V8 | `src/LocalAiPanel.jsx`, `src/shell.css` if needed |
| V9-V11 | `scripts/build_backend_sidecar.py`, `scripts/jarvis_backend_entry.py`, `.github/workflows/ci.yml`, `.github/workflows/release.yml` |
| Tests | `jarvis/tests/test_voice_setup.py` (new): catalog sanity (HTTPS, pinned commit, sizes, hashes); download with an injected HTTP source - success, wrong hash, wrong size, too many bytes, cut short, stalled, redirect to `http://` and too many redirects, cancel before and after a file is verified, no disk space, disk full mid-write, a linked model folder, two requests at once, a leftover `.part` at start, `os.replace` retried, `.part` never used; trust - an existing unverified file hash-checked before load, the `verified.json` fast path, a changed size or time re-checked, a damaged file never loaded; loading in the background - the backend answers while a model loads, one model failing leaves the other on; a provider swapped while a speak runs finishes on one provider; downloading over a loaded model refused; role refusal for a Child and a Guest; start-up with damaged or unloadable files (EBG-0179); an AAC-in-MP4 fixture transcribed with an injected model; a provider installed after download and `platform.status` reporting it; default-folder detection and the environment override. e2e: the Voice section for an Adult and for a Child, progress and completion. A test that the self-check runs. |
| Records | This EIP; ESR-0062; PST-0001; EBR-0001 (EBG-0167 and EBG-0179); REG-0001 |

---

# 5. Evidence Pack

Windows pytest; Linux pytest, ruff and validator in `python:3.12-slim` Docker; `cargo fmt --check`, clippy and `cargo test`; `vite build`; Playwright (Chromium); pip-audit. **The sidecar built locally on Windows, `--voice-self-check` passing, then a real check on the PC with the packaged app**: download both models from Settings (this PC already has Kokoro, so only Whisper downloads; Kokoro is checked by renaming its folder and downloading it again), hear a reply spoken, and speak a question into the microphone. CI runs the self-check on the macOS build; the same real check on the Mac is added to the Mac visit 1 list (WP4).

---

# 6. Explicitly Out of Scope

* Running Whisper on the GPU, or any speed tuning (measured at WP4 on the Mac).
* A choice of voices or Whisper sizes in Settings (D-1, D-2).
* Downloading voice during first-run setup: the Settings section is enough for v1.0; first run can point to it later.
* Bundling the model files inside the installer (D4 chose download).
* Wake word or room speakers (EBG-0159, EBG-0160, post-launch).

---

# 7. Validation Requirements

1. A fresh install with no voice files starts, shows no speak or microphone button, and offers the download in Settings to an Adult or Administrator only.
2. A download is refused for a Child and a Guest; any model not in the catalog is refused.
3. A completed download is used **only if** every file's size and SHA-256 match; a damaged, short, stalled, cancelled or redirected-to-`http://` download leaves nothing in place and says so.
4. After a download, speaking and listening work **without a restart**.
5. A damaged or unloadable voice file never stops the backend starting (EBG-0179); the screen offers to download it again.
6. The packaged backend passes `--voice-self-check` on Windows and macOS in CI, and speaks and listens for real on the PC.
7. An `audio/mp4` recording is transcribed (the Mac's format).
8. All existing tests pass unchanged.

---

# 8. Questions for the Engineering Reviewer

1. Is checking size and SHA-256 against a pinned catalog, with `.part` files and `os.replace`, enough to trust a downloaded model? Anything else needed for files that ONNX Runtime and CTranslate2 will parse?
2. At start, is "every file at its catalog size" (no hash, to avoid reading 350 MB each start) a sound test of "installed", given that downloads are hash-checked before they are moved into place?
3. Is installing a provider into a running `GuardianRuntime` after download safe against a `guardian.speak` or `guardian.transcribe` already running on the slow lane?
4. Does the self-check (V10) prove enough about the packaged voice without the model files, or should CI also download the models and synthesise once (about 500 MB per run)?
5. Anything rated Medium or higher.

---

# 9. Review Record

**Design review, Copilot CLI (bridge `ESR-0062`/`WP3`, 8 November 2026, `sender: reviewer`): Conditional Pass.** It verified Section 3 against the code, including EBG-0179 (the builders do not catch the load error) and that the sidecar build collects none of the voice data. Each finding and what v0.2 does:

| Finding | Rating | Disposition in v0.2 |
|---|---|---|
| M1: a same-size damaged file passes a size-only test and reaches native code, which can abort the process; check whether the voices file is a pickle | Medium | **Accepted**: V1 - hash-checked before the first load of any file the app did not download, then a `verified.json` of size and time; V6 - a mismatched model is never loaded. The voices file is read by `np.load` with pickles not allowed (NumPy's default; checked in `kokoro_onnx/__init__.py`) |
| M2: loading Kokoro (about 3.7 s) and Whisper inside start-up delays the first answer | Medium | **Accepted**: V5 - loaded in the background after start, each on its own, reporting `loading` |
| M3: download details - redirects, a byte cap, catalog file names, links, disk full, cancel after verification, one lock, leftover `.part` files, `os.replace` on Windows | Medium | **Accepted**: all in V3 |
| M4: `speak` reads the provider twice; atomic setters; replacing a loaded model fails on Windows | Medium | **Accepted**: V5 - read once, one assignment under a lock, downloading over a loaded model refused |
| M5: the self-check should phonemize, create an ONNX Runtime session, import `faster_whisper`, `tokenizers` and `av`, and run against the built executable; more `--collect-all`; CI should synthesise and transcribe for real | Medium | **Accepted**, the last part **partly**: V9 and V10 as recommended; V11 - a real synthesis and transcription in the two release jobs, models cached, not on every push (macOS runner minutes). The signed macOS build loading the espeak library is checked by V11 and at Mac visit 1 |
| Low: derive the models folder from the data-folder logic; log "not configured"; an AAC/MP4 fixture test; the role check in the backend | Low | **Accepted**: V1, V6, Section 4A, V7 |
| Info: D-1 to D-3 acceptable | Info | Noted |

---

# 11. Implementation (v0.3)

**Design approved** by the Programme Sponsor, 8 November 2026 (direct chat: "Approved and pushed"), on v0.2, with the Section 4.2 recommendations as the decisions - **D-1** the full Kokoro model, **D-2** Whisper `base.en`, **D-3** Adult or Administrator - and **EBG-0179 folded into this WP**.

## 11.1 Deviations and clarifications

| # | Item | What was built | Why |
|---|---|---|---|
| 1 | **PyAV capped below 19** (`pyproject.toml`), not in the design | `"av>=18.0.0,<19"` with the reason beside it | Found by the Linux check: a fresh install takes PyAV 19, which removed the `metadata_errors` argument that `faster-whisper` 1.2.1 (the latest) passes to `av.open`, so **every transcription fails**. This PC had PyAV 18, so Windows passed. It already affects every CI-built sidecar since PyAV 19 (including the macOS one), so the cap fixes listening on the Mac, not only these tests. Lift when `faster-whisper` adapts |
| 2 | V7, activity tracker | The three voice methods are **mapped to the "jarvis" cluster**, like the Ollama setup methods | v0.2 said "excluded ... the way the Ollama setup methods are", but the Ollama methods are in fact mapped, not excluded; the precedent was followed |
| 3 | V8, where the panel lives | Its own component, `src/VoicePanel.jsx`, under the Local AI panel on the **AI models** view, with its own `voice-panel` class sharing the Local AI styles | `LocalAiPanel` is also shown during first run, which Section 6 keeps voice out of. A Child or Guest never sees the AI models view (`roles.js`); the backend refusal is the boundary |
| 4 | Section 3, the speak button | Unchanged: **only the microphone button** follows `transcriptionAvailable`; the speak button is always shown and, with no voice, gives the existing "not connected" note | Section 3 said both buttons were gated; only the microphone is. The e2e test checks the microphone appears without a restart |
| 5 | V5, when loading starts | `VoiceSetup.start()` is called when the server starts serving (`serve_forever`), not in `build_default_runtime`, which loads nothing. **Eight existing tests** in `test_stdio_rpc.py` that set voice through the environment now wait for it (`_voice_ready`, which calls `load_now()`) | So no test, and no tool building a runtime, ever touches a real voice folder or waits for a model; disclosed test change |
| 6 | States | `failed` added beside `damaged`: a load that raised, or a model folder that is a link. Both offer "Download again"; a state change is announced only when it changes (`voice.changed`) | The screen needs to tell "files damaged" from "could not start"; announcing unchanged states broke the heartbeat-stream tests |
| 7 | V3, a damaged set | A file already present at its catalog hash is **not fetched again** | Downloading over a damaged model fetches only what is wrong |
| 8 | V11 helpers | `scripts/fetch_voice_models.py` (the app's own `VoiceSetup`, so CI fetches exactly as the app does) and `--voice-round-trip <folder>` on the backend entry; `.voice-models/` in `.gitignore` | Not listed in Section 4A |
| 9 | WP2 follow-up carried | The two WP2 tests that used macOS's `/etc` (a link there) now use `/usr`, `/USR`, `/Library`, plus a test that `/etc` is still refused | recorded in EIP-ESR0062-002 (its approval and post-commit record); both WP2 post-commit reviewers agreed it was a test defect only |

## 11.2 What was built

| Item | Where |
|---|---|
| V1, V2 | `jarvis/config/voice_models.py` (catalog: addresses, sizes, SHA-256; Whisper pinned to commit `3d3d5dee...`); `jarvis/interfaces/voice_setup.py` `VoiceSetup` (trust: hash before the first load, `verified.json` of size, time and hash); `~/.jarvis/models/kokoro`, `~/.jarvis/models/whisper/base.en` |
| V3 | `VoiceSetup.download` / `_run_download` / `_fetch`: one lock, catalog names only, `HttpsOnlyRedirects` (https at every hop, 5 redirects), byte cap, size and hash, `.part` then `os.replace` with retries, disk check, cancel, leftovers removed at start |
| V4, V7 | `voice.status` (with `mayDownload`), `voice.download`, `voice.cancelDownload` in `stdio_rpc.py`, Adult or Administrator checked in the backend; `voice_status`, `voice_download`, `voice_cancel_download` in `lib.rs` |
| V5, V6 | Background threads per model; `GuardianRuntime.set_speech_provider` / `set_transcription_provider` under a lock, `speak` and `transcribe` read the provider once; `_voice_loader` and `_voice_overrides` replace the two builders; nothing loads at build time, and no voice error can stop start-up (EBG-0179) |
| V8 | `src/VoicePanel.jsx`; `App.jsx` passes voice notifications to it and re-reads `platform_status` on `voice.changed`; `panels.css` |
| V9 | `VOICE_PACKAGING` in `scripts/build_backend_sidecar.py` |
| V10 | `jarvis/interfaces/voice_self_check.py`, `--voice-self-check` in `scripts/jarvis_backend_entry.py`; a step after the sidecar build in `rust-windows`, `rust-macos` and both release jobs |
| V11 | `--voice-round-trip`, `scripts/fetch_voice_models.py`, `actions/cache` (v6.1.0, pinned by commit) keyed on the catalog, in both release jobs |

## 11.3 Evidence

| Check | Result |
|---|---|
| New tests | `jarvis/tests/test_voice_setup.py`: **47 passed** - every Section 4A case, including eight requests at once starting one download, a provider swapped mid-speak, a junction as the model folder (ran on Windows), the role refusals through the RPC, EBG-0179 with the real `KokoroProvider`, an AAC-in-MP4 recording decoded, and the self-check from source |
| Windows pytest | **1596 passed, 5 skipped** (1549 before WP3); after the review fixes, the voice tests 48 passed, 1 skipped (the planted-link test needs a file link, which Windows does not make without extra rights) |
| Linux (`python:3.12-slim` Docker) | ruff clean; version check agrees; pytest **1595 passed, 6 skipped (PyAV 18.1.0)**, and **1597 passed, 6 skipped** after the review fixes (all 49 voice tests ran, the planted-link one included); validator 0 errors; pip-audit no known vulnerabilities. The first run found deviation 1 |
| Rust (Windows) | `cargo fmt --check`, `cargo clippy --all-targets -D warnings` clean; `cargo test` 19 passed, 1 ignored |
| Frontend | `vite build` succeeds; Playwright (Chromium) **202 passed, 5 skipped** (five new: an Administrator downloads and the microphone appears without a restart; an Adult downloads and cancels; a failed download says why; damaged and unstartable offer "Download again"; a developer setting is shown, not downloadable) |
| **A real download** | `fetch_voice_models.py` with this PC's Kokoro copies in place (a cache hit, hash-checked) and Whisper fetched from Hugging Face through its CDN redirects: 15 s, both `on` |
| **The packaged backend, built** | The Windows sidecar built with V9 (128 MB, was 115 MB): `--voice-self-check` passes all five parts; `--voice-round-trip` speaks "Good evening. This is a voice test." and Whisper hears "Good evening, this is a voice test." |
| **The self-check catches a bad build** | A sidecar built **without** V9: four of the five parts fail (`kokoro_onnx/config.json`, Whisper's voice-activity model), exit 1 |
| **The packaged backend over JSON-RPC** | The built sidecar, models in a scratch data folder: the first request answered while voice was still loading (speech and listening off), both on about 4 s later (`voice.changed` loading, then on); a reply spoken (224 KB of audio) and heard back word for word |
| Validator | 0 errors, 311 warnings |
| Manual check on the PC | Not yet run: in the app, open AI models, download Listening (Kokoro is already here and is checked, not downloaded), then hear a reply and speak a question. Offered to the Programme Sponsor; the same on the Mac at WP4 |

## 11.4 Implementation review (v0.4)

**Copilot CLI (bridge `ESR-0062`/`WP3`): Pass**, no High or Medium. It ran pytest (1596 passed), ruff and the validator itself, and confirmed M1 to M5 and the Lows were built as v0.2 says: no model file reaches Kokoro or Whisper without a SHA-256 match (apart from the designed developer override), HTTPS at every hop, no path-traversal route, loading never blocks start-up, the provider swap is safe, no path is logged, the role check is in the backend, the PyAV cap is the right fix and the `_voice_ready` test change is legitimate. It could not check the `actions/cache` pin offline: it was resolved through the GitHub API to the `v6.1.0` tag's commit `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` when it was written.

| Finding | Rating | Disposition |
|---|---|---|
| L1: a same-size file swap that also restores its modification time passes `verified.json` | Low | **Accepted**: it needs write access to the person's own data folder, which already allows anything the voice could do |
| L2: a link planted at a `.part` name is not checked | Low | **Fixed**: the name is removed first (a link itself, never its target) and the file created with `"xb"`, refusing anything that appears meanwhile; test `test_a_link_planted_at_the_partial_name_is_removed_not_followed` (runs on Linux and macOS) |
| L3: a download started just after start-up can have its state overwritten by the first check | Low | **Fixed**: a download is refused while that model's start-up check runs ("This voice is starting"); test `test_a_download_cannot_start_while_the_start_up_check_runs` |

**Antigravity (second reviewer, after the fixes): Pass**, no findings above Low; L2 and L3 verified in code and tests, L1 accepted. Its first run ended while waiting on a background test run and recorded nothing; it was resumed with the test results already in hand and recorded its verdict.

## 11.5 Approval, commit and post-commit (v0.5)

| Step | Record |
|---|---|
| Built-result approval | **Approved** by the Programme Sponsor through the Sponsor Approval Service on parent `765b5f6`; `submit-response ESR-0062 WP3` accepted (8 November 2026, 21:26 UTC), its own pytest and validator run clean. The optional manual check in the app on the PC was not run; it is on the Mac visit 1 list (WP4) with the Mac's own |
| Commit | **`56f4080`**, 28 files, carrying WP2's completion records and the macOS test fix; pushed by the Programme Sponsor |
| CI | Run 42525817585 **success**: python, python-macos (green again: the WP2 test fix works), rust, rust-windows, rust-macos, frontend-build, playwright. **The voice self-check passed all five parts on both real CI builds**, Windows and macOS (Apple Silicon, PyAV 18.1.0 arm64 wheel). playwright-webkit (allowed to fail) failed the same 5 microphone tests as before. The release jobs' real round trip (V11) runs only on the next version tag, so it is untested until then |
| Post-commit review | **Copilot Pass** (no High or Medium): all 28 paths expected, deviations present, no stray files, nothing revealing the private sentence set. Low: the commit message cites the Windows pytest count from before the L2 and L3 fixes (1596; the voice tests then added two, one Windows-skipped) - recorded here, not amended in a pushed commit. Info: `voice.status` is readable by any profile, exposing only model state; download and cancel are restricted. **Antigravity Pass**, the same conclusions |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.5 | 8 November 2026 | Claude Engineering Implementer | Approved and committed (`56f4080`); CI green, the voice self-check passing on the real Windows and macOS builds; post-commit review Pass from Copilot and Antigravity (Section 11.5). |
| 0.4 | 8 November 2026 | Claude Engineering Implementer | Implementation review: Copilot Pass (L2, L3 fixed with tests; L1 accepted), Antigravity Pass after the fixes (Section 11.4). |
| 0.3 | 8 November 2026 | Claude Engineering Implementer | Design approved (D-1 to D-3 as recommended, EBG-0179 folded in). Built (Section 11): nine deviations and clarifications disclosed, notably PyAV capped below 19 (found by the Linux check: PyAV 19 breaks faster-whisper's decoding, already affecting CI-built sidecars); evidence includes a real download, the packaged sidecar's self-check and round trip, a self-check failing on a build without the packaging, and the packaged backend over JSON-RPC. |
| 0.2 | 8 November 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot): M1 accepted (hash-checked before first load, `verified.json`, a damaged model never loaded), M2 (background loading), M3 (download details), M4 (provider read once, atomic setters, no download over a loaded model), M5 (fuller self-check against the built executable, more collected packages; real voice in the release jobs only, V11); Lows accepted. |
| 0.1 | 8 November 2026 | Claude Engineering Implementer | Drafted at ESR-0062 WP3: EBG-0167 (in-app voice download, default voice folders, packaged voice, a CI self-check) and EBG-0179 (a voice model that fails to load stops the backend starting, found by testing the packaged backend); three decisions for the Programme Sponsor (Kokoro file, Whisper model, who may download). |
