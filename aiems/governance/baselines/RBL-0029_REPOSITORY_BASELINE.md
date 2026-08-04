# RBL-0029 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0029 |
| Title | ESR-0047 Repository Baseline (Voice Faculty Increment B: Speech Input) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] |
| Previous Baseline | [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 4 August 2026 |
| HEAD at baseline creation | `5c02d3d` |

---

# 2. Purpose

RBL-0029 records the repository baseline accepted by the Programme Sponsor at ESR-0047 WP7, superseding [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]]. ESR-0047 ran four Work Packages plus a WP6-caught fix round: WP1 (Documentation Debt Discipline), WP2 (EBG-0118 investigation), WP3 (resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0117, Voice Faculty Increment B: Speech Input - a genuine, live product-capability change), WP4 (Repository Engineering Health Review, advisory only), and a session-wide WP6 fix round correcting a real capability-gating defect found by independent review. Guardian now has real, working push-to-talk speech input alongside its existing speech output, closing RSC-0001's scored "Basic Voice Input" Fail against MLP 0.1 and resolving the last of [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]]'s two Must-Ship items.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; flagged as a documentation-staleness finding at WP4, recommended for a future session's Documentation Debt sync. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Design review (Codex, direct `codex exec -s read-only` invocation)**: [[EIP-ESR0047-001_VOICE_PHASE6_INCREMENT_B_SPEECH_INPUT_SCOPE|EIP-ESR0047-001]] v0.1 reviewed Pass with non-blocking findings (softened GAM-0001 Section 8.4 analogy wording, clarified the enablement gate does not satisfy Household Role Model enforcement, tightened a "no live mechanism" claim) - all three folded into v0.2 before implementation.

**Session-wide WP6 Independent Repository Verification**: covering the full range `f36a465..5c02d3d` (5 commits). First pass returned **Fail**: Codex found that `src/App.jsx` always rendered the microphone button and started `getUserMedia`/`MediaRecorder` before learning whether transcription was configured - a genuine scope/privacy-gating mismatch against the approved EIP's own Section 5.5 item 12, not a wording nitpick. Fixed directly in the same WP6 pass (`GuardianRuntime.transcription_available`, a new `platform.status` field, conditional mic-button rendering) and re-submitted. **Second pass: Pass, no findings** - Codex confirmed the fix genuinely closes the gap (no other code path can reach `getUserMedia`), the fix commit carries no unrelated changes, and the new/modified tests genuinely exercise the gating rather than being cosmetic.

**Programme Sponsor approval**: obtained and verified via `submit-response` directly against the real Sponsor Approval Service for every Work Package (WP1 through WP4) and the WP6 fix round - not merely asserted in chat - before each round of implementation began.

