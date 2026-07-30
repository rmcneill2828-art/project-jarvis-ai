# STD-0006 - Configuration and Secrets Standard

> *"A credential that never appears in source code cannot leak from source control."*

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
| Effective Date | 30 July 2026 |
| Next Review | As Required |

---

# 2. Purpose

STD-0006 defines the configuration and secrets standard for Project JARVIS AI.

It answers the primary configuration question:

> How does Project JARVIS AI supply credentials, endpoints and other environment-specific configuration to engineering deliverables without ever committing a secret value to source control?

This standard formalises configuration and secrets practice already in live use across this repository - it does not introduce new rules the codebase does not already follow.

---

# 3. Scope

This standard applies to:

- credentials (API keys, tokens) supplied to any provider adapter, script or service;
- environment-variable-based configuration (models, endpoints, timeouts, file paths);
- local database files and other locally-persisted runtime state;
- test isolation from real credentials and real local state.

This standard does not define provider selection logic, Sentinel policy content, or the specific value of any credential - only how configuration and secrets are supplied, named and protected.

---

# 4. Relationship to AIEMS

STD-0006 forms part of the AI Engineering Management System.

AIEMS defines the governance framework for Project JARVIS AI. This standard defines the configuration and secrets expectations that keep credentials out of source control and configuration drift bounded.

Where conflict exists, approved AIEMS governance artefacts and Programme Sponsor decisions take precedence.

---

# 5. Configuration and Secrets Principles

Configuration and secrets handling shall follow these principles:

- No secret value shall ever appear in source code, a committed file, or a controlled artefact.
- Every credential is a named environment variable, referenced by name only - either via `CredentialReference` (`sentinel/provider_config.py`, used by JARVIS provider adapters) or an equivalent direct `os.environ.get(name)` read by name only (used by the AIEMS Exchange Bridge and Sponsor Approval Service tooling) - never a value held in a configuration object, dataclass default, or test fixture.
- Two distinct failure postures apply depending on what the credential gates (Section 6 defines both): an absent optional-capability credential (e.g. a JARVIS text-generation or Voice provider) degrades honestly to its next fallback; an absent authority-bearing credential (e.g. an AIEMS approval-service token) fails closed - refusing to proceed, not falling back to a weaker check.
- Test suites shall never depend on, or accidentally exercise, real credentials or real local state present on the host machine running the suite.

---

# 6. Credential Handling Requirements

1. A credential shall be represented in code only as a `CredentialReference` or an equivalent named-environment-variable indirection - never as a literal string value, even a placeholder that could be mistaken for real.
2. A component requiring a credential shall read it via `os.environ` (or an injected `environ` mapping in tests) at the point of use, never store it in a class attribute, log line, diagnostic event, or audit record.
3. This standard distinguishes two credential categories, each with its own required failure posture:
   - **Optional-capability credentials** (e.g. `OPENAI_API_KEY`, `GEMINI_API_KEY`, `JARVIS_PIPER_VOICE_PATH`) gate an optional runtime capability with a defined fallback. Where absent or blank, the component shall degrade to its next honest fallback (a lower-priority provider, `not_connected`, or equivalent) rather than fail startup or fabricate a result - matching `_build_real_provider()` and `_build_speech_provider()`'s established pattern in `jarvis/interfaces/stdio_rpc.py`.
   - **Authority-bearing credentials** (e.g. `AIEMS_AGENT_TOKEN`, `AIEMS_SPONSOR_TOKEN`) gate an engineering-authority decision with no safe fallback. Where absent or blank, the component shall fail closed - refusing to proceed - matching `scripts/sponsor_approval_service.py` and `scripts/sponsor_client.py`'s established behaviour (both refuse to run without their required token). A missing authority-bearing credential shall never be treated as "capability unavailable, continue anyway."
4. A present-but-blank non-credential configuration value (e.g. a model name) shall fall through to its documented default, not silently propagate an empty string into a downstream constructor that would reject it.

---

# 7. Environment Variable Naming Convention

Environment variables shall use one of the following prefixes, consistent with existing repository practice:

