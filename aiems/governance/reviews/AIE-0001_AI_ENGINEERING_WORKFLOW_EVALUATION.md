# AIE-0001 – AI Engineering Workflow Evaluation

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | AIE-0001 |
| Title | AI Engineering Workflow Evaluation |
| Version | Unversioned Draft |
| Status | Draft |
| Owner | Programme Sponsor |
| Approved By | Pending Programme Sponsor Review |
| Classification | Internal |

---

# 1. Executive Summary

Project JARVIS AI has reached a stage where engineering productivity is increasingly constrained by manual interaction between development tools, documentation and AI-assisted engineering. While the current workflow has successfully established governance, engineering standards and the initial JARVIS platform, it relies heavily on manual context sharing and repetitive copy-and-paste operations.

The purpose of this evaluation is to identify and recommend an AI-assisted engineering ecosystem that improves productivity while preserving engineering quality, governance and human accountability.

This evaluation is not intended to identify the "best AI tool". Instead, it seeks to define the engineering capabilities required by Project JARVIS AI and evaluate which combination of technologies best fulfils those capabilities over the next three to five years.

The outcome of this evaluation will be the adoption of an official Engineering Workflow v1.0 and Recommended Engineering Stack v1.0 for Project JARVIS AI.

---

# 2. Purpose

The objective of AIE-0001 is to evaluate, compare and recommend an engineering ecosystem that enables efficient, scalable and governed AI-assisted software engineering.

The evaluation will focus on reducing engineering friction while maintaining the principles established by AIEMS.

Specifically, the evaluation will determine how architecture, implementation, testing, documentation, governance and source control should be supported by AI technologies while ensuring that engineering judgement and accountability remain with the human engineer.

This evaluation will assess engineering capabilities before evaluating individual technologies.

---

# 3. Current Engineering Baseline

The current engineering environment for Project JARVIS AI consists of:

| Capability                             | Current Implementation | Status         |
| -------------------------------------- | ---------------------- | -------------- |
| Integrated Development Environment     | Visual Studio Code     | Adopted        |
| Programming Language                   | Python 3.12            | Adopted        |
| Source Control                         | GitHub                 | Adopted        |
| Static Analysis                        | Ruff                   | Adopted        |
| Automated Testing                      | Pytest                 | Adopted        |
| Engineering Governance                 | AIEMS                  | Adopted        |
| Architecture & Engineering Partner     | ChatGPT                | Adopted        |
| Repository-Aware Engineering Assistant | None                   | Capability Gap |
| Multi-file AI Engineering              | None                   | Capability Gap |
| AI-assisted GitHub Workflow            | None                   | Capability Gap |

The current engineering workflow has successfully supported the initial development of Project JARVIS AI. However, as the platform grows, manual context sharing and repetitive engineering tasks are expected to become significant constraints on productivity.

The purpose of this evaluation is therefore not to replace the existing engineering environment, but to identify technologies that address the identified capability gaps while remaining aligned with AIEMS engineering principles.

# 4. Required AI-Assisted Engineering Capabilities

The purpose of this section is to define the capabilities required by the Project JARVIS AI engineering ecosystem before evaluating individual technologies.

These capabilities represent the operational requirements of the engineering workflow and are intentionally independent of any specific product or vendor. Technologies will be evaluated against their ability to satisfy these capabilities rather than the capabilities being defined by the technologies themselves.

Each capability has been assigned a priority based upon its importance to the successful delivery of Project JARVIS AI.

