# FE-0007 – Approved Implementation of PBK-0001 AI Engineering Playbook (Part II)

**Status:** Draft

**Version:** 1.0

---

# Purpose

This Engineering Feature records the approved implementation package for **PBK-0001 – AI Engineering Playbook (Part II)**.

The purpose of FE-0007 is to provide the authoritative implementation design that shall be used when populating Part II of PBK-0001.

FE-0007 is an Engineering Authoring activity. It creates the approved implementation package only and does not modify PBK-0001.

---

# Background

PBK-0001 Part I established the foundational philosophy, governance relationship and Five Foundational Principles of AI Engineering.

FE-0006 authorised the future implementation of **Part II – Operational Engineering Workflow** within PBK-0001.

Engineering Synchronisation confirmed that PBK-0001 currently contains Part I only and that Part II has not yet been implemented.

FE-0007 provides the approved implementation design that shall govern the subsequent PBK-0001 Part II implementation activity.

---

# Objectives

The objectives of FE-0007 are to:

* Record the approved implementation design for PBK-0001 Part II.
* Preserve the approved implementation groups without reinterpretation.
* Establish the authoritative implementation package for the subsequent PBK-0001 Part II implementation activity.
* Confirm that no engineering decisions, wording reinterpretation or additional engineering doctrine are introduced during this authoring activity.
* Confirm that PBK-0001 is not modified by FE-0007.

---

# Approved Implementation Design

Part II – Operational Engineering Workflow

1. Engineering Activity Lifecycle

Purpose

The AI Engineering Management System (AIEMS) defines a repeatable operational engineering workflow to ensure that every Engineering Activity is performed in a disciplined, transparent and evidence-based manner.

The purpose of the Engineering Activity Lifecycle is not to constrain engineering judgement but to ensure that engineering decisions are made consistently, governance is preserved, and engineering confidence increases throughout the lifecycle of an activity.

Each Engineering Activity should leave the engineering system in a better state than it was found.

This improvement may be achieved through:

Improved repository artefacts.

Improved engineering processes.

Improved documentation.

Improved understanding.

Improved engineering recommendations.

Improved collaboration between human engineers and AI collaborators.

The Engineering Activity Lifecycle is therefore both an operational workflow and a continuous improvement model.

Every Engineering Activity progresses through four operational phases:

Discover

Plan

Execute

Baseline

Each phase has a defined objective, expected behaviours and measurable success criteria.

Engineering Activities shall not bypass phases unless explicitly authorised by the accountable human engineer.

2. Engineering Synchronisation

Purpose

Engineering Synchronisation establishes the authoritative engineering baseline before analysis, planning, recommendation or implementation begins.

Its purpose is to ensure that engineering decisions are based upon verified evidence rather than historical knowledge, assumptions or incomplete information.

Engineering Synchronisation is the first operational activity performed within every Engineering Activity.

Definition

Engineering Synchronisation is the process of establishing the current authoritative engineering baseline appropriate to the stage of the Engineering Activity.

The authoritative baseline may be:

The local engineering repository before commit.

The shared repository following publication.

Approved governance artefacts.

Controlled engineering documentation.

Other approved engineering knowledge sources.

The objective is not to collect all available information but to identify the information required to perform disciplined engineering.

Expected Behaviour

Engineering Synchronisation should:

Identify the authoritative engineering baseline.

Confirm repository status where applicable.

Identify applicable governance artefacts.

Discover related Engineering Features, ADRs, Registers and Playbooks.

Record observations where inconsistencies are identified.

Distinguish verified evidence from assumption.

Delay engineering reasoning until sufficient engineering context has been established.

Success Criteria

Engineering reasoning begins only after the authoritative engineering baseline has been established and sufficient engineering evidence has been gathered to support informed analysis.

Where the available evidence is incomplete, the uncertainty shall be identified explicitly rather than inferred or concealed.

3. Engineering Context Discovery

Purpose

Engineering Context Discovery identifies the engineering information required to understand an Engineering Activity before planning or implementation begins.

Its purpose is to establish the engineering context in which decisions will be made, ensuring that recommendations are relevant, traceable and aligned with the approved governance baseline.

Engineering Context Discovery follows Engineering Synchronisation and precedes engineering planning.

