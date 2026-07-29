# RBL-0025 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0025 |
| Title | ESR-0040 Repository Baseline (EBG-0112 Increment A - Guardian Voice Faculty, Speech Output) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] |
| Previous Baseline | [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 29 July 2026 |
| HEAD at baseline creation | `6f595ab` |

---

# 2. Purpose

RBL-0025 records the repository baseline accepted by the Programme Sponsor at ESR-0040 WP3, superseding [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]]. ESR-0040 ran one Work Package: WP1, closing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0112's Increment A scope - Guardian gains its first Voice faculty capability, speech output (text-to-speech), via a new Sentinel-gated speech-synthesis provider backed by self-hosted Piper. This is also the project's first runtime dependency addition beyond `psutil`. Both independent WP2 verification passes (pre-commit Codex design review and post-commit Codex diff review) converged that this real, tested product code change is baseline-worthy.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; a future PCB-0001 refresh should reflect Guardian's Voice faculty moving from not-started to speech-output-implemented |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Pre-commit design review (Codex, two rounds)**: v1.0 (ElevenLabs) PASS, no blocking findings. v1.2 (Piper revision, following a failed live smoke check against ElevenLabs and a Programme Sponsor-directed pivot to a self-hosted provider) also PASS, no blocking findings - Codex confirmed the parallel-contract design, the local-model `endpoint` reuse, eager model-load-at-construction, and the new ML-dependency-surface risk were all soundly reasoned, with two non-blocking clarifications folded in before implementation.

**Post-commit independent verification (Codex)**: PASS, no findings - independently re-read the real pushed diff for `1399c4f..6f595ab`, confirmed it touched exactly the 15 claimed files and nothing outside that scope, confirmed no `src/`, `src-tauri/`, `jarvis/memory/` or `.github/workflows/` file was touched, confirmed no change to any existing text-generation provider contract or adapter, confirmed `sentinel/elevenlabs_provider.py` and its test file are genuinely absent from the final committed tree, and spot-checked `PiperProvider` against the approved design (localised `import piper`, required/validated `endpoint`, safe `RuntimeError` wrapping).

**Real live end-to-end validation**: a genuine `GuardianRuntime.speak()` call, through the real Sentinel gate and the real Piper provider (no fake seam), produced a real 190,508-byte `audio/wav` payload; a second, unconfigured runtime correctly returned the honest `not_connected` outcome.

**The Programme Sponsor's determination**: **establish a new baseline**, per the same threshold applied at RBL-0021 through RBL-0024 - a genuine, independently-verified change to live Guardian capability (a new faculty, not merely an internal refactor), backed by new test coverage and a live-verified real output, rather than documentation or governance churn alone.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `sentinel/speech_providers.py` (new) | Parallel `SpeechSynthesisRequest`/`SpeechSynthesisResponse`/`SpeechSynthesisProvider` contracts and `execute_speech_synthesis_with_sentinel_decision`, independent of the existing text-only `ExecutionProvider`/`ProviderResponse` abstraction. |
| `sentinel/piper_provider.py` (new) | `PiperProvider`, backed by the self-hosted Piper local neural TTS engine. Loads a voice model once at construction; `import piper` localised to avoid an import cost for any code path that never constructs a real provider. |
| `jarvis/interfaces/voice.py` (new) | `SentinelGatedSpeechProvider` and the `SpeechOutcome` envelope - a dedicated, named-status boundary result (`synthesized`/`not_connected`/`not_running`/`denied`/`unavailable`), never `None` or an unstructured exception. |
| `jarvis/guardian/runtime.py` | `GuardianRuntime` gained an optional `speech_provider` parameter and a `speak(text) -> SpeechOutcome` method, gating on runtime state exactly like `converse()`. |
| `pyproject.toml` | `piper-tts>=1.6.0,<2.0` added - the project's first runtime dependency beyond `psutil`. |
| Test suite | 22 new tests (`test_speech_providers.py`, `test_piper_provider.py`, `test_voice_interface.py`, plus `test_guardian_runtime.py` extensions); 418 passed plus 1 skip (was 396 plus 1 skip); no regressions. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Cognitive Architecture section updated (0.5 to 0.6) recording the Voice faculty, Phase 6 Increment A as implemented; Action/Vision/speech-input remain not started. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0112 marked Complete (Increment A). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Section 7.1/7.2/7.3 corrected (Documentation Debt Discipline whole-document sweep) - Phase 1 rows updated to Delivered, Phase 6 row updated to record EBG-0112/Increment A. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. A future session should refresh it to reflect Guardian's Voice faculty moving from not-started to speech-output-implemented (Increment A only - speech input and Vision remain not started).

