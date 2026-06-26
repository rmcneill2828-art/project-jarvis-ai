# STD-0003 – Software / Python Engineering Standard

> *"Software engineering quality begins with clear boundaries, repeatable validation and accountable change."*

**Version:** 1.0

---

# Document Control

| Field | Value |
|------|------|
| Artefact ID | STD-0003 |
| Title | Software / Python Engineering Standard |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | Triggered or Periodic (as defined by the artefact) |
| Effective Date | 26 June 2026 |
| Next Review | As Required |

---

# 1. Purpose

This standard defines the mandatory software engineering requirements for Project JARVIS AI.

It establishes the minimum engineering expectations for source code, configuration, dependencies, testing, diagnostics, error handling, security and AI-assisted software development.

Python is the initial language focus for this standard because the current JARVIS implementation is a Python package.

The standard is intended to remain extensible so that future language-specific engineering standards can supplement it where required.

---

# 2. Scope

This standard applies to software created, modified or maintained within Project JARVIS AI.

It applies to:

- Python source code;
- tests;
- package structure;
- configuration used by software components;
- dependency declarations;
- diagnostics and logging behaviour;
- AI-assisted software changes.

This standard does not replace controlled governance, architecture, security or documentation standards.

Where another approved standard defines additional requirements, those requirements shall supplement this standard.

---

# 3. Relationship to AIEMS

This standard forms part of the AI Engineering Management System (AIEMS).

AIEMS establishes the governance framework for Project JARVIS AI.

This standard translates that governance into mandatory software engineering expectations for implementation activity.

All software changes shall remain traceable to approved Engineering Implementation Packages, controlled artefacts, repository evidence or other approved engineering authority.

Where conflict exists, AIEMS governance artefacts take precedence over this standard.

---

# 4. Software Engineering Principles

Software engineering within Project JARVIS AI shall be guided by the following principles.

## Readability and Maintainability

Code shall be readable, maintainable and understandable by future engineers.

Implementation clarity shall be preferred over unnecessary cleverness.

## Modular Design

Software shall be organised into clear modules with well-defined responsibilities.

Components shall be cohesive, loosely coupled and aligned with the approved repository architecture.

## Clear Boundaries

Package, module and interface boundaries shall be explicit.

Code shall not introduce hidden dependencies or unclear ownership between architectural areas.

## Traceable Change

Software changes shall be traceable to an approved Engineering Implementation Package or other approved engineering authority.

## Validation Before Baseline

Software shall be reviewed and validated before repository baseline acceptance.

---

# 5. Repository Standards

Software artefacts shall follow the approved repository structure.

Python package code shall remain under the approved package hierarchy unless an approved engineering activity changes the repository architecture.

Tests shall remain in the approved test location for the relevant package or component.

Source code, tests, configuration, secrets and runtime state shall remain separated.

Repository changes shall not introduce generated output, local environment artefacts, credentials, runtime state or temporary files into the approved baseline.

---

# 6. Python Coding Standards

Python code shall align with PEP 8 unless an approved engineering reason justifies a documented exception.

Python code shall use type hints for public interfaces, method signatures and functions where practical.

Python modules, classes, functions and methods shall use clear names that communicate their purpose.

Docstrings shall follow PEP 257-style conventions for public modules, classes and functions.

Code shall avoid unnecessary global state.

Code shall avoid broad or ambiguous behaviour where explicit behaviour is practical.

Imports shall be organised clearly and shall not create avoidable circular dependencies.

Public package APIs shall remain stable unless an approved engineering activity changes them.

---

# 7. Configuration Management

Configuration shall remain separate from source code.

Configuration values shall not be hard-coded where they represent environment-specific, deployment-specific or secret information.

Secrets, credentials, API keys and tokens shall never be committed to the repository.

Runtime state shall not be stored in source code directories unless explicitly approved for a test fixture or controlled example.