Definition

Engineering Context Discovery is the disciplined process of identifying the engineering artefacts, constraints, dependencies and historical decisions that are relevant to the current Engineering Activity.

The objective is to understand the engineering environment rather than merely retrieve information.

Expected Behaviour

Engineering Context Discovery should:

Identify the Engineering Feature or approved activity being undertaken.

Identify applicable governance artefacts, including Charters, Standards, ADRs, Registers and Playbooks.

Identify related Engineering Features and previous engineering decisions.

Identify dependencies, assumptions and constraints.

Identify unresolved recommendations that may influence the activity.

Distinguish verified engineering context from inferred context.

Record uncertainties or missing information before planning begins.

Engineering Context Discovery shall remain focused on information that materially influences the current Engineering Activity.

Success Criteria

The engineering context has been sufficiently established that planning can proceed with a shared understanding of:

the engineering objective;

the applicable governance;

the relevant repository baseline;

known constraints;

known dependencies; and

any identified uncertainties.

4. Engineering Planning

Purpose

Engineering Planning defines how an Engineering Activity will be completed before implementation begins.

Its purpose is to translate the engineering context into a structured implementation approach that is understandable, reviewable and capable of receiving informed human approval.

Planning establishes a shared understanding between the accountable human engineer and the AI collaborator.

Definition

Engineering Planning is the disciplined process of defining the intended implementation before any repository modifications are made.

The implementation plan should describe the proposed engineering approach rather than perform the engineering activity itself.

Expected Behaviour

Engineering Planning should:

Define the engineering objective.

Confirm the approved scope.

Identify work that is explicitly out of scope.

Describe the proposed implementation approach.

Identify assumptions, dependencies and risks.

Separate observations from recommendations.

Identify recommendations that require future Engineering Activities.

Present a concise summary of the proposed implementation.

Engineering Planning shall not initiate implementation.

Implementation begins only after explicit human approval.

Success Criteria

Planning is complete when:

the engineering objective is clearly understood;

the implementation approach has been documented;

the approved scope is unambiguous;

recommendations have been separated from implementation; and

the accountable human engineer has sufficient information to approve or reject the proposed activity.

5. Human Approval Gates

Purpose

Human Approval Gates ensure that implementation proceeds only after the accountable human engineer has reviewed the proposed Engineering Activity and explicitly authorised the intended scope of work.

Their purpose is to preserve human accountability while enabling AI collaborators to contribute efficiently within approved engineering boundaries.

Approval is a governance activity rather than an implementation activity.

Definition

A Human Approval Gate is a formal decision point within an Engineering Activity at which the accountable human engineer determines whether implementation may proceed.

Approval shall be based upon the proposed implementation plan, identified engineering context, applicable governance and known risks.

Approval authorises implementation only within the explicitly approved scope.

Expected Behaviour

Prior to requesting approval, the AI collaborator should:

Complete Engineering Synchronisation.

Complete Engineering Context Discovery.

Complete Engineering Planning.

Clearly distinguish observations from recommendations.

Clearly identify approved scope and out-of-scope work.

Present the proposed implementation in a concise and reviewable format.

Following approval, the AI collaborator shall:

Implement only the approved scope.

Preserve governance throughout implementation.

Record any newly discovered issues as recommendations unless additional approval is obtained.

Request further approval before expanding scope.

Approval shall not be inferred from previous activities, assumptions or implied intent.

Approval should be explicit, attributable and appropriate to the engineering risk associated with the activity.

Success Criteria

Implementation begins only after:

explicit human approval has been obtained;

the approved scope is understood by both the accountable human engineer and the AI collaborator;

governance obligations have been identified; and

authority to proceed has been clearly established.

Where approval is withheld, implementation shall not proceed until the Engineering Activity has been revised or further direction has been provided.

6. Controlled Implementation

Purpose

Controlled Implementation ensures that approved Engineering Activities are executed in a disciplined, transparent and predictable manner.

Its purpose is to translate the approved implementation plan into completed engineering work while preserving governance, maintaining repository integrity and preventing unintended change.

Implementation is the execution of an approved engineering decision rather than the discovery of a new one.

Definition

Controlled Implementation is the process of performing only the engineering work that has been explicitly authorised through the Human Approval Gate.

