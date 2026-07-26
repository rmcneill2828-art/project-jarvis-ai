# RBL-0022 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0022 |
| Title | ESR-0036 Repository Baseline (EBG-0108 First Increment - Guardian Persona Injection) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] |
| Previous Baseline | [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 26 July 2026 |
| HEAD at baseline creation | `26dfc55` |

---

# 2. Purpose

RBL-0022 records the repository baseline accepted by the Programme Sponsor at ESR-0036 WP4, superseding [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]]. ESR-0036 ran two Work Packages: WP1 (EBG-0108's first implementation increment - static Guardian persona injection, threaded through the Guardian conversation path into every live Sentinel provider adapter) and WP2 (consolidated documentation staleness fix - README.md/COC-0001/PBK-0001/PST-0001, plus retroactive creation of this session's own report). Both independent WP3 views (Engineering Implementer and Engineering Reviewer) converged on this being baseline-worthy, citing WP1's genuine product code change and new test coverage as the justification beyond pure governance churn.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; WP1's persona injection is a Guardian identity capability already covered by AAM-0001's architecture, not a new capability tier PCB-0001 tracks |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0036_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP3 handover]] recorded two independently-reached views (Sections 9-10), both recommending a new baseline rather than retaining RBL-0021.

**Engineering Implementer's view**: WP1 delivered a genuine, live-verified product code change - the first implementation work of any kind against EBG-0108 (Guardian Cognitive Core), touching `jarvis/guardian/`, `jarvis/interfaces/` and all three live Sentinel provider adapters, backed by 7 new automated tests. This is the same category of change that justified RBL-0021 itself at ESR-0035 WP5: a real, functionally-verified change to shipped conversation behaviour, not pure governance churn.

