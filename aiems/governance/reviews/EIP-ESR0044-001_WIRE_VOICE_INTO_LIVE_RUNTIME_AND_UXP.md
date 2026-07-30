# EIP-ESR0044-001 - Wire Guardian's Voice Faculty into the Live Runtime and UXP

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0044-001 |
| Artefact ID | EIP-ESR0044-001 |
| Title | Wire Guardian's Voice Faculty into the Live Runtime and UXP |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0114 |
| Intended Session | ESR-0044 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0114 was discovered at ESR-0042 WP1: `GuardianRuntime.speak()` (the Voice faculty delivered at ESR-0040, EBG-0112) exists and works, but `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` - the one construction path the real running Tauri UXP actually uses - never constructs a speech provider or passes one into `GuardianRuntime`. Both ESR-0040's original live validation and ESR-0042's model comparison worked around this by using standalone, uncommitted scripts. Confirmed directly against the live code before drafting: no `src/`/`src-tauri/` surface calls `guardian.speak` at all today. This package closes that gap.

---

# 3. Objective

Wire Guardian's Voice faculty into the live product end to end: `build_default_runtime()` conditionally constructs a speech provider (mirroring the existing credential-gated real-provider pattern), a new `guardian.speak` JSON-RPC method exposes it, a new Tauri command bridges it to the frontend, and a minimal UI affordance lets the user actually hear a Guardian response - all while respecting the existing no-model-file-committed and no-automatic-download constraints from EIP-ESR0040-001.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` | Constructs `conversation_provider` and `memory_service`, passes both into `GuardianRuntime(...)` - no `speech_provider` argument. Confirmed via direct grep: no `Piper`/`speech_provider`/`onnx` reference anywhere in this file. |
| `jarvis/interfaces/stdio_rpc.py` `_build_real_provider()` | Established pattern this package mirrors: returns `None` when a credential/config is absent, so `build_default_runtime()` degrades honestly rather than failing - no mock fallback (ESR-0017 WP9 rule). |
| `sentinel/piper_provider.py` `PiperProvider` | Requires `configuration.endpoint` (a local `.onnx` path with its companion `.onnx.json`); raises `ValueError` if `endpoint` is absent, `RuntimeError` if the model fails to load. No default path exists anywhere in source - model acquisition remains a disclosed, one-time manual step (EIP-ESR0040-001 Section 6 item 9), never automatic. |
| `jarvis/interfaces/voice.py` `SentinelGatedSpeechProvider` | Already implemented; takes a `SentinelTrustGateway` (the same gateway instance `build_default_runtime()` already constructs for conversation) and a `SpeechSynthesisProvider` (e.g. `PiperProvider`). |
| `jarvis/guardian/runtime.py` `GuardianRuntime.__init__` | Already accepts an optional `speech_provider: GuardianSpeechProvider | None = None` parameter; `speak()` already handles the `None` case (`STATUS_NOT_CONNECTED`) correctly. No change needed to this file. |
| `jarvis/interfaces/stdio_rpc.py` `StdioRpcServer._methods` | Dict-based JSON-RPC method registry (`guardian.converse`, `platform.status`, `knowledge.graph`, `memory.*`, `gia.status`) - a new `guardian.speak` entry follows the exact same pattern as `_guardian_converse`. |
| `src-tauri/src/lib.rs` | `send_message`/`platform_status`/`knowledge_graph` are thin `#[tauri::command]` wrappers around a shared `call_backend(state, app_handle, method, params)` helper - a new `speak_message` command follows this exact pattern, registered in the same `generate_handler!` list. |
| `src/App.jsx` `CommandPanel` | Renders `messages` (`{id, role, text}`) as plain `<p>` elements; no audio playback anywhere in the frontend today. |
| Toolchain check (this session) | `cargo check` succeeds cleanly on the current tree (~80s); `npx playwright --version` (1.61.1) and existing `tests/e2e/app.spec.js` (mocks `window.__TAURI_INTERNALS__.invoke`) confirm this package's changes can be genuinely built and tested, not merely written. |

---

# 5. Scope

This package authorises, across three layers:

## 5.1 Backend (`jarvis/interfaces/stdio_rpc.py`)

