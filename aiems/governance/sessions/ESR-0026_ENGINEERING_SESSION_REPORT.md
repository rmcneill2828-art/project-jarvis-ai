# ESR-0026 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0026 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0026 |
| Date Opened | 17 July 2026 |
| Date Closed | 17 July 2026 |
| Closure Status | Closed - WP1-WP3 complete, session-wide WP6 Pass, WP7 Accept (RBL-0015 retained) |

---

# 2. Purpose

This report records the opening and execution of ESR-0026, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

**This is the first session to run entirely through the AIEMS Exchange Bridge** (`scripts/aiems_bridge.py`, EBG-0057), following its preflight fix at ESR-0025A. Every review step across all three Work Packages and the session-wide WP6 verification went through genuine `submit-to-review`/`return-findings`/`sponsor-decision`/`submit-response` cycles - no manual relay was used anywhere in this session.

---

# 3. Scope

ESR-0026 opened with WP0A/WP0B repository synchronisation (ESR-0025 and ESR-0025A closed, RBL-0015 accepted baseline). The Programme Sponsor selected a three-Work-Package objective: WP1 (Ollama Local Fallback Provider, full implementation), WP2 (EBG-0019 Memory and Data Storage architecture specification), WP3 (EBG-0076 Sentinel network exposure security requirements). A scope check at WP0 flagged that WP3's original "hardening" framing had no concrete network interface to attach to yet - the Programme Sponsor agreed WP2 and WP3 should be scoped as specifications/decision records rather than working code, matching how GAM-0001/AAM-0001 were previously handled.

All three Work Packages completed the full real Working Report Lifecycle via the bridge: draft, Codex review, Programme Sponsor approval, implementation/registration, commit, a second post-commit Codex review of the real committed diff, and a final confirmation - a template the Programme Sponsor confirmed should be standing practice going forward. Session-wide WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance closed the session, both also conducted via the bridge.

---

# 4. Engineering Authority

ESR-0026 opening was authorised by Programme Sponsor instruction on 17 July 2026, following repository synchronisation confirming [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] and its [[ESR-0025A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0025A]] addendum were both closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Three Work Packages, selected by the Programme Sponsor at WP0B:

- **WP1** - EBG-0075 (Ollama Local Fallback Provider), full implementation, since the EIP was already drafted and scoped at ESR-0025.
- **WP2** - EBG-0019 (Memory and Data Storage Architecture), a specification, since no persistence code exists anywhere yet and the item is architecture-scale.
- **WP3** - EBG-0076 (Sentinel Network Exposure Security Hardening), a decision record, since no network interface exists yet to harden - reframed at WP0 as a prerequisite approval gate for any future proposal, not present-tense hardening.

All three were met by closure.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation; scope check on WP3's framing | Complete - Section 7 |
| WP1 | Implemented `sentinel/ollama_provider.py` per EIP-ESR0025-002, closing EBG-0075 | Complete - Section 8 |
| WP2 | Approved MDS-0001 (Memory and Data Storage Architecture), closing EBG-0019 | Complete - Section 9 |
| WP3 | Approved ADR-0020 (Sentinel Network Exposure Security Requirements), closing EBG-0076 | Complete - Section 10 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, RBL-0015 retained - Section 11 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.26) reviewed at session open.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] reviewed: confirmed ESR-0025 and ESR-0025A both closed, [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted baseline, permanent Claude Implementer / Codex (ChatGPT) Reviewer appointment in force.
- Repository state verified directly: `git status` clean, `main` at `85e62c3` (ESR-0025A's closing commit), `core.hooksPath` confirmed set.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0026 (this report, authored at closure per established practice).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (retained throughout, confirmed again at this session's own WP7).
- Session objective: three Work Packages, selected by the Programme Sponsor from a menu of ready candidates (EIP-ESR0025-002 already scoped; EBG-0019 and EBG-0076 both open) - see Section 5.
- **Scope check**: before drafting began, the Engineering Implementer flagged that EBG-0076's original "network exposure hardening" framing had nothing concrete to harden (no network interface exists), risking infrastructure built to fit a guessed shape. The Programme Sponsor agreed both EBG-0019 and EBG-0076 should be scoped as specifications/decision records (mirroring GAM-0001/AAM-0001's own precedent) rather than working code - recorded as an explicit, deliberate scope decision, not a compromise.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction and subsequent scope confirmation.

