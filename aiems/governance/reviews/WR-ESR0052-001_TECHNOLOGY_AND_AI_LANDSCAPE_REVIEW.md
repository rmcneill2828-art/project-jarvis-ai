# WR-ESR0052-001 - Technology, Code and AI-Landscape Review

**Status:** Working Report per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]'s Working Report Lifecycle - **not a controlled artefact**, not registered in REG-0001. Produced at the Programme Sponsor's direct request, ~3 months into the project, for a technology/code/AI-practice health check. Advisory only; does not itself authorise any implementation.

**Author:** Claude Engineering Implementer
**Date:** 26 August 2026
**Purpose:** Independent, evidence-verified answer to three questions: (1) are we still using the best available technology and writing sound code, (2) does our AI-assisted engineering practice hold up against current industry practice, and (3) has anything genuinely new appeared in the AI landscape since project start that JARVIS should adopt.
**Next step:** Programme Sponsor review and direction on the candidate backlog items below. Submitted to Codex Engineering Reviewer via the AIEMS Exchange Bridge for independent cross-review at the Sponsor's request (`ESR-0052`/`WP0-technology-review`); Codex's verdict and the corrections it required are recorded in Section 9.

---

## 1. Headline

Nothing is broken. The engineering practice and core architecture remain sound and, in places, ahead of where the industry has landed (see Section 4). The real findings are all **currency drift**, not defects: three real (if low-severity) frontend dependency vulnerabilities that a plain `npm audit fix` would clear, a one-line pip self-vulnerability, React and Vite sitting one-to-several versions behind stable, and one real architectural gap worth a deliberate look - JARVIS has no Anthropic/Claude provider option in Sentinel, despite Claude being the very model this project trusts to write its code. None of this is urgent; all of it is cheap to fix.

---

## 2. Evidence-Verified Current State

All of the following were re-run live today, not read off a document:

