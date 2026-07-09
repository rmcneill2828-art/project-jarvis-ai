# ESR-0017 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0017 |
| Title | Engineering Session Report |
| Version | 0.18 |
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
| WP6 | Independent Repository Verification (Engineering Reviewer) | Complete - Pass, see Section 13 |
| WP7 | Repository Baseline Acceptance (Programme Sponsor) | Complete - [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] accepted 9 July 2026, superseding RBL-0011 |
| WP8 | Feature-First Delivery Discipline - new standing PBK-0001 principle (minimise controlled artefact creation; every Engineering Session delivers product-moving work; every Engineering Session makes demonstrable progress toward the live UXP) | Complete and Reviewed - PBK-0001 v1.19; ChatGPT Engineering Reviewer: 0 Blocking, 0 Major, 1 Minor (incorporated), 1 Observation (incorporated); see Section 14 |
| WP9 | First Interactive UXP - implement ADR-0019's bridge at foundation scope (Python stdio JSON-RPC entry point, Tauri sidecar process management, React live-data wiring) | Complete and Reviewed - ChatGPT Engineering Reviewer: Approved with 4 Minor findings (2 fixed, 2 deliberately deferred to EBG-0050); see Section 15.1.1 |

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

**Outcome: WP1-WP4 content complete and reviewed. Repository staging, commit and push completed (authorised 9 July 2026). WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (RBL-0012 accepted) both complete. Two further Work Packages, WP8 and WP9, are pending Programme Sponsor scope definition before the session can close - see Section 13.**

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
| EE-0001 Lead self-assessment draft | Complete - reconciled with Reviewer, pending Programme Sponsor acceptance |
| Repository staging, commit, push | Complete - authorised 9 July 2026; 4 commits, `be873d1`..`3fabbca`, pushed to `origin/main` |
| Validator defect fix (`check_stale_status_references` flagging Open sessions as stale) | Complete - authorised, fixed, tested (166/166 passing), included in the push |
| WP6 Independent Repository Verification (Engineering Reviewer) | **Complete - Pass.** ChatGPT: repository state, content, OSE and scope compliance all Pass; one non-blocking finding (the disclosed `be873d1` commit-message deviation, confirmed accurate); recommends accepting the repository state. Reviewer could not execute `pytest`/`validate_repository.py` from its connector-only environment - independently covered by the Engineering Lead's own runtime execution (166 passed, 0 errors) earlier in the session. |
| WP7 Repository Baseline Acceptance (Programme Sponsor) | **Complete.** [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] accepted 9 July 2026 (new baseline, not incremental retention), superseding RBL-0011. Stands independently of WP8/WP9. |
| `bump_version.py` self-referential-target defect fix | Complete - fixed, tested (170/170 passing), regression tests added |
| PST-0001 update to reflect RBL-0012 and in-progress state | **Complete.** ESR-0017 recorded as still Open (not closed) since WP8/WP9 remain pending - see PST-0001 Sections 3, 4A, 8, 9. |
| **WP8** | **Complete and Reviewed.** Feature-First Delivery Discipline added to PBK-0001 v1.19 - see Section 14. |
| **WP9** | **Complete and Reviewed.** ChatGPT Engineering Reviewer: Approved with 4 Minor findings (2 fixed, 2 deliberately deferred to EBG-0050) - see Section 15.1.1. |
| Formal session closure (Status: Open to Closed, Date Closed) | Outstanding - Programme Sponsor has indicated further Work Packages may follow WP9; session remains Open pending explicit closure direction. |

---

# 14. WP8 - Feature-First Delivery Discipline

The Programme Sponsor directed a new standing engineering principle, quoting: *"Get ready for a major remodel, fellas! We're back in hardware mode."* Three rules, added to [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] v1.18 as a new "Feature-First Delivery Discipline" section (between "Operational Verification Before Reporting" and "Implementation and Engineering Judgement"), verbatim intent from the Programme Sponsor:

1. **Minimise Controlled Artefact Creation** - no new controlled artefact unless not creating one would cause repository or governance drift; update existing artefacts instead where that preserves traceability. Working Reports remain permitted where a review genuinely needs a self-contained handoff, but a new file per Work Package is no longer the default (this WP8 record itself is written into this existing session report, not a new file, applying the rule to itself).
2. **Every Engineering Session Shall Deliver Product-Moving Engineering Work** - features added to JARVIS, Guardian or its subsystems, not governance/documentation alone.
3. **Every Engineering Session Shall Improve the UXP** - a tangible step toward the mock-up (`src/`, `src-tauri/`) becoming a live system reflecting real backend state, sustained until that milestone is reached.

**Rationale, as directed:** engineering sessions had increasingly produced governance and reporting artefacts relative to delivered product capability - most visibly, the UXP remained a disconnected static mock-up many sessions after the backend it should present was first built (identified earlier in ESR-0017 itself, Sections 3-4).

**Self-review:** this WP8 change is itself an artefact-minimising example of rule 1 - no new file was created to record it; PBK-0001 (existing) and this session report (existing) were both updated in place.

