# EIP-ESR0047-001 - Voice Faculty Phase 6 Increment B: Speech Input Scope

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0047-001 |
| Artefact ID | EIP-ESR0047-001 |
| Title | Voice Faculty Phase 6 Increment B: Speech Input Scope |
| Version | 1.1 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0117 |
| Intended Session | ESR-0047 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] scored "Basic Voice Input" **Fail** against [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5's explicit MLP 0.1 requirement. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0117 splits this out of EBG-0112 (Voice Faculty, Phase 6) per that item's own text, now that Increment B is selected as this session's objective. Increment A (speech output, [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]]) explicitly deferred speech input, stating "Any Deepgram integration or other speech-to-text provider - reserved for a future Increment B package, which would need to name and evaluate STT providers on its own merits" (Section 8 item 7) and "Any household-role or speaker-identity plumbing - not needed for output-only voice, since no new input is being attributed to any household member" (Section 8 item 6) - the second statement is precisely what changes for this package: speech input is a new act of data collection about a person physically present, engaging [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's Household Role Model in a way output never did.

---

# 3. Objective

Deliver the smallest defensible first increment of speech input: push-to-talk microphone capture in the Guardian Desktop Platform Shell, transcribed locally by a self-hosted speech-to-text provider through a new Sentinel-gated transcription path, with the resulting text placed into the existing message composer for the household member to review and send - reusing the existing `guardian.converse` path exactly as typed text does today, rather than opening a new conversation entry point.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `sentinel/speech_providers.py` | Established parallel-contract pattern this package mirrors for the opposite direction: `SpeechSynthesisRequest`/`SpeechSynthesisResponse`, a `SpeechSynthesisProvider` Protocol, `execute_speech_synthesis_with_sentinel_decision()`. Deliberately not reused as-is (text-to-speech and speech-to-text carry different request/response shapes), but the same pattern. |
| `sentinel/piper_provider.py` | Established provider-adapter pattern: lazy import inside a `_load_synthesizer()`-equivalent method (never at module top level, so unit tests never pay the model-load cost via a fake seam), `ProviderConfiguration.endpoint` carrying a local model path, eager construction-time failure (`RuntimeError`) rather than soft degradation once configured. |
| `jarvis/interfaces/voice.py` | `SpeechOutcome` (frozen dataclass, named `status` values, `__post_init__` invariants - `synthesized` status requires `audio`, others must not carry it) and `SentinelGatedSpeechProvider.synthesize()` (lines 89-115): builds a `SentinelRequest(source="jarvis.guardian.voice", intent="speech.synthesize", metadata={"capability": "speech-synthesis"})` with no `requires_approval` flag set, evaluates via `gateway.evaluate()`, returns `STATUS_DENIED` on non-`ALLOW`, else executes and maps `RuntimeError` to `STATUS_UNAVAILABLE`. |
| `sentinel/policy.py` `TrustTierPolicy.classify()` (lines 124-143) | Reads `SentinelRequest.metadata`/`payload_type`/`requires_approval` to route to `UNSUPPORTED_HIGH_RISK`/`EMERGENCY_CONTROL`/`LOCAL_AGENT_ACTION` (all `DENY`), `HUMAN_APPROVAL_REQUIRED` (`REVIEW`, only if `requires_approval=True`), else `ROUTINE_INTERACTION` (`ALLOW`). Speech output's request sets none of these flags and therefore classifies `ROUTINE_INTERACTION`. **No generic live Sentinel `REVIEW`-resolution mechanism exists in this codebase today** (Codex design-review finding, folded in) - the Personal Memory `memory.propose`/`approve`/`deny` consent workflow is a distinct, purpose-specific mechanism, not a general Sentinel `REVIEW`-fulfilment path an Adult/Administrator could use to satisfy this capability's escalation. Setting `requires_approval=True` on a per-request basis would therefore make that request permanently unreachable, not merely gated, which shapes this package's design decision below. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 | "This role model governs who may direct or approve a Guardian action... the role model determines who may satisfy a `REVIEW` escalation, not whether one is required." Section 8.4 (Pre-Approved Emergency Actions) establishes the codebase's one existing precedent for converting a live, in-the-moment approval requirement into an Administrator-authored-in-advance decision: "explicitly authored and signed off by an Administrator-role user, in advance, as a named policy record - never inferred, defaulted, or granted by an AI judgement call at the moment." This package's design (Section 5.2) follows that same shape for a different capability. |
| `jarvis/interfaces/stdio_rpc.py` `PIPER_VOICE_PATH_ENV_VAR` / `_build_speech_provider()` | Absent/blank env var returns `None` (honest `not_connected`, no auto-download); present constructs the provider and wraps it in `SentinelGatedSpeechProvider`, reusing the single shared `gateway` instance also used for conversation and memory. This package's `_build_transcription_provider()` mirrors this exactly. |
| `jarvis/guardian/runtime.py` `GuardianRuntime.converse(message: str)` (line 160) | Takes a plain string; a transcript produced by this package is passed to the existing `send_message`/`guardian.converse` path unchanged - **no new conversation entry point is created**, matching the research finding that speech output already consumes Guardian's own already-generated text rather than opening a new one. |
| `src-tauri/src/lib.rs` `send_message`/`speak_message` (lines 473, 487) | Thin `#[tauri::command]` wrappers around a shared `call_backend` helper. `transcribe_audio` (new) follows this exact shape. |
| `src/App.jsx` speak button (lines ~486-495, ~680) | Established pattern for a per-action button that calls a Tauri command, decodes a result, and surfaces a non-blocking inline error note rather than a blocking modal - this package's microphone button follows the same shape for the input direction. |
| `pyproject.toml` | Runtime dependencies are `psutil` and `piper-tts` only (line 6-9) - no STT package (`whisper`, `faster-whisper`, `vosk`, `speech_recognition`) present anywhere in the repository today; no STT vendor decision has been pre-made by any prior package. `src-tauri/Cargo.toml` and `package.json` likewise have no audio-capture dependency today. |
| `tests/e2e/app.spec.js` `mockTauriIpc()` | Established pattern for stubbing `window.__TAURI_INTERNALS__.invoke` per command in Playwright, used for `speak_message`'s tests - this package's `transcribe_audio` tests follow the same pattern, using a small fixture audio buffer rather than real microphone hardware (no e2e test can exercise real hardware; matches Increment A's own disclosed limitation). |

---

# 5. Scope

## 5.1 STT Provider Selection

**Proposed**: `faster-whisper` (CTranslate2-based, MIT-licensed, self-hosted, no API key or recurring cost - same "self-hosted default" reasoning already applied when Piper was chosen over ElevenLabs at EBG-0112, and when Kokoro's ONNX build was preferred over its PyTorch build at EBG-0115), using the `tiny.en` or `base.en` English-only model (small download, CPU-viable, no GPU required) as the first-increment default - mirroring Piper's own "smallest/fastest quality tier first" precedent (EBG-0112 Increment A shipped `en_US-lessac-medium`, not the largest available voice).

This is a proposal for Engineering Reviewer and Programme Sponsor scrutiny, not a pre-decided fact like Piper's already-shipped choice - flagged explicitly as a genuine open design point this package's review should confirm or redirect, per RSC-0001/EIP-ESR0040-001's own instruction that a future Increment B package "would need to name and evaluate STT providers on its own merits."

## 5.2 Sentinel Gating Design Decision

Per Section 4's finding that no generic live Sentinel `REVIEW`-resolution mechanism exists, and drawing on GAM-0001 Section 8.4's pre-approved-emergency-action pattern **by analogy, not as an equivalent mechanism** (Codex design-review finding, folded in - Section 8.4 governs a named, Administrator-authored, signed policy record; an environment variable is neither role-authenticated nor recorded as a policy decision):

- **Capability enablement, not role-authenticated approval, is this package's gate.** Speech input is entirely absent (the microphone button does not render, `guardian.transcribe` is unreachable) unless a new environment variable, `JARVIS_WHISPER_MODEL_PATH`, is explicitly set on the household's own desktop - mirroring `JARVIS_PIPER_VOICE_PATH`'s existing absent-means-invisible pattern exactly. This is a deliberate, host-level configuration act, uses the same advance-authorisation *pattern* as GAM-0001 Section 8.4 by analogy, and is treated here as an **operational assumption** that whoever sets up the desktop installation is exercising Administrator-level judgement - it is not role-authenticated, signed, or enforced as a policy record, and this package does not claim otherwise.
- **Once enabled, individual transcription requests are audited but not blocked**, matching speech output's own precedent exactly: `SentinelRequest(source="jarvis.guardian.voice", intent="speech.transcribe", metadata={"capability": "speech-transcription"})`, no `requires_approval` flag set, classifying `ROUTINE_INTERACTION`/`ALLOW` under `TrustTierPolicy` - logged through the same Sentinel audit trail as every other request, not exempt from it.
- **This does not satisfy GAM-0001 Section 8.1's Household Role Model enforcement** (Codex design-review finding, folded in) - it is a temporary, bounded capability-enablement gate, not a substitute for role-authenticated approval; Section 8 exclusion 8 states this explicitly. This is a genuine design decision, not a mechanical copy of Increment A's pattern - flagged explicitly in this section for Engineering Reviewer and Programme Sponsor sign-off, since GAM-0001 Section 8.1 is what raises the concern this decision is answering.

## 5.3 Backend

1. `sentinel/transcription_providers.py` (new): `TranscriptionRequest` (`audio_bytes: bytes`, `mime_type: str`), `TranscriptionResponse` (`provider_name: str`, `text: str`, `metadata: dict`), `TranscriptionProvider` Protocol (`name`, `transcribe(request) -> TranscriptionResponse`), `execute_transcription_with_sentinel_decision()` - mirroring `speech_providers.py`'s shape exactly, for the opposite data direction.
2. `sentinel/whisper_provider.py` (new): `WhisperProvider` - lazy `import faster_whisper` inside a `_load_model()` method (never top-level); `ProviderConfiguration.endpoint` carries the local model path/size identifier (e.g. `"base.en"`); eager construction-time failure (`RuntimeError`) on load failure, matching `PiperProvider`'s pattern.
3. `jarvis/interfaces/voice.py`: add `TranscriptionOutcome` (frozen dataclass mirroring `SpeechOutcome`'s shape: `status` plus optional `text`/`message`, with the same `__post_init__` invariant style - a `transcribed` status requires `text`, others must not carry it) and `STATUS_TRANSCRIBED`/`STATUS_NOT_CONNECTED`/`STATUS_NOT_RUNNING`/`STATUS_DENIED`/`STATUS_UNAVAILABLE` constants alongside the existing speech-output ones. `SentinelGatedTranscriptionProvider.transcribe(audio_bytes, mime_type)` mirrors `SentinelGatedSpeechProvider.synthesize()` line-for-line for the opposite direction (Section 5.2's Sentinel request shape, `RuntimeError` mapped to `STATUS_UNAVAILABLE`, denial reason not surfaced per the established pattern).
4. `jarvis/guardian/runtime.py`: new `GuardianRuntime.transcribe(audio_bytes: bytes, mime_type: str) -> TranscriptionOutcome`, mirroring `speak()`'s existing provider-connected/runtime-RUNNING boundary checks (lines 189-209) exactly.
5. `jarvis/interfaces/stdio_rpc.py`: `WHISPER_MODEL_PATH_ENV_VAR = "JARVIS_WHISPER_MODEL_PATH"`; `_build_transcription_provider()` mirrors `_build_speech_provider()` exactly (absent/blank env var returns `None`, present constructs `WhisperProvider` wrapped in `SentinelGatedTranscriptionProvider`, reusing the single shared `gateway` instance). New `"guardian.transcribe"` RPC method entry; `_guardian_transcribe(params)` reads `params["audioBase64"]`/`params["mimeType"]`, decodes, calls `runtime.transcribe(...)`, serializes the `TranscriptionOutcome` (never including audio back, only `status`/`text`/`message`).
6. `pyproject.toml`: add `faster-whisper` to `dependencies`, matching `piper-tts`'s existing version-pinning style (`>=X,<Y`).

## 5.4 Tauri Bridge (`src-tauri/src/lib.rs`)

7. Add `transcribe_audio(state, app_handle, audio_base64: String, mime_type: String)`, a thin `#[tauri::command]` wrapper calling `call_backend(..., "guardian.transcribe", json!({"audioBase64": audio_base64, "mimeType": mime_type}))`, byte-for-byte the same shape as `speak_message`. Registered in the existing `tauri::generate_handler![...]` list.
8. **Investigate and disclose at implementation time** whether the Tauri webview's default capability set permits `navigator.mediaDevices.getUserMedia` (microphone access) without an explicit entry in `src-tauri/capabilities/` or `tauri.conf.json` - this was not confirmed during this package's research and is not assumed; if a permission/capability declaration is required, it is authorised as part of this package's scope (Section 6) even though the exact file was not identified in advance.

## 5.5 Frontend (`src/App.jsx`, `src/styles.css`)

9. A push-to-talk microphone button in the message composer (not a wake-word/continuous-listening control - explicitly excluded, Section 8): mouse-down/touch-start begins recording via the browser `MediaRecorder` API (bounded to a maximum 30 seconds, auto-stopping and transcribing at that limit as a safety bound rather than an unbounded capture), mouse-up/touch-end stops recording and immediately calls `transcribe_audio` with the base64-encoded captured audio.
10. On a `transcribed` outcome, the returned text populates the existing message-composer text input - **the household member must still press Send themselves**; this package does not auto-submit a transcript, so a mis-transcription is always reviewable/editable before it reaches Guardian, matching this package's general preference for an extra human-in-the-loop step over speed.
11. On any other outcome (`not_connected`, `denied`, `unavailable`, or a `getUserMedia` permission failure), a small, non-blocking inline note appears near the microphone button, matching `speak_message`'s established frontend error-handling pattern (EIP-ESR0044-001 Section 5.3 item 11) - never a blocking modal, never a silent failure.
12. If `JARVIS_WHISPER_MODEL_PATH` is unset (backend reports `not_connected` on first probe, or the microphone button is simply omitted client-side once the RPC layer signals the capability is absent - exact mechanism confirmed at implementation time, mirroring however the speak button already handles this for output), the microphone button does not render at all, rather than rendering and failing on every use.

## 5.6 Tests

13. New `jarvis/tests/test_transcription_providers.py`/`test_whisper_provider.py`/extended `test_voice_interface.py`: mirroring the existing `test_speech_providers.py`/`test_piper_provider.py`/`test_voice_interface.py` structure and fake-seam conventions exactly, for the opposite data direction.
14. Extend `jarvis/tests/test_stdio_rpc.py`: a `_FakeWhisperProvider` patched the same way `_FakePiperProvider` is (absent-env-var to `not_connected`, present-env-var to wired-and-`transcribed`, and a "reuses the same gateway" identity test).
15. Extend `src-tauri`'s existing test module with a `transcribe_audio` test mirroring `speak_message`'s own proportionate thinness.
16. Extend `tests/e2e/app.spec.js`: mocks `transcribe_audio` via `mockTauriIpc()`, confirms the transcribed-text-populates-composer path and the inline-error path, using a small fixture audio buffer (no real microphone hardware, matching Increment A's own disclosed e2e limitation for real audio playback).

---

# 6. Authorised Files

1. `sentinel/transcription_providers.py` (new)
2. `sentinel/whisper_provider.py` (new)
3. `jarvis/tests/test_transcription_providers.py` (new)
4. `jarvis/tests/test_whisper_provider.py` (new)
5. `jarvis/interfaces/voice.py`
6. `jarvis/tests/test_voice_interface.py`
7. `jarvis/guardian/runtime.py`
8. `jarvis/tests/test_guardian_runtime.py` (or equivalent existing runtime test module - exact filename confirmed at implementation time)
9. `jarvis/interfaces/stdio_rpc.py`
10. `jarvis/tests/test_stdio_rpc.py`
11. `pyproject.toml`
12. `src-tauri/src/lib.rs`
13. `src-tauri/capabilities/` and/or `src-tauri/tauri.conf.json` - anticipated per Section 5.4 item 8's disclosed uncertainty; confirmed and disclosed at implementation if actually touched, matching the disclosed-dependency precedent from EIP-ESR0046-001 Section 6 item 15.
14. `src/App.jsx`
15. `src/styles.css`
16. `tests/e2e/app.spec.js`
17. `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` - recording this package's Section 5.2 gating decision against Section 8.1/8.4.
18. `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md` - recording the Voice faculty's Increment B (speech input) as implemented, mirroring EIP-ESR0040-001's own Section 6 item 8 update for Increment A.
19. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
20. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
21. `aiems/governance/baselines/LGB-0001_LAUNCH_GAP_BACKLOG.md` - per its own Section 8 maintenance rule.

No other file is authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `TranscriptionOutcome` invariants enforced at the dataclass level (`__post_init__`), matching `SpeechOutcome`'s existing pattern exactly.
2. `WhisperProvider` must lazy-import `faster_whisper` only inside its model-loading method, never at module top level, matching `PiperProvider`'s existing fake-seam-friendly pattern.
3. No audio is ever persisted to disk or to the Personal Memory store by this package - a transcription request's `audio_bytes` exist only in-memory for the duration of the RPC call; only the resulting text (already subject to the household member's own Send/don't-Send decision) can ever reach any persistent store, and only via the pre-existing `guardian.converse`/Personal Memory path, unchanged by this package.
4. The microphone recording bound (30 seconds, Section 5.5 item 9) is a hard client-side cap, not merely a UI suggestion - `MediaRecorder` is explicitly stopped at that limit.
5. No wake-word detection, continuous/always-listening capture, or background audio monitoring of any kind - see Section 8 exclusion 1.
6. Rust changes must pass `cargo check`/`cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check` before being considered complete.

---

# 8. Explicit Exclusions

This package does not authorise:

1. **Wake-word detection, continuous listening, or any background/always-on microphone capture.** Push-to-talk only - the microphone is never active except while the button is explicitly held/engaged. A continuous-listening capability is a materially larger privacy/governance surface than this package's scope and would need its own dedicated future session, per the same judgement already applied to Increment A/Vision.
2. **Any speaker identification or attribution of a transcript to a specific household profile.** A transcript is placed into the composer as anonymous text; EIP-ESR0046-001's User Identity and Profile Foundation exists but is not wired into this package - who is speaking is not inferred or recorded. A future package could combine the two, but this one deliberately does not.
3. **Any live, per-request `REVIEW`-resolution UI or mechanism.** Section 5.2's design decision routes around this gap rather than building it - building a general Sentinel `REVIEW`-satisfaction mechanism is a distinct, larger piece of work this package does not attempt.
4. **Auto-submitting a transcript to Guardian.** The household member must press Send themselves (Section 5.5 item 10) - this package does not add a "transcribe and immediately converse" shortcut.
5. **Any cloud/paid STT provider** (Deepgram or otherwise) - `faster-whisper` only, per Section 5.1's self-hosted rationale; a cloud alternative remains a possible future option behind the same `TranscriptionProvider` Protocol, not part of this package.
6. **Multi-language support beyond English.** `base.en`/`tiny.en` are English-only models, matching Piper's own `en_US`-only first increment.
7. **Vision (Increment C).** Unrelated capability, separately deferred since EIP-ESR0040-001.
8. **Enforcement of GAM-0001 Section 8.1's role differences beyond the enablement gate in Section 5.2** - a Child-role or Guest-role household member using an already-enabled microphone is not distinguished from an Adult/Administrator by this package, since speaker identification itself is excluded (item 2 above).

---

# 9. Constraints

1. No file change shall be made until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template.
3. Section 5.1 (STT provider choice) and Section 5.2 (Sentinel gating design) are flagged as genuine open decisions for the Engineering Reviewer and Programme Sponsor to confirm, redirect, or reject - not settled facts this package assumes will pass review unchanged.

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

1. Full pytest suite passes, including new transcription-provider/Whisper-provider/voice-interface/stdio_rpc/runtime test cases, with no regression.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. Rust build/clippy/fmt/test all pass cleanly.
4. Playwright suite passes, including the new/extended microphone-button spec.
5. **A genuine live smoke check where practical**: a real short utterance recorded and transcribed through the actual RPC/storage layer (a real `faster-whisper` model, a real `GuardianRuntime`, real JSON-RPC dispatch, no mocks) - matching Increment A's own live-smoke-check discipline. **Disclosed in advance, matching EIP-ESR0046-001's own precedent**: a literal native-window microphone click-through in the real Tauri desktop shell may not be performable in this implementation environment (no confirmed audio-input-capable automation path here); if so, this will be disclosed honestly at completion, and the Programme Sponsor's own live test (mirroring EBG-0112/EBG-0113's precedent of the Sponsor personally verifying Guardian's voice) would be the genuine end-user validation step for the microphone path specifically.
6. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

1. `faster-whisper` (new runtime dependency) - self-hosted, no API key, no recurring cost; adds a CTranslate2-based inference runtime alongside Piper's existing ONNX runtime dependency. Model download (`tiny.en`/`base.en`) happens once, locally, via `faster-whisper`'s own model-fetch mechanism (mirroring how Piper's `download_voices` CLI was used at EBG-0112/EBG-0113) - confirmed and disclosed at implementation time.
2. Tauri webview microphone permission (Section 5.4 item 8) - genuinely unconfirmed until implementation; disclosed as a real risk rather than assumed to work.

## Risks

1. **Section 5.1's STT choice is unverified against real transcription accuracy for this household's actual voices/accents/room acoustics** - `tiny.en`/`base.en` are the smallest, fastest, least accurate tier of Whisper models; if accuracy proves poor in the Programme Sponsor's own live test, a follow-on package would need to evaluate a larger model or a different engine, at a size/latency cost. Disclosed upfront rather than assumed adequate.
2. **Section 5.2's gating design is a genuine judgement call, not an obviously-correct mechanical mirror of Increment A** - it is defensible against GAM-0001 Section 8.1/8.4's existing text, but it is this package's own interpretation, not a pre-existing rule the codebase already stated. Flagged explicitly for review rather than presented as settled.
3. **Tauri webview microphone access may require a capability/permission declaration not yet identified** (Section 5.4 item 8) - could expand this package's actual file-change footprint slightly beyond what Section 6 lists by name (already anticipated and pre-authorised there), or could surface as a genuine implementation blocker requiring a return to the Engineering Reviewer/Programme Sponsor if the fix is non-trivial.
4. **Bounded push-to-talk recording (30s cap) may prove too short or too long in practice** - a tunable constant, not hard-coded without a named identifier, so a future adjustment is a one-line change rather than a re-scope.

## New Backlog Item Registered by This Draft

None anticipated. This package directly implements EBG-0117 as scoped by its own registration text; Vision (Increment C) and any speaker-identity/profile-scoping follow-on remain pre-existing, separately-tracked future items rather than new discoveries.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation. **Result: Pass with non-blocking findings.** Codex independently verified every Section 4 Repository Context claim against the live cited files (`sentinel/speech_providers.py`, `sentinel/piper_provider.py`, `jarvis/interfaces/voice.py`, `sentinel/policy.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/guardian/runtime.py`, `src-tauri/src/lib.rs`, `pyproject.toml`, GAM-0001 Sections 8.1/8.4, EIP-ESR0040-001) as materially accurate, confirmed the package stays within EBG-0117's now-selected scope, assessed Section 5.1's `faster-whisper` proposal as reasonable and correctly framed as a proposal rather than a settled fact, and assessed Section 8's exclusions as the right blast-radius boundary for a first increment. Three non-blocking wording findings on Section 5.2's GAM-0001 Section 8.4 analogy and Section 4's "no live mechanism" phrasing - folded into v0.2 (see Section 4 and Section 5.2 above). No blocking design defect found.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (ESR-0047/WP3) before implementation began.

**Implemented as scoped, with one post-commit correction** - see Version History v1.1 below. Full detail, evidence and validation results recorded in [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] Section 6C/6E.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0117 (this package's parent item, to be marked Complete on approval and implementation). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Must-Ship item this package delivers; to be refreshed per its own Section 8 maintenance rule. |
| [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] | Scored the Basic Voice Input gap this package resolves. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.1 Household Role Model and Section 8.4 Pre-Approved Emergency Actions - both directly inform this package's Section 5.2 gating design. |
| [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] | Increment A (speech output), whose pattern this package mirrors for the opposite data direction and whose Section 8 explicitly deferred this package's scope. |
| [[EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION|EIP-ESR0046-001]] | User Identity and Profile Foundation - deliberately not wired into this package (Section 8 exclusion 2), a possible future combination. |
| [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Operational Verification Before Reporting discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 4 August 2026 | Claude Engineering Implementer | **Session-wide WP6 (Engineering Reviewer, Codex) finding, addressed.** The initial implementation never actually satisfied Section 5.5 item 12: the microphone button always rendered and `getUserMedia`/`MediaRecorder` always started before the backend's `not_connected` outcome was known - a real scope/privacy-gating mismatch, not merely wording, since Increment A's speech output never activates local hardware the way an unconfigured microphone button would. Fixed: `GuardianRuntime.transcription_available` (new property) and a new `transcriptionAvailable` field on `platform.status` let the frontend learn availability in advance; the mic button now conditionally renders only when true. 2 new tests (`test_guardian_runtime.py`, `test_stdio_rpc.py`) plus a new Playwright test asserting the button's absence by default. Full suite: 485 passed/1 skipped (was 483/1); Playwright 12/12 (was 11). |
| 1.0 | 4 August 2026 | Claude Engineering Implementer | **Implemented as scoped**, Programme Sponsor approval verified via the real Sponsor Approval Service (ESR-0047/WP3). Backend (`sentinel/transcription_providers.py`, `sentinel/whisper_provider.py`, `jarvis/interfaces/voice.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`), Tauri (`transcribe_audio` command) and frontend (push-to-talk mic button, `src/App.jsx`/`styles.css`) delivered exactly as scoped. One disclosed implementation refinement: push-to-talk implemented as click-to-start/click-to-stop rather than literal mouse-down/mouse-up hold (Section 5.5 item 9), for reliability - true hold-based capture risks losing the stop event if the cursor leaves the button before release; both remain a single, deliberate, bounded (30s max) user action, not continuous/wake-word listening. Full validation clean: 483 Python tests passed/1 skipped (was 453/1, 30 new), ruff clean; Rust build/clippy/fmt/test clean; frontend build clean; Playwright 11/11 passed (2 new). |
| 0.2 | 4 August 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: **Pass with non-blocking findings.** Every Repository Context claim independently verified against live cited files; scope confirmed within EBG-0117's authority; Section 5.1 STT proposal and Section 8 exclusions assessed as reasonable. Folded three non-blocking findings: softened Section 5.2's GAM-0001 Section 8.4 analogy from "follows that same shape" to an explicit by-analogy/operational-assumption framing, added an explicit statement that the enablement gate does not satisfy Household Role Model enforcement, and tightened Section 4's "no live mechanism exists anywhere" to "no generic live Sentinel REVIEW-resolution mechanism exists" (distinguishing the Personal Memory consent workflow). Awaiting Programme Sponsor approval. |
| 0.1 | 4 August 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0047 WP3. Scopes Voice Faculty Phase 6 Increment B (push-to-talk speech input via a self-hosted `faster-whisper` provider), with an explicit Sentinel-gating design decision (Section 5.2) grounded in GAM-0001 Section 8.1/8.4 rather than mechanically copying Increment A's pattern. Not yet reviewed or approved. |
