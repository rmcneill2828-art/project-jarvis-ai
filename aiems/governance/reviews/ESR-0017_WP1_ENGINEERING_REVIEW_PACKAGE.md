# ESR-0017 WP1 - Engineering Review Package

**Status:** Working Report - not a controlled artefact (per PBK-0001 Working Report Lifecycle), not registered in REG-0001.

---

# 1. Purpose

This package hands ESR-0017 WP1 to the Engineering Reviewer (ChatGPT) for independent review, per the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial. ESR-0017 is the trial's designated Cold Start Validation Session (Claude Lead, ChatGPT Reviewer, Section 3.4).

**Process correction this package exists to fix:** the Engineering Lead implemented WP1 and WP2 back-to-back without pausing for Reviewer review between them, which is not how EE-0001 defines the Reviewer's role ("reviews the Lead's proposals before Programme Sponsor approval, and independently verifies the resulting repository state afterward" - a per-step gate, not a batch-at-the-end check). The Programme Sponsor caught this. This package covers **WP1 only**. WP2 is complete but held back from further progress (WP3/WP4 paused) until WP1 and WP2 have both been reviewed.

---

# 2. Session Context

ESR-0017 is open (`aiems/governance/sessions/ESR-0017_ENGINEERING_SESSION_REPORT.md`, currently v0.1), with four Programme-Sponsor-approved Work Packages:

1. **WP1** (this package) - UXP&harr;Backend Integration Architecture Decision.
2. **WP2** (complete, separate review) - Connect Guardian Runtime through Sentinel.
3. **WP3** (paused, half-implemented) - Gemini provider adapter.
4. **WP4** (not started) - Five-session backlog progression roadmap.

WP1 was added mid-session after the Programme Sponsor asked about the Guardian UXP, which the Lead had not otherwise included in its original two-WP proposal.

---

# 3. Problem WP1 Addresses

Direct repository inspection (not governance narrative) found:

- `src/platformStatus.js`: every piece of platform/capability/diagnostic state is a hardcoded `Object.freeze` literal. Sentinel, Providers and Agents are permanently `PLACEHOLDER`/`OFFLINE`/`NOT_IMPLEMENTED` regardless of actual backend state.
- `src/App.jsx`: the chat input and send button are `disabled`; `guardianStatus.boundary` states outright "Conversation runtime is not yet implemented."
- `src-tauri/src/lib.rs`: unmodified Tauri boilerplate - zero registered commands, no IPC surface of any kind.
- No `invoke()` call exists anywhere in the React code.
- Neither [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] (UXP selection) nor [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] (Hybrid AI Runtime) address how the UXP is supposed to reach the Python backend (`jarvis/`, `sentinel/`). No architecture decision on this exists anywhere in the repository.

Net effect: every backend capability built since ESR-0014 (Sentinel Core, provider orchestration, trust-tier policy, and now WP2's Guardian&harr;Sentinel wiring) is invisible to the only approved product surface.

---

# 4. Decision Made

Recorded in `aiems/governance/decisions/ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE.md` (full text in Section 6 below). Summary:

**Selected:** Tauri sidecar-managed, persistent Python process, communicating over duplex, newline-delimited JSON-RPC over stdio (request/response plus async notifications, LSP-style).

**Rejected alternatives:**
- Local HTTP/WebSocket server - opens a loopback network attack surface that stdio doesn't, specifically undesirable given Sentinel's whole purpose is trust-boundary enforcement.
- PyO3 embedding - couples Sentinel's full dependency graph into the Tauri build, breaks independent `pytest` testability, adds runtime weight (contrary to ADR-0007's own stated rationale).
- Rust/Node rewrite - would discard the ESR-0014-0016 Sentinel implementation (144 tests) to solve a transport problem.

**Scope of this decision:** transport/process-ownership pattern only. Does not implement the bridge, does not define the JSON-RPC message schema, does not select which capabilities are exposed first.

---

# 5. What to Review

Please assess, independently:

1. **Evidence accuracy** - is the "UXP is a disconnected mockup" claim actually supported by the cited files? (You have GitHub connector access; `src/App.jsx`, `src/platformStatus.js`, `src-tauri/src/lib.rs` are all small and worth reading directly rather than trusting this summary.)
2. **Option coverage** - are there viable integration patterns not considered? (e.g., is there a reason to prefer gRPC, Unix domain sockets, or something else not evaluated?)
3. **Rejection reasoning** - is rejecting local HTTP/WebSocket specifically because of the Sentinel trust-boundary argument sound, or is that overweighted relative to HTTP/WebSocket's testability and streaming-tooling advantages?
4. **ADR-0007/ADR-0008 alignment** - does the decision actually follow from "UXP does not own business logic" and "avoid unnecessary runtime weight," or is that a post-hoc rationalisation?
5. **Scope discipline** - WP1 was scoped as design-only. Confirm no implementation code was written under this WP (it wasn't - see Section 7 for the full file list).
6. **EBG-0050** - is the new backlog item correctly scoped as distinct from EBG-0028 (UXP Evolution Roadmap)?

---

# 6. ADR-0019 Full Text

```markdown
# ADR-0019 - UXP-Backend Integration Architecture

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0019 |
| Title | UXP-Backend Integration Architecture |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 9 July 2026 |
| Review Trigger | Significant UXP or backend runtime architecture change |

---

# Purpose

Record the ESR-0017 decision on how the Tauri + React UXP shell connects to the Python-implemented JARVIS backend (`jarvis/`, `sentinel/`), which today do not communicate at all.

---

# Scope

This decision covers process ownership, transport and protocol shape between the UXP and the backend. It does not implement the bridge, does not change Sentinel's trust or policy model, and does not select which Guardian/Sentinel capabilities are exposed first - that remains separate, scoped implementation work.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0017 WP1, following an Engineering Lead proposal grounded in direct repository inspection (`src/`, `src-tauri/`, `jarvis/`, `sentinel/`) rather than the governance narrative alone.

---

# Evidence Sources

- `src/App.jsx`, `src/platformStatus.js` - confirmed the entire UXP shell renders hardcoded `Object.freeze` state; the conversation input is `disabled`; `guardianStatus.boundary` states outright "Conversation runtime is not yet implemented."
- `src-tauri/src/lib.rs` - confirmed unmodified Tauri boilerplate; zero registered commands, no IPC surface.
- `jarvis/guardian/runtime.py` - confirmed `GuardianRuntime` holds no reference to Sentinel or any transport.
- [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] - "UXP visualises state and interaction. It does not own business logic or system state," rationale citing "avoiding unnecessary runtime weight."
- [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] - provider abstraction and avoidance of hard-coupling as a general engineering direction (informative by analogy, not directly applicable to UXP transport).
- `sentinel/core.py`, `sentinel/orchestrator.py` - Sentinel's purpose is trust-boundary enforcement before any provider execution; any new local IPC surface should not undermine that purpose by opening an unauthenticated path around it.

---

# Main Content

# 1. Problem Statement

The approved UXP (Tauri + React) and the implemented backend (Python: `jarvis/`, `sentinel/`) are different language runtimes with no defined communication path. Every backend capability built since ESR-0014 (Sentinel Core, provider orchestration, trust-tier policy, Guardian Runtime) is currently invisible to the only approved product surface.

---

# 2. Background

`jarvis/gui/app.py` is a working, functional Tkinter interface (First Light) - it works because it is Python calling Python directly, in the same process. The Tauri + React UXP (`src/`, `src-tauri/`) is a separate, later, approved product direction (ADR-0007) implemented as a static visual shell only; it has never been connected to any backend, Python or otherwise, and no architecture decision exists for how it should be.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Tauri sidecar spawning a persistent Python process, duplex JSON-RPC over stdio (LSP-style) | No listening network socket; the Python process is reachable only via pipes inherited by its parent (Tauri), so no other local process can address it. Duplex JSON-RPC over stdio is a proven pattern for exactly this shape of problem (request/response plus async notifications) - the Language Server Protocol is the canonical existing proof this scales to streaming, bidirectional traffic between a thin client and a stateful backend process. |
| Tauri sidecar spawning a persistent Python process, local-only HTTP/WebSocket server | Familiar, well-tooled pattern (`fetch`/WebSocket from React, any Python web framework backend); independently testable with `pytest` and a plain HTTP client without a Tauri build. Opens a listening loopback socket, which is a real local attack surface even bound to `127.0.0.1` (any other local process or malicious localhost-binding software could attempt to connect) - would require an ephemeral port plus a per-session shared-secret token to be safe, adding complexity precisely to close a hole the stdio option doesn't open in the first place. |
| Embed Python in the Rust process via PyO3 | Removes IPC framing entirely (single process) but requires bundling a compatible CPython runtime inside the Tauri binary, GIL management inside a Rust async application, and couples Sentinel's full dependency graph into the Tauri build/release pipeline. Cannot be tested or run independently of a Tauri build, breaking the existing `pytest`-first validation culture. Heavier runtime footprint, contrary to ADR-0007's "avoiding unnecessary runtime weight" rationale. |
| Port or rewrite backend logic into Rust or Node | Would discard the ESR-0014 through ESR-0016 Sentinel implementation (144 passing tests, trust-tier policy, provider orchestration) to solve a transport problem. Disproportionate; rejected without further analysis. |

---

# 4. Decision

The UXP shall connect to the backend via a **Tauri sidecar-managed, persistent Python process, communicating over stdio using a duplex, newline-delimited JSON-RPC protocol** (request/response plus async server-initiated notifications, in the shape proven by the Language Server Protocol).

Tauri owns process lifecycle (spawn on app start, terminate on app exit, restart on crash). The Rust side of Tauri does not interpret backend business logic; it forwards structured JSON-RPC messages between the React frontend (via `invoke`/Tauri events) and the Python process's stdio.

The local HTTP/WebSocket option is not rejected permanently - if a concrete future need arises that stdio genuinely cannot serve well (for example, a requirement for the backend to be reachable from something other than the Tauri shell itself), it should be reconsidered explicitly against that need, not adopted by default.

---

# 5. Rationale

This decision follows directly from evidence already in the repository rather than a general preference:

- ADR-0007 states the UXP "does not own business logic or system state" and should avoid "unnecessary runtime weight" - stdio sidecar keeps all business logic in the existing Python backend, unmodified in ownership, and avoids embedding a second language runtime inside Rust.
- Sentinel exists specifically to be a trust gateway (`sentinel/core.py`). Opening a listening local network socket to reach it, even loopback-only, adds an attack surface whose entire purpose Sentinel is designed to guard against; a stdio pipe reachable only by its own parent process does not have this problem and requires no additional authentication scheme to compensate.
- The existing engineering culture (144 tests, `pytest`-first validation across ESR-0014-0016) is best preserved by keeping the Python backend a normal, independently-runnable and independently-testable process rather than an embedded interpreter inside a Rust build.

---

# 6. Consequences

- A new backend entry point is required (e.g. `python -m jarvis --ipc-stdio` or similar) that speaks the JSON-RPC protocol instead of, or alongside, the existing Tkinter First Light launch path. Selecting and implementing this entry point is future scoped work, not this ADR.
- The JSON-RPC message schema (method names, notification shapes for streaming Guardian/Sentinel state) is undefined by this ADR and must be specified before implementation begins.
- `src-tauri/src/lib.rs` will need a registered sidecar command and message-forwarding logic; `src/platformStatus.js`'s hardcoded state will need to be replaced by live data once the bridge exists - both are future implementation work, not part of this decision.
- This ADR does not implement any part of the bridge. Implementing it is recommended as a near-term follow-on session (see [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] for the new candidate backlog item this ADR is paired with).

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] | UXP selection decision this ADR extends with a concrete backend-integration pattern. |
| [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] | Related independence/avoid-hard-coupling philosophy, informative by analogy. |
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Session report recording this decision as WP1. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records the new candidate backlog item for implementing this decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future UXP-backend bridge implementation work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 9 July 2026 | Claude Engineering Lead | Initial approved ADR created during ESR-0017 WP1: Tauri sidecar-managed Python process, duplex JSON-RPC over stdio, selected over local HTTP/WebSocket (avoids opening a local network attack surface around Sentinel's trust boundary), PyO3 embedding (breaks independent testability, adds runtime weight) and a Rust/Node rewrite (would discard the existing Sentinel implementation). |
```

---

# 7. Full File List (WP1 scope only)

**New file:**
- `aiems/governance/decisions/ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE.md` (full text above)

**Modified files (registration only - diffs below):**
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - added ADR-0019 row, version 3.58 to 3.61 (also covers WP0's ESR-0017 registration and REG-0002/EBR-0001 version syncs; no WP1-unrelated content changed)
- `aiems/governance/registers/REG-0002_ADR_REGISTER.md` - added ADR-0019 row, version 2.7 to 2.8
- `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - added EBG-0050, version 1.12 to 1.13

No code, test, or product files were touched by WP1. (WP2 touched `jarvis/guardian/runtime.py` and `jarvis/tests/test_guardian_runtime.py` - covered by the separate WP2 review package, not this one.)

```diff
--- a/aiems/governance/registers/REG-0002_ADR_REGISTER.md
+++ b/aiems/governance/registers/REG-0002_ADR_REGISTER.md
@@ -2,7 +2,7 @@

 > *"Good architecture is not defined by the decisions it makes, but by the reasoning it preserves."*

-**Version:** 2.7
+**Version:** 2.8

 ---

@@ -48,6 +48,7 @@ This register includes Architecture Decision Records relating to:
 | [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE]] | Device Independence and Portable Restore | Architecture | Approved | 2 Jul 2026 | - | Established devices as execution environments with portable memory, configuration and restore requirements. |
 | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION]] | Engineering Ecosystem Synchronisation | Governance | Approved | 2 Jul 2026 | - | Established WP0 Engineering Ecosystem Synchronisation including GitHub, AIEMS, OSE, Obsidian and session evidence. |
 | [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM]] | Sentinel AI Execution and Security Platform | Architecture | Approved | 8 Jul 2026 | - | Positioned Sentinel as the AI Execution and Security Platform for AIEMS, expanding the earlier trust-gateway interpretation while preserving the Guardian/Sentinel separation. |
+| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE]] | UXP-Backend Integration Architecture | Architecture | Approved | 9 Jul 2026 | - | Selected a Tauri sidecar-managed Python process communicating over duplex stdio JSON-RPC as the UXP-to-backend integration pattern, over local HTTP/WebSocket, PyO3 embedding and a Rust/Node rewrite. |

 ---

@@ -161,6 +162,7 @@ They ensure that engineering reasoning is preserved alongside engineering implem

 | Version | Date | Author | Summary |
 |---------|------------|----------------------------|-------------------------------------------------------------|
+| 2.8 | 9 July 2026 | Claude Engineering Lead | Registered ADR-0019 UXP-Backend Integration Architecture, per ESR-0017 WP1. |
 | 2.7 | 8 July 2026 | Claude Engineering Implementer | Registered ADR-0018 Sentinel AI Execution and Security Platform, closing a gap where it was present in REG-0001 but missing from this ADR-specific register. |
 | 2.6 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing ADR governance. |

--- a/aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md
+++ b/aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md
@@ -2,7 +2,7 @@

 > *"Deferred work remains governed work."*

-**Version:** 1.12
+**Version:** 1.13

 ---

@@ -12,7 +12,7 @@
 |------|-------|
 | Artefact ID | EBR-0001 |
 | Title | Engineering Backlog Register |