**Reviewer outcome (ChatGPT Engineering Reviewer): Accept with one minor refinement, one non-blocking observation. 0 Blocking, 0 Major, 1 Minor, 1 Observation.** Both incorporated into PBK-0001 v1.19, evaluated on their own merits rather than deferred to on Reviewer authority:

- **Faithfulness (Review Item 1):** all three rules confirmed faithful to the Programme Sponsor's spoken direction, quoted verbatim against each rule.
- **Minor (Review Item 3, incorporated):** Rule 3's heading and body reworded from "Every Engineering Session Shall Improve the UXP" to "Every Engineering Session Shall Make Demonstrable Progress Toward the Live UXP" - explicitly permits backend-only sessions (Guardian memory, provider failover, runtime diagnostics) that enable a future UXP increment without touching `src/` directly, and explicitly rules out cosmetic UI edits made only to formally comply.
- **Observation (Review Item 2, incorporated):** Rule 1's threshold reworded from "would cause repository/governance drift" to "the repository or governance record no longer accurately reflects the implemented engineering state" - same bar, more objectively testable, ties directly to the existing repository-first philosophy.
- **Interaction with existing governance (Review Item 4):** Reviewer found WP8 compatible with PBK-0001's lifecycle, the Working Report Lifecycle (Working Reports remain valid, just no longer automatic), COC-0001 and EE-0001 - "rebalances what an Engineering Session is expected to produce" rather than replacing existing controls.

**Status: Reviewed and refined. WP9 may now begin.**

---

# 15. WP9 - First Interactive UXP (Design, Pre-Implementation)

Programme Sponsor direction: *"Bring JARVIS, Guardian and Sentinel to life - our first interactive UXP - a foundation to build from in the future."* This implements EBG-0050 (ADR-0019's decided bridge) at foundation scope, pulled forward from the WP4 roadmap's original ESR-0018/ESR-0019 split into this session, directly satisfying WP8's new UXP-progress rule by building rather than deferring.

**Environment confirmed by direct execution (not assumed):** `cargo 1.96.0`, `node v26.3.1`, `npm 11.16.0`, `python 3.12.10` all present; `node_modules/` already installed; no prior `src-tauri/target/` build cache (first Rust build will compile the full dependency tree from scratch). `src-tauri/Cargo.toml` has only the base `tauri` dependency - no shell/process plugin yet.

**Design, as reviewed and refined (ChatGPT Engineering Reviewer: approve with refinements, all incorporated):**

1. **Backend (Python) - new stdio JSON-RPC entry point.** A new module implementing a JSON-RPC **2.0**-compatible newline-delimited loop over stdin/stdout: requests `{"jsonrpc":"2.0","id":..., "method":..., "params":{...}}`, results `{"jsonrpc":"2.0","id":..., "result":{...}}`, errors `{"jsonrpc":"2.0","id":..., "error":{"code":..., "message":...}}` - the standard envelope, adopted now specifically to avoid a breaking change when EBG-0050's fuller schema (streaming notifications) arrives later. Minimal method set: `guardian.converse` (message in, Guardian's response out) and `platform.status`. Wires a zero-config Guardian+Sentinel stack by default - `SentinelTrustGateway()` + `ProviderOrchestrator()` with `LocalEchoProvider` (no API keys required, confirmed by the Reviewer as the right foundation default - WP9 proves the UXP-to-Sentinel *path*, not external model quality) + `SentinelGatedConversationProvider` + `GuardianRuntime(conversation_provider=...)`, started - the exact combination WP2's own end-to-end test already proved works. A new CLI flag on `python -m jarvis` (e.g. `--ipc-stdio`) launches this mode instead of the Tkinter GUI.
2. **Tauri (Rust) - sidecar process management + command.** A Tauri command using `std::process::Command` with piped stdio directly - **explicitly dev-mode only, not production sidecar packaging**; `tauri-plugin-shell`'s bundled-binary packaging and Tauri v2 capability/permission handling remain EBG-0050 work, not WP9. **Minimal lifecycle handling is in scope, not deferred** (per Reviewer finding 3): the child process is spawned once (at app start or on first message) and reused, not respawned per request; it is terminated on app exit where the Tauri API allows; if the backend is unavailable or the process has crashed, the UI surfaces that clearly - **there is no silent fallback to mock or placeholder data once live calls are wired**, since that would defeat WP9's actual purpose. Full crash-restart policy remains deferred to EBG-0050. This is the first real Rust code in the project beyond boilerplate - the highest-uncertainty part of WP9.
3. **Frontend (React) - replace the mock-up with live data.** `src/App.jsx`'s chat input becomes enabled; on submit, calls `invoke('send_message', { message })` and renders the real response, or a clear error state if the backend is unavailable - never silently substituted mock content. `src/platformStatus.js`'s hardcoded state is replaced by a live `platform.status` call where in scope.

