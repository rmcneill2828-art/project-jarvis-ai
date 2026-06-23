# Document Register

---

## Document Control

| Field          | Value                             |
| -------------- | --------------------------------- |
| Document ID    | PJAI-0000                         |
| Document Title | Document Register                 |
| Version        | 1.0                               |
| Status         | Approved Baseline                 |
| Owner          | Project Sponsor & Chief Architect |
| Programme      | Project JARVIS AI                 |
| Product        | JARVIS OS                         |
| Classification | Internal                          |
| Last Updated   | 23 June 2026                      |
| Next Review    | Phase Gate Review                 |

---

# 1. Purpose

The Document Register is the authoritative source for document control within Project JARVIS AI.

It defines the document numbering scheme, naming standards, versioning approach and the register of all controlled project documentation.

This document shall be consulted before creating any new controlled document.

---

# 2. Document Control Standard

## 2.1 Naming Convention

All controlled documents shall follow the naming standard:

```text
<Document ID>_<DOCUMENT_NAME>.md
```

Example:

```text
PJAI-0001_PROJECT_CHARTER.md
PJAI-1001_MASTER_SPECIFICATION.md
PJAI-0003_ADR_REGISTER.md
```

---

## 2.2 Repository Structure

Repository folder numbers organise content.

Document IDs identify controlled documents.

These numbering systems are independent.

Example:

```text
docs/
├── 0000-Governance/
├── 0100-Architecture/
└── 0900-Engineering-Knowledge/
```

is separate from

```text
PJAI-0001
PJAI-1001
ADR-0001
```

---

## 2.3 Versioning Standard

| Version | Meaning                 |
| ------- | ----------------------- |
| 0.x     | Draft                   |
| 1.0     | First Approved Baseline |
| 1.x     | Minor approved revision |
| 2.0+    | Major approved revision |

---

# 3. Document Numbering Scheme

| Range          | Category                 | Status   |
| -------------- | ------------------------ | -------- |
| PJAI-0000–0099 | Governance               | Active   |
| PJAI-1000–1999 | Architecture             | Active   |
| PJAI-2000–2999 | Security                 | Reserved |
| PJAI-3000–3999 | Development Standards    | Reserved |
| PJAI-4000–4999 | Technical Specifications | Reserved |
| PJAI-5000–5999 | User Documentation       | Reserved |
| PJAI-6000–6999 | Operations               | Reserved |
| PJAI-7000–7999 | Research                 | Reserved |
| PJAI-8000–8999 | Archive                  | Reserved |
| PJAI-9000–9999 | Engineering Knowledge    | Active   |

Architecture Decision Records (ADRs) use an independent numbering scheme:

```text
ADR-0001
ADR-0002
ADR-0003
```

---

# 4. Document Lifecycle

All controlled documents follow the lifecycle below:

```text
Draft
   │
   ▼
Review
   │
   ▼
Approved Baseline
   │
   ▼
Revision
```

Document IDs are allocated once and shall never be reused.

Retired documents retain their original identifier for traceability.

---

# 5. Controlled Document Register

| Document ID | Title                    | Location          | Owner           | Status   |
| ----------- | ------------------------ | ----------------- | --------------- | -------- |
| PJAI-0000   | Document Register        | 0000-Governance   | Joint           | Approved |
| PJAI-0001   | Project Charter          | 0000-Governance   | Project Sponsor | Approved |
| PJAI-0002   | Engineering Constitution | 0000-Governance   | Joint           | Approved |
| PJAI-0003   | ADR Register             | 0000-Governance   | Joint           | Approved |
| PJAI-1001   | Master Specification     | 0100-Architecture | Chief Architect | Approved |

---

# 6. Governance Rules

The following rules apply to all controlled documents:

* Every controlled document shall have a unique Document ID.
* Document IDs shall never be reused.
* Every document shall have a defined owner.
* Every approved document shall include document control information.
* Significant engineering decisions shall be recorded using ADRs.
* Controlled documents shall be maintained within Git.
* Changes to approved documents shall be reviewed before implementation.
* The filename, document title and Document ID shall always match.

---

# 7. Responsibilities

## Project Sponsor

Responsible for:

* Governance approval.
* Document approval.
* Business ownership.
* Strategic direction.

---

## Chief Architect

Responsible for:

* Technical authorship.
* Document quality.
* Architecture consistency.
* Engineering standards.

---

# 8. Revision History

| Version | Date         | Description                |
| ------- | ------------ | -------------------------- |
| 1.0     | 23 June 2026 | Initial approved baseline. |

---

# End of Approved Content

Any content below this point is considered draft until formally approved.
