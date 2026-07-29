# EIP-ESR0040-001 - Voice Faculty Phase 6, Increment A: Speech Output (Text-to-Speech)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0040-001 |
| Artefact ID | EIP-ESR0040-001 |
| Title | Voice Faculty Phase 6, Increment A: Speech Output (Text-to-Speech) |
| Version | 1.2 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0112 |
| Intended Session | ESR-0040 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0112 records that [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Phase 6 (Voice/Vision) is now unblocked - its stated prerequisite (Phase 1, Guardian Cognitive Core) closed at ESR-0039 - but explicitly withholds scoping authority: "a future session should define the actual Voice/Vision faculty scope (input modality selection, provider/capability requirements, Sentinel/GAM-0001 governance implications for audio/visual data) via its own Engineering Implementation Package." This package is that definition, for a deliberately narrow first increment.

Confirmed directly against the live code this session (not inferred from architecture documents alone): no voice or vision code exists anywhere in the repository (`jarvis/guardian/`, `sentinel/`, `jarvis/interfaces/` contain no audio, speech, camera or vision references). [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] names Voice and Vision as architectural faculties only ("Voice provides ears and speech channel... does not bypass Sentinel or Guardian"); [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s Voice Services / Vision Services sections are two-paragraph placeholders with no concrete design. This is a genuinely new capability area, not an extension of existing code.

---

# 3. Objective

Deliver the smallest defensible first increment of the Voice faculty: **Guardian speech output (text-to-speech) only** - rendering Guardian's own already-approved response text as synthesised audio, on request, through a new Sentinel-gated speech-synthesis provider. Speech input (microphone capture / speech-to-text) and all Vision work are explicitly out of scope for this increment (Section 8) and reserved for separate future packages.

**Provider revision (v1.1):** v1.0 was implemented against ElevenLabs (a cloud HTTP API) and live-validated end to end at the design level, but the Programme Sponsor's own live smoke check (Section 10) failed with `HTTP 402 Payment Required` - the available ElevenLabs account is on the Free plan, which blocks API access to library voices entirely; this is an account/billing constraint, not a code defect, and the adapter's error handling behaved exactly as designed (real request, safely-wrapped real failure, honest `unavailable` outcome, no fabricated result). On review, the Programme Sponsor identified that ElevenLabs was also a new paid-cloud-vendor relationship with no prior footprint anywhere in this repository (`CURRENT_ARCHITECTURE.md` lists Azure OpenAI as an *evaluated* candidate provider only; the only providers ever wired into `sentinel/` are OpenAI, Gemini and local Ollama), in tension with the project's standing no-discretionary-budget/self-hosted-default posture. This revision replaces the ElevenLabs adapter with a **self-hosted, local** provider (Piper), keeping the rest of the design (Sections 5-6's parallel contract, Section 8's exclusion boundary, the `SpeechOutcome` envelope) unchanged - only the specific adapter and its dependency footprint change.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `sentinel/providers.py` `ExecutionProvider`/`ProviderRequest`/`ProviderResponse` | Text-only abstraction: `ProviderResponse.content: str` is validated non-empty as a string (`__post_init__` raises `ValueError` on blank content). No binary/bytes field exists. Shared by every current adapter (OpenAI, Gemini, Ollama, LocalEcho), all of which return `capability="text-generation"` content. |
| `sentinel/openai_provider.py` (representative adapter pattern) | `ProviderConfiguration` (name, credential `CredentialReference`, default model, endpoint, timeout, retry policy) + a `Transport` callable seam for testing; reads the API key from an environment variable named by `CredentialReference.environment_variable`; raises `RuntimeError` with a safe, non-leaking message on missing credential or transport failure (HTTP status surfaced, raw exception text never surfaced). This package's new adapter follows the same shape. |
| `jarvis/guardian/runtime.py` `GuardianRuntime` | Owns `_conversation_provider`, `_memory_service`, `_cognitive_core`; `converse()` gates on runtime state and provider connectivity, returning an honest boundary string (never a mock response) when either is unavailable. No equivalent boundary exists yet for any voice capability. |
| `jarvis/guardian/config.py` `GuardianRuntimeConfig` | `runtime_name`, `persistence_enabled`, `diagnostics_enabled`, `persona`. No voice-related field exists. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] Guardian Faculties table | Voice: "Provides ears and speech channel; it does not bypass Sentinel or Guardian." Architecture-only; not yet implemented. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8 (Family Safety and Emergency Controls) | Section 8.1's Household Role Model governs who may direct or approve Guardian actions and distinguishes personal from family-shared memory; Section 8.3 names "approved camera access" within emergency-assistance scope. Neither section addresses microphone capture or speech output specifically - this package's own scoping judgement (Section 9) is that speech *output* does not engage this model, since it introduces no new data collection or household-member attribution. |
| No existing local ML/model dependency | `pyproject.toml` declares exactly one runtime dependency (`psutil`) beyond the standard library - every existing Sentinel provider adapter (OpenAI, Gemini, Ollama) is implemented against raw `urllib`, deliberately avoiding an SDK dependency. This package is the first to add a genuinely new runtime dependency (`piper-tts`, pulling in `onnxruntime`, `numpy`, `protobuf`), a materially different addition than an HTTP call against an existing credential. |

---

# 5. Design Decision: A Parallel Interface, Not an Extension of `ExecutionProvider`

`ProviderResponse.content` is a validated non-empty `str`, and every existing provider adapter, Sentinel policy check and audit-trail code path assumes text content. Forcing synthesised audio through that field (for example, base64-encoded into `content`) would either violate the field's existing contract in spirit or require changing a dataclass shared by every working text-generation adapter - directly against the blast-radius-minimisation judgement already made once for this exact reason in [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] Section 8 item 2 ("no change to `ConversationRequest`, `ProviderRequest`... deliberately avoiding a wider-blast-radius refactor of the provider abstraction").

This package therefore scopes a **new, independent set of contracts** parallel to `sentinel/providers.py`, not a change to it. Nothing in the existing text-conversation path (`ConversationRequest`, `ProviderRequest`, `ExecutionProvider`, `SentinelGatedConversationProvider`, any existing adapter) is touched by this increment.

---

# 6. Scope

This package authorises a future implementation to:

1. Create `sentinel/speech_providers.py`:
   - `SpeechSynthesisRequest` (frozen dataclass): `text: str` (non-empty, validated), `voice_id: str | None = None`, `metadata: dict[str, str] = field(default_factory=dict)`.
   - `SpeechSynthesisResponse` (frozen dataclass): `provider_name: str`, `audio_bytes: bytes` (non-empty, validated), `mime_type: str` (e.g. `"audio/mpeg"`), `metadata: dict[str, str] = field(default_factory=dict)`.
   - `SpeechSynthesisProvider` (Protocol): `name` property, `synthesize(request: SpeechSynthesisRequest) -> SpeechSynthesisResponse` method. Deliberately not reusing `ExecutionProvider`'s `capabilities`/`execute` shape - this is a distinct capability family, not a new `"text-generation"`-style capability string on the existing protocol, per Section 5's reasoning.
   - A `execute_speech_synthesis_with_sentinel_decision(sentinel_response, provider, request)` gate function, mirroring `sentinel/providers.py`'s `execute_with_sentinel_decision` - speech synthesis is only permitted once Sentinel has evaluated the trust boundary, exactly like text generation. No new Sentinel decision-classification logic is introduced; this package reuses Sentinel's existing `SentinelResponse`/`SentinelDecisionOutcome` machinery unchanged.
2. Create `sentinel/piper_provider.py`: `PiperProvider` implementing `SpeechSynthesisProvider`, backed by the [Piper](https://github.com/OHF-Voice/piper1-gpl) local neural TTS engine (`piper-tts` PyPI package - self-contained, bundles its own `espeak-ng` phonemiser data, no system-level `espeak-ng` install required, no GPU required). Loads a Piper voice model (`.onnx` + `.onnx.json`) **once at construction** (confirmed by direct measurement: ~3.5s load, ~0.25s per short-sentence synthesis thereafter - loading per-request would be needlessly slow) from a local filesystem path carried in `ProviderConfiguration.endpoint` (reused generically, as `default_model` is reused for ElevenLabs' voice ID in the superseded v1.0 design). **Path contract (Engineering Reviewer finding, folded into v1.2):** `endpoint` is required for real `PiperProvider` construction (raises `ValueError` if absent, mirroring `ElevenLabsProvider`'s missing-credential check) and is interpreted *only inside `PiperProvider`* as a local `.onnx` voice-model path - this reuse is not generalised into a URL/path dual meaning anywhere else. A missing or invalid model path (or missing companion `.onnx.json` config, which `piper.PiperVoice.load()` itself requires) produces a clear, safe `RuntimeError` naming the path, never a raw underlying exception. If a future voice provider needs multiple model assets, a model registry, or non-path settings, that should trigger a dedicated speech-provider configuration shape rather than further overloading `endpoint`/`metadata` - not pre-built here. No `CredentialReference` - Piper has no API key or account. An injectable `synthesizer: Callable[[str], bytes]` seam (mirroring `Transport`) lets tests substitute a fake producing WAV bytes without importing `piper` or loading a real model, matching `OpenAIProvider`'s test-double pattern - `import piper` stays localised inside `sentinel/piper_provider.py`'s real-construction path, never at module top-level, so fake-seam unit tests and any code path that never touches voice output pay no `onnxruntime` import cost.
3. Add `piper-tts` to `pyproject.toml`'s `dependencies` list - the first runtime dependency beyond `psutil`. The voice model itself (a downloaded `.onnx`/`.onnx.json` pair, tens of megabytes) is **not** committed to the repository or auto-downloaded by any code path in this package - model acquisition (`python -m piper.download_voices en_US-lessac-medium`, a Piper-provided CLI) is a disclosed, one-time local setup step, and `PiperProvider` raises an honest, clear error naming the missing path if the model is absent, rather than downloading anything itself. This keeps the "no silent side effects" discipline already established for credentials (a missing `OPENAI_API_KEY` is reported, never silently fetched).
5. Create `jarvis/interfaces/voice.py`: a thin `SentinelGatedSpeechProvider` wrapper, parallel to `jarvis/interfaces/sentinel_conversation.py`'s existing `SentinelGatedConversationProvider` pattern - routes a synthesis request through Sentinel, then the connected `SpeechSynthesisProvider`, returning an honest, named "no speech provider connected" response (never a mock or fabricated audio payload, per the no-mock-fallback rule established at ESR-0017 WP9) when no provider is configured.
6. `jarvis/guardian/runtime.py`: `GuardianRuntime` gains an optional `speech_provider` constructor parameter and a `speak(text: str) -> SpeechOutcome` method, gated on runtime state exactly like `converse()`. `SpeechOutcome` (new frozen dataclass, `jarvis/interfaces/voice.py`) is a dedicated, typed boundary envelope - not `None` - with a named `status` field (`"synthesized"`, `"not_connected"`, `"not_running"`, `"denied"`, `"unavailable"`) and an `audio: SpeechSynthesisResponse | None` field populated only when `status == "synthesized"`. Each non-success status is a distinct, separately testable outcome, mirroring `converse()`'s existing named boundary-string constants (`NOT_CONNECTED_RESPONSE`, `NOT_RUNNING_RESPONSE`, Sentinel-denial, provider-failure) rather than collapsing them into a single generic failure. `speak()` takes Guardian's own response text as input; it does not accept arbitrary caller-supplied text unrelated to a real conversation turn, keeping this increment's output strictly to content Guardian has already generated.
7. Add `jarvis/tests/test_speech_providers.py`, `jarvis/tests/test_piper_provider.py` and `jarvis/tests/test_voice_interface.py` (matching the existing `jarvis/tests/` location for all Sentinel-adjacent tests, e.g. `test_sentinel_providers.py`, `test_openai_provider.py`) plus `jarvis/tests/test_guardian_runtime.py` coverage for: no-provider-connected returns the honest boundary outcome; Sentinel-denied synthesis is never executed; a successful synthesis call returns non-empty `audio_bytes` and the expected `mime_type`; a missing/invalid model path raises the same disclosed-safe error pattern as `OpenAIProvider`'s missing-credential case.
8. Update [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Cognitive Architecture section to record the Voice faculty, Phase 6 Increment A (speech output only) as implemented, explicitly stating that speech input and Vision remain not started.
9. Update [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Section 7.3's Phase 6 row, which currently reads "No backlog item yet registered," to reference EBG-0112 and this package, consistent with the Documentation Debt Discipline's whole-document staleness sweep (checked in full while this row is edited, per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]).
10. Mark [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0112 as reflecting Increment A scoping/delivery, explicitly recording that speech input and Vision remain separate, not-yet-authorised future increments (Increment B, Increment C).

No product UXP changes (`src/`, `src-tauri/`) are required or in scope - this is a backend capability increment, consistent with [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]'s Feature-First Delivery Discipline, which explicitly permits a session to advance the live UXP requirement through backend capability a future UXP increment will depend on, without touching `src/` itself.

---

# 7. Authorised Files

1. `sentinel/speech_providers.py` (new)
2. `sentinel/piper_provider.py` (new)
3. `jarvis/interfaces/voice.py` (new)
4. `jarvis/guardian/runtime.py`
5. `pyproject.toml` (new `piper-tts` runtime dependency)
6. `jarvis/tests/test_speech_providers.py` (new), `jarvis/tests/test_piper_provider.py` (new), `jarvis/tests/test_voice_interface.py` (new), `jarvis/tests/test_guardian_runtime.py`
7. `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md`
8. `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md`
9. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
10. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

Superseded from v1.0 and no longer authorised: `sentinel/elevenlabs_provider.py`, `jarvis/tests/test_elevenlabs_provider.py` (both to be deleted as part of this revision's implementation).

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any speech input, microphone capture or speech-to-text work (a future Increment B) - deferred because it introduces genuinely new data collection from whoever is physically present, engaging [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's Household Role Model (who is speaking, and under what consent) in a way this output-only increment does not. Per the same judgement already applied to EBG-0021 (Local Agent Permission Boundary), this warrants its own dedicated future session, not incidental treatment here.
2. Any Vision/camera work (a future Increment C) - same reasoning as above, and GAM-0001 Section 8.3 already treats camera access as a distinct, narrowly-scoped emergency-assistance concern requiring its own governance attention.
3. Any change to `ConversationRequest`, `ProviderRequest`, `ExecutionProvider`, `SentinelGatedConversationProvider` or any existing text-generation provider adapter (Section 5).
4. Any UXP (`src/`, `src-tauri/`) change - no waveform UI, no play/pause control, no JSON-RPC method exposed to the Tauri shell in this increment.
5. Any persistence of synthesised audio - `speak()` returns audio bytes to its caller; nothing is written to disk or a database by this package. Matches the "no new persistence" restraint already applied in EIP-ESR0039-001.
6. Any household-role or speaker-identity plumbing - not needed for output-only voice, since no new input is being attributed to any household member.
7. Any Deepgram integration or other speech-to-text provider - reserved for a future Increment B package, which would need to name and evaluate STT providers on its own merits.
8. Any cloud/paid speech-synthesis provider (ElevenLabs or otherwise) - superseded by this revision's self-hosted direction; a future increment could still add a cloud provider as an alternative behind the same `SpeechSynthesisProvider` Protocol, but that is a separate future decision, not part of this package.
9. Automatic voice-model download inside any code path - model acquisition is a disclosed, one-time manual setup step (Section 6 item 3), never triggered silently by `PiperProvider` itself.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status, per PBK-0001 Principle 3 and EBG-0112's own registration text.
2. Implementation must be reviewed by the Engineering Reviewer (Codex) both at design stage (this package) and post-commit against the real pushed diff, per the standing WP template (draft, review, Programme Sponsor approval, implement, commit, post-commit review) confirmed repeatable across ESR-0026 through ESR-0039.
3. Live validation (Section 10) requires a Piper voice model already downloaded locally (Section 6 item 3) before the smoke check can run - this is a one-time environment setup step, not a per-run cost. Automated tests exercise the adapter via the injectable `synthesizer` seam (Section 6 item 2), never loading a real model or writing real audio, matching `OpenAIProvider`'s existing test pattern.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes, including new speech-provider/Guardian-runtime test coverage, with no regression to existing tests.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. A live smoke check: with a Piper voice model downloaded locally and its path configured, a single `GuardianRuntime.speak()` call against real Guardian response text returns non-empty `audio_bytes` with `mime_type == "audio/wav"`; without a speech provider connected, `speak()` returns the honest "no speech provider connected" outcome rather than an error or fabricated result. **Confirmed after implementation**: a real end-to-end `GuardianRuntime.speak()` call (real `SentinelGatedSpeechProvider`, real `PiperProvider`, real voice model, no fake seam) returned `status="synthesized"` with a genuine 190,508-byte `audio/wav` payload; a second, unconfigured runtime correctly returned `status="not_connected"` with no audio.
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

New: `piper-tts` (PyPI), pulling in `onnxruntime`, `numpy`, `protobuf`, `pathvalidate`, `flatbuffers` transitively - this package's first runtime dependency addition beyond `psutil`, disclosed plainly rather than treated as incidental. All packages are widely-used, actively maintained, permissively-licensed (Piper itself is MIT; `onnxruntime` is MIT). No account, API key or recurring spend of any kind - genuinely free and self-hosted, consistent with the project's standing no-discretionary-budget default. A downloaded voice model (tens of MB, not committed to the repository) is required locally before `PiperProvider` can be constructed.

## Risks

1. **First-ever addition of a local ML runtime dependency** (`onnxruntime` et al.) to a project that has so far kept every provider adapter dependency-free (raw `urllib`). This is a real increase in dependency surface (install size, supply-chain surface, Windows-build compatibility) that a pure-HTTP adapter does not carry - disclosed plainly rather than treated as a free swap. Mitigated by the packages' maturity and permissive licensing, by the parallel-contract design (Section 5) keeping this entirely isolated from the text-conversation path, and by two implementation requirements (Engineering Reviewer findings, folded into v1.2): `pyproject.toml` shall pin `piper-tts` with an explicit bounded version constraint (not an unbounded `>=`), confirmed compatible with Python 3.12/Windows at implementation time; and `import piper`/`import onnxruntime` shall be localised inside `sentinel/piper_provider.py`'s real-construction path only, never at that module's or any shared module's top level, so ordinary fake-seam unit tests and any code path that never touches voice output never pay the ML dependency's import cost.
2. **Voice-model asset management has no established pattern in this repository.** Unlike a credential (a single env-var-referenced secret), a Piper voice model is a real downloaded file the Programme Sponsor's machine must have in a known location. This package documents the one-time manual download step (Section 6 item 3) but does not build any first-run auto-setup, model-registry or STD-0006-style formal configuration standard - consistent with EBG-0065 (Configuration and Secrets Standard) remaining separately open and not resolved by this package.
3. **CPU-only synthesis latency** (~0.25s per short sentence, measured directly) is acceptable for Increment A's non-interactive backend capability, but has not been measured against longer Guardian responses or under concurrent load - a future increment wiring this into the live UXP conversation path should re-measure before assuming interactive-latency suitability.
4. ~~`GuardianRuntime.speak()`'s exact return shape is deliberately left open~~ - **Resolved in v0.2** per Codex design review: `speak()` returns a dedicated `SpeechOutcome` envelope with a named `status` field and per-outcome testability, rather than `None` or a raised exception (Section 6 item 6).
5. **This increment delivers no user-visible capability** (no UXP wiring) - by design, per Section 6's closing paragraph, but disclosed here as a genuine trade-off: the Programme Sponsor should be aware this session's product-moving work is a real, live-verified backend capability, not something a user can yet hear.

## New Backlog Items Anticipated (Not Registered by This Draft)

Increment B (speech input / speech-to-text) and Increment C (Vision) are natural future EBR-0001 items once the Programme Sponsor chooses to prioritise them; this draft does not register either, since EBG-0112 already covers Phase 6 as a whole and a further split can be registered when one of those increments is actually selected as a future session's objective.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via the AIEMS Exchange Bridge (`ESR-0040`/`WP1`) for design review, run in `-s read-only` sandbox mode per the established EBG-0096 pattern. **Result: no blocking findings.** Codex confirmed the parallel `SpeechSynthesisProvider` contract (Section 5) is the right call over extending the text-only `ExecutionProvider`/`ProviderResponse`, confirmed the output-only/GAM-0001 Section 8.1 exclusion boundary (Section 8) is soundly reasoned, and confirmed Sections 7/8 correctly bound blast radius. One non-blocking finding was raised and folded into v0.2 above: `speak()`'s return shape should be settled now rather than left open for implementation to decide - resolved via a dedicated `SpeechOutcome` envelope with named, separately-testable status outcomes (Section 6 item 4, Section 11 Risk 3).

Codex's own `return-findings` call failed inside its read-only sandbox (`PermissionError` creating the work-package lock file - the same disclosed limitation recorded in EBG-0096's history, e.g. ESR-0039 WP2's independent `pytest` attempt). Its findings were relayed verbatim into the bridge transcript by the Engineering Implementer, under explicit per-instance Programme Sponsor approval for that relay act, matching the EIP-ESR0039-001 precedent.

**v1.0 approved and implemented against ElevenLabs**, verified against the real Sponsor Approval Service via `submit-response` before implementation began, per ADR-0022/EIP-ESR0030-001 discipline. `sentinel/speech_providers.py`, `sentinel/elevenlabs_provider.py`, `jarvis/interfaces/voice.py` and `GuardianRuntime.speak()` were built and fully tested (22 new tests, full suite 418 passed/1 skipped). **Superseded by this v1.1 revision** following the Section 3 "Provider revision" finding (live ElevenLabs smoke check: HTTP 402, Free-plan API restriction; Programme Sponsor identified Azure/ElevenLabs as new paid-vendor relationships with no repository precedent, in tension with the standing self-hosted/no-discretionary-budget default) - the ElevenLabs adapter and its test file are removed as part of this revision; the parallel-contract design, `SpeechOutcome` envelope and all governance/documentation updates already delivered under v1.0 remain valid and unchanged.

**v1.1 submitted to Codex via the AIEMS Exchange Bridge (`ESR-0040`/`WP1`) for design review, run in `-s read-only` sandbox mode.** **Result: no blocking findings.** Codex confirmed all three submitted questions favourably: `ProviderConfiguration.endpoint` reuse for a local model path is defensible as a narrow, Piper-adapter-scoped reuse (not generalised elsewhere); eager model-load-at-construction is sound (no credential-refresh concern exists for a local model, and the measured ~3.5s load / ~0.25s per-request split makes per-request loading the worse choice); and the new ML dependency-surface risk is adequately disclosed for a design-stage decision, with subprocess isolation correctly judged unnecessary for this increment (no untrusted-model or crash-containment requirement exists yet). Two non-blocking findings raised and folded into v1.2 above: (1) Section 6 item 2 now states the exact `endpoint` path contract and validation behaviour explicitly, rather than leaving Piper-specific path semantics implicit; (2) Section 11 now requires a bounded `piper-tts` version constraint and `import piper`/`onnxruntime` localised inside `sentinel/piper_provider.py`'s real-construction path only, so fake-seam unit tests never pay the ML dependency's import cost.

Codex's own `return-findings` call again failed inside its read-only sandbox (same disclosed `PermissionError` limitation as this Work Package's v1.0 review). Its findings were relayed verbatim into the bridge transcript by the Engineering Implementer, under explicit per-instance Programme Sponsor approval for that relay act.

**Programme Sponsor approved v1.2 for implementation.** Verified against the real Sponsor Approval Service via `submit-response` before implementation began, per ADR-0022/EIP-ESR0030-001 discipline.

**Implemented exactly as scoped.** `sentinel/elevenlabs_provider.py` and `jarvis/tests/test_elevenlabs_provider.py` removed. `sentinel/piper_provider.py` (new): `PiperProvider`, with `import piper` localised to its real-construction path only, the exact `endpoint` path contract from Section 6 item 2, and the disclosed-safe `RuntimeError` pattern for a missing/invalid model path. `pyproject.toml` gained `piper-tts>=1.6.0,<2.0` - the project's first runtime dependency beyond `psutil`. `jarvis/tests/test_piper_provider.py` (new, six tests, all via the injectable `synthesizer` seam - no real model loaded). `sentinel/speech_providers.py`, `jarvis/interfaces/voice.py` and `GuardianRuntime.speak()` are unchanged from v1.0. 22 new tests total; full suite 418 passed/1 skipped (no regressions). [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (EBG-0112 Complete (Increment A)) updated to describe the final Piper-based delivery.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture this package builds against; updated by this package once implemented. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0112 (this package's parent item). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Section 7.3, Phase 6 - the roadmap placement this package scopes the first increment of. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Authority/boundary model considered in Section 8/9's exclusion reasoning; not itself changed by this package. |
| [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] | Precedent for the blast-radius-minimisation and no-mock-fallback discipline this package follows. |
| [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Working Report Lifecycle discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 29 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review of the Piper revision via AIEMS Exchange Bridge: no blocking findings, all three submitted questions answered favourably. Folded two non-blocking clarifications: Section 6 item 2's `endpoint` path contract stated explicitly; Section 11 now requires a bounded `piper-tts` version constraint and localised `import piper`/`onnxruntime` inside `sentinel/piper_provider.py` only. Programme Sponsor approved for implementation, verified via `submit-response` against the real Sponsor Approval Service. Implemented exactly as scoped: `sentinel/elevenlabs_provider.py` removed, `sentinel/piper_provider.py` added, `pyproject.toml` gained `piper-tts>=1.6.0,<2.0`. 22 new tests, full suite 418 passed/1 skipped. EBG-0112 marked Complete (Increment A) in EBR-0001; AAM-0001 and JRM-0001 updated to describe the final Piper-based delivery. |
| 1.1 | 29 July 2026 | Claude Engineering Implementer | Provider revision: v1.0's live ElevenLabs smoke check failed (HTTP 402, Free-plan API restriction on library voices) and the Programme Sponsor identified Azure/ElevenLabs as new paid-vendor relationships with no repository precedent, against the project's self-hosted/no-discretionary-budget default. Replaces the ElevenLabs adapter with a self-hosted Piper (local neural TTS) adapter - the first runtime dependency addition beyond `psutil`. Design otherwise unchanged (parallel contract, exclusion boundary, `SpeechOutcome` envelope). Draft, not yet reviewed or approved for this revision. |
| 1.0 | 29 July 2026 | Claude Engineering Implementer | Programme Sponsor approved for implementation, verified via `submit-response` against the real Sponsor Approval Service. Implemented exactly as scoped: new `sentinel/speech_providers.py`, `sentinel/elevenlabs_provider.py`, `jarvis/interfaces/voice.py`; `GuardianRuntime.speak()` wired. 22 new tests, full suite 418 passed/1 skipped. EBG-0112 marked Complete (Increment A) in EBR-0001; AAM-0001 and JRM-0001 updated. |
| 0.2 | 29 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via AIEMS Exchange Bridge: no blocking findings. Folded one non-blocking clarification: `GuardianRuntime.speak()` return shape settled as a dedicated `SpeechOutcome` envelope with named, separately-testable status outcomes rather than left open (Section 6 item 4, Section 11 Risk 3). Pending Programme Sponsor approval. |
| 0.1 | 29 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0040 WP1. Scopes Voice Faculty Phase 6 Increment A (speech output only) as a new, parallel Sentinel provider interface, explicitly excluding speech input and Vision. Not yet reviewed or approved. |