**Explicit foundation-scope exclusions (deferred, not part of WP9):** real external AI provider wiring (stays local/deterministic - a later toggle once the bridge is proven stable, per Reviewer finding 2); streaming/async JSON-RPC notifications (the envelope now supports adding these later without a breaking change, but none are implemented yet); production sidecar bundling/packaging; full crash-restart policy beyond the minimal lifecycle handling above.

**Reviewer verdict: approve with refinements before implementation - all five incorporated** (explicit dev-mode-only Rust process note; `LocalEchoProvider` confirmed as default; minimal child-process lifecycle/error handling brought into scope with an explicit no-mock-fallback rule; method set confirmed sufficient; JSON-RPC 2.0 envelope adopted from the start).

**Status: design reviewed and refined. Implementation now proceeding.**

## 15.1 Implementation Record

All three parts implemented at the agreed foundation scope, self-reviewed against the design above before handover for Reviewer verification.

1. **Backend (Python).** New `jarvis/interfaces/stdio_rpc.py`: `StdioRpcServer` implementing the agreed JSON-RPC 2.0 envelope, `guardian.converse` and `platform.status` methods, `build_default_runtime()` wiring the zero-config `SentinelTrustGateway` + `ProviderOrchestrator` + `LocalEchoProvider` + `SentinelGatedConversationProvider` + `GuardianRuntime` stack agreed in design. `jarvis/app.py`'s `main()` gained the agreed `--ipc-stdio` flag. **Verified by direct execution, not assumed**: `python -m jarvis --ipc-stdio` fed a real `guardian.converse` request over stdin returned `{"jsonrpc": "2.0", "id": 1, "result": {"message": "local-echo: hello from CLI", "provider": "local-echo"}}` on stdout. `jarvis/tests/test_stdio_rpc.py` adds 12 tests (envelope edge cases, malformed JSON/params, unknown method, handler exceptions not leaking internals, multi-line `serve_forever`, notification-without-id behaviour). Full suite: 182/182 passing.
2. **Tauri (Rust).** `src-tauri/src/lib.rs` rewritten: `BackendState` holds an optional lazily-spawned child process (`std::process::Command`, piped stdio); `call_backend()` writes one JSON-RPC line, blocks for one response line, and treats a closed pipe, write failure, or read failure as "backend unavailable" - clearing the child so the *next* call attempts a fresh spawn, per the agreed minimal lifecycle handling (no silent fallback to mock data). `send_message` and `platform_status` Tauri commands expose this to the frontend. Child process is killed on `RunEvent::Exit`. **Verified by `cargo build`** ("Finished `dev` profile ... in 23.13s" on the post-frontend-change rebuild) - this is compile verification only; the commands have not been exercised through a running windowed app (see Verification Boundary below). Two real environment defects were found and fixed while getting to a clean build, both disclosed at the time: an invalid guessed capability-permission pair removed from `src-tauri/capabilities/default.json` (Tauri v2 custom commands need no per-command permission entry, only `core:default`), and a missing `src-tauri/icons/icon.ico` (generated a minimal placeholder ICO) - the latter revealing this Tauri app had never actually been compiled before in the project's history.
3. **Frontend (React).** `src/App.jsx`'s `CommandPanel` is no longer disabled: it holds real input/conversation/sending/error state, submits via `invoke('send_message', { message })` (`@tauri-apps/api/core`), and renders Guardian's real response or a visible error banner - never a silent substitution. `src/platformStatus.js`'s static exports remain as the pre-connection default shape (now honestly labelled `Connecting`, not `Operational`); `App.jsx` calls `invoke('platform_status')` once on mount and derives live overrides for the Sentinel/Providers capability rows, the platform signal card, the header's platform indicator, and Guardian's own state/boundary text from the real response - falling to a clearly-labelled `Offline` state on failure, per the agreed no-mock-fallback rule. Diagnostics panel and quick-action shortcuts were left as static placeholders (out of WP9's agreed scope). **Verified by `npm run build`** (clean production build, 1790 modules transformed) - static/compile verification only.

