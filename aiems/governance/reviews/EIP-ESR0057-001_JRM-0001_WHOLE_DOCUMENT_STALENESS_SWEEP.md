# EIP-ESR0057-001 - JRM-0001 Whole-Document Staleness Sweep

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0057-001 |
| Title | Engineering Implementation Package: WP1 JRM-0001 Whole-Document Staleness Sweep |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0057 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0057 WP1. During WP0A session-open review, two rows in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Section 6.1 (EBG-0005, EBG-0068) were spotted still describing items as open Near-term work despite [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] showing both closed (Resolved by Attrition, Superseded respectively) since ESR-0028 WP1.

Per PBK-0001's Documentation Debt Discipline ("Whole-Document Staleness Sweep on Edit" - whenever a controlled artefact is opened to fix a specific stale claim, the entire document shall be swept for other stale current-state claims before the edit is considered complete), every `EBG-####` reference in JRM-0001 was cross-checked directly against EBR-0001's authoritative Status column rather than fixing only the two originally-spotted rows.

**Finding: 19 EBG references across four sections (6.1, 6.2, 6.3, 7.5) describe items as open, Candidate Backlog, or "left for a future session" that EBR-0001 shows already Complete, Superseded, or Resolved by Attrition** - the large majority closed in a single batch at ESR-0033 WP2 (Codex-led Theme 7 independent triage) that was never reflected back into this roadmap's own rows. Two of the nineteen are materially more significant than a missing annotation: EBG-0042 (Agent Framework Architecture) and EBG-0047 (Sentinel Gate of Durin Architecture Specification) are still described in Section 7.5 as open Candidate Backlog items "not confidently ready"/"not confidently satisfied," despite both having been resolved with real delivered architecture work (ESR-0048 WP2 and ESR-0050 WP3 respectively) that the rest of the repository (PST-0001, README) already correctly reflects as complete.

---

# 3. Repository Context Investigated

* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] v1.26 (full document read) - every `EBG-####` reference extracted from Sections 6.1, 6.2, 6.3, 7.3, 7.4, 7.5, 7.6, 8.1-8.4 and Section 9.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - each extracted ID's row (Status column plus resolution detail) pulled directly and compared against JRM-0001's own rationale text for the same ID.
* Cross-check method: a row was judged stale only where EBR-0001 shows a closed disposition (Complete/Completed/Superseded/Resolved by Attrition) that JRM-0001's own rationale text does not mention at all - not where JRM-0001 already carries a resolution annotation (many rows, e.g. EBG-0058, EBG-0057, EBG-0065, EBG-0018, EBG-0060, EBG-0067, already correctly annotated and left unchanged), and not where EBR-0001 itself still shows the item genuinely open (e.g. EBG-0008, EBG-0011, EBG-0040, EBG-0059, EBG-0061, EBG-0066 - all still Approved/Candidate Backlog, left unchanged).

---

# 4. Scope

## 4A. Section 6.1 (Near-term) - 2 rows

* EBG-0005 - annotate Resolved by Attrition, ESR-0028 WP1 (EIP-ESR0028-001 Section 4.1).
* EBG-0068 - annotate Closed Superseded, ESR-0028 WP1 (EIP-ESR0028-001 Section 4.2).

## 4B. Section 6.2 (Mid-term) - 3 rows

* EBG-0009, EBG-0010, EBG-0013 - annotate Closed Complete, ESR-0033 WP2 (Codex-led Theme 7 independent triage), each with its own brief resolution detail.

## 4C. Section 6.3 (Longer-term / Not Yet Justified) - 9 rows across 7 table rows

* EBG-0014 - annotate Closed Complete, ESR-0033 WP2 (paired with EBG-0010).
* EBG-0032 - annotate Closed Complete, ESR-0033 WP2.
* EBG-0033 - annotate Closed Complete, ESR-0033 WP2.
* EBG-0034/0035/0036/0037 (one combined row) - annotate: 0034/0035/0036 Closed Complete, 0037 Closed Superseded, all ESR-0033 WP2.
* EBG-0038 - annotate Closed Complete, ESR-0054 WP1 (relevance check, no new standard warranted).
* EBG-0040/0043/0044 (one combined row) - annotate: 0043/0044 Closed Complete at ESR-0033 WP2; 0040 remains genuinely open (Approved Backlog), explicitly distinguished within the same row.
* EBG-0062 - annotate Closed Superseded, ESR-0033 WP2.
* EBG-0064 - annotate Closed Complete, ESR-0033 WP2.

