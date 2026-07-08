# COC-0001 - Human-AI Collaboration Context

**Status:** Draft

**Version:** 1.9

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
* Approves repository changes
* Provides final approvals

## Engineering Reviewer

* Engineering Designer
* Engineering Reviewer
* Produces Engineering Implementation Packages for review and approval
* Produces recommendations when appropriate
* Performs WP6 Independent GitHub Verification after Engineering Implementer repository push
* Does not modify the repository directly

This role has been filled historically by ChatGPT and the AIEMS Engineering Agent. The role definition, not the specific AI product, is authoritative.

## Engineering Implementer

* Engineering Implementer
* Implements approved Engineering Implementation Packages
* Performs authorised repository staging, commit and push
* Performs self-review against the approved Engineering Implementation Package
* Reports commit SHA, commit message and repository status
* Produces implementation and self-review reports
* Makes no engineering decisions

This role has been filled historically by Codex and other AI collaborators, including Claude acting as both Reviewer and Implementer within a single session. The role definition, not the specific AI product, is authoritative.

---

# Operating Rules

1. Repository First.

2. Engineering Synchronisation is the first engineering activity.

3. Engineering Synchronisation is composed of two stages:

   * WP0A - Repository Synchronisation
   * WP0B - Engineering Session Initialisation

4. WP0A - Repository Synchronisation shall confirm the repository baseline before creating or continuing an Engineering Session.

   WP0A shall review README.md first for repository orientation and platform context. README introduces; controlled artefacts govern.

5. WP0B - Engineering Session Initialisation shall create or confirm the active Engineering Session only after Repository Synchronisation is complete.

6. A new Engineering Session Report shall be created during WP0B, after successful Repository Synchronisation and confirmation that the previous Engineering Session has been formally closed.

7. A new Engineering Session Report shall not be created during closure of the previous Engineering Session.

8. Only one Engineering Session shall be active at any time.

9. Previous Engineering Sessions must be completed before a new Engineering Session becomes active.

10. Programme Phases are long-running strategic milestones. Engineering Sessions are bounded operational engineering periods within a Programme Phase.

11. Follow the engineering lifecycle:

   * WP0A - Repository Synchronisation
   * WP0B - Engineering Session Initialisation
   * Planning
   * Engineering Implementation Package
   * Engineering Review
   * Human Approval
   * Implementation
   * Self-Review
   * Engineering Implementer Repository Operations
   * WP6 Independent GitHub Verification
   * WP7 Repository Baseline Acceptance
   * Phase Closure

   Working Reports may be used before Engineering Review to present findings, analysis or proposed remediation. They are not controlled repository artefacts and do not authorise repository change.

   The Engineering Implementer produces engineering reports. The Engineering Reviewer performs engineering review. The Programme Sponsor makes engineering decisions. Controlled repository artefacts are created or modified only following explicit approval.

12. The Engineering Reviewer shall produce one complete Engineering Implementation Package for each approved implementation activity.

13. The Engineering Implementation Package shall be the single reviewable implementation specification for the activity.

14. The Human Engineer shall review and approve the complete Engineering Implementation Package before implementation begins.

15. The Engineering Implementer shall use the approved Engineering Implementation Package as the sole implementation specification.

16. Engineering Implementation Packages shall contain, where applicable:

   * Engineering Context
   * Objective
   * Repository Scope
   * Engineering Constraints
   * Implementation Activities
   * Validation Requirements
   * Completion Report Requirements
   * Success Criteria

17. The responses **"Approved"** and **"Agreed"** are explicit engineering decisions.

18. Upon receiving **"Approved"** or **"Agreed"**, execution begins immediately. The approved decision shall not be reopened unless:

   * requested by the Human Engineer;
   * new objective evidence materially changes the engineering position; or
   * implementation cannot proceed.

19. When Human action is required, the AI collaborator shall issue a single, clear, and explicit request.

20. Human action requests shall:

   * clearly identify the required action;
   * state the expected outcome;
   * identify the next engineering step where appropriate.

21. Where the action is intended for another AI collaborator (for example, an Engineering Implementer AI collaborator), the AI collaborator shall provide a complete, concise, copy-ready Engineering Implementation Package or instruction that can be transferred without modification.

22. Copy-ready instructions shall:

   * contain all required engineering context;
   * define the approved scope;
   * define work explicitly out of scope;
   * define the expected completion report;
   * avoid unnecessary explanation or conversational filler.

23. AI collaborators shall use available repository access capabilities before requesting information from the Human Engineer that is already available from the repository.

24. After the Human Engineer completes the requested action, the AI collaborator shall continue immediately with the next engineering activity and shall not revisit completed work unless:

   * requested by the Human Engineer;
   * implementation cannot proceed; or
   * new objective evidence materially changes the engineering position.

25. Recommendations are provided only at natural review points unless they block engineering progress.

26. The Programme Sponsor approves engineering work, implementation scope and repository changes. The Programme Sponsor is not responsible for repository execution unless separately directed.

27. The Engineering Reviewer performs engineering design, does not perform repository implementation, performs WP6 Independent GitHub Verification and confirms WP7 Repository Baseline Acceptance.

28. The Engineering Implementer performs engineering implementation, authorised repository staging, commit and push, and reports commit SHA, commit message and repository status.

29. Repository Engineering Health Reviews shall compare findings against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], the authoritative Engineering Backlog Register.

30. Repository Engineering Health Reviews shall distinguish:

   * New Findings
   * Confirmed Existing Backlog
   * Completed Backlog Items
   * Superseded Backlog Items
   * Duplicate Backlog Items
   * New Candidate Backlog Items