**Verification boundary (disclosed honestly, per PBK-0001's Operational Verification Before Reporting):** the Python backend is verified end-to-end by real process execution and a passing test suite. The Rust and React layers are verified only by clean compilation/build - this execution environment has no display and no browser automation available, so the actual Tauri desktop window has not been opened, and no click-through of the chat input against a live spawned backend process has been observed. This is a real gap between "compiles" and "works when a human runs it," not claimed as full end-to-end proof.

**Status: implemented and self-reviewed. Awaiting Engineering Reviewer verification before WP9 is marked complete.**

## 15.1.1 Engineering Reviewer's Implementation Review Outcome

**Verdict: Approved with minor findings, not blocking.** ChatGPT Engineering Reviewer verified the implementation on `main` at commit `490997b`: Backend Pass (envelope, methods, `build_default_runtime()`, `--ipc-stdio` all aligned with the approved design); Tests Pass by inspection (12 stdio RPC tests covering the cases listed in 15.1); Tauri/Rust Pass with minor observations; Frontend Pass (live input/response/error handling, no silent mock substitution). The Reviewer explicitly agreed the compile-only Rust/React verification boundary disclosed in 15.1 is acceptable for foundation scope, while noting a real windowed click-through should be required before calling the UXP production-ready - consistent with, not a relaxation of, the disclosed boundary.

Four Minor findings raised, all considered on their merits rather than accepted blindly:

1. **`StdioRpcServer.handle_line()` did not validate `"jsonrpc": "2.0"`.** Confirmed real by inspection - the envelope's own version field was never checked. **Fixed**: `jarvis/interfaces/stdio_rpc.py` now returns `INVALID_REQUEST` if `jsonrpc` is missing or not `"2.0"`, matching the JSON-RPC 2.0 spec. Two regression tests added (`test_missing_jsonrpc_version_returns_invalid_request`, `test_wrong_jsonrpc_version_returns_invalid_request`); suite now 184/184.
2. **Handler errors expose `type(exc).__name__` and `str(exc)`.** Reviewer explicitly characterised this as acceptable for the current deterministic local-only scope, with the concern applying once external/provider-backed paths are wired through this bridge. Agreed - not fixed now (fixing it now would remove useful diagnostic detail during exactly the phase where it is safe and useful). **Deferred**: added to [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0050's note (v1.20) rather than opening a new backlog item, since EBG-0050 already covers this bridge's production hardening.
3. **Rust cleared backend state on write/EOF/read failure but not on a malformed JSON response.** Confirmed real by inspection - `serde_json::from_str` failure returned an error without clearing `BackendState`, an inconsistency with every other failure path. **Fixed**: `src-tauri/src/lib.rs`'s `call_backend()` now clears state on a malformed response too, so the next call restarts the backend rather than continuing to trust a process whose stdio framing could not be parsed. Verified by `cargo build` (clean, 24.37s).
4. **Compile-only Rust/React verification boundary.** Already disclosed in 15.1; Reviewer confirmed this is acceptable for WP9 specifically because it was disclosed, not glossed over, with a real windowed click-through required before any production-ready claim. No change - already the honest position taken.

**WP9 marked complete**, per the Reviewer's explicit recommendation: the first live UXP path (React &rarr; Tauri &rarr; Python &rarr; Guardian &rarr; Sentinel &rarr; Provider &rarr; UXP) exists at foundation scope, reviewed, with two of four findings fixed immediately and the remaining two deliberately deferred with reasoning recorded rather than silently dropped.

## 15.2 Dev-Environment Setup Automation

Raised by the Programme Sponsor after WP9's implementation was pushed: moving between machines (including a work laptop) previously meant manually re-deriving the setup sequence (`npm install`, `cargo build`, Python venv creation, `pip install -e ".[dev]"`, opting into the tracked pre-commit hook via `git config core.hooksPath scripts/hooks`) with no record of the correct order or a way to verify it worked.

Added `setup.bat` (repo root, double-click entry point) and `scripts/setup-dev-environment.ps1` (the actual bootstrap logic): checks Node/npm/Cargo/Python are on PATH with clear errors if not, runs `npm install`, builds the Rust/Tauri backend, creates/updates `.venv` and installs the project editable with dev extras, activates the tracked pre-commit hook, then runs `validate_repository.py` and the full pytest suite as a smoke test. Documented in `scripts/README.md`.

**Verified by direct execution**, not assumed: ran end-to-end in this environment (already-provisioned, so this also confirmed idempotency) - clean `npm install`, `cargo build` finished in 0.75s (cached), editable install succeeded, hook path set, validator passed 0 errors, and 182/182 tests passed.

`node_modules/`, `src-tauri/target/`, and `.venv/` remain gitignored throughout - they are derived from `package-lock.json`, `Cargo.lock` and `pyproject.toml` respectively (both lockfiles are tracked), not carried between machines. `src-tauri/.gitignore` was added in the same push as WP9 after discovering `src-tauri/target/` (2.8GB of Rust build output) had no gitignore rule excluding it at all.

Recorded as a candidate backlog item for future expansion rather than built out further now: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0054 (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks).

**Status: complete, verified, pushed.**

## 15.3 UAM-0001 Design-Baseline Consultation and Compliance Check

Prompted by the Programme Sponsor asking whether a "final look" design and Obsidian-interaction vision had already been discussed with ChatGPT - a fair challenge, since WP9's frontend work (15.1) had not consulted any prior design baseline before modifying `src/App.jsx`.

**Finding: it had been discussed, and formally baselined, but not consulted.** [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] (Guardian Experience Architecture v1.0, Approved Baseline, `aiems/models/`) defines the canonical desktop layout, Guardian Orb meaning, conversation-first interaction, capability awareness, Sentinel trust-posture representation, and colour/animation/accessibility principles. Its origin traces to `aiems/History/Full Chat/FCH-0009_ESR-0009_FULL_CHAT_HISTORY.md` (a ChatGPT-generated mock-up image, agreed as "UXP Design Baseline v1.0") and `FCH-0011_ESR-0011_FULL_CHAT_HISTORY.md` (further description as a "JARVIS AI Orb / Obsidian Knowledge Graph Visualisation" concept). The generated mock-up image itself is not present in the repository as a file - only described in the chat transcript text - so it is not recoverable from here if the Programme Sponsor no longer has the original.

**Obsidian-as-product-feature: already explicitly decided, and already correctly reflected in current architecture.** `FCH-0008_ESR-0008_FULL_CHAT_HISTORY.md` records an explicit decision that Guardian should not have an Obsidian connector: *"I don't think we actually need an Obsidian connector for Guardian. I think we need it for the Engineering Agent."* This is consistent with [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] ("Obsidian remains outside the JARVIS runtime platform") and `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md` Section 6. No inconsistency found here - both older prior-art and current governance agree.

**Compliance check of the current UXP (post-WP9) against UAM-0001 Sections 5-19: one real defect found and fixed.** `src/platformStatus.js`'s `diagnostics` array (rendered by `DiagnosticsPanel`) remained fully static after WP9 wired live data elsewhere, meaning the Diagnostics panel could show `Sentinel: Placeholder` / `Guardian: Operational` (hardcoded) at the same time the sidebar and status cards - fed by the same `platform.status` call - showed the real, potentially different, live state. Two panels on the same screen contradicting each other directly undermines UAM-0001 Section 10 ("Capability awareness exists to preserve trust") and Section 11 (diagnostics should show "what is available and what remains placeholder"). **Fixed**: `src/App.jsx` gained `deriveDiagnostics()`, deriving the `guardian`, `sentinel` and `providers` diagnostic rows from the same `platformState`/`platformError` already used for the sidebar and status cards; `boundary`, `shell`, `agents` and `first-light` remain legitimately static (still accurate). Verified by `npm run build` (clean) and confirmed live via Vite HMR against the already-running dev session from this conversation (`Guardian runtime foundation started` ... HMR updates picked up ... clean shutdown).

**Also noted, not fixed (lower urgency, broader scope):** `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md` is stale - still dated to ESR-0009 readiness, predating WP2 (Guardian-Sentinel connection) and WP9 (UXP-backend bridge) actually being implemented. Refreshing it is a multi-session documentation exercise beyond this check's scope; not actioned now.

**Status: complete for the material available at the time - superseded by 15.4 below, which found a larger gap in the same area.**

## 15.4 Guardian Orb Design Direction Recovered from FCH-0010

The Programme Sponsor located a design conversation and mock-up in `aiems/History/Full Chat/FCH-0010_ESR-0010_FULL_CHAT_HISTORY.md`, believing it had already been merged into the governed architecture. It had only partially been - a real gap 15.3 did not catch because it checked the current UXP against UAM-0001 as written, not UAM-0001 against everything ever approved in chat.

**What was found:** [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] Section 15 ("Guardian UXP Design Outcome") did capture and formally approve a design direction from that conversation - the Guardian Orb as a live rendering of the repository's knowledge graph (nodes as artefacts, connections as relationships, cluster illumination, agents appearing as nodes), correctly scoped as "approved design direction, not yet an implementation package," with "Guardian Orb prototype" explicitly deferred (Section 21). That part of the chain worked as intended.

**Where the chain broke:** [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] - the actual persistent Guardian Experience Architecture artefact - was created under ESR-0009, *before* the ESR-0010 conversation happened, and was never updated afterward to reference it. UAM-0001's only later revision (v1.1) addressed unrelated ADR-0018/Sentinel scope. The richest detail from the original conversation - the specific Orb status-colour semantics (calm pulse/gold highlight/green pulse etc.) and a four-phase achievability roadmap - existed only in the raw chat transcript, in neither ESR-0010's own summary nor UAM-0001.

**Fixed, per Programme Sponsor direction (full incorporation):**
- [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] v1.2: new Section 8.1 (Knowledge Graph Representation) and Section 8.2 (Orb Status Semantics), both explicitly marked as design direction only, not implementation, per UAM-0001's own Section 18. ESR-0010 added to OSE Relationships/Related Artefacts. A Subsequent Architectural Update note records the retroactive incorporation and why it happened late.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0028 (UXP Evolution Roadmap) v1.21: added the four-phase achievability sequencing (static graph -> cluster colours/chat UI -> agent traversal animation -> Guardian reasoning/telemetry connection) as candidate staging for when this backlog item is actioned.

**Note for the Programme Sponsor:** the original ChatGPT-generated mock-up image itself is not present anywhere in the repository - only described in FCH-0010's transcript text. If the original image file still exists outside the repository, it is worth adding to `aiems/models/` as a real reference asset; it cannot be recovered from here.

**Status: complete for the material recovered at the time.**

## 15.5 Reference Mock-Up Image Incorporated

The Programme Sponsor located and provided the actual mock-up image referenced in FCH-0010/FCH-0011 ("JARVIS AI ORB - Obsidian Knowledge Graph Visualisation"), confirming it is materially richer than the text description 15.4 had already incorporated into UAM-0001 8.1/8.2.

**Incorporated into [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] v1.3:**
- Section 7.1 Reference Dashboard Composition - System Health, Knowledge Metrics, Active Clusters (with the seven specific named domains), Real-Time Activity feed, an AIEMS Principles panel, and a persistent conversation bar with voice affordance - each mapped back to which of Section 7's five canonical layout elements it instantiates.
- Section 8.3 Orb Status Panel - the Mode/Confidence/Autonomy/Permission textual readout, explicitly distinguished from 8.2's ambient animation semantics and tied directly to [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] HITL governance, with an explicit rule that it must never show a more permissive state than what Guardian/Sentinel actually enforces.

Both new sections are explicitly framed as illustrative reference / design direction only, per Section 18's Capability Evolution Model - not an implementation specification, and not authorisation to build any of it now.

**The image file is now in the repository.** The Engineering Lead has no mechanism in this environment to extract and persist a pasted image's raw bytes to disk directly - only to view it and describe its content in text - so the Programme Sponsor saved it directly to `aiems/models/`. Renamed from `JARVIS mockup.jpg` to `UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` to match repository artefact naming convention, and referenced from UAM-0001 Section 7.1.

**Status: complete. Mock-up preserved as a real repository asset, referenced from UAM-0001, not just described.**

## 15.6 WP4 Roadmap Revised - EBG-0055 Slotted into Freed Capacity

The Programme Sponsor asked whether the Guardian Orb knowledge-graph work could be built "organically in line with planned WPs" rather than as a separate initiative. The Engineering Lead identified that it could, concretely: `EBG-0050` (the UXP-backend bridge) was originally planned as a two-session effort split across ESR-0018 (schema/Python) and ESR-0019 (Rust/frontend) per the WP4 roadmap - but WP9 delivered both phases in ESR-0017 itself, two sessions early, freeing real capacity in ESR-0018/ESR-0019 that did not exist when WP4 was reviewed.

**Actioned, on Programme Sponsor confirmation ("yes please"):**
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] v1.22: `EBG-0050` status corrected from Candidate Backlog to Completed (Foundation Scope) - it was stale, still showing as un-implemented after WP9 delivered it. New `EBG-0055` (Knowledge Graph Phase 1 - Static Live Graph) added: repository WikiLinks parsed into nodes/edges, exposed via a new JSON-RPC method over the existing bridge, first-pass 2D rendering (not the full 3D orb sphere - explicitly scoped as the achievable first slice, distinct from Phases 2-4).
- `aiems/governance/reviews/ESR-0017_WP4_ENGINEERING_REVIEW_PACKAGE.md` (Working Report, not REG-0001-registered) updated in place: Sections 5/6 mark `EBG-0050`'s rows as completed early (struck through, historical reasoning retained rather than deleted); Section 6.1's Decision Gate updated to show 2 of 3 conditions already satisfied (bridge complete, Guardian interactive - both verified via the real windowed Tauri session earlier in ESR-0017); `EBG-0055` recommended for ESR-0018 or ESR-0019's freed capacity; new Section 16 addendum records why and flags one open question below.

**Open question, not resolved by the Lead alone:** the WP4 roadmap was already reviewed and closed by ChatGPT Engineering Reviewer (Section 15, 0 Blocking/0 Major/4 Minor, all accepted). This revision was made by the Engineering Lead alone, after that review closed. Per this session's own per-Work-Package review discipline, the Programme Sponsor should decide whether striking through completed items and adding one new candidate (still separately gated on implementation authorisation) needs its own Reviewer pass, or whether it can stand without one - flagged in the addendum itself for that decision, not decided here.

**Status: complete, pending Programme Sponsor decision on whether a Reviewer pass is needed for this revision.**

## 15.7 Mock-Up Scale Corrected Against the Real Obsidian Graph

The Programme Sponsor shared a screenshot of the actual current Obsidian graph, noting the mock-up's node count appeared exaggerated by comparison. Confirmed by direct count rather than visual estimate: **~135 markdown artefacts repository-wide (125 within `aiems/`)**, consistent with the real screenshot's visible density and nowhere near the mock-up's stated "6,842 nodes, 18,392 connections" - those figures are illustrative of an aspirational future scale, not the current or near-term real state.

**Corrected, since this materially changes EBG-0055's difficulty assessment:** [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] v1.5 Section 7.1 and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] v1.23 EBG-0055 both now state the real ~135-node scale and remove the earlier "2D first, not the full 3D sphere, because performance at thousands of nodes" caveat - at real scale, rendering performance is not a significant Phase 1 constraint, and a modest 3D sphere is realistically achievable, not just a 2D fallback. Implementation should render live figures for the repository's actual current scale, re-assessing rendering approach only if the real node count grows by an order of magnitude later.

**Status: complete.**

---

# 16. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Immediately preceding closed session; ESR-0017 candidate focuses originated in its Section 16. |
| [[ESR-0016A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0016A]] | Post-closure governance/tooling addendum, closed before ESR-0017 opened. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial; ESR-0017 is the designated Cold Start Validation Session. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog source for WP1-WP4 scoping and the WP4 roadmap; now also holds EBG-0050, EBG-0051, EBG-0052, EBG-0053, EBG-0054. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Source of the WP3 Gemini (Secondary provider) decision. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current accepted repository baseline at session open. |
| [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] | Current accepted repository baseline, accepted mid-session (WP7). |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Approved Guardian Experience Architecture baseline; consulted and checked for compliance in Section 15.3 (one defect found and fixed); Guardian Orb knowledge-graph design direction retroactively incorporated in Section 15.4 (v1.2). |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] | Source of the Guardian Orb knowledge-graph design direction recovered and re-traced in Section 15.4. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Amended by WP8 (Feature-First Delivery Discipline). |

