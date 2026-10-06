# EIP-ESR0061-001 - Release Gate, Governance and Streamlining

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-001 |
| Title | Engineering Implementation Package: WP1 Release Gate, Governance and Streamlining |
| Version | 0.8 |
| Status | Draft - WP1c built; implementation review Pass; awaiting Programme Sponsor approval of the built result |
| Session | ESR-0061 |
| Work Package | WP1 (WP1a, WP1b, WP1c) |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 7, WP1 |
| Risk class | Standard (not one of the plan's high-risk WPs; Copilot CLI review only, per D19) |

---

# 2. Purpose

Implements go-live plan WP1: define what "done" means for Version 1.0, write the Programme Sponsor's 2 October 2026 decisions (D1-D29) into the controlled artefacts that govern delivery, clear the WP1 governance backlog, and deliver the streamlining tooling so every later WP runs faster without losing oversight.

Backlog folded in (WR-ESR0061-001 Section 8): EBG-0008, 0015, 0016, 0029, 0052, 0053, 0059, 0066, 0067, 0118, 0130, 0134. Also: EBG-0110's stale text, and registration of the new backlog items the later WPs need.

---

# 3. Proposed Decomposition (Programme Sponsor decision requested)

WP1 mixes documentation with code. Rule A5 (one approval for docs-only WPs) and rule A6 (two gates for code) cannot both apply to one commit, and WP1 is too large for one review. **Proposal: three sub-WPs, each reviewed, approved and committed separately**, in this order:

| Sub-WP | Content | Kind | Gates | Effort |
|---|---|---|---|---|
| **WP1a** | Governance enactment: PBK-0001, COC-0001, UAM-0001, product architecture, new ADR-0023 (provider strategy), GDE-0001 relationship vocabulary, EBR-0001 dispositions and new items | Docs only | **One** (A5): this EIP carries the exact text (Section 5) | 1 d |
| **WP1b** | Release gate: RSC-0001 re-scored and RC checklist (EBG-0130), go/no-go dimensions and maturity index (EBG-0066), LGB-0001 reconciled, capability refresh (EBG-0134), EIP standard with evidence pack and tabular ESR entries (EBG-0008, R3, R11) | Docs only | One (A5): exact text added in this EIP's v0.2, drafted while WP1a is in review (D22) | 1-1.5 d |
| **WP1c** | Delivery tooling: single-source baseline (R4), REG-0001 sync (R7), post-commit pre-check and reviewer wrapper (R8), validator warning triage (R10), Gemini CLI second reviewer (R2/D19), local pre-screen (D29) | Code | Two (A6): design in this EIP's v0.3, then the built result | 1.75-2.25 d |

**Dependency flagged (scope-creep discipline):** WP2 is a high-risk WP, so under D19 it needs the second reviewer that WP1c delivers. WP1c must therefore complete before WP2's implementation review - or the Programme Sponsor explicitly overrides D19 for WP2 and accepts Copilot-only review. WP2's *design* can still be drafted in parallel (D22). Recommendation: keep the order WP1a, WP1b, WP1c, WP2.

---

# 4. Repository Context Investigated

* **PBK-0001 1.48** - "Incremental Visual Convergence Toward the Reference Mock-up" (under Feature-First Delivery Discipline) is the rule D9 retires. Its second bullet carries the separate no-mock/capability-honest rule (UAM-0001 Section 10, ESR-0017 WP9), which was **not** retired and must survive. No section records rules A1-A7, milestone sessions, pipelined design drafting, the second-reviewer rule or the local pre-screen.
* **COC-0001 1.30** - Operating Rules end at rule 51. No approval-economy rule.
* **UAM-0001 1.5** - Section 7.1's last paragraph says the reference composition "shall only be approached incrementally". Section 8.1 makes the knowledge graph the Orb's long-term form; Section 8.2's semantics apply only to that graph Orb. Both conflict with D10/D11. Section 8.3 (textual status panel) is independent of the graph and needs no change.
* **JARVIS_PRODUCT_ARCHITECTURE 1.3** - Section 10's last row reads "Version 1.0 - Family AI Operating System", contradicting D2 (Version 1.0 = MLP 0.1). Section 4 has no capability-growth principle (EBG-0029).
* **ADR-0008 1.0** (Hybrid AI Runtime Strategy) - still valid as a principle (local plus cloud). It names no concrete Version 1.0 providers and holds none of the 2 October terms evidence. A new ADR keeps ADR-0008 intact and gives D25-D28 one citable home; ADR-0008 receives a pointer note (5.5A) because its own Review Trigger is met.
* **GDE-0001 1.3** - no relationship vocabulary (confirms EBG-0067's remaining gap).
* **EBR-0001 1.217** - EBG-0053 is "Adopted (10 July 2026)" but never closed; EBG-0118 concerns Codex CLI, retired as reviewer at ESR-0057 and returning 402 since ESR-0060; EBG-0110's text still names OpenAI/Gemini as live cloud providers. Highest existing ID: EBG-0160.
* **Validator** - 0 errors, 333 warnings: 330 are one heuristic ("references Section N, not found as a heading in this document"), mostly true references to *other* documents' sections; 3 are HST files with no parseable version. 67 of the 330 are in REG-0001.
* **Reviewer invocation** - `scripts/aiems_bridge.py` does not run the reviewer itself; the Engineering Implementer runs `copilot` by hand. At ESR-0060 the reviewer's tool permissions refused its own validation commands, so the Engineering Implementer re-ran them (R8's "permissions fix").

---

# 5. WP1a - Exact Text (Approval Under A5 Covers Exactly This)

Each change below is the complete text to be committed. ADR-0023 does not exist until this commit, so a link to it would not resolve in this EIP: "ADR-0023†" below is committed as a wiki link to the file named in 5.5, with display text ADR-0023. Version bumps go through `scripts/bump_version.py` (or by hand where its parser does not match, disclosed in the commit).

## 5.1 PBK-0001 (1.48 to 1.49)

**5.1.1 Remove** the whole sub-section "## Incremental Visual Convergence Toward the Reference Mock-up" (from its heading to "...made only to formally comply.") from Feature-First Delivery Discipline, and insert in its place, as a new **top-level** section immediately after Feature-First Delivery Discipline (before "# Scope-Creep and Cross-WP-Dependency Flagging Discipline"):

> # Capability-Honest Interface
>
> This section replaces "Incremental Visual Convergence Toward the Reference Mock-up" (ESR-0019 WP2), retired by the Programme Sponsor on 2 October 2026 (go-live decision D9, enacted at ESR-0061 WP1a) because step-by-step convergence was too slow for Version 1.0. The Guardian experience is redesigned in one Work Package instead (D10). The reference mock-up (`aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`) remains an illustrative input to that redesign, not a target to be approached in small steps.
>
> The rule the retired section carried is unchanged and stands on its own: **an interface element shall never imply a capability or status more complete than what is actually implemented and verified.** Data-bearing elements show only real, observed data - never illustrative figures, labels or mock fallbacks used as decoration - per [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 10 and the no-mock-fallback rule established at ESR-0017 WP9. Where a capability is unavailable, the interface says so.

**5.1.2 Insert** two further top-level sections immediately after "# Capability-Honest Interface" (so still before "# Scope-Creep and Cross-WP-Dependency Flagging Discipline"):

> # Approval Economy
>
> Decided by the Programme Sponsor on 2 October 2026 (go-live decision D24), enacted at ESR-0061 WP1a. Purpose: one approval act per real decision, without removing any oversight. The Programme Sponsor's time is the programme's scarcest resource; asking for the same decision twice spends it without adding control.
>
> | Rule | Statement |
> |---|---|
> | A1 | **One act per decision.** When a decision produces a commit, approval is requested once, through the Sponsor Approval Service (`~/approve <WP> "note"`). No parallel chat approval is requested for the same decision. Chat approval is used only for decisions that produce no commit (for example a code WP's design approval). |
> | A2 | **The Programme Sponsor's instruction is the approval.** An instruction that needs a commit is given as `~/approve` with the instruction in the note. The Engineering Implementer does not ask the Programme Sponsor to confirm what they have just instructed. Session closure: `~/approve CLOSE "establish"` (or `"retain"`), then "close it". |
> | A3 | **No approval for record-keeping alone.** Session-open records, review verdicts, CI results and post-commit verdicts are recorded in the bridge transcript at once (the primary evidence) and committed with the next approved commit, or at session closure. Between those points the session report trails the transcript by one step. |
> | A4 | **Known asks are front-loaded into the design approval.** New dependencies, crate or OS features and CI changes are listed in the EIP's evidence pack. A mid-WP ask is raised only for a genuine surprise, and every surprise is still flagged. |
> | A5 | **Documentation-only WPs take one approval.** When the EIP contains the exact text to be committed, a Sponsor Approval Service approval of that EIP authorises exactly that commit. |
> | A6 | **Code WPs keep two gates:** design approval ("build this") and approval of the built result ("commit what was built, after independent review"). |
> | A7 | **An approved plan authorises its sequence.** Opening a session to run the next Work Package of an approved plan needs no separate objective approval; WP0B's approval requirement is met by the plan approval plus that WP's own design approval. Any deviation from the plan still needs the Programme Sponsor. |
>
> Unchanged by these rules: the per-commit Sponsor Approval Service gate ([[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]]; fail-closed, never self-approved), independent review before and after each code commit, and the Programme Sponsor's sole authority over baselines, go/no-go and publication. An approval records the repository state at the moment it is given, so nothing is committed between requesting an approval and receiving it.
>
> ## Execute After Approval
>
> Once the Programme Sponsor approves, the Engineering Implementer proceeds to execute the approved work in the same turn. It does not reply with acknowledgement or further confirmation questions and wait to be prompted again. Genuine new questions are still raised, under Scope-Creep and Cross-WP-Dependency Flagging Discipline. (EBG-0052, from the EE-0001 trial at ESR-0017.)
>
> # Delivery Cadence and Independent Review
>
> Decided by the Programme Sponsor on 2 October 2026 (go-live decisions D19, D21, D22, D29), enacted at ESR-0061 WP1a.
>
> ## Milestone Sessions
>
> An Engineering Session covers one milestone of an approved plan - one or more Work Packages - rather than one Work Package. Each session still opens with WP0A/WP0B and closes with session-wide independent verification and the Programme Sponsor's baseline determination. Every commit within it remains individually gated, CI-checked and independently reviewed. (D21.)
>
> ## Pipelined Design Drafting
>
> While Work Package *n* waits for review or approval, the Engineering Implementer may draft Work Package *n+1*'s EIP and design. Drafting only: no code is changed, nothing is committed and nothing is implemented before Work Package *n+1*'s own approval. The pause between Work Packages still applies to implementation. (D22.)
>
> ## Independent Reviewers
>
> * **Engineering Reviewer:** GitHub Copilot CLI reviews every Work Package's design and its committed result.
> * **Second independent reviewer:** Gemini CLI (personal sign-in) also reviews Work Packages the plan or EIP classifies as **high-risk**, and stands in whenever Copilot's quota is exhausted, so that self-verification never becomes the normal path. A **High** finding from either reviewer blocks the Work Package until it is fixed or the Programme Sponsor explicitly overrides it. Lower findings are recorded and dispositioned as before. Review prompts carry no household personal data. (D19.)
> * **Local pre-screen (advisory only):** a local model (gpt-oss-20b via LM Studio, selected by scorecard on 2 October 2026) may pre-screen code Work Packages before Copilot. Its output is labelled advisory, is **never counted as independent review**, and every finding is verified by the Engineering Implementer before it is acted on. (D29.)

**5.1.3** Version History row (1.49): "ESR-0061 WP1a per EIP-ESR0061-001: retired Incremental Visual Convergence (D9), keeping its capability-honest rule as a standalone section; added Approval Economy (A1-A7, D24) and Execute After Approval (EBG-0052); added Delivery Cadence and Independent Review (milestone sessions D21, pipelined design drafting D22, second reviewer D19, advisory local pre-screen D29)."

## 5.2 COC-0001 (1.30 to 1.31)

**Append** to Operating Rules, after rule 51:

> 52. Approvals follow PBK-0001's Approval Economy (rules A1-A7): one approval act per real decision, given through the Sponsor Approval Service whenever it produces a commit. The Engineering Implementer does not request confirmation of an instruction the Programme Sponsor has just given, and proceeds to execute once approval is given.

Version History row (1.31): "ESR-0061 WP1a per EIP-ESR0061-001: rule 52 points to PBK-0001's Approval Economy (D24)."

## 5.3 UAM-0001 (1.5 to 1.6)

**5.3.1 Append** to "Subsequent Architectural Update":

> On 2 October 2026 the Programme Sponsor directed a full Guardian experience redesign delivered as one Work Package (go-live decisions D9-D11, enacted at ESR-0061 WP1a): the incremental approach to Section 7.1's composition is retired, and the Guardian Orb is **decoupled from the knowledge graph**. The Orb becomes a state-driven presence; the repository knowledge graph remains as its own view, with no loss of functionality. Sections 7.1, 8.1 and 8.2 are amended accordingly. Reason: an Orb drawn from the development repository's own files fails on every installed machine (EBG-0148). The Version 1.0 Orb must meet the acceptance criteria in Section 8.2 (D3). UAM-0001's Approved Baseline status is unchanged.

**5.3.2 Replace** Section 7.1's last paragraph ("This composition is dense relative to ... never built ahead of the platform it represents.") with:

> This composition is an illustrative input to the Guardian experience redesign, delivered as one Work Package (Programme Sponsor decisions D9-D10, 2 October 2026), not approached incrementally. Each data-bearing panel still appears only when real implemented capability backs it, per Section 10 - never built ahead of the platform it represents. The System Health illustration's ChatGPT and Codex entries are illustrative only: neither is a Version 1.0 provider (ADR-0023†).

**5.3.3 Replace** Section 8.1's heading and body with:

> ## 8.1 Knowledge Graph View (Decoupled from the Orb)
>
> ESR-0010 Section 15 approved the repository's engineering knowledge graph as the Orb's long-term form (nodes for artefacts, capabilities, systems and agents; connections for real engineering relationships; clusters that illuminate as their systems are accessed). **On 2 October 2026 the Programme Sponsor decoupled the two (D11).** The Orb no longer renders the graph.
>
> The knowledge graph remains a capability in its own right, presented as **its own view**, with the functionality it has today preserved. It is driven by observed repository data, not animation scripts, and is shown only where a repository is actually present. Where none is present it says so plainly rather than showing an error or placeholder data (Section 10). Further graph phases (originally phased under [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0028) remain design direction, built only through approved packages (Section 18).

**5.3.4 Replace** Section 8.2's body (from "The Orb's own animation may communicate..." to "...superseded by an approved implementation package.") with:

> The Orb is Guardian's state-driven presence. For Version 1.0 it shall meet these acceptance criteria (Programme Sponsor decision D3, 2 October 2026):
>
> 1. **Five real states** - idle, listening, thinking, speaking, and offline/error - each driven by an actual runtime event, never by a timer or script.
> 2. **A smooth frame rate** on the household PC and the household Mac (Apple Silicon); the numeric target is set in the redesign Work Package's design.
> 3. **Reduced-motion support**, with the current state also shown as text.
> 4. **Works identically with no repository present.**
> 5. **Matches the look the Programme Sponsor approves** in the redesign prototype.
>
> Further states (for example "awaiting human approval", per [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]) may be added by an approved package. The graph-specific semantics previously listed here (traversal paths, multi-agent paths) belong to the knowledge graph view (8.1), not the Orb. Section 14's colour language continues to apply.

**5.3.5** Version History row (1.6): "ESR-0061 WP1a per EIP-ESR0061-001: Guardian Orb decoupled from the knowledge graph (D11); graph kept as its own view (8.1); Orb Version 1.0 acceptance criteria (8.2, D3); 7.1 incremental approach retired (D9-D10)."

## 5.4 JARVIS_PRODUCT_ARCHITECTURE (1.3 to 1.4)

**5.4.1 Append** to Section 4's recovered product principles list (EBG-0029):

> - Grow by capability: JARVIS grows by acquiring capabilities - coherent, end-to-end abilities a family member can rely on - rather than by accumulating disconnected features.

**5.4.2 Replace** Section 10's table and the paragraph after it with:

> | Phase | Product Focus |
> |-------|---------------|
> | MLP 0.1 - **released as Version 1.0** | GUI dashboard, chat, text responses, animated avatar/orb, basic voice input, basic memory, user profiles and service status - on Windows and macOS, with household safety for the Child role. |
> | MLP 0.2 Voice | Improve voice input and introduce richer voice interaction. |
> | MLP 0.3 Family Profiles | Expand administrator, adult, child and guest profile behaviour. |
> | MLP 0.4 Memory | Improve personal memory, shared family memory and memory controls. |
> | MLP 0.5 Local Agent | Introduce Windows-first local device assistance. |
> | MLP 0.6 Internet | Add controlled internet-assisted capability. |
> | MLP 0.7 Vision | Add visual understanding foundations. |
> | MLP 0.8 Guardian | Expand permission, safety, audit and approval controls. |
> | Family AI Operating System | The combined outcome of MLP 0.2-0.8. |
>
> On 2 October 2026 the Programme Sponsor set the go-live target as MLP 0.1, released as **Version 1.0** (`v1.0.0`) (decisions D1-D2). The Family AI Operating System, previously labelled "Version 1.0", is the later milestone above and no longer carries a version number. Roadmap phases describe product direction. Each implementation package shall still be separately approved through AIEMS and selected against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] where appropriate.

**5.4.3** Version History row (1.4): "ESR-0061 WP1a per EIP-ESR0061-001: Version 1.0 = MLP 0.1 (D1-D2); the Family AI Operating System milestone renamed; Grow-by-capability principle (EBG-0029)."

## 5.5 New ADR-0023 - Version 1.0 Provider Strategy (1.0, Approved)

New file `aiems/governance/decisions/ADR-0023_VERSION_1_0_PROVIDER_STRATEGY.md`, registered in REG-0001 and REG-0002. Full text:

> # ADR-0023 - Version 1.0 Provider Strategy
>
> ---
>
> # Document Control
>
> | Field | Value |
> |-------|-------|
> | Artefact ID | ADR-0023 |
> | Title | Version 1.0 Provider Strategy |
> | Version | 1.0 |
> | Status | Approved |
> | Owner | Programme Sponsor & Chief Engineering Advisor |
> | Classification | Internal |
> | Decision Date | 2 October 2026 (recorded at ESR-0061 WP1a) |
> | Related | [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] (principle unchanged), [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Sections 3 and 5 |
>
> ---
>
> # 1. Context
>
> Version 1.0 will be used in a UK household by adults and by a household member under 18 using the Child role, on Windows and macOS, and then released publicly. Today a fresh install has no working provider unless API keys are set in environment variables. Each provider's own terms decide whether a family app with a minor may use it.
>
> # 2. Decision
>
> | Tier | Provider | When | Child role |
> |---|---|---|---|
> | Default | **Local Ollama** on each machine | Every conversation unless escalated | Yes, with local moderation |
> | Escalation | **Anthropic Claude API** (user's own API key) | Research, knowledge or harder questions - **suggested by JARVIS and confirmed by the user, never automatic** (D28) | Yes, only with recorded parental consent, moderation and AI disclosure |
> | Unregistered | OpenAI API | - | - (D25) |
> | Unregistered | Google Gemini API | - | - (D27) |
>
> 1. Claude escalation spend is capped at **£30 per month** (D26): set in the Anthropic Console and also enforced by JARVIS, which falls back to local Ollama at the cap. This is the plan's only recurring cost and an explicit exception to the no-discretionary-budget rule.
> 2. Unregistered adapters are kept, with their tests, but not wired into the runtime (the Piper precedent, ESR-0053), so these decisions can be reversed.
> 3. Subscription and coding-agent tools (Claude Code, GitHub Copilot, Codex, Antigravity) are **not** product backends. They remain engineering tools only.
> 4. ADR-0008's hybrid local-plus-cloud principle is unchanged; this ADR selects the concrete Version 1.0 providers.
>
> # 3. Evidence - provider terms, read 2 October 2026
>
> | Source | Relevant text (quoted) | Consequence |
> |---|---|---|
> | Anthropic Consumer Terms (anthropic.com/legal/consumer-terms) | "You must be at least 18 years old to use the Services." Prohibited: "Except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services through automated or non-human means". "You may not share your Account login information, Anthropic API key, or Account credentials with anyone else or make your Account available to anyone else." | A Claude subscription cannot power JARVIS for anyone else, least of all a minor. API key only. |
> | Anthropic - organisations serving minors (support.claude.com article 9307344) | Permitted with safeguards: "Age verification systems to ensure only intended users can access the product"; "Content moderation and filtering to block inappropriate or harmful content"; regulatory compliance documented publicly; users informed "they are interacting with an AI system rather than a human". | The Claude API may serve the Child role if these safeguards exist: Administrator PIN (WP6), local moderation (WP6), a public "Children and privacy" page (WP8), AI disclosure (WP4/WP6). |
> | Gemini API Terms (ai.google.dev/gemini-api/terms) | "You must be 18 years of age or older to use the APIs." "You also will not use the Services as part of a website, application, or other service... that is directed towards or is likely to be accessed by individuals under the age of 18." | A family app with a Child role is likely to be accessed by under-18s, so the Gemini API leaves the product (D27). Gemini **CLI** for engineering review is a separate question (PBK-0001 Independent Reviewers). |
>
> Not verified: GitHub Copilot, OpenAI Codex and Google Antigravity product terms. They are excluded as product backends on practical and security grounds regardless: they are coding agents with file and shell access, they would consume the engineering review quota, and other households cannot use the Programme Sponsor's subscriptions.
>
> # 4. Consequences
>
> * Go-live plan WP3 builds `sentinel/anthropic_provider.py` (matching the existing adapters' retry, circuit and deadline semantics), makes Ollama the default route with detection, guided install, in-app model pull and a hardware-based model recommendation, adds suggested-then-confirmed escalation with a visible "answered by Claude" indicator, enforces the spend cap, and unregisters OpenAI and Gemini.
> * WP6 delivers the safeguards Anthropic requires for minors; WP8 publishes the "Children and privacy" page.
> * Household data follows UK GDPR principles as the design standard (D23): local processing by default is the strongest position.
> * Review trigger: any change of escalation provider, a material change to any cited terms, or the cap proving insufficient.
>
> # Version History
>
> | Version | Date | Author | Summary |
> |---|---|---|---|
> | 1.0 | 6 October 2026 | Claude Engineering Implementer | Created at ESR-0061 WP1a per EIP-ESR0061-001, recording Programme Sponsor decisions D25-D28 of 2 October 2026 and the provider terms read that day. |

## 5.5A ADR-0008 (1.0 to 1.1) - pointer to ADR-0023

ADR-0008's own Review Trigger ("Significant AI runtime or provider architecture change") is met by ADR-0023. **Insert** after its Document Control section (following UAM-0001's precedent for ADR-0018):

> # Subsequent Architectural Update
>
> ADR-0023† (Version 1.0 Provider Strategy, decided 2 October 2026, recorded at ESR-0061 WP1a) selects the concrete Version 1.0 providers under this ADR's hybrid principle: local Ollama by default, the Anthropic Claude API for user-confirmed escalation, OpenAI and Gemini APIs unregistered. This review was triggered by this ADR's own Review Trigger. The hybrid local-plus-cloud principle is unchanged, and this note does not change ADR-0008's Approved status or other content.

Version History row (1.1): "ESR-0061 WP1a per EIP-ESR0061-001: Subsequent Architectural Update pointing to ADR-0023 (Review Trigger met)."

## 5.6 GDE-0001 (1.3 to 1.4) - relationship vocabulary (EBG-0067)

**Insert** a new section after Section 4 (Knowledge Tier Structure):

> # 4A. Relationship Vocabulary
>
> Approved at ESR-0006 (as part of the then-proposed "AIEMS Knowledge Architecture") and recorded here at ESR-0061 WP1a (EBG-0067). When an artefact states how it relates to another - in OSE Relationships, Related Artefacts or prose - it should use one of these terms, so relationships stay comparable across the repository and tool-independent:
>
> | Term | Meaning |
> |---|---|
> | implements | Puts an approved decision or design into effect (for example, an EIP implements an ADR) |
> | supports | Helps another artefact achieve its purpose without implementing it |
> | depends_on | Cannot be completed or remain valid without the other artefact |
> | verifies | Checks that the other artefact's claims hold (for example, a review or test) |
> | records | Is the record of an event or decision the other artefact describes |
> | supersedes | Replaces the other artefact, which remains for history |
> | references | Cites the other artefact for context |
> | relates_to | Is connected in a way none of the other terms describes |
> | derived_from | Was produced from the other artefact's content |
> | governed_by | Is subject to the other artefact's rules |
>
> Existing artefacts are not rewritten to adopt it; it applies to new and amended text.

Version History row (1.4): "ESR-0061 WP1a per EIP-ESR0061-001: Section 4A Relationship Vocabulary (EBG-0067)."

## 5.7 EBR-0001 (1.217 to 1.218)

**Dispositions** (Status column set as shown; one sentence appended to each row's text citing ESR-0061 WP1a):

| Item | New status | Appended reason |
|---|---|---|
| EBG-0015 | Superseded | Programme Sponsor decision D13 (2 October 2026): investigation overtaken by the delivered Guardian Cognitive Core and Personal Memory (ESR-0039 onwards); further memory scope is tracked under MLP 0.4. |
| EBG-0016 | Rejected | WP0 was already split into "WP0A - Repository Synchronisation" and "WP0B - Engineering Session Initialisation" (PBK-0001, COC-0001 rule 3), which makes the proposed rename unnecessary. |
| EBG-0029 | Completed | Grow-by-capability principle added to JARVIS_PRODUCT_ARCHITECTURE Section 4. |
| EBG-0052 | Completed | PBK-0001 "Execute After Approval" and COC-0001 rule 52. |
| EBG-0053 | Completed | Adopted as EE-0001 Section 5.12 on 10 July 2026; never closed. Closed now. |
| EBG-0059 | Superseded | Programme Sponsor decision D13: the independent, deterministic assurance it specified is now provided by the Sponsor Approval Service gate (ADR-0022), the AIEMS Exchange Bridge, two independent reviewers, and the R8 post-commit pre-check (WP1c). |
| EBG-0067 | Completed | GDE-0001 Section 4A Relationship Vocabulary. |
| EBG-0118 | Superseded | Codex CLI was retired as Engineering Reviewer at ESR-0057 and has returned `402 deactivated_workspace` since ESR-0060; the stall no longer affects any workflow. |

**EBG-0110 text** - append: "**Updated at ESR-0061 WP1a:** under ADR-0023† the only Version 1.0 cloud provider is the Anthropic Claude API, used only on user-confirmed escalation; OpenAI and Gemini are unregistered. The gap stands for that path. Allocated: backend control in go-live WP3, per-profile UI in WP5 (closes), Child default off in WP6."

**New items** (all Approved Backlog - approved as part of the go-live plan; each row's Source is "WR-ESR0061-001 (go-live plan, 2 October 2026); registered ESR-0061 WP1a"; Owner Programme Sponsor):

| ID | Title | Priority | WP | Text |
|---|---|---|---|---|
| EBG-0161 | Whitespace-Only Provider Model Environment Variable Used as Model Name | Low | WP3 | `jarvis/interfaces/stdio_rpc.py:293` takes `environ.get(spec["model_env_var"]) or spec["default_model"]`; a whitespace-only value (e.g. `"   "`) is truthy and is passed through as the model name. Found by the gpt-oss-20b local pre-screen scorecard on 2 October 2026 and verified on `main` by the Engineering Implementer. The new Anthropic adapter must not inherit the pattern. |
| EBG-0162 | macOS Platform Support (Apple Silicon) | High | WP2 | `aarch64-apple-darwin` sidecar; real Unix process-tree termination with an orphan watchdog; `macos` CI jobs and a Playwright WebKit project; `.dmg` and checksum in `release.yml`; `NSMicrophoneUsageDescription` and minimum OS; GIA macOS process names or an honest "not applicable"; live check on Mac visit 1. |
| EBG-0163 | Version 1.0 Provider Strategy - Ollama First, Claude API Escalation | High | WP3 | Implements ADR-0023: Anthropic adapter, Ollama default with detection, guided install, model pull and hardware recommendation; suggested-then-confirmed escalation with a visible indicator; £30/month cap enforced in JARVIS; OpenAI and Gemini unregistered. Measured on both machines. |
| EBG-0164 | Guardian Experience Redesign and Presence Orb | High | WP4 | One-WP redesign per UAM-0001 1.6: app shell with views; presence Orb meeting UAM-0001 Section 8.2's criteria; knowledge graph as its own view; bundled fonts; one look on WebView2 and WKWebView; role-aware UI; AI disclosure element; functionality-preservation inventory as the gate. Programme Sponsor approves the prototype. |
| EBG-0165 | First-Run Setup, Settings and Per-Profile Data Rights | High | WP5 | Ollama-first first-run; settings UI; Claude key in the OS keychain via `keyring` (STD-0006); per-profile erasure and export; time-based retention for audit and safety logs; privacy notice. Closes EBG-0110 with WP3's backend half. |
| EBG-0166 | Household Safety - Administrator PIN, Child Role, Moderation and Consent | High | WP6 | GAM-0001 Section 8.2 implemented: Administrator PIN (`hashlib.scrypt`, rate-limited); Child cannot switch profile or change settings; local moderation model on Child input and output; child-safety prompt layer; recorded parental consent before Child escalation; Child AI disclosure; safety events recorded as category and time only (D23). |
| EBG-0167 | Voice Provisioning on Windows and macOS | Medium | WP7 | In-app download of voice models (D4); `kokoro-onnx`/espeak and `faster-whisper` verified in both sidecars; WKWebView `audio/mp4` path verified. |
| EBG-0168 | User Guide, Parents' Guide and Public "Children and Privacy" Page | High | WP8 | User guide; parents' guide; public page meeting Anthropic's minors requirement (what is collected, where it goes, consent, retention, erasure); a data map of what JARVIS holds and where it goes. |
| EBG-0169 | Delivery Streamlining Tooling and Second Independent Reviewer | Medium | WP1c | R4 single-source baseline with validator rule; R7 REG-0001 sync check; R8 post-commit pre-check and reviewer wrapper with working tool permissions; R10 validator warning triage; Gemini CLI as second reviewer (terms verified before use; Programme Sponsor's one-time sign-in); gpt-oss-20b advisory pre-screen. |

## 5.8 REG-0001 / REG-0002

Version syncs for every artefact above (including ADR-0008 1.1 in REG-0001; REG-0002 carries no versions); new rows for ADR-0023 in REG-0001 and REG-0002 (REG-0002 summary: "Version 1.0 providers: local Ollama by default, Anthropic Claude API for user-confirmed escalation under a £30/month cap; OpenAI and Gemini APIs unregistered; provider terms for minors recorded."). ESR-0061 and this EIP are registered at session open.

---

# 6. WP1b - Exact Text (Approval Under A5 Covers Exactly This)

Drafted under D22 while WP1a was committed and post-commit reviewed. Same conventions as Section 5.

**Commit contents (the WP1b commit adds or changes exactly these files and no others):** `aiems/governance/baselines/RSC-0001_V1_0_READINESS_SCORECARD.md`, `aiems/governance/baselines/LGB-0001_LAUNCH_GAP_BACKLOG.md`, `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`, `aiems/templates/TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE.md` (filename kept), `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, this EIP, and `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md` (session records, rule A3). **Removed in v0.5:** a JRM-0001 sweep and a PST-0001 Section 8 update, which v0.3 added citing the plan's WP1 row and Appendix A.4 - that citation was wrong (both items came from an uncommitted earlier draft; the registered plan does not list them for WP1, and its Section 11 sets JRM-0001's post-launch order at WP9). PST-0001 Section 8 is refreshed at session closure as before.

## 6.1 RSC-0001 (1.1 to 2.0) - release gate (EBG-0130, EBG-0066)

**6.1.1 Replace** Section 3 (Scoring Method) body with:

> From version 2.0 (ESR-0061 WP1b, EBG-0130) each item is scored against a **fresh install from the release installer on a clean machine, separately for Windows and macOS** - not against the development checkout. A development machine has repository files, environment variables and locally installed models that a household install does not, so scoring there overstated readiness (version 1.1 scored 7 Pass against the checkout; the same product fails three items on a fresh install). Specification completeness is still never treated as the capability itself.
>
> | Score | Meaning |
> |-------|---------|
> | **Pass** | Works on a fresh install of that platform with no developer setup, through the live product, verified at least once. |
> | **Partial** | Works on a fresh install but is materially incomplete against the item's description, or breaches [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 10 (capability honesty). |
> | **Fail** | Does not work on a fresh install of that platform, including where no build for that platform exists. |

**6.1.2 Replace** Section 4 (MLP 0.1 Scorecard) with:

> # 4. MLP 0.1 Scorecard
>
> Per [[JARVIS_PRODUCT_ARCHITECTURE]] Section 5, MLP 0.1 "shall include" the following eight items. Version 1.0 is MLP 0.1 ([[JARVIS_PRODUCT_ARCHITECTURE]] Section 10). Scored at ESR-0061 WP1b from the go-live readiness review ([[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 4.1, 2 October 2026) against `v0.1.0`-era code.
>
> | MLP 0.1 Item | Windows (fresh install) | macOS | Gap | Closed by |
> |--------------|-------------------------|-------|-----|-----------|
> | GUI Dashboard | **Partial** | **Fail** (no build) | Long scrolling page; stale static capability labels and dead controls (a UAM-0001 Section 10 breach); fonts not bundled | Go-live WP2 (macOS), WP4 (redesign, EBG-0164) |
> | Chat Interface | **Partial** | **Fail** | Works, but the composer sits below the fold at 1280x820 | WP4 |
> | Text Responses | **Fail** | **Fail** | No provider answers on a fresh install: cloud keys only via environment variables, and Ollama is neither detected nor guided | WP3 (EBG-0163), WP5 (EBG-0165) |
> | Animated Avatar / Orb | **Fail** | **Fail** | The Orb draws the repository knowledge graph, so an installed machine shows no Orb; scored against UAM-0001 Section 8.2's Version 1.0 criteria (decision D3) | WP4 (EBG-0164) |
> | Basic Voice Input | **Fail** | **Fail** | Voice models are not provisioned by the installer; macOS microphone permission and audio format unverified | WP7 (EBG-0167) |
> | Basic Conversation Memory | **Pass** | **Fail** | Consent-gated Personal Memory, profile-scoped, with revocation, backup and restore | WP2 (macOS build) |
> | User Profiles | **Pass** | **Fail** | Profiles work; roles are enforced for memory only, so the Child role is not yet safe (see 4A) | WP2; WP6 (EBG-0166) |
> | Service Status Dashboard | **Partial** | **Fail** | Live `platform.status`, but surfaces repeat and some labels are static | WP4 |
>
> **Windows: 2 Pass, 3 Partial, 3 Fail. macOS: 8 Fail (no build). Not ready for Version 1.0.**
>
> # 4A. Version 1.0 Release Requirements Beyond the Eight Items
>
> Programme Sponsor decisions of 2 October 2026 add requirements that MLP 0.1's eight items do not name. They gate Version 1.0 equally.
>
> | Requirement | Source | Status | Closed by |
> |-------------|--------|--------|-----------|
> | macOS (Apple Silicon) build | D12, D14 | **Fail** | WP2 (EBG-0162) |
> | Provider strategy: Ollama default, consent-confirmed Claude escalation, spend cap, OpenAI/Gemini unregistered | [[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]] | **Fail** | WP3 (EBG-0163) |
> | Household safety for the Child role: Administrator PIN, local moderation, recorded parental consent, AI disclosure | D17, D25, ADR-0023 Section 3 | **Fail** | WP6 (EBG-0166) |
> | Data rights: per-profile erasure and export, retention limits, privacy notice | D23 | **Fail** | WP5 (EBG-0165) |
> | User guide, parents' guide and public "Children and privacy" page | ADR-0023 Section 3 | **Fail** | WP8 (EBG-0168) |
>
> # 4B. Go/No-Go Dimensions (EBG-0066)
>
> The Programme Sponsor's go/no-go decision at go-live WP9 reads these six dimensions. Each is **Ready** only when every listed criterion holds; the decision remains the Programme Sponsor's alone.
>
> | Dimension | Ready when | Current |
> |-----------|-----------|---------|
> | Product readiness | Every Section 4 item Pass on both platforms | Not ready |
> | Release requirements | Every Section 4A item Pass | Not ready |
> | Safety | Child-role safeguards live-verified on the household Mac; moderation on both input and output | Not ready |
> | Release-candidate checklist | Section 4C fully passed on the tagged build | Not run |
> | Review coverage | Every commit since the last baseline independently reviewed before and after commit; high-risk WPs reviewed by both reviewers | Ready to date |
> | Repository integrity | CI green on Linux, Windows and macOS; validator 0 errors; no open High backlog item allocated to Version 1.0 | Partial (no macOS CI) |
>
> **AIEMS maturity index.** The same evidence also answers how mature the engineering system itself is, without a separate scoring artefact. At each baseline, record: validator errors and warnings; the share of commits since the last baseline with both pre- and post-commit independent review; the count and age of open High backlog items; and the CI platforms covered. At ESR-0061 WP1b: 0 errors and 346 warnings (330-plus of one false-positive class, triaged in WP1c); every commit since ESR-0058 independently reviewed before commit, but the post-commit review of `1978070` (WP1a) was cut short by Copilot's quota (see the review record); open High items are EBG-0130 and six go-live items registered at WP1a (EBG-0162 to EBG-0166, EBG-0168); CI covers Linux and Windows.
>
> # 4C. Release-Candidate Checklist
>
> The actual release gate, run at go-live WP9 on the tagged build, on Windows Sandbox, the household PC and the household Mac:
>
> 1. CI green on the tag: Linux, Windows and macOS.
> 2. Installers (`.exe`, `.dmg`) and their checksums published by `release.yml`.
> 3. Clean install and first launch on each machine with no developer setup.
> 4. The same look on WebView2 and WKWebView, at two display scalings; no dead controls, scaffolding text or static capability labels.
> 5. The presence Orb meets UAM-0001 Section 8.2 with no repository present.
> 6. The functionality-preservation inventory (EBG-0164) passes on both engines.
> 7. Guided first run completes; a first conversation succeeds with local Ollama only.
> 8. Escalation: suggested, confirmed and labelled with a key; honestly unavailable without one; the spend cap falls back to Ollama.
> 9. The honest no-provider path works.
> 10. Voice installs and works, including the macOS microphone permission prompt; the voice-unavailable path is honest.
> 11. Memory: consent, revocation, per-profile export and erasure, backup and restore.
> 12. Profiles and roles: Administrator PIN; the Child role cannot change settings or profiles; moderation and consent records work.
> 13. Upgrade over `v0.1.0` data on Windows preserves memory and profiles.
> 14. Household soak (D7) completed with no unresolved High finding.

**6.1.3 Replace** Section 6 (Interpretation) body with:

> JARVIS is **not ready for Version 1.0**. Version 1.1 of this scorecard (7 Pass, 1 Partial) scored the development checkout; scored against a fresh install, three items fail on Windows and every item fails on macOS, which has no build yet. This resolves the contradiction EBG-0130 recorded between this scorecard and [[LGB-0001_LAUNCH_GAP_BACKLOG|LGB-0001]]: the Orb is a genuine launch blocker under UAM-0001 Section 8.2, and LGB-0001 now lists the same blockers. Every Fail and Partial in Sections 4 and 4A is allocated to a go-live Work Package in [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]]; this artefact still authorises none of them.

**6.1.4 Replace** Section 7 (Maintenance) body with:

> RSC-0001 is re-scored whenever a Work Package changes any Section 4 or 4A score, and in full at each session-closure baseline. Section 4C is run once, at go-live WP9, on the tagged build. Section 5 is unchanged.

**6.1.5** Version History row (2.0): "ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0130, EBG-0066): re-scored against a fresh install on Windows and macOS (Windows 2 Pass/3 Partial/3 Fail; macOS no build); Version 1.0 release requirements (4A); go/no-go dimensions and AIEMS maturity index (4B); release-candidate checklist (4C); contradiction with LGB-0001 resolved."

## 6.2 LGB-0001 (1.2 to 1.3)

**Replace** Section 4's heading and body (from "# 4. Must-Ship" to just before "# 5. Defer") with:

> # 4. Must-Ship (Blocks Version 1.0)
>
> Reconciled with [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] 2.0 at ESR-0061 WP1b (EBG-0130), so the two artefacts give one answer. **RSC-0001 holds the scores; this section lists the blocking gaps.** Version 1.0 = MLP 0.1, released on Windows and macOS (Programme Sponsor decisions D1-D2, D12).
>
> | Gap | RSC-0001 2.0 | Backlog | Go-live WP |
> |-----|--------------|---------|------------|
> | No macOS build | Section 4A Fail; every Section 4 item Fail on macOS | EBG-0162 | WP2 |
> | No working provider on a fresh install | Text Responses Fail | EBG-0163, EBG-0165 | WP3, WP5 |
> | Orb fails without a repository | Animated Avatar / Orb Fail | EBG-0164 | WP4 |
> | Dashboard, chat and status breach capability honesty and layout | Three items Partial | EBG-0164 | WP4 |
> | Voice not provisioned | Basic Voice Input Fail | EBG-0167 | WP7 |
> | Child role not safe | Section 4A Fail | EBG-0166 | WP6 |
> | Data rights | Section 4A Fail | EBG-0165 | WP5 |
> | User and parents' documentation, "Children and privacy" page | Section 4A Fail | EBG-0168 | WP8 |
>
> The two items this section listed before version 1.3 (EBG-0116 User Identity, EBG-0117 Speech Input) remain resolved: both were delivered at ESR-0046 and ESR-0047, and both still score Pass in a development checkout. Speech input fails on a fresh install only because its models are not provisioned, which is the new EBG-0167.

**Append** to Section 7 (Interpretation), after its last sentence (v0.5 addition; without it, "both Must-Ship items are now delivered" would read as contradicting the new Section 4): " Since version 1.3 (ESR-0061 WP1b), Section 4 lists eight Version 1.0 blockers from [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]] 2.0's fresh-install scoring; the two items above remain delivered."

**Version History** row (1.3): "ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0130): Must-Ship reconciled with RSC-0001 2.0's fresh-install scoring; eight go-live blockers allocated to WP2-WP8."

## 6.3 PCB-0001 (2.20 to 3.0) - capability re-audit (EBG-0134)

Rows re-audited against the code and the completion records in EBR-0001, not just pointer-synced. **Replace** these Section 4 rows (Baseline Area unchanged; Accepted Position text replaced):

> | User Experience Platform (UXP) | The Tauri+React UXP is live: capability/diagnostics panels derive from live `platform.status` data; an Agent Framework panel (`src/AgentFrameworkPanel.jsx`, ESR-0050) and a Memory Management panel with per-item revocation (`src/MemoryManagementPanel.jsx`, ESR-0058, ESR-0059 WP10) reach the real backend. The Guardian Orb renders the repository knowledge graph as a 2D force-directed, circle-confined visualisation with cluster illumination (Phase 2, ESR-0051) - which means it shows no graph on an installed machine without a repository (EBG-0148 made that failure honest at ESR-0059 WP11; decoupling the Orb from the graph is go-live WP4, EBG-0164, per UAM-0001 1.6). Distributed as a Windows installer with a packaged backend sidecar (ESR-0032, EBG-0102); a busy or hung backend is terminated with the app (Windows job object, ESR-0060, EBG-0154). No macOS build (EBG-0162). The Tkinter GUI remains the separate legacy First Light shell. |
> | Provider abstraction framework | OpenAI or Gemini is wired into the default conversation path when credentialed (`JARVIS_PRIMARY_PROVIDER`, normalised since ESR-0060, EBG-0155), the other as a credential-gated secondary, Ollama as the local fallback; no echo fallback (ESR-0059 WP3). Every text call has a per-turn deadline (ESR-0059 WP5), retry with backoff and a circuit breaker (ESR-0059 WP6); a deadline expiry is not counted as a provider fault (ESR-0060, EBG-0156). **Direction change:** [[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]] (2 October 2026) makes Ollama the Version 1.0 default with Claude API escalation and unregisters OpenAI and Gemini - not yet implemented (go-live WP3, EBG-0163). |
> | Voice faculty | Both directions implemented. Speech output uses self-hosted Kokoro with British English voices as the production voice (ESR-0053, EBG-0125); Piper is unregistered but kept. Speech input uses self-hosted `faster-whisper`, push-to-talk, conditionally rendered on real-time capability detection (ESR-0047). Models are not provisioned by the installer, so voice is unavailable on a fresh install (go-live WP7, EBG-0167). No wake word, continuous listening or speaker identification. |
> | Agent Framework | `jarvis/agents/` contract with three Sentinel-gated, read-only `ROUTINE_INTERACTION` specialist agents: GIA local-resource observability (ESR-0049), GIA engineering status (git, repository health and register state, ESR-0054/ESR-0055) and Home Assistant state query, registered only when `JARVIS_HOME_ASSISTANT_URL`/`_TOKEN` are set (ESR-0058, EBG-0127). Reachable via `guardian.agent.*` and the UXP Agent Framework panel. `LOCAL_AGENT_ACTION` (the Action faculty) remains a hard `DENY`. |
> | Personal Memory | Consent-gated, profile-scoped SQLite store with role enforcement (ESR-0027, ESR-0059 WP13-WP14), per-item revocation (`memory.delete`, ESR-0059 WP10), and backup and restore (`memory.backup`/`memory.restore`, Administrator-only, ESR-0057). |
> | Observability | Durable rotating audit trail with no conversation or memory content, bounded in-process histories and a rotating `backend.log` (ESR-0059 WP9, EBG-0144). |

The last two are **new rows**, inserted after "User Identity and Profiles". In Section 3, **append** to the v2.3 paragraph: "The v3.0 refresh (ESR-0061 WP1b, EBG-0134) re-audited the UXP, provider, voice and agent rows against delivered code for the first time since ESR-0050 - they had been pointer-synced only at each baseline - and added Personal Memory and Observability rows." **Replace** Section 6's knowledge-graph Orb and sidecar-packaging bullets with:

> - The Guardian Orb depends on repository data and shows no graph on an installed machine; Version 1.0 decouples it (UAM-0001 1.6, go-live WP4).
> - Windows only: no macOS build (go-live WP2). The Windows installer is unsigned (EBG-0146, Deferred).

**Version History** row (3.0): "ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0134): first content re-audit since ESR-0050 - UXP, provider, voice and agent rows refreshed against delivered code (Kokoro, three agents, Memory Management panel, packaged sidecar, job-object termination, retry/deadline); new Personal Memory and Observability rows; ADR-0023 direction recorded; constraints updated."

## 6.4 JARVIS Capability Readiness Matrix (2.20 to 3.0) (EBG-0134)

**Replace** these Section 2 rows:

> | Voice | Complete | Partial | Both increments: Kokoro British English speech output (production, ESR-0053) and `faster-whisper` speech input (ESR-0047); not provisioned on a fresh install | Implemented (unit-, RPC- and Playwright-tested) | Implemented (Foundation) |
> | User Experience Platform | Complete | Complete (redesign directed, UAM-0001 1.6) | Implemented (Foundation): live panels incl. Agent Framework and Memory Management; Windows installer; no macOS build | Implemented | Implemented (Foundation) - Version 1.0 redesign pending |
> | Agent Framework (specialist agents serving Guardian) | Complete | Complete | Three read-only `ROUTINE_INTERACTION` agents (GIA observability, GIA engineering status, Home Assistant state query), `guardian.agent.*` RPC and a UXP panel; `LOCAL_AGENT_ACTION` a hard `DENY` | Implemented | Implemented (Foundation) |
> | Knowledge | Complete | Complete | Phases 1-2 of 4 (graph plus cluster illumination); decoupled from the Orb as its own view for Version 1.0 | Implemented | Partial |
> | Provider Architecture | Complete | Complete ([[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]] direction set) | Implemented with deadline, retry and circuit breaker; Ollama-first strategy not yet implemented | Implemented | Implemented (Foundation) |

Set "Last Refreshed" to "ESR-0061 WP1b (6 October 2026)". In Section 3, **append** after the Agent Framework bullet: "- **Re-audited at ESR-0061 WP1b (EBG-0134)** against delivered code, not just pointer-synced: Kokoro production voice, three specialist agents with a UXP panel, Memory Management, packaged Windows distribution. Version 1.0 direction is set by UAM-0001 1.6 and ADR-0023; scores against a fresh install are in [[RSC-0001_V1_0_READINESS_SCORECARD|RSC-0001]]." Refresh History row (3.0): "ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0134): Voice, UXP, Agent Framework, Knowledge and Provider Architecture rows re-audited against delivered code; summary updated."

## 6.5 TPL-0001 (0.2 Draft to 1.0 Approved) - EIP standard (EBG-0008, R3, R11)

TPL-0001 0.2 is a Draft template for the ESR-0009-era "Engineering Execution Package" prompt format; no Work Package has used it since EIPs replaced it. **Proposal: rewrite it as the EIP standard and template** rather than create a new standard (Minimise Controlled Artefact Creation). Title becomes "Engineering Implementation Package Standard and Template"; Version 1.0, Status Approved, Effective Date 6 October 2026. **The filename is kept** (`TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE.md`): renaming would mean editing links inside nine files, including archived chat histories and closed session records, so only the title changes (v0.5 change - v0.4 proposed a rename). Sections 2 onward are replaced with:

> # 2. Purpose
>
> Defines the format, lifecycle, numbering and approval rules for an Engineering Implementation Package (EIP), and gives its template. Replaces the ESR-0009-era Engineering Execution Package template (TPL-0001 0.2), which no Work Package has used since EIPs superseded it. EBG-0008, ESR-0061 WP1b.
>
> # 3. Numbering and Location
>
> `EIP-ESR<session>-<nnn>_<TITLE>.md` in `aiems/governance/reviews/`, numbered in creation order within the session, registered in REG-0001 when created.
>
> # 4. Lifecycle and Approval
>
> | Step | Code WP (rule A6) | Documentation-only WP (rule A5) |
> |---|---|---|
> | 1 | EIP drafted with its evidence pack (Section 6) and commit contents | EIP drafted with the exact text and the full commit contents (Section 5, item 4A) |
> | 2 | Independent design review (both reviewers if high-risk) | Independent review |
> | 3 | Programme Sponsor design approval (chat; no commit) | - |
> | 4 | Implement; independent review of the built result | Apply the exact text |
> | 5 | Sponsor Approval Service approval; `submit-response`; commit | Sponsor Approval Service approval; `submit-response`; commit |
> | 6 | CI on every platform; post-commit pre-check and independent review | Same |
>
> Version 0.x while in draft; 1.0 when approved and implemented. Every review verdict and every change made after a review is recorded in the EIP itself.
>
> # 5. Mandatory Sections
>
> 1. **Document Control** - ID, title, version, status, session, Work Package, risk class (standard or high-risk).
> 2. **Purpose** - what is delivered and which backlog items it closes.
> 3. **Repository Context Investigated** - what the Engineering Implementer read and verified, with file references.
> 4. **Scope** - for code, the design; for documentation, the exact text.
> 4A. **Commit Contents** - every file the commit will add or change, including session records (the ESR, register rows, Working Reports, the EIP itself). An A5 approval covers exactly these files and this text; nothing else may enter that commit.
> 5. **Evidence Pack** - Section 6 below (code WPs).
> 6. **Explicitly Out of Scope** - including disclosed residuals.
> 7. **Validation Requirements** - tests, validator, CI jobs, live checks.
> 8. **Questions for the Engineering Reviewer.**
> 9. **Review Record** - each verdict, its findings and their dispositions.
> 10. **Version History.**
>
> # 6. Evidence Pack (R3)
>
> Built from ESR-0060 WP2, where three design rounds missed facts a source check would have caught. Required for every code WP before design review:
>
> | Item | Content |
> |---|---|
> | API facts | Every library, OS or framework behaviour the design relies on, checked against source or documentation, with the reference |
> | Platform coverage | Windows and macOS behaviour, stated separately; any platform-specific code path named |
> | CI | Which CI jobs will exercise the change, on which platforms; any CI change needed |
> | Tests | The test list, and which tests are shown failing on the old code |
> | New dependencies and features | Every new package, crate, crate feature, OS permission or capability - listed so the design approval covers them (rule A4) |
>
> # 7. ESR Work Package Entry (R11)
>
> An Engineering Session Report records each Work Package as one table row; detail stays in the EIP and the bridge transcript.
>
> | WP | EIP | Commit | CI run | Design review | Post-commit review | Decisions | Deviations |
> |---|---|---|---|---|---|---|---|
> | WPn | EIP-ESRxxxx-nnn vX | `abc1234` | run id, result | reviewer, verdict, findings | reviewer, verdict | approvals with timestamps | anything not as designed |
>
> # 8. Template
>
> ```text
> # EIP-ESRxxxx-nnn - <Title>
> # 1. Document Control   (table: ID, Title, Version, Status, Session, Work Package, Risk class)
> # 2. Purpose
> # 3. Repository Context Investigated
> # 4. Scope
> # 4A. Commit Contents
> # 5. Evidence Pack
> # 6. Explicitly Out of Scope
> # 7. Validation Requirements
> # 8. Questions for the Engineering Reviewer
> # 9. Review Record
> # 10. Version History
> ```
>
> # 9. Related Artefacts
>
> [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (Approval Economy, Delivery Cadence and Independent Review), [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]], [[CHR-0002_ENGINEERING_CONSTITUTION|CHR-0002]].
>
> # 10. Version History
>
> | Version | Date | Author | Summary |
> |---|---|---|---|
> | 1.0 | 6 October 2026 | Claude Engineering Implementer | ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0008, R3, R11): rewritten as the EIP standard and template - numbering, lifecycle and approval (A5/A6), mandatory sections including the full commit contents, evidence pack, tabular ESR entry. Replaces the unused 0.2 Engineering Execution Package template. |
> | 0.2 | (unchanged) | | |

(The 0.2 and earlier history rows are kept beneath the new 1.0 row.)

## 6.6 EBR-0001 and REG-0001

EBG-0008, EBG-0066, EBG-0130 and EBG-0134 set to Completed, each citing ESR-0061 WP1b and the artefact that closes it (TPL-0001 1.0; RSC-0001 Section 4B; RSC-0001 2.0 and LGB-0001 1.3; PCB-0001 3.0 and the matrix 3.0). REG-0001 rows synced, including TPL-0001's new title, version and status.

---

# 7. WP1c - Design (Code WP, Rule A6: Design Approval, Then Approval of the Built Result)

Drafted at v0.6 (6 October 2026) from the source, not from the outline. Risk class: standard. Reviewer: Antigravity CLI with a Gemini model, standing in under D19 while Copilot's quota is exhausted (until 1 November 2026).

## 7.1 What changed since the outline

* **Gemini CLI no longer exists for this use.** Google replaced it with Antigravity CLI on 18 June 2026 (Google's quota page and blog, read 6 October 2026). The second reviewer is therefore Antigravity CLI (`agy` 1.2.2, already installed and signed in on the Programme Sponsor's existing Google AI Pro subscription), always with a Gemini model. No sign-in step remains. Its terms (antigravity.google/terms) let Google use prompts and code to improve its models, with human review - acceptable for this public repository, so review prompts must never contain household personal data.
* **R7's gap is wider than the outline said.** `parse_register_rows()` only accepts IDs matching `^[A-Z]+-\d{4}$`, so the validator never version-checks 97 register rows: every EIP (`EIP-ESR0061-001` style, 77 rows), `JARVIS_PRODUCT_ARCHITECTURE`, the Capability Readiness Matrix and suffixed rows such as `ESR-0005A`. `bump_version.py` reuses the same parser, which is why it refused those rows this session. A simulation with a wider ID rule surfaces only four problems: two malformed rows (one whose ID cell opens a wiki link to RBL-0007's file but never closes it, and `ESR-0005-RELOAD`, which has no matching file) and two archive files with no version.
* **R10's warnings are mostly one heuristic's blind spots.** `_referenced_artefact()` only accepts an artefact ID or link *immediately* before "Section N". A sample of the warnings shows five patterns: the artefact named in an earlier cell of the same table row; a qualifier between the ID and "Section" ("JRM-0001 Track B Section 7.1", "UAM-0001's own Section 8.2"); a follow-on reference in the same clause ("MDS-0001 Section 9 ... and Section 10"); lists where only the first number is parsed ("Sections 6.1, 6.2, 6.3"); and narrative inside Version History tables.
* **R4's scope is 26 files, not a handful.** 41 lines across 26 artefacts call an RBL the "current" baseline: five live ones re-synced at every closure (README, COC-0001, PBK-0001, PCB-0001, the matrix) and about 21 frozen since July that still name RBL-0009 (ADR-0001 to ADR-0006, CHR-0001, MOD-0001, STD-0001/0003/0004/0006 and others).

## 7.2 Design

**R4 - single-source current baseline.**
1. The five live artefacts stop naming the baseline: their lines become "the current accepted repository baseline is recorded in [[PST-0001_PROGRAMME_STATUS|PST-0001]]". README's "Current Engineering Focus" row likewise points to PST-0001. Closure sweeps then update PST-0001 only.
2. New validator check `check_current_baseline_claims()`: in the five live artefacts plus README, a line saying "current (accepted) (repository) baseline" next to an RBL link is an **error**. In any other non-archive file it is a **warning** naming the file, so the 21 frozen claims are visible and reworded when each artefact is next revised, without 21 version bumps now. Session reports, review records, baselines and Version History rows are excluded (they record the baseline as it was).
3. **Programme Sponsor decision (direct chat, 6 October 2026): "warnings".** The 21 frozen claims stay as visible validator warnings and are reworded when each artefact is next revised; no bulk rewording in this WP.

**R7 - REG-0001 sync.**
1. `parse_register_rows()` accepts every register-row ID shape in use - including `EIP-ESR####-###`, `JARVIS_*` and suffixed IDs - while still skipping Version History rows (a row counts only if it has at least 8 cells and a location-like eighth cell). Both the validator and `bump_version.py` gain this through the shared parser.
2. New status check: an artefact's Document Control Status must equal its REG-0001 Status (an error); a document with no Status field is a warning, as a missing version is today. Three genuine mismatches exist (RBA-0001, RPCA-0001, ESR-0004, all closed records); their REG-0001 rows are corrected to match the documents.
3. The two malformed rows are repaired.
3A. **CI-safety gate (design review finding 2):** the wider parser, the new status check and every fix it needs land in the same commit, and the commit is only submitted once `python scripts/validate_repository.py` reports 0 errors on the exact tree being committed (`submit-response` and the pre-commit hook re-run it independently). The 6 October simulation of all 97 newly checked rows found four problems - the two malformed rows (3) and two unversioned archive files (`aiems/History`, exempted under R10) - and no version mismatches; the build re-runs it before submission and fixes anything new.
4. `bump_version.py`: `--author` becomes **required** (no default - it defaulted to "Claude Engineering Reviewer", wrongly labelling every row written this session); the Version History heading pattern also accepts "Refresh History" (the matrix's heading).

**R8 - post-commit pre-check and reviewer wrapper.**
1. `scripts/post_commit_precheck.py <commit> [--eip PATH]` - a deterministic report, run before the AI post-commit review and handed to it:
   * the working tree is clean and the commit is on `origin/main`;
   * if `--eip` is given, the commit's changed files equal the EIP's Commit Contents list (paths parsed from its backticks);
   * the latest `submit-response` transcript entry for the session/WP records the commit's parent as `repository_ref`;
   * pytest, ruff and the validator are re-run. **Hard checks** (non-zero exit): pytest has 0 failed and 0 errors, ruff is clean, the validator has 0 errors. **Advisory checks** (reported, never failing - design review finding 3): any "N passed", "N skipped" or "N warnings" figure in the commit message is compared with the actual result and a difference is shown, since those counts legitimately move.

   It exits non-zero only on a hard-check failure or a mismatch in the first three bullets. It replaces nothing: the independent post-commit review still runs.
2. `scripts/run_reviewer.py --tool {copilot,antigravity} --session S --wp W --prompt-file F [--resume "text"]`:
   * appends the standard TOOL RULES block for the tool;
   * runs it with the right flags - Copilot's scoped `--allow-tool` and `--deny-tool='write'`, which now include `shell(python -m pytest:*)` so its own validations are not refused; Antigravity with `--model gemini-3.1-pro-high --effort high` headless;
   * saves the output under `.aiems-exchange/reviews/` (git-ignored);
   * detects the two known failure modes - Copilot's "exceeded your monthly quota" and Antigravity's "no output produced ... auto-denied" - reporting the refused command from the Antigravity log so a resume is one step;
   * confirms afterwards that a new `sender: reviewer` entry appeared in the transcript, and says so plainly if not.

   It never writes findings itself.
3. `scripts/reviewer/antigravity_allowlist.json`: the tested allow-list, every rule anchored (`^...$`) so nothing can be appended. Exactly (hardened after design review finding 1):
   * `read_file` on the repository;
   * `git` with **only** the subcommands `log`, `show`, `diff`, `status`, `rev-parse`, `ls-files`, `grep`, `cat-file` (so `clean`, `reset`, `add`, `commit`, `push`, `branch`, `checkout` are refused), arguments with no `=`, no long option starting `--ou` (blocks `--output FILE` and `--output=FILE`, which write a file) and no short `-O` (blocks `git grep -O<pager>`, which launches a program); the bare `--` separator is allowed;
   * `cat` and `grep` on files; `ls`; `head`/`tail -n N FILE`; `wc`;
   * a `git`, `cat` or `grep` command may be followed by up to two read-only filters (`grep`, `head -n N`, `tail -n N`, `wc`);
   * `python -m pytest` with optional `-q` and **path arguments only** (no options, so no `--junitxml`, `-p`, `-c`);
   * `python -m ruff check` with **path arguments only** (no `--fix`);
   * `python scripts/validate_repository.py` with no arguments;
   * `python scripts/aiems_bridge.py return-findings` with a quoted message barring `` "`$;&|<> ``.

   Never allowed: `python -c`, redirects, `;`, `&`, `$`, backticks, any other command. The live copy in `~/.gemini/antigravity-cli/settings.json` was hardened the same way on 6 October 2026, before any further review. `run_reviewer.py --check-settings` reports any difference from the live file; `--install-settings` merges the list only when explicitly asked and never adds deny rules, so interactive use is unaffected. **Tests** assert that the list allows the read-only commands the reviews used and refuses: `git clean -fdx`, `git reset --hard`, `git add .`, `git push`, `git branch x`, `git diff --output x`, `git log --output=x`, `git grep -Ovim x`, `ruff check --fix`, `pytest --junitxml x`, `pytest -p x`, `python -c ...`, redirects and chained commands. The tests use Python's `re`; the build also runs a short live probe of the real `agy` matcher on a sample of allowed and refused commands, because its regex engine (likely Go RE2) may differ - the rules avoid look-around and back-references for that reason.
4. The bridge preflight already accepts any reviewer tool through `AIEMS_REVIEWER_TOOL` (presence plus `--version`; `agy --version` returns 1.2.2), so it needs no change - only documentation.

**R10 - section-reference warnings.** `_referenced_artefact()` and `check_section_references()` gain the five patterns in 7.1: an earlier table cell in the same row; up to four intervening words with no sentence punctuation; inheritance by a follow-on reference in the same clause; every number in a list; and skipping Version History and Refresh History tables. Remaining warnings are then either fixed (genuine broken references in live documents) or listed in the completion report. The three unversioned HST archives become a stated exemption for `aiems/History`. Target: the actual before and after counts are reported; no promise of zero.

**R2/D19 - governance text.** PBK-0001's Independent Reviewers bullet named Gemini CLI. Exact replacement text, included in this WP's commit: "**Second independent reviewer:** Antigravity CLI (Google's successor to Gemini CLI, which it replaced on 18 June 2026), always run with a Gemini model, never a Claude model, under the read-only permission allow-list in `scripts/reviewer/antigravity_allowlist.json` ..." followed by the existing rest of that bullet unchanged.

**D29 - advisory local pre-screen.** `scripts/local_prescreen.py [--base B] [--head H]` sends the diff to LM Studio's OpenAI-compatible endpoint (`http://localhost:1234/v1/chat/completions`, as used by the 2 October scorecard). The model is found by listing `/v1/models` for an id containing `gpt-oss-20b` (override: `AIEMS_PRESCREEN_MODEL`). The output is headed "ADVISORY - NOT INDEPENDENT REVIEW" and saved under `.aiems-exchange/prescreen/`; it never writes to the transcript. If the server is not running (the case on 6 October), it prints a skip message and exits 0. Large diffs are truncated with a notice. Standard library only.

## 7.3 Evidence Pack (TPL-0001 1.0 Section 6)

| Item | Content |
|---|---|
| API facts | `agy` 1.2.2 flags `-p`, `--model`, `--effort`, `--print-timeout`, `-c` (from `agy --help`); headless mode auto-denies unlisted tools and aborts the run (observed seven times on 6 October); allow-list syntax `action(target)` with `command(regex:...)` and precedence Deny > Ask > Allow (antigravity.google/docs/permissions, read 6 October 2026); Copilot flags as used at ESR-0060 and on 6 October; LM Studio `POST /v1/chat/completions` with `model`, `messages`, `temperature`, `max_tokens` (2 October scorecard script); `GET /v1/models` - **not verified live** (server off on 6 October), verified in the build before relying on it. |
| Platform coverage | Windows is where reviewers run; every script is pure-Python standard library with list-form `subprocess`. Copilot is an npm `.cmd` shim on Windows, which needs `shell=True` there (the bridge's own documented precedent); `agy.exe` does not. Nothing is macOS-specific. |
| CI | The CI `python` job (`ubuntu-latest`) runs pytest and the validator; all new tests mock `subprocess`, HTTP and the reviewer CLIs, so they run on Linux. No workflow change. The new validator errors must pass on the repository as committed (the R4/R7 fixes land in the same commit). |
| Tests | New or updated: `test_validate_repository.py` (wider register IDs; status check; current-baseline check, live versus frozen; each R10 pattern, plus guards showing a genuinely broken own-document reference still warns); `test_bump_version.py` (required `--author`; "Refresh History"; an EIP row and a `JARVIS_*` row); `test_post_commit_precheck.py`; `test_run_reviewer.py` (flag construction, quota and denial detection, missing-verdict reporting, allow-list refusals); `test_local_prescreen.py` (server down skips with exit 0; the advisory header; truncation). Tests for the parser and the `--author` change are shown failing on the old code. |
| New dependencies and features | None. No new packages, no CI change, no OS permission. One change to the Programme Sponsor's machine already made at their direction: the allow-list in `~/.gemini/antigravity-cli/settings.json` (6 October 2026). |

## 7.4 Commit Contents (final, as built)

New: `scripts/post_commit_precheck.py`, `scripts/run_reviewer.py`, `scripts/local_prescreen.py`, `scripts/reviewer/antigravity_allowlist.json`, `scripts/tests/test_post_commit_precheck.py`, `scripts/tests/test_run_reviewer.py`, `scripts/tests/test_local_prescreen.py`.

Changed: `scripts/validate_repository.py`, `scripts/bump_version.py`, `scripts/tests/test_validate_repository.py`, `scripts/tests/test_bump_version.py`, `scripts/README.md`, `README.md`, `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md`, `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`, `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/reviews/EIP-ESR0061-001_RELEASE_GATE_GOVERNANCE_AND_STREAMLINING.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`.

**Added during the build** (disclosed, 7.5): `aiems/governance/baselines/RBL-0007_REPOSITORY_BASELINE.md` and `aiems/governance/reviews/EIP-ESR0046-001_USER_IDENTITY_AND_PROFILE_FOUNDATION.md` - one stale Status cell each, surfaced by the new status check.

## 7.5 Build Record (6 October 2026)

| Item | Result |
|---|---|
| R7 | `parse_register_rows()` now covers every ID shape and keeps a piped WikiLink in its cell. **Correction to 7.1:** the "malformed" RBL-0007 row was not malformed - the parser split the pipe inside its WikiLink's display-text separator, which is a parser bug, now fixed. `ESR-0005-RELOAD` is a genuine compound ID, now resolved by `find_registered_file()`. **The status check found 12 genuine mismatches, not 3** (the simulation had only covered rows the old parser could read): 10 register rows synced to their documents' more precise Status, and 2 documents (RBL-0007 "Pending Acceptance", EIP-ESR0046-001 "Approved - implementing") corrected because their own Status was stale, each with a version bump. `bump_version.py --author` is required, and the "Refresh History" heading is accepted - shown working by bumping the Capability Readiness Matrix, which it had refused before. |
| R10 | "Section N" warnings: about **342 to 260**. The remainder are mostly references whose referent is set by the paragraph, not the line (for example a whole EIP discussing GAM-0001), which a line-level check cannot resolve; no promise of zero was made. Every number in a list is now checked, which adds a few genuine warnings. Unversioned/unstatused `aiems/History` archives are exempt from the register warnings. |
| R4 | No current-baseline claim remains in the five live artefacts or README; 28 frozen claims now show as warnings (Programme Sponsor decision "warnings"). |
| R8 | `post_commit_precheck.py` - while testing, found and fixed its own parser: the validator prints "0 errors" when passing but "2 error(s)" when failing. `run_reviewer.py` - **two hardenings beyond the design**, both narrowing: Copilot's `--allow-tool` rules are now read-only (ESR-0060's `shell(git:*)`/`shell(python:*)` also allowed `git push` and `python -c`); and the full prompt is written to a git-ignored file, with the CLI given only a fixed shell-safe instruction to read it, so no prompt text reaches a Windows `cmd.exe` command line. Two bugs found by its tests and fixed: same-second verdict timestamps were ignored, and the Antigravity log path could not be redirected. |
| Live matcher probe | Real `agy` with the committed allow-list: a piped `git grep ... | grep -v ... | wc -l` ran (output 118); `git diff --output FILE` was refused and no file was created - matching the Python-regex tests. |
| D29 | `local_prescreen.py` skips cleanly (LM Studio not running on 6 October). `/v1/models` remains unverified live; the script treats any failure as a skip. |
| Tests | 85 new tests (validator 19, `bump_version` 3, `run_reviewer` 51, pre-check 7, pre-screen 5). The R7 parser, status and compound-ID tests, the R10 pattern tests, the R4 tests and the `--author`/"Refresh History" tests were each run against the old code first and failed there. Full suite **844 passed, 1 skipped**; ruff clean; validator **0 errors** once this EIP's own register row is synced at commit. |

---

# 8. Validation Requirements

* WP1a/WP1b: validator 0 errors; any new warnings only of the known "Section N not found" false-positive class that R10 fixes (cross-document references such as "UAM-0001 Section 8.2"); pytest unchanged (759 passed, 1 skipped); every changed artefact's REG-0001 row matches its Document Control; every wiki link resolves.
* WP1c: new tests for each script and validator check, each shown failing before the change where applicable; full pytest, ruff and validator green; CI green on all jobs.

# 9. Explicitly Out of Scope

* Any product code (`jarvis/`, `sentinel/`, `src/`, `src-tauri/`) - WP2 onwards.
* Deleting qwen3-coder from E: (D29 item 3) - a Programme Sponsor housekeeping action outside the repository.
* EBG-0090 - closes in WP3 with ADR-0023 Section 2 item 3 as its answer.

# 10. Questions for the Engineering Reviewer

1. Is a new ADR-0023 the right home for D25-D28, or should ADR-0008 be amended instead?
2. Is the WP1a / WP1b / WP1c split sound, and is WP1c-before-WP2 (Section 3) the right way to handle WP2's need for the second reviewer?
3. Does the Capability-Honest Interface text (5.1.1) fully preserve the retained rule?
4. Does any text in Section 5 contradict another controlled artefact not listed here?

WP1c (Section 7, added at v0.6):

5. R4: leave the 21 frozen "current baseline" claims as visible warnings (recommended), or reword all of them now with 21 version bumps? This is also a Programme Sponsor decision.
6. R7: is a wider register-ID rule safe - can it pick up a non-artefact row (Version History, notes) as an artefact? Is the status check worth its three corrections?
7. R10: do the five heuristics risk hiding genuinely broken references? Are the proposed guard tests enough?
8. R8: is a pre-check that compares commit-message figures with real results robust enough to be useful, or will it be brittle?
9. Is anything in the 7.3 evidence pack wrong or missing - in particular the Antigravity allow-list's safety, and Windows/Linux behaviour in the new scripts?

---

# 10A. Design Review Record

**v0.1 design review** (GitHub Copilot CLI through the bridge, `ESR-0061`/`WP1`, 2026-10-06T07:19:31Z, `sender: reviewer`): **Conditional Pass**, no High findings. The reviewer also posted a stray one-word "test" entry at 07:18:47Z before its real verdict; it carries no content. Its tool permissions blocked its validator and pytest runs on the first attempt - the very gap R8 fixes - so it relied on the figures re-run by the Engineering Implementer (pytest 759 passed/1 skipped; validator 0 errors).

| # | Finding | Disposition in v0.2 |
|---|---|---|
| 1 (Medium) | ADR-0008's own Review Trigger is met, but WP1a left it untouched | Fixed: 5.5A adds a Subsequent Architectural Update pointer (ADR-0008 1.1) |
| 2 (Low) | Capability-Honest Interface is a general rule but sat under Feature-First Delivery Discipline | Fixed: now its own top-level section (5.1.1) |
| 3 (Low) | New UAM-0001 8.1 dropped the EBG-0028 traceability pointer | Fixed: pointer restored (5.3.3) |

Questions in Section 10, as answered: (1) a new ADR is right, with a pointer in ADR-0008 (finding 1); (2) the WP1a/b/c split and WP1c-before-WP2 are sound; (3) the capability-honest rule is preserved verbatim and strengthened; (4) the "Version 1.0 = Family AI OS" contradiction is confined to the one artefact WP1a fixes, and every target anchor exists exactly once. The reviewer verified that the EBG-0161 defect reproduces, that every disposition matches its row's current text, and that EBG-0161 to EBG-0169 do not collide.

**WP1a post-commit review** of `1978070`. Copilot CLI's run stopped on its monthly quota before recording a verdict. Under D19 the second reviewer stood in: **Antigravity CLI** with a Gemini model (`gemini-3.1-pro-high`) on the Programme Sponsor's existing Google AI Pro subscription (Google replaced Gemini CLI with Antigravity CLI on 18 June 2026). It ran headless with a read-only permission allow-list; its run was refused, and resumed, three times on read-only command patterns not yet allowed (`git ... | grep`, a quoted grep pattern, `| head`), each then allowed; an attempted `> file` redirect stayed refused. Verdict recorded at 2026-10-06T08:21:32Z (`sender: reviewer`, `repository_ref: 1978070`): **Fail**, one High finding - the commit added WR-ESR0061-001, which Section 5 did not list, so under a strict reading of rule A5 it was unapproved. Otherwise Section 5 landed exactly, versions and register rows aligned, the v0.1 findings were fixed, and the validator was clean.

**Disposition: Programme Sponsor override under D19** (direct chat decision "1", 6 October 2026). The Engineering Implementer's assessment, accepted by the Programme Sponsor: Low rather than High - the approval request explicitly named the Working Report as part of the commit, the plan's handover step 2 required registering it in a single A5 commit, and Copilot had reviewed it at v0.1. The genuine gap is that Section 5 did not list every file in the commit; the session report and this EIP were outside it in the same way. **Fix:** TPL-0001 1.0 (6.5) adds a mandatory Commit Contents section, and WP1b's own commit contents are listed at the top of Section 6.

**WP1b review** (Section 6 at v0.4; Antigravity CLI, Gemini 3.1 Pro, standing in for quota-exhausted Copilot; bridge `ESR-0061`/`WP1b`, 2026-10-06T08:47:53Z, `sender: reviewer`, `repository_ref: 9e6c1ea`): **Conditional Pass**. Every anchor exists exactly once and reads coherently; every PCB-0001 and matrix claim matches the code and EBR-0001; RSC-0001 2.0's fresh-install scores match the plan and the code; the EBG-0130 contradiction is genuinely resolved; rewriting TPL-0001 is the right call (remaining references to its old content are only in historical ESR-0017/ESR-0019 records); the commit contents are complete. The run was refused, and resumed, four times on read-only command patterns not yet allowed (`cat`, `grep` on a file, `cat | grep -A`), each then allowed.

| # | Finding | Disposition in v0.5 |
|---|---|---|
| 7 (Medium) | Section 6's intro falsely claimed the plan lists a JRM-0001 sweep and PST-0001 Section 8 for WP1; it does not, and the plan sets JRM-0001's post-launch order at WP9 - unapproved scope under a false citation | **Accepted and fixed** by removing both (former 6.6 and 6.7) and correcting the intro; confirmed against the registered plan - the wording came from an uncommitted earlier draft. A removal only, so no re-review is needed; the reviewer's stated condition is met |

**WP1c design review** (Section 7 at v0.6; Antigravity CLI, Gemini 3.1 Pro; 2026-10-06T09:35:01Z, `sender: reviewer`, `repository_ref: 23e95bd`): **Fail**. Its run was refused, and resumed, four times: three on read-only patterns then allowed (pipe into `wc`, two chained filters), and once on `python -c` with an inline script, which stays refused permanently - arbitrary code is never allowed to the reviewer. It verified the factual claims about the scripts and the CI platform.

| # | Finding | Engineering Implementer assessment | Disposition in v0.7 |
|---|---|---|---|
| 1 (High) | Allow-list safety: "read-only git without `=` arguments" permits `git clean -fdx`, `git reset --hard`, `git add`; `ruff --fix` writes files | **Partly wrong, partly right.** The live rule already restricted git to eight read-only subcommands, so `clean`/`reset`/`add` were refused - the EIP's wording was too loose to show that. But following the finding, real holes existed: `ruff check --fix` and pytest options such as `--junitxml` (write files), `git diff --output FILE` with a space (writes a file), and `git grep -O<pager>` (launches a program) | **Fixed**: 7.2 R8 point 3 now states the exact rule set; the live list was hardened at once and tested against 13 allowed and 15 refused commands; tests and a live `agy` probe are part of the build |
| 2 (High) | R7 could break CI if any of the 97 newly checked rows is out of sync | Valid as a risk; the 6 October simulation found four problems and no version mismatches | **Fixed**: 7.2 R7 point 3A makes "validator 0 errors on the exact committed tree" an explicit gate, with the simulation re-run in the build |
| 3 (Medium) | Exact "N passed" comparison is brittle | Valid | **Fixed**: hard checks are failures and errors only; count comparisons are advisory |
| 4, 5 (Info) | Q5 - leave the frozen R4 claims as warnings; Q7 - the R10 guard tests are adequate | Agreed (Q5 matches the Programme Sponsor's "warnings" decision) | None needed |

**WP1c design re-review** (v0.7; Antigravity CLI, Gemini 3.1 Pro, fresh conversation; 2026-10-06T09:39:30Z, `sender: reviewer`): **Pass**, information-only notes. It confirmed the Engineering Implementer's assessment that the original live rule already refused `clean`/`reset`/`add`, that the hardened rule set blocks file modification, git state changes and arbitrary code, that the R7 point 3A gate prevents a CI break, and that the hard/advisory split in R8 is sound. Ran without a single refused command.

**WP1c implementation review** (v0.8 built tree; Antigravity CLI, Gemini 3.1 Pro, run through the new `scripts/run_reviewer.py`; 2026-10-06T10:09Z, `sender: reviewer`): **Pass**, no findings. It re-ran pytest (844 passed, 1 skipped), ruff (clean) and the validator (0 errors, 303 warnings), judged the allow-list and the prompt-by-file approach safe, and accepted the two hardenings beyond the design and the two files added during the build. The run needed no allow-list change and no resume - the wrapper's first real use. **Engineering Implementer's caveat, disclosed:** the review is brief and largely affirmative, and Gemini was the only reviewer (Copilot's quota is exhausted until 1 November). One path is untested live: `run_reviewer.py --tool copilot` on Windows (Copilot is a `.cmd` shim launched without `shell=True`; its arguments are fixed shell-safe strings). It is exercised by unit tests only, and should be run live once the quota resets.

Two further v0.5 changes found by the Engineering Implementer while applying the text, both disclosed rather than re-reviewed: TPL-0001 keeps its filename instead of being renamed, which avoids editing links in archived histories and closed records (a reduction in scope); and LGB-0001 Section 7 gains one sentence, so that "both Must-Ship items are now delivered" does not contradict the new Section 4 (the reviewer did not raise this).

Also in v0.5: Section 5's quoted ADR-0023 and UAM-0001 text brought into line with the committed personal-data minimisation (`9e6c1ea`, ADR-0023 1.1, UAM-0001 1.7); the committed artefacts are authoritative.

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.8 | 6 October 2026 | Claude Engineering Implementer | WP1c built per the approved v0.7 design (Programme Sponsor "Approved", rule A6 gate 1). Build record 7.5: 12 status mismatches fixed (not 3); the RBL-0007 row was a parser bug, not malformed; Section N warnings about 342 to 260; Copilot permissions narrowed and prompts passed by file (beyond the design, both narrowing); live agy matcher probe matches the tests. 85 new tests; 844 passed, 1 skipped. Awaiting implementation review. |
| 0.7 | 6 October 2026 | Claude Engineering Implementer | WP1c design review Fail (Antigravity CLI): two Highs and a Medium fixed - allow-list stated exactly and hardened (live list too: no ruff --fix, no pytest options, no git --output or grep -O), explicit validator-clean gate for the wider register parser, advisory-only figure comparison. R4 decision "warnings" recorded. Awaiting re-review. |
| 0.6 | 6 October 2026 | Claude Engineering Implementer | WP1a and WP1b closed (1978070, 9e6c1ea, 23e95bd all CI green; post-commit reviews of 9e6c1ea and 23e95bd Pass). WP1c full design and evidence pack (Section 7) drafted from the source: second reviewer is Antigravity CLI (Gemini CLI replaced 18 June 2026); register parser blind to 97 rows; R10's five heuristic gaps; R4's 26 files. Questions 5-9 added. Awaiting design review. |
| 0.5 | 6 October 2026 | Claude Engineering Implementer | WP1b review Conditional Pass (Antigravity CLI, Gemini 3.1 Pro); its Medium finding accepted - the JRM-0001 sweep and PST-0001 Section 8 update removed (wrongly cited as plan scope). Section 5 quotes aligned with the committed personal-data minimisation (9e6c1ea). |
| 0.4 | 6 October 2026 | Claude Engineering Implementer | WP1a post-commit review (Antigravity CLI, Gemini 3.1 Pro, standing in for quota-exhausted Copilot): Fail on one High - Working Report not listed in Section 5; overridden by the Programme Sponsor, recorded in 10A. TPL-0001 text gains a mandatory Commit Contents section; WP1b commit contents listed; Section 6 wording made neutral ("the household Mac") per D23 minimisation. |
| 0.3 | 6 October 2026 | Claude Engineering Implementer | WP1a committed as 1978070 (Sponsor Approval Service approval at e153874, 07:41:15Z; submit-response 07:42:32Z); CI run 37431602802 green on all five jobs. Post-commit Copilot review cut short by its monthly quota before a verdict. WP1b exact text drafted (Section 6, D22), adding the JRM-0001 sweep and PST-0001 Section 8 that v0.2 omitted; TPL-0001 proposed for rewrite as the EIP standard. |
| 0.2 | 6 October 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot CLI); all three findings fixed: ADR-0008 pointer note added (5.5A), Capability-Honest Interface made a top-level PBK-0001 section, EBG-0028 pointer restored in UAM-0001 8.1. Review record added (10A). EBG-0016 disposition corrected to Rejected (EBR-0001 Section 8 defines no "Closed - not adopted" status). |
| 0.1 | 6 October 2026 | Claude Engineering Implementer | Initial draft at ESR-0061 WP0B. WP1 split into WP1a (governance, exact text), WP1b (release gate, design) and WP1c (tooling, outline); WP2 dependency on WP1c flagged. Awaiting design review. |
