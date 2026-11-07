# WR-ESR0061-002 - Technology, Security and Industry Landscape Review

---

## Document Control

| Field | Value |
|------|------|
| Artefact ID | WR-ESR0061-002 (Working Report - numbered at ESR-0061 WP7, 7 November 2026) |
| Title | Technology, Security and Industry Landscape Review |
| Version | 1.0 |
| Status | Working Report - received and triaged; findings dispositioned in [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] Section 6C |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Author | Antigravity (independent reviewer, commissioned directly by the Programme Sponsor); triage by Claude Engineering Implementer |
| Classification | Internal |
| Date | 7 November 2026 |
| Baseline assessed | `main` at `82103e6` (ESR-0061 WP6d) |

This is a Working Report. It is not a controlled artefact, and it authorises nothing. The report below is reproduced as received; the Engineering Implementer's verification and triage follow it (Section T).

---

**Date:** 7 November 2026  
**Reviewer:** Antigravity  
**Repository Baseline Assessed:** `main` at `82103e6` (`ESR-0061 WP6d`)  

---

## 1. What Project JARVIS AI Is Trying to Achieve

Project JARVIS AI delivers two tightly coupled deliverables (`README.md`, `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md`, `aiems/governance/reviews/WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN.md`):

1. **AIEMS (AI Engineering Management System):** A repository-first, evidence-led governance framework where architectural decisions (`ADR-*`), authority boundaries (`GAM-0001`), implementation packages (`EIP-*`), and dual independent AI peer reviews (GitHub Copilot CLI + Antigravity, with local `gpt-oss-20b` advisory pre-screening per Decision D29) are tracked as versioned artefacts.
2. **JARVIS OS / Guardian Desktop Platform:** A **local-first, privacy-by-design, family-safe AI companion and smart-home operating environment** targeting Version 1.0 (MLP 0.1) across Windows and macOS:
   - **Local-First Conversation:** Every ordinary conversation runs locally via Ollama (`qwen3.5:2b` default, hardware-sized via `OllamaSetup` in `jarvis/interfaces/ollama_setup.py`), with zero silent cloud failover (`build_default_runtime` in `jarvis/interfaces/stdio_rpc.py`).
   - **Explicit, Metered Cloud Escalation:** Cloud intelligence (`claude-sonnet-5-5` via `AnthropicProvider` in `sentinel/anthropic_provider.py`) is never used automatically; it requires a one-time, profile-bound confirmation token (`EscalationOffers` in `jarvis/interfaces/escalation.py`) and pre-call reservation against a hard monthly spend ledger (`SpendLedger` in `jarvis/shared/spend_ledger.py`, capped at £30/month per Decision D26).
   - **Enforced Household Roles & Child Safety:** Implements the 4-tier Household Role Model (`Administrator`, `Adult`, `Child`, `Guest`) from `GAM-0001` §8.1 with `scrypt`-backed Administrator PIN elevation (`AdminPin` in `jarvis/identity/admin_pin.py`), dual-stage parental + child consent for cloud escalation (`ProfileService` in `jarvis/identity/service.py`), first-use child disclosure (`ChildDisclosureStore` in `jarvis/identity/child_disclosure.py`), and fail-closed CPU-pinned input/output hazard moderation (`llama-guard3:1b` via `ModerationService` in `jarvis/interfaces/moderation.py`).
   - **Sentinel Trust Boundary:** All capabilities—conversation, personal memory (`SQLite`), local voice (`kokoro-onnx` TTS + `faster-whisper` STT), and specialist agents (GIA observability, Home Assistant read-only state query)—pass through `SentinelTrustGateway` (`sentinel/core.py`) and `TrustTierPolicy` (`sentinel/policy.py`).

---

## 2. Technology Review

### 2.1 Architecture & Stack Assessment

