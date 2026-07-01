# JARVIS Capability Readiness Matrix

---

# 1. Purpose

This matrix provides a single engineering view of current JARVIS capability maturity for JARVIS product engineering after [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]].

It supports product capability prioritisation without approving implementation by itself. Approved package selection remains governed through [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and the active Engineering Session.

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
| Home Automation | Complete | Planned | Not Started | Not Started | Planned |
| Productivity | Complete | Planned | Not Started | Not Started | Planned |
| Engineering | Complete | Planned | Not Started | Not Started | Planned |
| Knowledge | Complete | Partial | Not Started | Not Started | Planned |
| Multi-device | Complete | Planned | Not Started | Not Started | Planned |
| Provider Abstraction | Complete | Planned | Not Started | Not Started | Planned |

---

# 3. Overall Programme Capability Summary

JARVIS has a strong product vision and early executable foundation.

Conversation is the most implementation-ready capability because the repository already contains a deterministic conversation path, GUI shell, service model and tests.

Most other capabilities are vision-led and architecture-aware but not implementation-ready. [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] should prioritise product engineering candidates before implementation and then select a small user-visible capability slice with clear validation evidence.

JARVIS implementation maturity remains early and foundation-level.

---

## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture source for capability intent and hierarchy. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture context for JARVIS as flagship implementation. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Current repository baseline for ESR-0007 product engineering. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Current session context for capability prioritisation. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register for candidate package selection. |
