# TPL-0001 - Engineering Execution Package Template

> *"A repeatable execution package turns approved intent into governed delivery."*

**Version:** 0.2

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | TPL-0001 |
| Title | Engineering Execution Package Template |
| Version | 0.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[CHR-0002_ENGINEERING_CONSTITUTION|CHR-0002]] |
| Effective Date | 2 July 2026 |
| Review Frequency | At Engineering Execution Package review or template change |

---

# 2. Template Purpose

This artefact is a template, not an Engineering Execution Package.

It shall be copied or instantiated for future Engineering Execution Packages. Placeholder fields shall be replaced during package generation before the package is issued for Engineering Implementer execution.

This template defines the canonical reusable structure for Engineering Execution Packages ready for Engineering Implementer execution under AIEMS.

---

# 3. AIEMS Engineering Execution Package Header

```text
============================================================
AIEMS ENGINEERING EXECUTION PACKAGE
===================================

Package ID:
{{PACKAGE_ID}}

Engineering Session:
{{ENGINEERING_SESSION}}

Work Package:
{{WORK_PACKAGE}}

Artefact:
{{ARTEFACT_ID}}

Title:
{{TITLE}}

Mode:
{{MODE}}

Repository:
project-jarvis-ai

Branch:
main
============================================================
```

---

# 4. Package Metadata

| Field | Placeholder |
|-------|-------------|
| Package ID | {{PACKAGE_ID}} |
| Engineering Session | {{ENGINEERING_SESSION}} |
| Work Package | {{WORK_PACKAGE}} |
| Artefact ID | {{ARTEFACT_ID}} |
| Title | {{TITLE}} |
| Mode | {{MODE}} |
| Objective | {{OBJECTIVE}} |
| Save Location | {{SAVE_LOCATION}} |
| Authorised Files | {{AUTHORISED_FILES}} |
| Validation Commands | {{VALIDATION_COMMANDS}} |
| Commit Message | {{COMMIT_MESSAGE}} |

---

# 5. Role and Authority

```text
You are acting as Engineering Implementer under AIEMS.

This Engineering Execution Package has been approved by the Programme Sponsor.

Controlled repository artefacts shall only be created, modified or removed within the authorised scope of this package.

GitHub remains the authoritative source of truth.
```

The Programme Sponsor remains final approval authority.

---

# 6. Delivery Authority

The Engineering Implementer is the delivery mechanism for repository artefact creation or modification unless the package explicitly authorises another delivery mechanism.

The Engineering Reviewer performs independent GitHub verification after Engineering Implementer execution.

---

# 7. Engineering Directive

```text
{{ENGINEERING_DIRECTIVE}}
```

The directive shall state the approved engineering action and any required OSE application.

---

# 8. Objective

```text
{{OBJECTIVE}}
```

The objective shall describe the intended repository outcome without relying on conversational memory.

---

# 9. Repository Synchronisation

Before implementation, verify:

1. Current branch is `main`.
2. Working tree is clean.
3. Repository is up to date with `origin/main`.
4. Current accepted repository baseline is identified.
5. Current engineering session or transition state is identified.
6. No conflicting target artefact already exists unless the package authorises modification.

Recommended commands:

```powershell
git status
git branch --show-current
git log --oneline -10
```

Where up-to-date confirmation is required, fetch and compare with `origin/main` before implementation.

---

# 10. Engineering Authority

The package shall identify:

| Authority Field | Placeholder |
|-----------------|-------------|
| Programme Sponsor approval basis | {{PROGRAMME_SPONSOR_APPROVAL}} |
| Engineering Implementer scope | {{IMPLEMENTER_SCOPE}} |
| Final approval authority | Programme Sponsor |
| Source of truth | GitHub |
| Independent verification role | Engineering Reviewer |

---

# 11. Architecture / Governance Context

Record the verified governance and architecture context required for the package.

```text
{{ARCHITECTURE_GOVERNANCE_CONTEXT}}
```