| ID       | Capability Category              | Capability                                                                                                                                                                            |  Priority | Success Criteria                                                                                                      |
| -------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: | --------------------------------------------------------------------------------------------------------------------- |
| AIEC-001 | Repository Intelligence          | The engineering assistant shall understand the structure, relationships and context of the project repository without requiring repeated manual context sharing.                      |  Critical | Relevant files, project structure and relationships can be identified with minimal manual intervention.               |
| AIEC-002 | Multi-file Engineering           | The engineering assistant shall support coordinated changes across multiple files, ensuring implementations remain consistent throughout the repository.                              |  Critical | Features requiring updates to source code, tests and documentation can be completed as a single engineering activity. |
| AIEC-003 | Source Control Integration       | The engineering ecosystem shall integrate naturally with Git and GitHub to support commits, branches, reviews and pull requests.                                                      |    High   | Source control becomes a natural part of the engineering workflow rather than a separate manual process.              |
| AIEC-004 | Architecture Partnership         | The engineering ecosystem shall support architectural discussion, design review and engineering decision-making without replacing human judgement.                                    |  Critical | AI enhances engineering reasoning while final architectural decisions remain the responsibility of the engineer.      |
| AIEC-005 | Quality Assurance                | The engineering ecosystem shall encourage automated testing, static analysis and engineering best practice throughout the software lifecycle.                                         |  Critical | Engineering quality is improved through consistent verification and automated quality gates.                          |
| AIEC-006 | Governance Documentation Maintenance    | The engineering ecosystem shall support the maintenance of engineering documentation and ensure implementation remains aligned with governance artefacts.                             |    High   | Engineering documentation and implementation remain synchronised with minimal manual effort.                          |
| AIEC-007 | Human Governance                 | The engineering ecosystem shall preserve human approval and accountability for all engineering decisions.                                                                             | Mandatory | AI may recommend changes, but implementation and approval remain under human control.                                 |
| AIEC-008 | Security & Intellectual Property | The engineering ecosystem shall protect project information, source code and organisational knowledge through appropriate security and governance controls.                           | Mandatory | Engineering activities comply with organisational security and information governance requirements.                   |
| AIEC-009 | Vendor Independence              | The engineering ecosystem shall minimise dependence upon any single technology vendor through the use of defined capabilities and interchangeable implementations wherever practical. |    High   | Individual products can be replaced with minimal disruption to the engineering workflow.                              |
| AIEC-010 | Future Adaptability              | The engineering ecosystem shall remain sufficiently flexible to support future technologies, engineering practices and organisational growth without requiring fundamental redesign.  |  Critical | The engineering workflow continues to evolve while preserving the principles established by AIEMS.                    |

## Engineering Principle

Project JARVIS AI evaluates engineering capabilities before selecting technologies.

This ensures that engineering requirements remain stable while allowing technologies to evolve over time. Products may change, but the capabilities required to support professional AI-assisted engineering remain consistent.

# 5. Capability Gap Analysis & Evidence Requirements

This section compares the current engineering environment against the required AI-assisted engineering capabilities defined in Section 4.

The purpose of this assessment is to identify capability gaps, understand the associated engineering risks, define the desired future state and establish the evidence required to demonstrate that a proposed solution satisfies the identified capability.

This evaluation is intentionally evidence-based. Recommendations will only be made where sufficient evidence demonstrates that a candidate technology improves the engineering workflow while remaining aligned with AIEMS principles.