## 4D. Section 7.5 (Parallel - Track B) - 2 rows

* EBG-0042 - annotate Resolved, ESR-0048 WP2 (EIP-ESR0048-001, MOD-0001 Agent Framework subsection, subsequently built as real code ESR-0049/ESR-0050).
* EBG-0047 - annotate Resolved, ESR-0050 WP3 (EIP-ESR0050-002, CURRENT_ARCHITECTURE.md registered, Gate of Durin subsection).

## 4E. Version History

* New v1.27 row summarising the sweep and its scale.

## 4F. Explicitly out of scope

* No row is deleted - every correction is an additive annotation, matching the pattern already established throughout this document (e.g. EBG-0058, EBG-0057).
* No EBR-0001 edit - EBR-0001's own Status column is already accurate for every ID checked; only JRM-0001 is stale. PBK-0001's Repository Engineering Health Review Guidance reserves EBR-0001 edits for a Programme Sponsor-directed backlog review, not this Work Package.
* No re-sequencing of items between horizon buckets (e.g. moving now-closed rows out of Section 6.3 into a "Closed" section) - out of scope for a staleness-annotation fix; a future roadmap refresh (as JRM-0001 v1.18/v1.34 have each done previously) is the right vehicle for structural re-bucketing.
* EBG-0011, EBG-0040, EBG-0059, EBG-0061, EBG-0066 and all Track B/C rows not named in Section 4A-4D above were checked and found not stale (EBR-0001 status matches JRM-0001's description) - no change.

---

# 5. Validation Requirements

* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* Manual cross-check: every corrected row's cited EBR-0001 status and resolution session/WP re-verified against the live EBR-0001 text immediately before implementation, not only at drafting time.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* All 19 identified EBG references in JRM-0001 carry a resolution annotation consistent with EBR-0001's actual current Status.
* No row's rationale text is deleted; every correction is additive.
* `validate_repository.py` remains clean.
* No EBR-0001, REG-0001 backlog-status, or other controlled-artefact content changed beyond JRM-0001 itself and this Work Package's own registration entries.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 14 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved as drafted")**, reviewing directly in place of Codex given the disclosed account outage. Implemented exactly as drafted at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 14 September 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review could not be obtained: `codex exec` invoked twice via the AIEMS Exchange Bridge submission (09:26 and 09:34 UTC), both attempts failing identically before any review content was produced - `HTTP 402 Payment Required`, `auth error code: deactivated_workspace`, on every `chatgpt.com/backend-api/codex/*` call, despite `codex login status` reporting a valid login. No `return-findings` call occurred either time (confirmed: `.aiems-exchange/transcript/ESR-0057-WP1.md` carries no findings entry). Reported plainly to the Programme Sponsor rather than treated as a Pass by default. The Programme Sponsor confirmed the account issue may take time to resolve and elected to review this Work Package directly in place of Codex for this session - a disclosed deviation from the standing draft-Codex-review-approval-implement-commit-post-commit-review template, made necessary by a genuine external service outage rather than by choice. |
| 0.1 | 14 September 2026 | Claude Engineering Implementer | ESR-0057 WP1 draft. Whole-document staleness sweep of JRM-0001: 19 EBG references across Sections 6.1/6.2/6.3/7.5 found describing closed items as open. Drafted directly against the working-tree copy of JRM-0001 (disclosed process note: the Programme Sponsor's "Please start on WP1" was read as covering this drafting step, matching the disclosed precedent at ESR-0056 WP4; the real `submit-response`/Sponsor Approval Service gate still governs the actual commit). Not yet reviewed, approved or implemented/committed. |
