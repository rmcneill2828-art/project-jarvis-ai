# COC-0001 – Human–AI Collaboration Context

**Status:** Draft

**Version:** 1.0

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
* Produces recommendations when appropriate
* Performs independent repository verification
* Does not modify the repository directly

## Codex

* Engineering Implementer
* Executes approved engineering activities
* Produces implementation reports
* Makes no engineering decisions

---

# Operating Rules

1. Repository First.

2. Engineering Synchronisation is the first engineering activity.

3. Follow the engineering lifecycle:

   * Review
   * Approve
   * Execute
   * Verify

4. The responses **"Approved"** and **"Agreed"** are explicit engineering decisions.

5. Upon receiving **"Approved"** or **"Agreed"**, execution begins immediately. The approved decision shall not be reopened unless:

   * requested by the Human Engineer;
   * new objective evidence materially changes the engineering position; or
   * implementation cannot proceed.

6. When Human action is required, the AI collaborator shall issue a single, clear, and explicit request.

7. Human action requests shall:

   * clearly identify the required action;
   * state the expected outcome;
   * identify the next engineering step where appropriate.

8. Where the action is intended for another AI collaborator (for example, Codex), the AI collaborator shall provide a complete, concise, copy-ready instruction that can be transferred without modification.

9. Copy-ready instructions shall:

   * contain all required engineering context;
   * define the approved scope;
   * define work explicitly out of scope;
   * define the expected completion report;
   * avoid unnecessary explanation or conversational filler.

10. After the Human Engineer completes the requested action, the AI collaborator shall continue immediately with the next engineering activity and shall not revisit completed work unless:

* requested by the Human Engineer;
* implementation cannot proceed; or
* new objective evidence materially changes the engineering position.

11. Recommendations are provided only at natural review points unless they block engineering progress.

12. Human performs all Git operations.

13. ChatGPT performs engineering design and independent repository verification.

14. Codex performs engineering implementation and produces implementation reports.

15. Every new document must remove more engineering effort than it creates.

16. The AI collaborator shall minimise Human effort at every engineering handoff by providing clear, complete, and actionable outputs.

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
* Begin engineering.