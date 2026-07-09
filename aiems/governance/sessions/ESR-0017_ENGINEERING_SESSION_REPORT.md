# ESR-0017 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0017 |
| Title | Engineering Session Report |
| Version | 0.3 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Session | ESR-0017 |
| Date Opened | 9 July 2026 |
| Date Closed | - |
| Closure Status | Open |
| Final Validation | Pending |

---

# 2. Purpose

This report records the opening, execution and closure of ESR-0017.

ESR-0017 is the third Engineering Session run under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial, and is separately designated the **Cold Start Validation Session** (EE-0001 Section 3.4): Claude as Engineering Lead, ChatGPT as Independent Reviewer, Programme Sponsor gating every step, session begun in a fresh conversation using only README.md, PST-0001, the Current ESR (ESR-0016) and repository artefacts referenced from those, per GDE-0001 knowledge tiering.

---

# 3. Scope

ESR-0017 addresses four Programme-Sponsor-approved Work Packages, arrived at through a backlog review against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and direct inspection of current repository state:

1. **WP1** - UXP&harr;Backend Integration Architecture Decision (design only; new ADR).
2. **WP2** - Connect Guardian Runtime through Sentinel.
3. **WP3** - Gemini provider adapter (second PEM-001 external provider).
4. **WP4** - Five-session backlog progression roadmap (ESR-0017 through ESR-0021).

WP1 was added after the Programme Sponsor raised, mid-session, that the Guardian UXP (`src/`, `src-tauri/`) remains a static Tauri/React mock-up with no backend connection - a gap not previously captured as its own backlog item and not addressed by WP2/WP3's backend-only scope.

---

# 4. Engineering Authority

ESR-0017 opening was authorised by Programme Sponsor approval of WP0B on 9 July 2026, following WP0A Repository Synchronisation confirming ESR-0016 and its post-closure addendum ([[ESR-0016A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0016A]]) were both formally closed and [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] retained as the current repository baseline.

The four-WP scope (WP1-WP4) was proposed by the Engineering Lead following a repository-grounded backlog review, and explicitly approved by the Programme Sponsor, including the Engineering Lead's own flag that a 4-WP session exceeds the originally-scoped 2-WP proposal.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Decide the UXP-to-backend integration pattern (WP1); connect the existing Guardian Runtime and Sentinel subsystems, which are implemented but currently unwired to each other (WP2); extend Sentinel's provider roster with the PEM-001-approved Secondary provider (WP3); and produce a five-session backlog progression roadmap so future session sequencing is evidence-led rather than ad hoc (WP4).

**Outcome: in progress.**

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation | Complete |
| WP1 | UXP&harr;Backend Integration Architecture Decision - evaluate Tauri sidecar, local HTTP/WebSocket server, PyO3 embedding and Rust/Node port options; record decision as a new ADR; register a new EBR-0001 candidate backlog item | Complete and Reviewed - [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] v1.1; ChatGPT Engineering Reviewer: 0 Blocking, 0 Major, 1 Minor (accepted, fixed); see [[ESR-0017_WP1_ENGINEERING_REVIEW_PACKAGE|WP1 Review Package]] Section 11 |
| WP2 | Connect Guardian Runtime through Sentinel - wire `GuardianRuntime`'s `Guardian Provider Boundary` service to `SentinelGatedConversationProvider` (or equivalent), with tests | Complete and Reviewed - 8 new tests, 152/152 passing; ChatGPT Engineering Reviewer: 0 Blocking, 0 Major, 2 Minor Observations (both deferred to EBG-0050); see [[ESR-0017_WP2_ENGINEERING_REVIEW_PACKAGE|WP2 Review Package]] Section 10 |
| WP3 | Gemini provider adapter - implement `GeminiProvider` mirroring `sentinel/openai_provider.py`'s shape, export from `sentinel/__init__.py`, with tests | Complete and Reviewed - 11 new tests, 163/163 passing; ChatGPT Engineering Reviewer: 0 Blocking, 0 Major, 3 Minor Observations (all deferred to new EBG-0051); see [[ESR-0017_WP3_ENGINEERING_REVIEW_PACKAGE|WP3 Review Package]] Section 10 |
| WP4 | Five-session backlog progression roadmap (ESR-0017-ESR-0021) against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Complete and Reviewed - ChatGPT Engineering Reviewer: 0 Blocking, 0 Major, 4 Minor Observations (all accepted and incorporated); see [[ESR-0017_WP4_ENGINEERING_REVIEW_PACKAGE|WP4 Review Package]] Section 15 |

---

# 7. Architectural Milestones

- First architecture decision governing how the approved UXP (Tauri + React) is meant to reach the Python backend (`jarvis/`, `sentinel/`) - none existed before ADR-0019.
- First working connection between `GuardianRuntime` and Sentinel - `CURRENT_ARCHITECTURE.md` roadmap item 6 ("Connect Guardian through Sentinel") implemented for the first time, proven against real `SentinelTrustGateway`/`ProviderOrchestrator` components, not just a stub.
- Second external Sentinel provider adapter (`GeminiProvider`, after `OpenAIProvider` in ESR-0015) - first real exercise of Sentinel's provider-independence claim (PEM-001, ADR-0008) with more than one concrete adapter to be independent *between*.
- First explicit five-session backlog progression roadmap produced mid-session at Programme Sponsor request, rather than only at session closure as PBK-0001's default Repository Engineering Health Review timing would otherwise imply.