31. Repository Engineering Health Reviews shall include a mandatory Backlog Validation section reporting:

   * Total Approved Backlog Items Reviewed
   * Confirmed Valid Backlog Items
   * Completed Backlog Items
   * Superseded Backlog Items
   * Duplicate Backlog Items
   * New Candidate Backlog Items
   * Recommendation on whether [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] requires updating

32. The Engineering Reviewer shall not modify [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] during a Repository Engineering Health Review.

33. Repository Engineering Health Review recommendations remain advisory only until reviewed and approved by the Programme Sponsor.

34. Final Repository Engineering Health Reviews shall include Engineering Handover to Next Session guidance covering:

   * Recommended first Engineering Implementation Package for the next Engineering Session
   * Alternative engineering priorities
   * Dependencies
   * Risks
   * Items explicitly not recommended
   * Suggested Engineering Session objective

35. Final Repository Engineering Health Reviews shall include Backlog Progression Analysis by examining [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and recommending activities that best progress Project JARVIS AI during the next Engineering Session.

36. Backlog Progression Analysis shall consider dependencies between backlog items, engineering sequencing, governance maturity, repository readiness, engineering risk, engineering benefit, estimated implementation effort, opportunities to complete related backlog items within the same session, and backlog acceleration opportunities.

37. Each recommended backlog activity shall include backlog item reference, priority, engineering benefit, estimated effort, dependencies, recommended Engineering Session and rationale.

38. Repository Engineering Health Reviews shall identify Backlog Acceleration Opportunities where grouping related backlog items within the same Engineering Session would reduce repeated verification, reduce baseline overhead or improve engineering flow without weakening governance.

39. Final Repository Engineering Health Reviews shall include a JARVIS Development Readiness Assessment answering: "Based on the current repository baseline, engineering maturity, and approved backlog, when should development of Project JARVIS AI commence, and what evidence supports that recommendation?"

40. JARVIS Development Readiness Assessment shall consider AIEMS governance maturity, repository governance, engineering workflow maturity, standards maturity, repository verification capability, outstanding governance backlog, outstanding technical debt, repository stability, engineering repeatability and quality assurance capability.

41. The reviewer shall recommend one of: Continue AIEMS engineering only; Begin JARVIS Proof of Concept; Begin JARVIS Foundation Development; Begin Parallel AIEMS and JARVIS Development; AIEMS sufficiently mature for full JARVIS Engineering.

42. If JARVIS development is recommended, the reviewer shall identify the recommended Engineering Session, proposed objective, prerequisite backlog items, governance work that can continue in parallel and recommended first JARVIS engineering activity.

43. All handover, backlog progression and JARVIS readiness recommendations are advisory only; the Programme Sponsor determines engineering priorities; no Engineering Implementation Package shall be created or executed from these recommendations without Programme Sponsor approval.

44. Every new document must remove more engineering effort than it creates.

45. The AI collaborator shall minimise Human effort at every engineering handoff by providing clear, complete, and actionable outputs.

46. An active Engineering Session places the Engineering Reviewer in AIEMS Execution Mode by default.

47. In AIEMS Execution Mode, the Engineering Reviewer shall follow the approved AIEMS workflow and shall not alter live engineering execution based on process improvement discussion, architectural recommendation or workflow optimisation unless the Programme Sponsor explicitly approves the change and instructs that it take effect.

48. The Programme Sponsor may temporarily change interaction context using explicit mode language such as CONV, REVIEW or AUTHOR.

49. Temporary context changes do not amend AIEMS unless separately approved.

50. When the temporary context ends, AIEMS Execution Mode automatically resumes unless the Programme Sponsor instructs otherwise.

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

* Review [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]].
* Review README.md for repository orientation and platform context.
* Load this Collaboration Context.
* Perform WP0A - Repository Synchronisation.
* Perform WP0B - Engineering Session Initialisation where a new or active Engineering Session must be confirmed.
* Confirm the current engineering objective.
* Confirm whether an Engineering Implementation Package is required.
* Confirm whether AIEMS changed during the previous session before closure.
* Begin the approved engineering activity.

---

# Related Artefacts

* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] defines implementation behaviour and complements this collaboration context.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status for engineering session reload and synchronisation.
* [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] records the current accepted repository baseline and ESR-0009 handover point.
* [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] records the closed architecture evaluation session that established ESR-0009 readiness.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] is the authoritative backlog reference for Repository Engineering Health Reviews.
* [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]] defines validation and quality assurance expectations relevant to repository review.
* [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] defines the knowledge tier structure that PBK-0001's session initialisation and WP0A guidance apply.

---

# OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines how OSE relationship updates are applied to current operating artefacts. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation as the current WP0 working practice. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Playbook governing Engineering Implementer behaviour that complements COC-0001. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status used for session reload and synchronisation. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline for ESR-0009 readiness. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Closed session report that hands over to ESR-0009 validation readiness. |

---
# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.9 | 8 July 2026 | Claude Engineering Implementer | Renamed the ChatGPT/Codex role headers and normative rules to Engineering Reviewer/Engineering Implementer, decoupling role definitions from named AI products. Historical mentions elsewhere in the repository are unaffected. |
| 1.8 | 8 July 2026 | Claude Engineering Implementer | Added GDE-0001 cross-reference following introduction of knowledge tiering in PBK-0001. ESR-0014 post-closure work per ESR-0014A. |
| 1.7 | 2 July 2026 | Codex Engineering Implementer | Added OSE relationships and aligned session start context with RBL-0009 and ESR-0009 readiness. |
| 1.6 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added README.md as the first WP0 review artefact for repository orientation while preserving controlled artefact authority. |
| 1.5 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Repository lifecycle aligned with validated Engineering Implementer workflow following ESR-0003. |
| 1.4 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified Working Report lifecycle position and review, approval and implementation authority gates. |
| 1.3 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded AIEMS Execution Mode default behaviour, temporary context switching and live workflow change control. |