| Check | Result |
|---|---|
| `python -m pytest jarvis/tests sentinel scripts/tests` | **523 passed, 1 skipped** - up from 512 at ESR-0051's close (26 August 2026, RBL-0032). No regression. |
| `python scripts/validate_repository.py` | **0 errors, 292 warnings** at the time this report was drafted. **Correction per Codex's independent review (Section 9):** once this report itself was saved to the repository, validation exited **1 error, 292 warnings** - this file introduced an unresolved WikiLink (now fixed below, in the same edit that added this correction). The pre-existing 292 warnings are the same stale same-document section-cross-reference class as previous reviews (cosmetic, non-blocking). |
| `git status` / `git log` | The tracked/committed baseline (`main`) matches `origin/main` exactly - unlike the gap found in [[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]], there is no unpushed commit this time. **Correction per Codex's independent review:** the working tree itself was not clean at review time, since this report was untracked pending Sponsor review - the same distinction WR-ESR0051-001 itself had to correct for. |
| `pip list --outdated` | Python runtime dependencies (`psutil`, `piper-tts`, `faster-whisper` and transitive deps) are all at most one minor/patch release behind. Healthy. |
| `pip-audit` | **1 finding**: `pip` itself, 26.1.2, has a known advisory (PYSEC-2026-3721), fixed in 26.2. Tooling-only, not a shipped dependency. |
| `npm outdated` | React 18.3.1 -> 19.2.8 stable available; Vite 5.4.21 -> 8.2.2 (three majors behind); `@vitejs/plugin-react` 4.7.0 -> 6.1.0; `lucide-react` 1.23.0 -> 1.34.0; `@playwright/test` 1.61.1 -> 1.62.1. |
| `npm audit --omit=dev` | **0 vulnerabilities** - the shipped production bundle is clean, confirming ESR-0032's dev-only characterisation still holds. |
| `npm audit` (full) | **4 vulnerabilities (1 moderate, 3 high)**, all dev-tooling: `esbuild`/`vite` (moderate, dev-server-only, fix requires the major Vite bump above), `nanoid` (high) and `postcss` (high) - **these last two are new since the last review and are fixable today with a plain, non-breaking `npm audit fix`.** |
| Sentinel provider inventory | `openai_provider.py`, `gemini_provider.py`, `ollama_provider.py`, `local_provider.py` (echo fallback). No `anthropic_provider.py` / Claude adapter exists. |
| `sentinel/policy.py` spot-read | `TrustTierPolicy` is sound: deny-by-default for `LOCAL_AGENT_ACTION`/`EMERGENCY_CONTROL`/`UNSUPPORTED_HIGH_RISK`, immutable decision objects, documented precedence order a caller cannot soften by also setting `requires_approval=True`. One documented limitation, not a defect: classification trusts caller-declared `payload_type`/metadata strings rather than inspecting request content - reasonable for the current single-caller (Guardian backend) trust boundary, worth revisiting once external-facing entry points (`ADR-0020`) exist. |
| CI (`.github/workflows/ci.yml`) | `pip-audit` runs with `continue-on-error: true` (advisory only, per its own comment, pending an initial findings baseline). That baseline now genuinely exists (the pip finding above) and was never triaged - see Section 6. No Dependabot/Renovate config exists anywhere in the repository; dependency-currency drift (Section 2's `npm outdated`/`pip list --outdated` findings) is currently only ever caught by someone running these commands by hand, as this review just did. |

Conclusion: no regression, no silent breakage. What decayed is dependency currency, at a pace consistent with three months of otherwise well-run engineering and zero automated drift detection.

---

## 3. Technology Stack Assessment

**Backend (Python 3.12, self-hosted-first):** sound and, per Section 5, still the right call. `piper-tts` and `faster-whisper` keep voice fully local/offline, consistent with the project's standing no-discretionary-budget-for-tooling constraint and privacy posture. No dependency bloat - the runtime dependency list is still three packages.

**Frontend (Tauri 2 + React 18 + Vite 5):** Tauri's choice of the v2 line is still correct - v3 has no stable release as of today, only forward references in the changelog (confirmed by web search, Section 5). React 18 is the one piece genuinely worth moving off: React 19 has been stable and widely adopted for well over a year, and nothing in `src/` (Playwright/Vitest coverage, `d3-force` usage) looks like it would fight the upgrade. Vite's currency gap is larger in version-number terms (5 -> 8) but lower-priority - it is a build tool, not shipped code, and the only live issues it carries (`esbuild`, dev-server-only) don't reach production.

**Rust (Tauri shell):** `Cargo.toml` shows deliberate, well-documented version pinning (the `indexmap` workaround, the SHA-pinned GitHub Actions per OpenSSF hardening guidance) - this is engineering discipline the review has no correction for.

**CI/CD:** genuinely good - separate Python/frontend/Playwright/Rust jobs, a real production-vs-dev audit distinction (not just `npm audit` run blind), SHA-pinned third-party Actions, and a version-drift guard (`sync_product_version.py --check`). The one gap is the advisory-only `pip-audit` step now sitting on an actual unaddressed finding (Section 2/6).

---

## 4. AI-Assisted Engineering Practice vs Current Industry Practice

This project's dual-AI workflow (Claude Engineering Implementer, Codex Engineering Reviewer, human-gated approval and Git operations, per [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]]/[[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]) was compared against how the wider industry is now formalising agentic AI engineering (web search, Section 5's Claude Agent SDK results):

