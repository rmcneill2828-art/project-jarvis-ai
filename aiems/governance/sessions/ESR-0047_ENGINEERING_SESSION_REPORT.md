# ESR-0047 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0047 |
| Title | Engineering Session Report |
| Version | 1.2 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0047 |
| Date Opened | 4 August 2026 |
| Date Closed | - |
| Closure Status | Open |

---

# 2. Purpose

This report records the opening and execution of ESR-0047, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] closed (31 July 2026), [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), README.md and PST-0001 both current (no staleness found).

WP0A also found that [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] both still cited RBL-0021 as the current accepted repository baseline in their Related Artefacts/OSE Relationships sections - seven baselines stale (RBL-0022 through RBL-0028 established since each artefact's last correction of this reference at ESR-0036).

The Programme Sponsor selected this session's objective directly: fix the PBK-0001/COC-0001 documentation staleness first as WP1 (Documentation Debt Discipline, matching the established correction pattern recurring since ESR-0029), then investigate [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118 (local Codex CLI state causing `codex exec` invocations to stall indefinitely, first disclosed at ESR-0046 WP6) as WP2.

---

# 4. Engineering Authority

ESR-0047 opening was authorised by direct Programme Sponsor instruction on 4 August 2026, following review of PBK-0001, WP0A repository synchronisation findings, and an explicit objective-selection question covering both the documentation staleness finding and the choice between EBG-0117 (Voice Faculty Increment B) and EBG-0118 (Codex CLI tooling stall) as the session's primary objective.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

WP1: correct the stale RBL-0021 current-baseline references in PBK-0001 and COC-0001 to RBL-0028, per PBK-0001's own Documentation Debt Discipline.

WP2: investigate [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118 (local Codex CLI state, `~/.codex/logs_2.sqlite` at 322 MB plus stale lock files, causing `codex exec` invocations to stall indefinitely) so that WP6 Independent Repository Verification can rely on a real Codex re-review again rather than a reduced-rigour direct substitute.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | Documentation Debt Discipline: correct stale RBL-0021 references in PBK-0001 and COC-0001 to RBL-0028 | Complete |
| WP2 | Investigate and, if possible, resolve EBG-0118 (Codex CLI tooling stall) | Complete |

Further Work Packages will be added if the Programme Sponsor directs the session remain open beyond WP2.

---

# 6A. WP1 - Documentation Debt Discipline: PBK-0001/COC-0001 Stale Baseline References

Approved directly by the Programme Sponsor via an explicit objective-selection question at session open, matching the precedent of prior direct WP0A/WP1 corrections of this exact reference (ESR-0029 through ESR-0036) - a factual citation correction with no design decision, not requiring a full Engineering Implementation Package or Codex design review cycle.

Swept both documents in full for other stale RBL references (Whole-Document Staleness Sweep on Edit) before considering the edit complete - only the live Related Artefacts/OSE Relationships/Session Start Checklist references were stale; all Version History table entries citing earlier RBL numbers are correctly frozen historical record, left unchanged.

- **PBK-0001** (1.34 to 1.35): Related Artefacts and OSE Relationships RBL-0021 references corrected to RBL-0028 (established at ESR-0046 WP7).
- **COC-0001** (1.16 to 1.17): Session Start Checklist, Related Artefacts and OSE Relationships RBL-0021 references corrected to RBL-0028, including the superseding-baseline detail (ESR-0046 WP7, 31 July 2026, superseding RBL-0027, was: ESR-0035 WP5, 25 July 2026, superseding RBL-0020).
- **REG-0001** (3.444 to 3.445): registered ESR-0047 (Open, 1.0); synced PBK-0001 and COC-0001 rows.

Validation: `python scripts/validate_repository.py --governance-only` - 0 errors, 268 warnings (unchanged from the ESR-0046 baseline count; all pre-existing dangling section-heading references, none newly introduced).

Files: `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`, `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/sessions/ESR-0047_ENGINEERING_SESSION_REPORT.md` (new).

---

# 6B. WP2 - Investigate EBG-0118 (Codex CLI Tooling Stall)

Approved directly by the Programme Sponsor via explicit questions at two decision points: first to investigate before attempting new capability work, then, once initial evidence pointed at `~/.codex/config.toml`'s `[windows] sandbox = "elevated"` setting rather than the originally-suspected `logs_2.sqlite` size, to try changing it.

**Baseline state check**: `~/.codex/logs_2.sqlite` still present, 307 MB (was 322 MB at ESR-0046, now actively growing via an accompanying WAL file); the same two lock files from ESR-0046's disclosure still present but confirmed stale - no live Codex process held them (`tasklist`/`ps` showed none running).

**Live reproduction attempts** (four `codex exec -s read-only` invocations against this real repository, each run to completion, none killed early):

1. A minimal prompt with no tool use - 7.6s.
2. A prompt requiring a real single-file read via a `pwsh.exe` exec call - 6.2s.
3. An independent review of the real ESR-0047 WP1 committed diff (`f36a465..9936702`) - 24.5s. During this run, two batches of parallel `git grep <rev> -- <paths>` calls failed with `windows sandbox: runner failed during SpawnChild: CreateProcessAsUserW failed: 1920 (The file cannot be accessed by the system.)` - the previously-disclosed, separate, immediate/explicit sandbox limitation (distinct from EBG-0118's own silent-hang symptom) - while sibling `git diff`/`git status` calls in the same batches succeeded. Codex's own agent loop recovered without hanging and delivered a genuine, evidence-based verdict: **Pass - "the diff touches only governance Markdown artefacts, the live PBK-0001/COC-0001 baseline references changed from RBL-0021 to RBL-0028 with matching ESR/register updates, and I found no changes outside the claimed documentation-only scope."** This stands as a real WP6-equivalent independent review of WP1, an improvement on ESR-0046 WP6's direct-only substitute.
4. After removing `[windows] sandbox = "elevated"` from `~/.codex/config.toml` (backed up first to `~/.codex/config.toml.esr0047-backup`, a full pre-change copy) and re-running the same diff-review test with an explicit instruction to use `git grep` and parallel tool calls: the `CreateProcessAsUserW` spawn crash did not recur, but the same `git grep <rev> -- <paths>` pattern instead failed immediately as "blocked by policy" - a different, still non-hanging failure mode. Codex again recovered, falling back to `git diff --unified=80`, and completed in 46s. This run returned a "Fail" verdict, but that was caused by this session's own over-literal test prompt ("confirm no RBL-0021 references remain in the changed files"), which did not account for Version History rows correctly and deliberately retaining historical RBL-0021 mentions per PBK-0001's Documentation Debt Discipline - Codex's finding was accurate to the letter of the (poorly worded) question asked, not a real defect in WP1.

None of the four runs reproduced EBG-0118's actual disclosed symptom (a 30+ minute hang with no output beyond the initial banner).

**Disclosed conclusion**: inconclusive on EBG-0118 itself, honestly reported as such rather than claimed resolved. The large `logs_2.sqlite` file's role as sole cause is neither confirmed nor disproven - the hang simply did not occur today under either sandbox setting, so there was nothing to observe "fixed." What is new, confirmed evidence: the `[windows] sandbox = "elevated"` setting is linked to a related, previously-known, different failure mode (`CreateProcessAsUserW` spawn crash) that stopped occurring once removed, replaced by an immediate policy rejection rather than a crash or a hang; and `codex exec` is currently usable in practice for real reviews against this repository, including the genuine WP1 Pass verdict obtained above. Full detail, including the updated config's location and backup path, recorded in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0118 (1.152 to 1.153) - left open, Candidate Backlog, since the actual stall was not confirmed fixed.

Files: `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/sessions/ESR-0047_ENGINEERING_SESSION_REPORT.md`. Outside the repository: `~/.codex/config.toml` (edited, `[windows] sandbox = "elevated"` removed), `~/.codex/config.toml.esr0047-backup` (new, pre-change backup).

---

# 7. Related Artefacts

* [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Documentation Debt Discipline guidance followed; WP1 target artefact.
* [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] - WP1 target artefact.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0118 (this session's WP2 objective).
* [[RBL-0028_REPOSITORY_BASELINE|RBL-0028]] - repository baseline at session open.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 4 August 2026 | Claude Engineering Implementer | WP2 Complete: investigated EBG-0118 via four live `codex exec` tests (7.6s-46s each, none reproduced the disclosed 30+ minute hang). Found and disclosed a related `CreateProcessAsUserW` sandbox spawn failure on parallel `git grep` calls; removed `[windows] sandbox = "elevated"` from `~/.codex/config.toml` (backed up) per Programme Sponsor direction, which changed that failure mode without a hang recurring. One test run delivered a genuine, evidence-based Codex Pass review of the real WP1 commit. Net outcome disclosed as inconclusive on EBG-0118's actual stall; EBR-0001 updated (1.152 to 1.153), left open. |
| 1.1 | 4 August 2026 | Claude Engineering Implementer | WP1 Complete: corrected PBK-0001 (1.34 to 1.35) and COC-0001 (1.16 to 1.17) stale RBL-0021 current-baseline references to RBL-0028, registered in REG-0001 (3.444 to 3.445). `validate_repository.py --governance-only` 0 errors, 268 warnings (unchanged pre-existing count). |
| 1.0 | 4 August 2026 | Claude Engineering Implementer | ESR-0047 opened at WP0B, before WP1 began. WP0A found PBK-0001/COC-0001 seven baselines stale on their RBL current-baseline reference. Objective: WP1 fixes that staleness; WP2 investigates EBG-0118 (Codex CLI tooling stall). Both selected by the Programme Sponsor via explicit objective-selection questions. |
