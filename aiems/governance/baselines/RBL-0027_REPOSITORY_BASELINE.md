# RBL-0027 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0027 |
| Title | ESR-0044 Repository Baseline (Guardian Voice Faculty Wired into the Live Runtime and UXP) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] |
| Previous Baseline | [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 30 July 2026 |
| HEAD at baseline creation | `899e67f` |

---

# 2. Purpose

RBL-0027 records the repository baseline accepted by the Programme Sponsor at ESR-0044 WP3, superseding [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]]. ESR-0044 ran one Work Package: WP1, closing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0114 - Guardian's Voice faculty (EBG-0112, ESR-0040) is now reachable through the real running Tauri UXP for the first time, not only standalone validation scripts. A genuine, live-verified 3-layer product capability change, without modifying any already-approved Voice component itself.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; a future refresh should note the Voice faculty is now reachable through the live product, not only backend-only |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Design review (Codex, direct `codex exec -s read-only` invocation)**: Pass, with non-blocking findings - confirmed the credential-gated `JARVIS_PIPER_VOICE_PATH` pattern was correct, reusing the single `SentinelTrustGateway` instance was correct, the `guardian.speak` RPC shape was sound, and the frontend scope was appropriately minimal. Three non-blocking clarifications folded in before implementation.

**Post-commit independent verification (Codex)**: Pass, no blocking findings - independently re-read the real pushed diff for commit `899e67f`, confirmed it touched exactly the 11 claimed files and nothing outside that scope, confirmed via direct `git diff` that `jarvis/guardian/runtime.py`, `jarvis/interfaces/voice.py`, `sentinel/piper_provider.py` and `sentinel/speech_providers.py` were genuinely untouched, confirmed the RPC/Tauri wiring shapes matched the claimed design, and confirmed the new unit tests never construct or load a real Piper model. One non-blocking observation (a whitespace-only `JARVIS_PIPER_VOICE_PATH` is treated as configured, consistent with the existing codebase convention) was disclosed, not treated as blocking.