| Layer | Technology | Assessment |
|---|---|---|
| **UXP Desktop Shell** | Tauri v2 (Rust) + React 18 + Vite + D3-Force (`package.json`, `src-tauri/Cargo.toml`) | **Strong.** Lightweight footprint compared to Electron. Process lifecycle management uses Windows Job Objects (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`) and Unix process groups in `src-tauri/src/lib.rs` to prevent orphaned PyInstaller sidecars. |
| **UXP ↔ Backend IPC** | Newline-delimited JSON-RPC 2.0 over stdio (`StdioRpcServer` in `jarvis/interfaces/stdio_rpc.py`) | **Solid foundation, nearing scale limits.** Splitting `SLOW_METHODS` onto a single-worker `ThreadPoolExecutor` (`stdio_rpc.py` lines 122–124, 1760) keeps UI status/profile calls responsive during LLM generation while preserving turn ordering. |
| **AI Execution & Routing** | Custom `urllib` adapters (`OllamaProvider`, `AnthropicProvider`) + `ProviderOrchestrator` | **Clean & zero-bloat.** Avoiding heavy vendor SDKs keeps the PyInstaller bundle deterministic and lets Sentinel own retries, circuit breaking, and turn deadlines (`remaining_timeout_budget` in `sentinel/providers.py`). |
| **Voice Pipeline** | Self-hosted `kokoro-onnx` (TTS, `bm_george`/`bf_isabella`) & `faster-whisper` (STT) (`pyproject.toml`) | **High quality, fully offline.** Push-to-talk with no auto-submit (`GuardianRuntime.transcribe` in `jarvis/guardian/runtime.py`) avoids continuous ambient eavesdropping. |
| **Data & Persistence** | Local SQLite with explicit schema migrations (`profiles.db`, `personal.db`, `spend.db`) + rotating `audit.jsonl` | **Disciplined.** Explicit context-managed connection closing (`PersonalMemoryStore._transaction` in `jarvis/memory/store.py`) and `BEGIN IMMEDIATE` write transactions (`ProfileStore.write_transaction` in `jarvis/identity/store.py`) prevent race conditions and Windows file-locking bugs. |

### 2.2 Technical Strengths & Bottlenecks to Watch

1. **Single Slow-Lane Worker Bottleneck (`stdio_rpc.py`):**
   - `SLOW_METHODS` (`guardian.converse`, `guardian.escalate`, `guardian.speak`, `guardian.transcribe`, `guardian.agent.invoke`) share a single worker (`max_workers=1` in `serve_forever`, line 1760).
   - Consequently, synthesizing speech (`guardian.speak`) or querying a slow Home Assistant endpoint blocks the next conversation turn or transcription request. Separating voice/agent I/O onto its own bounded executor while keeping conversation turns serialized would improve perceived responsiveness.
2. **Non-Streaming Responses (`stream: False`):**
   - Both `OllamaProvider.execute` (`sentinel/ollama_provider.py` line 110) and `AnthropicProvider.execute` (`sentinel/anthropic_provider.py` line 152) wait for the entire completion before returning.
   - On CPU/consumer GPUs (and especially for Child profiles where input check + generation + output check takes ~7 seconds on the PC), waiting without progressive feedback feels slow. Because JSON-RPC notifications (`_emit_notification` in `stdio_rpc.py` lines 1241–1250) already exist, token streaming (`guardian.converse.chunk`) for unmoderated Adult/Administrator profiles—and step-progress notifications ("Checking safety…", "Thinking…") for moderated profiles—would significantly improve UX.
3. **LLM-to-Agent Disconnection:**
   - `HomeAssistantStateQueryAgent` (`jarvis/agents/home_assistant_agent.py`) and `GiaObservabilityAgent` (`jarvis/agents/gia_agent.py`) can be invoked via `guardian.agent.invoke` from the UI panel, but **the conversational LLM cannot call them as tools** during `guardian.converse` (and `AnthropicProvider` line 206 explicitly raises `RuntimeError` on `stop_reason == "tool_use"`). If a user asks in chat *"Is the front door locked?"* or *"What's the living room temperature?"*, Guardian's chat pipeline has no grounded way to query `HomeAssistantStateQueryAgent`.

---

## 3. Security & Privacy Review

### 3.1 What the Repository Gets Right (Best-in-Class Practices)

- **Prompt Injection Structural Separation:** Memory notes and prior turns are never interpolated into `system_prompt` (`GuardianCognitiveCore` in `jarvis/guardian/cognitive_core.py`). System prompts hold only the approved persona; memory is framed in `<retained_memory>` user-role blocks with tag-neutralisation (`framed_prompt` in `sentinel/providers.py` lines 102–124) so user notes cannot break out of their XML tags.
- **Child Name Sanitization Against Persona Injection:** When appending the child's first name to the local child-safety system prompt, `child_first_name` (`jarvis/interfaces/moderation.py` lines 120–134) normalizes Unicode (`NFC`) and enforces a strict single-word letter regex (`_FIRST_NAME`), preventing a crafted `display_name` from injecting instructions into the system prompt. Furthermore, the child's name is omitted from the system prompt when escalating to Claude (`GuardianRuntime.escalate` in `jarvis/guardian/runtime.py` line 405).
- **Fail-Closed Moderation with Overlapping Chunking:** `ModerationService` (`jarvis/interfaces/moderation.py` lines 175–296) runs `llama-guard3:1b` on CPU (`num_gpu: 0`, `num_ctx: 4096`) so it never evicts the chat model from 8 GB VRAM, splits long model replies into 4,000-character chunks with 400-character overlap (`split_for_checking`) so unsafe text cannot hide across chunk boundaries or overflow context, and fails closed (`UNCHECKED`) on any network/parse error.
- **Zero-Content Audit & Telemetry Discipline:** Exceptions crossing the RPC boundary strip `str(exc)` for unexpected errors (`handle_line` in `jarvis/interfaces/stdio_rpc.py` lines 1689–1696), logging only exception type and stack location (`_raise_location`) so user messages or secrets never leak into `backend.log` or `audit.jsonl`.
- **OS Keyring Isolation:** `SecretStore` (`jarvis/shared/secret_store.py`) uses Windows Credential Manager / macOS Keychain directly, rejects inert/plaintext fallback backends, and strips exception chains (`from _drop(exc)`).
- **Strict Tauri CSP & Capability Lockdown:** `src-tauri/tauri.conf.json` sets a tight CSP (`default-src 'self'`, `object-src 'none'`), and `src-tauri/capabilities/default.json` grants no frontend `shell` execute permissions.
- **Path Traversal Prevention on Home Assistant Entities:** `is_valid_entity_id` (`jarvis/agents/home_assistant_agent.py` lines 35–41) enforces `[a-z0-9_]+\.[a-z0-9_]+` before interpolating into `/api/states/{entity_id}`.

### 3.2 Concrete Security, Privacy & Governance Findings

| # | Severity | Location | Finding & Impact | Recommended Fix |
|---|---|---|---|---|
| **F1** | **Medium** | `jarvis/interfaces/stdio_rpc.py` (`_profile_export` L1093, `_memory_backup` L1497, `_memory_restore` L1523) | **Unconstrained Filesystem Paths in Export/Backup/Restore RPCs:** While gated to `Administrator` (or `Adult` for `profile.export`), the backend accepts any arbitrary path string (`params.directory`, `params.backupDir`, `params.backupPath`) without path containment or symlink checks. An `Adult` profile calling `profile.export` can write files into arbitrary user-writable system/startup directories. | Validate paths on the backend (rejecting system/executable directories and symlinks) or resolve export/backup paths through Tauri's native dialog in Rust so the frontend cannot supply arbitrary paths directly. |
| **F2** | **Medium** | `jarvis/memory/store.py` (`list_visible` L227), `jarvis/guardian/runtime.py` (`converse` L296) | **Shared Household Notes (`profile_id IS NULL`) Bypass Input Moderation for Child Profiles:** A `Child` profile receives shared household notes (`_sees_household_notes` is `True` for `Child`, `False` only for `Guest`). However, `ModerationService.check_input` only checks `message`, not `memory_notes` injected into `framed_prompt()`. If an Adult or pre-scoping migration leaves adult-oriented text in a shared household note, it is injected into every Child turn unchecked. | Either require explicit Administrator opt-in (`child_visible`) on shared household notes, or include active `memory_notes` in the moderation check for `Child` sessions. |
| **F3** | **Low / Medium** | `jarvis/agents/home_assistant_agent.py` (`HomeAssistantClient.__init__` L47), `sentinel/ollama_provider.py` (L100) | **Missing URL Scheme Validation (`file://` / `ftp://` SSRF via `urllib`):** Python's `urllib.request.urlopen` accepts `file://` and `ftp://` URLs by default. Neither `HomeAssistantClient`, `OllamaProvider`, nor `ModerationService` verifies that the configured endpoint URL starts with `http://` or `https://`. | Validate `urllib.parse.urlparse(url).scheme in {"http", "https"}` (and non-empty `netloc`) in `HomeAssistantClient.__init__`, `OllamaProvider`, and `ModerationService`. |
| **F4** | **Low** | `jarvis/interfaces/stdio_rpc.py` (`_guardian_speak` L1297) | **Unmoderated Speech Synthesis (`guardian.speak`) for Child/Guest Roles:** `GuardianRuntime.speak` assumes `text` is Guardian's own already-generated reply, but the RPC endpoint `_guardian_speak` accepts any caller-supplied `params.text` up to 5,000 characters without checking `ModerationService` when the active profile is `Child` or `Guest`. | Run `ModerationService.check_input(text)` when the active role is in `MODERATED_ROLES`, or restrict `guardian.speak` to synthesizing the most recent approved assistant response. |
| **F5** | **Low** | `src/SettingsView.jsx` (`PrivacyNotice` L61) | **Stale Privacy Notice Text After WP6c:** Line 61 of `src/SettingsView.jsx` still states: *"Only an Administrator or an Adult profile can ask Claude. A Child or Guest profile cannot."* Following WP6c (`e5faa77`), a `Child` profile **can** ask Claude when an Administrator records consent and the child acknowledges it. | Update `src/SettingsView.jsx` line 61 to match WP6c/WP6d's approved disclosure (e.g., *"An Administrator or an Adult profile can ask Claude. A Child profile can ask Claude only if an Administrator turns it on for them and the child says they understand; a Guest profile never can."*). |
| **F6** | **Low** | `jarvis/identity/store.py` (`active_profile` L39), `EIP-ESR0061-006` (Decision P4) | **Persistent Administrator Session Across Restarts & Idle Periods:** Because `active_profile` persists across restarts and has no idle timer in v1.0, an Administrator who closes the window or walks away from a shared family computer leaves the next person in an unprompted Administrator session. | Add an optional idle auto-lock (e.g., 15 minutes) and/or clear `active_profile` to `None` on backend startup when `AdminPin.is_set()` is true. |

---

## 4. Industry Comparison: What Others Are Doing in AI Home Assistance (2025–2026)

| Dimension | Home Assistant (`Assist` + `Voice PE` + Local LLM / MCP) | Commercial Cloud Assistants (Alexa+, Google Home Gemini, Apple Intelligence) | Open-Source Agentic Assistants (OpenWebUI, Khoj, Leon, FutureProofHomes) | **Project JARVIS AI (Guardian + Sentinel)** |
|---|---|---|---|---|
| **Primary Architecture** | 3-Tier Plane: Hardware (Matter/Thread) → Deterministic Core (HA OS) → Intelligence Plane (Ollama / Cloud LLM + Wyoming voice satellites). | Cloud-centric multimodal LLMs with edge wake-word/NPU routing and proprietary smart-home graphs. | Chat/RAG workspaces with broad plugin/tool calling, often running in Docker with web UIs. | **Governed Desktop Companion:** Tauri + Python sidecar, Sentinel trust gateway, local Ollama + metered Claude escalation. |
| **Tool Use & Smart Home Integration** | **Model Context Protocol (MCP)** & Native Assist API: LLMs call exposed HA intents (`HassTurnOn`, `HassGetState`) over strictly scoped entity allowlists. | Deep native device control, routine generation, and camera event summarization. | Unfettered function calling / MCP tool execution (often vulnerable to indirect prompt injection). | **Conservative by design:** `LOCAL_AGENT_ACTION` is hard-`DENY` in Sentinel; read-only `HomeAssistantStateQueryAgent` exists, but is not yet wired to LLM tool-calling. |
| **Voice Pipeline** | **Wyoming Protocol:** Distributed ESP32 hardware satellites (`Voice PE`), `openWakeWord` / `microWakeWord`, Faster-Whisper, Piper/Kokoro TTS, streaming audio. | Always-listening hardware arrays, custom wake-word silicon, duplex low-latency streaming voice. | Browser WebRTC / Whisper API, mostly single-machine push-to-talk. | **Push-to-talk desktop:** Local Faster-Whisper STT + Kokoro UK voice (`bm_george`), explicit user submit before sending to LLM. |
| **Multi-User & Child Safety** | Basic user accounts for dashboard visibility; **almost no native LLM child-safety moderation**, parental consent workflows, or spend caps per role. | Voice-print recognition (Voice ID) + kid profiles (Amazon Kids+), coupled with heavy cloud telemetry. | Single-user oriented; minimal RBAC or child hazard filtering. | **Industry-Leading Governance:** Enforced `Administrator`/`Adult`/`Child`/`Guest` roles, `scrypt` PIN elevation, local `llama-guard3:1b` I/O moderation, dual consent records, zero-content safety logs, hard £30/mo cloud spend ledger. |
| **Memory & Privacy** | Ephemeral conversation context; state history lives in time-series DB. | Continuous cloud profiling, opt-out dark patterns. | Automatic RAG vector databases (Chroma/pgvector) indexing user chats automatically. | **Explicit Consent-Per-Memory:** Every saved note requires an Adult/Admin `REVIEW` approval and stores a `ConsentDecisionRecord` in SQLite. |

### Key Takeaways from the Comparison
- **Where JARVIS Leads the Field:** Your **household governance, child-safety engineering, consent-traceable memory, and metered cloud escalation** (`EIP-ESR0061-006`, `GAM-0001`) are substantially more mature and rigorous than almost any open-source smart-home AI project, and far more privacy-respecting than commercial ecosystems.
- **Where Others Lead (and Where JARVIS Can Improve):** The broader AI Home Assistant community has converged on **structured intent/tool routing (MCP / Exposed Entity Allowlists)**, **hybrid deterministic + LLM routing**, and **low-latency streaming**. Currently, JARVIS treats conversation (`guardian.converse`) and specialist agents (`home-assistant-state-query`, `gia-observability`) as separate UI silos rather than letting Guardian reason over live home state during conversation.

---

## 5. Actionable Roadmap Recommendations

### 5.1 Near-Term Security & Compliance Polish (Pre-Launch / WP7–WP8)
1. **Fix Stale Privacy Notice Wording (`F5`):** Update `src/SettingsView.jsx` line 61 so `PrivacyNotice` accurately reflects WP6c's consented Child escalation path.
2. **Enforce `http`/`https` URL Scheme Validation (`F3`):** Add a strict URL scheme check (`http`/`https` only) in `HomeAssistantClient.__init__`, `OllamaProvider`, and `ModerationService`.
3. **Confine Export/Backup Paths (`F1`):** Harden `_profile_export`, `_memory_backup`, and `_memory_restore` so callers cannot write to arbitrary system paths.
4. **Moderate or Bind `guardian.speak` (`F4`) & Household Notes (`F2`):** Ensure `_guardian_speak` runs `ModerationService.check_input` for `Child`/`Guest` profiles, and ensure shared household notes visible to a Child are either moderated or explicitly marked child-safe by an Administrator.

### 5.2 Smart Home & Agentic Architecture (Post-1.0 Evolution)
1. **Connect Read-Only Specialist Agents to Conversation ("Exposed Entities" Pattern):**
   - Borrow Home Assistant's **Exposed Entities allowlist** concept: let an Administrator configure a small allowlist of friendly-named entities (e.g., `sensor.living_room_temperature` → *"Living Room Temperature"*, `lock.front_door` → *"Front Door Lock"*).
   - Allow `GuardianRuntime.converse()` to query `HomeAssistantStateQueryAgent` (or `GiaObservabilityAgent`) via Sentinel-gated read-only tool calls or context injection so users can naturally ask *"Is the front door locked?"* in chat.
2. **Adopt a "Deterministic Fast-Path + LLM Slow-Path" Router:**
   - Leading local smart-home assistants (such as Home Assistant Assist) resolve high-frequency status queries (*"What's the system status?"*, *"What's the living room temperature?"*) via fast intent matching in `<50ms` or lightweight tool routing, reserving full LLM reasoning for open-ended questions.
3. **Standardize on Model Context Protocol (MCP) for Future Read-Only Integrations:**
   - Rather than writing bespoke adapters for every future household data source (calendars, weather, energy tariffs/HEMS, Home Assistant), support local MCP servers gated behind Sentinel's `TrustTierPolicy` with explicit per-tool classification (`ROUTINE_INTERACTION` for read-only queries, `HUMAN_APPROVAL_REQUIRED` for state-changing calls).
4. **Reuse `EscalationOffers` One-Time Tokens for Future Device Control (`GAM-0001` §8A.3):**
   - When JARVIS eventually implements Track B Phase 3 (conditionally eligible local/smart-home actions like toggling a smart plug or light), reuse the exact **one-time, profile-bound confirmation token pattern** from `EscalationOffers` (`jarvis/interfaces/escalation.py`). Returning a structured `actionOffer` card showing the target device, action, and undo path—requiring an Adult/Administrator click before execution—will operationalize `GAM-0001` §8A with zero architectural friction.

### 5.3 User Experience & Core Intelligence Improvements
1. **Token Streaming (`stream: True`) + Moderation Progress Events:**
   - Stream responses via JSON-RPC notifications (`guardian.converse.chunk`) for `Administrator` and `Adult` profiles so the first words appear in `<500ms`.
   - For `Child` and `Guest` profiles, emit stage notifications (`"Checking safety…"`, `"Generating reply…"`, `"Verifying reply safety…"`) so the ~7-second moderated turn feels responsive while preserving strict whole-reply fail-closed safety.
2. **SQLite FTS5 / Relevance-Filtered Memory Retrieval:**
   - Currently `GuardianCognitiveCore.memory_notes` (`jarvis/guardian/cognitive_core.py` lines 69–84) takes only the newest notes up to `1,500` characters (`MEMORY_NOTES_CHAR_BUDGET`) and drops older notes.
   - Using SQLite's built-in `FTS5` full-text search (standard library `sqlite3`, zero new dependencies) to select the most relevant approved memories for the current turn (plus pinned core memories) will allow a household's memory store to scale over months and years without losing early foundational notes.

---

## T. Engineering Implementer Verification and Triage (7 November 2026)

Each security finding was checked against the code at `82103e6` before being accepted.

| # | Verified? | Disposition |
|---|---|---|
| F1 | Real: the export, backup and restore paths are taken as given (the screens pass a path chosen in the native dialog, but the backend does not contain it). Reaching it needs an Adult or Administrator session | **EBG-0172** (hardening, with F3 and F4), go-live WP9 |
| F2 | Real: shared household notes reach a Child's conversation and are not checked by the classifier; each note was approved by an Adult or Administrator | **EBG-0171** (Medium), before go-live; a design choice for the Programme Sponsor (hide household notes from a Child, mark notes child-visible, or check them) |
| F3 | Real: the endpoints are not limited to `http`/`https`; they come from environment configuration, not from a user | **EBG-0172** |
| F4 | Real: `guardian.speak` takes any text from the screen; the packaged app only sends JARVIS's own replies | **EBG-0172** |
| F5 | **Confirmed**: the privacy notice still said a Child can never ask Claude (missed in WP6c) | **Fixed in ESR-0061 WP7**, wording approved by the Programme Sponsor |
| F6 | **Confirmed, and more serious than Low**: the signed-in profile survives a restart, so the next person to open JARVIS after an Administrator closed it is the Administrator with no PIN asked | **Fixed in ESR-0061 WP7** (`ProfileService.begin_app_session`), Programme Sponsor decision |

| Improvement (Section 5) | Disposition |
|---|---|
| Streaming replies; stage progress ("Checking safety…") for a moderated turn | **EBG-0173**, candidate before go-live (a Child's turn is about 7 s) |
| Read-only Home Assistant and GIA state in conversation (an exposed-entities allowlist), a fast path for simple status questions, MCP for future read-only sources | **EBG-0174**, after 1.0, linked to EBG-0128 |
| One-time confirmation tokens reused for future device control | Note added to **EBG-0128** |
| Relevance-based memory selection (SQLite FTS5) | **EBG-0175**, after 1.0 |
| Voice and agent calls on their own worker (Section 2.2 item 1) | Note added to **EBG-0150** |

The industry comparison (Section 4) is the reviewer's own assessment and was not independently verified.