-| Version | 1.12 |
+| Version | 1.13 |
 | Status | Draft |
 | Owner | Programme Sponsor & Chief Engineering Advisor |
 | Classification | Internal |
@@ -116,6 +116,7 @@ Engineering backlog management shall follow these principles:
 | EBG-0047 | Sentinel Gate of Durin Architecture Specification | [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0030 with Sentinel trust gateway, trust tiers and platform-entry validation details. |
 | EBG-0048 | Guardian HITL Governance Specification | [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0031 with consent, policy, privacy, approval, memory retention and trusted mobile approve/deny governance. |
 | EBG-0049 | Cost-Aware Provider Routing and PEM-001 Revisit | [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]]; overlaps EBG-0045 | Candidate Backlog | High | Programme Sponsor | Define a cost/performance balance policy for Sentinel provider routing (leveraging ESR-0016's trust-tier classification as a candidate mechanism for cost-aware routing decisions), and revisit [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]]'s provider scoring to confirm cost is weighted as an explicit first-class criterion rather than incidental. Should account for institutional cloud/education resources potentially available to the Programme Sponsor as a cost-reduction lever. Overlapping scope with EBG-0045 (Cost and Strategic Value Framework, still Candidate Backlog, not yet actioned) - not a duplicate, but closely related and should be considered together when either is actioned. |
+| EBG-0050 | UXP-Backend Bridge Implementation | [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]]; [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] WP1 | Candidate Backlog | High | Programme Sponsor | Implement the Tauri sidecar-managed Python process and duplex stdio JSON-RPC bridge decided in ADR-0019: new `python -m jarvis` headless IPC entry point, JSON-RPC message schema (including streaming notifications for Guardian/Sentinel state), `src-tauri/src/lib.rs` sidecar command and message forwarding, and replacing `src/platformStatus.js`'s hardcoded state with live data. Distinct from EBG-0028 (UXP Evolution Roadmap, which covers staged UXP maturity broadly, not this specific integration pattern). No implementation is authorised by this backlog entry. |

 ---

@@ -231,6 +232,7 @@ Updates to this register shall preserve unique backlog identifiers and maintain

 | Version | Date | Author | Summary |
 |---------|------|--------|---------|
+| 1.13 | 9 July 2026 | Claude Engineering Lead | Added EBG-0050 (UXP-Backend Bridge Implementation) per ADR-0019 / ESR-0017 WP1. |
 | 1.12 | 9 July 2026 | Claude Engineering Reviewer | Added EBG-0049 (Cost-Aware Provider Routing and PEM-001 Revisit) per Programme Sponsor request following post-ESR-0016A discussion on balancing JARVIS running cost against performance. Cross-referenced with EBG-0045 (overlapping scope, not a duplicate) in both directions. |
 | 1.10 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing backlog governance. |
```

REG-0001's diff is larger (also covers WP0 session registration and version-sync propagation from the two register bumps above) and is available via `git diff aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` if you want to inspect it directly; the substantive WP1 content is a single added row: `| ADR-0019 | Architecture Decision Record | UXP-Backend Integration Architecture | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0017 | \`aiems/governance/decisions/\` |`.

---

# 8. Validation Performed

- `python scripts/validate_repository.py` was run after WP1's changes. Result: 1 pre-existing ERROR, 8 WARNINGs - **none newly introduced by WP1's substantive content**, with one exception noted below.
- The ERROR (`PST-0001 Current Mode references ESR-0016, latest closed session is ESR-0017.`) is a validator defect the Lead discovered incidentally: `check_stale_status_references` in `scripts/validate_repository.py` picks the highest-numbered `ESR-*.md` file as "latest closed session" without checking its `Status` field, so it fires the moment any new session file exists, even correctly `Open` (not closed) ones - which is exactly what WP0B requires (PST-0001 must NOT be updated to reference an unclosed session). **Not fixed** - out of WP1-4 scope, flagged here for Reviewer/Sponsor awareness and likely belongs in EBR-0001 as a new candidate item.
- One of the 8 WARNINGs is newly attributable to WP1: `ESR-0017_ENGINEERING_SESSION_REPORT.md:79 references Section 16, not found as a heading in this document` - this is the same known adjacency-heuristic false-positive class already documented and accepted by the Programme Sponsor in ESR-0016A WP3 (6 residual false positives, all "artefact mentioned in prose without immediate adjacency to the Section reference"). The reference is correct (ESR-0016 genuinely has a "# 16. Closure Statement" heading); the validator just can't find the adjacent WikiLink in this instance.
- **Also discovered, not fixed:** ADR-0018 (approved 8 July 2026, ESR-0014) is missing from REG-0001's own artefact table, despite REG-0002's own changelog claiming otherwise ("closing a gap where it was present in REG-0001 but missing from this ADR-specific register" - that claim appears to be false; grep confirms no `| ADR-0018 | Architecture Decision Record |` row exists in REG-0001). Not fixed as part of WP1 (out of scope); flagged for awareness.
- No code changed under WP1, so `pytest` is unaffected (152/152 passing, unchanged from before WP1 - the +8 over the 144 baseline are WP2's tests, not WP1's).

---

# 9. Explicit Non-Claims

- This package does not claim WP1 is fully validated end-to-end - there is no code to run, since WP1 is a design decision.
- This package does not ask for approval to proceed with EBG-0050 (bridge implementation) - that remains future, separately-scoped work per ADR-0019's own Consequences section.
- This package does not include WP2, WP3 or WP4 status - see the session report (`ESR-0017_ENGINEERING_SESSION_REPORT.md`) for the full four-WP picture if needed.

---

# 10. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Parent session report for this Work Package. |
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | The decision this package presents for review. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial governing this review's process. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Contains EBG-0050, the follow-on implementation item this decision enables. |

---

# 11. Reviewer Findings and Disposition

ChatGPT Engineering Reviewer returned: **0 Blocking, 0 Major, 1 Minor Observation**, plus 3 Recommendations.

| # | Finding/Recommendation | Disposition |
|---|---|---|
| Minor Observation / Recommendation 1 | HTTP/WebSocket wording implied loopback HTTP is inherently insecure; should instead state it adds unnecessary complexity for current requirements | **Accepted and fixed.** ADR-0019 bumped 1.0 to 1.1 - reworded the Options Considered row and the Rationale bullet to frame the choice as avoiding unneeded complexity (auth/port machinery) rather than calling HTTP insecure. |
| Recommendation 2 | Future implementation ADRs should define the JSON-RPC message schema separately from this transport decision | **Already satisfied, no change made.** ADR-0019's Consequences section already states the schema "is undefined by this ADR and must be specified before implementation begins." |
| Recommendation 3 | EBG-0050 implementation should define explicit failure-mode behaviour: backend crash, restart policy, version negotiation, protocol compatibility, IPC timeout strategy | **Accepted.** Correctly scoped by the Reviewer as implementation-time, not ADR-time. Folded into EBG-0050's backlog note (EBR-0001 1.13 to 1.14) so it isn't lost before that work begins. |

WP1 is now considered reviewed and closed, pending Programme Sponsor acceptance of this disposition.
