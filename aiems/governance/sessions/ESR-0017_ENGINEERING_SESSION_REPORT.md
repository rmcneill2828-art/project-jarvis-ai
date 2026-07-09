# ESR-0017 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0017 |
| Title | Engineering Session Report |
| Version | 0.11 |
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
| WP9 | First Interactive UXP - implement ADR-0019's bridge at foundation scope (Python stdio JSON-RPC entry point, Tauri sidecar process management, React live-data wiring) | Implemented and self-reviewed; awaiting Engineering Reviewer verification; see Section 15 |

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
| **WP8** | **Drafted, awaiting Engineering Reviewer review.** Feature-First Delivery Discipline added to PBK-0001 - see Section 14. |
| **WP9** | **Implemented and self-reviewed** (Python backend, Tauri Rust bridge, React frontend all wired to real calls). Awaiting Engineering Reviewer verification before it can be marked complete - see Section 15.1. |
| Formal session closure (Status: Open to Closed, Date Closed) | Outstanding - blocked on WP8 review and WP9 |

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

## 15.2 Dev-Environment Setup Automation

Raised by the Programme Sponsor after WP9's implementation was pushed: moving between machines (including a work laptop) previously meant manually re-deriving the setup sequence (`npm install`, `cargo build`, Python venv creation, `pip install -e ".[dev]"`, opting into the tracked pre-commit hook via `git config core.hooksPath scripts/hooks`) with no record of the correct order or a way to verify it worked.

Added `setup.bat` (repo root, double-click entry point) and `scripts/setup-dev-environment.ps1` (the actual bootstrap logic): checks Node/npm/Cargo/Python are on PATH with clear errors if not, runs `npm install`, builds the Rust/Tauri backend, creates/updates `.venv` and installs the project editable with dev extras, activates the tracked pre-commit hook, then runs `validate_repository.py` and the full pytest suite as a smoke test. Documented in `scripts/README.md`.

**Verified by direct execution**, not assumed: ran end-to-end in this environment (already-provisioned, so this also confirmed idempotency) - clean `npm install`, `cargo build` finished in 0.75s (cached), editable install succeeded, hook path set, validator passed 0 errors, and 182/182 tests passed.

`node_modules/`, `src-tauri/target/`, and `.venv/` remain gitignored throughout - they are derived from `package-lock.json`, `Cargo.lock` and `pyproject.toml` respectively (both lockfiles are tracked), not carried between machines. `src-tauri/.gitignore` was added in the same push as WP9 after discovering `src-tauri/target/` (2.8GB of Rust build output) had no gitignore rule excluding it at all.

Recorded as a candidate backlog item for future expansion rather than built out further now: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0054 (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks).

**Status: complete, verified, pushed.**

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
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Amended by WP8 (Feature-First Delivery Discipline). |

---

# 17. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
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
