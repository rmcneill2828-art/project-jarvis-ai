# PST-0001 – Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 1.9

---

# Document Control

| Field            | Value                                              |
| ---------------- | -------------------------------------------------- |
| Artefact ID      | PST-0001                                           |
| Title            | Programme Status                                   |
| Version          | 1.9                                                |
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
| Current Mode                  | ESR-0004 repository baseline accepted; ESR-0005 ready to commence                                             |
| Current Phase                 | Foundation Phase complete; ESR-0005 Product Capability Delivery ready                                         |
| Current Workflow              | AIEMS Engineering Workflow v3 with Engineering Implementer repository lifecycle                                 |
| Current Engineering Objective | RBL-0004 accepted at commit `9007331ae0219b9a500564adbc9cf9738bd94681`; ESR-0005 handover ready |

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
7. Engineering Implementer Repository Operations
8. WP6 Independent GitHub Verification
9. WP7 Repository Baseline Acceptance
10. Phase Closure

COC-0001 is the authoritative collaboration context for this workflow.

Repository execution separation of duties:

```text
Programme Sponsor
    |
    v
Approves Engineering Implementation
    |
    v
Engineering Implementer
    |
    +-- Implements
    +-- Stages
    +-- Commits
    +-- Pushes
    +-- Reports Repository Completion
    |
    v
Engineering Reviewer
    |
    v
WP6 Independent GitHub Verification
    |
    v
WP7 Repository Baseline Acceptance
```

---

# 5. Current Capability Roadmap

| Capability              | Status      | Maturity | Notes                                                                                   |
| ----------------------- | ----------- | -------- | --------------------------------------------------------------------------------------- |
| Repository Architecture | Complete    | Complete | Repository structure, package layout and governance separation are established.         |
| Governance Framework    | In Progress | High     | Core AIEMS governance artefacts exist and are sufficient to support controlled product delivery. |
| Engineering Standards   | In Progress | High     | STD-0001, STD-0002, STD-0003 and STD-0004 are approved; additional build-facing standards remain planned. |
| Platform Architecture   | Planned     | Partial  | MOD-0001 exists but requires decomposition into implementable subsystem specifications. |
| JARVIS Product Architecture | Complete | High | JARVIS product vision, behaviour, principles and capability relationships are represented in the product architecture. |
| JARVIS Development      | In Progress | Early    | First Light executable skeleton exists; product capabilities remain foundation-level.   |

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
| AIEMS governance remediation completed through ESR-0003         | Complete |
| Engineering Implementer repository lifecycle implemented        | Complete |
| HABEI research capability established                           | Complete |
| Repository baseline reviewed through EBR-0002                   | Complete |
| README.md added to WP0 synchronisation review                   | Complete |
| STD-0004 Validation and Quality Assurance Standard approved     | Complete |
| JARVIS product architecture established and recovered knowledge promoted | Complete |
| JARVIS First Light executable skeleton established              | Complete |
| ESR-0004 repository baseline assessed through RBA-0001          | Complete |
| ESR-0004 repository baseline accepted through RBL-0004          | Complete |

---

# 7. Current Engineering Standards Position

| Artefact | Status   | Notes                                                                   |
| -------- | -------- | ----------------------------------------------------------------------- |
| STD-0001 | Approved | Controlled Artefact Standard approved and independently verified.       |
| STD-0002 | Approved | Engineering Documentation Standard approved and independently verified. |
| STD-0003 | Approved | Software / Python Engineering Standard. Baseline accepted.              |
| STD-0004 | Approved | Validation and Quality Assurance Standard.                              |
| STD-0005 | Planned  | Development Environment Standard.                                       |
| STD-0006 | Planned  | Configuration and Secrets Standard.                                     |
| STD-0008 | Planned  | Engineering Review and Assurance Standard.                              |

---

# 8. Active and Next Planned Work