Only verified repository artefacts shall be referenced. Do not invent links to artefacts that do not exist.

---

# 12. Save Location

```text
{{SAVE_LOCATION}}
```

No alternative filename or location is permitted unless the approved package explicitly allows it.

---

# 13. Scope

```text
{{SCOPE}}
```

The scope shall define the intended repository change and the artefact boundaries of the work.

---

# 14. Authorised Changes

Authorised files:

```text
{{AUTHORISED_FILES}}
```

No other files shall be modified unless required by repository validation and explicitly reported in the completion handoff.

---

# 15. OSE Requirements

OSE applies only to authorised modified artefacts.

When OSE is required:

- use verified WikiLinks only;
- expose existing engineering relationships only;
- do not create speculative links;
- do not add YAML front matter;
- do not add Obsidian Properties;
- do not add tags;
- preserve GitHub Markdown readability;
- include a Related Artefacts section where verified relationships exist.

Package-specific OSE requirements:

```text
{{OSE_REQUIREMENTS}}
```

---

# 16. Implementation Requirements

```text
{{IMPLEMENTATION_REQUIREMENTS}}
```

Implementation requirements shall be specific enough for Engineering Implementer execution without requiring reconstruction from chat history.

---

# 17. Explicit Exclusions

```text
{{EXPLICIT_EXCLUSIONS}}
```

Exclusions shall state what must not be created, modified, removed or inferred during execution.

---

# 18. Constraints

```text
{{CONSTRAINTS}}
```

Constraints shall include repository, governance, validation, scope and execution limits.

---

# 19. Validation

Run the validation commands specified by the package.

```powershell
{{VALIDATION_COMMANDS}}
```

Minimum confirmation should include:

- target artefact exists at the required path;
- placeholder fields have been replaced where the package is an execution package;
- no unauthorised files were modified;
- OSE links are verified and non-speculative;
- repository validation passes or any failure is explained.

---

# 20. AIEMS Git Execution

Repository status:

```powershell
git status
```

Stage approved deliverables:

```powershell
git add {{AUTHORISED_FILES}}
```

Review staged files:

```powershell
git status
```

Create engineering commit:

```powershell
git commit -m "{{COMMIT_MESSAGE}}"
```

Push repository:

```powershell
git push origin main
```

Final status:

```powershell
git status
```

---

# 21. Post Implementation / Post Push

Return the following handoff:

1. Current branch.
2. HEAD before implementation.
3. Commit SHA.
4. Confirmation push completed successfully.
5. Files created.
6. Files modified.
7. Summary of content.
8. OSE links added.
9. Validation commands run.
10. Validation results.
11. Final git status.
12. Any exceptions or deviations.

---

# 22. Independent GitHub Verification Handoff

The Engineering Reviewer shall perform independent GitHub verification after Engineering Implementer execution, including:

1. Repository state verification.
2. Content review.
3. OSE compliance review.
4. Scope compliance review.
5. Recommendation for Programme Sponsor acceptance or rework.

---

# 23. Completion Marker

```text
============================================================
END OF ENGINEERING EXECUTION PACKAGE
============================================================
```

---

# 24. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines OSE requirements for controlled artefact relationship enrichment. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and the repository-compatible OSE context. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers TPL-0001 as a controlled AIEMS template artefact. |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines controlled artefact structure and metadata expectations. |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] | Defines documentation quality expectations for reusable engineering artefacts. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Records current programme status and repository baseline context. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline at the time TPL-0001 was created. |

---

# 25. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source for approved engineering work that may be delivered through execution packages. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report preceding ESR-0009 readiness and RBL-0009 acceptance. |

---

# 26. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 8 July 2026 | Claude Engineering Implementer | Replaced ChatGPT/Codex role naming with Engineering Reviewer/Engineering Implementer throughout, decoupling this template from named AI products. |
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial Engineering Execution Package Template created under EIP-ESR0009-002. |