---

# 8. Executive Summary

ESR-0017 opened as a two-WP proposal (Guardian&harr;Sentinel connection, Gemini adapter) following backlog review against EBR-0001 and direct repository inspection. The Programme Sponsor raised, mid-session, that the Guardian UXP remains a disconnected static mock-up - a gap the original two-WP proposal did not address - and the Lead added WP1 (UXP&harr;Backend Integration Architecture Decision) in response, expanding the session to four WPs with explicit Programme Sponsor approval and an explicit Lead flag that this exceeded the original scope.

WP1-WP3 were then implemented back-to-back, including starting WP3, before any Engineering Reviewer had seen WP1 or WP2 - a process deviation from EE-0001's per-step Lead/Reviewer gating, caught and corrected by the Programme Sponsor mid-session. From that point on, each Work Package was completed, self-reviewed, packaged into a self-contained review document and paused for independent ChatGPT review before the next began. All four Work Packages (WP1-WP4) were reviewed this way: 0 Blocking and 0 Major findings across all four, 10 Minor/Observation-severity findings total, all accepted. Findings were either fixed immediately (WP1's ADR wording) or deliberately deferred into new, explicitly-scoped backlog items (EBG-0050, EBG-0051) or incorporated directly into the WP4 roadmap document itself (WP4's four observations).

163 tests pass (144 at session start, +19 new: 8 for Guardian&harr;Sentinel, 11 for Gemini), zero regressions. Repository validation is clean except one pre-existing, out-of-scope validator defect discovered incidentally (Section 10) and a documented class of adjacency-heuristic false positives already accepted by the Programme Sponsor in ESR-0016A.

**Outcome: WP1-WP4 content complete and reviewed. Repository staging, commit and push are pending explicit Programme Sponsor authorisation (not yet given). WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance remain outstanding, as does formal session closure.**

---

# 9. Engineering Outcomes

1. Created [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] (v1.1 after Reviewer-driven wording revision): Tauri sidecar-managed Python process, duplex stdio JSON-RPC, over local HTTP/WebSocket, PyO3 embedding and a Rust/Node rewrite.
2. Added `conversation_provider` to `GuardianRuntime` (optional, default `None`, zero regressions to the 16 pre-existing Guardian runtime tests), a new `converse()` method, and provider-boundary lifecycle wiring mirroring the existing `Guardian Runtime` service's own start/stop pattern. 8 new tests, including one exercising real `SentinelTrustGateway` + `ProviderOrchestrator` components.
3. Implemented `sentinel/gemini_provider.py`'s `GeminiProvider`, mirroring `OpenAIProvider`'s shape and conservative error-handling conventions, adapted to Gemini's actual `generateContent` request/response shape. Exported from `sentinel/__init__.py`. 11 new tests. Not wired into any production route.
4. Registered four new candidate backlog items: EBG-0050 (UXP-Backend Bridge Implementation), EBG-0051 (Gemini Provider Production Readiness), and EBG-0052 (PBK-0001/EE-0001 "Execute After Approval" Principle, a Programme-Sponsor-reported EE-0001 trial finding).
5. Produced a five-session backlog progression roadmap (WP4) against EBR-0001, including a Reviewer-added decision gate (Section 6.1 of the WP4 review package) and worked contingency example.
6. Recorded a draft EE-0001 Lead self-assessment for ESR-0017 in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9, including the first empirical verification of the Cold Start Validation Session's documentation-only handoff claim (Section 5.4: **✓**), and two Programme-Sponsor-directed findings (one positive, one improvement) about the trial itself.
7. Self-caught and fixed one defect before it reached the Reviewer: a WikiLink backslash-escaping error introduced while editing this session report, caught by the Lead's own `validate_repository.py` run.
8. Discovered, and explicitly did not fix (out of WP1-4 scope), two pre-existing repository defects: `scripts/validate_repository.py`'s `check_stale_status_references` fires an ERROR the moment any new (correctly Open, not yet closed) session file exists, since it doesn't check the file's `Status` field; and ADR-0018 is missing from REG-0001's own artefact table despite REG-0002's changelog claiming otherwise.

---

# 10. Validation Summary

| Checkpoint | Tests | Result |
|---|---:|---|
| Session start (ESR-0016A closed baseline) | 144 | 144 passing |
| After WP2 (Guardian&harr;Sentinel, 8 new tests) | 152 | 152 passing |
| After WP3 (Gemini adapter, 11 new tests) | 163 | 163 passing |
| Current (after WP4 and EE-0001/EBR-0001 documentation updates) | 163 | **163 passing, zero regressions** |

`python scripts/validate_repository.py`: 1 error (pre-existing, out-of-scope - see Engineering Outcomes item 8), warnings limited to the documented adjacency-heuristic false-positive class already accepted in ESR-0016A WP3, plus this session's own instances of the same class (session/review-package files referencing EE-0001/ESR-0016 section numbers without an adjacent WikiLink). No warning or error was newly introduced by WP1-WP4's substantive content.

No live external API call was made against either OpenAI or Google's real endpoints this session - all Sentinel provider tests use transport injection (fake/stub transports).

---

# 11. Repository Deliverables

**New files:**
- `aiems/governance/decisions/ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE.md`
- `sentinel/gemini_provider.py`
- `jarvis/tests/test_gemini_provider.py`
- `aiems/governance/reviews/ESR-0017_WP1_ENGINEERING_REVIEW_PACKAGE.md`
- `aiems/governance/reviews/ESR-0017_WP2_ENGINEERING_REVIEW_PACKAGE.md`
- `aiems/governance/reviews/ESR-0017_WP3_ENGINEERING_REVIEW_PACKAGE.md`
- `aiems/governance/reviews/ESR-0017_WP4_ENGINEERING_REVIEW_PACKAGE.md`
- `aiems/governance/sessions/ESR-0017_ENGINEERING_SESSION_REPORT.md` (this report)

**Modified files:**
- `jarvis/guardian/runtime.py`, `jarvis/tests/test_guardian_runtime.py` (WP2)
- `sentinel/__init__.py` (WP3 export)
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` (ESR-0017, ADR-0019 registration; multiple self-row version syncs)
- `aiems/governance/registers/REG-0002_ADR_REGISTER.md` (ADR-0019 registration)
- `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` (EBG-0050, EBG-0051, EBG-0052)
- `research/EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL.md` (Section 6 scorecard row, Section 9 ESR-0017 entry)

No product source or test files outside `jarvis/guardian/runtime.py`, `sentinel/gemini_provider.py`, `sentinel/__init__.py` and their two corresponding test files were touched.

---

# 12. EE-0001 Trial Observations

Full detail is recorded in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9's ESR-0017 entry, not duplicated here. Summary: **Reconciled** (Lead draft reviewed and refined by ChatGPT Engineering Reviewer, who "substantially agree[d]" and would "not materially change the session conclusions"; not yet accepted by the Programme Sponsor) - 10/10 findings accepted, 0 rejected, Documentation-only handoff verified **✓** (the first empirical test of this claim in the trial), one process-cadence deviation (WP1/WP2/early-WP3 implemented before Reviewer pause) corrected mid-session and now the basis of a jointly-recommended new EE-0001 criterion (EBG-0053, "Review Gate Compliance"), and the Programme-Sponsor-directed Improvement finding independently confirmed and reworded by the Reviewer itself (tracked as EBG-0052).

---

# 13. Outstanding Work (Status at This Point)

| Item | Status |
|---|---|
| WP1-WP4 implementation and Reviewer disposition | Complete |
| Consolidated Engineering Completion Report | Complete (this section) |
| EE-0001 Lead self-assessment draft | Complete, pending independent Reviewer scoring |
| Repository staging, commit, push | **Not authorised yet - awaiting explicit Programme Sponsor go-ahead** |
| WP6 Independent Repository Verification (Engineering Reviewer) | Outstanding - follows the push |
| WP7 Repository Baseline Acceptance (Programme Sponsor) | Outstanding - follows WP6 |
| PST-0001 update to reflect ESR-0017 closure | Outstanding - last step, resolves the known stale-Current-Mode validator error |
| Formal session closure (Status: Open to Closed, Date Closed) | Outstanding |

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Immediately preceding closed session; ESR-0017 candidate focuses originated in its Section 16. |
| [[ESR-0016A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0016A]] | Post-closure governance/tooling addendum, closed before ESR-0017 opened. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial; ESR-0017 is the designated Cold Start Validation Session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog source for WP1-WP4 scoping and the WP4 roadmap; now also holds EBG-0050, EBG-0051, EBG-0052. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Source of the WP3 Gemini (Secondary provider) decision. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current accepted repository baseline at session open. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 9 July 2026 | Claude Engineering Lead | Recorded EE-0001 scorecard reconciliation: Engineering Reviewer (ChatGPT) reviewed the Lead's ESR-0017 draft self-assessment, substantially agreed, and provided four refinements (signal-to-noise recorded as instrument gap, evidence responsiveness marked not meaningfully exercised, Reviewer behavioural finding reworded in its own words, new EBG-0053 Review Gate Compliance criterion jointly recommended). Not yet accepted by the Programme Sponsor. |
| 0.2 | 9 July 2026 | Claude Engineering Lead | Added consolidated Engineering Completion Report (Architectural Milestones, Executive Summary, Engineering Outcomes, Validation Summary, Repository Deliverables, EE-0001 Trial Observations, Outstanding Work) following WP1-WP4 completion and Reviewer disposition. Session remains Open pending Programme Sponsor authorisation for repository operations. |
| 0.1 | 9 July 2026 | Claude Engineering Lead | ESR-0017 opened. Recorded WP0B authorisation, session objective and four-WP plan (UXP&harr;Backend Integration Architecture Decision, Guardian&harr;Sentinel connection, Gemini provider adapter, five-session backlog roadmap). |
