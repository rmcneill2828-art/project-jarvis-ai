# ESR-0040 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0040 |
| Title | Engineering Session Report |
| Version | 1.4 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0040 |
| Date Opened | 29 July 2026 |
| Date Closed | 29 July 2026 |
| Closure Status | Closed - WP1 complete, session-wide WP2 Pass, WP3 Establish (RBL-0025 accepted) |

---

# 2. Purpose

This report records the opening and execution of ESR-0040, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]] closed (29 July 2026), [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`). Three direct Programme Sponsor-requested governance edits landed after ESR-0039 closure but outside any open session (EBG-0111 Composio registration and its MCP-server addendum; EBG-0112 Voice/Vision unblocked-notice registration) - confirmed already correctly disclosed in their own commit messages and REG-0001/EBR-0001 version history, not requiring correction here. No open [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] item concerns documentation staleness as its own category, so PBK-0001's Documentation-Debt Priority discipline does not constrain WP0/WP1 selection this session.

`scripts/session_launcher.py` was run to surface candidate objectives. Presented to the Programme Sponsor: EBG-0112 (Voice/Vision, JRM-0001 Track B Phase 6, newly unblocked), EBG-0021 (Local Agent Permission Boundary, High, Approved), EBG-0065 (STD-0006 Configuration and Secrets Standard, High, Approved), and the remaining Section 5A theme candidates. The Programme Sponsor selected **EBG-0112 (Voice/Vision faculty scoping)**.

EBG-0112's own registration text is explicit that "no implementation, scoping or architecture decision is authorised by this entry - a future session should define the actual Voice/Vision faculty scope... via its own Engineering Implementation Package when the Programme Sponsor selects it as a session objective." This session's objective is therefore scoping, per that same pattern established at ESR-0039 for EBG-0108: produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval. Whether implementation proceeds within this same session depends on what that review and approval actually authorise.

---

# 4. Engineering Authority

ESR-0040 opening was authorised by direct Programme Sponsor instruction on 29 July 2026, following review of PBK-0001, README.md, PST-0001 and ESR-0039, confirming [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit scoping question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Scope [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0112 (JRM-0001 Track B Phase 6, Voice/Vision): define, against [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s existing faculty architecture, the concrete first increment of Voice/Vision that Guardian's live conversation path could deliver next, and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before any code is written.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0112: scope, design and implement Voice/Vision Phase 6 Increment A (speech output); Codex design review; Programme Sponsor approval | Complete |
| WP2 | Session-wide Independent Repository Verification | Complete - Pass, no findings |
| WP3 | Session-wide Repository Baseline Determination | Complete - Establish (RBL-0025) |

---

# 6A. WP1 - EBG-0112: Voice/Vision Phase 6 Scoping

Reviewed `sentinel/providers.py`, `sentinel/openai_provider.py`, `sentinel/provider_config.py`, `jarvis/guardian/runtime.py`, `jarvis/guardian/config.py`, `jarvis/interfaces/conversation.py`, [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8 and [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s Voice/Vision Services sections before drafting scope. Confirmed directly against the live code: no voice or vision code exists anywhere in the repository; `ProviderResponse.content` is a validated non-empty `str` (text-only), making the existing `ExecutionProvider` abstraction unsuited to binary audio without either violating its contract or widening blast radius across every working text adapter.

Produced [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] (v0.1, Draft): scopes a deliberately narrow first increment of Voice Phase 6 - Guardian speech **output** only (text-to-speech via a new ElevenLabs-backed Sentinel provider), via a new parallel `SpeechSynthesisProvider`/`SpeechSynthesisRequest`/`SpeechSynthesisResponse` contract rather than extending the existing text-only provider abstraction. Speech input (microphone/STT) and Vision are explicitly excluded as separate future increments, reasoned against [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1's Household Role Model: output-only voice introduces no new data collection or household-member attribution, unlike microphone or camera input.

Submitted to Codex for design review via the AIEMS Exchange Bridge, run in `-s read-only` sandbox mode per the established EBG-0096 pattern - **no blocking findings**. Codex confirmed the parallel-contract design decision and the output-only/GAM-0001 exclusion boundary were both sound; one non-blocking clarification (settle `GuardianRuntime.speak()`'s return shape as a dedicated `SpeechOutcome` envelope with named, separately-testable status outcomes, rather than leaving it open) folded into v0.2. Codex's own `return-findings` call failed inside its read-only sandbox (write-permission error on the work-package lock file, the same disclosed limitation recorded in EBG-0096's history); its findings were relayed verbatim into the bridge transcript by the Engineering Implementer under explicit per-instance Programme Sponsor approval for that relay act, matching the EIP-ESR0039-001 precedent.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**v1.0 implemented against ElevenLabs exactly as scoped**: `sentinel/speech_providers.py` (new) parallel contracts; `sentinel/elevenlabs_provider.py` (new) modelled on `OpenAIProvider`'s pattern; `jarvis/interfaces/voice.py` (new) `SentinelGatedSpeechProvider` plus the `SpeechOutcome` envelope; `jarvis/guardian/runtime.py`'s `speak()` method. 22 new tests; full suite 418 passed, 1 skipped.

**Live validation (EIP Section 10) failed**: a single real `GuardianRuntime.speak()` call returned `HTTP 402 Payment Required` from ElevenLabs - the available account is on the Free plan, which blocks API access to library voices entirely. The adapter's own error handling behaved exactly as designed (real request, safely-wrapped real failure, honest `unavailable` outcome, no fabricated result) - this was an account/billing constraint, not a code defect. Disclosed to the Programme Sponsor, who identified that ElevenLabs (and a considered alternative, Azure Speech Services) would be genuinely new paid-cloud-vendor relationships with zero prior footprint in this repository, in tension with the project's standing no-discretionary-budget/self-hosted default, and directed a pivot to a self-hosted provider.

**EIP-ESR0040-001 revised to v1.1/v1.2**: the ElevenLabs adapter replaced with `PiperProvider` (`sentinel/piper_provider.py`), backed by the self-hosted Piper local neural TTS engine (`piper-tts`, the project's first runtime dependency beyond `psutil` - no API key, no account, no recurring cost). Confirmed working end to end before drafting the revision (`PiperVoice.load()` + `synthesize_wav()` producing a real 178KB WAV file from real text). Resubmitted to Codex for design review of the swap specifically - **no blocking findings**; all three submitted design questions (endpoint reuse for a local model path; eager model-load-at-construction; the new ML-dependency-surface risk) answered favourably, with two non-blocking clarifications folded into v1.2 (explicit `endpoint` path contract; bounded `piper-tts` version constraint and `import piper` localised inside `sentinel/piper_provider.py` only). Codex's `return-findings` again failed inside its read-only sandbox; relayed verbatim under explicit per-instance Programme Sponsor approval, as before. Programme Sponsor approval for the revision separately verified via `submit-response` against the real Sponsor Approval Service.

**v1.2 implemented exactly as scoped.** `sentinel/elevenlabs_provider.py` and its test file removed; `sentinel/piper_provider.py` (new) added, with the exact `endpoint`-path contract and `RuntimeError` wrapping Codex's review required, and `import piper` localised to its real-construction path only so fake-seam tests never pay the ML dependency's import cost. `pyproject.toml` gained `piper-tts>=1.6.0,<2.0`. `sentinel/speech_providers.py`, `jarvis/interfaces/voice.py` and `jarvis/guardian/runtime.py`'s `speak()` are unchanged from v1.0 - only the specific provider adapter and its dependency changed. 22 new tests (six for `PiperProvider`, replacing the six removed ElevenLabs tests); full suite 418 passed, 1 skipped (was 396/1, no regressions). [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (EBG-0112 marked Complete (Increment A)) all describe the final Piper-based delivery, not the superseded ElevenLabs draft.

**Live validation (EIP Section 10) confirmed end to end.** A real `GuardianRuntime.speak()` call, routed through the real `SentinelGatedSpeechProvider` and the real `PiperProvider` (local `en_US-lessac-medium` voice model, no fake seam), returned `status="synthesized"` with a genuine 190,508-byte `audio/wav` payload. A second, unconfigured `GuardianRuntime` correctly returned `status="not_connected"` with no audio - the honest no-provider boundary, not a fabricated result.

- Files: `sentinel/speech_providers.py` (new), `sentinel/piper_provider.py` (new), `jarvis/interfaces/voice.py` (new), `jarvis/guardian/runtime.py`, `pyproject.toml`, `jarvis/tests/test_speech_providers.py` (new), `jarvis/tests/test_piper_provider.py` (new), `jarvis/tests/test_voice_interface.py` (new), `jarvis/tests/test_guardian_runtime.py`, [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[JRM-0001_PROJECT_ROADMAP|JRM-0001]], [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- `python -m pytest`: 418 passed, 1 skipped (was 396 passed, 1 skipped - 22 new tests, no regressions).
- `python scripts/validate_repository.py` (full mode): 0 errors, 192 warnings (was 190 - two new cross-document Section-reference false positives, consistent with the established disclosed category).
- Committed as `6f595ab` (`1399c4f..6f595ab`), pushed to `origin/main`.

---

# 6B. Session-Wide WP2 - Independent Repository Verification

**Pass, no findings.** Codex independently reviewed the real pushed diff for commit range `1399c4f..6f595ab` via a fresh, read-only CLI pass: confirmed the diff touches exactly the 15 claimed files and none outside that scope, confirmed no `src/`, `src-tauri/`, `jarvis/memory/` or `.github/workflows/` file was touched, confirmed no change to `ConversationRequest`, `ProviderRequest`, `ExecutionProvider`, `SentinelGatedConversationProvider` or any existing text-generation provider adapter, confirmed (via `git ls-files`) that `sentinel/elevenlabs_provider.py` and its test file are genuinely absent from the final committed tree, and spot-checked `PiperProvider` against the approved v1.2 design (localised `import piper`, required/validated `endpoint`, safe `RuntimeError` wrapping). Independently re-ran `python scripts/validate_repository.py`: 0 errors, 192 warnings, matching this session's own evidence. Independently attempted `python -m pytest` but could not complete it in Codex's own read-only sandbox (`FileNotFoundError: No usable temporary directory found`) - the same disclosed, pre-existing Codex read-only-sandbox limitation recorded in EBG-0096's history, not a new issue or evidence against this session's own 418-passed/1-skipped result. Codex's `return-findings` call again failed inside its sandbox; relayed verbatim under explicit per-instance Programme Sponsor approval.

- `python scripts/validate_repository.py` (full mode): 0 errors, 192 warnings throughout - unchanged from WP1's close.

---

# 6C. Session-Wide WP3 - Repository Baseline Determination (RBL-0025 Established)

**Both independent verification passes recommended establishing a new baseline** rather than retaining RBL-0024: the pre-commit Codex design reviews (two rounds, both Pass) and the post-commit Codex diff review (Pass, no findings) all confirmed WP1 delivered a genuine, live-verified product code change - Guardian's first Voice faculty capability, backed by new test coverage (22 new tests) and a real end-to-end live audio-synthesis confirmation. The Programme Sponsor's determination: **establish** - [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] is accepted as the new current repository baseline, superseding [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]].

- `python -m pytest`: 418 passed, 1 skipped throughout. `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count held at 192 across this WP's own governance edits.

---

# 7. Related Artefacts

* [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed for WP0A/WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0112 (this session's objective).
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] - the approved architecture the scoping must be defined against.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Section 7.3, Phase 6, the roadmap placement motivating this session's objective selection.
* [[RBL-0024_REPOSITORY_BASELINE|RBL-0024]] - repository baseline at session open.
* [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] - this session's WP1 deliverable, design-reviewed by Codex (no blocking findings), pending Programme Sponsor approval.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.4 | 29 July 2026 | Claude Engineering Implementer | ESR-0040 formally closed. Session-wide WP2 (Independent Repository Verification: Pass, no findings) and WP3 (Repository Baseline Determination: Establish - RBL-0025 accepted, superseding RBL-0024) complete, per explicit Programme Sponsor decision. |
| 1.3 | 29 July 2026 | Claude Engineering Implementer | WP1 finalised: v1.0's ElevenLabs implementation failed live validation (HTTP 402, Free-plan API restriction) and was superseded, on Programme Sponsor direction, by a self-hosted Piper local-TTS adapter (`sentinel/piper_provider.py`) - the project's first runtime dependency beyond `psutil`. Revision separately Codex design-reviewed (no blocking findings) and Programme Sponsor-approved via the real Sponsor Approval Service. `sentinel/elevenlabs_provider.py` and its tests removed; `sentinel/piper_provider.py` and its tests added. 22 new tests, full suite 418 passed/1 skipped. AAM-0001, JRM-0001 and EBR-0001 (EBG-0112 Increment A Complete) updated to describe the final Piper-based delivery. |
| 1.2 | 29 July 2026 | Claude Engineering Implementer | WP1 Complete: Codex design review no blocking findings (one non-blocking clarification folded into v0.2), Programme Sponsor approval verified via `submit-response` against the real Sponsor Approval Service, Voice Faculty Phase 6 Increment A (speech output) implemented exactly as scoped against ElevenLabs (later superseded - see v1.3). 22 new tests, full suite 418 passed/1 skipped. AAM-0001, JRM-0001 and EBR-0001 (EBG-0112 Increment A Complete) updated. |
| 1.1 | 29 July 2026 | Claude Engineering Implementer | WP1 In Progress: drafted [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] v0.1 scoping Voice Phase 6 Increment A (speech output only), submitted to Codex for design review (no blocking findings, one non-blocking clarification folded into v0.2). No source code changed. Programme Sponsor approval pending. |
| 1.0 | 29 July 2026 | Claude Engineering Implementer | ESR-0040 opened at WP0B, before WP1 began. Objective: scope EBG-0112 (Voice/Vision, JRM-0001 Track B Phase 6) and produce an Engineering Implementation Package for Codex review and Programme Sponsor approval. |
