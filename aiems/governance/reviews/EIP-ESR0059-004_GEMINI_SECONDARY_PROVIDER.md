# EIP-ESR0059-004 - Gemini Secondary Provider

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-004 |
| Title | Engineering Implementation Package: WP4 Gemini Secondary Provider |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP4 |

---

# 2. Purpose

Implements ESR-0059 WP4 on the Programme Sponsor's decision to add Gemini as the secondary provider between OpenAI and Ollama (decision 3 of 4, "start from 1. and work your way down"). This authorises the step [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0051 named as "a separate, not-yet-authorised implementation decision", and progresses the routing part of EBG-0140.

Before this package, only the selected primary was ever registered: with OpenAI primary, a Gemini key was ignored, and an OpenAI outage fell straight through to local Ollama.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` and `_build_real_provider()` - one cloud provider, chosen by `JARVIS_PRIMARY_PROVIDER`, credential-gated.
* `jarvis/tests/test_stdio_rpc.py` `test_build_default_runtime_ignores_unselected_provider_credential` - encoded the old rule this decision replaces.
* `sentinel/openai_provider.py`, `sentinel/gemini_provider.py` - both read their key from the process environment at call time and both surface HTTP failures as `RuntimeError`, which `ProviderOrchestrator` already fails over on. No adapter change is needed.
* **Real pre-existing defect found while writing this package's tests**: `_build_real_provider()` treated a whitespace-only key as present, registering a provider that then fails authentication on every call, costing its timeout. It affected the primary as much as the new secondary.
* **Real WP3 miss found while updating documentation**: PCB-0001's Current Constraints section still said "Ollama and the deterministic local provider as further fallbacks". WP3's search looked for "echo" wording and did not match this phrasing, and WP3's design and post-commit reviews did not catch it either. Corrected here. **A second copy of the same stale claim, in PCB-0001's Conversation Workspace row, was missed by this package too and caught by its own design review** (Conditional Pass) - corrected before approval.

---

# 4. Scope

## 4A. Route

* The route is now: primary (if credentialled), secondary (if credentialled), then Ollama.
* **Secondary selection**: unset or blank `JARVIS_SECONDARY_PROVIDER` means the other one of `openai`/`gemini`, so the arrangement is symmetric when Gemini is primary. `none` (case-insensitive) disables the secondary, because every failover call to a cloud provider is billed. Any other value names the secondary directly.
* A selected primary without a key is skipped, not fatal: a credentialled secondary still serves. No provider is ever registered twice.
* `_build_real_provider()` now treats a whitespace-only key as absent.

## 4B. Documentation

* Route descriptions updated: CURRENT_ARCHITECTURE 1.1 to 1.2, PCB-0001 2.15 to 2.16 (including the WP3 miss above), PST-0001 3.42 to 3.43, JARVIS Capability Readiness Matrix 2.14 to 2.15.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0051 records the decision as authorised and delivered; EBG-0140 records the routing part as delivered, with its retry, backoff, circuit-breaker and deny-check scope still open.

## 4C. Tests (`jarvis/tests/test_stdio_rpc.py`)

* The old "ignores unselected credential" test is replaced: with Gemini primary and only an OpenAI key, OpenAI now serves.
* Route order with both keys, both ways round; `none` disables the secondary; a whitespace-only secondary key is absent; no duplicate registration.
* **End-to-end failover** through the real runtime and RPC path, with network calls faked at `urlopen`: OpenAI returns HTTP 503, Gemini answers, the RPC result names `gemini`, and Ollama is never reached.

## 4D. Explicitly out of scope

* Retry, backoff and circuit breaking - a failed primary still costs its full timeout on every turn until EBG-0140's remaining scope is done.
* A per-turn deadline shorter than the Tauri timeout (EBG-0139). With both cloud providers timing out (30s each) plus Ollama (90s), the worst case now exceeds the 120s Tauri-side timeout; the user then sees the backend-timeout message rather than the provider-unavailable one.
* Choosing different default models.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`.
* **Live check not possible on this machine**: no OpenAI or Gemini key is set in this environment. Failover is proven by the end-to-end test in 4C; both adapters were independently live-validated in earlier sessions (OpenAI ESR-0015 WP5, Gemini ESR-0020 WP3) and are unchanged.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* With both keys set, the route is primary, secondary, Ollama.
* A primary failure is answered by the secondary before Ollama is tried.
* The secondary can be disabled without removing its key.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")**, read as also choosing the recommended review option: disclosed self-verification while GitHub Copilot CLI's monthly quota is exhausted, with a retrospective Copilot review once it resets. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation through the real bridge - **Conditional Pass**, one real finding: a third copy of the stale deterministic-provider claim in PCB-0001's Conversation Workspace row. Corrected. The re-review stopped mid-way when Copilot reported its monthly quota exhausted, with no verdict; a disclosed self-verification of the correction was substituted (see ESR-0059). |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP4 draft. Credential-gated secondary cloud provider (symmetric, `JARVIS_SECONDARY_PROVIDER`, `none` to disable); whitespace-only keys treated as absent (a pre-existing defect found here); route descriptions updated in four controlled documents, including a PCB-0001 claim WP3 missed. End-to-end OpenAI-to-Gemini failover test through the real RPC path. Not yet reviewed, approved or committed. |