---

# 17. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.18 | 9 July 2026 | Claude Engineering Lead | Recorded Section 15.7: Programme Sponsor's real Obsidian graph screenshot showed the mock-up's node count was exaggerated. Confirmed by direct count (~135 markdown artefacts, not thousands), corrected EBG-0055's difficulty assessment accordingly in UAM-0001 v1.5 and EBR-0001 v1.23 - removed the 2D-only performance caveat, since real scale is not a rendering-performance constraint. |
| 0.17 | 9 July 2026 | Claude Engineering Lead | Recorded Section 15.6: revised the WP4 five-session roadmap after confirming with the Programme Sponsor that Knowledge Graph Phase 1 should build organically in line with planned WPs. EBG-0050 corrected from stale Candidate Backlog to Completed (Foundation Scope) in EBR-0001 v1.22; new EBG-0055 (Knowledge Graph Phase 1) added, slotted into ESR-0018/ESR-0019 capacity freed by EBG-0050's early completion. ESR-0017_WP4_ENGINEERING_REVIEW_PACKAGE.md updated in place (Sections 5/6/6.1 struck through and corrected, new Section 16 addendum). Flagged an open question for the Programme Sponsor: this revision was made by the Lead alone after the original WP4 Reviewer pass closed, and per this session's own per-WP review discipline it may warrant its own Reviewer check before being treated as accepted. |
| 0.16 | 9 July 2026 | Claude Engineering Lead | Updated Section 15.5: Programme Sponsor saved the mock-up image directly into the repository (aiems/models/, renamed to UAM-0001_GUARDIAN_ORB_MOCKUP.jpg for convention). UAM-0001 (now v1.4) updated to reference the real file instead of describing it as outstanding. |
| 0.15 | 9 July 2026 | Claude Engineering Lead | Recorded Section 15.5: Programme Sponsor located and provided the actual FCH-0010/FCH-0011 mock-up image, confirming it is materially richer than the text description already incorporated. Added UAM-0001 Sections 7.1 (Reference Dashboard Composition - System Health, Knowledge Metrics, Active Clusters, Real-Time Activity, AIEMS Principles panel, persistent conversation bar) and 8.3 (Orb Status Panel - Mode/Confidence/Autonomy/Permission, tied to ADR-0010 HITL governance), both explicit design-direction-only (UAM-0001 v1.3). Noted the image file itself cannot be persisted to the repository from this environment - no mechanism exists to extract pasted image bytes to disk - and remains outstanding pending the Programme Sponsor saving it directly. |
| 0.14 | 9 July 2026 | Claude Engineering Lead | Recorded Section 15.4: Programme Sponsor located FCH-0010's Guardian Orb design conversation, believing it was already merged into governed architecture. Traced the chain - ESR-0010 Section 15 did approve and record a design direction correctly, but UAM-0001 (created earlier, under ESR-0009) was never updated afterward to reference it. Fixed per Programme Sponsor's full-incorporation decision: UAM-0001 v1.2 (Sections 8.1 Knowledge Graph Representation, 8.2 Orb Status Semantics, both explicit design-direction-only) and EBR-0001 v1.21 (EBG-0028 phased achievability roadmap). Noted the original mock-up image is not recoverable from the repository. |
| 0.13 | 9 July 2026 | Claude Engineering Lead | Recorded Section 15.3: consulted UAM-0001 (Approved Guardian Experience Architecture baseline, previously not checked before WP9's frontend work) and its FCH-0009/FCH-0011 origin (a ChatGPT-generated mock-up, not preserved in-repo). Confirmed Obsidian-as-product-feature was already explicitly decided against (FCH-0008), consistent with current architecture. Compliance check against UAM-0001 Sections 5-19 found and fixed one real defect: DiagnosticsPanel's guardian/sentinel/providers rows were static and could contradict the live sidebar/status-card state from the same platform.status call; now derived consistently via a new deriveDiagnostics() in App.jsx. Verified by npm run build (clean) and live via Vite HMR against the running dev session. Noted JARVIS_CAPABILITY_READINESS_MATRIX.md is stale (pre-dates WP2/WP9) but did not action it - out of this check's scope. |
| 0.12 | 9 July 2026 | Claude Engineering Lead | Recorded ChatGPT Engineering Reviewer's WP9 implementation review outcome (Section 15.1.1): Approved with 4 Minor findings. Fixed 2 (jsonrpc version validation in stdio_rpc.py with 2 new regression tests, 184/184 passing; Rust state cleared on malformed response too, cargo build clean); deliberately deferred 2 (handler exception detail leakage - noted on EBR-0001 EBG-0050 v1.20; compile-only verification boundary - already honestly disclosed, Reviewer confirmed acceptable for foundation scope). WP9 marked Complete and Reviewed per Reviewer recommendation. Corrected a stale Section 13 WP8 row that still read 'awaiting review' after WP8 was already completed. |
| 0.11 | 9 July 2026 | Claude Engineering Lead | Recorded WP9-adjacent Dev-Environment Setup Automation (Section 15.2): setup.bat / scripts/setup-dev-environment.ps1, prompted by the Programme Sponsor's work-laptop move. Verified by direct execution (idempotent re-run, 182/182 tests). Added EBR-0001 EBG-0054 as the forward-looking backlog item for future expansion (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks). Committed and pushed as b3806d5. |
| 0.10 | 9 July 2026 | Claude Engineering Lead | Recorded WP9 Implementation Record (Section 15.1): all three parts (Python backend, Tauri Rust bridge, React frontend) implemented and self-reviewed against the approved design. Backend verified end-to-end by direct execution and 12 passing tests; Rust and React verified by clean build/compile only - verification boundary disclosed honestly (no windowed-app or click-through testing possible in this environment). Status: awaiting Engineering Reviewer verification before WP9 is marked complete. |
| 0.9 | 9 July 2026 | Claude Engineering Lead | Recorded ChatGPT Engineering Reviewer's WP9 design review outcome: approve with five refinements, all incorporated (JSON-RPC 2.0 envelope, LocalEchoProvider default confirmed, minimal child-process lifecycle handling with explicit no-mock-fallback rule, method set confirmed sufficient, explicit dev-mode-only Rust process note). Implementation now proceeding. |
| 0.8 | 9 July 2026 | Claude Engineering Lead | Recorded WP9 (First Interactive UXP - Bring JARVIS, Guardian and Sentinel to life) design plan: three-part foundation-scope implementation of ADR-0019's bridge (Python stdio JSON-RPC entry point, Tauri Rust sidecar process management, React live-data wiring), environment confirmed by direct execution, explicit scope exclusions stated. Design only, not yet implemented - awaiting Engineering Reviewer input per Programme Sponsor direction before coding begins. |
| 0.7 | 9 July 2026 | Claude Engineering Lead | Recorded ChatGPT Engineering Reviewer's WP8 review outcome: Accept with one minor refinement, one non-blocking observation (0 Blocking, 0 Major). Both incorporated into PBK-0001 v1.19. WP8 complete and reviewed; WP9 may now begin. |
| 0.6 | 9 July 2026 | Claude Engineering Lead | Recorded WP8 (Feature-First Delivery Discipline, added to PBK-0001 v1.18) directly in this session report per the new artefact-minimisation rule it introduces - no new file created. Drafted, awaiting Engineering Reviewer review before WP9 begins. |
| 0.5 | 9 July 2026 | Claude Engineering Lead | Recorded WP7 Repository Baseline Acceptance (RBL-0012) and WP6/WP8/WP9 rows in Work Package Plan. Programme Sponsor indicated two further Work Packages (WP8, WP9) before session closure - scope not yet defined. Session remains Open. |
| 0.4 | 9 July 2026 | Claude Engineering Lead | Recorded WP6 Independent Repository Verification result: ChatGPT Engineering Reviewer PASS (repository state, content, OSE and scope compliance all Pass; one disclosed non-blocking commit-message deviation; recommends baseline acceptance). WP7 Repository Baseline Acceptance now outstanding, Programme Sponsor decision. |
| 0.3 | 9 July 2026 | Claude Engineering Lead | Recorded EE-0001 scorecard reconciliation: Engineering Reviewer (ChatGPT) reviewed the Lead's ESR-0017 draft self-assessment, substantially agreed, and provided four refinements (signal-to-noise recorded as instrument gap, evidence responsiveness marked not meaningfully exercised, Reviewer behavioural finding reworded in its own words, new EBG-0053 Review Gate Compliance criterion jointly recommended). Not yet accepted by the Programme Sponsor. |
| 0.2 | 9 July 2026 | Claude Engineering Lead | Added consolidated Engineering Completion Report (Architectural Milestones, Executive Summary, Engineering Outcomes, Validation Summary, Repository Deliverables, EE-0001 Trial Observations, Outstanding Work) following WP1-WP4 completion and Reviewer disposition. Session remains Open pending Programme Sponsor authorisation for repository operations. |
| 0.1 | 9 July 2026 | Claude Engineering Lead | ESR-0017 opened. Recorded WP0B authorisation, session objective and four-WP plan (UXP&harr;Backend Integration Architecture Decision, Guardian&harr;Sentinel connection, Gemini provider adapter, five-session backlog roadmap). |
