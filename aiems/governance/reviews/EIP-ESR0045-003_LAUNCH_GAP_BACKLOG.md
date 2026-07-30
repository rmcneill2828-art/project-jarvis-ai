# EIP-ESR0045-003 - Launch Gap Backlog

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0045-003 |
| Artefact ID | EIP-ESR0045-003 |
| Title | Launch Gap Backlog |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | Independent Codex `govreview`/`v1_0_gap_analysis` finding, recommendation 2 |
| Intended Session | ESR-0045 |
| Effective Date | 30 July 2026 |

---

# 2. Purpose

The same independent Codex governance/v1.0-readiness gap analysis that prompted [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] (ESR-0045 WP4) also recommended, as its second "recommended next action": "a prioritised launch-gap backlog split into must-ship vs defer." This package creates that artefact, LGB-0001.

---

# 3. Objective

Split RSC-0001's scored gaps (2 Fail, 1 Partial MLP 0.1 items, plus RSC-0001 Section 5's beyond-MLP-0.1 gaps) into Must-Ship (blocks the MLP 0.1/v1.0 launch itself) versus Defer (a later MLP phase or an enhancement beyond MLP 0.1's own bar), and register any genuinely untracked Must-Ship gap in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] so it is visible and governed, without authorising implementation.

---

# 4. Repository Context

Confirmed directly against the live [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] before drafting (not assumed):

| Gap | Existing Backlog Coverage Found |
|-----|-----------------------------------|
| User Identity / Profile Foundation | None. Searched for `identity`, `login`, `profile`, `authentic`, `household` across every EBG title - only EBG-0041 (Guardian's own identity architecture, not user identity), EBG-0076 (network/auth hardening, unrelated) and EBG-0095 (unrelated) matched. Theme 8's own narrative already says several items are "parked pending prerequisites (identity/authentication...)" without ever giving that prerequisite its own tracked item. |
| Basic Voice Input (Speech Input) | EBG-0112 (Voice/Vision Faculty) is marked `Complete (Increment A)` overall - its own text explicitly states Increment B (speech input) and Increment C (Vision) are deliberately not registered as separate items "since this entry already covers Phase 6 as a whole and a further split can be registered when one of those increments is actually selected as a future session's objective." That condition is now met for Increment B. |
| Guardian Orb Phases 2-4 | None found. |
| Family Profiles | None found as a standalone item; logically subsumed by the User Identity gap above. |
| Session/Shared-Family memory | None found; [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] specifies the architecture only. |
| Local Agent | EBG-0042 (Agent Framework Architecture, Candidate Backlog, High) and EBG-0021 (Local Agent Permission Boundary, Completed) exist. |
| Internet-assisted capability | EBG-0025 (Home Assistant and Smart Home Integration Assessment, Approved Backlog, Medium) partially overlaps; no broader item found. |
| Vision | Covered by EBG-0112's own Increment C text, same pattern as Increment B. |
| Expanded Guardian/HITL/network interface | EBG-0048 (Guardian HITL Governance Specification, Completed) and EBG-0076/ADR-0020 (Completed) are specifications only; no implementation item found. |

---

# 5. Scope

This package authorises:

1. Creating `aiems/governance/baselines/LGB-0001_LAUNCH_GAP_BACKLOG.md` (already drafted in full, subject to this review).
2. Registering exactly two new [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] entries, both Candidate Backlog (no implementation authorised):
   - **EBG-0116** - User Identity and Profile Foundation.
   - **EBG-0117** - Voice Faculty Increment B: Speech Input.
3. REG-0001 registration for LGB-0001 and this EIP.

It does **not** authorise registering a new EBG for every other Defer-bucket gap identified - those remain either subsumed by an existing item, covered by an existing item's own deferred-increment text, or explicitly left for a future dedicated backlog-curation pass (matching the Theme 7 precedent, ESR-0033 WP2), to keep this package's scope to the genuine launch-blockers only. It does not prioritise, schedule or approve implementation of EBG-0116 or EBG-0117 beyond registering them as Candidate Backlog - a future Engineering Implementation Package would still need to be drafted, reviewed and approved for either.

No `jarvis/`, `sentinel/`, `src/`, `src-tauri/` or `scripts/` file is touched.

---

# 6. Risks and Considerations

- **Scope discipline risk**: the temptation to register every named gap as its own EBG was deliberately resisted - only the two genuine MLP 0.1 launch-blockers are registered, per PBK-0001's Engineering Scope Control and the Flag Scope Creep discipline.
- **Priority-inflation risk**: both new items are registered High priority because MLP 0.1 explicitly requires them, not because of any independent urgency judgement - this is disclosed in each entry's own text.
- **Staleness risk**: like RSC-0001, this backlog will go stale as items are delivered or re-scoped; an explicit Maintenance section directs refresh triggers.

---

# 7. Approval

Programme Sponsor approval required before LGB-0001 is created and before EBG-0116/EBG-0117 are registered, verified via `submit-response` against the real Sponsor Approval Service - chat approval alone is not sufficient.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 30 July 2026**, verified via `submit-response` against the real Sponsor Approval Service. LGB-0001 created and EBG-0116/EBG-0117 registered as scoped. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Fix round after Engineering Reviewer (Codex) design review - v0.1: Fail with one finding (EBG-0042 misstated as "Approved Backlog" when it is "Candidate Backlog" in EBR-0001). Corrected in both LGB-0001 and this package. Resubmitted - **Pass**. |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, submitted for Engineering Reviewer (Codex) design review. |
