# EIP-ESR0053-002 - Kokoro Production Voice Wiring (EBG-0125)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0053-002 |
| Title | Engineering Implementation Package: WP2 Kokoro Production Voice Wiring |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0053 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0053 WP2: resolves EBG-0125 by wiring the already-built, already-tested `KokoroProvider` (`sentinel/kokoro_provider.py`, EIP-ESR0052-002) into Guardian's production speech-output path, replacing Piper.

Two decisions were made directly by the Programme Sponsor ahead of this package, following a real live listening comparison performed at WP0 of this WP (four genuine `.wav` files, Kokoro's four confirmed UK English voices, synthesized through the real `KokoroProvider` and delivered to the Programme Sponsor's Desktop, mirroring EBG-0113/EBG-0115's exact precedent methodology):

1. **Voice**: `bm_george` (primary), `bf_isabella` (automatic fallback if primary synthesis fails at runtime).
2. **Provider**: Kokoro **replaces** Piper outright as Guardian's sole production speech-synthesis provider - not a second selectable option.

This package scopes the wiring implementing both decisions.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py`: `_build_speech_provider()` currently constructs a `PiperProvider` gated by `PIPER_VOICE_PATH_ENV_VAR` (`JARVIS_PIPER_VOICE_PATH`) - absent/blank means the capability is not available, mirroring `_build_real_provider()`'s credential-gating pattern. `build_default_runtime()` calls it once and passes the result into `GuardianRuntime`. No other file (`src/`, `src-tauri/`) references Piper by name - confirmed by direct search - so `guardian.speak`'s RPC/UXP surface is already provider-agnostic and needs no change.
* `sentinel/kokoro_provider.py` (current, from EIP-ESR0052-002): `KokoroProvider.__init__` loads a single `Kokoro` engine bound to one fixed `voice` (from `configuration.metadata["voice"]`, default `af_sarah`) at construction time via `_load_synthesizer(model_path, voices_path, voice, lang)`, which returns a `VoiceSynthesizer = Callable[[str], bytes]` closure already bound to that one voice. There is no fallback-voice concept anywhere in the current adapter.
* `jarvis/tests/test_kokoro_provider.py`: exercises the current single-voice `synthesizer` seam (`Callable[[str], bytes]`) exclusively via fake callables, never a real model load.
* `jarvis/tests/test_stdio_rpc.py`: `_FakePiperProvider` and every Piper-path test patches `jarvis.interfaces.stdio_rpc.PiperProvider` and sets `JARVIS_PIPER_VOICE_PATH`.
* `pyproject.toml`: `kokoro-onnx`, `espeakng-loader`, `phonemizer-fork` currently sit in the `voice-eval` optional-dependency group, explicitly scoped as "evaluation-only... not a permanent runtime dependency unless the comparison favours adoption." `piper-tts` is a base `dependencies` entry.
* `git status`: clean; current branch `main`; up to date with `origin/main` as of WP1's push (`248924a`).

---

# 4. Scope by Item

## 4A. `sentinel/kokoro_provider.py`: dual-voice fallback support

The construction-time voice binding is removed in favour of a voice-parameterised synthesizer, so one loaded `Kokoro` engine (the expensive ~90 MB ONNX session load) can serve both the primary and fallback voice without loading the model twice:

* `VoiceSynthesizer` changes from `Callable[[str], bytes]` (text) to `Callable[[str, str], bytes]` (text, voice) - **a disclosed breaking change** to the adapter's internal seam and its test contract (Section 6, Explicit Exclusions covers what does *not* change).
* `_load_synthesizer(model_path, voices_path, lang)` loads the engine once and returns a `(text, voice) -> bytes` closure; `lang` remains fixed per adapter instance (unchanged from today - Kokoro's `engine.create()` call takes both `voice` and `lang` per call, but this package only varies `voice` between primary/fallback, matching the Sponsor's actual decision).
* `KokoroProvider.__init__` reads `configuration.metadata.get("voice", DEFAULT_VOICE)` (unchanged) and a new optional `configuration.metadata.get("fallback_voice")` (default `None` - no fallback unless explicitly configured, so existing single-voice callers are unaffected in behaviour, only in the injected-seam shape).
* `KokoroProvider.synthesize()`: calls the synthesizer with the primary voice; on any exception, if a fallback voice is configured, retries once with the fallback voice before raising; if the fallback also fails (or none is configured), raises `RuntimeError` exactly as today. `SpeechSynthesisResponse.metadata` gains a `voice_used` key (`"bm_george"` or `"bf_isabella"`, whichever actually produced the returned audio) - the Sentinel audit trail should not have to guess which voice a response came from. Both the primary-only and primary-plus-fallback failure paths raise via `raise RuntimeError(msg) from exc`, preserving exception chaining for diagnostics without leaking the wrapped exception's own message text into `msg` - matching the existing single-voice behaviour's own established pattern exactly (Codex design-review guidance, non-blocking).

## 4B. `jarvis/interfaces/stdio_rpc.py`: replace Piper wiring with Kokoro

* `PIPER_VOICE_PATH_ENV_VAR` removed; two new env vars added, mirroring its exact absent-means-invisible pattern: `KOKORO_MODEL_PATH_ENV_VAR = "JARVIS_KOKORO_MODEL_PATH"` and `KOKORO_VOICES_PATH_ENV_VAR = "JARVIS_KOKORO_VOICES_PATH"` - **both** must be present and non-blank for the capability to be available (Kokoro's two-file requirement, already disclosed in `kokoro_provider.py`'s own docstring); either absent/blank means `not_connected`, never a startup failure.
* New module-level constants `KOKORO_VOICE = "bm_george"`, `KOKORO_FALLBACK_VOICE = "bf_isabella"`, `KOKORO_LANG = "en-gb"` - hardcoded, not env-var-configurable in this package (Section 6 disclosed simplification).
* `from sentinel.piper_provider import PiperProvider` removed; `from sentinel.kokoro_provider import KokoroProvider` added. `_build_speech_provider()` rewritten to construct `KokoroProvider(ProviderConfiguration(provider_name="kokoro", endpoint=<model path>, metadata={"voices_path": <voices path>, "voice": KOKORO_VOICE, "fallback_voice": KOKORO_FALLBACK_VOICE, "lang": KOKORO_LANG}))`, still wrapped in the same `SentinelGatedSpeechProvider(gateway=gateway, provider=...)` and still reusing the shared `gateway` instance unchanged.
* `build_default_runtime()`'s docstring updated to describe Kokoro instead of Piper.

## 4C. `pyproject.toml`

* `kokoro-onnx`, `espeakng-loader`, `phonemizer-fork` moved from the `voice-eval` optional group into base `dependencies` - Kokoro is now a real runtime dependency, per EBG-0125's own scoped item 3. The `voice-eval` group is removed entirely (nothing else was in it; its stated evaluation-only purpose is fulfilled).
* `piper-tts` remains a base dependency, unchanged (Section 6).

## 4D. Tests

* `jarvis/tests/test_kokoro_provider.py`: existing tests updated for the two-arg `(text, voice)` synthesizer seam; new tests added for fallback behaviour - primary succeeds (fallback never called); primary fails + fallback configured and succeeds (no exception, `voice_used` reflects the fallback); primary fails + no fallback configured (raises, matching today's existing behaviour exactly); primary and fallback both fail (raises, message does not leak the fallback's own internal exception text either).
* `jarvis/tests/test_stdio_rpc.py`: `_FakePiperProvider` replaced with `_FakeKokoroProvider` (mirroring its exact shape - injectable, no real model load); every Piper-path test's `JARVIS_PIPER_VOICE_PATH` env var and `PiperProvider` patch target replaced with `JARVIS_KOKORO_MODEL_PATH`/`JARVIS_KOKORO_VOICES_PATH` and `KokoroProvider`.

## 4E. `EBR-0001`

EBG-0125's Section 5 row closed `Completed`, Notes extended with an implementation summary and a pointer to this package.

---

# 5. Validation

* `python -m pytest jarvis/tests/test_kokoro_provider.py jarvis/tests/test_stdio_rpc.py` - all existing behavioural assertions preserved (only the seam shape and Piper-to-Kokoro substitution change), plus new fallback-specific tests passing.
* `python -m pytest jarvis/tests sentinel scripts/tests` (full suite) - no other production path touched; count should rise only by the new fallback-behaviour tests added in 4D.
* `python scripts/validate_repository.py` (full mode) - 0 errors expected.
* Live run, mirroring EIP-ESR0044-001's own precedent: with real `JARVIS_KOKORO_MODEL_PATH`/`JARVIS_KOKORO_VOICES_PATH` set (the same model/voices files used for WP0's comparison, re-downloaded and deleted again afterward per the established never-committed pattern), a real `python -m jarvis --ipc-stdio` invocation of `guardian.speak` confirmed to return real `bm_george` audio - not merely that the fake-seam tests pass.

**Actual results:** `python -m pytest jarvis/tests/test_stdio_rpc.py jarvis/tests/test_kokoro_provider.py` - 79 passed. Full suite `python -m pytest jarvis/tests sentinel scripts/tests` - **537 passed, 1 skipped** (up from ESR-0053 WP1's closing 532/1; +5 new tests: 4 fallback-behaviour tests in `test_kokoro_provider.py`, 1 both-paths-required test in `test_stdio_rpc.py`). `python scripts/validate_repository.py` (full mode) - 0 errors, 298 warnings (unchanged). **Live end-to-end verification, real engine not fake seam**: a real `build_default_runtime()` + `runtime.speak()` call against genuinely downloaded model files returned synthesized `bm_george` audio (229,420 bytes, `status: synthesized`, `provider: kokoro`); a second real call with a deliberately invalid primary voice confirmed the automatic fallback genuinely engages against the real Kokoro engine, producing genuine `bf_isabella` audio (65,580 bytes) - not merely that the fallback unit tests pass against a fake seam. Model files never committed, deleted after verification (confirmed via `git status`).

---

# 6. Explicitly Excluded

* Any change to `src/`/`src-tauri/` - the UXP's `guardian.speak` call site is already provider-agnostic, confirmed by direct search, not assumed.
* Any change to `sentinel/piper_provider.py` or `jarvis/tests/test_piper_provider.py` - the module and its own tests remain fully intact and valid, simply unregistered from production (the same posture Kokoro itself held before this package, now reciprocated).
* Removing `piper-tts` from `pyproject.toml`'s base `dependencies` - `PiperProvider` remains constructible/testable, so its real dependency stays available; not asked for by EBG-0125 and not touched here.
* Env-var-configurable voice/fallback-voice/language selection - `KOKORO_VOICE`/`KOKORO_FALLBACK_VOICE`/`KOKORO_LANG` are hardcoded module constants in this package. A future backlog item, not this one, if per-deployment voice configurability is wanted.
* Any change to `sentinel/provider_config.py`'s `ProviderConfigurationRegistry`/text-generation route machinery - speech continues to use the same single-provider-plus-gateway pattern it always has, not the orchestrator/route system text-generation uses.
* Any change to the Whisper/transcription (speech-input) path.
* Any Sentinel policy/trust-tier change.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0053`/`WP2`). **Verdict: Conditional Pass with correction(s)**, timestamp 2026-08-27T21:01Z (approx). Codex independently agreed with all six requested assessments: (1) the `VoiceSynthesizer` seam change is sound and minimal, honestly disclosed, internal to `KokoroProvider` (not a public RPC contract change); (2) the fallback semantics are acceptable for a production speech-output path, with non-blocking guidance to preserve exception chaining and avoid leaking raw internals - folded into Section 4A above; (3) replacing Piper wiring outright while leaving `sentinel/piper_provider.py` fully untouched is the correct scope boundary given the Sponsor's explicit decision; (4) the `pyproject.toml` dependency move is correctly scoped against EBG-0125's own text, with a note that keeping `piper-tts` in base is not a blocker provided the package does not overstate Kokoro as the sole installed speech stack (it does not - Section 6 discloses this explicitly); (5) the "no `src/`/`src-tauri/` change needed" claim is adequately verified via direct repository search, not assumed; (6) REG-0001/WikiLink hygiene found clean. **Required correction, folded in before seeking approval:** EBG-0125's own `EBR-0001` Section 5 row still read "No implementation, provider selection or voice choice is authorised by this entry," stale relative to the Programme Sponsor's actual decision recorded in this session - corrected with a dated authorisation note (see EBR-0001 v1.173).

---

# 8. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0125 (closed by this package).
* [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] - built and tested the `KokoroProvider` adapter this package now wires into production.
* [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] - Piper's original wiring into the live JSON-RPC bridge/UXP; the pattern this package's `_build_speech_provider()` change mirrors, in reverse.
* [[ESR-0053_ENGINEERING_SESSION_REPORT|ESR-0053]] - this session's report, WP2.
* `sentinel/kokoro_provider.py`, `jarvis/interfaces/stdio_rpc.py`, `pyproject.toml`, `jarvis/tests/test_kokoro_provider.py`, `jarvis/tests/test_stdio_rpc.py` - modified by this package.
