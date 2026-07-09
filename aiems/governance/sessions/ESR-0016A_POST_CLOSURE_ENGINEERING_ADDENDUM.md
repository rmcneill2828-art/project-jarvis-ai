# ESR-0016A - Post-Closure Engineering Addendum

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0016A |
| Title | Post-Closure Engineering Addendum - Governance and Tooling Improvements |
| Version | 0.3 |
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
| WP2 | One-command version-bump tool to replace the three-touch REG-0001 mirror pattern | Complete (built and sanity-tested; real usage proof deferred to WP4/WP5) |
| WP3 | Extend validator to check internal section-number cross-references | Complete (warning-only, 6 documented residual false positives accepted) |
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

# 5. WP2 - Version-Bump Tool

**Approved EIP:** one command to sync an artefact's own version fields, its REG-0001 row, and REG-0001's own self-row/version, given a required `--summary`; mechanical only, no auto-generated prose.

**Delivered:** `scripts/bump_version.py`, reusing `validate_repository.py`'s existing parsing functions (`parse_register_rows`, `find_registered_file`, `extract_document_version`) rather than duplicating logic.

**Validation:**
- Dry-run sanity check (`plan_bump()` called directly, no `write_text`) against real content (GDE-0001, a genuine registered artefact) surfaced a real bug: the version-badge regex's `\s*$` was consuming the following blank line, silently collapsing spacing. Fixed to `[ \t]*$` (same-line trailing whitespace only); re-verified clean.
- Error paths verified: an unregistered artefact ID and a no-op (already-current) version both refuse cleanly with exit code 1 and no file writes - confirmed via `git status` showing no changes.
- `pytest` 144/144 (no product code touched); `scripts/validate_repository.py` clean throughout.
- Real end-to-end proof (an actual controlled-artefact edit, not a dry run) deferred to WP4 and WP5 below, both of which edit registered artefacts (PBK-0001, COC-0001) and will use this tool for their own version sync - consistent with what the approved EIP anticipated, since WP2/WP3 alone don't touch a REG-0001-registered artefact.

**Self-review:** scope held to the approved mechanical behaviour; no prose auto-generated; the one bug found was fixed before any real usage, not discovered later on live content.

---

# 6. WP3 - Section-Reference Cross-Check

**Approved EIP:** warn when a "Section N" reference doesn't resolve to a heading, in the current document or an immediately-adjacent linked one; heuristic, not exhaustive; run against the full repository and triage every hit rather than a synthetic test.

**Delivered:** `check_section_references` in `scripts/validate_repository.py`. Excludes `aiems/History/` (HST/FCH) entirely - frozen chat transcripts reference "Section N" in conversational, not structural, ways and would otherwise dominate the output with noise.

**Validation, run against the full repository as required:**

- Two genuine bugs found and fixed before considering this done: (1) the adjacency check used `.search()` within a lookback window, returning the *first* WikiLink found rather than the one truly immediately adjacent, misattributing references on lines mentioning multiple artefacts; (2) a table-row fallback attempt split rows naively on the pipe character, which breaks because a double-bracket WikiLink's own display-text separator is also a literal pipe, silently misaligning cells.
- One heuristic extension (fall back to a table row's first-cell link when nothing else is adjacent) was tried, found to fix one case while introducing five new false positives - because this repository's Related Artefacts tables predominantly describe *the current document's own* sections in relation to the linked artefact, not the linked artefact's sections - and was reverted rather than kept as a net-negative change.
- Detection confirmed: a deliberately injected reference to a fake, non-existent section number was caught, then cleanly reverted via `git checkout --` with no residual test content (`git status` confirmed).
- **6 residual false positives remain**, all sharing one root cause: an artefact mentioned in prose without being immediately adjacent to the "Section N" text (e.g. mentioned one clause earlier, or in an earlier table row of the same block). Listed in full in the Programme Sponsor decision below. Warning severity specifically absorbs this known limitation.
- `pytest` 144/144 throughout (no product code touched); `validate_repository.py` reports 0 errors, 6 warnings (all the documented residual cases) in the current repository state.

**Programme Sponsor decision:** accept the 6 residual false positives as a documented limitation rather than scope down to same-document-only checking (which would eliminate them but also stop catching genuine cross-document breaks like the EE-0001/ESR-0016 mutual-reference pattern this check is partly meant to protect). Residual false positives, all "artefact mentioned in prose without immediate adjacency to the Section reference":
  - `REG-0001:276`, `ESR-0016:164` (x2), `ESR-0016:192`, `ESR-0016A:80`, `EE-0001:223`.

**Self-review:** scope held to `validate_repository.py` only; the reverted heuristic left no dead code; every claim above independently re-verified by re-running the full validator, not assumed from the design discussion.

---

# 7. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Parent closed engineering session; Section 16 raised the reflective question this addendum answers. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Precedent for post-closure engineering addenda. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Amended by WP1; target of planned WP4. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Target of planned WP5. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current repository baseline preserved by this addendum. |
| `scripts/bump_version.py` | New tool created by WP2; will be used for WP4/WP5's own version syncs. |
| `scripts/validate_repository.py` | Extended by WP1 and WP3. |

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 9 July 2026 | Claude Engineering Reviewer | Completed WP3 (section-reference cross-check): found and fixed two real bugs (wrong-match adjacency lookup, WikiLink-pipe table misparse); tried and reverted a table-row heuristic that fixed one case but broke five others; confirmed detection on an injected broken reference; Programme Sponsor accepted 6 residual false positives as a documented limitation rather than scoping down to same-document-only checking. |
| 0.2 | 9 July 2026 | Claude Engineering Reviewer | Completed WP2 (version-bump tool): `scripts/bump_version.py` created, reusing existing validator parsing functions. Dry-run sanity check against real content (GDE-0001) found and fixed a blank-line-swallowing regex bug before any real usage. Error paths (unregistered artefact, no-op version) verified to refuse cleanly with no partial writes. Real end-to-end proof deferred to WP4/WP5. |
| 0.1 | 9 July 2026 | Claude Engineering Reviewer | Opened ESR-0016A. Completed WP1 (pre-commit hook visibility): validator now warns when the tracked hook is inactive; PBK-0001 WP0A checklist updated; verified in both states. |
