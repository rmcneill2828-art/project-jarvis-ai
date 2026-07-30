# EIP-ESR0042-001 - Higher-Quality Guardian Voice Model

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0042-001 |
| Artefact ID | EIP-ESR0042-001 |
| Title | Higher-Quality Guardian Voice Model |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0113 |
| Intended Session | ESR-0042 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0113 was registered at ESR-0040 closure following the Programme Sponsor's own direct observation after hearing EBG-0112 Increment A's live speech output: "will we able to provide a more realistic voice later down the line." Its own registration text withholds authority: "No implementation, evaluation or model selection is authorised by this entry." This package is that evaluation and selection.

`sentinel/piper_provider.py`'s `PiperProvider` already accepts any local `.onnx` voice model path via `ProviderConfiguration.endpoint` (confirmed directly against the live code) - no code change is required to point it at a different model file. However, confirmed directly against the repository: no default Piper model path is wired anywhere in source (`jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` does not construct a speech provider at all; `en_US-lessac-medium` appears only as a fake path string inside `jarvis/tests/test_piper_provider.py`, never as a production constant). The model file itself is not and should not be committed to the repository (see Constraints) - ESR-0040's own Voice faculty delivery already disclosed voice-model acquisition as "a disclosed, one-time manual setup step," never triggered automatically by `PiperProvider` itself (EIP-ESR0040-001 Section 6 item 9).

---

# 3. Objective

Select a specific higher-quality Piper voice model, obtain genuine live evidence (not automated-output-only) that it is actually an improvement over the `en_US-lessac-medium` model validated at ESR-0040, and record that selection - without wiring a default speech provider into `build_default_runtime()`, which remains separate, unauthorised scope (see Section 11, New Backlog Item).

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `sentinel/piper_provider.py` `PiperProvider.__init__` | Requires `configuration.endpoint` (a local filesystem path to a `.onnx` model, with its companion `.onnx.json` alongside it); loads the model once at construction (~3.5s measured at ESR-0040). No change needed to accept a different model path - this is exactly what the existing contract is for. |
| `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` | Confirmed via direct grep: does not construct or wire any speech provider at all. `GuardianRuntime.speak()` is reachable only when a caller explicitly injects a `speech_provider` at construction (`jarvis/guardian/runtime.py` constructor parameter) - the live Tauri UXP's default runtime has no voice capability wired in today. ESR-0040's live validation (EIP-ESR0040-001 Section 10) was performed via a standalone, non-committed script constructing `GuardianRuntime` with a `PiperProvider` injected directly, not through the running application. |
| Model provenance (verified this session via direct web lookup, not assumed from training data) | `rhasspy/piper-voices` on Hugging Face (`https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US`) hosts the `en_US` voice catalogue actually used at ESR-0040. `en/en_US/lessac/` (`https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac`) contains three quality tiers: `low`, `medium` (already validated at ESR-0040) and `high`. `en/en_US/lessac/high/` (`https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/high`) contains `en_US-lessac-high.onnx` (114 MB) and its companion `en_US-lessac-high.onnx.json` (4.88 kB) - the same file-pair shape `PiperProvider` already requires. Per Piper's own convention, "high" denotes a larger model (~28M parameters vs medium's ~15M), not a higher output sample rate - both remain 22.05 kHz, the same infrastructure already proven working at ESR-0040. |
| EBG-0112's own provider evaluation (ESR-0040) | Considered Kokoro (a materially more natural-sounding alternative, PyTorch-based) and set it aside in favour of Piper's lighter ONNX-runtime dependency footprint for the first increment - EBG-0113's own text confirms Kokoro "remains a live option if voice quality becomes the priority over dependency weight." This package evaluates a same-engine quality upgrade (Piper medium to high) rather than reopening the Piper-vs-Kokoro engine decision, which is a materially larger scope (a new dependency stack) not requested by EBG-0113's own text. |

---

# 5. Scope