Implementation shall remain aligned with the approved scope throughout the Engineering Activity.

New observations, opportunities or engineering improvements identified during implementation shall be recorded as recommendations unless additional approval is obtained.

Expected Behaviour

During implementation, the AI collaborator should:

Execute only the approved implementation plan.

Preserve repository integrity.

Maintain alignment with applicable governance artefacts.

Avoid introducing unrelated engineering changes.

Preserve traceability between the Engineering Activity and repository modifications.

Clearly distinguish completed implementation from future recommendations.

Record newly identified risks or opportunities without expanding scope.

Where implementation reveals that the approved plan is no longer appropriate, implementation should pause until further human direction is obtained.

Implementation shall favour small, reviewable and traceable changes over large or unnecessary modifications.

Success Criteria

Controlled Implementation is complete when:

all approved engineering work has been completed;

no unauthorised repository changes have been introduced;

implementation remains fully traceable to the approved Engineering Activity;

recommendations have been separated from implementation; and

the Engineering Activity is ready for validation.

7. Validation and Self-Review

Purpose

Validation and Self-Review ensure that completed engineering work satisfies the approved Engineering Activity before it is reported as complete.

Its purpose is to increase engineering confidence by verifying that implementation aligns with the approved scope, preserves governance and accurately reflects the intended engineering outcome.

Validation is an engineering activity, not an administrative task.

Definition

Validation is the disciplined process of confirming that completed engineering work matches the approved implementation plan.

Self-Review is the process by which the AI collaborator critically evaluates its own implementation before presenting the work for human review.

Validation confirms engineering correctness.

Self-Review confirms engineering discipline.

Expected Behaviour

Before reporting completion, the AI collaborator should:

Review the completed implementation against the approved Engineering Activity.

Confirm that only approved artefacts have been modified.

Verify that implementation remains within the approved scope.

Review repository differences where appropriate.

Confirm that recommendations remain separate from completed implementation.

Identify any deviations from the approved plan.

Clearly communicate any uncertainties or limitations that remain.

Validation should be appropriate to the Engineering Activity.

For example:

Documentation activities should verify scope, structure, traceability and consistency.

Governance activities should verify artefact integrity and alignment with approved governance.

Source-code activities may additionally include testing, build verification or other agreed engineering quality checks.

Validation shall provide evidence that the Engineering Activity is ready for human acceptance.

Success Criteria

Validation and Self-Review are complete when:

implementation has been independently reviewed against the approved plan;

approved scope has been preserved;

repository modifications have been verified;

remaining uncertainties have been identified; and

the Engineering Activity is ready for human review and Git operations.

8. Human Git Operations and Repository Baselining

Purpose

Human Git Operations and Repository Baselining ensure that the authoritative engineering baseline is updated through accountable human action following successful validation.

Its purpose is to preserve repository integrity, maintain engineering traceability and ensure that publication of engineering work remains an explicit human responsibility.

Repository publication is a governance activity rather than an implementation activity.

Definition

Repository Baselining is the process of incorporating validated engineering work into the authoritative engineering repository.

The accountable human engineer is responsible for determining when validated work is suitable for publication.

AI collaborators may prepare engineering work for publication but shall not independently establish a new engineering baseline unless explicitly authorised within an approved engineering environment.

Expected Behaviour

Following successful validation:

The AI collaborator shall present a completion summary.

Repository modifications shall be clearly identified.

Recommendations shall remain separate from completed implementation.

Human Git operations shall be performed by the accountable human engineer unless alternative authority has been explicitly established.

Repository publication shall preserve engineering traceability.

The published repository becomes the new authoritative engineering baseline.

Following publication, Engineering Synchronisation should establish that the published repository accurately reflects the completed Engineering Activity.

Success Criteria

Repository Baselining is complete when:

validated engineering work has been published to the authoritative repository;

engineering traceability has been preserved;

the authoritative engineering baseline has been updated;

repository synchronisation confirms publication; and

the Engineering Activity is ready to be formally closed.

9. Engineering Completion Reporting

Purpose

Engineering Completion Reporting provides a structured summary of an Engineering Activity following successful validation and prior to repository baselining.

