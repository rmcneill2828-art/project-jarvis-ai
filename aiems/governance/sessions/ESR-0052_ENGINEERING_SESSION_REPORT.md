# ESR-0052 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0052 |
| Title | Engineering Session Report |
| Version | 1.6 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0052 |
| Date Opened | 26 August 2026 |
| Date Closed | (not yet closed) |
| Closure Status | Open - WP1 complete and implemented; WP2 investigation complete; WP3 implemented, EBG-0115 disposition awaits Programme Sponsor listening verdict |

---

# 2. Purpose

This report records the opening and execution of ESR-0052, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened at the Programme Sponsor's direct request, following [[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]] (a technology/code/AI-practice review requested ~3 months into the project) and its instruction to draft a Work Package informed by that review's findings. WP0A/WP0B session initialisation follows [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (re-reviewed in full at the Programme Sponsor's explicit request as part of this session's opening) and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

**WP0 - Technology, Code and AI-Landscape Review** was performed ahead of formally opening this session, in the form of a Working Report ([[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]]) rather than a controlled artefact, per the Working Report Lifecycle. Live-evidence-verified (`pytest` 523 passed/1 skipped; `validate_repository.py` 0 errors/292 warnings; `pip-audit`, `npm audit`/`npm outdated`, `git status` against `origin/main`), submitted to Codex Engineering Reviewer via the AIEMS Exchange Bridge (`ESR-0052`/`WP0-technology-review`) for independent cross-review - **Conditional Pass with corrections** (a genuine unresolved-WikiLink defect the report's own drafting introduced, plus a git-status wording overstatement), both folded in. A separate ad hoc ChatGPT/Codex second opinion, obtained by the Programme Sponsor outside the AIEMS Exchange Bridge, was independently verified against the real repository and reconciled into the report as a distinct, clearly-labelled addendum (Section 10) - two of its three code findings confirmed with scope/mechanism corrections, one partly overstated, and its OpenAI-landscape claims (GPT-5.6, Responses-API MCP-native default) confirmed accurate by web search. WR-ESR0052-001 was committed and pushed (`7b8b3d5`) directly by the Programme Sponsor, per this project's standing Git-operations authority model.

The Programme Sponsor selected this session's initial objective directly: draft a Work Package informed by WR-ESR0052-001's findings. **WP1** clears the three concrete, low-risk currency-drift items identified by that review (EBG-0122 frontend dependency vulnerability remediation, EBG-0123 dependency-freshness automation, EBG-0124 `pip-audit` CI gate hardening) - drafted in [[EIP-ESR0052-001_PROCESS_TOOLING_CURRENCY_CLUSTER|EIP-ESR0052-001]], Codex design-reviewed via the AIEMS Exchange Bridge (`ESR-0052`/`WP1`, **Conditional Pass with correction**, folded in - v0.2), **approval-to-implement verified via the real Sponsor Approval Service** (`submit-response`, ESR-0052/WP1) before any code was written, and **implemented exactly as scoped in v0.2**:

* **EBG-0122**: `npm audit fix` (non-forced) ran cleanly, touching only `package-lock.json` (7 lines) - no `package.json` version-range change required. `nanoid`/`postcss` both cleared; `npm run build` re-verified clean. `esbuild`/`vite` (moderate/high, requiring the major Vite bump) remain, exactly as scoped.
* **EBG-0123**: new `.github/dependabot.yml` - four ecosystems (`npm`/`pip` at `/`, `cargo` at `/src-tauri`, `github-actions` at `/.github/workflows`), weekly, no auto-merge.
* **EBG-0124**: `continue-on-error: true` removed from `.github/workflows/ci.yml`'s `pip-audit` step; its comment updated to reflect the now-triaged baseline. Disclosed, not yet resolved: whether the GitHub-hosted runner's own bundled `pip` is already patched can only be confirmed by the first real CI run after this lands - the actual test, per PBK-0001 Principle 2.

Validation: `python -m pytest jarvis/tests sentinel scripts/tests` - 523 passed, 1 skipped (unchanged, no production code touched); `python scripts/validate_repository.py` (full mode) - 0 errors, 297 warnings; `npm run build` clean; both new/edited YAML files (`ci.yml`, `dependabot.yml`) confirmed to parse via `yaml.safe_load`.

**Post-commit independent review** (direct `codex exec -s workspace-write` invocation against the real pushed commit `28dbf29`, diff `7b8b3d5..28dbf29`): **Conditional Pass with limitation.** Codex independently re-ran `git show --stat`/`git diff` and confirmed only the expected files changed (no unexpected `jarvis/`/`sentinel/`/`src/`/`package.json` path); confirmed `ci.yml`'s `pip-audit` step no longer carries `continue-on-error: true`; confirmed `dependabot.yml`'s four ecosystem entries exactly as scoped; confirmed the `package-lock.json` diff bumps only `nanoid` (3.3.15 to 3.3.18) and `postcss` (8.5.16 to 8.5.26); independently re-ran `pytest` (523 passed, 1 skipped, matching) and `validate_repository.py` (0 errors, 297 warnings, matching); confirmed EBR-0001/REG-0001 rows internally consistent. Disclosed limitation, not a finding against the commit: Codex's own environment blocked every `npm audit` invocation before execution, so that specific claim was verified via the lockfile version diff rather than a live re-run - the same class of environment restriction disclosed in this session's earlier reviews.

Per PBK-0001's Feature-First Delivery Discipline, WP1 alone (process/tooling only) does not satisfy "every Engineering Session shall deliver product-moving engineering work" - flagged here plainly, matching the discipline this session's own re-review of PBK-0001 was intended to confirm. WR-ESR0052-001 Section 7 recommended pairing this cluster with a product objective (EBG-0115 Kokoro TTS evaluation or EBG-0111 Composio assessment); the Programme Sponsor selected **EBG-0111 (Composio assessment)** as WP2.

**WP2 - EBG-0111 Composio Assessment (Complete, investigation only):** verified via direct web search, not assumed from memory - Composio's core infrastructure (credential storage, tool execution) is closed-source and cloud-hosted, not self-hostable; only the client SDK/CLI is MIT-licensed. Pricing as of August 2026: a hard-capped free tier and a $29/month Pro tier both require Composio's own cloud to custody every connected external account's OAuth credentials; self-managed credentials (JARVIS/the household keeping custody of its own tokens) sits behind a $599/month tier. **Recommendation: Deferred, not adopted** - the financially-viable tiers conflict with the project's standing self-hosted-first/no-third-party-credential-custody posture, and the credential-custody tier conflicts with the standing no-discretionary-budget-for-tooling constraint; separately, `GAM-0001` Section 8A has no boundary category yet for third-party-cloud-relayed external-service actions regardless of cost. Recorded in EBG-0111's own [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] entry (Candidate Backlog to Deferred). This closes a stale "not yet assessed" item with a real, evidence-based decision - it is not itself a shipped JARVIS capability.

**Feature-First Delivery Discipline note, flagged at WP1/WP2, now resolved by WP3:** WP1 (drafted, not yet implemented) and WP2 (an investigation concluding non-adoption) together did not deliver a shipped, product-moving JARVIS capability - both were process/decision outputs, not a feature added to JARVIS, Guardian or its subsystems. The Programme Sponsor selected **EBG-0115 (Kokoro TTS evaluation) as WP3** to close this gap.

**WP3 - EBG-0115 Kokoro TTS Live Comparison (implemented):** scoped in [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]], Codex design-reviewed via the AIEMS Exchange Bridge (`ESR-0052`/`WP3`, **Conditional Pass with corrections**, folded in - v0.2), **approval-to-implement verified via the real Sponsor Approval Service** (`submit-response`, ESR-0052/WP3) before any code was written, and **implemented exactly as scoped in v0.2** (v1.0):

* New optional `voice-eval` dependency group in `pyproject.toml` (`kokoro-onnx`, `espeakng-loader`, `phonemizer-fork`) - not in the base install.
* New `sentinel/kokoro_provider.py` (`KokoroProvider`), built to the explicit contract Codex's design review required, plus one disclosed implementation-time addition: `_load_synthesizer()` wires `espeakng_loader`'s bundled `espeak-ng` binary/data into `kokoro_onnx` via `EspeakConfig` - without it, synthesis would fail on this self-hosted-first machine's lack of a system `espeak-ng` install. New `jarvis/tests/test_kokoro_provider.py` (7 tests, mirroring `test_piper_provider.py` exactly, no real `kokoro_onnx` import in tests).
* **Live comparison performed for real, not simulated**, mirroring EBG-0113's exact precedent methodology ([[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]]): `en_US-lessac-medium` (current production Piper voice) and Kokoro's model files (`kokoro-v1.0.int8.onnx`, 88 MB quantized; `voices-v1.0.bin`) downloaded to an uncommitted `.voice-models-local/` directory; an uncommitted comparison script synthesized the identical fixed test utterance ("Hello Robert. This is Guardian. If you can hear this, speech output is working correctly.") through the real `PiperProvider` and the real `KokoroProvider` - both succeeded (Piper 223,788 bytes; Kokoro 255,020 bytes, voice `af_sarah`) - writing two genuine `.wav` files to the Programme Sponsor's actual Desktop (OneDrive-redirected path). Models and script deleted after the comparison, confirmed via `git status` to have never entered the repository.
* **No adoption decision made by this package.** EBG-0115 remains **In Progress**, not Completed, in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - its final disposition awaits the Programme Sponsor's own listening verdict on the two delivered files, honest either way, matching EBG-0113's own accepted negative result.

Validation: `python -m pytest jarvis/tests sentinel scripts/tests` - **530 passed, 1 skipped** (up from 523/1 - the 7 new `KokoroProvider` tests, no other production code touched); `python scripts/validate_repository.py` (full mode) - 0 errors, 297 warnings.

This satisfies the Feature-First Delivery Discipline gap flagged at WP1/WP2: a real capability (a working, tested, self-hosted TTS adapter, live-verified against genuine synthesis) now exists in the repository, even though whether it ships further depends on a decision only the Programme Sponsor can make.

---

# 4. Engineering Authority

ESR-0052 opening was authorised by direct Programme Sponsor instruction on 26 August 2026, following WR-ESR0052-001's technology/AI-landscape review, its independent Codex cross-review, and the Programme Sponsor's explicit direction to draft a Work Package informed by it.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

WP1 (drafted, not yet approved-to-implement): clear the EBG-0122 through EBG-0124 process/tooling currency cluster (frontend dependency vulnerability remediation, dependency-freshness automation, `pip-audit` CI gate hardening).

WP2 (complete): investigate and decide EBG-0111 (Composio assessment) - Deferred, not adopted.

WP3 (drafted, not yet approved-to-implement): EBG-0115 - a live Kokoro-versus-Piper voice comparison for the Programme Sponsor's own listening verdict.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0 | Technology, Code and AI-Landscape Review (WR-ESR0052-001, Codex cross-reviewed, ad hoc second opinion reconciled) | Complete |
| WP1 | Clear EBG-0122-0124 process/tooling currency cluster | Complete |
| WP2 | Investigate and decide EBG-0111 (Composio assessment) | Complete - Deferred, not adopted |
| WP3 | EBG-0115 Kokoro TTS live comparison | Implemented - EBG-0115 disposition awaits Programme Sponsor listening verdict |

Further Work Packages will be added if the Programme Sponsor directs the session to proceed beyond WP1/WP3.

---

# 7. Related Artefacts

* [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] - prior closed session, immediate predecessor.
* [[WR-ESR0052-001_TECHNOLOGY_AND_AI_LANDSCAPE_REVIEW|WR-ESR0052-001]] - Working Report produced ahead of this session's opening; source of WP1's objective.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Feature-First Delivery Discipline guidance followed; re-reviewed in full at the Programme Sponsor's explicit request opening this session.
* [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] - current accepted repository baseline at session open.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0122 through EBG-0124 (WP1's target items), EBG-0111 (WP2's investigated and Deferred item) and EBG-0115 (WP3's target item).
* [[EIP-ESR0052-001_PROCESS_TOOLING_CURRENCY_CLUSTER|EIP-ESR0052-001]] - draft Engineering Implementation Package for WP1, not yet reviewed or approved.
* [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] - draft Engineering Implementation Package for WP3, not yet reviewed or approved.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - Section 8A, the boundary-coverage gap WP2's Composio assessment identified for third-party-cloud-relayed external-service actions.
* [[EIP-ESR0042-001_HIGHER_QUALITY_GUARDIAN_VOICE_MODEL|EIP-ESR0042-001]] - EBG-0113's live-comparison methodology, mirrored exactly by WP3.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.6 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP3 Implemented: EBG-0115 (Kokoro TTS) per [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] v1.0. New `sentinel/kokoro_provider.py` (7 tests) and `voice-eval` optional dependency group; genuine live comparison performed (real audio, both providers, two `.wav` files delivered to the Programme Sponsor's Desktop); models/script deleted, never entered the repository. `pytest` 530/1 (up from 523/1), `validate_repository.py` 0 errors/297 warnings. EBG-0115 remains In Progress pending the Programme Sponsor's listening verdict. |
| 1.5 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP1 post-commit independent review: genuine `codex exec -s workspace-write` review of the real pushed commit `28dbf29` (diff `7b8b3d5..28dbf29`) - **Conditional Pass with limitation**. All inspectable scope/governance/pytest/validation checks independently re-run and matched; the only limitation is Codex's own environment blocking `npm audit` execution, verified instead via the lockfile diff. No corrections required. |
| 1.4 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP1 Complete: EBG-0122 through EBG-0124 resolved per [[EIP-ESR0052-001_PROCESS_TOOLING_CURRENCY_CLUSTER|EIP-ESR0052-001]] v1.0. `npm audit fix` cleared nanoid/postcss (package-lock.json only); new `.github/dependabot.yml`; `pip-audit` CI gate hardened. Approval-to-implement verified via the real Sponsor Approval Service (`submit-response`, ESR-0052/WP1) before any code was written. `pytest` 523/1 unchanged, `validate_repository.py` 0 errors/297 warnings, `npm run build` clean. |
| 1.3 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP1/WP3 Codex design review: both draft EIPs submitted via the AIEMS Exchange Bridge and returned Conditional Pass with corrections, both folded in (EIP-ESR0052-001 to v0.2: stale "Section 10" reference fixed; EIP-ESR0052-002 to v0.2: Section 6 exclusion narrowed to Kokoro-specific RPC/UXP scope, Section 4B's KokoroProvider contract spelled out explicitly). Neither WP yet approved by the Programme Sponsor or implemented. |
| 1.2 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP3: Programme Sponsor selected EBG-0115 (Kokoro TTS evaluation) to resolve the Feature-First Delivery Discipline gap flagged at WP1/WP2. Drafted [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] v0.1 - new `sentinel/kokoro_provider.py` mirroring `PiperProvider`'s contract, a new optional `voice-eval` dependency group, and a live listening comparison mirroring EBG-0113's exact precedent methodology (identical fixed test utterance, two `.wav` files to the Programme Sponsor's Desktop, no adoption decision made by the package itself). Not yet reviewed, approved or implemented. |
| 1.1 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 WP2: Programme Sponsor selected EBG-0111 (Composio assessment) as the paired product-moving objective. Investigated and closed **Deferred, not adopted**: Composio's backend is closed-source/cloud-hosted, not self-hostable; free/affordable tiers require Composio's cloud to custody connected-account credentials (conflicts with self-hosted-first posture), and the self-managed-credentials tier costs $599/month (conflicts with no-discretionary-budget constraint); GAM-0001 also has no boundary category yet for third-party-cloud-relayed actions. Recorded in EBG-0111's EBR-0001 entry. **Feature-First Delivery Discipline note flagged, not resolved**: WP1 (drafted) + WP2 (investigation) together still do not deliver a shipped JARVIS capability - a further WP may be needed before this session can close. |
| 1.0 | 26 August 2026 | Claude Engineering Implementer | ESR-0052 opened at WP0B. WP0 (Technology, Code and AI-Landscape Review) complete: WR-ESR0052-001 produced, independently cross-reviewed by Codex (Conditional Pass with corrections, folded in), an ad hoc second opinion reconciled as a distinct addendum, committed and pushed by the Programme Sponsor (`7b8b3d5`). WP1 drafted per [[EIP-ESR0052-001_PROCESS_TOOLING_CURRENCY_CLUSTER|EIP-ESR0052-001]] v0.1 (EBG-0122 through EBG-0124, process/tooling currency cluster) - not yet reviewed, approved or implemented. Feature-First Delivery Discipline pairing requirement flagged, not yet resolved. |
