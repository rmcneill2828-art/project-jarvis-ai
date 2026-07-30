# ESR-0045 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0045 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0045 |
| Date Opened | 30 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 complete, further governance WPs to follow per Programme Sponsor direction |

---

# 2. Purpose

This report records the opening and execution of ESR-0045, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] closed (30 July 2026), [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), PBK-0001 confirmed unchanged since last read (still last touched at ESR-0036).

`scripts/session_launcher.py` was run to surface candidate objectives. Presented to the Programme Sponsor: EBG-0065 (STD-0006 Configuration and Secrets Standard, High, Approved), EBG-0115 (Evaluate Kokoro TTS, Low), EBG-0038/0046/0042 (further candidates), and Theme 7's dormant governance debt. **The Programme Sponsor selected EBG-0065 (STD-0006 Configuration and Secrets Standard)**.

EBG-0065's own registration text withholds implementation authority: "No implementation is authorised by this promotion; a future Engineering Implementation Package would still need to be drafted, reviewed and approved." This session's objective is therefore to draft STD-0006 as a new controlled Standard artefact, grounded in the repository's already-established (but never formally documented) configuration/secrets practice, and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval.

---

# 4. Engineering Authority

ESR-0045 opening was authorised by direct Programme Sponsor instruction on 30 July 2026, following review of PBK-0001, README.md, PST-0001 and ESR-0044, confirming [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit objective-selection question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Draft [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0065 (STD-0006 Configuration and Secrets Standard): formalise the repository's already-established configuration/secrets practice (environment-variable-only credential supply, `CredentialReference` indirection, the agent-accessible/Sponsor-only token boundary, local database file conventions, test-isolation requirements) into a new controlled Standard artefact, mirroring [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]]'s structure, and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before the artefact is created.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0065: draft STD-0006 Configuration and Secrets Standard; Codex design review; Programme Sponsor approval | Complete |

The Programme Sponsor has directed that this session remain open for further governance work beyond WP1, rather than closing after a single Work Package - additional WPs will be added to this table as they are scoped. Session-wide Independent Repository Verification and Repository Baseline Determination remain pending until the session's final Work Package.

---

# 6A. WP1 - EBG-0065: STD-0006 Configuration and Secrets Standard

Reviewed `sentinel/provider_config.py`'s `CredentialReference`, a full grep of every `JARVIS_*`/`AIEMS_*`/provider-native environment variable actually in use across `jarvis/`, `sentinel/`, `scripts/`, `scripts/aiems_bridge.py`/`scripts/sponsor_client.py`/`scripts/sponsor_approval_service.py` (the `AIEMS_AGENT_TOKEN`/`AIEMS_SPONSOR_TOKEN` boundary), `.gitignore`'s existing documented rules, and `personal.db`/`sponsor_decisions.db`'s path conventions before drafting scope. Confirmed directly: the repository already follows a consistent, disciplined configuration/secrets practice across every provider adapter and the AIEMS tooling - it had simply never been written down as a controlled Standard.

Produced [[EIP-ESR0045-001_STD0006_CONFIGURATION_AND_SECRETS_STANDARD|EIP-ESR0045-001]] (v0.1, Draft): a new STD-0006, mirroring STD-0004's structure, documenting existing practice only - no code change required, since the codebase already complies.

Submitted to Codex for design review via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern - **v0.1: Fail with findings**. Three blocking findings: (1) "every credential is a `CredentialReference`" was overstated - AIEMS tooling reads its tokens via direct `os.environ.get(name)`, not `CredentialReference`; (2) the "absent credential degrades honestly" rule was too broad - AIEMS approval tooling correctly fails closed rather than degrading; (3) Section 8's token-boundary wording inaccurately implied no code path may "accept" `AIEMS_SPONSOR_TOKEN`, when `sponsor_approval_service.py` necessarily reads/validates it as the authority itself - the real boundary is about which processes may possess the token, not which service checks it.

**v0.2 revision**: reworded credential-reference language throughout to "`CredentialReference` or an equivalent named-environment-variable indirection"; split credentials into optional-capability (degrade honestly) versus authority-bearing (fail closed) categories; corrected Section 8 to state the boundary as process-possession, explicitly permitting `sponsor_approval_service.py` to read/validate the Sponsor token as the authority it protects. Resubmitted to Codex - **v0.2/v0.3: Pass**, all three findings confirmed adequately addressed (one minor non-blocking note on the Compliance Checklist's wording, explicitly not treated as blocking).

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service before implementation began.

**Implemented exactly as scoped.** `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` (new) created directly at Approved/1.0, matching how STD-0001 through STD-0004 were each created and approved together rather than Draft-then-promoted - appropriate here since this standard documents pre-existing, already-followed practice rather than proposing new, untested rules. No `jarvis/`, `sentinel/`, or `scripts/` file touched.

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0065 marked Completed. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]: EBG-0065 marked Resolved/Delivered in Section 7.1 and Section 7.4 - a minor, directly necessary dependency discovered during implementation, not in the EIP's original Authorised Files list, disclosed rather than silently expanded (matching the `src/styles.css` precedent from ESR-0044).

- Files: `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` (new), `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md` (discovered dependency), [[EIP-ESR0045-001_STD0006_CONFIGURATION_AND_SECRETS_STANDARD|EIP-ESR0045-001]] (new).
- `python -m pytest`: no regression expected (no code touched); to be confirmed at validation.
- `python scripts/validate_repository.py` (full mode): to be confirmed at validation.
- Committed and pushed to `origin/main` (SHA reported at closure).

---

# 7. Related Artefacts

* [[ESR-0044_ENGINEERING_SESSION_REPORT|ESR-0044]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0065 (this session's objective).
* [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] / [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] - structural precedent for the new standard.
* [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] - repository baseline at session open.
* [[EIP-ESR0045-001_STD0006_CONFIGURATION_AND_SECRETS_STANDARD|EIP-ESR0045-001]] - this session's WP1 deliverable, Codex design-reviewed (v0.1 Fail with findings, v0.2/v0.3 Pass) and Programme Sponsor-approved via the real Sponsor Approval Service.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 30 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0065 (STD-0006 Configuration and Secrets Standard) resolved via EIP-ESR0045-001 (Codex design review: v0.1 Fail with findings on three overstated/inaccurate credential-handling claims, v0.2/v0.3 Pass after correction). STD-0006 created directly at Approved/1.0, formalising already-established practice - no code changed. Session kept open per Programme Sponsor direction for further governance work beyond WP1. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | ESR-0045 opened at WP0B, before WP1 began. Objective: draft STD-0006 (Configuration and Secrets Standard, EBG-0065), producing an Engineering Implementation Package for Codex review and Programme Sponsor approval before the artefact is created. |
