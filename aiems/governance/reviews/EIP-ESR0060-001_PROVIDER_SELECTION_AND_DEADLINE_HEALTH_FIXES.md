# EIP-ESR0060-001 - Provider-Selection and Deadline-Health Fixes

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0060-001 |
| Title | Engineering Implementation Package: WP1b Provider-Selection and Deadline-Health Fixes |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0060 |
| Work Package | WP1b |

---

# 2. Purpose

Implements ESR-0060 WP1b, added by Programme Sponsor decision (a) after the WP1 retrospective review: fix the two real defects that review found in ESR-0059 WP4 to WP6 before WP2 begins.

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0155 (High) - `JARVIS_PRIMARY_PROVIDER` matched case-sensitively, so a credentialed cloud provider was silently ignored.
* EBG-0156 (Medium) - a turn deadline expiring inside a provider's own `remaining_timeout()` was treated as a provider fault.

The other WP1 findings (EBG-0157) are out of scope.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` - read `JARVIS_PRIMARY_PROVIDER` with `environ.get(name, default)` and used it verbatim. `_secondary_provider_name()` already stripped and lower-cased its own variable (ESR-0059 WP4).
* **Second, related defect found while reading the code, not in the review**: `environ.get(name, default)` returns `""` for a variable that is set but blank, bypassing the default. A blank `JARVIS_PRIMARY_PROVIDER` therefore also built no primary, and because `""` matches neither known provider, `_secondary_provider_name()` returned nothing either - no cloud provider at all, the same silent outcome as the case mismatch.
* `sentinel/providers.py` `remaining_timeout()` - raised a plain `RuntimeError` when the deadline had passed. All three adapters (`openai_provider.py`, `gemini_provider.py`, `ollama_provider.py`) call it outside their transport `try` blocks, so the exception reaches the orchestrator unwrapped.
* `sentinel/orchestrator.py` `ProviderOrchestrator.execute()` - its own pre-call deadline check stops without touching health ("skipped for time, not failed"), but its generic `except Exception` marked any other failure DEGRADED and opened the circuit. `_execute_with_retry()` re-raises immediately any exception without `transient=True`, so the deadline error is never retried.

---

# 4. Scope

## 4A. EBG-0155 - provider selection (`jarvis/interfaces/stdio_rpc.py`)

* New `_primary_provider_name()`: the primary name is stripped and lower-cased exactly like the secondary; unset or blank means the default (`openai`).
* New `_warn_if_unknown_provider()`: `build_default_runtime()` logs one warning for each configured primary or secondary name that matches no known provider. The warning carries the variable name, the configured value and the known names - never a credential. An unknown name is still ignored, as before; it is just no longer silent. The warning reaches the backend log file because `run()` configures logging before building the runtime.
* Behaviour otherwise unchanged: route order, credential gating, `none` disabling the secondary, and no double registration.

## 4B. EBG-0156 - deadline expiry is not a fault (`sentinel/providers.py`, `sentinel/orchestrator.py`)

* New `DeadlineExceededError(RuntimeError)`, raised by `remaining_timeout()` in place of the plain `RuntimeError`, with the same message. Subclassing `RuntimeError` keeps every existing caller and test that expects one working (the three adapters' own "refuses to start after the deadline" tests pass unchanged).
* `ProviderOrchestrator.execute()` catches it before the generic handler and treats it exactly like its own pre-call check: it stops the failover loop, records "Request deadline reached after attempting: ...", and leaves the provider's health and circuit untouched.

## 4C. Tests

* `jarvis/tests/test_stdio_rpc.py`: `Gemini`, `GEMINI` and `  gemini  ` as primary (parametrised) give `gemini, openai, ollama`; a blank primary gives the default route; unknown primary and secondary names each produce a warning naming them, with no credential in any warning; known names (including `none`) produce no warning.
* `jarvis/tests/test_sentinel_orchestrator.py`: a provider raising `DeadlineExceededError` stays HEALTHY, is not retried, is recorded as attempted, and still has a closed circuit - the next request reaches it again. `remaining_timeout()` raises `DeadlineExceededError`, still a `RuntimeError`.
* **Tests proven to detect the defects**: with only the source changes reverted, five of the six new provider-selection tests fail (the sixth, no warning for known names, passes either way by design - the old code never warned). The orchestrator test cannot import against the old code (the exception type is new); the old behaviour it guards against was reproduced directly by the WP1 Engineering Reviewer.

## 4D. Explicitly out of scope, disclosed

* **A deadline-capped network timeout still counts as a fault.** When `remaining_timeout()` returns less than the provider's configured timeout and the transport then times out, the adapter raises a transient `ProviderError`. If the backoff would cross the deadline it is re-raised and the provider is marked degraded, although the deadline caused the shortened call. Distinguishing this needs the adapters to report whether their timeout was capped. This is a narrower case than EBG-0156 (it needs a call already in flight when the budget runs out), and a provider genuinely hanging until its own configured timeout is still correctly degraded. Raised as an open question for the design review rather than fixed here. **Design review answer**: an acceptable residual for the backlog, since it is narrower than EBG-0156 and errs on the safe side (a 30-second cooldown, never a wrong answer). Recorded as item (6) of EBG-0157 with the reviewer's suggested design.
* **An unknown primary does not fall back to the default.** A typo such as `opanai` now warns but still builds no cloud provider, matching the existing documented behaviour for unknown names. Changing it would silently pick a provider the user did not name.
* **A deadline error after a retry backoff loses the earlier transient error.** If the second attempt's `remaining_timeout()` raises, the first attempt's real failure is not recorded and the provider is not degraded. This is unreachable in practice, because `_execute_with_retry()` already refuses to sleep past the deadline.
* EBG-0157's low-severity items.

---

# 5. Validation Requirements

* `python -m pytest -q`: 759 passed, 1 skipped (751 before, plus 8 new tests).
* `python -m ruff check .`: clean.
* `python scripts/validate_repository.py`: 0 errors, 333 warnings (all pre-existing).
* No live provider call is needed: both fixes act before any network call and are covered by the tests in 4C.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* A primary provider name in any case, or with surrounding whitespace, selects that provider; a blank one selects the default.
* An unknown configured provider name produces a warning in the backend log.
* A deadline expiring inside a provider call leaves that provider HEALTHY with its circuit closed.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 October 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation through the real bridge (`ESR-0060`/`WP1b`, 9-file scope) - **Pass**, no blocking findings. It traced every primary/secondary combination, confirmed against `git show HEAD` that five of the six provider-selection tests fail on the old code, confirmed `DeadlineExceededError` is raised only by `remaining_timeout()` and reaches the orchestrator unwrapped from all three adapters, and re-ran pytest (759 passed/1 skipped), ruff (clean) and the validator (0 errors). Two informational notes: a provider stopped by the deadline is listed as attempted, which matches the existing pre-call path (no change); the EBG-0155 row named the wrong function (corrected). Section 4D residual agreed as backlog (EBG-0157 item 6). **Programme Sponsor approved via the Sponsor Approval Service.** Pending commit through `submit-response`. |
| 0.1 | 1 October 2026 | Claude Engineering Implementer | ESR-0060 WP1b draft, implemented in the working tree. EBG-0155: primary provider name normalised like the secondary, blank means the default (a second defect found while reading the code), unknown names warned about. EBG-0156: `DeadlineExceededError` handled by the orchestrator as out of time, not a fault. 8 new tests; five of the six provider-selection tests proven to fail on the old code. Deadline-capped network timeouts disclosed as an open question. Not yet reviewed, approved or committed. |
