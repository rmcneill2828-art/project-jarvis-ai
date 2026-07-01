# PST-0001 - Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 2.5

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PST-0001 |
| Title | Programme Status |
| Version | 2.5 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | At phase closure or engineering session transition |
| Effective Date | 1 July 2026 |
| Next Review | At next phase closure or ESR-0008 transition |

---

# 1. Purpose

This artefact records the current programme status for Project JARVIS AI.

It exists to provide a concise engineering context snapshot at the start of future engineering sessions.

PST-0001 supports faster session start-up by preserving the current programme state without requiring long conversation history to be reloaded.

Repository evidence remains authoritative over conversational memory.

---

# 2. Scope

This artefact records:

- current programme phase;
- current engineering workflow;
- current capability roadmap;
- completed engineering milestones;
- active and next planned engineering work;
- current repository and product baselines;
- outstanding observations;
- session start guidance.

This artefact does not record detailed engineering decisions. Detailed decisions remain in controlled artefacts, accepted baselines, registers, standards, reviews and session reports.

---

# 3. Current Programme State

| Item | Current State |
|------|---------------|
| Project | Project JARVIS AI |
| Engineering System | AI Engineering Management System (AIEMS) |
| Repository | project-jarvis-ai |
| Primary Branch | main |
| Current Mode | ESR-0007 closed; ESR-0008 readiness established. |
| Current Repository Baseline | [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] accepted as current repository baseline. |
| Current Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] accepted as current operational JARVIS product baseline. |
| Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] completed and accepted. |
| Current Phase | JARVIS product engineering continuation from accepted product capability baseline. |
| Current Workflow | AIEMS Engineering Workflow v3 with Repository-First Engineering Protocol working practice. |
| Current Engineering Objective | Prepare ESR-0008 to validate and, if approved, implement the JARVIS Runtime Chat Archive candidate EBG-0039. |

---

# 4. Current Engineering Workflow

The current approved workflow remains AIEMS Engineering Workflow v3 with clarified authority, validation, verification and acceptance lifecycle.

Workflow sequence:

1. Engineering Planning
2. Programme Sponsor Approval
3. Implementation
4. Programme Sponsor Validation
5. Commit and Push
6. Independent Repository Verification
7. Programme Sponsor Baseline Acceptance
8. Phase Closure

ESR-0007 added the following accepted working practices pending future standards review:

| Working Practice | Status | Notes |
|------------------|--------|-------|
| Repository-First Engineering Protocol (RFEP) | Accepted ESR-0007 working practice | Repository evidence is the primary engineering memory. |
| Repository-First Decision Protocol (RFDP) | Accepted ESR-0007 working practice | Engineering decisions are grounded in controlled artefacts and executable evidence. |
| Continuous Repository Synchronisation | Accepted ESR-0007 working practice | Session, status, register and baseline artefacts are synchronised at closure. |

These practices are not formal AIEMS standards unless separately reviewed and standardised through future approved work.

---

# 4A. Current Engineering Focus

ESR-0007 is closed.

The current engineering focus transitions to ESR-0008 readiness. ESR-0008 should begin with Repository-First Synchronisation, then validate EBG-0039 JARVIS Runtime Chat Archive as the recommended next engineering candidate.

EBG-0039 is a recommended candidate only. Implementation is not authorised by PST-0001.

---

# 5. Current Capability Roadmap

| Capability | Status | Maturity | Notes |
|------------|--------|----------|-------|
| Repository Architecture | Complete | Complete | Repository structure, package layout and governance separation are established. |
| Governance Framework | In Progress | High | Core AIEMS governance artefacts support controlled product delivery. |
| Engineering Standards | In Progress | High | Approved standards remain in place; RFEP, RFDP and Continuous Repository Synchronisation are working practices pending any future standards review. |
| JARVIS Product Architecture | Complete | High | [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] remains the product architecture authority. |
| JARVIS Product Capability Baseline | Accepted | Foundation | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational product baseline. |
| JARVIS Capability Maturity | Maintained | Early | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] remains the authoritative maturity model. |
| JARVIS Development | In Progress | Early | First Light / Conversation Workspace is accepted as the current operational foundation. |

---

# 6. Completed Programme Milestones

| Milestone | Status |
|-----------|--------|
| Repository Architecture established | Complete |
| Repository Integrity Review completed | Complete |
| AIEMS Engineering Workflow v3 established | Complete |
| Engineering standards baseline established | Complete |
| JARVIS product architecture established | Complete |
| JARVIS First Light executable skeleton established | Complete |
| JARVIS Conversation Workspace operationally validated | Complete |
| Repository baseline accepted through [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Complete |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] Repository Product Capability Assessment completed | Complete |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] Product Capability Baseline accepted | Complete |
| Repository-First Engineering Protocol adopted as ESR-0007 working practice | Complete |
| Repository-First Decision Protocol adopted as ESR-0007 working practice | Complete |
| Continuous Repository Synchronisation adopted as ESR-0007 working practice | Complete |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] accepted as ESR-0007 repository baseline | Complete |
| ESR-0007 closed | Complete |

---

# 7. Current Engineering Standards Position

Approved standards remain current. ESR-0007 methodology outcomes are working practices only and shall not be treated as standards unless promoted through future approved standards review.

---

# 8. Active and Next Planned Work