This package authorises:

1. **Evaluation**: compare `en_US-lessac-medium` (current, ESR-0040-validated) against `en_US-lessac-high` (candidate) - same voice dataset/identity (Lessac), same Piper engine, same file-pair contract `PiperProvider` already requires. This is deliberately the narrowest possible "higher quality" change: it changes model size/fidelity only, not voice identity, dependency stack, or code.
2. **One-time manual model acquisition** (Programme Sponsor's own machine, outside the repository): download `en_US-lessac-high.onnx` and `en_US-lessac-high.onnx.json` from `rhasspy/piper-voices` on Hugging Face to a local path, alongside the already-downloaded `en_US-lessac-medium` files from ESR-0040. Neither model file is committed to the repository - both remain local, disclosed, Sponsor-machine configuration, matching the precedent already established for the medium model.
3. **Live comparison**: synthesize the same test utterance (matching ESR-0040's own validation utterance, "Hello Robert. This is Guardian. If you can hear this, speech output is working correctly." or an equivalent fixed sentence) through the real `PiperProvider` against both model paths, producing two real `.wav` files - no fake seam, no automated-output-only claim.
4. **Genuine Programme Sponsor Validation** (PBK-0001 Repository Lifecycle step 3 / PST-0001 workflow step 4, applied proactively this time rather than corrected post-hoc as ESR-0040 required): the Programme Sponsor personally listens to both files and confirms, in their own words, whether `lessac-high` is actually a perceptible improvement - not an Engineering Implementer assertion that "the model is objectively higher quality" based on parameter count alone.
5. **Recording the outcome**: if the Programme Sponsor confirms `lessac-high` as an improvement, [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0113 is marked Complete, recording `en_US-lessac-high` as the recommended default model reference for a future implementation package to wire in (Section 11 new backlog item). If the Sponsor does not confirm an improvement (or prefers the existing medium model for other reasons - e.g. synthesis latency, file size), EBG-0113 is marked Complete on the basis that the evaluation was genuinely performed, recording the negative or mixed result honestly rather than only recording a positive outcome.

No code file is authorised to change under this package - `sentinel/piper_provider.py`'s existing `endpoint`-configuration contract already supports everything this package needs.

---

# 6. Authorised Files

1. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No source code file is authorised to change. No other governance artefact is authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. The comparison utterance must be identical for both models - no wording change between the two synthesis calls, so any perceived difference is attributable to the model, not the text.
2. Both `.wav` files must be produced via the real `PiperProvider.synthesize()` call path (the same class used in production), not a direct/bypassed call into the `piper` package - matching this project's no-fake-seam-for-live-validation discipline (PBK-0001 Operational Verification Before Reporting).
3. The Programme Sponsor's actual verdict (improvement confirmed / not confirmed / mixed) must be recorded verbatim or in close paraphrase in EBR-0001's EBG-0113 entry - not summarised as a bare "Complete" with no disclosed listening outcome, matching the ESR-0040 post-hoc correction precedent this package is designed to avoid repeating.
4. Both `.onnx`/`.onnx.json` file pairs remain outside the repository (`.gitignore`-equivalent by simply never being staged) - this package does not authorise committing binary model files.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Wiring any speech provider into `build_default_runtime()` or otherwise connecting Voice output to the live running Tauri UXP by default - that is a distinct, larger gap (Section 11 new backlog item), not requested by EBG-0113's own text and not evaluated by this package's live-comparison scope.
2. Reopening the Piper-vs-Kokoro (or any other TTS engine) decision - EBG-0112's own evaluation already considered and set that aside for dependency-footprint reasons; this package stays within the Piper engine already approved and shipped.
3. Evaluating any voice identity other than Lessac (e.g. Ryan, LibriTTS) - EBG-0113's own framing is about quality, not a voice-identity change, which would be a materially different (more subjective, UX-facing) decision.
4. Any change to `sentinel/piper_provider.py`, `sentinel/speech_providers.py`, `jarvis/interfaces/voice.py` or `jarvis/guardian/runtime.py` - the existing contract already supports this package's scope without modification.
5. Committing any `.onnx`/`.onnx.json` model file to the repository.

---

# 9. Constraints

1. No EBR-0001 status change shall be recorded until the live comparison has actually been performed and the Programme Sponsor's genuine verdict obtained - per PBK-0001 Principle 2 (Evidence Before Conclusion) and Principle 4 (Validation Before Completion).
2. This package must be reviewed by the Engineering Reviewer (Codex) at design stage before the live comparison proceeds, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0041.
3. Model file provenance (source URL, file sizes) must be independently verifiable, not asserted from training-data memory alone - confirmed this session via direct web lookup against `huggingface.co/rhasspy/piper-voices`, matching PBK-0001 Principle 2's evidence requirement.

---

# 10. Validation

After the Programme Sponsor downloads `en_US-lessac-high.onnx`/`.onnx.json` to their machine:

1. Run a short comparison script (not committed to the repository, matching the pattern of ESR-0040's own uncommitted validation script) that constructs two `PiperProvider` instances - one per model path - and synthesizes the identical test utterance through each, writing two `.wav` files to the Programme Sponsor's Desktop (matching the exact ESR-0040 post-hoc-validation delivery mechanism the Sponsor already confirmed works).
2. The Programme Sponsor personally plays both files and reports their verdict.
3. `python -m pytest` and `python scripts/validate_repository.py` re-run to confirm no regression (expected unchanged, since no code file is authorised to change).

---

# 11. Risks and Dependencies

## Dependencies

None new for the evaluation itself. Depends on the Programme Sponsor completing a one-time ~114 MB manual download - the same category of dependency already accepted for the medium model at ESR-0040, not a new kind of dependency this package introduces.

## Risks

1. **`high` denoting model size, not guaranteed perceptual quality, is Piper's own convention, not this package's claim** - a larger model does not guarantee the Programme Sponsor will perceive an improvement large enough to justify the size/latency cost. This is exactly why Section 5 item 4 requires a genuine listening verdict rather than assuming "high > medium" from the tier name alone.
2. **114 MB is a materially larger download than the medium model** (exact medium-tier size not independently re-verified this session, but disclosed as smaller per Piper's own parameter-count convention) - a real cost to disclose, not hide, consistent with EIP-ESR0040-001's own disclosure of the `piper-tts` dependency's install cost.

## New Backlog Item Registered by This Draft

**EBG-0114** (Candidate Backlog, registered at draft time per the established EIP-ESR0031-001/EIP-ESR0039-001 pattern): confirmed this session that `build_default_runtime()` does not wire any speech provider into the live Tauri UXP's default runtime - `GuardianRuntime.speak()` is reachable only via manual construction with an explicitly injected `PiperProvider`, meaning the Voice faculty delivered at ESR-0040 is not actually reachable through the running product today, only through ad hoc validation scripts. A future implementation package should scope: an environment-variable-driven default model path (mirroring `JARVIS_OLLAMA_MODEL`'s existing pattern), whether wiring should be unconditional or feature-flagged, and how the UXP should expose a "speak this response" affordance (currently no `src/`/`src-tauri/` UI surface calls `guardian.speak` at all). No implementation authorised by this entry.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via the AIEMS Exchange Bridge (`ESR-0042`/`WP1`), reviewed by direct `codex exec -s read-only` invocation per the established EBG-0096 pattern. **Result: Pass, with a non-blocking caveat and minor non-blocking findings.** Codex independently verified `PiperProvider`'s `endpoint` contract (`sentinel/piper_provider.py`, `sentinel/provider_config.py`) and confirmed `build_default_runtime()` genuinely wires no speech provider (`jarvis/interfaces/stdio_rpc.py`), matching this package's claims. Codex's own sandbox hit the same disclosed spawn-error limitation reading `EBR-0001` directly (could not independently verify the exact EBG-0113/EBG-0114 row text, but found the described consistency conceptually sound from the EIP's own quoted content). Confirmed: the Lessac-only/Piper-only scope boundary is correct for EBG-0113's text; Section 5 item 5's honest-negative-result handling is correct; EBG-0114 is correctly scoped as separate future work; the no-code Authorised Files list is right. Non-blocking: preserve source URL evidence for auditability (addressed in v0.2 below), and the exact 114 MB/4.88 kB figures were not independently re-verified by Codex in its own sandbox (this session's own direct web lookup stands as the evidence).

**v0.2**: Section 4's model provenance row now cites the exact Hugging Face source URLs (`rhasspy/piper-voices` tree paths for `en_US`, `lessac`, and `lessac/high`) alongside the file sizes, addressing Codex's auditability suggestion.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before the live comparison proceeded.

**Live comparison performed exactly as scoped.** Both `en_US-lessac-medium` and `en_US-lessac-high` were downloaded via `piper-tts`'s own bundled `python -m piper.download_voices` CLI (a real, disclosed download mechanism - not requiring a manual browser download after all, correcting this package's earlier assumption) to a local, uncommitted directory (`.voice-models-local/`, confirmed untracked via `git status`, deleted after the comparison). The identical test utterance was synthesized through the real `PiperProvider.synthesize()` call path against both model paths, producing two genuine `.wav` files (`medium`: 202,284 bytes; `high`: 223,788 bytes) written to the Programme Sponsor's own Desktop.

**Programme Sponsor Validation - genuine, proactive (not corrected post-hoc as ESR-0040 required): the Programme Sponsor personally listened to both files and reported, in their own words, "honestly i cant tell any differnce between them - they sound the same."** No perceptible improvement from `lessac-high` despite its materially larger model size (~28M vs ~15M parameters, ~108.6 MB vs ~60.3 MB on disk) and correspondingly larger one-time download cost. This is the honest negative result Section 5 item 5 anticipated, not a positive outcome - EBG-0113 is marked Complete on the basis that the evaluation was genuinely performed, recording that the Programme Sponsor did not confirm an improvement, and that the existing `en_US-lessac-medium` model remains the better choice on a cost/benefit basis (materially smaller download, no perceptible quality tradeoff for this utterance). Switching to `lessac-high` is explicitly not recommended by this outcome.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0113 (this package's parent item, to be marked Complete on approval and live validation); EBG-0114 (new, registered by this draft). |
| [[EIP-ESR0040-001_VOICE_PHASE6_INCREMENT_A_SPEECH_OUTPUT_SCOPE|EIP-ESR0040-001]] | Delivered the `en_US-lessac-medium` baseline and `PiperProvider` contract this package evaluates against. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Records the Voice faculty this package's evaluation informs; not itself changed by this package. |
| [[ESR-0042_ENGINEERING_SESSION_REPORT|ESR-0042]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change, Evidence Before Conclusion and Operational Verification Before Reporting discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Programme Sponsor approved**, verified via `submit-response` against the real Sponsor Approval Service. **Live comparison performed**: both models downloaded via `piper-tts`'s own `download_voices` CLI (no manual browser download needed after all); identical utterance synthesized through the real `PiperProvider` for both; two genuine `.wav` files written to the Programme Sponsor's Desktop. **Programme Sponsor Validation**: no perceptible difference reported ("honestly i cant tell any differnce between them - they sound the same"). EBG-0113 marked Complete recording this honest negative result - `lessac-high` is not recommended; `lessac-medium` remains the better cost/benefit choice. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: Pass, non-blocking caveat and findings. Added explicit Hugging Face source URLs to Section 4's model provenance row, addressing the auditability suggestion. Pending Programme Sponsor approval. |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0042 WP1. Registers EBG-0114 (Candidate Backlog) in EBR-0001. Not yet reviewed or approved. |
