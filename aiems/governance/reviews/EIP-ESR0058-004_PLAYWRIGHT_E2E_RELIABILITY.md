# EIP-ESR0058-004 - Playwright E2E Reliability

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0058-004 |
| Title | Engineering Implementation Package: WP5 Playwright E2E Reliability |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0058 |
| Work Package | WP5 |

---

# 2. Purpose

Implements ESR-0058 WP5, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0129: the Playwright E2E suite's cold-start parallel-worker race (reproduced live: 12 failed/6 passed at default parallelism, 17 passed/1 failed sequentially, the one failure an initial `page.goto()` timeout, not an assertion failure).

---

# 3. Repository Context Investigated

* `playwright.config.js` - confirmed the suite drives the Vite dev server (`npm run dev`) directly, with no warm-up step before Playwright's default parallel workers begin.
* The gap analysis's own recommendation ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0129 row): test against a production build plus a pre-warmed preview server. **Tried first, and reverted** - see Section 4C below; this is a real, disclosed deviation from the source recommendation, not a silent substitution.
* `tests/e2e/animationScheduler.spec.js` - read in full. All three of its tests deliberately dynamic-import the raw `/src/animationScheduler.js` source path inside `page.evaluate()`, to exercise that module's contract in isolation (EBG-0081 Question 1) independent of the app's own rendered UI. This only works against a server that serves raw unbundled `/src/*.js` paths.
* `src/GuardianOrbGraph.jsx` - confirmed it imports `animationScheduler.js` as part of the app's ordinary render path, so a real-browser navigation to `/` already walks Vite's transform of that module as a side effect, with no need to warm it separately by path.
* `.github/workflows/ci.yml` - confirmed CI just runs `npm ci` -> `npx playwright install --with-deps chromium` -> `npx playwright test`, so a `playwright.config.js`-only fix (no separate CI workflow change) is sufficient and will propagate automatically.

---

# 4. Scope

## 4A. Diagnosis

A cold Vite dev server transforms each module the first time it is requested. Playwright's default parallel workers all issue their first `page.goto()` at once, right after the dev server reports itself ready on its bound port - several workers race to trigger the very first transform of the app's module graph, and the slowest can miss the navigation timeout. This is a startup-ordering problem, not a defect in the animation scheduler, the rendered app, or the tests' own assertions (the 17/1 sequential result already showed the suite is otherwise reliable once warm).

## 4B. Fix implemented

* `tests/e2e/global-setup.js` (new file): a Playwright `globalSetup` hook that launches a real headless browser, navigates once to the app root (`waitUntil: "networkidle"`), and closes - forcing Vite to pre-transform and cache the app's module graph (`main.jsx` -> `App.jsx` -> `GuardianOrbGraph.jsx` -> `animationScheduler.js`, etc.) before any parallel test worker starts. `globalSetup` runs after Playwright's `webServer` is confirmed reachable and before any worker spins up, which is exactly the ordering this fix needs.
* `playwright.config.js`: registered `globalSetup: "./tests/e2e/global-setup.js"`; kept the dev server (`npm run dev`) as `webServer.command`; kept the previously-added `use.actionTimeout`/`use.navigationTimeout` (15s each, up from Playwright's implicit defaults) as a reasonable safety margin independent of the warm-up fix; reverted `webServer.timeout` to 30s (its original value, since the dev server itself starts near-instantly - the 120s figure only made sense for the reverted build+preview approach, where a cold production build ran inside the same command).

## 4C. Rejected alternative (disclosed, not silently dropped)

The gap analysis's literal recommendation - build once, serve via `vite preview` (`npm run e2e:serve`, added to `package.json`) - was implemented and genuinely run first. It solved the original race (no more per-request transform contention) but broke `tests/e2e/animationScheduler.spec.js`: a production build does not serve raw `/src/*.js` paths (they get bundled into hashed `dist/assets/` files), so all three of that file's `page.evaluate()` calls failed with `TypeError: Failed to fetch dynamically imported module`. This traded one real, reproduced failure mode for a different one rather than fixing it, so it was reverted; `package.json`'s `e2e:serve` script was removed again along with it. This is recorded here because the gap analysis's recommendation was a Programme Sponsor-visible artefact (EBR-0001's EBG-0129 row) and diverging from it without disclosure would itself be a process gap.

## 4D. Tests

No new test cases were added - this Work Package fixes the harness the existing 18 E2E tests run under, not the tests themselves. Verification is the full suite's own pass/fail record (Section 7).

## 4E. Explicitly out of scope

* EBG-0130 through EBG-0134 (the other five gap-analysis findings) - each remains Candidate Backlog, not scheduled to this or any session.
* Any change to `tests/e2e/animationScheduler.spec.js` itself, or to `src/animationScheduler.js` - both are working as designed; only the harness that serves them needed to change.
* CI workflow changes - `.github/workflows/ci.yml` already runs `npx playwright test` directly against whatever `playwright.config.js` specifies, so this fix propagates without a separate workflow edit.

---

# 5. Validation Requirements

* `npx playwright test` - run at least three consecutive times at default parallelism (the same parallel/cold-start conditions that originally reproduced the race), confirming a consistent green suite, not a single lucky run.
* `python -m pytest jarvis/tests scripts/tests -q` - full suite, confirming no regression outside the frontend E2E harness.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* Manual confirmation that no dev-server process is left listening on port 1420 after the runs complete (per this project's own prior leaked-port incident).

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `npx playwright test` passes 18/18 across at least three consecutive runs at default (`fullyParallel: true`) settings, with no `workers: 1` workaround.
* `tests/e2e/animationScheduler.spec.js`'s three tests continue to pass unmodified.
* No dev-server process leaked on port 1420 after any run.
* Full Python test suite and `validate_repository.py` remain clean.
* EBG-0129 closed Complete, with the rejected build+preview alternative disclosed in the same entry.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary directly. Implemented exactly as drafted at v0.2 - no further content change. `submit-response` succeeded against the real Sponsor Approval Service. Pending commit/push. |
| 0.2 | 16 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation routed through the real bridge (`ESR-0058`/`WP5`, complete 6-file `files_in_scope`) - **Pass**, single clean `return-findings` entry, independently verified against the transcript (`repository_ref: 3871e44...` matching HEAD exactly). Confirmed via its own `npm run build` that `dist/` contains no `/src/` path and no `'/src/'` substring in the bundled JS; confirmed `global-setup.js`'s wiring and ordering against Playwright's own `globalSetup` semantics; ran `npx playwright test` itself twice at default parallelism (18/18 both times, 4 workers, no `workers: 1` override); confirmed `webServer.timeout` at 30s matches the baseline commit, untouched by this diff; confirmed the exact 6-file scope with nothing extra or missing. Re-ran `pytest` (583 passed/1 skipped) and `validate_repository.py` (0 errors, 332 warnings) independently, both matching. Not yet approved or committed. |
| 0.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP5 draft. Fix implemented and verified directly against the working tree: build+preview approach tried first and reverted (broke `animationScheduler.spec.js`'s raw-source-import design); `tests/e2e/global-setup.js` warm-up approach implemented instead, verified via three consecutive real `npx playwright test` runs at default parallelism (18/18 passed each time), full Python suite (583 passed/1 skipped) and `validate_repository.py` (0 errors, 332 warnings) re-run clean. Not yet reviewed, approved, or committed. |
