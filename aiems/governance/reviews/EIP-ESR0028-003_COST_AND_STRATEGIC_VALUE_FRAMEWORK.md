# EIP-ESR0028-003 - Cost and Strategic Value Framework

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0028-003 |
| Artefact ID | EIP-ESR0028-003 |
| Title | Cost and Strategic Value Framework |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0045, EBG-0049, EBG-0024) |
| Intended Session | ESR-0028 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Close EBG-0045 (Cost and Strategic Value Framework), EBG-0049 (Cost-Aware Provider Routing and PEM-001 Revisit) and EBG-0024 (JARVIS Cost Strategy) by revising the existing provider evaluation artefact rather than creating a new document, following direct repository investigation.

---

# 3. Related Backlog Items

- **EBG-0045** (`EBR-0001:114`): "Define evaluation criteria for cloud providers, commercial options, cost, privacy, strategic value and product benefit. See also EBG-0049 ... overlapping scope, consider together when either is actioned."
- **EBG-0049** (`EBR-0001:118`): "Define a cost/performance balance policy for Sentinel provider routing ..., and revisit PEM-001's provider scoring to confirm cost is weighted as an explicit first-class criterion rather than incidental. Should account for institutional cloud/education resources potentially available to the Programme Sponsor as a cost-reduction lever."
- **EBG-0024** (`EBR-0001:93`): "Define cost principles before paid providers, cloud services, voice, vision or storage decisions materially affect the programme."

---

# 4. Repository Context and Investigation Findings

## 4.1 PEM-001's current cost treatment

`aiems/evaluations/PEM-001_AI_PROVIDER_EVALUATION_MATRIX.md` (v1.0, Approved, registered `REG-0001:182`) already names Cost as a weighted criterion (line 106): "Cost | 10% | Pricing predictability and suitability for iterative development." Cost is not literally missing, but EBG-0049's own framing - "confirm cost is weighted as an explicit first-class criterion rather than incidental" - is fair: at 10% it is tied for the lowest weight alongside three other criteria, its description is about predictability rather than active cost minimisation, and the Decision Outcome section (lines 176-193, ESR-0015 WP3a) records no visible cost tradeoff in the scoring rationale for selecting OpenAI/Gemini - reliability and capability language dominates. No self-hosted/free-tier-first posture appears anywhere in the document.

## 4.2 ADR-0008's anticipation of this work

`aiems/governance/decisions/ADR-0008_HYBRID_AI_RUNTIME_STRATEGY.md` (v1.0, Approved) decides "local-first where appropriate; cloud providers allowed where strategic value justifies cost" (lines 69-76) and states "Provider selection shall consider trust, policy, privacy, cost, value and context" (line 82) - but only at the strategy-principle level. Its own Related Artefacts table (line 109) points to EBR-0001 as where "future provider and cost framework work" is recorded, i.e. ADR-0008 explicitly anticipated EBG-0045-type work rather than performing it. Nothing here needs to change; PEM-001 is the correct place to concretise the principle ADR-0008 already states.

## 4.3 ESR-0016 trust-tier classification

**Corrected at v0.2** - v0.1 stated this mechanism was unwired from production; that was wrong and has been corrected following an Engineering Reviewer finding. `sentinel/policy.py` defines a real, implemented `TrustTier`/`TrustCategory`/`TrustTierPolicy` mechanism (lines 10-32, 79). `SentinelTrustGateway`'s own class-level default remains `SimpleApprovalPolicy` (unchanged, confining blast radius per EBG-0074's own design), but the live runtime construction path - `build_default_runtime()` in `jarvis/interfaces/stdio_rpc.py` - has wired `TrustTierPolicy` in as the actual production policy engine since **ESR-0024 WP1 (EBG-0074, Complete, `EBR-0001:172`)**, directly asserted by `jarvis/tests/test_stdio_rpc.py` (`build_default_runtime().sentinel_gateway().policy_engine` is `TrustTierPolicy`). `TrustTierPolicy` is therefore genuinely in the live decision path today, not additive-only. It still classifies purely on trust/safety dimensions - source, intent, payload type, approval requirement - and **no cost dimension exists in it**: no per-request cost estimation, no budget data, no cost-routing design. EBG-0049's "candidate mechanism" framing was about cost-routing specifically, and on that narrower point it remains accurate - `TrustTierPolicy` is production-wired but cost-blind, which is the correct basis for excluding a code change here (see Explicit Exclusions below), not any claim that it is unwired.

## 4.4 No existing cost logic in provider orchestration code

