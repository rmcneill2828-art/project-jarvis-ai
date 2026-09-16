# EIP-ESR0058-001 - Engineering Reviewer Re-appointment

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0058-001 |
| Title | Engineering Implementation Package: WP2 Engineering Reviewer Re-appointment |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0058 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0058 WP2, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0126: retire ChatGPT/Codex as the permanent Engineering Reviewer (confirmed retired on cost grounds at ESR-0057 WP1, not merely unavailable) and appoint GitHub Copilot CLI in its place.

WP1 (this session) established the technical prerequisite this package assumes: a scoped, non-interactive `copilot -p ... --allow-tool='shell(git:*)' --allow-tool='shell(python:*)' --deny-tool='write'` invocation completed a genuine post-commit review task correctly and in full - confirming the exact commit range, the exact four-file changed-set, the specific content of the diff (including two named materially-stale rows), and a fresh `validate_repository.py` run - without triggering Claude Code's `Create Unsafe Agents` classifier, unlike a same-session Antigravity CLI attempt using its blanket `--dangerously-skip-permissions` flag.

---

# 3. Repository Context Investigated

* [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] Engineering Reviewer section - the binding appointment statement ("ChatGPT is currently the permanent holder of this role, per the EE-0001 Section 7 appointment").
* [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7 - the original appointment mechanism. Confirmed this is a frozen historical trial record (OSE-0001) that should not itself be rewritten; COC-0001 is the standing-governance artefact that records the current holder and is the correct edit target.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - searched for an equivalent Reviewer-appointment binding statement; found none. PBK-0001 binds only the Engineering Implementer role (Claude); the Reviewer appointment lives solely in COC-0001. No PBK-0001 edit required for the appointment itself.
* [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] Section 7 - the role-terminology lookup table. Confirmed this maps naming conventions across time periods (COC-0001/EE-0001/Historical), not which tool currently holds a role - no edit required.
* `scripts/aiems_bridge.py` and `scripts/tests/test_aiems_bridge.py` - full read. Confirmed `codex` was hardcoded as the Reviewer's transcript identity (`sender`/`recipient` fields), exchange directory names (`.aiems-exchange/codex/inbox`, `/outbox`), and a preflight check (`shutil.which("codex")`, `codex login status`) - not a config value, genuine code-level role-locking (EBG-0057's own security property).

---

# 4. Scope

## 4A. Governance re-appointment

[[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] Engineering Reviewer section updated: records ChatGPT/Codex's tenure (10 July 2026 EE-0001 Section 7 appointment to 14 September 2026 confirmed retirement) and GitHub Copilot CLI's appointment as the new permanent holder (16 September 2026, this Work Package), citing the WP1 feasibility finding as the basis for confidence the tool can genuinely fill the role from within this environment.

## 4B. Bridge role-identity generalisation

`scripts/aiems_bridge.py`:

* New constants `REVIEWER_TOOL_ENV_VAR = "AIEMS_REVIEWER_TOOL"`, `DEFAULT_REVIEWER_TOOL = "copilot"`.
* `sender`/`recipient` fields and exchange directory names changed from the vendor-named `"codex"` to the role-based `"reviewer"` throughout `ensure_layout`, `cmd_submit_to_review`, `cmd_return_findings` - matching the role-definition-not-vendor-name principle already established elsewhere in this project's governance (COC-0001/PBK-0001 already describe roles this way; the bridge's internal implementation had drifted from it).
* `run_preflight()` reads the reviewer tool name from `AIEMS_REVIEWER_TOOL` (default `copilot`) instead of hardcoding `"codex"`.
* **Disclosed simplification**: the Codex-specific `codex login status` preflight check is removed rather than generalised - no equivalent one-liner exists across reviewer tools, and `"claude"` receives no equivalent authentication check either. Preflight now holds both identities to the same bar: binary present on PATH, `--version` runs successfully.
* Docstrings and CLI help text updated from "Codex" to "the Engineering Reviewer" throughout, matching the module's own stated role-based design.

## 4C. Test updates

`scripts/tests/test_aiems_bridge.py`: all `"codex"`-identity assertions updated to `"reviewer"`; the Windows-shell-shim test updated to assert against `bridge.DEFAULT_REVIEWER_TOOL` and to confirm no `login`-subcommand call occurs; a new test confirms `AIEMS_REVIEWER_TOOL` genuinely overrides which binary preflight checks for.

## 4D. Explicitly out of scope

* No change to the Engineering Implementer role or the `"claude"` identity - Claude remains the unchanged holder of that role; renaming it now would be an unrelated, unrequested change.
* No change to `EE-0001`'s own historical trial record - frozen per OSE-0001, referenced but not rewritten.
* No change to PBK-0001 - confirmed to hold no Reviewer-appointment binding of its own.
* No attempt to make `run_preflight()`'s tool-presence check itself configurable beyond the single `AIEMS_REVIEWER_TOOL` env var - a fuller multi-reviewer-tool abstraction is not scoped here.

---

# 5. Validation Requirements

* `python -m pytest jarvis/tests scripts/tests -q` - full suite.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* A real functional smoke test of `cmd_init`/`cmd_submit_to_review`/`cmd_return_findings` against a real (non-mocked) temporary directory, confirming the renamed `reviewer/inbox`/`reviewer/outbox` layout is created and populated correctly - not merely asserted via unit-test mocks.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* COC-0001 accurately records GitHub Copilot CLI as the current permanent Engineering Reviewer, with ChatGPT/Codex's tenure and retirement both disclosed rather than silently erased.
* `scripts/aiems_bridge.py` contains no remaining vendor-named (`codex`) identity in its transcript/directory logic - only the role-based `reviewer` identity, plus historically-accurate prose references to Codex's past tenure.
* Full test suite passes; `validate_repository.py` remains clean.
* A genuine `copilot`-driven design review of this very package is obtained and recorded, closing the loop on WP1's feasibility finding.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary directly. Implemented exactly as drafted at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 16 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation, routed through the real bridge (`ESR-0058`/`WP2`) - **Pass**: independently confirmed COC-0001's wording discloses rather than erases Codex's history, no vendor-named `codex` string remains in any `aiems_bridge.py` code path, the test suite exercises actual renamed behaviour, full suite (562 passed/1 skipped) and `validate_repository.py` (0 errors) both re-run independently, no scope creep. This is the first genuine end-to-end use of the renamed `reviewer` identity - Copilot CLI's own `return-findings` call landed for real (`sender: reviewer`), independently verified against the transcript and the new `.aiems-exchange/reviewer/outbox/` directory. Not yet approved or implemented/committed. |
| 0.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP2 draft. Bridge role-identity generalised (`codex` to `reviewer`, `AIEMS_REVIEWER_TOOL` env var added); COC-0001 re-appointment wording drafted. Not yet reviewed, approved or implemented/committed. |