- **Hooks that block dangerous actions before they execute** and **structured, auditable output over free-form trust** are now called out as the two things "most tutorials skip" in production agent deployments. JARVIS already has both, independently arrived at: Sentinel's deny-by-default `TrustTierPolicy` gate (Section 2) is the same shape as a permission hook, and the AIEMS Exchange Bridge's `return-findings` contract is exactly the "structured findings come back, not free text" pattern now recommended for subagent handoffs. The project's own governance model converged on current best practice without having read about it.
- **Subagent sprawl** is flagged industry-wide as the most common failure mode (memory/cost/context multiplication). This project's two-collaborator model (one Implementer, one Reviewer, human-gated) structurally avoids that failure mode by construction - there is no sprawl to have.
- **Cost tracking as a v1 requirement**, not a postmortem afterthought, is now standard industry advice for agentic workloads. This repository has no visible cost-tracking artefact for AI engineering spend itself (as distinct from the "no discretionary budget for tooling" constraint, which is a different concern). Not urgent given the current session-based, human-approved cadence, but worth a note if session frequency or scope grows.
- **Automated dependency-freshness tooling** (Dependabot/Renovate) is now close to a default expectation for any actively maintained repository, and its absence here is exactly why Section 2's drift had to be found by hand rather than surfaced automatically. This is the one concrete practice gap this review found between JARVIS's process and current baseline industry hygiene.

Overall: the AI-assistance practice here is not behind - on the human-gating and structured-review dimensions it is ahead of what a lot of write-ups describe as best practice. The one real gap is automated currency detection (dependency bots), which is a tooling gap, not a practice gap.

---

## 5. AI Landscape Scan - What's New Since Project Start

Live web search performed today; findings below are what's actually changed, filtered for relevance to JARVIS's own architecture and open backlog rather than a general survey.

- **Model Context Protocol (MCP) is now the industry-standard tool-integration protocol**, not a vendor feature: Anthropic donated it to a new Linux-Foundation-hosted body (the Agentic AI Foundation) in December 2025, co-founded with OpenAI and Block; it now has ~97M monthly SDK downloads and 9,400+ public servers, with native support across Anthropic, OpenAI, Google DeepMind and Microsoft. **Relevance:** JARVIS's Agent Framework (`jarvis/agents/`, `SpecialistAgent` contract, custom `guardian.agent.*` RPC methods, [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]) is a bespoke protocol built before this consolidation happened. It works, and nothing here says rip it out - but any future specialist agent beyond GIA (especially one that needs to reach an external service) should be evaluated against "build another custom RPC method" vs "expose it as an MCP server behind the existing Sentinel gate," since the second option would get free interoperability with the wider ecosystem this session itself is a live example of (Composio, listed below, is MCP-shaped tooling).
- **Claude Agent SDK** (renamed from "Claude Code SDK" in early 2026) packages the exact agent loop, permission system and subagent machinery that runs this very engineering session, as a reusable Python/TypeScript library. **Relevance:** it is directly relevant prior art for two unbuilt pieces of JARVIS - the Agent Framework's next specialist agents, and the still-entirely-unimplemented Local Agent/Action faculty ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A). It is not a drop-in replacement (JARVIS's trust boundary is Sentinel-specific and already well-designed for this project), but its documented failure modes (subagent sprawl, missing cost tracking, permission hooks as a v1 requirement) are a ready-made checklist against which to design that faculty's first implementation.
- **Claude Computer Use** (screen-observing, mouse/keyboard-driving desktop control) is real and shipping, but as of the most recent evidence found, remains a **macOS-only research preview**; Windows support is stated as planned, not released. **Relevance:** this is the single most on-point external development for JARVIS's largest capability gap (Local Agent/Action faculty), but it is not yet a usable building block for a Windows-first project (this repository's own dev/CI environment is Windows-primary). Worth tracking, not worth designing against yet. Its safety pattern - request permission before any significant action, allow interrupt at any time - is architecturally identical to what `GAM-0001` Section 8A and `TrustTierPolicy`'s deny-by-default gate already specify, which is a useful external validation of that design rather than a reason to change it.
- **Kokoro-82M** is now consistently rated (across independent 2026 comparisons) as the best-quality open, self-hosted TTS model at small size (327MB, Apache 2.0, 54 voices/8 languages, no GPU required), with Piper (JARVIS's current choice) explicitly characterised as faster/smaller but "the most robotic" by comparison. **Relevance:** this directly validates EBG-0115 ("Evaluate Kokoro TTS for a more expressive Guardian voice"), already sitting as an open candidate backlog item since before ESR-0051. The independent evidence found today suggests this item is well-timed for pickup rather than continuing to sit unassessed - it is a same-shape self-hosted swap (Piper's own provider-adapter pattern in `sentinel/piper_provider.py` already shows what a `kokoro_provider.py` would need to look like), not a new architectural direction.
- **Composio** (the managed 1,000+-app integration tool this Claude session itself has live access to) remains exactly what it was at the last review: real, and still unassessed against JARVIS's own architecture (EBG-0111). Per the correction Codex made to the last review, this session's own tool access is a property of this Claude session, not evidence about what the deployed JARVIS product can do - repeating that distinction here rather than re-making the same overclaim.

