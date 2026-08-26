# EIP-ESR0052-002 - Kokoro TTS Live Comparison (EBG-0115)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0052-002 |
| Title | Engineering Implementation Package: WP3 Kokoro TTS Live Comparison |
| Version | 1.0 |
| Status | Approved - implemented (comparison performed; final EBG-0115 disposition awaits the Programme Sponsor's listening verdict) |
| Session | ESR-0052 |
| Work Package | WP3 |

---

# 2. Purpose

Implements ESR-0052 WP3: EBG-0115 (evaluate Kokoro TTS as a materially more expressive alternative to Piper, the current self-hosted Guardian voice engine). Selected by the Programme Sponsor as this session's product-moving objective, resolving the Feature-First Delivery Discipline gap flagged at WP1/WP2 (neither a drafted process cluster nor a Composio non-adoption decision ships a JARVIS capability; this package can, if the comparison favours adoption).

Produces a genuine live side-by-side listening comparison for the Programme Sponsor's own verdict - mirroring EBG-0113's exact methodology ([[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]]), which itself produced an honest negative result (`lessac-high` indistinguishable from `lessac-medium`) rather than an assumed improvement. This package makes no assumption about Kokoro's outcome either way.

---

# 3. Repository Context Investigated

* `sentinel/piper_provider.py`: `PiperProvider(configuration, synthesizer=None)` - lazy `import piper` localised inside `_load_synthesizer()` (never at module top level, so tests never pay the import cost), a `VoiceSynthesizer = Callable[[str], bytes]` seam for test injection, `synthesize()` returning `SpeechSynthesisResponse` (`sentinel/speech_providers.py`'s shared contract) with `provider_name`/`audio_bytes`/`mime_type`/`metadata`. `ProviderConfiguration.endpoint` carries the local model path.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0115's own entry: an ONNX-runtime build of Kokoro exists (`kokoro-onnx` on PyPI, same runtime family Piper already depends on, not the heavier PyTorch stack originally compared against at EBG-0112). Confirmed resource profile: ~80 MB quantized model, ~1.5-2 GB peak RAM during synthesis, 5-20x real-time CPU inference, no GPU required; additionally depends on an `espeak-ng`-based phonemizer (`espeakng-loader`, `phonemizer-fork`) Piper does not need.
* EBG-0113's exact live-comparison methodology ([[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]]): an uncommitted comparison script (not added to the repository), an uncommitted local model directory (`.voice-models-local/`, deleted after the comparison), the identical fixed test utterance "Hello Robert. This is Guardian. If you can hear this, speech output is working correctly." synthesized through the real provider for each candidate, two genuine `.wav` files written to the Programme Sponsor's own Desktop, and an honest verdict recorded either way - the Programme Sponsor personally reported no perceptible difference for `lessac-high`, which was accepted and recorded as a negative result rather than second-guessed.
* `pyproject.toml`: current `dependencies` (`psutil`, `piper-tts`, `faster-whisper`) and `[project.optional-dependencies] dev`. No existing "evaluation-only" dependency group.

---

# 4. Scope

## 4A. New Optional Dependency Group

A new `[project.optional-dependencies] voice-eval` group in `pyproject.toml`: `kokoro-onnx`, `espeakng-loader`, `phonemizer-fork` (exact version pins confirmed against PyPI at implementation time). Kept out of the base `dependencies` list and out of `dev` - these packages exist to make the comparison possible, not to become a permanent runtime dependency unless the comparison favours adoption.

## 4B. New `sentinel/kokoro_provider.py`

A `KokoroProvider` class mirroring `PiperProvider`'s contract exactly, spelled out explicitly (Codex design-review correction) rather than left as an unverifiable "mirrors Piper" claim:

* Same constructor shape: `ProviderConfiguration` plus an optional injectable synthesizer callable, `configuration.endpoint` validated as required (raising `ValueError` if absent, matching `PiperProvider.__init__`'s own check).
* `name` property returning `self._configuration.provider_name`.
* Real-engine loading (`kokoro_onnx`) localised inside a `_load_synthesizer()`-shaped function, never imported at module top level, so no test pays the import/model-load cost unless it actually constructs a real provider - identical to `PiperProvider`'s own `_load_synthesizer()` pattern.
* The same `VoiceSynthesizer = Callable[[str], bytes]` test-injection seam.
* `synthesize()` returning `SpeechSynthesisResponse` with `mime_type="audio/wav"`, non-empty-audio validation (`RuntimeError` if the engine returns empty bytes), synthesis failures wrapped in `RuntimeError` (not left as a raw exception type), and `metadata` carrying the model path sourced from `configuration.endpoint` - matching `PiperProvider.synthesize()`'s exact response-construction and error-handling shape, unless a genuine Kokoro-specific reason to deviate is found and disclosed during implementation.

Real, working code - but **not registered in `sentinel/provider_config.py`'s production provider-selection wiring, and not reachable from any RPC or UXP path.** Constructible and testable directly only, exactly matching EBG-0115's own register entry's scope boundary.

## 4C. New Tests

`jarvis/tests/test_kokoro_provider.py`, mirroring `test_piper_provider.py`'s existing pattern: a fake injected synthesizer callable, asserting `KokoroProvider`'s construction/validation/response-shape behaviour without importing the real `kokoro_onnx` package.

## 4D. Live Comparison (after approval-to-implement only)

An uncommitted comparison script (not added to the repository, matching EBG-0113's own precedent) constructs the existing `PiperProvider` (`en_US-lessac-medium`, the current production voice) and the new `KokoroProvider`, synthesizes the **identical** fixed test utterance used at EBG-0113 ("Hello Robert. This is Guardian. If you can hear this, speech output is working correctly.") through each, and writes two genuine `.wav` files to the Programme Sponsor's Desktop. Any downloaded Kokoro model file is kept in an uncommitted local directory and deleted after the comparison, matching EBG-0113's exact hygiene.

**No adoption decision is made by this package.** The Programme Sponsor's own listening verdict determines whether EBG-0115 closes Complete (Kokoro adopted, follow-on wiring work scoped separately) or as an honest negative result (Piper retained), mirroring EBG-0113's own precedent of accepting a negative result rather than assuming improvement from spec sheets alone.

---

# 5. Validation

* `python -m pytest jarvis/tests sentinel scripts/tests` - new `KokoroProvider` tests pass; existing count otherwise unchanged (no other production code touched).
* `python scripts/validate_repository.py` (full mode).
* Live comparison (4D) produces two genuine, audible `.wav` files on the Programme Sponsor's Desktop; the Programme Sponsor's own verbatim listening verdict is recorded in EBG-0115's EBR-0001 entry, honestly, regardless of outcome.

---

# 6. Explicitly Excluded

* Any `sentinel/provider_config.py` production wiring, new RPC method, or UXP surface change **for Kokoro specifically** - this package produces a constructible-and-testable adapter only, not a reachable Guardian capability. (Correction, Codex design review: this does not mean no speech RPC/UXP surface exists at all - Piper's speech output is already live-wired via `guardian.speak`/`speak_message` since EBG-0114/ESR-0044. This exclusion is narrower: no *new or changed* RPC/UXP exposure, and no `provider_config.py` change, as a result of Kokoro's addition.)
* Any decision to replace or retain Piper - deferred entirely to the Programme Sponsor's listening verdict.
* Any change to Sentinel's trust-gate or policy code (`sentinel/policy.py`, `sentinel/core.py`).
* Any change to the base runtime dependency list - Kokoro's dependencies land only in the new `voice-eval` optional group.
* Committing the comparison script or any downloaded model file to the repository.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0052`/`WP3`). **Verdict: Conditional Pass with corrections**, timestamp 2026-08-26T08:46:39Z. Codex independently confirmed `sentinel/piper_provider.py`'s real contract (constructor validation, `name` property, `_load_synthesizer()` lazy import, `Callable[[str], bytes]` seam, `SpeechSynthesisResponse` shape with `audio/wav` MIME and `model_path` metadata) and `speech_providers.py`'s provider-neutral request/response contract; confirmed `pyproject.toml`'s current base dependencies (`psutil`, `piper-tts`, `faster-whisper`, `dev`-only optional group) make a new `voice-eval` optional group correctly non-runtime scope; confirmed `sentinel/kokoro_provider.py` does not yet exist, matching design-draft-only status; confirmed EIP-ESR0042-001 supports the claimed EBG-0113 live-comparison precedent (identical utterance, real provider call path, Desktop `.wav` outputs, uncommitted local model files, honest negative Sponsor verdict); confirmed EBR-0001/REG-0001 registration entries internally consistent. **Two required corrections, both folded into v0.2 above:** (1) Section 6's exclusion wording could be read as implying no speech RPC/UXP surface exists at all, when Piper's speech output has been live-wired via `guardian.speak`/`speak_message` since EBG-0114/ESR-0044 - narrowed to exclude only *new or changed* RPC/UXP exposure and `provider_config.py` wiring *for Kokoro specifically*. (2) Section 4B's "mirrors PiperProvider's contract" claim was too vague to verify or hold accountable at implementation time - spelled out explicitly (endpoint validation, `name` property, lazy-import pattern, test seam, MIME type, non-empty-audio/`RuntimeError` handling, response metadata).

---

# 8. Implementation Record

**Implemented exactly as scoped in v0.2**, approval-to-implement verified via the real Sponsor Approval Service (`submit-response`, ESR-0052/WP3) before any code was written.

* New optional `voice-eval` dependency group added to `pyproject.toml` (`kokoro-onnx>=0.6.1,<1.0`, `espeakng-loader>=0.2.4,<1.0`, `phonemizer-fork>=3.3.2,<4.0`, exact current PyPI versions confirmed at implementation time) - not in `dependencies` or `dev`.
* New `sentinel/kokoro_provider.py` (`KokoroProvider`), implemented per the explicit contract spelled out in Section 4B, plus one implementation-time addition disclosed here rather than silently added: `_load_synthesizer()` also wires `espeakng_loader.make_library_available()` and passes an `EspeakConfig` (library/data paths) into `Kokoro(...)` - without it, construction succeeds but real synthesis fails the moment phonemizer looks for a system `espeak-ng` install this self-hosted-first machine does not have. `espeakng_loader` (already in the `voice-eval` group) ships the actual binary/data, so this is required wiring, not a new dependency.
* New `jarvis/tests/test_kokoro_provider.py` (7 tests, mirroring `test_piper_provider.py` exactly, injected-synthesizer seam throughout - `python -m pytest jarvis/tests/test_kokoro_provider.py` passes standalone with no real `kokoro_onnx` import).
* **Live comparison performed exactly as scoped.** `en_US-lessac-medium` (the current production Piper voice) downloaded via `piper-tts`'s own `python -m piper.download_voices` CLI; Kokoro's `kokoro-v1.0.int8.onnx` (88 MB, the quantized variant matching EBG-0115's original ~80 MB resource-profile research) and `voices-v1.0.bin` downloaded directly from the upstream GitHub release - all three files to a local, uncommitted `.voice-models-local/` directory, confirmed via `git status` to never enter the repository and deleted after the comparison. An uncommitted comparison script (also never committed, deleted after use) constructed the real `PiperProvider` and the real `KokoroProvider` and synthesized the identical fixed test utterance ("Hello Robert. This is Guardian. If you can hear this, speech output is working correctly.") through each - both succeeded genuinely (Piper: 223,788 bytes; Kokoro: 255,020 bytes, voice `af_sarah`) - producing two real `.wav` files (`guardian-voice-piper-lessac-medium.wav`, `guardian-voice-kokoro-af_sarah.wav`) written to the Programme Sponsor's actual Desktop (OneDrive-redirected path, confirmed live rather than assumed).
* **No adoption decision made by this package**, per Section 4D. The Programme Sponsor's own listening verdict, once given, determines EBG-0115's final disposition in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (Complete/adopted, with follow-on wiring scoped separately, or an honest negative result matching EBG-0113's own precedent).

Validation: `python -m pytest jarvis/tests sentinel scripts/tests` - 530 passed, 1 skipped (up from 523/1 - the 7 new `KokoroProvider` tests, no other production code touched); `python scripts/validate_repository.py` (full mode) - 0 errors, 297 warnings.

---

# 9. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0115, this package's target item.
* [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] - EBG-0113's live-comparison methodology, mirrored exactly by Section 4D.
* [[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]] - independently corroborated Kokoro as best-in-class open, self-hosted TTS via live web search (Section 5), reinforcing EBG-0115's own prior research.
* [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] - this session's report, WP3.
* `sentinel/piper_provider.py` - the exact contract shape `KokoroProvider` mirrors.