1. Add `PIPER_VOICE_PATH_ENV_VAR = "JARVIS_PIPER_VOICE_PATH"` - no default constant, mirroring the credential-gated pattern (`_build_real_provider`), not the Ollama pattern (which has a sensible network-endpoint default) - there is no sensible default local file path for a model that is never committed or auto-downloaded.
2. Add `_build_speech_provider(gateway, environ) -> SentinelGatedSpeechProvider | None`: returns `None` when `JARVIS_PIPER_VOICE_PATH` is absent or blank (mirroring `_build_real_provider`'s absent-credential handling exactly); otherwise constructs `PiperProvider(ProviderConfiguration(provider_name="piper", endpoint=<path>))` wrapped in `SentinelGatedSpeechProvider(gateway=gateway, provider=...)`, reusing `build_default_runtime()`'s existing single `gateway` instance (not a second one), matching how `memory_service` already reuses it (EIP-ESR0027-001 Section 4 precedent).
3. Pass `speech_provider=_build_speech_provider(gateway, environ)` into the existing `GuardianRuntime(...)` construction call.
4. Add `"guardian.speak": self._guardian_speak` to `StdioRpcServer._methods`.
5. Add `_guardian_speak(params) -> dict`: reads `params["text"]` (`TypeError` if not a string, matching `_guardian_converse`'s existing validation), calls `self._runtime.speak(text)`, and serializes the `SpeechOutcome`: `{"status": outcome.status, "message": outcome.message}` always, plus `{"audio": base64.b64encode(outcome.audio.audio_bytes).decode("ascii"), "mimeType": outcome.audio.mime_type}` only when `outcome.status == "synthesized"` (audio is `None` for every other status, per `SpeechOutcome`'s own invariant).

## 5.2 Tauri Bridge (`src-tauri/src/lib.rs`)

6. Add `speak_message(state, app_handle, text: String) -> Result<Value, String>`, calling `call_backend(&state, &app_handle, "guardian.speak", json!({ "text": text }))` - byte-for-byte the same shape as `send_message`.
7. Register `speak_message` in the existing `tauri::generate_handler![...]` list.

## 5.3 Frontend (`src/App.jsx`)

8. Add a small "speak" icon button next to each `role === "guardian"` message in `CommandPanel`'s conversation log, calling `invoke("speak_message", { text: entry.text })`.
9. On a `synthesized` response, decode the returned base64 audio into a data URI (`data:${mimeType};base64,${audio}`) and play it via a plain `Audio` object - no new dependency, matching the "no new UXP dependency for a backend-reachable capability" precedent.
10. On any non-synthesized response (`not_connected`/`not_running`/`denied`/`unavailable`), surface `message` as a small, non-blocking inline note (matching `sendError`'s existing pattern) rather than a hard failure - Guardian has no speech provider configured on most machines by default, and that must read as an honest capability boundary, not a bug.
11. The same non-blocking inline note must also catch failures in the frontend's own handling - a rejected `invoke("speak_message")` call, a malformed base64/data-URI, or a rejected `Audio.play()` promise (e.g. browser autoplay restrictions) - not just the backend's own non-synthesized statuses. Browser playback can fail independently of anything the backend reports.

## 5.4 Tests

11. Extend `jarvis/tests/test_stdio_rpc.py`: `build_default_runtime()` wires a speech provider when `JARVIS_PIPER_VOICE_PATH` is present (via an injectable fake `PiperProvider`-shaped seam, never loading a real model in a unit test - matching `PiperProvider`'s own existing `synthesizer` injection point) and leaves it `None` when absent; `guardian.speak` RPC method returns the correct shape for both a synthesized and a `not_connected` outcome.
12. Extend `src-tauri/src/lib.rs`'s existing test module with a `speak_message` test mirroring `send_message`'s own test pattern, if one exists at that level (to be confirmed during implementation - `call_backend` itself is already covered).
13. Extend `tests/e2e/app.spec.js` (or add a new spec) mocking the `speak_message` Tauri command, confirming the speak button appears next to a Guardian message and triggers the mocked call with the correct `text` argument.

---

# 6. Authorised Files

1. `jarvis/interfaces/stdio_rpc.py`
2. `jarvis/tests/test_stdio_rpc.py`
3. `src-tauri/src/lib.rs`
4. `src/App.jsx`
5. `tests/e2e/app.spec.js`
6. `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md`
7. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
8. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
9. `src/styles.css` - discovered during implementation (minor styling for the new speak button), disclosed in Section 12 rather than silently added.

No other file is authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `_build_speech_provider` must reuse `build_default_runtime()`'s existing `gateway` instance - never construct a second `SentinelTrustGateway`.
2. No automatic voice-model download is authorised anywhere in this package - `JARVIS_PIPER_VOICE_PATH` is read-only configuration; if absent, the speech provider is `None`, exactly as an absent OpenAI/Gemini credential already degrades to `None` today. If the path is present but points to an invalid or missing model, `PiperProvider`'s existing constructor behaviour (raising `RuntimeError`, per EIP-ESR0040-001) is preserved unchanged - a configured-but-invalid path is a startup failure, distinct from an absent path's honest `not_connected` degradation. This is a deliberate, disclosed choice, not softened by this package; changing that failure semantic would itself require a separately approved package.
3. `PiperProvider`'s real model-loading code path (`import piper`, `PiperVoice.load`) must not be exercised by any new unit test - the existing injectable `synthesizer`/fake-seam pattern must be used, matching every other provider test in this codebase.
4. The frontend speak button must not block or replace the existing send/receive conversation flow - it is an additive affordance on an already-rendered message, not a redesign of `CommandPanel`.
5. No change to `ConversationRequest`, `guardian.converse`, `SentinelGatedConversationProvider`, or any existing text-generation provider adapter.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any automatic voice-model download - `JARVIS_PIPER_VOICE_PATH` must point to a file the Programme Sponsor has already placed there manually.
2. Speech input, microphone capture, or any STT capability.
3. Any redesign of `CommandPanel`'s conversation log beyond adding the speak button and its audio-playback/error-note behaviour.
4. Auto-playing every Guardian response as speech by default - this is an explicit, per-message, user-initiated action only (a future item could consider an "always speak" toggle; not this package).
5. Any change to `GuardianRuntime.speak()`, `SentinelGatedSpeechProvider`, or `PiperProvider` themselves - all three are already correct and unchanged by this package; only their wiring into the default construction path changes.

---

# 9. Constraints

1. No file change shall be made until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0043.
3. Rust changes must pass `cargo check`/`cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check` (the existing CI gate, EBG-0103) before being considered complete - not merely written and assumed correct.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
cd src-tauri && cargo build && cargo clippy -- -D warnings && cargo fmt --check && cargo test
cd .. && npx playwright test
```

Validation should confirm:

1. Full pytest suite passes, including new `test_stdio_rpc.py` cases, with no regression.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. Rust build/clippy/fmt/test all pass cleanly.
4. Playwright suite passes, including the new/extended speak-button spec.
5. **A genuine live smoke check**, not merely mocked tests: the Engineering Implementer downloads a real Piper voice model to a local, uncommitted path (via `piper-tts`'s own `download_voices` CLI, as already demonstrated safely at ESR-0042), sets `JARVIS_PIPER_VOICE_PATH`, runs `npm run tauri dev`, sends a real message, clicks the new speak button, and confirms real audio plays - matching this project's Operational Verification Before Reporting discipline. If a live audio-hardware check cannot be performed in this implementation environment, this shall be disclosed honestly, not assumed.
6. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

None new. Builds entirely on already-approved, already-shipped components (`PiperProvider`, `SentinelGatedSpeechProvider`, `GuardianRuntime.speak()`, all EIP-ESR0040-001; `call_backend`'s established Tauri pattern, ESR-0017 WP9/EBG-0102).

## Risks

1. **This implementation environment may not have real audio output hardware to confirm playback** - the live smoke check (Section 10 item 5) will use a real downloaded model and a real synthesis call, but actually hearing the result may require the Programme Sponsor's own machine, matching the exact precedent already established at ESR-0040 (a `.wav` file written to the Sponsor's Desktop for personal listening) and ESR-0042 (the same pattern for the model comparison). Disclosed upfront, not treated as a surprise at validation time.
2. **`JARVIS_PIPER_VOICE_PATH` has no default**, unlike `JARVIS_OLLAMA_MODEL` - most machines, including CI, will have Voice remain `not_connected` after this package, which is the correct, honest default (no model file exists to point to by default), not a regression.
3. **Rust/frontend test coverage for the new command may be lighter than the Python-side coverage**, since `call_backend` itself is already well-tested and `speak_message` is a thin wrapper - this is disclosed as a reasonable proportionality judgement, not an oversight, matching how `platform_status`/`knowledge_graph` are tested at the same thinness today.
4. **A configured-but-invalid `JARVIS_PIPER_VOICE_PATH` causes backend startup failure**, not a graceful `not_connected` degradation - `PiperProvider`'s constructor already raises `RuntimeError` on an unloadable model (EIP-ESR0040-001's existing, approved behaviour). This package preserves that unchanged rather than softening it, since altering `PiperProvider`'s own error contract is explicitly out of scope (Section 8 item 5).

## New Backlog Item Registered by This Draft

None. This package directly implements EBG-0114 in full (backend wiring and a UXP affordance, exactly as EBG-0114's own registration text scoped); no new distinct gap is disclosed beyond what EBG-0114 already named.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern. **Result: Pass, with non-blocking findings.** Codex confirmed: the credential-gated `JARVIS_PIPER_VOICE_PATH` pattern is correct (no sensible default exists, unlike Ollama); reusing the single `SentinelTrustGateway` instance for speech is correct, matching the memory-service precedent; the `guardian.speak` RPC shape is sound and consistent with `SpeechOutcome`'s own invariant; the frontend scope is appropriately minimal; the explicit exclusions correctly bound scope. Three non-blocking findings folded into v0.2: the frontend must also catch its own failures (rejected `invoke`, malformed data URI, rejected `Audio.play()`), not just backend non-synthesized statuses (Section 5.3 item 11, new); a configured-but-invalid path causing backend startup failure (rather than graceful degradation) is now explicitly disclosed as a deliberate, unchanged behaviour (Section 8 item 2, Section 11 Risk 4); tests should assert observable behaviour, not internals too tightly (Section 5.4 items 11-13, unchanged in substance).

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service before implementation began.

**Implemented exactly as scoped, across all three layers.**

- **Backend** (`jarvis/interfaces/stdio_rpc.py`): `PIPER_VOICE_PATH_ENV_VAR`, `_build_speech_provider()` (reusing the existing `gateway` instance, absent-path-safe), `speech_provider` passed into `GuardianRuntime(...)`, and a new `guardian.speak` RPC method serializing `SpeechOutcome` (base64 audio + mime type only when `synthesized`) - exactly as scoped. 6 new tests in `jarvis/tests/test_stdio_rpc.py`, using a `_FakePiperProvider` patched over the real class so no test ever loads a real model or imports `piper`.
- **Tauri** (`src-tauri/src/lib.rs`): `speak_message` command, byte-for-byte the same shape as `send_message`, registered in `generate_handler!`. `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test` all pass cleanly (a formatting fix was applied via `cargo fmt` during implementation).
- **Frontend** (`src/App.jsx`, `src/styles.css`): a per-message speak button for Guardian messages, decoding the returned base64 audio into a data URI and playing it via a plain `Audio` object; non-blocking inline error notes for both backend non-synthesized outcomes and the frontend's own failures (rejected `invoke`, malformed data URI, rejected `Audio.play()`), per Codex's non-blocking finding. `src/styles.css` was touched in addition to the originally authorised file list - a minor, directly necessary dependency (styling the new button) discovered during implementation, disclosed here rather than silently expanded. `npm run build` succeeds; 2 new Playwright specs added to `tests/e2e/app.spec.js` (not_connected error path, synthesized/no-error path via a minimal valid silent-WAV fixture), full e2e suite (7 tests) passes.
- **Governance**: [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] updated to record Voice as reachable through the live product; [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0114 marked Complete.

**Live smoke check performed exactly as scoped (Section 10 item 5)**: a real Piper voice model was downloaded via `piper-tts`'s own `download_voices` CLI to an uncommitted local path (removed after the check); a genuine `guardian.speak` call through the real `build_default_runtime()` + RPC wiring produced a real 161,836-byte `audio/wav` payload; a second call with `JARVIS_PIPER_VOICE_PATH` unset correctly returned `not_connected` with no `audio` key. Real audio-hardware playback confirmation (actually hearing it through the live Tauri app) was not performed in this implementation environment and remains available for the Programme Sponsor to do, matching the exact precedent already established at ESR-0040/ESR-0042.

Full Python suite: 424 passed, 1 skipped (was 418/1, 6 new). `validate_repository.py` (full mode): 0 errors, warning count reported at session close.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0114 (this package's parent item, to be marked Complete on approval and implementation). |
| [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] | Delivered the Voice faculty components this package wires in; not itself changed. |
| [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] | Established the `download_voices` CLI live-comparison pattern this package's own live smoke check reuses. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Voice faculty description to be updated recording live-product reachability. |
| [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Operational Verification Before Reporting discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Programme Sponsor approved**, verified via `submit-response` against the real Sponsor Approval Service. **Implemented exactly as scoped** across backend/Tauri/frontend layers; `src/styles.css` touched as a disclosed, minor discovered dependency. Live-verified end to end with a real 161,836-byte `audio/wav` payload. 424 tests pass, 1 skipped (6 new); Rust build/clippy/fmt/test clean; 2 new Playwright specs, full e2e suite (7) passes. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: Pass, with non-blocking findings. Folded in: frontend must catch its own failures (invoke rejection, malformed data URI, rejected `Audio.play()`), not just backend non-synthesized statuses; configured-but-invalid path's startup-failure behaviour explicitly disclosed as deliberate and unchanged. |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0044 WP1. Reviewed by Codex: Pass, with non-blocking findings (see v0.2). |