No other externally-sourced finding rose to the level of a recommendation. Nothing found suggests the current architecture direction (Tauri + React shell, Sentinel trust gateway, self-hosted voice, SQLite personal memory) is wrong or behind; the findings above are additive options, not corrections.

---

## 6. Backlog Validation

Cross-checked against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] directly.

| Category | Result |
|---|---|
| Confirmed Valid Backlog Items | EBG-0110 (memory-content/external-provider policy gap), EBG-0111 (Composio assessment), EBG-0115 (Kokoro TTS evaluation), EBG-0118 (Codex CLI stall, inconclusive, low severity) - all still open, all still accurately described. |
| Completed Backlog Items | None found miscategorised as open. |
| Superseded / Duplicate Items | None found. |
| New Candidate Backlog Items | See below - all newly proposed by this review, none yet in EBR-0001. |
| Recommendation on EBR-0001 | Update recommended to register the five new candidate items below; no other change needed. |

**New Candidate Backlog Items proposed by this review:**

| Proposed Item | Theme | Priority | Effort |
|---|---|---|---|
| Frontend dependency vulnerability remediation | `npm audit fix` (non-forced) for `nanoid`/`postcss` (Section 2) | Low-Medium (real high-severity advisories, but dev-tooling-only exposure) | Trivial |
| pip self-update | Bump `pip` to 26.2+ (PYSEC-2026-3721) | Low | Trivial |
| React 18 -> 19 upgrade | Stable for over a year industry-wide; no identified blocker in current `src/` usage | Low-Medium | Small-Medium (needs a real regression pass, not just a version bump) |
| pip-audit CI gate hardening | Convert the advisory-only `pip-audit` CI step to a hard gate now that a real baseline finding exists and has been triaged (Section 2/6) | Low | Trivial |
| Dependency-freshness automation | Add Dependabot (or equivalent) so currency drift like Section 2's is caught continuously rather than only when someone runs a manual review | Medium | Small |

Vite's larger version gap and the MCP/Agent-Framework architecture question (Section 5) are deliberately **not** proposed as backlog items yet - both need a scoped design/effort conversation before they're actionable, not a one-line register entry.

---

## 7. Recommendation for Next Session

In priority order, all advisory:

1. **Clear the five trivial/small items in Section 6 in one session** - all independent, all low-risk, a natural Backlog Acceleration Opportunity per PBK-0001, and (per Feature-First Delivery Discipline) should be paired with a genuine product-moving item rather than run as a process-only session.
2. **Paired product objective candidates**, in order of readiness: EBG-0115 (Kokoro TTS) is the most concretely actionable given today's independent evidence (Section 5) and an existing provider-adapter pattern to follow; EBG-0111 (Composio assessment) is a short, contained investigation, not implementation, that would finally turn a stale "not yet assessed" item into a real decision.
3. **Longer-range**: the Local Agent/Action faculty ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A) remains, as the last review also found, the single highest-leverage next capability and the biggest gap between what's built and the original JARVIS vision. This review adds one input to that future design conversation: Claude Agent SDK's documented failure modes and Claude Computer Use's permission/interrupt pattern (Section 5) are both directly relevant prior art to design against once that work is scoped - not a reason to start it sooner than the Programme Sponsor otherwise judges appropriate.
4. **Not recommended right now**: the Vite major-version bump (real but low-urgency, dev-tooling-only exposure) and any MCP-based rearchitecture of the existing Agent Framework (works today; only future specialist agents need this question answered, not the existing one).

