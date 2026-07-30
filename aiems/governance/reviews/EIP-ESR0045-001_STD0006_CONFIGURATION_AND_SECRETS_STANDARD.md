# EIP-ESR0045-001 - STD-0006 Configuration and Secrets Standard

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0045-001 |
| Artefact ID | EIP-ESR0045-001 |
| Title | STD-0006 Configuration and Secrets Standard |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0065 |
| Intended Session | ESR-0045 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0065 was explicitly named and scoped during the initial project bootstrapping conversation ("prevent configuration drift, and protect sensitive information"), sequenced alongside STD-0003 through STD-0008 in a proposed standards roadmap, but never created. Promoted to Approved Backlog at ESR-0034 WP1 on the basis that the condition it was originally parked pending - real credential references and credential-gated live routes existing in the codebase - is now satisfied. Its own registration text withholds implementation authority: "a future Engineering Implementation Package would still need to be drafted, reviewed and approved." This package is that draft.

Confirmed directly against the live repository before drafting (not assumed): the project already follows a consistent, disciplined configuration/secrets practice across every provider adapter, the AIEMS Exchange Bridge and the Sponsor Approval Service - it has simply never been written down as a controlled Standard. This package formalises existing, working practice; it does not invent new rules the codebase does not already follow.

---

# 3. Objective

Create STD-0006 (Configuration and Secrets Standard) as a new controlled Standard artefact, mirroring [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]]'s structure (per [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]]'s mandatory sections), documenting the environment-variable-only credential model, the `CredentialReference` indirection pattern, the agent-accessible/Sponsor-only token security boundary, local database file conventions, and test-isolation requirements already in live use.

---

# 4. Repository Context

