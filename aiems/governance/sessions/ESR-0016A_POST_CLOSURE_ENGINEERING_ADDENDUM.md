# ESR-0016A - Post-Closure Engineering Addendum

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0016A |
| Title | Post-Closure Engineering Addendum - Governance and Tooling Improvements |
| Version | 0.1 |
| Status | In Progress |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Parent Session | [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] |
| Repository Baseline | [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] |
| Classification | Internal |
| Date Opened | 9 July 2026 |

---

# 2. Executive Summary

Following ESR-0016 closure, the Programme Sponsor asked the Engineering Reviewer to reflect on how easy AIEMS was to follow during the session, and approved five resulting improvement recommendations for implementation.

This work is folded into ESR-0016 closure as a post-closure addendum rather than opening ESR-0017, consistent with the [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] precedent: these are governance/tooling improvements, not JARVIS engineering work, and ESR-0017 is reserved as the EE-0001 Cold Start Validation Session, which requires a fresh conversation to be a meaningful test. Doing this work here preserves both ESR-0016's closure and ESR-0017's validity.

Each work package below is executed against its own approved Engineering Implementation Package, per PBK-0001.

---

# 3. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP1 | Pre-commit governance hook visibility - warn when `core.hooksPath` is not configured | Complete (this update) |
| WP2 | One-command version-bump tool to replace the three-touch REG-0001 mirror pattern | Not started |
| WP3 | Extend validator to check internal section-number cross-references | Not started |
| WP4 | Standing PBK-0001 rule: no reporting a repository operation's outcome without invoking it and observing the result | Not started |
| WP5 | Formalise the report-authorship exception (Reviewer maintaining the session report under Lead tooling constraints) in COC-0001 | Not started |

---

# 4. WP1 - Pre-commit Hook Visibility

**Approved EIP:** detect whether `core.hooksPath` is configured to `scripts/hooks`; warn (not fail) if not, since CI remains the ultimate backstop; add the check to PBK-0001's WP0A checklist.

**Delivered:**

- `scripts/validate_repository.py`: added `check_precommit_hook_installed`, wired into `run_validation`. Verified empirically in both states - warns when unconfigured, silent when configured.
- `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md` (1.15 to 1.16): added hook-activity confirmation to the WP0A checklist.
- `scripts/README.md`: cross-referenced the new check in the validator's description.
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`: registered PBK-0001's version bump (the newly-activated hook itself caught this mismatch before commit - a live demonstration of WP1 working).

**Validation:** 144/144 tests passing (docs/script change only, no product code touched); `python scripts/validate_repository.py` clean with 0 errors, 0 warnings, `core.hooksPath` now configured on this machine.

**Self-review:** scope held to the approved files; no validator behaviour changed beyond the new warning; no existing check weakened.

---

# 5. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Parent closed engineering session; Section 16 raised the reflective question this addendum answers. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Precedent for post-closure engineering addenda. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Amended by WP1; target of planned WP4. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Target of planned WP5. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current repository baseline preserved by this addendum. |

---

# 6. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 9 July 2026 | Claude Engineering Reviewer | Opened ESR-0016A. Completed WP1 (pre-commit hook visibility): validator now warns when the tracked hook is inactive; PBK-0001 WP0A checklist updated; verified in both states. |