---

## 8. JARVIS Development Readiness Assessment

Per PBK-0001's mandatory question: the evidence in this review does not change the assessment [[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]] already reached four days ago - **"AIEMS sufficiently mature for full JARVIS Engineering"**. Nothing found here is a governance, stability or repeatability regression; every finding is either a cheap currency fix or an additive option for a future capability that was already the correctly-identified next horizon (Local Agent/Action). The engineering constraint remains capability-building time, not governance or technology-currency maturity.

This assessment and the ranked recommendations above are advisory only, per PBK-0001 - the Programme Sponsor determines engineering priorities and any actual session objective.

---

## 9. Codex Independent Review

Submitted to Codex Engineering Reviewer via the AIEMS Exchange Bridge (`ESR-0052`/`WP0-technology-review`), per the standing dual-AI cross-review workflow, using a fully-unattended `codex exec -s workspace-write` round trip (the primary mode per EBG-0096, superseding the read-only-plus-relay fallback) - completed cleanly on the first attempt.

**Codex's verdict: Conditional Pass with corrections**, timestamp 2026-08-26T07:47:51Z. Codex independently re-read the report and the live Sentinel source rather than trusting the stated claims, and found:

- **One material correction (addressed above):** the report's `validate_repository.py` claim was wrong for the actual current repository state - saving the report itself introduced an unresolved WikiLink (`project_jarvis_no_discretionary_budget`, a personal-memory file slug mistakenly written with WikiLink brackets as if it were a registered repository artefact), which validation catches as an error. Fixed by removing the invalid WikiLink (Section 3) and correcting Section 2's wording to describe validation state before and after that fix, rather than silently reporting only the now-clean figure.
- **One wording correction (addressed above):** the git-status claim was too strong - "matches origin/main exactly" was true of the tracked/committed baseline, but the working tree itself was not clean while this report sat untracked pending review, the same distinction [[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]] itself had already had to correct for once.
- **Independently confirmed, no correction needed:** `pytest` (523 passed, 1 skipped, matching); Sentinel provider inventory (OpenAI, Gemini, Ollama, LocalEcho, Piper and Whisper-style adapters, no Anthropic/Claude provider); `sentinel/policy.py` `TrustTierPolicy` behaviour (deny-by-default for `LOCAL_AGENT_ACTION`/`EMERGENCY_CONTROL`/`UNSUPPORTED_HIGH_RISK`, frozen `PolicyDecision`, caller-declared-metadata classification, all as described); Section 5's AI-landscape framing (external findings, not overclaimed as confirmed repository capability - the Composio/EBG-0111 caveat specifically checked and found not repeated as an overclaim); Section 6's backlog validation against the live EBR-0001 state.
- **Disclosed limitation, not a finding against the report:** Codex's own environment blocked it from independently re-running `pip-audit`, `npm audit` (both forms), `npm outdated` or `pip list --outdated` (a managed command-policy restriction on Codex's side, not a repository issue) - those specific live-evidence figures in Section 2 are therefore this report's own direct evidence only, not independently cross-verified by Codex, and should be read with that caveat until a future review can re-run them from an environment that permits it.

No other material issue was found; Sections 3, 4, 5 and 7's substantive analysis were not disputed.

---

## 10. Independent Second Opinion (Ad Hoc, Outside the AIEMS Exchange Bridge)