| Item | Current State (confirmed directly, not assumed) |
|------|----------------|
| `sentinel/provider_config.py` `CredentialReference` | A frozen dataclass holding only an `environment_variable` name - used by JARVIS provider adapters (`OPENAI_API_KEY`, `GEMINI_API_KEY`). AIEMS tooling (`scripts/aiems_bridge.py`, `scripts/sponsor_client.py`, `scripts/sponsor_approval_service.py`) reads its tokens via a direct `os.environ.get(name)` call by name, not through `CredentialReference` - both are equally "named-reference-only," but the mechanism differs between subsystems, confirmed directly rather than assumed uniform. No secret value is ever held in a `ProviderConfiguration` object, in source, or in a committed file, in either case. |
| Environment variables in live use (direct grep across `jarvis/`, `sentinel/`, `scripts/`) | `AIEMS_AGENT_TOKEN`, `AIEMS_SPONSOR_DB_PATH`, `AIEMS_SPONSOR_TOKEN`, `AIEMS_SPONSOR_URL`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `JARVIS_HEARTBEAT_INTERVAL_SECONDS`, `JARVIS_MEMORY_DB_PATH`, `JARVIS_OLLAMA_ENDPOINT`, `JARVIS_OLLAMA_MODEL`, `JARVIS_PIPER_VOICE_PATH`, `JARVIS_PRIMARY_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL` - a real, consistent `JARVIS_*`/`AIEMS_*`/provider-native (`OPENAI_*`/`GEMINI_*`) naming convention already in force, never documented. |
| `scripts/aiems_bridge.py` / `scripts/sponsor_approval_service.py` / `scripts/sponsor_client.py` | A genuine, load-bearing security boundary already exists in code: `aiems_bridge.py` (agent-side) reads only `AIEMS_AGENT_TOKEN`/`AIEMS_SPONSOR_URL` and does not read `AIEMS_SPONSOR_TOKEN` at all; `sponsor_client.py` (Sponsor-side only, run from the Programme Sponsor's own host-side terminal, never from an agent-reachable environment) reads `AIEMS_SPONSOR_TOKEN` to submit a decision; `sponsor_approval_service.py` (the server-hosted authority) necessarily reads and validates `AIEMS_SPONSOR_TOKEN` against incoming requests, since it is the service the boundary protects - the boundary is about which *processes possess* the token (never an agent-reachable one), not about which service is allowed to check it. Both `sponsor_approval_service.py` and `sponsor_client.py` fail closed (refuse to run) if their required token is missing - confirmed directly, not assumed. This is currently enforced by convention and code comments, not by a controlled Standard. |
| `.gitignore` | Already documents (in comments) the exact rules this standard formalises: `.env`/`.env.*` ignored because "every credential in this codebase is a `CredentialReference` to an environment variable name, never a value in source" (confirmed by external security review, 19 July 2026, EBG-0088/ESR-0033 WP4); `.aiems-exchange/` ignored, with `scripts/aiems_bridge.py` additionally restricting filesystem permissions on POSIX (EBG-0086, ESR-0033 WP4, disclosed as not enforced on Windows). |
| Local database files | `personal.db` (`jarvis/interfaces/stdio_rpc.py` `DEFAULT_MEMORY_DB_PATH = Path.home() / ".jarvis" / "memory" / "personal.db"`, overridable via `JARVIS_MEMORY_DB_PATH`) and `sponsor_decisions.db` (`scripts/sponsor_approval_service.py` `DEFAULT_DB_PATH = REPO_ROOT / ".aiems-exchange" / "sponsor_decisions.db"`, overridable via `AIEMS_SPONSOR_DB_PATH`) - both local-only, never committed, both already overridable for test isolation. |
| Test isolation convention | `jarvis/tests/test_stdio_rpc.py`'s own code comments state the exact rationale already: tests must never depend on, or accidentally exercise, real credentials or real local databases "on whatever machine runs the suite" - every test passes an explicit `environ` mapping and a `tmp_path`-scoped database path, a pattern ESR-0026 WP1 established after a real test-isolation defect (a shared Ollama test helper making real network calls). |

---

# 5. Scope

This package authorises creating `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` as a new controlled Standard, with the following content (verbatim subject to Codex/Programme Sponsor review), mirroring STD-0004's approved structure per STD-0001's mandatory sections (Document Control, Purpose, Scope, Main Content, Version History):

```text
# STD-0006 - Configuration and Secrets Standard

> "A credential that never appears in source code cannot leak from source
> control."

**Version:** 1.0

---

# 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | STD-0006 |
| Title | Configuration and Secrets Standard |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | Triggered |
| Effective Date | Pending approval |
| Next Review | As Required |

---

# 2. Purpose

STD-0006 defines the configuration and secrets standard for Project JARVIS AI.

It answers the primary configuration question:

> How does Project JARVIS AI supply credentials, endpoints and other
> environment-specific configuration to engineering deliverables without
> ever committing a secret value to source control?

This standard formalises configuration and secrets practice already in
live use across this repository - it does not introduce new rules the
codebase does not already follow.

---

# 3. Scope

This standard applies to:

- credentials (API keys, tokens) supplied to any provider adapter, script
  or service;
- environment-variable-based configuration (models, endpoints, timeouts,
  file paths);
- local database files and other locally-persisted runtime state;
- test isolation from real credentials and real local state.

This standard does not define provider selection logic, Sentinel policy
content, or the specific value of any credential - only how configuration
and secrets are supplied, named and protected.

---

# 4. Relationship to AIEMS

STD-0006 forms part of the AI Engineering Management System.

AIEMS defines the governance framework for Project JARVIS AI. This
standard defines the configuration and secrets expectations that keep
credentials out of source control and configuration drift bounded.

Where conflict exists, approved AIEMS governance artefacts and Programme
Sponsor decisions take precedence.

---

# 5. Configuration and Secrets Principles

Configuration and secrets handling shall follow these principles:

- No secret value shall ever appear in source code, a committed file, or
  a controlled artefact.
- Every credential is a named environment variable, referenced by name
  only - either via `CredentialReference` (`sentinel/provider_config.py`,
  used by JARVIS provider adapters) or an equivalent direct
  `os.environ.get(name)` read by name only (used by the AIEMS Exchange
  Bridge and Sponsor Approval Service tooling) - never a value held in a
  configuration object, dataclass default, or test fixture.
- Two distinct failure postures apply depending on what the credential
  gates (Section 6 defines both): an absent optional-capability
  credential (e.g. a JARVIS text-generation or Voice provider) degrades
  honestly to its next fallback; an absent authority-bearing credential
  (e.g. an AIEMS approval-service token) fails closed - refusing to
  proceed, not falling back to a weaker check.
- Test suites shall never depend on, or accidentally exercise, real
  credentials or real local state present on the host machine running
  the suite.

---

# 6. Credential Handling Requirements

1. A credential shall be represented in code only as a `CredentialReference`
   or an equivalent named-environment-variable indirection - never as a
   literal string value, even a placeholder that could be mistaken for
   real.
2. A component requiring a credential shall read it via `os.environ` (or
   an injected `environ` mapping in tests) at the point of use, never
   store it in a class attribute, log line, diagnostic event, or audit
   record.
3. This standard distinguishes two credential categories, each with its
   own required failure posture:
   - **Optional-capability credentials** (e.g. `OPENAI_API_KEY`,
     `GEMINI_API_KEY`, `JARVIS_PIPER_VOICE_PATH`) gate an optional runtime
     capability with a defined fallback. Where absent or blank, the
     component shall degrade to its next honest fallback (a lower-priority
     provider, `not_connected`, or equivalent) rather than fail startup or
     fabricate a result - matching `_build_real_provider()` and
     `_build_speech_provider()`'s established pattern in
     `jarvis/interfaces/stdio_rpc.py`.
   - **Authority-bearing credentials** (e.g. `AIEMS_AGENT_TOKEN`,
     `AIEMS_SPONSOR_TOKEN`) gate an engineering-authority decision with no
     safe fallback. Where absent or blank, the component shall fail
     closed - refusing to proceed - matching
     `scripts/sponsor_approval_service.py` and `scripts/sponsor_client.py`'s
     established behaviour (both refuse to run without their required
     token). A missing authority-bearing credential shall never be
     treated as "capability unavailable, continue anyway."
4. A present-but-blank non-credential configuration value (e.g. a model
   name) shall fall through to its documented default, not silently
   propagate an empty string into a downstream constructor that would
   reject it.

---

# 7. Environment Variable Naming Convention

Environment variables shall use one of the following prefixes,
consistent with existing repository practice:

| Prefix | Scope | Examples |
|--------|-------|----------|
| `JARVIS_` | JARVIS backend runtime configuration (models, endpoints, timeouts, file paths, feature-specific paths) | `JARVIS_OLLAMA_MODEL`, `JARVIS_MEMORY_DB_PATH`, `JARVIS_PIPER_VOICE_PATH`, `JARVIS_PRIMARY_PROVIDER` |
| `AIEMS_` | AIEMS engineering tooling (the Exchange Bridge, Sponsor Approval Service) | `AIEMS_AGENT_TOKEN`, `AIEMS_SPONSOR_TOKEN`, `AIEMS_SPONSOR_URL`, `AIEMS_SPONSOR_DB_PATH` |
| Provider-native | Third-party provider SDK/API conventions, used as-is rather than reprefixed | `OPENAI_API_KEY`, `OPENAI_MODEL`, `GEMINI_API_KEY`, `GEMINI_MODEL` |

A new environment variable shall use the prefix matching its actual
scope - a new JARVIS backend setting shall not be given an `AIEMS_`
prefix, and vice versa.

---

# 8. Agent-Accessible vs Sponsor-Only Credential Boundary

Some credentials govern a hard authority boundary between AI engineering
collaborators (Claude, Codex) and the Programme Sponsor. The boundary is
about which *processes may possess* a token, not which service checks it
- the Sponsor Approval Service itself necessarily reads and compares
against `AIEMS_SPONSOR_TOKEN`, since it is the authority the boundary
protects:

- `AIEMS_AGENT_TOKEN` is the agent-facing token. `scripts/aiems_bridge.py`
  (run from an environment an AI collaborator's own tool calls can reach)
  reads only `AIEMS_AGENT_TOKEN` and `AIEMS_SPONSOR_URL` - it does not
  read `AIEMS_SPONSOR_TOKEN` at all.
- `AIEMS_SPONSOR_TOKEN` shall never be set in, or readable from, an
  environment an AI collaborator's own tool calls can reach.
  `scripts/sponsor_client.py` (the only tool that supplies it as a
  decision, via the Programme Sponsor's own host-side terminal) and
  `scripts/sponsor_approval_service.py` (the server-hosted authority that
  validates it against incoming approval requests) are the only two
  processes that shall ever hold this token.
- This boundary is a security control, not a convenience distinction - a
  future capability that appears to need an AI-collaborator-reachable
  process to possess `AIEMS_SPONSOR_TOKEN` is a signal that the
  capability's design crosses this boundary and needs its own explicit
  Programme Sponsor decision, not a workaround.

---

# 9. Local Data and Database File Requirements

1. A locally-persisted runtime data file (e.g. `personal.db`,
   `sponsor_decisions.db`) shall never be committed to the repository.
2. Its default path shall live outside the repository working tree where
   practical (e.g. under the user's home directory) or under an
   already-`.gitignore`d repository-local directory (e.g.
   `.aiems-exchange/`) where a working-tree-relative default is more
   appropriate.
3. Its path shall be overridable via a named environment variable
   following Section 7's convention, so tests and alternate deployments
   never depend on the default location.
4. Where filesystem permission hardening is available (POSIX), it should
   be applied at creation; where it is not available (Windows), that
   limitation shall be disclosed, not silently assumed equivalent.

---

# 10. Test Isolation Requirements

1. Automated tests shall never rely on `os.environ`'s real, ambient state
   - every test that depends on configuration shall pass an explicit
   `environ` mapping (even an empty one) rather than defaulting to the
   real environment.
2. Automated tests shall never read or write a real local database file
   at its default path - every test shall use a `tmp_path`-scoped (or
   equivalent) override.
3. A test helper shared across multiple tests (e.g. a provider construction
   helper) shall itself be test-isolated, not merely relied upon to be
   called correctly by each test - the exact defect class ESR-0026 WP1
   found and fixed for a shared Ollama test helper.

---

# 11. .gitignore Requirements

1. `.env` and `.env.*` shall remain permanently ignored, as a standing
   guard against an accidental commit, even though no `.env` file is
   expected to exist in this repository's working practice.
2. Any new local-only working directory analogous to `.aiems-exchange/`
   shall be added to `.gitignore` at the point it is introduced, with a
   comment explaining what it holds and why it is excluded - matching
   the existing disclosed pattern, not a bare, unexplained ignore entry.

---

# 12. Compliance Checklist

| Check | Result |
|-------|--------|
| No secret value appears in source code, a committed file, or a controlled artefact. | Pass / Fail / N/A |
| Every credential is represented as a named-environment-variable reference, not a literal value. | Pass / Fail / N/A |
| An absent/blank credential degrades honestly rather than failing startup or fabricating a result. | Pass / Fail / N/A |
| A new environment variable uses the correct prefix for its scope (Section 7). | Pass / Fail / N/A |
| No process reachable by an AI collaborator's own tool calls possesses or reads `AIEMS_SPONSOR_TOKEN`. | Pass / Fail / N/A |
| An absent authority-bearing credential (e.g. an AIEMS approval-service token) fails closed, never degrades to a weaker check. | Pass / Fail / N/A |
| A new local database/data file is never committed, has an overridable path, and is `.gitignore`d with an explanatory comment. | Pass / Fail / N/A |
| New or affected tests pass an explicit `environ`/`tmp_path` override rather than depending on ambient host state. | Pass / Fail / N/A |

---

# 13. Maintenance Requirements

STD-0006 shall remain concise and delivery-focused.

It shall not become a general security policy document beyond
configuration and secrets handling.

This standard shall be reviewed when configuration/secrets practice
changes materially (a new credential category, a new local-data pattern,
or a change to the agent/Sponsor token boundary), or when a security
review finding requires an updated rule.

---

## OSE Relationships

| Artefact | OSE Relationship |
|----------|------------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective relationship-only enrichment rule applied to this standard. |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Defines software engineering expectations this standard's configuration/secrets rules extend. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Records authoritative artefact identity, ownership, status and current version. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Records current programme readiness and approved position. |
| [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] | Current accepted repository baseline at this standard's creation. |

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines controlled artefact structure this standard follows. |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Software engineering expectations this standard extends into configuration/secrets territory specifically. |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Structural precedent this standard's sections mirror. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Operational engineering behaviour; Approval Before Change discipline this standard's credential-handling rules operate within. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status. |
| [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] | Current accepted repository baseline context. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial Configuration and Secrets Standard created for Project JARVIS AI, formalising already-established repository practice (EBG-0065, ESR-0045). |
```

---

# 6. Authorised Files

1. `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` (new)
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
4. `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md` - discovered during implementation (two existing EBG-0065 references needed resolution updates), disclosed in Section 12 rather than silently expanded.

No other file is authorised unless a dependency is discovered during validation and explicitly reported. No source code (`jarvis/`, `sentinel/`, `scripts/`) is authorised to change - this package documents already-existing, already-followed practice; it does not itself require any code to be brought into compliance, since the codebase already complies (confirmed directly in Section 4).

---

# 7. Implementation Requirements

1. STD-0006 shall be created directly at Approved status, version 1.0 - matching STD-0001 through STD-0004's own creation pattern (each was created and approved together, not created Draft and later separately promoted), since this package documents pre-existing practice rather than proposing new, untested rules.
2. Every concrete claim in STD-0006 (env var names, file paths, the agent/Sponsor token boundary) must be traceable to the live code cited in Section 4 - no invented convention not already followed.
3. EBG-0065 shall be marked Complete, recording STD-0006's creation.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to `jarvis/`, `sentinel/`, or `scripts/` source code - the codebase already complies with the practice this standard documents.
2. Any new credential, environment variable, or configuration mechanism - this package documents existing practice only.
3. Any change to the `AIEMS_AGENT_TOKEN`/`AIEMS_SPONSOR_TOKEN` security boundary itself - Section 8 records the boundary as it already exists in `scripts/aiems_bridge.py`/`scripts/sponsor_client.py`/`scripts/sponsor_approval_service.py`.
4. Any change to `.gitignore` - Section 11's rules already match the current file exactly.

---

# 9. Constraints

1. No STD-0006 file shall be created until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0044.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors, and specifically confirms STD-0006 is correctly registered in REG-0001 with a matching version.
2. Every WikiLink in STD-0006 resolves to a real, existing artefact.
3. No unauthorised files changed - specifically, no `jarvis/`, `sentinel/`, or `scripts/` file touched.

`python -m pytest` is not expected to change (no code touched) but should be re-run to confirm no regression, consistent with PBK-0001's Operational Verification Before Reporting.

---

# 11. Risks and Dependencies

## Dependencies

None new. This package documents already-implemented, already-tested practice (`CredentialReference`, the agent/Sponsor token boundary, `.gitignore`'s existing entries, test-isolation conventions already followed across `jarvis/tests/`).

## Risks

1. **A standard that only documents existing practice risks becoming stale the moment a new configuration pattern is introduced without updating it** - Section 13's Maintenance Requirements name the specific triggers (new credential category, new local-data pattern, token-boundary change) to keep this from silently drifting the way other artefacts have been found to drift in past sessions' Documentation Debt Discipline work.
2. **Section 8's agent/Sponsor token boundary is stated as a possession rule, not a "no service may check it" rule** - the Sponsor Approval Service itself necessarily reads `AIEMS_SPONSOR_TOKEN` to validate incoming requests, since it is the authority the boundary protects; what must never happen is an agent-reachable process holding or supplying that token. A future capability that seems to need an agent-reachable process to possess the Sponsor token is a signal requiring a separate Programme Sponsor decision, not an exception this standard pre-authorises.

## New Backlog Item Registered by This Draft

None. This package resolves EBG-0065 in full.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern. **Result: Fail with findings.** Three blocking findings, all addressed in v0.2:

1. "Every credential is a `CredentialReference`" was overstated - AIEMS tooling (`aiems_bridge.py`, `sponsor_client.py`, `sponsor_approval_service.py`) reads its tokens via direct `os.environ.get(name)`, not through `CredentialReference`. Reworded throughout to "`CredentialReference` or an equivalent named-environment-variable indirection."
2. The "absent credential degrades honestly" rule was too broad - it correctly describes optional JARVIS provider/voice capabilities, but AIEMS approval tooling fails closed by design (a missing token must refuse to proceed, not degrade). Section 5/6 now explicitly distinguish optional-capability credentials (degrade) from authority-bearing credentials (fail closed).
3. Section 8's token-boundary wording inaccurately implied no code path may "accept" `AIEMS_SPONSOR_TOKEN` - but `sponsor_approval_service.py` necessarily reads and validates it, since it is the authority the boundary protects. Reworded to state the real boundary: which *processes may possess* the token (never an agent-reachable one), not which service is allowed to check it.

Codex confirmed all other claims (the full environment-variable inventory, `.gitignore` handling, `personal.db`/`sponsor_decisions.db` path conventions, the STD-0001/STD-0004 structural precedent, and the Authorised Files scope) were accurate as drafted.

**v0.2 resubmitted to Codex for confirmation via direct `codex exec -s read-only` invocation. Result: Pass.** Codex confirmed all three findings adequately addressed. One minor non-blocking note: the Compliance Checklist's broad "an absent/blank credential degrades honestly" row is retained alongside a separate fail-closed row for authority-bearing credentials - Codex explicitly stated this should not be treated as a remaining blocking finding, since the controlling Sections 5-6 normative text is already clear and correctly split.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**Implemented exactly as scoped.** `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` created directly at Approved/1.0, matching the exact verbatim text reviewed in Section 5 above (Effective Date filled in as 30 July 2026, Version History entry recording the Codex review cycle). No `jarvis/`, `sentinel/`, or `scripts/` file touched. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0065 marked Completed. One discovered dependency beyond the original Authorised Files list: [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]'s two EBG-0065 references (Section 7.1, Section 7.4) updated to record resolution - disclosed here rather than silently expanded, matching the `src/styles.css` precedent from ESR-0044.

`python -m pytest`: 424 passed, 1 skipped (unchanged - no code touched). `python scripts/validate_repository.py` (full mode): 0 errors, warning count reported at session close.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0065 (this package's parent item, to be marked Complete on approval and implementation). |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines the controlled artefact structure this package's new STD-0006 follows. |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Structural precedent this package's STD-0006 draft mirrors. |
| [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Programme Sponsor approved**, verified via `submit-response` against the real Sponsor Approval Service. **Implemented exactly as scoped**: STD-0006 created directly at Approved/1.0; EBR-0001 EBG-0065 marked Completed; JRM-0001 touched as a disclosed discovered dependency. No code changed. 424 tests pass, 1 skipped (unchanged). |
| 0.3 | 30 July 2026 | Claude Engineering Implementer | v0.2 resubmitted to Codex via direct `codex exec -s read-only` invocation for confirmation: **Pass**, all three prior findings adequately addressed. Pending Programme Sponsor approval. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: Fail with findings. Fixed three blocking issues: overstated "every credential is a CredentialReference" claim; too-broad "absent credential degrades" rule (now split into optional-capability vs authority-bearing categories); Section 8's token-boundary wording corrected from "no code path may accept" to "no agent-reachable process may possess." |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0045 WP1. Reviewed by Codex: Fail with findings (see v0.2). |
