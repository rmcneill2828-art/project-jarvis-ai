# PST-0001 – Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 1.1

---

# Document Control

| Field            | Value                                              |
| ---------------- | -------------------------------------------------- |
| Artefact ID      | PST-0001                                           |
| Title            | Programme Status                                   |
| Version          | 1.1                                                |
| Status           | Approved                                           |
| Owner            | Programme Sponsor & Chief Engineering Advisor      |
| Approved By      | Programme Sponsor                                  |
| Classification   | Internal                                           |
| Review Frequency | At phase closure or engineering session transition |
| Effective Date   | 26 June 2026                                       |
| Next Review      | At next phase closure                              |

---

# 1. Purpose

This artefact records the current programme status for Project JARVIS AI.

It exists to provide a concise engineering context snapshot at the start of future engineering sessions.

PST-0001 supports faster session start-up by preserving the current programme state without requiring long conversation history to be reloaded.

This artefact complements COC-0001. It does not replace AIEMS governance, registers, standards, reviews, playbooks or repository evidence.

---

# 2. Scope

This artefact records:

* current programme phase;
* current engineering workflow;
* current capability roadmap;
* completed engineering milestones;
* active and next planned Engineering Implementation Packages;
* current baseline status;
* outstanding observations;
* session start guidance.

This artefact does not record detailed engineering decisions. Detailed decisions remain in ADRs, registers, standards, reviews, playbooks and other controlled artefacts.

---

# 3. Current Programme State

| Item                          | Current State                                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Project                       | Project JARVIS AI                                                                                               |
| Engineering System            | AI Engineering Management System (AIEMS)                                                                        |
| Repository                    | project-jarvis-ai                                                                                               |
| Primary Branch                | main                                                                                                            |
| Current Mode                  | Governance-led engineering moving into engineering standards completion                                         |
| Current Phase                 | Phase 2 – Engineering Standards                                                                                 |
| Current Workflow              | AIEMS Engineering Workflow v3                                                                                   |
| Current Engineering Objective | ESR-0002 closure complete; next recommended activity EBG-0005 |

---

# 4. Current Engineering Workflow

The current approved workflow is AIEMS Engineering Workflow v3.

Workflow sequence:

1. Engineering Synchronisation
2. Planning and Scope Agreement
3. Engineering Implementation Package
4. Human Engineering Review
5. Human Approval
6. Codex Implementation and Self-Review
7. Human Git Commit and Push
8. Independent Repository Verification
9. Baseline Acceptance
10. Phase Closure

COC-0001 is the authoritative collaboration context for this workflow.

---

# 5. Current Capability Roadmap

| Capability              | Status      | Maturity | Notes                                                                                   |
| ----------------------- | ----------- | -------- | --------------------------------------------------------------------------------------- |
| Repository Architecture | Complete    | Complete | Repository structure, package layout and governance separation are established.         |
| Governance Framework    | In Progress | High     | Core AIEMS governance artefacts exist and are stabilising.                              |
| Engineering Standards   | In Progress | High     | STD-0001, STD-0002 and STD-0003 are approved; additional build-facing standards remain planned. |
| Platform Architecture   | Planned     | Partial  | MOD-0001 exists but requires decomposition into implementable subsystem specifications. |
| JARVIS Development      | Planned     | Early    | JARVIS lifecycle skeleton exists; product capabilities are not yet implemented.         |

---

# 6. Completed Programme Milestones

| Milestone                                                      | Status   |
| -------------------------------------------------------------- | -------- |
| Repository Architecture established                            | Complete |
| Repository Integrity Review completed                          | Complete |
| COC-0001 Human-AI Collaboration Context updated to Workflow v3 | Complete |
| Engineering Standards Gap Review completed                     | Complete |
| STD-0001 Controlled Artefact Standard approved                 | Complete |
| STD-0002 Engineering Documentation Standard approved           | Complete |
| STD-0003 Software / Python Engineering Standard approved       | Complete |
| REG-0001 Controlled Artefact Register independently verified   | Complete |
| REG-0004 Action Register independently verified                | Complete |
| EIP-based implementation workflow validated                    | Complete |

---

# 7. Current Engineering Standards Position

| Artefact | Status   | Notes                                                                   |
| -------- | -------- | ----------------------------------------------------------------------- |
| STD-0001 | Approved | Controlled Artefact Standard approved and independently verified.       |
| STD-0002 | Approved | Engineering Documentation Standard approved and independently verified. |
| STD-0003 | Approved | Software / Python Engineering Standard. Baseline accepted.              |
| STD-0004 | Planned  | Engineering Verification or Validation and Quality Assurance Standard.  |
| STD-0005 | Planned  | Development Environment Standard.                                       |
| STD-0006 | Planned  | Configuration and Secrets Standard.                                     |
| STD-0008 | Planned  | Engineering Review and Assurance Standard.                              |

---

# 8. Active and Next Planned Work

| Item                         | Status                              | Notes                                                     |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------- |
| Current Engineering Session  | ESR-0002 Completed                  | Engineering Session closed with repository accepted with observations. |
| Current Engineering Activity | ESC-0002 Formal Engineering Session Closure | Completed. |
| P2-003                       | Complete                            | STD-0003 Software / Python Engineering Standard approved. |
| Next Engineering Session     | ESR-0003 Planned                    | Next session identifier. |
| Next Recommended Activity    | EBG-0005                            | REG-0001 metadata alignment following P2-004A. |
| Current Review State         | Final ESR-0002 health review completed | Repository health reviewed as Good. |

---

# 9. Repository Health

| Item                                | Status                             |
| ----------------------------------- | ---------------------------------- |
| Repository Health                   | Good                               |
| Repository Acceptance               | Accepted with observations         |
| Latest Repository Engineering Health Review | ESR-0002 Final Repository Engineering Health Review |
| Current Activity                    | ESR-0002 closed; ESR-0003 planned  |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

* ADR-0004 and ADR-0005 remain historically referenced but corresponding artefact files are absent.
* Additional build-facing engineering standards are required before substantive JARVIS development.
* MOD-0001 requires decomposition into implementable subsystem specifications.
* JARVIS remains at lifecycle skeleton stage.
* A future AI collaboration or engineering assurance standard may be appropriate after further workflow evidence is gathered.

---

# 11. Session Start Guidance

At the start of a new engineering session:

1. Load COC-0001.
2. Load PST-0001.
3. Perform Engineering Synchronisation.
4. Confirm the current repository baseline.
5. Confirm the current engineering objective.
6. Continue from the next approved EIP unless the Programme Sponsor directs otherwise.
7. Current recommended first ESR-0003 EIP is EBG-0005, subject to Programme Sponsor approval.

This allows future sessions to start from a clean conversational state while preserving programme continuity through repository evidence.

---

# 12. Maintenance

PST-0001 shall be reviewed and updated:

* at phase closure;
* when the active engineering phase changes;
* when the next planned EIP changes materially;
* when the capability roadmap changes;
* when a major baseline is accepted;
* when the Programme Sponsor directs an update.

PST-0001 should remain concise.

It shall not duplicate detailed content from controlled artefacts.

---

# Guiding Principle

> *"The repository is the programme memory. PST-0001 is the session reload point."*

---

# Version History

| Version | Date         | Author                                        | Summary                                                                                                                      |
| ------- | ------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1.1     | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0002 closure, repository health outcome, ESR-0003 handover and next recommended activity. |
| 1.0     | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Programme Status artefact created to preserve session continuity and reduce dependency on long conversation history. |

---