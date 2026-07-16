# RBL-0015 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0015 |
| Title | ESR-0022 Repository Baseline (Production Provider Wiring) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0022 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 16 July 2026 |
| HEAD at baseline creation | `e4a04a0` |

---

# 2. Purpose

RBL-0015 records the repository baseline accepted by the Programme Sponsor at ESR-0022 WP7, superseding [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]]. Unlike ESR-0020/ESR-0021's UXP-polish increments (both judged incremental relative to RBL-0014's establishing session and retained), ESR-0022 WP1 changes JARVIS/Guardian's *default runtime behaviour*, not just its presentation: the production conversation path can now call a real external AI provider (OpenAI or Gemini) rather than only the deterministic local echo. The Programme Sponsor's own WP6/WP7 determination judged this a materially new operational capability, comparable in kind to RBL-0014's own establishing delivery (the Guardian Orb knowledge-graph capability at ESR-0019), not merely a UI refresh.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - stale, unchanged by this baseline, tracked as EBG-0056 |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0022 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0022_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP6 handover]] deliberately left the retain-vs-new-baseline question open (Section 8) rather than presuming an answer, since it was judged genuinely borderline - closer to RBL-0014's own establishing decision than to ESR-0020/ESR-0021's retentions.

The Programme Sponsor's determination: **establish a new baseline**, not retain RBL-0014. Rationale, in the Programme Sponsor's own words: RBL-0014 is explicitly the ESR-0019 baseline for the knowledge-graph delivery; this session is not just another incremental UI refresh - it adds the first default production provider wiring path, which changes Guardian's normal runtime behaviour, not just its presentation, a materially new operational capability. The repository now has a different default execution path plus a new live UXP status surface (the System Health panel), even though the separately-authorised sidecar cwd fix was its own distinct, smaller change.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/interfaces/stdio_rpc.py` | `build_default_runtime()` now optionally registers a real `OpenAIProvider` or `GeminiProvider` as the primary `text-generation` route provider - configurable via `JARVIS_PRIMARY_PROVIDER` (default `openai`, per PEM-001's Primary designation), gated on that provider's credential env var being present and non-blank - with `LocalEchoProvider` always retained as the final failover. `platform.status` gained a new `providers` field. |
| `jarvis/interfaces/sentinel_conversation.py`, `jarvis/guardian/runtime.py` | New `configured_providers()` accessors surfacing the active provider route to the RPC layer. |
| `jarvis/tests/test_stdio_rpc.py` | Six new tests: default-primary wiring, explicit `JARVIS_PRIMARY_PROVIDER` selection, credential-absent fallback, unselected-provider-credential-ignored, and a blank-but-present model env var falling through to the default model. All use an explicit synthetic `environ`, never depending on or exercising real host credentials. |
| `src/App.jsx`, `src/styles.css` | New `SystemHealthPanel`: Guardian/Sentinel/Providers, derived only from real `platform.status` fields, distinct from `DiagnosticsPanel`'s mixed real/static rows. Verified via Playwright against the real Vite dev server across connecting/error/populated states. |
| `src-tauri/src/lib.rs` | Separately Sponsor-authorised fix (outside EIP-ESR0022-001's scope): `spawn_backend()` now anchors the Python sidecar's working directory to `CARGO_MANIFEST_DIR`'s parent (the repository root), fixing a pre-existing defect (from ESR-0017 WP9) where `python -m jarvis` silently failed whenever `cargo run`'s launch cwd wasn't the repository root - found during the Programme Sponsor's live visual verification of this WP. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0070 and EBG-0072 marked Complete; EBG-0073 (UXP Duplicate Monitoring Elements Tidy-up) added as a new Approved Backlog item, discovered by the Programme Sponsor during the same live verification - not actioned by this baseline. |
| [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] | v1.0, Approved. An earlier revision (0.1) was retroactive - implementation drafted before the package existed - and was correctly declined by the Engineering Reviewer; fully reverted before any commit. v0.2 was reviewed and approved as a genuine prospective package before real implementation began. |
| Test suite | Grew from 204 (RBL-0014) to 209 passing tests, zero regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is unchanged by this baseline and remains stale on the specific point this session addresses - it does not yet describe JARVIS as having a live external-provider conversation path. Tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056 (not actioned this session; that item covers PCB-0001's broader staleness generally).

---

# 7. Architecture Outcomes

- First session where JARVIS/Guardian's default production conversation path (`build_default_runtime()`, the function the Tauri sidecar actually spawns) can call a real external AI model, not only the deterministic local-echo provider used since ESR-0017 WP9's foundation scope.
- `platform.status`'s RPC contract extended (`providers` field) for the first time since ESR-0017 WP9 established it - a precedent for how future real-state fields should be added to that contract.
- First dedicated System Health UXP surface, distinct from the general-purpose `DiagnosticsPanel` - though this surfaced a real duplication (EBG-0073) between the two, not yet resolved.
- A second, unrelated defect (the sidecar `cwd` anchoring) was found and fixed only because the Programme Sponsor insisted on a live visual check before accepting the WP - direct evidence for why live verification, not just automated tests, remains part of this project's acceptance process.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0023 artefact is created by this baseline - ESR-0022 may continue with further Work Packages, or a future session may open separately; both are Programme Sponsor decisions not made by this baseline;
- PCB-0001 is not refreshed - tracked as EBG-0056, not actioned here;
- EBG-0073 (System Health panel / Diagnostics panel duplication) is recorded but not resolved by this baseline;
- streaming notifications, production sidecar packaging (`tauri-plugin-shell`), and Anthropic/OpenRouter/Ollama provider adapters remain not implemented (EBG-0050 remaining scope, PEM-001);
- only one real provider (the selected primary) plus `LocalEchoProvider` is wired per route - simultaneous multi-real-provider failover ahead of local-echo was explicitly excluded by EIP-ESR0022-001.

---

# 9. Verification

Repository validation performed during ESR-0022 WP6/WP7:

- Git working tree was clean; a single commit (`e4a04a0`) pushed to `origin/main` since RBL-0014's baseline point (`29e7306`, ESR-0021 WP7 acceptance).
- Repository branch was `main`, synchronised with `origin/main` (`HEAD` confirmed at `e4a04a0` via `git rev-parse` against both local and `origin/main` after `git fetch origin main`).
- 209/209 tests passing, zero regressions since RBL-0014's 204.
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 85 warnings - the same pre-existing warning count as every prior baseline.
- The live Tauri desktop app (`npm run tauri dev`) was run twice during this session: once revealing the sidecar `cwd` defect (`No module named jarvis`), and once confirming the fix (`Guardian runtime foundation started.`) - real end-to-end verification, not only automated/mocked checks.
- The Engineering Reviewer performed WP6 Independent Repository Verification: **Pass** - repository state confirmed to match the commit's claims, the disclosed process deviation (EIP-ESR0022-001 v0.1's retroactive implementation, fully reverted before any commit) confirmed accurately characterised with no trace in repository history.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0014 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0022 or open a new session** - whether ESR-0022 continues with further Work Packages or closes here is a separate Programme Sponsor decision, not made by this baseline.

Future work against this baseline should include:

1. This document and [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - specifically EBG-0073 (UXP duplicate monitoring tidy-up, a natural quick next WP) and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]'s remaining Near-term horizon (EBG-0058, EBG-0065, EBG-0068, the REG-0001 HST/FCH gap).
5. [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] and the [[ESR-0022_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP6 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0022_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0022 WP6 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]] | Approved implementation package this baseline's deliverables were implemented against. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - remains stale on this point, tracked as EBG-0056, not refreshed by this baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0070/EBG-0072 completed, EBG-0073 remains a candidate for a future WP. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Roadmap that sequenced this session's WP selection. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0014, following the Engineering Reviewer's WP6 Pass and the Programme Sponsor's explicit WP7 decision to cut a new baseline rather than retain RBL-0014: production provider wiring changes Guardian's default runtime behaviour, a materially new operational capability. |