| Item                         | Status                              | Notes                                                     |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------- |
| Current Engineering Session  | ESR-0004 Ready for Final Closure     | Repository baseline accepted through RBL-0004. |
| Current Engineering Activity | RBL-0004 ESR-0004 Repository Baseline | Accepted. |
| ESR-0001                     | Closed                              | Latest accepted Engineering Session Report reviewed as historical baseline. |
| ESR-0002                     | Closed                              | Engineering Session closed with repository accepted with observations. |
| ESR-0003                     | Closed                              | Repository baseline accepted for ESR-0004. |
| ESR-0004                     | Ready for Final Closure             | Repository baseline accepted for ESR-0005 handover. |
| P2-003                       | Complete                            | STD-0003 Software / Python Engineering Standard approved. |
| Next Engineering Session     | ESR-0005 Ready                      | Product Capability Delivery ready to commence from RBL-0004. |
| Next Recommended Activity    | ESR-0005 WP0 Engineering Synchronisation and Product Capability Backlog Prioritisation | Begin from RBL-0004 and select a small executable conversation capability slice. |
| Current Review State         | RBL-0004 accepted                   | ESR-0004 repository baseline accepted for ESR-0005. |

---

# 9. Repository Health

| Item                                | Status                             |
| ----------------------------------- | ---------------------------------- |
| Repository Health                   | Good                               |
| Repository Acceptance               | Accepted for ESR-0005 handover through RBL-0004 |
| Current Repository Baseline         | RBL-0004 / `9007331ae0219b9a500564adbc9cf9738bd94681` |
| Latest Repository Engineering Health Review | RBA-0001 ESR-0004 Repository Baseline Assessment |
| Baseline Review Scope               | ESR-0004 final repository baseline, product knowledge consolidation and ESR-0005 readiness |
| Current Activity                    | ESR-0004 final closure and ESR-0005 start readiness |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

* ADR-0004 and ADR-0005 have been recovered as controlled ADR artefacts and are registered in REG-0001 and REG-0002.
* Additional build-facing engineering standards remain planned and should be added only when they directly support delivery.
* MOD-0001 requires decomposition into implementable subsystem specifications.
* JARVIS implementation remains at First Light skeleton stage.
* JARVIS product requirements and capability backlog prioritisation should open ESR-0005.
* AI provider abstraction, memory/data storage, Guardian safety, local agent permissions and cost strategy remain candidate backlog topics until separately approved.
* Repeatable local validation tooling should be confirmed early in ESR-0005.
* A future AI collaboration or engineering assurance standard may be appropriate after further workflow evidence is gathered.
* Encoding artefacts identified during EBR-0002 remain candidates for separately approved remediation.

---

# 11. Session Start Guidance

At the start of a new engineering session:

1. Review README.md for repository orientation and platform context.
2. Load PST-0001.
3. Review the previous Engineering Session Report.
4. Load PBK-0001.
5. Load COC-0001.
6. Perform Engineering Synchronisation.
7. Confirm the current repository baseline.
8. Confirm the current engineering objective.
9. Continue from the next approved EIP unless the Programme Sponsor directs otherwise.
10. Current recommended next activity is ESR-0005 WP0 Engineering Synchronisation from RBL-0004 followed by Product Capability Backlog Prioritisation.
11. Confirm the current interaction context. An active Engineering Session defaults to AIEMS Execution Mode unless the Programme Sponsor explicitly changes the context.

This allows future sessions to start from a clean conversational state while preserving programme continuity through repository evidence.

README.md introduces the repository and platform context. Controlled AIEMS artefacts remain authoritative for programme status, governance, execution and collaboration rules.

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
| 1.9     | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBL-0004 accepted ESR-0004 repository baseline and ESR-0005 readiness. |
| 1.8     | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBA-0001 ESR-0004 repository baseline assessment and ESR-0005 handover recommendation. |
| 1.7     | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded STD-0004 Validation and Quality Assurance Standard as approved. |
| 1.6     | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added README.md as the first WP0 review artefact before controlled governance artefacts. |
| 1.5     | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0003 closure and repository baseline acceptance for ESR-0004. |
| 1.4     | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Refreshed programme status following ESR-0003 completion, repository lifecycle alignment, ADR recovery and EBR-0002 baseline review. |
| 1.3     | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded AIEMS Execution Mode default behaviour, temporary context switching and live workflow change control. |
| 1.2     | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded final ESR-0002 closure wording and Engineering Session Archive reference position. |
| 1.1     | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0002 closure, repository health outcome, ESR-0003 handover and next recommended activity. |
| 1.0     | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Programme Status artefact created to preserve session continuity and reduce dependency on long conversation history. |

---
