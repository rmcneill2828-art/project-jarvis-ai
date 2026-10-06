# RSC-0001 - v1.0 Readiness Scorecard

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RSC-0001 |
| Title | v1.0 Readiness Scorecard |
| Version | 2.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 (Minimum Lovable Product) |
| Approval | Approved by Programme Sponsor |

---

# 2. Purpose

RSC-0001 records a pass/fail-per-capability assessment of JARVIS against the Minimum Lovable Product (MLP 0.1) defined in [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5 - the artefact's own stated definition of what "a useful JARVIS that can be enjoyed every day" requires.

This artefact exists because no single controlled artefact previously answered, in one place and against one explicit release-criteria definition, "is JARVIS at v1.0 yet?" [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational baseline and its constraints; [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] tracks per-capability maturity across the full product vision, not specifically MLP 0.1. Neither is structured as a scorecard against explicit release criteria.

This artefact was created following an independent Codex governance/v1.0-readiness gap analysis (`govreview`/`v1_0_gap_analysis`, delivered to the AIEMS Exchange Bridge inbox outside any open engineering session), whose first recommendation was exactly this: "a single explicit v1.0 release-criteria artefact." [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] WP2 and WP3 addressed that review's other findings (documentation staleness, PCB-0001 refresh) first, per the Programme Sponsor's direction; this WP4 addresses the scorecard recommendation.

RSC-0001 does not itself approve, prioritise or schedule any implementation. It records an assessment only. Future engineering priorities remain governed by [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] and [[JRM-0001_PROJECT_ROADMAP|JRM-0001]].

---

# 3. Scoring Method

From version 2.0 (ESR-0061 WP1b, EBG-0130) each item is scored against a **fresh install from the release installer on a clean machine, separately for Windows and macOS** - not against the development checkout. A development machine has repository files, environment variables and locally installed models that a household install does not, so scoring there overstated readiness (version 1.1 scored 7 Pass against the checkout; the same product fails three items on a fresh install). Specification completeness is still never treated as the capability itself.

| Score | Meaning |
|-------|---------|
| **Pass** | Works on a fresh install of that platform with no developer setup, through the live product, verified at least once. |
| **Partial** | Works on a fresh install but is materially incomplete against the item's description, or breaches [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 10 (capability honesty). |
| **Fail** | Does not work on a fresh install of that platform, including where no build for that platform exists. |

---

# 4. MLP 0.1 Scorecard

Per [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5, MLP 0.1 "shall include" the following eight items. Version 1.0 is MLP 0.1 ([[JARVIS_PRODUCT_ARCHITECTURE]] Section 10). Scored at ESR-0061 WP1b from the go-live readiness review ([[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 4.1, 2 October 2026) against `v0.1.0`-era code.

| MLP 0.1 Item | Windows (fresh install) | macOS | Gap | Closed by |
|--------------|-------------------------|-------|-----|-----------|
| GUI Dashboard | **Partial** | **Fail** (no build) | Long scrolling page; stale static capability labels and dead controls (a UAM-0001 Section 10 breach); fonts not bundled | Go-live WP2 (macOS), WP4 (redesign, EBG-0164) |
| Chat Interface | **Partial** | **Fail** | Works, but the composer sits below the fold at 1280x820 | WP4 |
| Text Responses | **Fail** | **Fail** | No provider answers on a fresh install: cloud keys only via environment variables, and Ollama is neither detected nor guided | WP3 (EBG-0163), WP5 (EBG-0165) |
| Animated Avatar / Orb | **Fail** | **Fail** | The Orb draws the repository knowledge graph, so an installed machine shows no Orb; scored against UAM-0001 Section 8.2's Version 1.0 criteria (decision D3) | WP4 (EBG-0164) |
| Basic Voice Input | **Fail** | **Fail** | Voice models are not provisioned by the installer; macOS microphone permission and audio format unverified | WP7 (EBG-0167) |
| Basic Conversation Memory | **Pass** | **Fail** | Consent-gated Personal Memory, profile-scoped, with revocation, backup and restore | WP2 (macOS build) |
| User Profiles | **Pass** | **Fail** | Profiles work; roles are enforced for memory only, so the Child role is not yet safe (see 4A) | WP2; WP6 (EBG-0166) |
| Service Status Dashboard | **Partial** | **Fail** | Live `platform.status`, but surfaces repeat and some labels are static | WP4 |

**Windows: 2 Pass, 3 Partial, 3 Fail. macOS: 8 Fail (no build). Not ready for Version 1.0.**

# 4A. Version 1.0 Release Requirements Beyond the Eight Items

Programme Sponsor decisions of 2 October 2026 add requirements that MLP 0.1's eight items do not name. They gate Version 1.0 equally.

| Requirement | Source | Status | Closed by |
|-------------|--------|--------|-----------|
| macOS (Apple Silicon) build | D12, D14 | **Fail** | WP2 (EBG-0162) |
| Provider strategy: Ollama default, consent-confirmed Claude escalation, spend cap, OpenAI/Gemini unregistered | [[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]] | **Fail** | WP3 (EBG-0163) |
| Household safety for the Child role: Administrator PIN, local moderation, recorded parental consent, AI disclosure | D17, D25, ADR-0023 Section 3 | **Fail** | WP6 (EBG-0166) |
| Data rights: per-profile erasure and export, retention limits, privacy notice | D23 | **Fail** | WP5 (EBG-0165) |
| User guide, parents' guide and public "Children and privacy" page | ADR-0023 Section 3 | **Fail** | WP8 (EBG-0168) |

# 4B. Go/No-Go Dimensions (EBG-0066)

The Programme Sponsor's go/no-go decision at go-live WP9 reads these six dimensions. Each is **Ready** only when every listed criterion holds; the decision remains the Programme Sponsor's alone.

| Dimension | Ready when | Current |
|-----------|-----------|---------|
| Product readiness | Every Section 4 item Pass on both platforms | Not ready |
| Release requirements | Every Section 4A item Pass | Not ready |
| Safety | Child-role safeguards live-verified on the household Mac; moderation on both input and output | Not ready |
| Release-candidate checklist | Section 4C fully passed on the tagged build | Not run |
| Review coverage | Every commit since the last baseline independently reviewed before and after commit; high-risk WPs reviewed by both reviewers | Ready to date |
| Repository integrity | CI green on Linux, Windows and macOS; validator 0 errors; no open High backlog item allocated to Version 1.0 | Partial (no macOS CI) |

**AIEMS maturity index.** The same evidence also answers how mature the engineering system itself is, without a separate scoring artefact. At each baseline, record: validator errors and warnings; the share of commits since the last baseline with both pre- and post-commit independent review; the count and age of open High backlog items; and the CI platforms covered. At ESR-0061 WP1b: 0 errors and 346 warnings (330-plus of one false-positive class, triaged in WP1c); every commit since ESR-0058 independently reviewed before commit, but the post-commit review of `1978070` (WP1a) was cut short by Copilot's quota (see the review record); open High items are EBG-0130 and six go-live items registered at WP1a (EBG-0162 to EBG-0166, EBG-0168); CI covers Linux and Windows.

# 4C. Release-Candidate Checklist

The actual release gate, run at go-live WP9 on the tagged build, on Windows Sandbox, the household PC and the household Mac:

1. CI green on the tag: Linux, Windows and macOS.
2. Installers (`.exe`, `.dmg`) and their checksums published by `release.yml`.
3. Clean install and first launch on each machine with no developer setup.
4. The same look on WebView2 and WKWebView, at two display scalings; no dead controls, scaffolding text or static capability labels.
5. The presence Orb meets UAM-0001 Section 8.2 with no repository present.
6. The functionality-preservation inventory (EBG-0164) passes on both engines.
7. Guided first run completes; a first conversation succeeds with local Ollama only.
8. Escalation: suggested, confirmed and labelled with a key; honestly unavailable without one; the spend cap falls back to Ollama.
9. The honest no-provider path works.
10. Voice installs and works, including the macOS microphone permission prompt; the voice-unavailable path is honest.
11. Memory: consent, revocation, per-profile export and erasure, backup and restore.
12. Profiles and roles: Administrator PIN; the Child role cannot change settings or profiles; moderation and consent records work.
13. Upgrade over `v0.1.0` data on Windows preserves memory and profiles.
14. Household soak (D7) completed with no unresolved High finding.

---

# 5. Beyond MLP 0.1: Related Gaps Identified by the Triggering Review

The independent Codex `govreview` finding that prompted this artefact also named gaps beyond MLP 0.1's own scope - these belong to later MLP phases ([[JARVIS_PRODUCT_ARCHITECTURE]] Section 10, Product Roadmap: MLP 0.2 through 0.8) and are recorded here for completeness, not scored against MLP 0.1 criteria they were never part of:

| Gap | MLP Phase | Status |
|-----|-----------|--------|
| Richer voice interaction beyond basic push-to-talk input | MLP 0.2 Voice | Basic input now Pass (see above); richer interaction (continuous listening, multi-language, speaker identification) remains not started. |
| Family profile behaviour (Administrator/Adult/Child/Guest differentiation) | MLP 0.3 Family Profiles | User identity/profile plumbing now exists (EBG-0116), but role-authority enforcement against Sentinel/`TrustTierPolicy` remains not implemented - the actual differentiation this MLP phase describes is still not started. |
| Session and Shared Family memory tiers | MLP 0.4 Memory | Not started ([[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6.1/6.3 specify the architecture; no implementation exists). |
| Local device assistance (Local Agent) | MLP 0.5 Local Agent | Not started - the permission boundary is defined ([[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, EBG-0021, ESR-0041), but no Local Agent module exists under `jarvis/`; `Sentinel`'s `TrustCategory.LOCAL_AGENT_ACTION` remains `DENY` for every request today. |
| Controlled internet-assisted capability | MLP 0.6 Internet | Not started. |
| Visual understanding (Vision) | MLP 0.7 Vision | Not started - deferred alongside speech input for the same Household Role Model reason (EBG-0112). |
| Expanded permission, safety, audit and approval controls; full HITL live wiring | MLP 0.8 Guardian | Partially specified, not fully live - GAM-0001's authority model, family-safety principles (EBG-0020) and HITL governance mechanics (EBG-0048) are all approved specifications, but a network-facing Guardian/Sentinel interface does not exist yet ([[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] remains an approved specification with no implementation), and the family-safety/consent mechanics they specify are not wired into a live multi-user flow (there being no user-identity plumbing to wire them into yet). |

---

# 6. Interpretation

JARVIS is **not ready for Version 1.0**. Version 1.1 of this scorecard (7 Pass, 1 Partial) scored the development checkout; scored against a fresh install, three items fail on Windows and every item fails on macOS, which has no build yet. This resolves the contradiction EBG-0130 recorded between this scorecard and [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]]: the Orb is a genuine launch blocker under UAM-0001 Section 8.2, and LGB-0001 now lists the same blockers. Every Fail and Partial in Sections 4 and 4A is allocated to a go-live Work Package in [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]]; this artefact still authorises none of them.

---

# 7. Maintenance

RSC-0001 is re-scored whenever a Work Package changes any Section 4 or 4A score, and in full at each session-closure baseline. Section 4C is run once, at go-live WP9, on the tagged build. Section 5 is unchanged.

---

# 8. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE]] | Source of the MLP 0.1 release criteria this scorecard assesses against. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product baseline and constraints; shares much of the same underlying evidence. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Broader per-capability maturity tracking across the full product vision, not specifically MLP 0.1; not yet refreshed for ESR-0040/0041/0043/0044 (a pre-existing, separately tracked staleness). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Source of the Household Role Model and Local Agent Permission Boundary referenced in the User Profiles and beyond-MLP-0.1 rows. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Governed source for future engineering priorities; this artefact does not itself prioritise. |
| [[ESR-0045_ENGINEERING_SESSION_REPORT|ESR-0045]] | Session that created this artefact (WP4), triggered by an independent Codex governance/v1.0-readiness gap analysis. |
| [[ESR-0046_ENGINEERING_SESSION_REPORT|ESR-0046]] | Delivered EBG-0116 (User Profiles), the first of this scorecard's two Fail items, now Pass. |
| [[ESR-0047_ENGINEERING_SESSION_REPORT|ESR-0047]] | Delivered EBG-0117 (Basic Voice Input), the second of this scorecard's two Fail items, now Pass. |

---

# 9. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0 | 6 October 2026 | Claude Engineering Implementer | ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0130, EBG-0066): re-scored against a fresh install on Windows and macOS (Windows 2 Pass/3 Partial/3 Fail; macOS no build); Version 1.0 release requirements (4A); go/no-go dimensions and AIEMS maturity index (4B); release-candidate checklist (4C); contradiction with LGB-0001 resolved. |
| 1.1 | 4 August 2026 | Claude Engineering Implementer | ESR-0048 WP1 (Documentation Debt Discipline), per this artefact's own Section 7 maintenance rule: refreshed both Fail items to Pass - Basic Voice Input (EBG-0117, ESR-0047) and User Profiles (EBG-0116, ESR-0046). Score corrected from 5 Pass/1 Partial/2 Fail to 7 Pass/1 Partial/0 Fail. Section 5's Voice/Family Profiles rows and Section 6's Interpretation updated accordingly. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | Initial RSC-0001 created at ESR-0045 WP4, per the Programme Sponsor's selection of the triggering Codex governance review's first recommendation (a single explicit v1.0 release-criteria artefact). Scored all 8 MLP 0.1 items against live repository evidence: 5 Pass, 1 Partial (Animated Avatar/Orb), 2 Fail (Basic Voice Input, User Profiles). Recorded beyond-MLP-0.1 gaps for completeness. |