**Programme Sponsor approval**: obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**The Programme Sponsor's determination**: **establish a new baseline**, since this session's WP1 delivered a genuine, live product-capability change - Guardian's Voice faculty is reachable through the actual running Tauri UXP for the first time, backed by a real end-to-end synthesis confirmation (161,836-byte `audio/wav` payload) through the exact new wiring, matching the same threshold applied at RBL-0025 (Voice faculty first delivered) and RBL-0026 (persona behaviour change).

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/interfaces/stdio_rpc.py` | `PIPER_VOICE_PATH_ENV_VAR`, `_build_speech_provider()` (credential-gated, reuses the existing `SentinelTrustGateway`), `speech_provider` wired into `GuardianRuntime(...)`, and a new `guardian.speak` JSON-RPC method serializing `SpeechOutcome` (base64 audio + mime type only when `synthesized`). |
| `jarvis/tests/test_stdio_rpc.py` | 6 new tests, using a `_FakePiperProvider` patched over the real class - env-var absent/present wiring, gateway reuse, and RPC serialization for both synthesized and `not_connected` outcomes, without ever loading a real model. |
| `src-tauri/src/lib.rs` | New `speak_message` Tauri command, byte-for-byte matching `send_message`'s `call_backend` shape, registered in `generate_handler!`. `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test` all pass cleanly. |
| `src/App.jsx`, `src/styles.css` | A minimal per-message speak button decoding and playing the returned base64 audio via a plain `Audio` object, with non-blocking inline error notes for both backend non-synthesized outcomes and the frontend's own playback failures. `src/styles.css` was a disclosed, minor discovered dependency (button styling), not in the original authorised file list. |
| `tests/e2e/app.spec.js` | 2 new Playwright specs (not-connected error path; synthesized/no-error path via a minimal valid silent-WAV fixture) - full e2e suite (7 tests) passes. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Updated (0.7 to 0.8) to record Voice as reachable through the live product. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0114 marked Completed. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. A future session should refresh it to reflect Guardian's Voice faculty as reachable through the live UXP, not merely implemented in the backend.

---

# 7. Architecture Outcomes

- Guardian's Voice faculty (EBG-0112, ESR-0040) is reachable through the real running product for the first time - previously only standalone, uncommitted scripts could exercise it.
- No already-approved Voice component (`PiperProvider`, `SentinelGatedSpeechProvider`, `GuardianRuntime.speak()`, `SpeechOutcome`) was modified - this session changed wiring/construction only, independently confirmed by Codex's post-commit diff review.
- The credential-gated wiring pattern (`JARVIS_PIPER_VOICE_PATH` absent means honest `not_connected`, never a startup failure, no auto-download) directly mirrors the project's existing OpenAI/Gemini credential-gating convention, keeping the codebase's degradation philosophy consistent across faculties.
- The new UXP affordance is deliberately minimal - a single per-message speak button, no auto-play, no redesign - consistent with PBK-0001's Incremental Visual Convergence discipline (small, real, additive UXP progress rather than a large speculative redesign).

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no automatic voice-model download exists in any code path - model acquisition remains a disclosed, one-time manual step;
- no speech input, microphone capture, or STT capability;
- no redesign of `CommandPanel`'s conversation log beyond the speak button and its audio-playback/error-note behaviour;
- no auto-play of every Guardian response as speech by default - explicit, per-message, user-initiated only;
- no change to `GuardianRuntime.speak()`, `SentinelGatedSpeechProvider`, `PiperProvider`, `SpeechOutcome` or `SpeechSynthesisResponse` themselves - only their wiring into the default construction path and RPC/Tauri/UI surface changed.

---

# 9. Verification

Repository validation performed during ESR-0044 WP2/WP3:

- Git working tree was clean; the session's intended content (`75e4717..899e67f`) pushed to `origin/main`.
- 424/425 Python tests passing plus 1 correctly-skipped test, up from 418/419 at RBL-0026 (6 new tests).
- `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test`: all clean.
- `npx playwright test`: 7 passed (2 new, was 5 at RBL-0026's era for `app.spec.js`/`animationScheduler.spec.js` combined).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count at 258, consistent with the established pre-existing cross-document-reference false-positive category.
- Design review (Codex, two rounds - v0.1 Pass with non-blocking findings folded into v0.2): both Pass. Post-commit independent diff review (Codex): Pass, no blocking findings - one non-blocking observation about whitespace-only env var handling, consistent with existing codebase convention.
- Live end-to-end smoke validation: a real Piper voice model downloaded via `piper-tts`'s own `download_voices` CLI to an uncommitted local path (removed afterward); a genuine `guardian.speak` call through the real `build_default_runtime()` + RPC wiring produced a real 161,836-byte `audio/wav` payload; the unconfigured case correctly returned `not_connected` with no `audio` key.
- The Programme Sponsor's own WP3 determination: establish a new baseline rather than retain RBL-0026 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0044** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. Real audio-hardware playback confirmation through the live Tauri app was not performed in this implementation environment - remains available for the Programme Sponsor, matching the exact precedent already established at ESR-0040/ESR-0042.
5. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0115 (Evaluate Kokoro TTS) remains open, unaffected by this session's wiring work - the model-quality question and the reachability question were always distinct.
6. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at a future session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] | Session this baseline is drawn from. |
| [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture updated to record Voice as reachable through the live product. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0114 (closed this session); EBG-0115 (unaffected, remains open). |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0026, following Codex's design review (Pass, non-blocking findings folded in) and post-commit independent diff review (Pass, no blocking findings) and the Programme Sponsor's explicit WP3 decision to cut a new baseline rather than retain RBL-0026: WP1's real, live-verified Guardian Voice faculty wiring into the running product warrants a new baseline. |
