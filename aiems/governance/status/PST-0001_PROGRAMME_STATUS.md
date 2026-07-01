# PST-0001 – Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 2.4

---

# Document Control

| Field            | Value                                              |
| ---------------- | -------------------------------------------------- |
| Artefact ID      | PST-0001                                           |
| Title            | Programme Status                                   |
| Version          | 2.4                                                |
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

This artefact complements [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]]. It does not replace AIEMS governance, registers, standards, reviews, playbooks or repository evidence.

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
| Current Mode                  | ESR-0006 repository baseline created and [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] accepted as current repository baseline |
| Current Phase                 | Repository governance activities substantially complete; engineering focus transitions back to JARVIS product engineering during ESR-0007 |
| Current Workflow              | AIEMS Engineering Workflow v3 with Engineering Implementer repository lifecycle                                 |
| Current Engineering Objective | Complete formal ESR-0006 closure from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] and return focus to JARVIS product engineering during ESR-0007. |

---

# 4. Current Engineering Workflow

The current approved workflow is AIEMS Engineering Workflow v3 with clarified authority, validation, verification and acceptance lifecycle.

Workflow sequence:

1. Engineering Planning
2. Programme Sponsor Approval
3. Implementation
4. Programme Sponsor Validation
5. Commit and Push
6. Independent Repository Verification
7. Programme Sponsor Baseline Acceptance
8. Phase Closure

