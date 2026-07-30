# RBL-0026 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0026 |
| Title | ESR-0043 Repository Baseline (Guardian Persona - JARVIS Characterisation Refinement) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] |
| Previous Baseline | [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 30 July 2026 |
| HEAD at baseline creation | `5a88539` |

---

# 2. Purpose

RBL-0026 records the repository baseline accepted by the Programme Sponsor at ESR-0043 WP3, superseding [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]]. ESR-0043 ran one Work Package: WP1, refining Guardian's persona toward the classic film J.A.R.V.I.S. characterisation the Programme Sponsor described - precise/economical phrasing, an understated register with bounded dry wit, mild reasoned pushback, and a "Sir"/preferred-name addressing convention - implemented additively in `jarvis/guardian/config.py`'s `DEFAULT_GUARDIAN_PERSONA`, the literal text Guardian composes into every live conversation turn. Unlike ESR-0041/ESR-0042 (architecture/policy-definition or evaluation-only work with no runtime behaviour change), this session changed real, live product behaviour, warranting a new baseline per the Programme Sponsor's explicit determination.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; a future refresh should note Guardian's persona has been extended beyond the ESR-0036-approved baseline |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for a future session |

---

# 4. Baseline Recommendation Rationale

**Design review (Codex, direct `codex exec -s read-only` invocation)**: Pass, with non-blocking findings - confirmed the additive-only approach was correct, the "Sir" addressing convention was an acceptable Sponsor-facing tradeoff correctly scoped as a single-user stopgap pending GAM-0001's household-role wiring, the British-cadence/American-voice mismatch disclosure was honest and correctly excluded from the injected persona text, and the "dry wit"/"mild pushback" wording did not conflict with the existing "never claims emotions"/"assists, humans decide" constraints. Three non-blocking clarifications folded in before implementation.

**Post-commit independent verification (Codex)**: Pass - independently re-read the real pushed diff for commit `5a88539`, confirmed it touched exactly the 5 claimed files and nothing outside that scope, confirmed the AAM-0001 diff shows only added lines to the Guardian Persona section (no existing sentence deleted or reworded), confirmed `DEFAULT_GUARDIAN_PERSONA`'s new text substantively matches AAM-0001's new persona text despite the person-perspective transformation, and confirmed no other `jarvis/` or `sentinel/` file was touched.

**Programme Sponsor approval**: obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**The Programme Sponsor's determination**: **establish a new baseline**, since this session's WP1 changed the actual text Guardian composes into every live conversation - a genuine, live, observable product-behaviour change (unlike ESR-0041's GAM-0001 architecture-only addition or ESR-0042's negative-result evaluation, both retained), backed by a clean pytest run and confirmed by independent Codex review.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/guardian/config.py` | `DEFAULT_GUARDIAN_PERSONA` extended additively with the JARVIS characterisation refinement - precise/economical phrasing, understated register with bounded dry wit, mild reasoned pushback, and a "Sir"/preferred-name addressing convention with an explicit no-implied-GAM-0001-authority disclaimer. No existing text reworded or removed. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian Persona section updated (0.6 to 0.7), recording the refinement and a governance-only note disclosing the Piper voice (`en_US-lessac`) remains American-accented regardless of this refinement's British-inflected wording. |
| Test suite | No new tests required - `test_guardian_runtime.py:392` compares `DEFAULT_GUARDIAN_PERSONA` against itself and is unaffected by a text-content change. 418 passed, 1 skipped (unchanged). |
| [[EIP-ESR0043-001_GUARDIAN_PERSONA_JARVIS_CHARACTERISATION_REFINEMENT|EIP-ESR0043-001]] | New Engineering Implementation Package recording this session's scope, Codex review and Programme Sponsor approval. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. A future session should note that Guardian's persona now includes the classic-JARVIS refinement layer alongside the ESR-0036-approved baseline persona.

---

# 7. Architecture Outcomes

- Guardian's persona is extended, not replaced - every existing approved trait (calm/measured/professional, honest-by-default, respects human authority, notices risk without controlling, transparent about reasoning/uncertainty, quiet competence, never claims emotion/humanity, stable identity) remains unchanged.
- A disclosed, unresolved product-experience mismatch is recorded: Guardian's wording may lean British-inflected while its synthesised voice (`en_US-lessac`, EBG-0112/EBG-0113) remains American-accented - no code change is authorised to resolve this by this baseline.
- The household-role addressing gap (GAM-0001 Section 8.1 not wired to the conversation path) is disclosed, not solved - the "Sir" convention is an explicit, temporary single-user stopgap.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no change to `ConversationRequest`, `GuardianCognitiveCore`, `ProviderRequest`, or any provider adapter - this is a persona-text-only change, folded entirely into the existing static `persona` string;
- no household-role/speaker-identity wiring into the conversation path;
- no evaluation or adoption of a British-accented Piper voice dataset;
- no UXP (`src/`, `src-tauri/`) change;
- `jarvis/memory/`, `sentinel/` and `.github/workflows/` were not touched at all this session.

---

# 9. Verification

Repository validation performed during ESR-0043 WP2/WP3:

- Git working tree was clean; the session's intended content (`115212a..5a88539`) pushed to `origin/main`.
- 418/419 Python tests passing plus 1 correctly-skipped test, unchanged from RBL-0025 (no test needed rewriting - the existing equality assertion is unaffected by a text-content change).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors throughout; warning count at 257, consistent with the established pre-existing cross-document-reference false-positive category (two additional warnings from this session's own new cross-referencing text).
- Codex design review (direct `codex exec -s read-only` invocation): Pass, with non-blocking findings, folded in before implementation. Post-commit Codex independent diff review: Pass, no findings (one disclosed, pre-existing Codex read-only-sandbox limitation again prevented Codex from independently running `validate_repository.py`/`pytest` itself - the diff/content spot-check was completed successfully in that same sandbox).
- Live qualitative check not performed - no conversational provider was configured in this implementation environment, disclosed honestly rather than fabricated.
- The Programme Sponsor's own WP3 determination: establish a new baseline rather than retain RBL-0025 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0043** - the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. A future session performing a live qualitative smoke check of the refined persona once a conversational provider is configured, per EIP-ESR0043-001 Section 10 item 3 (advisory, not blocking).
5. **The README/COC-0001/PBK-0001 current-baseline references will themselves become stale the moment this baseline is accepted** - by established pattern, this is expected to surface at a future session's WP0A and should be corrected there per PBK-0001's Documentation-Debt Priority discipline, not treated as a surprise.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0025_REPOSITORY_BASELINE|RBL-0025]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] | Session this baseline is drawn from. |
| [[EIP-ESR0043-001_GUARDIAN_PERSONA_JARVIS_CHARACTERISATION_REFINEMENT|EIP-ESR0043-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture updated to record the persona refinement. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.1 Household Role Model - the deferred capability the "Sir" convention is a disclosed stopgap for. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0025, following Codex's design review (Pass, with non-blocking findings folded in) and post-commit independent diff review (Pass) and the Programme Sponsor's explicit WP3 decision to cut a new baseline rather than retain RBL-0025: WP1's real, live-behaviour-changing Guardian persona refinement warrants a new baseline. |
