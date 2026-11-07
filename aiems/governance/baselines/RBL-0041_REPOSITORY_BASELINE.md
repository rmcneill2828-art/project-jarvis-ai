# RBL-0041 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0041 |
| Title | ESR-0061 Repository Baseline (Go-Live Session A: Ollama First, Claude Escalation, Guardian Redesign, Settings and Data Rights, Household Safety) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] |
| Previous Baseline | [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 7 November 2026 |
| HEAD at baseline creation | `80b462f` |

---

# 2. Purpose

RBL-0041 records the repository baseline accepted by the Programme Sponsor at the close of ESR-0061, superseding [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]].

ESR-0061 was **Session A of the go-live plan** ([[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]]), extended by Programme Sponsor direction from WP1-WP2 to WP1-WP6, and closed after WP6 with the Mac checks carried forward (Programme Sponsor decision, 7 November 2026). It turned JARVIS from a desktop shell with provider plumbing into a product a household can install and use: a local model by default, Claude only when a person confirms it, a redesigned interface, a first-run flow and per-profile data rights, and household safety for a child.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v3.1 - content re-audited at ESR-0061 WP1b (6 October 2026); the capabilities WP3 to WP6 added are **not yet re-audited into it** (handover item 2). |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0061 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP1 - Release gate, governance and streamlining** ([[EIP-ESR0061-001_RELEASE_GATE_GOVERNANCE_AND_STREAMLINING|EIP-ESR0061-001]]): go-live governance enacted, the v1.0 release gate resolved (EBG-0130), a register status check and Antigravity as the second independent reviewer (EBG-0169).

**WP2 - Platform hardening and macOS** ([[EIP-ESR0061-002_PLATFORM_HARDENING_AND_MACOS|EIP-ESR0061-002]]): SQLite WAL and busy timeout, error replies without content, and macOS builds in CI (EBG-0162; the real-Mac checks carried).

**WP3 - Provider strategy** ([[EIP-ESR0061-003_PROVIDER_STRATEGY_OLLAMA_FIRST_AND_CLAUDE_ESCALATION|EIP-ESR0061-003]], ADR-0023): Ollama on each machine for every conversation; Claude only on a confirmed, profile-bound, metered escalation; OpenAI and Gemini unregistered; local model detection, recommendation and download (EBG-0163).

**WP4 - Guardian experience redesign** ([[EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN|EIP-ESR0061-004]]): a new shell, the presence Orb, AI disclosure, role-aware views and accessibility checks (EBG-0164).

**WP5 - Setup, settings, privacy and data rights** ([[EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS|EIP-ESR0061-005]]): the Claude key in the operating system's credential store, note sharing per profile, audit retention, per-profile export and erasure, and the first-run flow (EBG-0165, EBG-0110).

**WP6 - Household safety** ([[EIP-ESR0061-006_HOUSEHOLD_SAFETY_PIN_MODERATION_AND_CHILD_CONSENT|EIP-ESR0061-006]]): the Administrator PIN and elevation rule; local moderation of Child and Guest conversations with Llama Guard 3, failing closed; the child-safety persona layer; consent before a child may ask Claude (off by default); the child's first-use explanation and the Children and safety view (EBG-0166). Every child-facing text approved by the Programme Sponsor.

**WP7 - Session-wide verification and the independent technology and security review**: Copilot Conditional Pass (six Mediums, all dispositioned); Antigravity's review ([[WR-ESR0061-002_TECHNOLOGY_AND_SECURITY_LANDSCAPE_REVIEW|WR-ESR0061-002]]) triaged, its two confirmed findings fixed (an Adult or Administrator session no longer survives a restart once a PIN is set; the privacy line about a Child and Claude).

**The Programme Sponsor's determination** (WP8): **establish a new baseline** ("please establish a new baseline", 7 November 2026).

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `sentinel/anthropic_provider.py`, `sentinel/policy.py`, `jarvis/interfaces/escalation.py`, `jarvis/shared/spend_ledger.py` | Claude adapter; confirmed, profile-bound escalation tokens; the monthly spend cap; Sentinel's cloud rule (Administrator and Adult, or a Child with recorded consent) |
| `jarvis/interfaces/ollama_setup.py`, `jarvis/config/ollama_models.py` | Ollama detection, hardware recommendation, allow-listed downloads |
| `src/` | The redesigned shell, Orb, Settings, first-run flow, PIN screens, Children and safety, the child's first-use page and Claude card |
| `jarvis/identity/` | The Administrator PIN (scrypt, lock-out), safety events, child consents, the first-use acknowledgement (profile migrations 3 to 6) |
| `jarvis/interfaces/moderation.py` | Llama Guard 3 moderation of Child and Guest turns, on the processor, failing closed |
| `jarvis/memory/profile_export.py`, `jarvis/shared/secret_store.py` | Per-profile export (schema version 2) and erasure; the Claude key in the credential store |
| `jarvis/tools/` | `reset_admin_pin` and `add_administrator`, run on the computer |
| `scripts/measure_moderation.py`, `scripts/run_reviewer.py` | The classifier measurements; reviewer runs through the bridge |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0110, 0130, 0157, 0161, 0163, 0164, 0165, 0166, 0169 Completed; EBG-0170 to EBG-0177 registered |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v3.1 was content re-audited at ESR-0061 WP1b. The product capabilities delivered in WP3 to WP6 (Ollama-first conversation, confirmed Claude escalation, the redesigned interface, setup and data rights, household safety) are recorded in their EIPs and ESR-0061 but **not yet re-audited into PCB-0001 and the Capability Readiness Matrix**; that re-audit is owed (handover item 2).

