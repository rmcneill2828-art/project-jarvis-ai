# EIP-ESR0027-002 - UXP DiagnosticsPanel Static Row Reconciliation Against UAM-0001

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0027-002 |
| Artefact ID | EIP-ESR0027-002 |
| Title | UXP DiagnosticsPanel Static Row Reconciliation Against UAM-0001 |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0077) |
| Intended Session | ESR-0027 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Implements EBG-0077: a row-by-row reconciliation of `DiagnosticsPanel`'s four permanently-static rows (`boundary`, `shell`, `agents`, `first-light`) against UAM-0001's Diagnostics Philosophy (Section 11) and the current capability roadmap - keeping honestly-labelled placeholders only for capabilities genuinely on the roadmap, removing the rest. Explicitly not a uniform "remove all placeholders" job, per EBG-0077's own framing.

---

# 3. Objective

Make the UXP more usable ahead of the planned Guardian self-awareness/introspection work (the Programme Sponsor's stated motivation at ESR-0025) by ensuring every static diagnostic row answers UAM-0001 Section 11's question - "what is available and what remains placeholder" for *this shell* - rather than surfacing content that doesn't fit that purpose.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `src/platformStatus.js` | `diagnostics` export: four static rows. Comment already notes Guardian/Sentinel/Providers were removed at ESR-0023 WP6 (EBG-0073); these four are what remained. |
| `src/App.jsx` | `DiagnosticsPanel` renders `diagnostics` via `diagnosticIcons` lookup (`boundary`, `shell`, `agents`, `first-light`). No other component reads this export. |
| UAM-0001 Section 11 (Diagnostics Philosophy) | "Diagnostics should expose implementation boundaries clearly and calmly... help reviewers and future implementers understand what is available and what remains placeholder." |
| UAM-0001 Section 14 (Colour Language) | Explicitly lists "unknown or diagnostic" as one of five valid semantic roles - `boundary`/`shell`'s `STATUS.UNKNOWN` state is this semantic, not an admission of missing information. |
| `JARVIS_CAPABILITY_READINESS_MATRIX.md` | "Engineering Agent (JARVIS-internal specialist agent) \| Complete \| Partial \| Proof of Concept only (GIA-BOOT) \| Not Started \| Planned" - confirms Agent Framework/GIA execution is genuinely not started but genuinely planned, not invented scaffolding. |
| No frontend test files exist anywhere in the repository (confirmed: `git ls-files` matches zero `*.spec.*`/`*.test.*`/Playwright files) - a separately-tracked gap (identified in an earlier repository review, not this package's scope to close). EBG-0072/EBG-0073 precedent verified UXP changes via an ad hoc live Playwright-driven headless-Chromium check against the real Vite dev server, not a committed test file - this package follows the same verification pattern. |

---

# 5. Row-by-Row Reconciliation

| Row | Current content | Judgement | Rationale |
|---|---|---|---|
| `boundary` | "Implementation Boundary" / `UNKNOWN` / "Tauri + React UXP shell" | **Keep, unchanged** | A true, structural statement about the current shell's own architecture, not a capability claim about something unbuilt. Directly serves Section 11's purpose. `UNKNOWN` correctly uses Section 14's "diagnostic" semantic, not a false "we don't know" claim. |
| `shell` | "Shell Status" / `UNKNOWN` / "Interface shell only" | **Keep, unchanged** | Same reasoning as `boundary` - an honest statement of the current foundation-scope UXP's own limits. |
| `agents` | "Agents" / `OFFLINE` / "No execution" | **Keep, unchanged** | Exactly the case EBG-0077 itself flagged as a legitimate keep: maps to the real, roadmapped Agent Framework/GIA capability, confirmed genuinely "Not Started" (not invented) by the Capability Readiness Matrix. Honestly labelled - claims no execution, which is true. |
| `first-light` | "First Light" / `OPERATIONAL` / "Python reference preserved" | **Remove** | Does not describe *this shell's* implementation boundary at all - it reports on a different, separate product (the legacy Tkinter `python -m jarvis` app) from inside the Tauri/React UXP's own diagnostics surface. Not a false statement (First Light genuinely still works), but it doesn't answer the question `DiagnosticsPanel` exists to answer per UAM-0001 Section 11, and its presence here reads as an unrelated aside rather than a diagnostic about the running shell. This is the "leftover scaffolding with nothing in the actual product vision behind it" case EBG-0077 anticipated, even though the underlying fact it reports is true. |

Net result: `DiagnosticsPanel` goes from four rows to three. No row is reworded or re-themed - the three kept rows are judged accurate as they stand.

---

# 6. Scope

This package authorises a future implementation to:

1. Remove the `first-light` entry from `src/platformStatus.js`'s `diagnostics` array.
2. Remove the corresponding `"first-light": Zap` entry from `src/App.jsx`'s `diagnosticIcons` map, and confirm `Zap` is not imported for any other use before removing its import line (Engineering Reviewer advisory).
3. Update `src/App.jsx`'s comment at line 94 - "its remaining rows (boundary, shell, agents, first-light) are permanently-static placeholders" - to read `(boundary, shell, agents)`, closing the stale-documentation gap the Engineering Reviewer flagged (v0.1 Finding 1).
4. No other row, component, or file changes - `boundary`, `shell` and `agents` are explicitly unchanged, and no backend (`jarvis/`, `sentinel/`) code is touched.
5. Verify live via the real Vite dev server (Playwright-driven headless Chromium, ad hoc per the EBG-0072/EBG-0073 precedent, not a committed test file): `DiagnosticsPanel` renders exactly three rows, zero console errors, no orphaned icon import.

---

# 7. Authorised Files

1. `src/platformStatus.js`
2. `src/App.jsx`
3. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
4. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
5. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to `boundary`, `shell` or `agents` rows - judged accurate as-is (Section 5).
2. Any change to `CapabilitySidebar`'s separate `capabilityStatuses` list (Sentinel Gateway, Platform Services, Memory, Providers, Agent Framework) - a distinct component with a distinct purpose (platform capability status, not implementation-boundary diagnostics); whether it overlaps `agents`/`agent-framework` in spirit is a separate question EBG-0077 does not ask and this package does not answer.
3. Removing or altering the legacy Tkinter First Light application (`jarvis/gui/`, `python -m jarvis`) itself - only its unrelated appearance inside the Tauri/React UXP's diagnostics surface is in scope.
4. Building committed frontend test infrastructure - the separately-tracked test-coverage gap remains out of scope; verification here follows the existing ad hoc live-Playwright-check precedent.
5. Any backend (`jarvis/`, `sentinel/`) code change.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. The three kept rows (`boundary`, `shell`, `agents`) shall not be reworded, restyled, or reordered - this package is a subtraction only, not a broader tidy-up.

---

# 10. Validation

After implementation, run:

```powershell
npm run build
```

and a live check against the real Vite dev server (`npm run dev`), confirming:

1. `DiagnosticsPanel` renders exactly three rows: Implementation Boundary, Shell Status, Agents.
2. No console errors.
3. No unused import warning for the removed `Zap` icon usage (or `Zap` remains correctly imported if used elsewhere - `AppFooter`'s quick-action button also uses `FlaskConical`/other icons; confirm `Zap` isn't referenced anywhere else in `App.jsx` before removing its import, only its `diagnosticIcons` map entry).
4. `validate_repository.py` 0 errors, same disclosed warning baseline.

---

# 11. Risks and Dependencies

## Dependencies

None - this is a self-contained frontend change with no backend dependency.

## Risks

1. **The `first-light` removal judgement is a subjective call**, not a mechanical one - unlike `boundary`/`shell`/`agents`, which have a clear UAM-0001-grounded rationale either way, "does this row belong in a diagnostics-of-this-shell panel" is a product-shape opinion. Disclosed plainly as a judgement, not a certainty, for the Engineering Reviewer and Programme Sponsor to weigh in on before approval.
2. **No committed regression test** for `DiagnosticsPanel`'s row count - relies on the same ad hoc live-check pattern already accepted for EBG-0072/EBG-0073, not a new gap this package introduces.

---

# 12. Approval Request

v0.1 reviewed by the Engineering Reviewer (Codex) via the AIEMS Exchange Bridge: "concept approved... no blocking findings." All four review questions confirmed the proposed design (first-light removal judgement sound; boundary/shell/agents correctly left unchanged; CapabilitySidebar correctly out of scope; ad hoc Playwright verification proportionate). One Low/editorial finding (a stale comment in `App.jsx` enumerating the four rows would need updating) addressed at v0.2. **Programme Sponsor approved v0.2 via `sponsor-decision` at ESR-0027 WP2.** Implemented exactly as scoped - see EBR-0001 EBG-0077 for full implementation detail and live verification evidence.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Diagnostics Philosophy (Section 11) and Colour Language (Section 14) this reconciliation is judged against. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0077 (this package's parent), EBG-0073 (precedent for the same category of DiagnosticsPanel tidy-up). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track C Near-term/Mid-term horizon context for the Guardian Orb/UXP evolution this reconciliation prepares for. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status, to record EBG-0077 completion once implemented. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Programme Sponsor approved v0.2 via `sponsor-decision` at ESR-0027 WP2. Implemented exactly as scoped: `first-light` removed from `src/platformStatus.js`'s `diagnostics` export and `src/App.jsx`'s `diagnosticIcons` map, the now-unused `Zap` import removed, the stale row-enumeration comment corrected. Verified live via an ad hoc Playwright check against the real Vite dev server (mocking the Tauri invoke bridge) - `DiagnosticsPanel` renders exactly three rows, zero console errors. `npm run build` clean. Status Draft to Approved - implemented, version 0.2 to 1.0. |
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) confirmed v0.1's concept with no blocking findings - all four review questions answered in favour of the proposed design. One Low/editorial finding addressed: added Scope item 3 requiring the stale `App.jsx` comment (line 94, still enumerating "boundary, shell, agents, first-light") to be updated once first-light is removed. Ready for Programme Sponsor approval. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0027 WP2. Row-by-row reconciliation of DiagnosticsPanel's four static rows against UAM-0001: boundary/shell/agents kept unchanged (each judged to genuinely serve UAM-0001 Section 11's diagnostics purpose or map to a real roadmapped capability), first-light proposed for removal (reports on an unrelated legacy product, not this shell's own boundary). Not yet Engineering Reviewer or Programme Sponsor reviewed. |