---

# 8. WP1 - Ollama Local Fallback Provider (EBG-0075)

Resolves EBG-0075 per [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]], drafted at ESR-0025. This was the first Work Package to run entirely through the AIEMS Exchange Bridge, following its preflight fix at ESR-0025A.

**Pre-implementation review**: submitted to Codex via `submit-to-review`; returned no blocking findings, one non-blocking observation (keep the no-credential-rejection and `thinking`-field-discard tests explicit) already satisfied by the EIP's own requirements. Programme Sponsor approved via `sponsor-decision`.

**Implementation**: `sentinel/ollama_provider.py` implements `OllamaProvider`, mirroring `OpenAIProvider`/`GeminiProvider`'s shape with one deliberate difference - it rejects any configuration carrying a credential, since Ollama's local HTTP API is unauthenticated. Wired into `build_default_runtime()`'s `text-generation` route between the primary cloud provider and `LocalEchoProvider`, via `JARVIS_OLLAMA_MODEL` (default `qwen3.5:2b`) and `JARVIS_OLLAMA_ENDPOINT` env vars, `timeout_seconds=90.0`.

**A genuine test-isolation defect was found and fixed during implementation**: because Ollama needs no credential gate, the shared `_server()` test helper's `build_default_runtime(environ={})` began making a real, non-deterministic network call to the Programme Sponsor's actual running Ollama server during automated tests. Fixed by pointing `JARVIS_OLLAMA_ENDPOINT` at a reserved, never-listening port in that helper.

**Live smoke check finding, disclosed rather than hidden**: the EIP's own recommended 90-second timeout actually timed out on the first real attempt, only succeeding at 180 seconds - confirming the EIP's own cold-start risk section was right to flag this, with wider real-world variance than the single prior ~64s measurement suggested. Implemented at the approved 90.0s regardless, flagged as a future tuning candidate, not unilaterally extended.

**Post-implementation review of the real committed diff** found one genuine finding: `execute()` called `data.get("response")` without confirming the parsed JSON was a dict - valid JSON that isn't an object (`null`, an array, a bare string/number) has no `.get` method, raising `AttributeError` instead of the intended `RuntimeError`. Fixed with an explicit `isinstance` check, four new parametrised tests. Codex's final confirmation closed WP1 entirely: no blocking findings, the fix closes the finding, everything else remains sound.

**A mid-session tooling deviation**: while awaiting Codex's post-implementation review, Codex appeared to hang 12+ minutes on the review request. Investigation found a genuine bug in `scripts/validate_repository.py` - `.aiems-exchange/` was never excluded from its markdown scan, and since the bridge's own evidence capture embeds `validate_repository.py`'s output as evidence inside `.aiems-exchange/`'s own files, each subsequent evidence capture re-scanned and re-embedded the growing pile, ballooning the warning count from 104 to 425 to 1279 across three real evidence captures - very likely the actual cause of Codex's apparent hang. The Programme Sponsor explicitly authorised fixing this directly, outside the standard Working Report Lifecycle (no prior EIP), mirroring the ESR-0025A precedent. Fixed by adding `.aiems-exchange` to `IGNORED_DIRS`; registered as EBG-0079 (Completed).

- Commit SHAs: `2cb31fe` (implementation), `5cfd335` (validator fix), `2c55005` (AttributeError fix), `e45c793` (final closure)
- `python -m pytest`: 254 passed (was 238 at session start). `python scripts/validate_repository.py`: 0 errors, 104 pre-existing warnings.

---

# 9. WP2 - Memory and Data Storage Architecture (EBG-0019)

Resolves EBG-0019, open since ESR-0004's EIP-EKR-0001 vision recovery. Scoped as a specification per WP0's scope check.

**[[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]** (v1.0, Approved) defines a Session/Personal/Shared-Family memory taxonomy grounded in AAM-0001's Memory faculty and the existing product architecture; storage principles (local-first persistence per ADR-0012, data-layer partitioning enforcing GAM-0001 Section 9.4's personal/shared-family boundary, an initial SQLite recommendation, technical retention/deletion tied to consent traceability); device portability bound by ADR-0012's existing decision; and the extension point EBG-0023 needs once actioned. Mirrors GAM-0001/AAM-0001's structure and depth; grounded via an Explore agent's research pass confirming no persistence code exists anywhere in the repository today (`jarvis/memory/` remains an empty stub).

