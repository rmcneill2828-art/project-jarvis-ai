# ESR-0042 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0042 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0042 |
| Date Opened | 30 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 complete |

---

# 2. Purpose

This report records the opening and execution of ESR-0042, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]] closed (30 July 2026), [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] the current accepted baseline (retained at ESR-0041), working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), PBK-0001 confirmed unchanged since last read (still last touched at ESR-0036). No open [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] item concerns documentation staleness as its own category, so PBK-0001's Documentation-Debt Priority discipline does not constrain WP0/WP1 selection this session.

**Observation disclosed at WP0A:** ESR-0041 was governance/architecture-only (no code, no UXP progress). PBK-0001's Feature-First Delivery Discipline does not forbid an occasional architecture-only session (ESR-0023's GAM-0001 creation is the standing precedent), but this was flagged to the Programme Sponsor ahead of objective selection so it would inform, not silently repeat.

`scripts/session_launcher.py` was run to surface candidate objectives. Presented to the Programme Sponsor: EBG-0113 (Higher-Quality Guardian Voice Model, newly registered at ESR-0040 closure), EBG-0085 (esbuild/vite dev-server vulnerability), EBG-0065 (STD-0006 Configuration and Secrets Standard, High, Approved), EBG-0038/0046/0042 (architecture-only candidates), and the remaining Section 5A theme candidates. **The Programme Sponsor selected EBG-0113 (Higher-Quality Guardian Voice Model)**, a genuine product-code-adjacent deliverable following the architecture-only ESR-0041.

EBG-0113's own registration text explicitly withholds authority: "No implementation, evaluation or model selection is authorised by this entry." This session's objective is therefore to evaluate the available higher-quality Piper voice options, select and live-validate a specific model against the real `en_US-lessac-medium` baseline delivered at ESR-0040, and produce an Engineering Implementation Package for Codex review and Programme Sponsor approval - matching the scoping-first pattern established at ESR-0039/0040/0041.

---

# 4. Engineering Authority

ESR-0042 opening was authorised by direct Programme Sponsor instruction on 30 July 2026, following review of PBK-0001, README.md, PST-0001 and ESR-0041, confirming [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit objective-selection question that also disclosed ESR-0041's architecture-only shape.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Evaluate [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0113 (Higher-Quality Guardian Voice Model): select a concrete higher-quality Piper voice model against `en_US-lessac-medium` (the model validated at ESR-0040), obtain genuine live evidence (not automated-output-only) that the alternative is actually better, and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before any repository or configuration change.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0113: evaluate and select a higher-quality Piper voice model; live comparison; Codex design review; Programme Sponsor approval | Complete |
| WP2 | Session-wide Independent Repository Verification | Pending |
| WP3 | Session-wide Repository Baseline Determination | Pending |

---

# 6A. WP1 - EBG-0113: Higher-Quality Guardian Voice Model

Reviewed `sentinel/piper_provider.py`, `sentinel/provider_config.py` and `jarvis/interfaces/stdio_rpc.py` before drafting scope. Confirmed directly against the live code: `PiperProvider` already accepts any local `.onnx` model path via `ProviderConfiguration.endpoint` (no code change required to point it at a different model), but `build_default_runtime()` does not wire any speech provider at all - `en_US-lessac-medium` (the model validated at ESR-0040) exists only as a fake path string in a unit test, never as a production default. Verified via direct web lookup (not assumed from training data) that `rhasspy/piper-voices` on Hugging Face hosts `en_US-lessac-high` alongside the already-used `en_US-lessac-medium` - same voice identity, larger model (~28M vs ~15M parameters).

Produced [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] (v0.1, Draft): scopes a narrow, same-engine, same-voice-identity quality comparison (`lessac-medium` vs `lessac-high`) rather than reopening the Piper-vs-Kokoro engine decision or evaluating a different voice identity - deliberately no code change, since the existing `endpoint` configuration contract already supports it.

Submitted to Codex for design review via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern - **Pass, with one non-blocking auditability finding** (preserve exact Hugging Face source URLs for the model provenance claim), folded into v0.2. Codex independently confirmed the `PiperProvider`/`ProviderConfiguration` contract claims and the `build_default_runtime()` wiring gap directly against the live code.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service before the live comparison proceeded.

**Live comparison performed exactly as scoped.** Both `en_US-lessac-medium` and `en_US-lessac-high` were downloaded via `piper-tts`'s own bundled `python -m piper.download_voices` CLI (correcting this package's initial assumption that a manual browser download was required) to a local, uncommitted directory, deleted after the comparison. The identical test utterance was synthesized through the real `PiperProvider.synthesize()` call path against both models, producing two genuine `.wav` files (202,284 and 223,788 bytes) written to the Programme Sponsor's Desktop.

**Genuine Programme Sponsor Validation, proactive this time (not corrected post-hoc as ESR-0040 required).** The Programme Sponsor personally listened to both files and reported: "honestly i cant tell any differnce between them - they sound the same." Honest negative result: `lessac-high` is not a perceptible improvement despite its materially larger size (~108.6 MB vs ~60.3 MB on disk); `lessac-medium` remains the better cost/benefit choice. No code changed.

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0113 marked Completed, recording the honest result rather than only a positive outcome; EBG-0114 registered (Candidate Backlog, Medium) - `build_default_runtime()` does not wire any speech provider, so the Voice faculty (EBG-0112) remains unreachable through the live running product, a genuinely new finding surfaced while scoping this package.

- Files: `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] (new).
- `python -m pytest`: 418 passed, 1 skipped (unchanged - no code touched).
- `python scripts/validate_repository.py` (full mode): 0 errors (warning count reported at session close).
- Committed and pushed to `origin/main` (SHA reported at session close).

---

# 7. Related Artefacts

* [[ESR-0041_ENGINEERING_SESSION_REPORT|ESR-0041]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed for WP0A/WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0113 (this session's objective).
* [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] - delivered the baseline `en_US-lessac-medium` Voice faculty (EBG-0112) this session evaluates against.
* [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] - repository baseline at session open.
* [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] - this session's WP1 deliverable, Codex design-reviewed (Pass) and Programme Sponsor-approved via the real Sponsor Approval Service.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 30 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0113 (Higher-Quality Guardian Voice Model) evaluated via EIP-ESR0042-001 (Codex design review Pass). Real live comparison of `en_US-lessac-medium` vs `en_US-lessac-high` - Programme Sponsor personally listened to both and reported no perceptible difference. EBG-0113 marked Completed recording the honest negative result; EBG-0114 registered (Voice faculty not wired into `build_default_runtime()`, discovered while scoping this package). No code changed. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | ESR-0042 opened at WP0B, before WP1 began. Objective: evaluate EBG-0113 (Higher-Quality Guardian Voice Model), select and live-validate a candidate against the ESR-0040 baseline, and produce an Engineering Implementation Package for Codex review and Programme Sponsor approval. |
