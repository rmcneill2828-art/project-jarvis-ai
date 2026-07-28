# RBL-0023 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0023 |
| Title | ESR-0037 Repository Baseline (EBG-0109 Findings 1/2(c) - Ollama Timeout Risk and Tauri IPC Indefinite Hang) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0037_ENGINEERING_SESSION_REPORT|ESR-0037]] |
| Previous Baseline | [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 28 July 2026 |
| HEAD at baseline creation | `2b1e531` |

---

# 2. Purpose

RBL-0023 records the repository baseline accepted by the Programme Sponsor at ESR-0037 WP3, superseding [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]]. ESR-0037 ran one Work Package: WP1, closing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0109's Findings 1 and 2(c) - a reasoning-model timeout risk in the Ollama provider adapter, and an indefinite-hang/no-visible-error symptom in the Tauri desktop shell's backend IPC path. Both independent WP2 verification passes (pre-commit Codex design review and post-commit Codex diff review) converged that this real, tested product code change is baseline-worthy.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; this WP is a reliability fix to an already-tracked capability (Ollama fallback provider, UXP-backend bridge), not a new capability tier |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Pre-commit design review (Codex)**: PASS, no blocking findings - confirmed the proposed scope against the live source of `sentinel/ollama_provider.py` and `src-tauri/src/lib.rs` was technically sound and correctly bounded, not overreaching into Finding 2(b)'s still-unconfirmed root cause.

**Post-commit independent verification (Codex)**: PASS, no findings - independently re-read the real committed diff for `2b1e531`, confirmed it matched the approved design exactly, confirmed no file under `src/`, `jarvis/memory/` or `.github/workflows/` was touched, and confirmed the governance record (EBR-0001, ESR-0037) accurately describes the actual change with no aspirational overclaiming.

**Real GitHub Actions CI**: green across all four jobs (`python`, `rust`, `playwright`, `frontend-build`) for `2b1e531` (run `30342589297`).

**The Programme Sponsor's determination**: **establish a new baseline**, per the same threshold applied at RBL-0021/RBL-0022 - a genuine, independently-verified change to live conversation-path/IPC behaviour, backed by new test coverage, rather than documentation or governance churn alone.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `sentinel/ollama_provider.py` | `execute()` now unconditionally sends `think: false` and `options: {"num_ctx": 4096}` (new `DEFAULT_NUM_CTX` constant) - fixes EBG-0109 Finding 1's disclosed 3m15s reasoning-model timeout measurement. |
| `src-tauri/src/lib.rs` | `call_backend()` replaces the previously-unbounded `receiver.recv()` with a 120s `recv_timeout` (new `BACKEND_CALL_TIMEOUT` constant); a new `remove_pending()` helper cleans up the stale pending-map entry on timeout; a new `route_response()`, extracted from `dispatch_line()`, makes the response-routing path unit-testable. Fixes EBG-0109 Finding 2(c)'s indefinite-hang/no-visible-error symptom. |
| `jarvis/tests/test_ollama_provider.py` | Two existing payload-shape assertions updated, one new test added confirming `think`/`options.num_ctx` are always present. |
| `src-tauri/src/lib.rs` (tests) | 5 new Rust unit tests covering `remove_pending()` and `route_response()`, including the late-response-after-cleanup case Codex's design review specifically asked for. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0109 updated: Findings 1 and 2(c) marked closed; Findings 2(a)/2(b) and recommendation (d) explicitly disclosed as still open, pending a live, controlled reproduction this implementation environment cannot perform. |
| Test suite | 382 Python tests plus 1 skip (was 381 plus 1 skip); 5 new Rust unit tests; no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. This WP is a reliability fix to the already-tracked Ollama fallback provider and UXP-backend bridge capabilities, not a new capability.

---

# 7. Architecture Outcomes

- The Ollama provider adapter no longer risks a structural timeout from ordinary reasoning-model behaviour - `think`/`num_ctx` are now bounded on every request, independent of which model is configured.
- The Tauri desktop shell's backend IPC path can no longer hang indefinitely with no user-visible error; a stalled backend now surfaces a clear, bounded-time error instead of the OS's native "(Not Responding)" state.
- EBG-0109's more serious, still-unconfirmed defect (Finding 2(b): a request sometimes never reaching Ollama at all) remains open, honestly disclosed rather than assumed fixed - this baseline improves the symptom's visibility and the timeout-adjacent risk, but does not claim to have root-caused it.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- Finding 2(a)/2(b) (live GUI reproduction) and recommendation (d) (stdio_rpc.py write-lock/heartbeat interaction) are explicitly not resolved by this baseline - EBG-0109 remains open;
- no change was made to `stdio_rpc.py`, `sentinel/orchestrator.py` or `jarvis/interfaces/sentinel_conversation.py` - all three were reviewed and found to carry no code-level defect explaining Finding 2(b);
- all other open EBR-0001 backlog items remain out of scope;
- no new third-party product dependencies were introduced this session;
- `src/`, `jarvis/memory/` and `.github/workflows/` were not touched at all this session.

---

# 9. Verification

Repository validation performed during ESR-0037 WP2/WP3:

- Git working tree was clean; the session's intended content (`ff5f67d..2b1e531`) pushed to `origin/main`.
- 382/382 Python tests passing plus 1 correctly-skipped win32-conditional test, up from 381/381 at RBL-0022 (1 new Ollama provider test). 5 new Rust unit tests, all passing. `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check` all clean.
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count rose from 172 at RBL-0022's closing figure to 177 by this baseline's acceptance, across this session's own governance edits (ESR-0037/REG-0001 registrations, this document's own creation, and several REG-0001 version-history entries whose summary text occasionally contains a phrase the checker's cross-document "Section N" pattern matches against an unrelated document) - all disclosed as the same pre-existing false-positive category, not new defects.
- Real GitHub Actions CI (run `30342589297`) green across all four jobs for `2b1e531`.
- Pre-commit Codex design review: Pass, no blocking findings. Post-commit Codex independent diff review: Pass, no findings.
- The Programme Sponsor's own WP3 determination: establish a new baseline rather than retain RBL-0022 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0037** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0109 remains open (Findings 2(a)/2(b), recommendation (d)) pending a live, controlled reproduction on the Programme Sponsor's own desktop session.
5. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at the next session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0037_ENGINEERING_SESSION_REPORT|ESR-0037]] | Session this baseline is drawn from. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0109 - Findings 1/2(c) closed this session; item remains open. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not affected by this session's scope. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0022, following Codex's pre-commit design review (Pass) and post-commit independent diff review (Pass) and the Programme Sponsor's explicit WP3 decision to cut a new baseline rather than retain RBL-0022: WP1's real, tested fix to the Ollama provider adapter and Tauri IPC layer warrants a new baseline. |
