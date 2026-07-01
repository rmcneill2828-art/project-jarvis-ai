# PCB-0001 - Product Capability Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PCB-0001 |
| Title | Product Capability Baseline |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[JARVIS_PRODUCT_ARCHITECTURE]] |
| Approval | Approved by Programme Sponsor |

---

# 2. Purpose

PCB-0001 records the accepted operational product baseline for JARVIS following review of repository evidence during [[ESR-0007_ENGINEERING_SESSION_REPORT]].

This artefact is an acceptance baseline. It does not replace the repository assessment, product architecture, capability readiness matrix or engineering backlog.

---

# 3. Repository Evidence

PCB-0001 is based on independently reviewed repository evidence recorded in [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]] and the accepted repository context established by [[RBL-0007_REPOSITORY_BASELINE]].

Repository validation confirmed that the following evidence artefacts exist:

- [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]]
- [[RBL-0007_REPOSITORY_BASELINE]]
- [[JARVIS_PRODUCT_ARCHITECTURE]]
- [[JARVIS_CAPABILITY_READINESS_MATRIX]]
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]]

No previous Product Capability Baseline was present before PCB-0001.

---

# 4. Accepted Product Baseline

The Programme Sponsor accepts the following as the current operational JARVIS product baseline:

| Baseline Area | Accepted Position |
|---------------|-------------------|
| First Light foundation | JARVIS has an executable First Light foundation capable of launching the current application shell. |
| Conversation Workspace | JARVIS provides an operational local conversation workspace with deterministic text responses. |
| GUI | JARVIS includes a Tkinter GUI with conversation controls, animated orb presence indicator and service status display. |
| Provider abstraction framework | JARVIS includes an initial provider protocol, orchestrator and deterministic local provider; external AI providers are not yet integrated. |
| Session lifecycle | JARVIS tracks current-session metadata and supports new conversation and clear conversation behaviour. |
| Transcript export | JARVIS supports user-initiated transcript export in Markdown and plain-text formats. |
| Health/status model | JARVIS exposes a lightweight service status and health model for current and future product services. |
| Repository governance integration | JARVIS product capability is governed through AIEMS repository evidence, controlled architecture, baseline and backlog artefacts. |

This accepted baseline shall be used as the reference point for future JARVIS product engineering unless superseded by a later accepted Product Capability Baseline.

---

# 5. Capability Maturity

The authoritative capability maturity assessment is maintained within [[JARVIS_CAPABILITY_READINESS_MATRIX]].

PCB-0001 does not duplicate the matrix. Future maturity changes shall be assessed through the authoritative matrix and accepted through appropriate AIEMS baseline or review activity.

---

# 6. Current Constraints

The accepted product baseline includes the following constraints:

- External AI providers are not integrated.
- Persistent memory is not implemented.
- Voice capability is not implemented.
- Vision capability is not implemented.
- Guardian capability is not implemented.
- Local agent capability is not implemented.
- Internet-backed assistance is not implemented.
- Runtime service health checks remain lightweight and do not yet provide active diagnostics.

These constraints are accepted baseline limitations. They are not defects in PCB-0001 and shall not be treated as implementation authority.

---

# 7. Future Engineering Direction

Future implementation priorities are governed by [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]].

PCB-0001 does not select, approve or reprioritise backlog items. Future product capability changes shall proceed only through approved engineering work packages or other Programme Sponsor authority.

---

# 8. Operational Acceptance Statement

The Programme Sponsor accepts PCB-0001 as the operational product baseline for JARVIS following ESR-0007 repository product capability assessment.

This acceptance records the current operational foundation and its known constraints. It does not approve expansion beyond the accepted baseline.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT]] | Repository product capability evidence supporting this baseline. |
| [[RBL-0007_REPOSITORY_BASELINE]] | Repository baseline context for ESR-0007 product engineering. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT]] | Engineering session context for PCB-0001 creation. |
| [[JARVIS_PRODUCT_ARCHITECTURE]] | Product architecture defining intended JARVIS direction and capability relationships. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX]] | Authoritative capability maturity assessment. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER]] | Governed source for future engineering priorities and candidate work. |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 July 2026 | Codex Engineering Implementer | Initial Product Capability Baseline created following RPCA-0001 repository product capability assessment. |