Its purpose is to communicate completed engineering work clearly, preserve engineering traceability and enable informed human acceptance.

Completion Reporting shall distinguish completed engineering work from future engineering recommendations.

Definition

Engineering Completion Reporting is the formal communication of the outcome of an Engineering Activity.

It records what was completed, confirms adherence to the approved scope, identifies any outstanding observations and records recommendations separately from implemented work.

Completion Reporting is an engineering communication activity rather than a repository modification.

Expected Behaviour

An Engineering Completion Report should include:

A concise summary of the completed Engineering Activity.

Confirmation of the approved scope.

Confirmation of repository artefacts created, modified or left unchanged.

Confirmation that implementation remained within the approved scope.

Identification of any deviations from the approved implementation plan.

Outstanding observations requiring attention.

Recommendations for future Engineering Activities, clearly separated from completed implementation.

Confirmation that the Engineering Activity is awaiting human Git operations or has progressed to repository baselining.

Completion Reporting shall present engineering evidence objectively and avoid overstating confidence where uncertainty remains.

Success Criteria

Engineering Completion Reporting is complete when:

completed engineering work has been accurately summarised;

engineering scope has been confirmed;

repository impact has been clearly identified;

recommendations have been separated from implementation; and

the accountable human engineer has sufficient information to determine the next engineering action.

10. Lessons Learned and Continuous Improvement

Purpose

Lessons Learned and Continuous Improvement ensure that every Engineering Activity contributes to the ongoing improvement of the engineering system.

Its purpose is to preserve newly acquired engineering knowledge, improve future Engineering Activities and strengthen AIEMS through evidence-based refinement.

Engineering Activities should improve both the engineering outcome and the engineering process.

Definition

A Lesson Learned is an observation arising from an Engineering Activity that has the potential to improve future engineering practice.

Continuous Improvement is the disciplined process of evaluating those lessons and incorporating appropriate improvements into the engineering system through approved governance.

Not every observation becomes a change.

Improvements should be evidence-based, proportionate and subject to the same engineering discipline as any other Engineering Activity.

Expected Behaviour

Following completion of an Engineering Activity, the AI collaborator and accountable human engineer should consider:

What engineering practices worked well?

What engineering practices should be improved?

What assumptions proved incorrect?

What unnecessary engineering effort was identified?

What engineering knowledge should be preserved?

What future Engineering Features should be recommended?

Lessons Learned should distinguish:

observations;

recommendations;

approved improvements; and

implemented improvements.

Recommendations arising from Lessons Learned shall be recorded separately from completed Engineering Activities.

Success Criteria

Continuous Improvement is successful when:

valuable engineering knowledge has been preserved;

opportunities for improvement have been identified;

recommendations are traceable to observed evidence;

future Engineering Activities have been identified where appropriate; and

AIEMS has the opportunity to evolve without compromising governance or engineering integrity.

11. Exception Handling

Purpose

Exception Handling provides a governed mechanism for managing Engineering Activities that cannot reasonably follow the standard Engineering Activity Lifecycle.

Its purpose is to preserve engineering discipline during unusual circumstances while recognising that effective engineering sometimes requires controlled deviation from normal practice.

Exceptions shall remain visible, justified and accountable.

Definition

An engineering exception is a deliberate deviation from the standard Engineering Activity Lifecycle that has been authorised by the accountable human engineer.

Exceptions do not suspend governance.

They modify the operational approach while preserving accountability, traceability and engineering integrity.

Examples may include:

Critical incidents requiring urgent response.

Security vulnerabilities requiring immediate remediation.

Prototype or research activities.

Disaster recovery or business continuity activities.

Other exceptional engineering circumstances explicitly authorised by the accountable human engineer.

Expected Behaviour

Where an exception is required:

The reason for the exception shall be identified.

The accountable human engineer shall authorise the deviation where practicable.

The scope of the exception shall be clearly defined.

Engineering decisions shall continue to be evidence-based.

Governance shall be preserved to the greatest extent reasonably possible.

The exception and its rationale shall be documented.

A post-activity review should determine whether any temporary deviation requires follow-up Engineering Activities.

Exception Handling shall not be used to bypass governance for convenience.

Success Criteria

Exception Handling is successful when:

the engineering objective has been achieved;

