# JARVIS Capability Readiness Matrix

---

# 1. Purpose

This matrix provides a single engineering view of current JARVIS capability maturity for ESR-0009 readiness after [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]].

It supports product capability prioritisation and ESR-0008 architecture validation without approving implementation by itself. Approved package selection remains governed through [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and the active Engineering Session.

---

# 2. Capability Readiness

| Capability | Vision | Architecture | Implementation | Testing | Overall Readiness |
|------------|--------|--------------|----------------|---------|-------------------|
| Conversation | Complete | Partial | Partial | Partial | Partial |
| Intelligence | Complete | Partial | Planned | Not Started | Planned |
| Memory | Complete | Partial | Not Started | Not Started | Planned |
| Voice | Complete | Partial | Not Started | Not Started | Planned |
| Vision | Complete | Partial | Not Started | Not Started | Planned |
| Guardian | Complete | Partial | Not Started | Not Started | Planned |
| Sentinel | Complete | Partial | Not Started | Not Started | Planned |
| Platform Services | Complete | Partial | Planned | Not Started | Planned |
| User Experience Platform | Complete | Partial | Partial | Partial | Partial |
| Home Automation | Complete | Planned | Not Started | Not Started | Planned |
| Productivity | Complete | Planned | Not Started | Not Started | Planned |
| Engineering Agent | Complete | Partial | Not Started | Not Started | Planned |
| Knowledge | Complete | Partial | Not Started | Not Started | Planned |
| Multi-device | Complete | Planned | Not Started | Not Started | Planned |
| Provider Architecture | Complete | Partial | Not Started | Not Started | Planned |

---

# 3. Overall Programme Capability Summary

JARVIS has a strong product vision and early executable foundation.

Conversation is the most implementation-ready capability because the repository already contains a deterministic conversation path, GUI shell, service model and tests.

ESR-0008 improved the architecture position for Guardian, Sentinel, Platform Services, User Experience Platform, Provider Architecture and the Agent Framework. These remain validation-ready rather than implementation-authorised.

Most other capabilities are vision-led and architecture-aware but not implementation-ready. ESR-0009 should validate ESR-0008 architecture outcomes before implementation package selection, then select a small user-visible capability slice with clear validation evidence.

JARVIS implementation maturity remains early and foundation-level.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture source for capability intent and hierarchy. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture context for JARVIS as flagship implementation. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline for ESR-0009 readiness. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Closed session context for Guardian, Sentinel, Platform Services, UXP, Provider Architecture and Agent Framework outcomes. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture source for ESR-0009 validation. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register for candidate package selection. |