| Item | Status | Notes |
|------|--------|-------|
| Current Engineering Session | ESR-0007 closed | Closure recorded in [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]]. |
| Current Repository Baseline | [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Accepted ESR-0007 repository baseline. |
| Current Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational JARVIS product baseline. |
| Current Review State | ESR-0008 readiness | Repository is prepared for next-session synchronisation. |
| Next Recommended Candidate | EBG-0039 JARVIS Runtime Chat Archive | Candidate should be validated during ESR-0008 before implementation authority is assumed. |
| Authoritative Backlog Source | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Future engineering priorities remain governed by the backlog register. |

---

# 9. Repository Health

| Item | Status |
|------|--------|
| Repository Health | Good |
| Repository Acceptance | Accepted through [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] |
| Current Repository Baseline | [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] |
| Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Latest Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] |
| Current Activity | ESR-0008 readiness and next-candidate validation preparation |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

- EBG-0039 JARVIS Runtime Chat Archive is the recommended next engineering candidate for ESR-0008 validation.
- External AI providers, persistent memory, voice, vision, Guardian, local agent and internet-backed assistance remain outside the accepted operational product baseline.
- RFEP, RFDP and Continuous Repository Synchronisation may be considered in a future formal AIEMS standards review.
- JARVIS future knowledge capability should be explored from ESR-0008 onward, subject to approved scope.
- Governed domain memory remains a future architectural consideration only and is not promoted to backlog or architecture by ESR-0007 closure.

---

# 11. ESR-0007 Outcomes

1. Started from [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] accepted baseline.
2. Completed [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]].
3. Completed and accepted [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]].
4. Preserved [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] as the authoritative maturity model.
5. Preserved [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] as the authoritative backlog source.
6. Adopted RFEP, RFDP and Continuous Repository Synchronisation as ESR-0007 working practices.
7. Selected EBG-0039 JARVIS Runtime Chat Archive as the next engineering candidate.
8. Created and accepted [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]].

---

# 12. ESR-0007 Success Criteria

ESR-0007 success criteria have been met:

- repository product capability was assessed using executable repository evidence;
- the first Product Capability Baseline was accepted;
- capability maturity remained in the authoritative matrix rather than being duplicated;
- future work remained governed through [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]];
- repository-first methodology outcomes were recorded as working practices, not standards;
- ESR-0008 readiness was established without creating an ESR-0008 artefact prematurely.

---

# 13. Session Start Guidance

At the start of ESR-0008:

1. Perform Repository-First Synchronisation.
2. Review [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]].
3. Review [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]].
4. Review [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]].
5. Review [[PST-0001_PROGRAMME_STATUS|PST-0001]].
6. Review [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].
7. Review [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].
8. Validate EBG-0039 JARVIS Runtime Chat Archive as the recommended next engineering candidate.
9. Confirm approved scope before implementation.

This guidance is textual handover only. No ESR-0008 Engineering Session Report exists at ESR-0007 closure.

---

# 14. Maintenance

[[PST-0001_PROGRAMME_STATUS|PST-0001]] shall be reviewed and updated:

- at phase closure;
- when the active engineering phase changes;
- when the next planned engineering activity changes materially;
- when the capability roadmap changes;
- when a major baseline is accepted;
- when the Programme Sponsor directs an update.

PST-0001 should remain concise and must not duplicate detailed controlled artefacts.

---

# Guiding Principle

> *"The repository is the programme memory. PST-0001 is the session reload point."*

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Closed engineering session that established ESR-0008 readiness. |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Current accepted repository baseline. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Previous accepted repository baseline and ESR-0007 starting point. |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Repository product capability assessment completed during ESR-0007. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Current accepted product capability baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog source and EBG-0039 candidate source. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture context for JARVIS engineering. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Authoritative capability maturity model. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register updated for ESR-0007 closure. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.5 | 1 July 2026 | Codex Engineering Implementer | Recorded ESR-0007 closure, RBL-0008 acceptance, PCB-0001 acceptance, RPCA-0001 completion, repository-first working practices and ESR-0008 readiness. |
| 2.4 | 1 July 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0006 outcomes, RBL-0007 accepted baseline, validated working practices and ESR-0007 product engineering handover position. |
| 2.3 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0005 closure, RBL-0006 accepted baseline and ESR-0006 planning readiness. |
| 2.2 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Corrected authority lifecycle diagram so Programme Sponsor Validation occurs before Engineering Implementer commit and push. |
| 2.1 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified current workflow distinction between engineering approval, validation, independent verification and Programme Sponsor baseline acceptance. |
| 2.0 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0005 opening objectives and success criteria for engineering readiness. |
| 1.9 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBL-0004 accepted ESR-0004 repository baseline and ESR-0005 readiness. |
| 1.8 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBA-0001 ESR-0004 repository baseline assessment and ESR-0005 handover recommendation. |
| 1.7 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded STD-0004 Validation and Quality Assurance Standard as approved. |
| 1.6 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added README.md as the first WP0 review artefact before controlled governance artefacts. |
| 1.5 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0003 closure and repository baseline acceptance for ESR-0004. |
| 1.4 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Refreshed programme status following ESR-0003 completion, repository lifecycle alignment, ADR recovery and EBR-0002 baseline review. |
| 1.3 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded AIEMS Execution Mode default behaviour, temporary context switching and live workflow change control. |
| 1.2 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded final ESR-0002 closure wording and Engineering Session Archive reference position. |
| 1.1 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0002 closure, repository health outcome, ESR-0003 handover and next recommended activity. |
| 1.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Programme Status artefact created to preserve session continuity and reduce dependency on long conversation history. |
