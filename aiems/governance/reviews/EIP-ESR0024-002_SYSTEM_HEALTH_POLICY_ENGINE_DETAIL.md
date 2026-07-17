# EIP-ESR0024-002 - System Health Policy Engine Detail

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0024-002 |
| Artefact ID | EIP-ESR0024-002 |
| Title | System Health Policy Engine Detail |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | PBK-0001 (Feature-First Delivery Discipline, Incremental Visual Convergence) |
| Intended Session | ESR-0024 |
| Effective Date | 17 July 2026 |

---

# 2. Purpose

ESR-0024 WP1 ([[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]]) delivered backend-only work: wiring `TrustTierPolicy` into `build_default_runtime()`. PBK-0001's Feature-First Delivery Discipline permits a session to satisfy its UXP-progress requirement through backend capability alone, but its Incremental Visual Convergence clause additionally asks that a session include a small UXP change toward the reference mock-up wherever a natural opportunity exists. WP1 created exactly such an opportunity: for the first time, the live runtime has a real, observable answer to "which policy engine is actually governing Sentinel" - data that did not exist before this session.

This package proposes surfacing that one fact - honestly, without inventing anything - in the live System Health panel's existing Sentinel row.

---

# 3. Objective

Make the System Health panel's Sentinel row name the connected policy engine (e.g. "Trust gateway active (TrustTierPolicy)") using only data `build_default_runtime()` and this session's own WP1 accessors already produce - no new capability, no fabricated fields.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `src/App.jsx`'s `deriveSystemHealth()` (Sentinel row) | `detail: running ? "Trust gateway active" : "Not running"` - fixed text, does not name which policy engine is connected |
| `jarvis/interfaces/stdio_rpc.py`'s `_platform_status` | Returns `state`, `runtimeHealth`, `providerConnected`, `providers` - no policy engine field exists |
| `GuardianRuntime.sentinel_gateway()` / `SentinelTrustGateway.policy_engine` | Both added at ESR-0024 WP1 specifically for wiring-confirmation tests; already public, already unit-tested, reusable here without new production surface |
| Frontend test coverage | None exists in this repository (confirmed at ESR-0023 WP6) - verification here follows the established Playwright-against-real-dev-server methodology (EBG-0072/EBG-0073) |

---

# 5. Scope

This package authorises a future implementation to:

1. `jarvis/interfaces/stdio_rpc.py`'s `_platform_status`: add a `"policyEngine"` field - `type(gateway.policy_engine).__name__` where `gateway = self._runtime.sentinel_gateway()`, or `None` if no gateway is connected. All existing fields (`state`, `runtimeHealth`, `providerConnected`, `providers`) remain unchanged.
2. `src/App.jsx`'s `deriveSystemHealth()`: the Sentinel row's `detail` becomes `` `Trust gateway active (${platformState.policyEngine})` `` when running and `policyEngine` is present, falling back to the current unqualified "Trust gateway active" if the field is ever absent (defensive only - `build_default_runtime()` always wires a policy engine today, so this fallback is not expected to trigger in practice, but keeps the row honest if that ever changes). Guardian and Providers rows are unaffected.
3. Update `jarvis/tests/test_stdio_rpc.py`'s existing exact-dict assertion (`test_platform_status_reflects_real_runtime_state`) to include the new field, and add one new test asserting `policyEngine == "TrustTierPolicy"` for the real production runtime.
4. Manually verify, via a Playwright-driven check against the real Vite dev server (mocking `window.__TAURI_INTERNALS__.invoke`, no live backend), that the Sentinel row's connecting, offline and running states all render honestly, including the new policy-engine detail in the running state.

No other panel, row, or field is authorised to change.

---

# 6. Authorised Files

1. `jarvis/interfaces/stdio_rpc.py`
2. `jarvis/tests/test_stdio_rpc.py`
3. `src/App.jsx`
4. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `_platform_status`: `gateway = self._runtime.sentinel_gateway()`; `"policyEngine": type(gateway.policy_engine).__name__ if gateway is not None else None`.
2. `deriveSystemHealth()`'s Sentinel row: `detail: running ? (platformState.policyEngine ? \`Trust gateway active (${platformState.policyEngine})\` : "Trust gateway active") : "Not running"`.
3. No change to the Guardian or Providers row derivation functions.
4. New/updated tests must use `environ={}` throughout, matching every existing test in the file - no real network calls, no host-credential dependence.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to the Guardian or Providers System Health rows.
2. A new panel, or any of the reference mock-up's `MODE`/`CONFIDENCE`/`AUTONOMY`/`PERMISSION` fields (`aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`'s "Orb Status" panel) - Guardian does not compute any of those concepts today, and inventing labels for them would violate the no-mock-fallback rule (PBK-0001, ESR-0017 WP9) exactly as the Incremental Visual Convergence clause itself warns against.
3. Any change to `TrustTierPolicy`, `SimpleApprovalPolicy`, or Sentinel's classification/decision logic - display-only.
4. Any change to `DiagnosticsPanel`'s four static placeholder rows.

---

# 9. Constraints