---

# 7. Architecture Outcomes

- Guardian gains its first Voice faculty capability: speech output only, via a new Sentinel-gated, self-hosted local TTS provider.
- The project's first runtime dependency beyond `psutil` (`piper-tts`, pulling in `onnxruntime`/`numpy`/`protobuf` transitively) - a real, disclosed increase in dependency surface, deliberately isolated to a new speech adapter via localised imports.
- No cloud vendor relationship, credential or recurring cost was introduced - a deliberate correction from the session's initial ElevenLabs design, made after a live validation failure (HTTP 402, Free-plan API restriction) surfaced that ElevenLabs (and a considered alternative, Azure) had no prior footprint in this repository and sat against the project's standing self-hosted/no-discretionary-budget default.
- This closes Increment A of JRM-0001 Track B Phase 6 (Voice/Vision); Increment B (speech input) and Increment C (Vision) remain future work, each requiring its own Engineering Implementation Package and warranting its own dedicated session given their GAM-0001 Section 8.1 Household Role Model implications.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- speech input (microphone capture / speech-to-text) and Vision are explicitly not implemented by this baseline;
- no UXP (`src/`, `src-tauri/`) change was made - this is a backend-only capability increment;
- no change was made to `ConversationRequest`, `ProviderRequest`, `ExecutionProvider`, `SentinelGatedConversationProvider` or any existing text-generation provider adapter;
- no persistence of synthesised audio was added - `speak()` returns audio bytes to its caller only;
- no automatic voice-model download exists in any code path - model acquisition is a disclosed, one-time manual setup step;
- `jarvis/memory/` and `.github/workflows/` were not touched at all this session.

---

# 9. Verification

Repository validation performed during ESR-0040 WP2/WP3:

- Git working tree was clean; the session's intended content (`1399c4f..6f595ab`) pushed to `origin/main`.
- 418/419 Python tests passing plus 1 correctly-skipped win32-conditional test, up from 396/397 at RBL-0024 (22 new tests).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count at 192, consistent with the established pre-existing cross-document-reference false-positive category (one additional warning from this session's own new cross-referencing text).
- Pre-commit Codex design review (two rounds, ElevenLabs then Piper): both Pass, no blocking findings. Post-commit Codex independent diff review: Pass, no findings (one disclosed, pre-existing Codex read-only-sandbox limitation again prevented Codex from independently running `pytest` itself - `validate_repository.py` and the diff/design spot-check were both completed successfully in that same sandbox).
- Live end-to-end smoke validation: a real `GuardianRuntime.speak()` call produced a genuine 190,508-byte `audio/wav` payload via the real Sentinel gate and real Piper provider; the no-provider boundary case returned the honest outcome.
- The Programme Sponsor's own WP3 determination: establish a new baseline rather than retain RBL-0024 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0040** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - Increment B (speech input) and Increment C (Vision) remain unauthorised future work under EBG-0112, each warranting its own dedicated future session given GAM-0001 Section 8.1 implications.
5. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at the next session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] | Session this baseline is drawn from. |
| [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0112 (Increment A closed this session). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture updated to record the Voice faculty Increment A as implemented. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Phase 6 updated; Phase 1 rows corrected as part of this session's documentation-debt sweep. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session, though this baseline's outcome makes it stale (Section 6). |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0024, following Codex's pre-commit design review (two rounds, both Pass) and post-commit independent diff review (Pass) and the Programme Sponsor's explicit WP3 decision to cut a new baseline rather than retain RBL-0024: WP1's real, tested Guardian Voice faculty delivery (speech output, self-hosted Piper) warrants a new baseline. |
