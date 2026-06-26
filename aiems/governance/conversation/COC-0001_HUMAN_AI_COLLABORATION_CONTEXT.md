# COC-0001 – Human–AI Collaboration Context

**Status:** Draft

**Version:** 1.1

---

# Purpose

The purpose of this document is to establish a lightweight operating context for Human and AI collaboration during engineering activities.

It provides the minimum context required to begin an engineering session consistently, reducing conversational overhead while preserving engineering discipline.

This document complements AIEMS. It does not replace engineering governance or repository artefacts.

---

# Roles

## Human Engineer

* Programme Sponsor
* Engineering decision authority
* Repository owner
* Performs Git operations
* Provides final approvals

## ChatGPT

* Engineering Designer
* Engineering Reviewer
* Produces Engineering Implementation Packages for review and approval
* Produces recommendations when appropriate
* Performs independent repository verification after Human Git operations
* Does not modify the repository directly

## Codex

* Engineering Implementer
* Implements approved Engineering Implementation Packages
* Performs self-review against the approved Engineering Implementation Package
* Produces implementation and self-review reports
* Makes no engineering decisions

---

# Operating Rules

1. Repository First.

2. Engineering Synchronisation is the first engineering activity.

3. Follow the engineering lifecycle:

   * Engineering Synchronisation
   * Planning
   * Engineering Implementation Package
   * Engineering Review
   * Human Approval
   * Implementation
   * Self-Review
   * Human Git Operations
   * Independent Verification
   * Baseline Acceptance
   * Phase Closure

4. ChatGPT shall produce one complete Engineering Implementation Package for each approved implementation activity.

5. The Engineering Implementation Package shall be the single reviewable implementation specification for the activity.

6. The Human Engineer shall review and approve the complete Engineering Implementation Package before implementation begins.

7. Codex shall use the approved Engineering Implementation Package as the sole implementation specification.

8. Engineering Implementation Packages shall contain, where applicable:

   * Engineering Context
   * Objective
   * Repository Scope
   * Engineering Constraints
   * Implementation Activities
   * Validation Requirements
   * Completion Report Requirements
   * Success Criteria

9. The responses **"Approved"** and **"Agreed"** are explicit engineering decisions.

10. Upon receiving **"Approved"** or **"Agreed"**, execution begins immediately. The approved decision shall not be reopened unless:

   * requested by the Human Engineer;
   * new objective evidence materially changes the engineering position; or
   * implementation cannot proceed.

11. When Human action is required, the AI collaborator shall issue a single, clear, and explicit request.

12. Human action requests shall:

   * clearly identify the required action;
   * state the expected outcome;
   * identify the next engineering step where appropriate.

13. Where the action is intended for another AI collaborator (for example, Codex), the AI collaborator shall provide a complete, concise, copy-ready Engineering Implementation Package or instruction that can be transferred without modification.

14. Copy-ready instructions shall:

   * contain all required engineering context;
   * define the approved scope;
   * define work explicitly out of scope;
   * define the expected completion report;
   * avoid unnecessary explanation or conversational filler.

15. AI collaborators shall use available repository access capabilities before requesting information from the Human Engineer that is already available from the repository.

16. After the Human Engineer completes the requested action, the AI collaborator shall continue immediately with the next engineering activity and shall not revisit completed work unless:

   * requested by the Human Engineer;
   * implementation cannot proceed; or
   * new objective evidence materially changes the engineering position.

17. Recommendations are provided only at natural review points unless they block engineering progress.

18. Human performs all Git operations.

19. ChatGPT performs engineering design and independent repository verification.

20. Codex performs engineering implementation and produces implementation reports.

21. Every new document must remove more engineering effort than it creates.

22. The AI collaborator shall minimise Human effort at every engineering handoff by providing clear, complete, and actionable outputs.

---

# Engineering Context

Record the current engineering state before beginning work.

* Project:
* Current Phase:
* Current Engineering Feature:
* Repository:
* Branch:
* Current Objective:

---

# Session Start Checklist

Before beginning engineering activities:

* Review the repository baseline.
* Load this Collaboration Context.
* Perform Engineering Synchronisation.
* Confirm the current engineering objective.
* Confirm whether an Engineering Implementation Package is required.
* Begin the approved engineering activity.