Configuration mechanisms shall be documented where they affect development, testing or operation.

---

# 8. Dependency Management

Dependencies shall be declared through approved project configuration files.

Dependencies shall be pinned or constrained where appropriate to support reproducible development and validation.

New dependencies shall be introduced only where they provide justified engineering value.

Dependency changes shall be traceable to an approved Engineering Implementation Package or other approved engineering authority.

Development dependencies shall be distinguishable from runtime dependencies where the project configuration supports that distinction.

---

# 9. Testing Standards

Software changes shall include appropriate unit tests unless an approved engineering reason justifies deferral.

Tests shall verify behaviour that is relevant to the approved engineering activity.

Integration tests shall be added where behaviour crosses module, package, service or external-interface boundaries.

Regression tests shall be added when fixing defects where practical.

Tests shall be repeatable in the approved development environment.

A software activity shall not be reported complete until the agreed validation checks have been run or an inability to run them has been clearly reported.

---

# 10. Logging and Diagnostics

Operational diagnostics shall use logging rather than print statements.

Logging shall support engineering understanding without exposing secrets, credentials or sensitive information.

Diagnostic messages shall be clear enough to support troubleshooting.

Logging behaviour shall not obscure failures or replace proper error handling.

Print statements may be used in tests, examples or temporary debugging only where they are not committed as operational diagnostics.

---

# 11. Error Handling

Errors shall be handled explicitly where failure is expected or recoverable.

Exceptions shall not be silently swallowed.

Broad exception handling shall be avoided unless the handling behaviour is justified and clear.

Error messages shall provide useful engineering context without exposing secrets or sensitive information.

Failure behaviour shall be tested where it forms part of the approved software behaviour.

---

# 12. Security Requirements

Software shall be engineered with security considerations from the start of implementation.

Credentials, secrets, API keys and tokens shall not be committed to the repository.

Software shall avoid exposing sensitive information in logs, exceptions, test output or documentation.

External inputs shall be validated where they affect security, stability or correctness.

Dependency additions shall consider security, maintenance and provenance risks.

Security-sensitive changes shall receive engineering review before baseline acceptance.

---

# 13. AI-Assisted Development Requirements

AI-generated software shall originate from an approved Engineering Implementation Package or other approved engineering authority.

AI-generated software shall remain within the approved scope of the engineering activity.

AI-generated software shall be subject to engineering review before baseline acceptance.

AI-assisted changes shall preserve repository traceability.

AI collaborators shall not bypass governance, approval gates or human accountability.

The Human Engineer remains accountable for final approval, acceptance and Git operations.

---

# 14. Engineering Review Checklist

Before software changes are accepted into the repository baseline, the engineering review should confirm that:

- the change is traceable to an approved Engineering Implementation Package or approved engineering authority;
- package and module boundaries remain clear;
- Python code follows this standard;
- type hints are present where required;
- public code has appropriate docstrings;
- configuration, secrets and runtime state remain separated from source code;
- dependencies are justified and declared appropriately;
- unit tests or justified test deferrals are present;
- integration or regression tests are present where required;
- logging is used for operational diagnostics;
- error handling is explicit and appropriate;
- security requirements have been considered;
- validation results have been reported;
- no unrelated files were modified.

---

# 15. Maintenance Requirements

This standard shall be reviewed when:

- Python engineering practices change materially;
- new implementation languages are introduced;
- repository architecture changes affect software layout;
- development tooling changes materially;
- Engineering Reviews identify recurring software quality issues;
- Strategic Alignment Reviews recommend revision.

Future language-specific standards may supplement this standard where required.

This standard shall remain aligned with AIEMS governance, approved repository architecture and the current engineering workflow.

---

# Guiding Principle

> *"Software is not complete when it works once. It is complete when it can be understood, validated, maintained and safely changed."*

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------------------|--------------------------------------------------------------|
| 1.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Software / Python Engineering Standard established for Project JARVIS AI. |