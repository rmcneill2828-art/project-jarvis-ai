# ADR-0019 - UXP-Backend Integration Architecture

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0019 |
| Title | UXP-Backend Integration Architecture |
| Version | 1.1 |
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
| Tauri sidecar spawning a persistent Python process, local-only HTTP/WebSocket server | Familiar, well-tooled pattern (`fetch`/WebSocket from React, any Python web framework backend); independently testable with `pytest` and a plain HTTP client without a Tauri build. Not inherently insecure, but opens a listening loopback socket - reaching the same "only my own parent process can reach me" guarantee stdio provides by construction would require deliberately adding an ephemeral port and a per-session shared-secret token, which is unnecessary complexity given no current requirement forces it. |
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
- Sentinel exists specifically to be a trust gateway (`sentinel/core.py`). A stdio pipe reachable only by its own parent process reaches that same posture with no additional authentication scheme; a local HTTP/WebSocket server would need one (ephemeral port, shared-secret token) to match it - not because loopback HTTP is inherently insecure, but because there is no current requirement that justifies building and maintaining that extra machinery.
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
| 1.1 | 9 July 2026 | Claude Engineering Lead | Softened HTTP/WebSocket wording per ChatGPT Engineering Reviewer WP1 finding - reframed from implying loopback HTTP is inherently insecure to the actual reason (avoidable complexity for no current requirement). |
| 1.0 | 9 July 2026 | Claude Engineering Lead | Initial approved ADR created during ESR-0017 WP1: Tauri sidecar-managed Python process, duplex JSON-RPC over stdio, selected over local HTTP/WebSocket (avoids opening a local network attack surface around Sentinel's trust boundary), PyO3 embedding (breaks independent testability, adds runtime weight) and a Rust/Node rewrite (would discard the existing Sentinel implementation). |