[[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] is the authoritative collaboration context for this workflow.

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
    +-- Implements Approved Scope
    |
    v
Programme Sponsor Validation
    |
    v
Engineering Implementer
    |
    +-- Stages
    +-- Commits
    +-- Pushes
    +-- Reports Repository Completion
    |
    v
Engineering Reviewer
    |
    v
WP6 Independent Repository Verification
    |
    v
Programme Sponsor
    |
    v
WP7 Repository Baseline Acceptance
```

Engineering Approval authorises work. Validation provides evidence. Verification confirms implementation. Acceptance establishes engineering authority for the repository baseline.

---

# 4A. Current Engineering Focus

Repository governance activities are substantially complete.

ESR-0006 established validated working practices for Engineering Implementation Briefs, Organic Semantic Enhancement, Independent Repository Review, Repository Readiness Review, Continuous Engineering Improvements and Engineering Workspace Evaluation.

These practices are current working practices. They are not formal standards unless separately reviewed and standardised through a future approved work package.

Engineering focus transitions back to JARVIS product engineering during ESR-0007, with AIEMS, Obsidian and OSE retained as supporting engineering practices.

---

# 5. Current Capability Roadmap

| Capability              | Status      | Maturity | Notes                                                                                   |
| ----------------------- | ----------- | -------- | --------------------------------------------------------------------------------------- |
| Repository Architecture | Complete    | Complete | Repository structure, package layout and governance separation are established.         |
| Governance Framework    | In Progress | High     | Core AIEMS governance artefacts exist and are sufficient to support controlled product delivery. |
| Engineering Standards   | In Progress | High     | [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]], [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]], [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] and [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] are approved; additional build-facing standards remain planned. |
| Platform Architecture   | Planned     | Partial  | [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] exists but requires decomposition into implementable subsystem specifications. |
| JARVIS Product Architecture | Complete | High | JARVIS product vision, behaviour, principles and capability relationships are represented in the product architecture. |
| JARVIS Development      | In Progress | Early    | First Light executable skeleton exists; product capabilities remain foundation-level.   |

---

# 6. Completed Programme Milestones

| Milestone                                                      | Status   |
| -------------------------------------------------------------- | -------- |
| Repository Architecture established                            | Complete |
| Repository Integrity Review completed                          | Complete |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] Human-AI Collaboration Context updated to Workflow v3 | Complete |
| Engineering Standards Gap Review completed                     | Complete |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] Controlled Artefact Standard approved                 | Complete |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] Engineering Documentation Standard approved           | Complete |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] Software / Python Engineering Standard approved       | Complete |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] Controlled Artefact Register independently verified   | Complete |
| [[REG-0004_ACTION_REGISTER|REG-0004]] Action Register independently verified                | Complete |
| EIP-based implementation workflow validated                    | Complete |
| AIEMS governance remediation completed through ESR-0003         | Complete |
| Engineering Implementer repository lifecycle implemented        | Complete |
| HABEI research capability established                           | Complete |
| Repository baseline reviewed through EBR-0002                   | Complete |
| README.md added to WP0 synchronisation review                   | Complete |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] Validation and Quality Assurance Standard approved     | Complete |
| JARVIS product architecture established and recovered knowledge promoted | Complete |
| JARVIS First Light executable skeleton established              | Complete |
| [[ESR-0004_ENGINEERING_SESSION_REPORT|ESR-0004]] repository baseline assessed through [[RBA-0001_ESR-0004_REPOSITORY_BASELINE_ASSESSMENT|RBA-0001]]          | Complete |
| [[ESR-0004_ENGINEERING_SESSION_REPORT|ESR-0004]] repository baseline accepted through [[RBL-0004_REPOSITORY_BASELINE|RBL-0004]]          | Complete |
| JARVIS Conversation Workspace operationally validated            | Complete |
| [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]] repository baseline accepted through [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]]           | Complete |
| Repository integrity improvements completed during ESR-0006       | Complete |
| Obsidian engineering workspace evaluation completed               | Complete |
| Organic Semantic Enhancement pilot completed                      | Complete |
| Independent Repository Review completed for ESR-0006              | Complete |
| Repository Readiness Review completed for ESR-0006                | Complete |
| Repository baseline created and accepted through [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Complete |

---

# 7. Current Engineering Standards Position

| Artefact | Status   | Notes                                                                   |
| -------- | -------- | ----------------------------------------------------------------------- |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Approved | Controlled Artefact Standard approved and independently verified.       |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] | Approved | Engineering Documentation Standard approved and independently verified. |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Approved | Software / Python Engineering Standard. Baseline accepted.              |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Approved | Validation and Quality Assurance Standard.                              |
| STD-0005 | Planned  | Development Environment Standard.                                       |
| STD-0006 | Planned  | Configuration and Secrets Standard.                                     |
| STD-0008 | Planned  | Engineering Review and Assurance Standard.                              |

Validated ESR-0006 working practices:

| Working Practice | Status | Notes |
|------------------|--------|-------|
| Engineering Implementation Briefs | Current Working Practice | Used to scope and authorise ESR-0006 work packages. |
| Organic Semantic Enhancement | Current Working Practice | Applied to authorised artefacts using verified WikiLinks and preserved Markdown readability. |
| Independent Repository Review | Current Working Practice | Used to assess implementation outcomes independently before acceptance. |
| Repository Readiness Review | Current Working Practice | Used to separate implementation acceptance from baseline readiness. |
| Continuous Engineering Improvements | Current Working Practice | Used to capture AIEMS process improvements without promoting them directly to standards. |
| Engineering Workspace Evaluation | Current Working Practice | Used to evaluate Obsidian as a supporting engineering workspace. |

---

# 8. Active and Next Planned Work

| Item                         | Status                              | Notes                                                     |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------- |
| Current Engineering Session  | ESR-0006 closure preparation                      | Repository baseline accepted through [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]. |
| Current Engineering Activity | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] Repository Baseline | Accepted following ESR-0006 repository governance work. |
| [[ESR-0001_ENGINEERING_SESSION_REPORT|ESR-0001]]                     | Closed                              | Latest accepted Engineering Session Report reviewed as historical baseline. |
| [[ESR-0002_ENGINEERING_SESSION_REPORT|ESR-0002]]                     | Closed                              | Engineering Session closed with repository accepted with observations. |
| [[ESR-0003_ENGINEERING_SESSION_REPORT|ESR-0003]]                     | Closed                              | Repository baseline accepted for [[ESR-0004_ENGINEERING_SESSION_REPORT|ESR-0004]]. |
| [[ESR-0004_ENGINEERING_SESSION_REPORT|ESR-0004]]                     | Closed                              | Repository baseline accepted for [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]] handover. |
| [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]]                     | Closed                              | Operational First Light / Conversation Workspace accepted through [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]]. |
| P2-003                       | Complete                            | [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] Software / Python Engineering Standard approved. |
| Next Engineering Session     | ESR-0007 product engineering focus | Return focus to JARVIS product engineering from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]. |
| Next Recommended Activity    | ESR-0007 Engineering Synchronisation from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Review [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and select the next approved JARVIS product engineering package. |
| Current Review State         | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] accepted | ESR-0006 repository baseline ready for formal session closure. |

---

# 9. Repository Health

| Item                                | Status                             |
| ----------------------------------- | ---------------------------------- |
| Repository Health                   | Good                               |
| Repository Acceptance               | Accepted through [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Current Repository Baseline         | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Latest Repository Engineering Health Review | ESR-0006 Independent Repository Review and Repository Readiness Review |
| Baseline Review Scope               | ESR-0006 Obsidian evaluation, repository integrity improvements, OSE pilot and baseline readiness |
| Current Activity                    | ESR-0006 formal closure preparation |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

* Additional build-facing engineering standards remain planned and should be added only when they directly support delivery.
* [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] requires decomposition into implementable subsystem specifications.
* JARVIS implementation remains at First Light skeleton stage.
* JARVIS product requirements and capability backlog prioritisation should resume during ESR-0007.
* AI provider abstraction, memory/data storage, Guardian safety, local agent permissions and cost strategy remain candidate backlog topics until separately approved.
* Prototype JARVIS chat export artefacts should be addressed under future product engineering and the approved runtime chat archive direction.
* Formal AIEMS standards review, JARVIS runtime chat archive and repository integrity troubleshooting playbook items are recorded in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].

No outstanding AIEMS governance risks are recorded at this point. Remaining work relates to product engineering or separately governed candidate backlog items.

---

# 11. ESR-0006 Outcomes

1. Started from [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] accepted baseline.
2. Completed repository integrity improvements including `.obsidian/` ignore handling and `.gitattributes` line-ending control.
3. Completed Obsidian engineering workspace evaluation.
4. Completed Organic Semantic Enhancement pilot using verified WikiLinks and related artefact sections.
5. Completed Independent Repository Review and Repository Readiness Review.
6. Created and accepted [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] as the current repository baseline.
7. Recorded follow-up engineering backlog items in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].

---

# 12. ESR-0006 Success Criteria

ESR-0006 success criteria have been met:

* approved work remained traceable to accepted baseline evidence and controlled engineering briefs;
* no strategic roadmap capability was introduced without architecture and approval;
* repository health was maintained;
* the next repository baseline was independently reviewed before acceptance;
* repository governance activity reached a stable handover point for ESR-0007 product engineering.

---

# 13. Session Start Guidance

At the start of a new engineering session:

1. Review README.md for repository orientation and platform context.
2. Load [[PST-0001_PROGRAMME_STATUS|PST-0001]].
3. Review the previous Engineering Session Report.
4. Load [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].
5. Load [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
6. Perform Engineering Synchronisation.
7. Confirm the current repository baseline.
8. Confirm the current engineering objective.
9. Continue from the next approved EIP unless the Programme Sponsor directs otherwise.
10. Current recommended next activity is ESR-0007 Engineering Synchronisation from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] followed by [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] review and next-package selection.
11. Confirm the current interaction context. An active Engineering Session defaults to AIEMS Execution Mode unless the Programme Sponsor explicitly changes the context.

This allows future sessions to start from a clean conversational state while preserving programme continuity through repository evidence.

README.md introduces the repository and platform context. Controlled AIEMS artefacts remain authoritative for programme status, governance, execution and collaboration rules.

---

# 14. Maintenance

[[PST-0001_PROGRAMME_STATUS|PST-0001]] shall be reviewed and updated:

* at phase closure;
* when the active engineering phase changes;
* when the next planned EIP changes materially;
* when the capability roadmap changes;
* when a major baseline is accepted;
* when the Programme Sponsor directs an update.

[[PST-0001_PROGRAMME_STATUS|PST-0001]] should remain concise.

It shall not duplicate detailed content from controlled artefacts.

---

# Guiding Principle

> *"The repository is the programme memory. PST-0001 is the session reload point."*

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Complementary collaboration context and authoritative workflow reference. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Session start guidance directs loading this playbook. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Current accepted repository baseline for ESR-0006 closure and ESR-0007 handover. |
| [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] | Previous accepted repository baseline and ESR-0006 starting point. |
| [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]] | Previous closed engineering session and handover basis. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records ESR-0006 follow-up backlog items and future product engineering candidates. |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Current approved engineering standard position. |
| [[STD-0002_ENGINEERING_DOCUMENTATION_STANDARD|STD-0002]] | Current approved engineering standard position. |
| [[STD-0003_SOFTWARE_PYTHON_ENGINEERING_STANDARD|STD-0003]] | Current approved engineering standard position. |
| [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] | Current approved engineering standard position. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Current platform architecture position and outstanding decomposition observation. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register referenced in completed milestones and observations. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | ADR register referenced in outstanding observations. |
| [[REG-0004_ACTION_REGISTER|REG-0004]] | Action register referenced in completed milestones. |
| [[ADR-0001_DOCUMENTATION_FIRST|ADR-0001]] | Documentation-first engineering decision supporting repository-first AIEMS practice. |
| [[RBA-0001_ESR-0004_REPOSITORY_BASELINE_ASSESSMENT|RBA-0001]] | ESR-0004 baseline assessment referenced in completed milestones. |

---

# Version History

| Version | Date         | Author                                        | Summary                                                                                                                      |
| ------- | ------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 2.4     | 1 July 2026  | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0006 outcomes, RBL-0007 accepted baseline, validated working practices and ESR-0007 product engineering handover position. |
| 2.3     | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0005 closure, RBL-0006 accepted baseline and ESR-0006 planning readiness. |
| 2.2     | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Corrected authority lifecycle diagram so Programme Sponsor Validation occurs before Engineering Implementer commit and push. |
| 2.1     | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified current workflow distinction between engineering approval, validation, independent verification and Programme Sponsor baseline acceptance. |
| 2.0     | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0005 opening objectives and success criteria for engineering readiness. |
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