`sentinel/providers.py`, `provider_config.py`, `gemini_provider.py`, `openai_provider.py`, `ollama_provider.py` and `local_provider.py` contain zero cost, budget or pricing logic. Building genuine dynamic cost-aware routing (per-request cost estimation, budget thresholds, automatic tier escalation) is entirely greenfield product code, not a documentation revision.

## 4.5 Institutional education credits

The only concrete detail anywhere in the repository is in an unprocessed raw chat log, `aiems/History/Full Chat/FCH-0016a_GPT_FULL_CHAT_HISTORY.md:1191-1256` - a `@regents.ac.uk` email potentially unlocking GitHub Education / Azure for Students ($100 credit); OpenAI is noted as having no equivalent academic credit programme. This is exploratory chat content, not an approved artefact, and not confirmed (eligibility untested, credit not claimed). It can be disclosed as a known, not-yet-actioned lever - it cannot be treated as an available resource or budgeted against.

## 4.6 JRM-0001 sequencing and EBG-0024 overlap

`JRM-0001_PROJECT_ROADMAP.md:137`: "EBG-0045 / EBG-0049 ... action together, not separately ... directly relevant once the Near-term production-provider-wiring item ... happens, since that is where cost first becomes a live concern." That trigger has occurred: `PST-0001:375` confirms these are "now live-relevant since real billed provider usage exists via EBG-0070" (production provider wiring, Complete, ESR-0022 WP1). `JRM-0001:146` separately flags EBG-0024 as "likely mergeable" with this cluster. EBG-0024's own trigger condition - "before paid providers ... materially affect the programme" - has also now occurred via EBG-0070's live billed usage, making it timely to close alongside its siblings rather than leaving it as a fourth, near-duplicate open item.

## 4.7 An existing precedent to generalise

`EBR-0001:133` (EBG-0057, Complete) already records an explicit Programme Sponsor budget constraint for a different backlog item: no budget for new recurring spend beyond what is already decided, self-hosted/no-new-recurring-spend as the hard default unless the Programme Sponsor states otherwise. This has been treated as a general standing rule in practice, but has never been written into PEM-001 - the artefact that actually governs AI provider selection. Generalising it there, rather than leaving it scoped to one unrelated backlog item's rationale, is the natural fix and directly satisfies EBG-0024's "define cost principles" ask.

---

# 5. Scope

This package authorises a future implementation to revise `PEM-001_AI_PROVIDER_EVALUATION_MATRIX.md` only - no new document is created (avoiding duplicate documentation), and no product code is touched:

1. Reweight the Evaluation Criteria table so Cost is genuinely first-class rather than tied-lowest, and revise its description to state an explicit no-discretionary-recurring-spend default (generalising EBG-0057's precedent into provider selection specifically).
2. Add a new "Cost and Strategic Value Principles" section stating: the no-discretionary-budget default; that strategic value and product benefit are already covered by the existing Capability Coverage / Resilience Fit / Vendor Independence criteria (no new criteria invented); and disclosing the institutional education credit possibility as a known, unconfirmed, not-yet-actionable future lever, citing its raw chat-log origin honestly.
3. Add a "Cost-Aware Routing Policy (Design Principle)" note recording the *policy decision* EBG-0049 asks for - prefer lower-cost/local/free providers by default, escalate to higher-capability/cost providers only when task requirements demand it - while explicitly scoping out dynamic implementation (adding a cost dimension to `TrustTierPolicy`'s classification, or otherwise wiring cost logic into `ProviderOrchestrator`) as separate, not-yet-authorised future work, since no per-token cost data exists in-repo yet. `TrustTierPolicy` is already production-wired (EBG-0074) but remains cost-blind by design today - this package defines the policy it would need to implement against, not the implementation itself.
4. Record a Decision Outcome addendum disclosing this revision, dated and attributed.
5. Close EBG-0045, EBG-0049 and EBG-0024 in EBR-0001 as `Complete`, each with a disclosed rationale distinguishing "policy defined" (delivered by this package) from "dynamic routing implemented" (explicitly not delivered, remains future work).

---

# 6. Authorised Files

1. `aiems/evaluations/PEM-001_AI_PROVIDER_EVALUATION_MATRIX.md`
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. Evaluation Criteria table: Cost moves from 10% to 15%, description changes to name the no-discretionary-recurring-spend default explicitly. Weight taken from Latency and SDK/API Maturity (10% each to 7.5% each, i.e. -2.5pp each) rather than from Capability Coverage or Reliability, since those two remain the most safety/quality-relevant criteria and should not be diluted to fund the cost reweighting. Total remains 100%.
2. New "Cost and Strategic Value Principles" section inserted after Evaluation Criteria, before Initial Qualitative Assessment, containing exactly the three points in Scope item 2.
3. New "Cost-Aware Routing Policy (Design Principle)" note inserted immediately after Resilience Principles, containing exactly the policy statement and explicit implementation-scoped-out disclosure from Scope item 3.
4. Decision Outcome section gets a dated addendum paragraph (not a rewrite of the existing ESR-0015 WP3a record) noting this framework revision and its date/session.
5. PEM-001 Version History gets a new entry; Document Control Version bumped to 1.1, Status remains Approved.
6. EBR-0001 closures for EBG-0045/EBG-0049/EBG-0024 each disclose: what was defined (criteria reweighting, principles, policy statement) versus what remains future work (dynamic cost-aware routing code, any actual claim on institutional education credits).

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to `sentinel/` provider orchestration code, `TrustTierPolicy` (already production-wired per EBG-0074, but cost-blind by design), or any dynamic/automatic cost-based routing logic - Section 4.3/4.4 found this would require real design work and cost data this package does not have; EBG-0049's own text asks only for a defined *policy*, not an implementation.
2. Any claim, application, or configuration action toward the institutional education credit possibility - Section 4.5 found it unconfirmed and outside this package's evidence base.
3. Creating a new, separate cost-strategy document - Section 4.1/4.7 found PEM-001 is the correct, already-existing home; a new document would duplicate it.
4. Any product code, test, or UXP change - this package is governance-artefact-only.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Every EBR-0001 status change in this package shall carry a disclosed rationale distinguishing defined-policy from implemented-code.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
python -m pytest
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors.
2. No unauthorised files changed - in particular, no `sentinel/` or other product code files.
3. `pytest` unaffected (governance-only change, no code touched) - run anyway to confirm no incidental breakage.

---

# 11. Risks and Dependencies

## Dependencies

None - self-contained governance changes.

## Risks

1. **The specific reweighting (Cost 10% to 15%, drawn from Latency and SDK/API Maturity) is a judgement call, not a derived fact.** Disclosed here for the Engineering Reviewer and Programme Sponsor to weigh rather than presented as objectively correct.
2. **Closing EBG-0049 as Complete could be read as claiming more than was delivered if the "policy defined, not implemented" distinction is lost.** Mitigated by Section 8's explicit exclusion and requiring the EBR-0001 closure note to state the distinction directly (Implementation Requirement 6).

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0045, EBG-0049, EBG-0024 (this package's parents), all closed by this package. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Revised (1.0 to 1.1) by this package - the identified authoritative home for cost/strategic-value criteria, not a new document. |
| [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] | Already states the cost/value principle at strategy level; this package concretises it in PEM-001, per ADR-0008's own Related Artefacts pointer to EBR-0001. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Already sequenced this cluster together and flagged the EBG-0070-driven live-relevance trigger. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Confirms production billed provider usage now exists (EBG-0070), the trigger condition for this package's timeliness. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: beb3c0117085d637c50d5237985d3fe7540f6d44`, 18 July 2026 20:14:17Z). All items applied: PEM-001 reweighted and revised (1.0 to 1.1) with the Cost and Strategic Value Principles and Cost-Aware Routing Policy sections, EBG-0045/EBG-0049/EBG-0024 closed Complete in EBR-0001 each preserving the policy-defined-versus-code-not-implemented distinction. Status promoted Draft to Approved-implemented. |
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Addressed a Medium finding from the Engineering Reviewer (Codex) on v0.1: Section 4.3 incorrectly stated `TrustTierPolicy` was unwired from production. Corrected against direct evidence - `build_default_runtime()` has wired `TrustTierPolicy` as the live runtime's policy engine since ESR-0024 WP1 (EBG-0074, Complete), directly asserted by `test_stdio_rpc.py`. The exclusion of dynamic cost-routing code (Section 8 item 1) is unchanged, but its rationale is now correctly framed around `TrustTierPolicy` being production-wired but cost-blind, not unwired. Section 5/7 wording touching this point also corrected. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0028 WP3. Investigated EBG-0045/EBG-0049/EBG-0024 against direct repository evidence: found PEM-001 already treats cost as a named but tied-lowest-weight criterion; found ESR-0016's trust-tier mechanism real but cost-blind and unwired from production; found zero existing cost logic anywhere in Sentinel provider code (genuinely greenfield for dynamic routing); found the institutional education credit lever unconfirmed, resting only on raw unprocessed chat content; found EBG-0024 genuinely overlapping and now-triggered by EBG-0070's live billed usage. Scoped to a policy-and-criteria revision of PEM-001 only, explicitly excluding any dynamic cost-aware routing code as premature without real cost data or a dedicated design review. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