governance has been preserved as far as reasonably practicable;

the rationale for the exception has been documented;

accountability has been maintained; and

lessons learned have been captured for future Engineering Activities.

12. Engineering Maturity

Purpose

Engineering Maturity describes the long-term objective of applying the AI Engineering Management System (AIEMS).

Its purpose is to define the characteristics of a Human–AI engineering capability that consistently delivers governed, evidence-based and continually improving engineering outcomes.

Engineering Maturity is not measured by the amount of AI used or the speed of delivery.

It is measured by the quality, confidence, repeatability and continual improvement of engineering outcomes.

Definition

Engineering Maturity is the capability of an engineering organisation to perform Engineering Activities consistently, transparently and accountably through disciplined collaboration between human engineers and AI collaborators.

A mature engineering capability preserves knowledge, continuously improves its engineering practices and applies governance without unnecessarily restricting engineering judgement.

Engineering Maturity is a journey rather than a fixed destination.

Characteristics of Engineering Maturity

A mature Human–AI engineering capability demonstrates the following characteristics:

Engineering decisions are evidence-based.

Governance is preserved throughout the engineering lifecycle.

Human accountability remains clear.

AI collaboration is disciplined, transparent and reviewable.

Engineering Activities are planned before implementation.

Validation precedes publication.

Lessons Learned drive continual improvement.

Engineering knowledge is preserved for future Engineering Activities.

The authoritative engineering baseline is trusted by both human engineers and AI collaborators.

Expected Behaviour

Organisations applying AIEMS should seek continual improvement rather than procedural perfection.

Engineering maturity should be reflected through:

increasing engineering confidence;

reducing unnecessary engineering effort;

improving engineering quality;

strengthening governance;

improving collaboration between human engineers and AI collaborators; and

leaving the engineering system in a better state after every Engineering Activity.

Success Criteria

Engineering Maturity is demonstrated when:

engineering outcomes are consistently reliable;

governance supports rather than constrains engineering;

engineering knowledge accumulates over time;

improvements become part of normal engineering practice; and

Human–AI collaboration continually strengthens the engineering capability of the organisation.

Engineering Maturity is achieved not by eliminating human judgement or maximising AI automation, but by combining the strengths of both through disciplined engineering practice.

Engineering Maturity is achieved not by eliminating human judgement or maximising AI automation, but by combining the strengths of both through disciplined engineering practice.

---

# Approved Scope

Create only:

```text
aiems/governance/reviews/FE-0007_APPROVED_IMPLEMENTATION_OF_PBK-0001_PART_II.md
```

---

# Out of Scope

This Engineering Feature shall not modify:

* PBK-0001.
* Architecture Decision Records.
* Engineering Reviews.
* Registers.
* Charters.
* Standards.
* Source code.
* Tests.
* Repository structure.

---

# Required Workflow

Before any future implementation of PBK-0001 Part II, the engineering activity shall:

* Review PBK-0001 Part I.
* Review FE-0006.
* Review this FE-0007 implementation package.
* Confirm the approved implementation groups.
* Produce an implementation plan.
* Wait for explicit human approval before modifying PBK-0001.

During the future implementation activity, the engineering activity shall:

* Modify only PBK-0001.
* Preserve PBK-0001 Part I.
* Implement only the approved Part II content.
* Avoid modifying registers, ADRs, reviews, charters, standards, source code, tests or repository structure.

After the future implementation activity, the engineering activity shall:

* Summarise all changes made.
* Confirm only PBK-0001 was modified.
* Confirm the implemented content matches the approved implementation design.
* Identify implementation observations separately from recommendations.
* Await human Git operations.

---

# Expected Deliverables

The deliverable of FE-0007 is this Engineering Feature artefact.

The deliverable of the future implementation activity is a populated PBK-0001 Part II section based on the approved implementation design recorded in this document.

---

# Success Criteria

FE-0007 shall be considered complete when:

* This Engineering Feature artefact has been created.
* The approved implementation groups have been recorded.
* No existing repository artefacts have been modified.
* PBK-0001 has not been modified.
* The document is ready to become the authoritative implementation package for PBK-0001 Part II.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 1.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Engineering Feature created as the authoritative implementation package for PBK-0001 Part II. |