The Programme Sponsor separately asked a ChatGPT/Codex session the same review question directly, outside this report's AIEMS Exchange Bridge submission (no role-lock, no evidence capture, no `return-findings` structured contract - that session also disclosed it could not run `npm run build` or find `python` on PATH in its own shell). Treated here as an informal second opinion, cross-checked against the real repository before being folded in - not a substitute for, or a repeat of, Section 9's formal bridge review.

**Code findings - verified directly against current source:**

| Claim | Verification | Correction |
|---|---|---|
| `src-tauri/src/lib.rs` hardcodes `python` for the dev backend launcher | **Confirmed** (`spawn_dev_backend`, `Command::new("python")`). | Scope correction: this is exclusively the `cfg!(debug_assertions)` dev path. The production/installer path (`spawn_sidecar_backend`) runs the pre-built sidecar binary and never invokes `python` at all - this cannot affect the shipped product, only a contributor's `npm run tauri dev` experience on a machine without `python` (as opposed to `python3`) on PATH. Real, but a developer-experience gap, not a product-severity "High." |
| Push-to-talk can start overlapping recordings because the mic button isn't disabled while recording | **Not as described**: `handleToggleRecording` already routes a click during active recording to `handleStopRecording`, not a second `handleStartRecording` - the button *is* effectively guarded once `isRecording` is `true`. **A narrower, real race does exist**: `handleStartRecording` only sets `isRecording=true` after its `await navigator.mediaDevices.getUserMedia(...)` resolves; two clicks landing before that promise settles (e.g. while the OS permission prompt is up) can each call `handleStartRecording()`, and the second `MediaRecorder`/stream silently overwrites `mediaRecorderRef.current`, leaking the first stream's tracks. Real, Medium severity, different mechanism than described. |
| Desktop-shell affordances with no click handlers are misleading | **Confirmed for one set, overstated for the other.** `AppHeader`'s window-action buttons (Notifications/Settings/Minimize/Maximize/Close, `App.jsx`) genuinely have no `onClick` and nothing marking them as inert - a real "looks real, does nothing" gap. The other buttons this claim also named (the `quick-actions` row: Platform Status/View Capabilities/Run Diagnostics/Show Roadmap) sit inside a container the code itself labels `aria-label="Static Guardian shortcuts"`, under a sidebar heading that literally reads "Platform Placeholders" - these are disclosed placeholders in the accessibility tree, not a hidden defect, and treating both sets the same overstates the second. |

**AI Workspace Update - verified by web search, not merely taken on trust:** GPT-5.6 (Sol/Terra/Luna capability tiers) is real, reached general availability 9 July 2026, and OpenAI's Responses API is now MCP-connector-native by default - corroborating, independently, Section 5's MCP finding above from the OpenAI side rather than only the Anthropic side. This second opinion's OpenAI-specific framing surfaced one genuinely new, verified finding this report did not originally have: **`sentinel/openai_provider.py` targets the legacy Chat Completions endpoint (`https://api.openai.com/v1/chat/completions`), not the Responses API.** Chat Completions remains supported (it is not being sunset - only the older Assistants API is, coincidentally on today's date), so this is not broken, but it means Sentinel's OpenAI adapter is not on the path OpenAI itself now treats as the native route to MCP connectors. Worth evaluating alongside Section 5's own MCP recommendation, not urgent on its own.

**Assessment:** a useful, mostly-accurate second opinion once corrected for scope and one overstatement - none of it changes Section 9's Codex-verified conclusions, and none of it rises to a backlog item on its own without the Programme Sponsor's view on priority. Not re-submitted through the bridge for a second formal cross-review; the Programme Sponsor may direct that if wanted.

---

## 11. Related Artefacts

* [[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]] - prior Working Report this one follows in structure and cadence.
* [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] - last closed session, source of current baseline.
* [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] - current accepted repository baseline.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - source of Section 6's backlog validation.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - source of the Local Agent permission boundary referenced in Section 5/7.
* [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] - Agent Framework architecture referenced in Section 5.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Working Report Lifecycle and Repository Engineering Health Review guidance followed by this report's structure.