1. Only data already computable from the existing production runtime may be shown - no illustrative or placeholder values.
2. The Sentinel row's existing connecting/offline states must remain unchanged; only the running-state detail text changes.
3. No implementation shall begin until this package reaches Approved status.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
npm run build
```

Validation should confirm:

1. Full pytest suite passes, including the updated and new tests.
2. `validate_repository.py` (full mode) passes with the same pre-existing warning count, 0 errors.
3. `npm run build` is clean.
4. A manual Playwright check against the real Vite dev server confirms the Sentinel row's connecting/offline/running-with-policy-name states all render honestly, with zero console errors.

---

# 11. Risks and Dependencies

## Dependencies

1. `GuardianRuntime.sentinel_gateway()` and `SentinelTrustGateway.policy_engine` (both added at ESR-0024 WP1, [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]], already committed at `82ea244`).
2. PBK-0001's Incremental Visual Convergence practice (added ESR-0019 WP2 closure) and Feature-First Delivery Discipline (ESR-0017 WP8), which this package satisfies.

## Risks

1. Low risk: an additive, display-only field and one text-string change to an already-honest row; no behavioural or policy change.
2. Minor scope-discipline risk if reviewers see this as an opening to add further mock-up fields in the same pass - explicitly excluded (Section 8 item 2) to keep this package to the one fact WP1 actually produced.
3. **Engineering Reviewer (Codex) residual-risk finding, accepted, not actioned by this package:** verification of the frontend change depends on a manual Playwright check rather than an automated UI test, so the visual assertion is only as strong as that manual step - the same pre-existing limitation EBG-0072/EBG-0073 and EIP-ESR0021's Knowledge Metrics work were verified under, since no frontend test/snapshot infrastructure exists in this repository at all (confirmed directly at ESR-0023 WP6). Building that infrastructure is a materially larger, separately-scoped undertaking, not this package's - flagged here as a candidate for a future backlog item at the Programme Sponsor's discretion, not created as one by this package.
4. **Engineering Reviewer (Codex) post-implementation residual-risk finding, accepted, not actioned by this package:** `policyEngine` (`type(gateway.policy_engine).__name__`) is now part of the `platform.status` RPC response contract the live UXP consumes - a future rename of the `TrustTierPolicy` class would therefore be a user-visible API/UI change, not merely an internal one, even though nothing about this package's own scope makes such a rename more or less likely. No action taken now; a future rename (if it ever happens) should account for this coupling at that time.

---

# 12. Approval Request

**Engineering Reviewer (Codex) reviewed v0.1: no blocking findings.** Codex checked the draft against the current implementation (`sentinel/core.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_stdio_rpc.py`, `src/App.jsx`) and confirmed internal consistency. One residual risk noted (Section 11, item 3) - accepted as a pre-existing, out-of-scope limitation, not a blocker. **Approved by the Programme Sponsor, 17 July 2026.** Implemented exactly as scoped in Sections 5-9: `_platform_status` adds `policyEngine`; `deriveSystemHealth()`'s Sentinel row now names it when running; `test_platform_status_reflects_real_runtime_state` updated, one new test (`test_platform_status_policy_engine_is_none_without_a_connected_gateway`) added for the defensive `None` branch. 212 tests pass (was 211), `validate_repository.py` 0 errors, `npm run build` clean. Frontend verified via a Playwright-driven check against the real Vite dev server (mocking `window.__TAURI_INTERNALS__.invoke`): connecting -> "Connecting to the JARVIS backend...", offline -> "JARVIS backend is unavailable", running -> "Trust gateway active (TrustTierPolicy)", zero console errors in all three states.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] | Source of the `sentinel_gateway()`/`policy_engine` accessors this package reuses; already implemented and committed. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Feature-First Delivery Discipline and Incremental Visual Convergence practice this package satisfies. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status, to record this convergence step once implemented. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | Programme Sponsor approved implementation following Codex's no-blocking-findings review. Implemented exactly as scoped: `jarvis/interfaces/stdio_rpc.py` (`policyEngine` field), `src/App.jsx` (Sentinel row detail), `jarvis/tests/test_stdio_rpc.py` (1 updated + 1 new test). PST-0001 (2.36 to 2.37) aligned. 212 tests pass, validator 0 errors, build clean, Playwright-verified across connecting/offline/running states. Status Draft to Approved, version 0.2 to 1.0. Post-implementation, Codex reviewed the actual diff (no blocking findings) and recorded one further residual risk (Section 11 item 4): `policyEngine` is now part of the `platform.status` RPC contract, so a future `TrustTierPolicy` rename would be a user-visible change - accepted, not actioned. |
| 0.2 | 17 July 2026 | Claude Engineering Implementer | Recorded Engineering Reviewer (Codex) v0.1 review: no blocking findings, internal consistency confirmed against current code. Added Section 11 item 3 recording Codex's residual-risk note (manual Playwright verification only, no automated frontend test infrastructure exists) - accepted as a pre-existing, out-of-scope limitation. Pending Programme Sponsor approval. |
| 0.1 | 17 July 2026 | Claude Engineering Implementer | Initial draft: surface the ESR-0024 WP1-wired policy engine's identity in the System Health panel's Sentinel row, satisfying PBK-0001's Incremental Visual Convergence practice with real data only. Pending Engineering Reviewer review and Programme Sponsor approval. |