| Capability ID | Current State                                                                                        | Capability Gap | Engineering Risk                                                                                       | Desired Future State                                                                                          | Evidence Required                                                                                                     |
| ------------- | ---------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| AIEC-001      | Repository context is provided through manual explanation and copy/paste.                            | Yes            | Increasing engineering time, context switching and potential misunderstanding as the repository grows. | AI can understand repository structure, relationships and relevant files with minimal manual context sharing. | Demonstrate successful repository navigation and engineering discussion using existing Project JARVIS AI source code. |
| AIEC-002      | Engineering changes are applied manually across multiple files.                                      | Yes            | Inconsistent implementation, increased engineering effort and higher risk of omissions.                | AI supports coordinated engineering changes across multiple source files, tests and documentation.            | Demonstrate a feature implementation requiring coordinated updates across multiple artefacts.                         |
| AIEC-003      | Git operations are performed manually using Git CLI and GitHub.                                      | Partial        | Source control remains disconnected from AI-assisted engineering workflow.                             | AI integrates naturally with branches, commits, pull requests and engineering reviews.                        | Demonstrate support for commit preparation, pull request workflows and repository review.                             |
| AIEC-004      | Architectural guidance is provided through ChatGPT discussion.                                       | No             | None identified. Current capability satisfies engineering requirements.                                | Continue using ChatGPT as the primary architecture and engineering discussion partner.                        | Confirm that repository-aware tooling complements rather than replaces architectural decision-making.                 |
| AIEC-005      | Quality verification is performed using Ruff and Pytest.                                             | Partial        | Quality verification remains separate from AI-assisted implementation.                                 | AI supports engineering quality by encouraging testing, static analysis and verification.                     | Demonstrate integration with existing Ruff and Pytest workflow without reducing engineering discipline.               |
| AIEC-006      | Engineering documentation is maintained manually.                                                    | Yes            | Documentation may diverge from implementation over time.                                               | AI assists with maintaining synchronisation between implementation and AIEMS documentation.                   | Demonstrate coordinated updates to implementation and controlled documentation within the same engineering activity.  |
| AIEC-007      | Human approval is maintained throughout the engineering process.                                     | No             | None identified. Existing governance aligns with AIEMS principles.                                     | Preserve human approval and engineering accountability for all recommendations and implementations.           | Demonstrate workflows where AI proposes changes and the engineer retains approval and implementation authority.       |
| AIEC-008      | Security decisions rely upon existing organisational controls and engineering judgement.             | Partial        | AI integration could introduce additional security and intellectual property considerations.           | AI-assisted engineering operates within clearly defined security, privacy and governance controls.            | Evaluate security model, data handling, permissions and organisational controls for each candidate solution.          |
| AIEC-009      | Current workflow relies primarily upon open engineering standards and Git-based development.         | Partial        | Adoption of proprietary tooling may increase long-term dependency.                                     | Engineering capabilities remain portable between vendors wherever practical.                                  | Assess migration effort, interoperability and vendor lock-in risk for each evaluated ecosystem.                       |
| AIEC-010      | Current engineering workflow is suitable for the present project size but may not scale efficiently. | Yes            | Engineering productivity will reduce as repository size and complexity increase.                       | Engineering workflow scales naturally as Project JARVIS AI evolves.                                           | Demonstrate improved productivity and reduced manual effort when performing representative engineering tasks.         |

## Assessment Summary

The current engineering environment provides a strong foundation for disciplined software development and governance. The principal gaps do not relate to engineering quality or governance, but to engineering efficiency, repository intelligence and workflow integration.

The objective of the remaining evaluation is therefore not to replace the existing engineering environment, but to identify technologies that demonstrably address the identified capability gaps while preserving the principles established by AIEMS.

Only solutions supported by reproducible evidence will be recommended for adoption.
---

# 6. Codex Evaluation Evidence

This section records observed evidence gathered during the Codex engineering workflow evaluation session.

The evidence below is limited to capabilities actually exercised during the session. It does not infer or claim capabilities that were not tested.

## Observed Evidence

| Evidence Area | Observation |
| ------------- | ----------- |
| Repository inspection | Codex inspected the repository structure, source package, tests, project configuration, governance documentation and Git working tree state before recommending changes. |
| Engineering recommendation | Codex recommended a stable public package API based on observed coupling between tests and internal module paths. |
| Multi-file implementation | Following approval, Codex implemented a public package API across package exports, tests and lifecycle documentation. |
| Packaging correction | Codex identified that setuptools was configured to include only the top-level package and corrected package discovery after approval. |
| Test coverage | Codex added a public API smoke test to verify the package-level import boundary. |
| Quality verification | Codex ran Ruff and Pytest after implementation. |
| Packaging verification | Codex performed an editable-install dry run and inspected a built wheel in a temporary directory to confirm subpackages were included. |
| Governance maintenance | Codex registered AIE-0001 in REG-0001 after the artefact was identified as a new controlled governance review artefact. |
| Human approval | Codex requested approval before implementation activities and waited for authorisation before modifying files. |
| Scope control | Codex limited modifications to approved files during each implementation activity. |