---

# 7. Architecture Outcomes

- Conversation is local by default; the cloud is an explicit, confirmed, metered step, never a fallback (ADR-0023).
- Household roles are enforced with an Administrator PIN; a Child or Guest conversation is moderated both ways and fails closed; a Child reaches Claude only with recorded, acknowledged consent, checked by the RPC layer and by Sentinel independently.
- No conversation text is kept anywhere: safety events, audit and logs hold kinds, counts and times only.
- macOS is a build target in CI.

---

# 8. Scope Boundaries

- no `LOCAL_AGENT_ACTION` change: device control stays denied;
- no age verification, idle lock, email or message reporting to parents, or moderation of Adult and Administrator conversations (EIP-ESR0061-006 Section 7);
- Claude for a Child is built but **stays off until the public "Children and privacy" page is published** (Programme Sponsor decision, go-live WP8);
- no code signing (EBG-0146, Deferred);
- the real-Mac checks and measurements not yet run.

---

# 9. Verification

- 30 session commits (`0669a53..80b462f`), every product commit gated through the real Sponsor Approval Service via `submit-response` against an approval recorded on its parent (confirmed by the session-wide review); one register-only commit before the session opened (`e153874`) recorded as an explicit exception.
- CI on `main` green on every pushed session commit, including `80b462f` (run 42411987427); the informational WebKit job fails five microphone tests, unchanged since before WP6.
- pytest 1461 passed, 4 skipped (Windows); 1465 passed (Linux, python:3.12-slim); Playwright (chromium) 192 passed, 5 skipped; cargo test 19 passed, 1 ignored, clippy `--tests` and fmt clean; ruff clean; validator 0 errors, 311 warnings; `sync_product_version.py --check` agrees; `npm run build` clean; `npm audit` (production) and `pip-audit` (fresh Linux environment) no known vulnerabilities.
- Engineering Reviewer coverage: GitHub Copilot CLI and Antigravity, one after the other, at every high-risk step (D19); Copilot post-commit review of every committed WP; a session-wide Copilot review; an independent Antigravity technology and security review.
- Measurements on the household PC (Ryzen 5 5600, RTX 4060 8 GB): message check median 0.69 s; reply check median 2.68 s (target 2 s missed, slower check accepted by the Programme Sponsor); the classifier on the processor with no graphics memory; 20 of 20 unsafe and 19 of 20 safe test sentences right.

---

# 10. Handover

Future work against this baseline should include:

1. This document, [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] Sections 6A (carried items), 6B and 6C, and [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]] for prior context.
2. **PCB-0001 and Capability Readiness Matrix re-audit** for WP3 to WP6 (EBG-0134 cadence).
3. **The Mac visit** (EBG-0162): the real-Mac checks and the Mac measurements on the new Mac.
4. **Before go-live**: EBG-0171 (household notes reaching a Child unchecked, a design choice), EBG-0172 (backend hardening, go-live WP9), the go-live WPs 7 to 9 (voice provisioning EBG-0167; guides and the "Children and privacy" page EBG-0168, which Claude for a Child waits on; clean-machine first run), and the Claude Console spend-limit check.
5. **The Programme Sponsor's camera priorities**: EBG-0176 (the computer's camera on request, the priority; timing a scope decision for the next planning) and EBG-0177 (home cameras through Home Assistant, required after go-live).
6. Candidates: EBG-0173 (streaming and moderated-turn progress), EBG-0174, EBG-0175, EBG-0170, and the open Dependabot pull requests.
7. The moderation sentence set at `i:\tmp\jarvis-wp6d\` should move somewhere durable and private.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] | Session this baseline is drawn from. |
| [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] | The go-live plan; this session is its Session A. |
| [[WR-ESR0061-002_TECHNOLOGY_AND_SECURITY_LANDSCAPE_REVIEW|WR-ESR0061-002]] | The independent technology and security review, triaged at WP7. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | The session's closures and registrations. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Product capability baseline; re-audit owed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 7 November 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0040, on the Programme Sponsor's direction ("please establish a new baseline"): go-live Session A delivered WP1 to WP6 and the session-wide verification, every product commit gated and independently reviewed. |