**Review**: Codex confirmed via the bridge - the boundary against GAM-0001 stays at the storage-architecture layer without reopening the consent gate, the taxonomy matches AAM-0001/product architecture, and the SQLite recommendation is appropriately scoped as a starting point, not a final decision. No blocking findings. Programme Sponsor approved. **Post-commit review** confirmed the committed content matched the reviewed draft exactly, with only Document Control/Version History changes between review and approval.

- Commit SHAs: `624d3ad` (approval and registration), `885c25f` (final closure)
- `python -m pytest`: 254 passed (unaffected, docs-only). `python scripts/validate_repository.py`: 0 errors, 111 warnings (104 pre-existing plus 7 known cross-document Section-reference false positives, disclosed and accepted).

---

# 10. WP3 - Sentinel Network Exposure Security Requirements (EBG-0076)

Resolves EBG-0076, registered at ESR-0025 following the Programme Sponsor's direct question on Sentinel's internet-exposure safety. Scoped as a decision record per WP0's scope check.

**[[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]]** (v1.0, Approved) defines a binding three-part security gate - authentication, rate limiting, TLS - that any future network-facing Guardian/Sentinel interface proposal must satisfy before approval. Mirrors ADR-0019's evidence-grounded style; directly builds on ADR-0019 Section 6, which had already named this exact scenario as its own revisit trigger. Grounded in `sentinel/policy.py` (confirming `TrustTierPolicy` carries no authentication/rate-limiting/transport-security concept) and PEM-001 (confirming `guardian.converse`'s billed-provider routing as a direct cost-exposure risk, not only a confidentiality one).

**Review**: Codex confirmed via the bridge - scope is coherent with ADR-0019/GAM-0001/PEM-001, correctly framed as a future proposal's approval gate rather than implementation, no scope overreach. No blocking findings. Programme Sponsor approved. **Post-commit review** confirmed the committed content matched the reviewed draft, and that EBR-0001/REG-0001/REG-0002 entries accurately reflect what was approved.

- Commit SHAs: `1578e6c` (approval and registration), `9058f5c` (final closure)
- `python -m pytest`: 254 passed (unaffected, docs-only). `python scripts/validate_repository.py`: 0 errors, 111 warnings (unchanged).

---

# 11. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0026_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0026 WP6 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge - the session-wide verification step itself run through the same real exchange mechanism as all three Work Packages, not manual relay.

**Session-wide WP6 (Independent Repository Verification)**: Codex independently confirmed repository state at `9058f5c` matches the handover's claims, that the full commit chain from `85e62c3` supports the session-wide claim, that scope boundaries are correctly characterised (MDS-0001/ADR-0020 as specifications only, the WP1 defects and EBG-0079 deviation disclosed accurately, not understated), and provided an independent baseline view. **Pass.**

**Session-wide WP7 (Repository Baseline Acceptance): [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline.** Both independent views converged: this session's diff (a small, well-tested Sentinel provider adapter, two governance/architecture specifications with no runtime code, and a tooling bug fix) does not touch `src/` (UXP) and does not change the product runtime baseline in the way ESR-0022's production provider wiring did. Programme Sponsor's own determination, informed by both: **Accept - retain RBL-0015**.

- Commit SHA: `57169b0`
- `python -m pytest`: 254 passed. `python scripts/validate_repository.py`: 0 errors, 111 warnings.

---

# 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0075, EBG-0079, EBG-0019, EBG-0076 all closed Complete this session. |
| [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] | Approved and implemented package for WP1, v1.1. |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Approved specification for WP2, v1.0. |
| [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] | Approved decision for WP3, v1.0. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0026_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0026 WP6 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.3, Section 11. |
| [[ESR-0025A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0025A]] | Recorded the bridge preflight fix this session's real usage throughout depends on. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Retained as the current accepted repository baseline at Section 11. |

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0-WP3, the session-wide WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (RBL-0015 retained). First session run entirely through the AIEMS Exchange Bridge with no manual relay. Status Open to Closed. |
