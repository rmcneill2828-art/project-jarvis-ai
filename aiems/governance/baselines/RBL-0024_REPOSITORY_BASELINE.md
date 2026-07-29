# RBL-0024 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0024 |
| Title | ESR-0039 Repository Baseline (EBG-0108 Phase 1 - Guardian Cognitive Core) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]] |
| Previous Baseline | [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 29 July 2026 |
| HEAD at baseline creation | `0c2e7a2` |

---

# 2. Purpose

RBL-0024 records the repository baseline accepted by the Programme Sponsor at ESR-0039 WP3, superseding [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]]. ESR-0039 ran one Work Package: WP1, closing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108's Phase 1 scope - Guardian's conversation path was stateless and single-turn, with retained Personal Memory content never consulted; a new Guardian Cognitive Core now composes persona, retained memory and bounded conversation history before every provider call. Both independent WP2 verification passes (pre-commit Codex design review and post-commit Codex diff review) converged that this real, tested product code change is baseline-worthy.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; a future PCB-0001 refresh should reflect Guardian's Reasoning/Memory faculties moving from stateless pass-through to a genuine cognitive core |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Pre-commit design review (Codex)**: PASS, no blocking findings - confirmed the persona-string composition scope boundary was the right Phase 1 call given `ProviderRequest`'s single-turn shape shared by every provider adapter, and confirmed the Risk 2/EBG-0110 framing (Programme Sponsor decision, not silently resolved) was appropriate.

**Post-commit independent verification (Codex)**: PASS, no findings - independently re-read the real committed diff for `0c2e7a2`, confirmed it matched the approved design exactly (byte-identical persona with no memory/history, memory read fresh per call, bounded 6-exchange history, all four non-recordable response strings correctly excluded), confirmed no file under `src/`, `src-tauri/`, `jarvis/memory/` or `.github/workflows/` was touched, and confirmed the governance record (EBR-0001, AAM-0001, ESR-0039) accurately describes the actual change with no aspirational overclaiming.

**Real GitHub Actions CI**: green for `0c2e7a2` (run `30436758080`).

**The Programme Sponsor's determination**: **establish a new baseline**, per the same threshold applied at RBL-0021/RBL-0022/RBL-0023 - a genuine, independently-verified change to live conversation-path behaviour, backed by new test coverage, rather than documentation or governance churn alone.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/guardian/cognitive_core.py` (new) | `GuardianCognitiveCore` composes persona, retained Personal Memory content (read fresh every turn) and bounded (6-exchange) recent conversation history into a single system-prompt string. |
| `jarvis/guardian/runtime.py` | `GuardianRuntime.converse()` now composes via the cognitive core before each provider call, and records only semantically successful exchanges (excluding both `GuardianRuntime` boundary-error strings and `SentinelGatedConversationProvider`'s Sentinel-denial/provider-failure strings) into history. |
| `jarvis/tests/test_guardian_cognitive_core.py` (new) | 9 unit tests covering composition, memory/history section rendering and omission, metadata exclusion, and history bounding. |
| `jarvis/tests/test_guardian_runtime.py` | 5 new integration tests covering memory inclusion, fresh-per-turn memory reads, history threading, and exclusion of non-recordable responses from history. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Cognitive Architecture section updated (0.4 to 0.5) recording Reasoning/Memory faculties as Phase 1 implemented; Action/Voice/Vision remain not started. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108 marked Complete (Phase 1); EBG-0110 (Candidate Backlog) registered for the disclosed memory-content/external-provider policy gap. |
| Test suite | 396 Python tests plus 1 skip (was 382 plus 1 skip); no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. A future session should refresh it to reflect Guardian's conversation path moving from stateless single-turn pass-through to a memory-informed, multi-turn cognitive core - a materially different capability than PCB-0001's current description.

---

# 7. Architecture Outcomes

- Guardian's conversation path is no longer stateless or single-turn - a bounded recent-history window now informs every response.
- Retained Personal Memory content, previously implemented but entirely unconsulted during conversation, now genuinely informs Guardian's responses.
- This closes Phase 1 of JRM-0001's dependency chain (Guardian Cognitive Core); Phase 3 (Action), Phase 4 (Memory expansion), Phase 5 (Knowledge Graph/reasoning connection) and Phase 6 (Voice/Vision) remain future work, each requiring its own Engineering Implementation Package.
- A disclosed, not-yet-resolved policy gap (EBG-0110) now has live consequence: retained memory content reaches whichever provider is configured, including external cloud providers, with no policy layer distinguishing memory-sensitivity - accepted as scoped by Programme Sponsor decision at this session's WP1 approval.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- Action, Voice and Vision faculties are explicitly not implemented by this baseline;
- no relevance-ranking, summarisation or embedding-based retrieval was added to Personal Memory retrieval - `list_records()`'s full, unfiltered result is used as-is, disclosed as not scalable past a small personal store;
- no change was made to `ConversationRequest`, `ProviderRequest`, `SentinelGatedConversationProvider` or any provider adapter;
- no Sentinel/`TrustTierPolicy` policy change was made - EBG-0110 tracks the disclosed gap as separate future work;
- `src/`, `src-tauri/`, `jarvis/memory/` and `.github/workflows/` were not touched at all this session.

---

# 9. Verification

Repository validation performed during ESR-0039 WP2/WP3:

- Git working tree was clean; the session's intended content (`503c9a9..0c2e7a2`) pushed to `origin/main`.
- 396/397 Python tests passing plus 1 correctly-skipped win32-conditional test, up from 382/383 at RBL-0023 (14 new tests: 9 `GuardianCognitiveCore` unit tests, 5 `GuardianRuntime` integration tests).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count held at 184 across this session's governance edits, consistent with the established pre-existing false-positive category.
- Real GitHub Actions CI (run `30436758080`) green for `0c2e7a2`.
- Pre-commit Codex design review: Pass, no blocking findings. Post-commit Codex independent diff review: Pass, no findings (one disclosed, pre-existing Codex read-only-sandbox limitation prevented Codex from independently running `pytest` itself - `validate_repository.py` and the diff/design spot-check were both completed successfully in that same sandbox).
- The Programme Sponsor's own WP3 determination: establish a new baseline rather than retain RBL-0023 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0039** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0110 remains open (Candidate Backlog), tracking the disclosed memory-content/external-provider policy gap. Phase 3 (Action), Phase 4 (Memory expansion), Phase 5 (reasoning connection) and Phase 6 (Voice/Vision) remain unauthorised future work.
5. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at the next session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]] | Session this baseline is drawn from. |
| [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108 (Phase 1 closed this session) and EBG-0110 (registered this session, remains open). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture updated to record the Guardian Cognitive Core as Phase 1 implemented. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session, though this baseline's outcome makes it stale (Section 6). |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0023, following Codex's pre-commit design review (Pass) and post-commit independent diff review (Pass) and the Programme Sponsor's explicit WP3 decision to cut a new baseline rather than retain RBL-0023: WP1's real, tested Guardian Cognitive Core delivery warrants a new baseline. |