| Prefix | Scope | Examples |
|--------|-------|----------|
| `JARVIS_` | JARVIS backend runtime configuration (models, endpoints, timeouts, file paths, feature-specific paths) | `JARVIS_OLLAMA_MODEL`, `JARVIS_MEMORY_DB_PATH`, `JARVIS_PIPER_VOICE_PATH`, `JARVIS_PRIMARY_PROVIDER` |
| `AIEMS_` | AIEMS engineering tooling (the Exchange Bridge, Sponsor Approval Service) | `AIEMS_AGENT_TOKEN`, `AIEMS_SPONSOR_TOKEN`, `AIEMS_SPONSOR_URL`, `AIEMS_SPONSOR_DB_PATH` |
| Provider-native | Third-party provider SDK/API conventions, used as-is rather than reprefixed | `OPENAI_API_KEY`, `OPENAI_MODEL`, `GEMINI_API_KEY`, `GEMINI_MODEL` |

A new environment variable shall use the prefix matching its actual scope - a new JARVIS backend setting shall not be given an `AIEMS_` prefix, and vice versa.

---

# 8. Agent-Accessible vs Sponsor-Only Credential Boundary

Some credentials govern a hard authority boundary between AI engineering collaborators (Claude, Codex) and the Programme Sponsor. The boundary is about which *processes may possess* a token, not which service checks it - the Sponsor Approval Service itself necessarily reads and compares against `AIEMS_SPONSOR_TOKEN`, since it is the authority the boundary protects:

- `AIEMS_AGENT_TOKEN` is the agent-facing token. `scripts/aiems_bridge.py` (run from an environment an AI collaborator's own tool calls can reach) reads only `AIEMS_AGENT_TOKEN` and `AIEMS_SPONSOR_URL` - it does not read `AIEMS_SPONSOR_TOKEN` at all.
- `AIEMS_SPONSOR_TOKEN` shall never be set in, or readable from, an environment an AI collaborator's own tool calls can reach. `scripts/sponsor_client.py` (the only tool that supplies it as a decision, via the Programme Sponsor's own host-side terminal) and `scripts/sponsor_approval_service.py` (the server-hosted authority that validates it against incoming approval requests) are the only two processes that shall ever hold this token.
- This boundary is a security control, not a convenience distinction - a future capability that appears to need an AI-collaborator-reachable process to possess `AIEMS_SPONSOR_TOKEN` is a signal that the capability's design crosses this boundary and needs its own explicit Programme Sponsor decision, not a workaround.

---

# 9. Local Data and Database File Requirements

1. A locally-persisted runtime data file (e.g. `personal.db`, `sponsor_decisions.db`) shall never be committed to the repository.
2. Its default path shall live outside the repository working tree where practical (e.g. under the user's home directory) or under an already-`.gitignore`d repository-local directory (e.g. `.aiems-exchange/`) where a working-tree-relative default is more appropriate.
3. Its path shall be overridable via a named environment variable following Section 7's convention, so tests and alternate deployments never depend on the default location.
4. Where filesystem permission hardening is available (POSIX), it should be applied at creation; where it is not available (Windows), that limitation shall be disclosed, not silently assumed equivalent.

---

# 10. Test Isolation Requirements

1. Automated tests shall never rely on `os.environ`'s real, ambient state - every test that depends on configuration shall pass an explicit `environ` mapping (even an empty one) rather than defaulting to the real environment.
2. Automated tests shall never read or write a real local database file at its default path - every test shall use a `tmp_path`-scoped (or equivalent) override.
3. A test helper shared across multiple tests (e.g. a provider construction helper) shall itself be test-isolated, not merely relied upon to be called correctly by each test - the exact defect class ESR-0026 WP1 found and fixed for a shared Ollama test helper.

---

# 11. .gitignore Requirements

1. `.env` and `.env.*` shall remain permanently ignored, as a standing guard against an accidental commit, even though no `.env` file is expected to exist in this repository's working practice.
2. Any new local-only working directory analogous to `.aiems-exchange/` shall be added to `.gitignore` at the point it is introduced, with a comment explaining what it holds and why it is excluded - matching the existing disclosed pattern, not a bare, unexplained ignore entry.

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

It shall not become a general security policy document beyond configuration and secrets handling.

This standard shall be reviewed when configuration/secrets practice changes materially (a new credential category, a new local-data pattern, or a change to the agent/Sponsor token boundary), or when a security review finding requires an updated rule.

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
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial Configuration and Secrets Standard created for Project JARVIS AI, formalising already-established repository practice (EBG-0065, ESR-0045). Codex design-reviewed (v0.1 Fail with findings - overstated CredentialReference claim, too-broad degradation rule, inaccurate token-boundary wording; v0.2 Pass after correction). Programme Sponsor approved via the real Sponsor Approval Service. |