## Evidence Boundaries

The evaluation did not test every capability defined in Section 4.

The following capabilities remain unevaluated or only partially evaluated:

| Capability ID | Evaluation Status | Notes |
| ------------- | ----------------- | ----- |
| AIEC-001 | Partially evaluated | Repository navigation and local context analysis were demonstrated. Large-scale repository intelligence was not tested. |
| AIEC-002 | Evaluated in limited scope | Multi-file changes were demonstrated across source, tests, configuration and governance documentation. Larger architectural changes were not tested. |
| AIEC-003 | Partially evaluated | Local Git status, diff and commit-state inspection were demonstrated. GitHub pull requests, branches and review workflows were not tested. |
| AIEC-004 | Partially evaluated | Engineering recommendation and architectural reasoning were demonstrated. Broader architecture review workflows were not tested. |
| AIEC-005 | Partially evaluated | Ruff, Pytest, editable-install dry run and wheel inspection were demonstrated. Continuous integration was not tested. |
| AIEC-006 | Partially evaluated | Governance documentation maintenance was demonstrated through controlled documentation and register updates. Full lifecycle governance was not tested. |
| AIEC-007 | Evaluated | Human approval gates were observed before modification activities. |
| AIEC-008 | Not evaluated | Security, privacy, intellectual property and data-handling controls were not tested. |
| AIEC-009 | Not evaluated | Vendor independence, portability and migration effort were not tested. |
| AIEC-010 | Not evaluated | Long-term adaptability and scaling across a larger programme were not tested. |

---

# 7. Observed Engineering Behaviour

This section records engineering behaviour observed during the evaluation session.

## Evidence Gathering Before Implementation

Codex inspected repository structure, existing source code, tests, configuration and governance artefacts before recommending or implementing changes.

This behaviour supports evidence-based engineering by reducing reliance on assumption.

## Permission Discipline

Codex requested approval before making modifications where the activity required authorisation.

When implementation was approved, Codex operated within the approved task boundaries.

## Scope Discipline

Codex limited changes to the files explicitly approved for each implementation activity.

When a change was outside the approved scope, Codex identified it as a follow-up recommendation rather than modifying additional files.

## Self-Validation

Codex inspected diffs after implementation and corrected issues identified during its own review before reporting completion.

This included checking that only intended files were modified.

## Validation Depth

Codex used multiple validation methods appropriate to the change being made.

Observed validation included static analysis, automated tests, editable-install dry run and wheel-content inspection.

## Human Approval Gates

Human approval gates were preserved throughout the evaluation.

Codex proposed changes, explained rationale and waited for approval before implementation.

---

# 8. Evaluation Conclusions

The evaluation provides evidence that Codex can support repository-aware engineering tasks within a governed workflow when scope, approval and validation expectations are clearly defined.

The strongest observed capabilities were:

- Repository inspection and contextual engineering recommendation.
- Coordinated multi-file implementation within approved scope.
- Integration with local quality checks.
- Evidence-based follow-up identification.
- Governance documentation maintenance.
- Preservation of human approval and accountability.

These conclusions are limited to the activities actually performed during this evaluation session.

---

# 9. Capabilities Remaining Unevaluated

The following areas require further evaluation before final engineering workflow adoption decisions are made:

- GitHub pull request creation, review and merge workflows.
- Branch management and remote collaboration.
- Review-thread handling.
- Continuous integration workflows.
- Security, privacy and intellectual property controls.
- Vendor independence and migration effort.
- Performance on larger repositories and longer-running engineering tasks.
- Full controlled artefact lifecycle management for new governance documents.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| Unversioned Draft | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded Codex evaluation evidence, observed engineering behaviour and remaining unevaluated capabilities. |
