# EIP-ESR0061-001 - Release Gate, Governance and Streamlining

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-001 |
| Title | Engineering Implementation Package: WP1 Release Gate, Governance and Streamlining |
| Version | 0.2 |
| Status | Draft - design review Conditional Pass, findings fixed; WP1a awaiting Programme Sponsor approval |
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
> 2. **A smooth frame rate** on the household PC and the Apple M1 Pro; the numeric target is set in the redesign Work Package's design.
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
> Version 1.0 will be used in a UK household by adults and by a 15-year-old under the Child role, on Windows and macOS, and then released publicly. Today a fresh install has no working provider unless API keys are set in environment variables. Each provider's own terms decide whether a family app with a minor may use it.
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

# 6. WP1b - Design (exact text follows in v0.2)

* **EBG-0130 release gate.** RSC-0001 re-scored (version 2.0) against a **fresh install on Windows and macOS**, not the development checkout, using WR-ESR0061-001 Section 4.1's assessment. The Orb item is scored against UAM-0001 Section 8.2's criteria (D3), so it is a genuine launch blocker until WP4. A new **Release-Candidate Checklist** section becomes the actual gate: CI green on the tag (Linux, Windows, macOS); installers and checksums published; install and launch smoke test on a clean machine per OS; first conversation with Ollama only; escalation with and without a key; voice unavailable and available paths; backup and restore; Child-role safeguards; household soak. LGB-0001's Must-Ship list is reconciled with RSC-0001 so the two give one answer.
* **EBG-0066.** Scored go/no-go dimensions added to RSC-0001 (product readiness, platform coverage, safety, documentation, repository integrity, review coverage), plus a short AIEMS maturity index read from data the repository already holds (validator results, review coverage, backlog age). No new artefact.
* **EBG-0134.** PCB-0001 and the Capability Readiness Matrix re-audited against delivered code, not just pointer-synced.
* **EBG-0008 + R3 + R11.** TPL-0001 extended into the EIP standard: mandatory sections, numbering, lifecycle and approval rules (A4-A6); an **evidence pack** (affected-API facts checked against source, Windows and macOS coverage, CI jobs that will run it, test list, new dependencies); a **tabular ESR Work Package entry** (commit, CI run, review verdicts, decisions, deviations). Extending TPL-0001 rather than creating a new standard follows Minimise Controlled Artefact Creation.

# 7. WP1c - Design outline (full design in v0.3)

* **R4.** PST-0001 becomes the single statement of the current baseline. Other artefacts say "see PST-0001"; README's per-session rows become a pointer. New validator check: a hard-coded "current baseline is RBL-NNNN" claim outside PST-0001 is an error.
* **R7.** New validator check: each artefact's Document Control version and status must match its REG-0001 row. `bump_version.py`'s row parser fixed for the row shapes it currently misses (disclosed by hand at ESR-0060).
* **R8.** `scripts/post_commit_precheck.py`: proves the committed tree equals the reviewed tree, re-runs pytest, ruff and the validator, and checks commit-message figures against the actual results. `scripts/run_reviewer.py`: one wrapper for Copilot and Gemini CLI with read-only tools that still allow `git`, `python -m pytest`, `ruff` and the validator, so the reviewer can run its own validations.
* **R10.** The "Section N not found" heuristic changed to skip references qualified by another artefact (for example "GAM-0001 Section 8.1" or a wiki link in the same sentence); the remaining genuine broken references fixed; the three unversioned HST files given a justification record.
* **R2/D19.** Gemini CLI terms (free tier limits, data use) verified **before** any use and recorded; the Programme Sponsor signs in once; `AIEMS_REVIEWER_TOOL=gemini` supported by the wrapper and the bridge preflight.
* **D29.** `scripts/local_prescreen.py`: sends a diff to LM Studio's local API (gpt-oss-20b), with output headed "ADVISORY - NOT INDEPENDENT REVIEW". Skips cleanly if LM Studio is not running. Never a gate.
* **New dependencies:** none expected (standard library HTTP for LM Studio). Any change is listed here before design approval (A4).

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

---

# 10A. Design Review Record

**v0.1 design review** (GitHub Copilot CLI through the bridge, `ESR-0061`/`WP1`, 2026-10-06T07:19:31Z, `sender: reviewer`): **Conditional Pass**, no High findings. The reviewer also posted a stray one-word "test" entry at 07:18:47Z before its real verdict; it carries no content. Its tool permissions blocked its validator and pytest runs on the first attempt - the very gap R8 fixes - so it relied on the figures re-run by the Engineering Implementer (pytest 759 passed/1 skipped; validator 0 errors).

| # | Finding | Disposition in v0.2 |
|---|---|---|
| 1 (Medium) | ADR-0008's own Review Trigger is met, but WP1a left it untouched | Fixed: 5.5A adds a Subsequent Architectural Update pointer (ADR-0008 1.1) |
| 2 (Low) | Capability-Honest Interface is a general rule but sat under Feature-First Delivery Discipline | Fixed: now its own top-level section (5.1.1) |
| 3 (Low) | New UAM-0001 8.1 dropped the EBG-0028 traceability pointer | Fixed: pointer restored (5.3.3) |

Questions in Section 10, as answered: (1) a new ADR is right, with a pointer in ADR-0008 (finding 1); (2) the WP1a/b/c split and WP1c-before-WP2 are sound; (3) the capability-honest rule is preserved verbatim and strengthened; (4) the "Version 1.0 = Family AI OS" contradiction is confined to the one artefact WP1a fixes, and every target anchor exists exactly once. The reviewer verified that the EBG-0161 defect reproduces, that every disposition matches its row's current text, and that EBG-0161 to EBG-0169 do not collide.

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.2 | 6 October 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot CLI); all three findings fixed: ADR-0008 pointer note added (5.5A), Capability-Honest Interface made a top-level PBK-0001 section, EBG-0028 pointer restored in UAM-0001 8.1. Review record added (10A). EBG-0016 disposition corrected to Rejected (EBR-0001 Section 8 defines no "Closed - not adopted" status). |
| 0.1 | 6 October 2026 | Claude Engineering Implementer | Initial draft at ESR-0061 WP0B. WP1 split into WP1a (governance, exact text), WP1b (release gate, design) and WP1c (tooling, outline); WP2 dependency on WP1c flagged. Awaiting design review. |
