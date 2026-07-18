# EIP-ESR0028-002 - JARVIS Product Requirements Backlog Identification

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0028-002 |
| Artefact ID | EIP-ESR0028-002 |
| Title | JARVIS Product Requirements Backlog Identification |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0017) |
| Intended Session | ESR-0028 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Close EBG-0017 ("Create or identify the authoritative product requirements backlog for recovered JARVIS capability intent, avoiding raw transcript import and duplicate product documentation") by direct repository investigation, following the same evidence-first discipline as ESR-0028 WP1.

---

# 3. Related Backlog Item

EBG-0017 (`aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md:86`): "JARVIS Product Requirements and Capability Backlog | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Create or identify the authoritative product requirements backlog for recovered JARVIS capability intent, avoiding raw transcript import and duplicate product documentation."

---

# 4. Repository Context and Investigation Findings

## 4.1 What EIP-EKR-0001 actually was

The cited source is not a registered controlled artefact - no REG-0001 row, no standalone file. It exists only inside the ESR-0004 transcript (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`) as a Codex execution package, "Engineering Knowledge Promotion & Repository Consolidation." Its objective was knowledge consolidation, not building a requirements backlog, and it carried an explicit constraint: "DO NOT: Create documentation for completeness. Duplicate information. Rewrite history. Create overlapping artefacts." Its concrete output was `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md`, README updates, and the addition of EBG-0017 (through EBG-0025) to EBR-0001 as future candidate work. EIP-EKR-0001 is the origin event that *created* EBG-0017 - it did not itself satisfy it.

## 4.2 Candidate artefacts already in the repository

Four existing documents were checked against "authoritative product requirements backlog for recovered JARVIS capability intent":

- **`jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md`** (v1.3) - the actual recovered product intent document. Contains Vision, Product Objectives, Design Principles, the Minimum Lovable Product definition, a full Product Roadmap table (MLP 0.1 through Version 1.0, each phase naming its specific capabilities), a Capability Hierarchy, and per-service purpose/responsibilities/future-expansion sections. This is the requirements content EBG-0017 is asking to locate.
- **`jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`** (v2.0, refreshed ESR-0021 WP7) - tracks each capability named in the Product Architecture's roadmap against Vision/Architecture/Implementation/Testing maturity and an Overall Readiness column. This is the tracking half of a requirements backlog: not what to build, but how far each already-defined requirement has progressed.
- **`aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`** (v2.1, Accepted, registered REG-0001:139) - explicitly disclaims this role in its own text: "does not replace the repository assessment, product architecture, capability readiness matrix or engineering backlog" and "does not select, approve or reprioritise backlog items." It records what is currently accepted as operational, not product intent or forward requirements.
- **`aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md`** - sequences existing backlog items; does not define requirements. Its own EBG-0017 entry (line 133) already concludes: "the programme has functioned without it for 20+ sessions by using EBR-0001 and PST-0001 together - not urgent, but overdue."

No fifth, undiscovered document exists. No raw-transcript-derived product requirements document exists anywhere in the repository - `git grep` for "raw transcript" outside EBG-0017's own line returns only two unrelated FCH-0003 passages about a different (behavioural-knowledge) topic.

## 4.3 Finding: JARVIS_PRODUCT_ARCHITECTURE.md and JARVIS_CAPABILITY_READINESS_MATRIX.md together already are the authoritative product requirements backlog

Between them, these two documents already provide exactly what EBG-0017 asks for: recovered capability intent (Product Architecture's roadmap, capability hierarchy and per-service definitions) paired with live tracking of how far each has progressed (the Readiness Matrix). Creating a new, separate "product requirements backlog" artefact would directly violate EBG-0017's own explicit caution against "duplicate product documentation" - it would restate the same roadmap and capability list a third time. The correct disposition is **identify**, not **create**, which the backlog item's own wording ("Create or identify") already anticipates as a valid outcome.

## 4.4 Registration gap found

Neither document is currently registered as a controlled artefact in REG-0001. PCB-0001's REG-0001 row (line 139) references `JARVIS_PRODUCT_ARCHITECTURE` only as its **Parent** column value - the Product Architecture document itself has no row. The Readiness Matrix's own Refresh History (v2.0, ESR-0021 WP7) already flags this directly for the Matrix: "this document has never been registered in REG-0001 as a controlled artefact (no artefact ID, unlike its sibling PCB-0001) - flagged for a separate Programme Sponsor decision on whether to register it formally." An "authoritative" backlog that isn't itself a registered, governed artefact is a weaker claim than the same documents once they are registered - this closes both the EBG-0017 disposition and the Matrix's own disclosed gap in the same package.

## 4.5 Currency check

Read `PST-0001_PROGRAMME_STATUS.md` Section 5 (Current Capability Roadmap) directly against the Readiness Matrix's per-row claims to confirm the Matrix is still accurate before treating it as authoritative:

- **Memory row**: Matrix shows "Not Started" across Implementation/Testing (v2.0, refreshed 15 July 2026, ESR-0021). `jarvis/memory/` (`store.py`, `service.py`) exists with a working `PersonalMemoryStore`/`PersonalMemoryService`, wired into `GuardianRuntime` and `stdio_rpc.py`, delivered at **ESR-0027 WP1** (16-18 July 2026) - after the Matrix's own refresh. The row is stale by one implemented capability.
- **Provider Architecture row**: Matrix shows "Implemented (live-validated, unwired from production runtime)". PST-0001:140 confirms EBG-0070 (Complete, ESR-0022 WP1, per EIP-ESR0022-001 v1.0) wired a live provider into the default runtime conversation path the day after the Matrix's refresh. The row's "unwired" qualifier is now factually wrong.

No other row was found stale on inspection against PST-0001 Section 5 - Guardian, Sentinel, Platform Services, UXP, Voice, Vision, Home Automation, Productivity, Engineering Agent, Knowledge and Multi-device all still match PST-0001's current descriptions.

## 4.6 Findings from Engineering Reviewer (Codex) pre-implementation review of v0.1

**Finding 1 (Medium)**: v0.1 scoped the Matrix update to the two rows only, but Section 3 ("Overall Programme Capability Summary") prose directly contradicts the row fixes if left untouched - it states "Provider Architecture has two live-validated adapters, though neither is wired into a default/production runtime route yet" (line 56) and lists Memory among capabilities that "remain not implemented" (line 58) and "still ahead" (line 60). Related Artefacts (line 70) also still cites `RBL-0014` as the "Current accepted repository baseline" - stale since RBL-0015 was accepted at ESR-0022 (the same reference PBK-0001 corrected at ESR-0028 WP1). All three now expanded into scope alongside the row changes, so the refreshed document is internally consistent rather than contradicting itself between Sections 2 and 3.

**Finding 2 (Medium)**: v0.1 proposed registering `JARVIS_PRODUCT_ARCHITECTURE.md` in REG-0001 under the ID `JARVIS_PRODUCT_ARCHITECTURE` (matching its WikiLink target, used consistently elsewhere - PST-0001:138, the Matrix's own Related Artefacts, PCB-0001's Parent column), but the document's own Document Control table (line 9) reads "Document ID | JARVIS-PRODUCT-ARCHITECTURE" (hyphenated, and using the field label "Document ID" rather than "Artefact ID" used by every other REG-0001-registered artefact's internal Document Control). Registering the underscore WikiLink form while leaving the document's own internal identity hyphenated and differently-labelled would create exactly the kind of controlled-identity mismatch REG-0001's own governance rules exist to prevent. Resolved by authorising a minimal, identity-only Document Control edit in `JARVIS_PRODUCT_ARCHITECTURE.md` itself: relabel "Document ID" to "Artefact ID" and correct its value to `JARVIS_PRODUCT_ARCHITECTURE`, matching the form already used everywhere the document is referenced. No other content in the document changes - Section 4.5 already confirmed the rest of the document is still accurate.

---

# 5. Scope

This package authorises a future implementation to:

1. Register `JARVIS_PRODUCT_ARCHITECTURE` and `JARVIS_CAPABILITY_READINESS_MATRIX` as controlled artefacts in REG-0001, using their existing WikiLink-referenced filenames as Artefact ID (matching how they are already referenced throughout the repository, e.g. PST-0001:138, PCB-0001:139's Parent column), Status taken from each document's own internal Document Control field (`Approved Product Architecture` / `Maintained`), Owner `Programme Sponsor & Chief Engineering Advisor`, Parent `EBG-0017`, location `jarvis/architecture/`.
2. In `JARVIS_PRODUCT_ARCHITECTURE.md`: relabel Document Control's "Document ID" field to "Artefact ID" and correct its value from `JARVIS-PRODUCT-ARCHITECTURE` to `JARVIS_PRODUCT_ARCHITECTURE`, resolving Section 4.6 Finding 2. No other content changes.
3. Correct `JARVIS_CAPABILITY_READINESS_MATRIX.md`'s Memory row (Implementation/Testing/Overall Readiness) to reflect the ESR-0027 WP1 Personal Memory foundation, and its Provider Architecture row to remove the now-incorrect "unwired from production runtime" qualifier, replacing it with a reference to EBG-0070's production wiring. Update Section 3's narrative (the Provider Architecture bullet, and the Memory mentions in the "remain not implemented" and "still ahead" lists) so it no longer contradicts the corrected rows, per Section 4.6 Finding 1. Correct Related Artefacts' `RBL-0014` reference to `RBL-0015`. Add a new Refresh History entry (v2.1) disclosing all of the above and this registration.
4. Close EBG-0017 in EBR-0001 as `Complete`, with the Section 4.3/4.4 rationale recorded: identified (not created) as the disposition, both documents now registered, the Matrix's own previously-disclosed registration gap closed in the same package, two concrete staleness corrections applied (rows and narrative), the JARVIS_PRODUCT_ARCHITECTURE.md identity-field alignment noted.

---

# 6. Authorised Files

1. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
3. `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`
4. `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md` (Document Control identity field only - see Implementation Requirements item 6 below)

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. REG-0001 rows use the existing table's eight-column format, matching the Model/Baseline row precedent (e.g. PCB-0001, MOD-0001).
2. Readiness Matrix Memory row: Implementation changes from "Not Started" to a description naming the ESR-0027 WP1 foundation (`PersonalMemoryStore`/`PersonalMemoryService`, consent-gated, wired into `GuardianRuntime`); Testing changes from "Not Started" to reflect the delivered unit test coverage (`test_memory_store.py`, `test_memory_service.py`); Overall Readiness changes from "Planned" to "Implemented (Foundation)", consistent with the Overall Readiness language already used for Guardian/Sentinel/Platform Services/UXP.
3. Readiness Matrix Provider Architecture row: Implementation cell changes from "Implemented (live-validated, unwired from production runtime)" to "Implemented (live-validated, wired into production runtime per EBG-0070)".
4. Readiness Matrix Section 3 narrative: the Provider Architecture bullet (line 56) drops "though neither is wired into a default/production runtime route yet" in favour of language matching the corrected row (production-wired per EBG-0070); the "remain not implemented" list (line 58) and the "still ahead" list (line 60) both drop "Memory" (formerly implying Session/Shared-Family memory too - the corrected wording should name only the delivered Personal Memory foundation, not imply Session or Shared Family memory now exist, per the Engineering Reviewer's advisory).
5. Readiness Matrix Related Artefacts: `RBL-0014` reference (line 70) corrected to `RBL-0015`, matching the same fix already applied to PBK-0001 at ESR-0028 WP1.
6. `JARVIS_PRODUCT_ARCHITECTURE.md` Document Control: relabel "Document ID" to "Artefact ID" and correct its value from `JARVIS-PRODUCT-ARCHITECTURE` to `JARVIS_PRODUCT_ARCHITECTURE`. No other field or content in the document changes.
7. All Matrix changes (rows, narrative, Related Artefacts) are recorded together in a single new Refresh History entry (v2.0 to v2.1).
8. EBG-0017 closure in EBR-0001 discloses the full disposition: identify-not-create rationale, both artefacts registered, Matrix row/narrative/reference corrections, the JARVIS_PRODUCT_ARCHITECTURE.md identity-field alignment, and explicitly notes this also closes the Matrix's own previously-disclosed registration gap from its v2.0 Refresh History entry.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Creating any new product requirements document - Section 4.3 found this would violate EBG-0017's own anti-duplication caution.
2. Any change to `JARVIS_PRODUCT_ARCHITECTURE.md`'s substantive content, vision, roadmap or capability definitions - Section 4.5 found these still accurate; only the Document Control identity field (Implementation Requirements item 6) is corrected.
3. A full re-audit of every Readiness Matrix row and every narrative sentence beyond the two rows (and their directly-dependent Section 3/Related Artefacts references) Section 4.5/4.6 found concretely stale against direct PST-0001 evidence.
4. Any product code, test, or UXP change - this package is governance-artefact-only.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Every EBR-0001 status change in this package shall carry a disclosed rationale in the item's own note.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
python -m pytest
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors.
2. No unauthorised files changed.
3. `pytest` unaffected (governance-only change, no code touched) - run anyway to confirm no incidental breakage.

---

# 11. Risks and Dependencies

## Dependencies

None - self-contained governance changes.

## Risks

1. **Registering a long-lived, informally-maintained document retroactively could be read as implying past non-compliance.** Mitigated by framing the registration as closing a disclosed, known gap (the Matrix's own v2.0 Refresh History already named it) rather than a correction of prior wrongdoing.
2. **The Memory/Provider Architecture row corrections are judgement calls about wording, not just fact.** The underlying facts (code exists, tests pass, EBG-0070 wired a route) are directly verified; the specific Overall Readiness label chosen ("Implemented (Foundation)") is a judgement call by analogy to Guardian/Sentinel's existing labels, disclosed here for the Engineering Reviewer and Programme Sponsor to weigh.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0017 (this package's parent), closed by this package. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Identified as (one half of) the authoritative product requirements backlog; registered and identity-aligned only (Document Control ID field) by this package - no substantive content change. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Identified as (the other half of) the authoritative product requirements backlog; registered and refreshed (v2.0 to v2.1) by this package. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Sibling document, already registered; explicitly disclaims the product-requirements-backlog role in its own text (Section 4.2). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Already names EBG-0017 as "overdue" and identifies EBR-0001/PST-0001 as the current de facto stand-in. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Section 5 used as the direct evidence source for the Section 4.5 currency check. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: 568aa584237693fb02d462b1c24fe16833ef814b`, 18 July 2026 19:50:48Z). All items applied: both artefacts registered in REG-0001, JARVIS_PRODUCT_ARCHITECTURE.md's Document Control identity field corrected, JARVIS_CAPABILITY_READINESS_MATRIX.md refreshed to v2.1 (Memory/Provider Architecture rows, Section 3 narrative, RBL-0014 to RBL-0015), EBG-0017 closed Complete in EBR-0001. Status promoted Draft to Approved-implemented. |
| 0.4 | 18 July 2026 | Claude Engineering Implementer | Addressed a residual Low/editorial Engineering Reviewer finding on v0.3: the v0.3 fix for REG-0001's own changelog wording had itself re-introduced the same class of avoidable validator warning by quoting two raw heading-number phrases in that changelog entry's description of the fix. Reworded the REG-0001 entry a second time to describe the changes without quoting any heading-number phrase at all. Ready for Programme Sponsor approval. |
| 0.3 | 18 July 2026 | Claude Engineering Implementer | Addressed two Low/editorial Engineering Reviewer (Codex) findings on v0.2. Finding 1: Section 13's JARVIS_PRODUCT_ARCHITECTURE relationship note said "registered but not edited by this package", contradicting the identity-only edit v0.2 itself authorised - corrected to "registered and identity-aligned only". Finding 2: REG-0001's own v3.213 version-history entry used the literal phrase "Section 3 narrative", producing an avoidable validate_repository.py warning (REG-0001 has no "Section 3" heading) - reworded to "Overall Programme Capability Summary narrative". Ready for Programme Sponsor approval. |
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Addressed Engineering Reviewer (Codex) findings on v0.1, returned via the bridge. Finding 1 (Medium, Matrix internal contradiction) - expanded scope to also update Section 3's narrative (Provider Architecture bullet, Memory mentions) and the stale RBL-0014 Related Artefacts reference, so the refreshed rows don't contradict the surrounding prose. Finding 2 (Medium, REG-0001 identity mismatch) - added a minimal, identity-only Document Control edit to `JARVIS_PRODUCT_ARCHITECTURE.md` itself (Document ID to Artefact ID, hyphenated to underscore form) so the registered REG-0001 ID matches the document's own internal identity rather than only its external WikiLink usage. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0028 WP2. Investigated EBG-0017 against direct repository evidence: identified `JARVIS_PRODUCT_ARCHITECTURE.md` and `JARVIS_CAPABILITY_READINESS_MATRIX.md` together as the already-existing authoritative product requirements backlog (identify, not create, per the item's own wording and its anti-duplication caution); found neither document registered in REG-0001, including a gap the Matrix's own v2.0 Refresh History already disclosed; found two concrete Matrix rows (Memory, Provider Architecture) stale against direct PST-0001 Section 5 evidence. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