**The Programme Sponsor's determination**: **establish a new baseline**, since this session's WP3 (and its WP6 fix) delivered a genuine, live product-capability change - Guardian now has real, working push-to-talk speech input reachable through the actual running Tauri UXP, backed by a real end-to-end round trip (Guardian's own Piper-synthesized speech transcribed back by Guardian's own Whisper path, exact text match) - matching the same threshold applied at RBL-0025/RBL-0027/RBL-0028 rather than the Retain threshold applied at architecture/documentation-only sessions.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `sentinel/transcription_providers.py`, `sentinel/whisper_provider.py` (new) | Provider-neutral transcription contract and a self-hosted `faster-whisper` adapter, mirroring `sentinel/speech_providers.py`/`sentinel/piper_provider.py`'s established pattern exactly for the opposite data direction. |
| `jarvis/interfaces/voice.py` | `TranscriptionOutcome` and `SentinelGatedTranscriptionProvider`, mirroring `SpeechOutcome`/`SentinelGatedSpeechProvider`. |
| `jarvis/guardian/runtime.py` | `GuardianRuntime.transcribe()` (mirrors `speak()`'s boundary checks) and `transcription_available` (new property, added at the WP6 fix round to let capability availability be known before any UI is offered). |
| `jarvis/interfaces/stdio_rpc.py` | New `guardian.transcribe` RPC method, `_build_transcription_provider()` (env-var-gated behind `JARVIS_WHISPER_MODEL_PATH`, mirroring Piper's pattern), and a new `transcriptionAvailable` field on `platform.status` (WP6 fix round). |
| `pyproject.toml` | `faster-whisper>=1.0,<2.0` added and installed; live-confirmed working (`faster-whisper` 1.2.1). |
| `src-tauri/src/lib.rs` | `transcribe_audio` command, byte-for-byte matching `speak_message`'s `call_backend` shape. `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test` all pass cleanly. |
| `src/App.jsx`, `src/styles.css` | A push-to-talk mic button in the message composer (`MediaRecorder`/`getUserMedia`, 30s hard cap), conditionally rendered only when `platform.status` reports `transcriptionAvailable` (WP6 fix round); `.input-shell` changed from a fixed grid to flex layout to degrade cleanly without the button. Transcripts populate the composer for review - never auto-submitted. |
| `jarvis/tests/test_transcription_providers.py`, `test_whisper_provider.py`, extended `test_voice_interface.py`/`test_guardian_runtime.py`/`test_stdio_rpc.py` | 32 new/extended tests (30 at WP3, 2 more at the WP6 fix round). |
| `tests/e2e/app.spec.js` | 3 new Playwright specs (mic-button-absent-by-default, inline-error path, populates-composer path) - full e2e suite (12 tests) passes. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.4 records the capability-enablement gating decision and its explicit non-equivalence to a genuine pre-approved policy record (1.4 to 1.5). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Voice faculty Increment B recorded as implemented; Increment A's own paragraph (which still said speech input "remains not started") corrected (0.8 to 0.9). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0117 marked Completed; EBG-0118 investigated (inconclusive, remains open, Candidate Backlog). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Both Must-Ship rows now struck through - the launch-blocking gap list is empty pending any future RSC-0001 refresh. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. WP4's Repository Engineering Health Review flagged this as one of six documentation-staleness findings, recommending a batched Documentation Debt sync as the next session's WP1.

---

# 7. Architecture Outcomes

- Guardian's Voice faculty is now bidirectional - speech output (Increment A, ESR-0040/ESR-0044) and speech input (Increment B, this session) both implemented, Sentinel-gated, reachable through the live UXP.
- A new Sentinel-gating pattern was established for capability-enablement-as-approval-gate (by analogy to GAM-0001 Section 8.4, not as an equivalent mechanism), disclosed and reviewed rather than assumed - the first instance of this pattern being applied to a capability outside emergency actions.
- Session-wide WP6 caught and fixed a real defect in that gating's actual implementation (the button rendered/activated hardware regardless of backend configuration) - proof the independent-review step is doing real work, not a formality, on a session where the reviewing tool (Codex) had itself been the subject of a separate reliability investigation (WP2) earlier the same session.
- No speaker identification, role attribution, or enforcement of GAM-0001 Section 8.1's role differences is implemented - deliberately excluded, disclosed in both the EIP and GAM-0001 itself.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no wake-word detection, continuous/always-on listening, or background microphone capture - push-to-talk only;
- no speaker identification or attribution of a transcript to a household profile;
- no auto-submission of a transcript to Guardian - the household member must press Send themselves;
- no cloud/paid STT provider - `faster-whisper` only, self-hosted;
- English-only (`tiny.en`/`base.en` models);
- no enforcement of GAM-0001 Section 8.1's role differences beyond the deployment-level enablement gate;
- Vision (Increment C) remains not started.

---

# 9. Verification

Repository validation performed across ESR-0047's Work Packages and at WP6/WP7 closure:

- Git working tree was clean throughout; the session's content (`f36a465..5c02d3d`, 5 commits) pushed to `origin/main`.
- 485/486 Python tests passing plus 1 correctly-skipped test, up from 453/454 at RBL-0028 (32 new).
- `ruff check`: clean throughout.
- `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test`: all clean.
- `npx playwright test`: 12 passed (3 new, was 9 at RBL-0028's era).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count grew from 268 to 278, all new warnings being the same established non-blocking "unlinked section back-reference" class already present repository-wide - none newly introduced as a content defect.
- Design review (Codex): Pass with non-blocking findings, folded in before implementation. Session-wide WP6: first pass Fail (real defect found), fixed, second pass Pass with no findings.
- Live end-to-end smoke validation: Guardian's own Piper-synthesized speech for a real test sentence, fed back through Guardian's own Whisper transcription path via the real `guardian.transcribe` RPC dispatch - transcribed back as the exact, identical sentence. `platform.status`'s `transcriptionAvailable` field independently confirmed to read `False`/`True` correctly against the real `build_default_runtime()` path.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0028 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0047** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. A literal native-window microphone click-through (`npm run tauri dev`, a real WebView2 window, real hardware) was not performed in this implementation environment - remains available for the Programme Sponsor, matching the precedent already established for real-hardware/real-window confirmation steps this implementation environment cannot perform.
5. WP4's six documentation-staleness findings (RSC-0001, PCB-0001, JARVIS_CAPABILITY_READINESS_MATRIX, README.md, PST-0001, JRM-0001, plus EBR-0001 Section 5A's snapshot) - recommended as a single batched Documentation Debt sync for the next session's WP1.
6. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118 (Codex CLI tooling stall) remains open, Candidate Backlog, Low - this session's investigation was inconclusive; left for a future session with fresh evidence, not further chased speculatively.
7. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, expected to surface at a future session's WP0A and correctable there per PBK-0001's Documentation-Debt Priority discipline.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] | Session this baseline is drawn from. |
| [[EIP-ESR0047-001_VOICE_PHASE6_INCREMENT_B_SPEECH_INPUT_SCOPE|EIP-ESR0047-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.4 updated to record the capability-enablement gating decision. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Voice faculty Increment B recorded as implemented. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0117 (closed this session); EBG-0118 (investigated this session, remains open). |
| [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]] | Both Must-Ship rows now struck through. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0028, following Codex's design review (Pass with non-blocking findings, folded in) and session-wide WP6 Independent Repository Verification - which caught a real capability-gating defect on first pass, saw it fixed, and returned Pass with no findings on re-review - and the Programme Sponsor's explicit WP7 decision to cut a new baseline: WP3's real, live-verified Voice Faculty Increment B (Speech Input) delivery warrants a new baseline. |