**Engineering Reviewer's (Codex) independent view**: converged, naming RBL-0022 directly - "the session includes real product behavior changes in the Guardian conversation path and Sentinel provider request plumbing, with tests added across affected layers. That is baseline-worthy; the documentation-only WP2 would not be enough on its own." Codex independently confirmed the exact diff-stat figures (20 files, 315 insertions, 47 deletions) and that no `src/`/`src-tauri/`/`.github/workflows/`/`jarvis/memory/` file changed, before reaching this view - and separately caught a real REG-0001/ESR-0036 version-tracking mismatch during its own WP3 verification pass, fixed before this baseline was accepted.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/guardian/config.py` | New `DEFAULT_GUARDIAN_PERSONA` constant and `GuardianRuntimeConfig.persona` field, formally adopted from AAM-0001's Guardian Persona section (WP1). |
| `jarvis/guardian/runtime.py`, `jarvis/interfaces/conversation.py`, `jarvis/interfaces/sentinel_conversation.py` | `GuardianRuntime.converse()` threads the configured persona through a new `ConversationRequest.persona` field into `SentinelGatedConversationProvider.generate()` (WP1). |
| `sentinel/providers.py`, `sentinel/openai_provider.py`, `sentinel/gemini_provider.py`, `sentinel/ollama_provider.py` | New `ProviderRequest.system_prompt` field, injected into each provider's own native system-prompt mechanism only when truthy - additive, backward-compatible. `LocalEchoProvider` untouched (WP1). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | New "Guardian Persona" section (0.3 to 0.4) formally adopting the ESR-0004 recovered "EKR-0001 Task 2" JARVIS character draft for Guardian, Sponsor-approved verbatim; household-role differentiation explicitly disclosed as deferred (WP1). |
| `README.md`, [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Stale RBL-0020/ESR-0035-open current-state references corrected to RBL-0021/ESR-0036-open, applying PBK-0001's own Whole-Document Staleness Sweep on Edit discipline, across two follow-on fix rounds (WP2). |
| [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] | Created retroactively during WP2 - a disclosed process gap against PBK-0001's own session lifecycle, which specifies the report should be created at WP0B (WP2). |
| Test suite | 381 Python tests plus 1 skip, up from 374 (7 new tests across persona-injection layers); no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. WP1's persona injection realises a capability AAM-0001's architecture already described (Guardian identity) rather than introducing a new capability tier PCB-0001 needs to record.

---

# 7. Architecture Outcomes

- Guardian now has a persistent, configurable identity reaching every live provider call - closing the "no persistent persona" portion of the gap AAM-0001 and EBG-0108 both flagged. Memory-informed context and any reasoning loop remain explicitly deferred to future EBG-0108 increments.
- A previously dropped thread - Guardian's actual character, recovered at ESR-0004 as "EKR-0001 Task 2" but never promoted into backlog alongside its siblings - is now formally closed via AAM-0001 v0.4.
- The recurring RBL-current-baseline documentation-staleness pattern (ESR-0033 WP1, ESR-0035 WP1, now ESR-0036 WP2) was corrected again, this time deliberately deferred to the session's close by Programme Sponsor direction to consolidate two passes into one - and itself surfaced a genuine lesson: a targeted sweep of only the directly-touched sections missed further stale references elsewhere in the same document, caught by Codex's independent post-commit review.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no memory-context retrieval or reasoning loop is authorised by this baseline - only static persona injection;
- household-role differentiation (children/adults/guests) remains explicitly deferred, pending user-identity plumbing that does not exist in `ConversationRequest` today;
- all other open EBR-0001 backlog items remain out of scope, not addressed by this baseline;
- no new third-party product dependencies were introduced this session;
- `src/`, `src-tauri/`, `.github/workflows/` and `jarvis/memory/` were not touched at all this session.

---

# 9. Verification

Repository validation performed during ESR-0036 WP3/WP4:

- Git working tree was clean; the session's intended content range (`6cf2aeb`..`26dfc55`) pushed to `origin/main`.
- 381/381 Python tests passing plus 1 correctly-skipped win32-conditional test, up from 374/374 at RBL-0021 (7 new persona-injection tests).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 172 warnings - unchanged from RBL-0021's closing figure, after one real fix (a REG-0001/ESR-0036 version-tracking mismatch caught by the Engineering Reviewer's own WP3 verification pass, fixed and re-confirmed clean).
- `git diff --stat 6cf2aeb..26dfc55` independently re-run by the Engineering Reviewer, confirmed to match exactly (20 files, 315 insertions, 47 deletions).
- The Engineering Reviewer performed WP3 Independent Repository Verification: **Pass, after one fix round** - independently confirmed the diff-stat figures, file-list accuracy, that `src/`/`src-tauri/`/`.github/workflows/`/`jarvis/memory/` were untouched, and independently re-ran `validate_repository.py` itself to confirm the fix (its sandbox allowed this on the fix-round pass, unlike `pytest`, which remained blocked by a temp-directory restriction - a disclosed environmental limitation consistent with prior sessions).
- The Programme Sponsor's own WP4 determination: establish a new baseline rather than retain RBL-0021 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0036** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0108's first increment delivered; the item remains open for its memory/reasoning-loop increments.
5. The [[ESR-0036_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP3 handover]] for full delivery detail.
6. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern (ESR-0033 WP1, ESR-0035 WP1, ESR-0036 WP2), this is expected to surface at the next session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0021_REPOSITORY_BASELINE|RBL-0021]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0036_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0036 WP3 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian Persona section (0.3 to 0.4) - the architecture WP1 implements against. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not affected by this session's scope. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0108's first increment delivered this session. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 26 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0021, following the Engineering Reviewer's WP3 Pass (after one fix round) and the Programme Sponsor's explicit WP4 decision to cut a new baseline rather than retain RBL-0021: WP1's real Guardian persona-injection change (new module wiring, live conversation-path refactor, new test coverage) together with WP2's documentation correction warrant a new baseline, agreeing with both independent WP3 baseline views. |
