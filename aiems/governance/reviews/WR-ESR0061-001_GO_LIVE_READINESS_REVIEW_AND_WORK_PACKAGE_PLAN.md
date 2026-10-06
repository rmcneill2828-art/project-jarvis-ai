# WR-ESR0061-001 - Go-Live Readiness Review and Work Package Plan

---

## Document Control

| Field | Value |
|------|------|
| Artefact ID | WR-ESR0061-001 (Working Report - numbered at ESR-0061 WP0B, 6 October 2026; drafted outside a session as an unnumbered draft) |
| Title | Go-Live Readiness Review and Work Package Plan |
| Version | 0.11 |
| Status | Working Report - **registered; with the Engineering Reviewer** (PBK-0001 Working Report Lifecycle step 1 of 5 complete; step 2 in progress) |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Author | Claude Engineering Implementer |
| Classification | Internal |
| Date | 2 October 2026 |
| Baseline assessed | [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]], `main` at `0669a53` (clean, CI run 36913564033 green) |

This is a Working Report. It is not a controlled artefact, and it authorises nothing. It goes next to the Engineering Reviewer (GitHub Copilot CLI) and then to the Programme Sponsor. Each Work Package still needs its own EIP, design review, Sponsor approval, `submit-response` commit and post-commit review.

---

## 1. Purpose and Decision Register

The Programme Sponsor asked for a readiness review of what is needed to **push Project JARVIS AI live**, as an ordered Work Package plan with timings, run to completion. Decisions taken in conversation on 2 October 2026 are recorded here and enacted formally in WP1.

| # | Decision | Status |
|---|---|---|
| D1 | Go-live target = **MLP 0.1** | **Decided** |
| D2 | Released as **Version 1.0** (`v1.0.0`); the product architecture's future "Version 1.0 = Family AI OS" milestone is renamed in WP1 | **Decided** |
| D3 | The Orb does not pass on basic animation; it must meet the §4.5 acceptance criteria | **Decided** |
| D4-D8 | Voice models downloaded in-app; Windows unsigned unless free signing; `keyring`; household soak first; defer `react-dom` 19 | **Decided** (as recommended) |
| D9-D12 | Incremental rule defunct; full redesign; Orb decoupled; Windows + macOS | **Decided** |
| D13 | EBG-0015/0059 Superseded; 0022/0111/0128 post-launch | **Decided** (as recommended) |
| D14 | Apple M1 Pro, macOS Tahoe 26 → one `aarch64` build | **Decided** |
| D15 | macOS: free one-time "Open Anyway" rather than paid notarisation | **Decided** (as recommended) |
| D16 / D17 | Mac access on agreed dates; daughter (15) under the Child role | **Decided** |
| D18 | Sessions **Tuesday-Friday** | **Decided** |
| D19 | Second independent reviewer, **high-risk WPs only** (and on Copilot quota exhaustion); a High finding from either reviewer blocks; one-time Google sign-in by the Sponsor | **Decided** |
| D20 | Fold record-only commits (= rule A3) | **Decided** (via D24) |
| D21 | Milestone sessions | **Decided** |
| D22 | Pipelined design drafting (design only) | **Decided** |
| D23 | GDPR principles for family data; safety events = category + time, never content | **Decided** |
| D24 | Approval rules A1-A7 | **Decided** |
| D25 | UK; **remove OpenAI**; **Ollama by default, escalate to a more capable model** for research/knowledge; **APIs where possible**; **parental consent required**; option **(A)**: Child restricted to compliant providers | **Decided** → provider strategy §5 |
| D26 | Claude API escalation capped at **£30/month**: set in the Anthropic Console and enforced by JARVIS; falls back to local Ollama at the cap. The only recurring cost in the plan - an explicit exception to the no-budget rule | **Decided** |
| D27 | **Gemini API unregistered** from the shipped product (terms bar apps likely used by under-18s); Gemini CLI for engineering review unaffected | **Decided** |
| D28 | Escalation is **suggested by JARVIS and confirmed by the user** - never automatic | **Decided** |
| D29 | **gpt-oss-20b as an optional, advisory local pre-screen** before Copilot. Never counted as independent review; every finding verified before acting. Set up in WP1 with the Gemini CLI reviewer. Qwen3-Coder rejected | **Decided** (§5A) |
| HW | Household PC: i7-7700K, 32 GB RAM, **RTX 4060 8 GB**. Daughter's Mac: M1 Pro, **16 GB** unified memory | **Provided** → §5.4 |

---

## 2. Executive Summary

**Verdict: not ready to go live. Target Friday 11 December 2026, released as Version 1.0 (MLP 0.1) on Windows and macOS. Planning date 18 December; risk-adjusted January 2027 (Christmas).**

**What changed in v0.7:**
- D25 replaces the provider strategy with **local Ollama by default + the Anthropic Claude API for escalation**. That adds a Work Package (WP3 Provider Strategy, about 4-5 days), which moves the target one week later than v0.6's 4 December.
- **Your VS Code question has a clear answer: no for the product, yes for engineering.** The reasons below come from the actual terms pages, checked today (§5.2).
- **Gemini must leave the product, not just her profile.** Its API terms prohibit use in any application "likely to be accessed by individuals under the age of 18". A family app with a Child role is exactly that (D27).
- **The Claude API can serve a 15-year-old,** provided the safeguards Anthropic requires are in place. JARVIS's planned PIN, moderation and AI disclosure match them almost one for one (§5.3).

**Plan: 9 Work Packages, about 30-38 engineering days** after the bottleneck reductions, at 4 session days a week from Tuesday 6 October.

**Backlog:** 25 of 29 open items closed by go-live; 3 post-launch; 1 conditional.

---

## 3. Evidence Base

As v0.6, plus **terms pages fetched and quoted on 2 October 2026**:

| Source | Exact text (quoted) |
|---|---|
| Anthropic Consumer Terms - anthropic.com/legal/consumer-terms | "You must be at least 18 years old to use the Services." / prohibited: "Except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services through automated or non-human means, whether through a bot, script, or otherwise." / "You may not share your Account login information, Anthropic API key, or Account credentials with anyone else or make your Account available to anyone else." |
| Anthropic - organisations serving minors - support.claude.com article 9307344 | Permitted with safeguards: "Age verification systems to ensure only intended users can access the product"; "Content moderation and filtering to block inappropriate or harmful content"; regulatory compliance documented publicly; inform users "they are interacting with an AI system rather than a human"; "Failure to implement these recommendations… may lead to the suspension or termination of your account." |
| Gemini API Terms - ai.google.dev/gemini-api/terms | "You must be 18 years of age or older to use the APIs." / "You also will not use the Services as part of a website, application, or other service… that is directed towards or is likely to be accessed by individuals under the age of 18." / UK, EEA and Switzerland: paid-service data terms apply even to the free quota |

**Not verified:** GitHub Copilot, OpenAI Codex and Google Antigravity product terms. The GitHub terms page fetched only points to other documents. They are excluded from the product on practical and security grounds regardless (§5.2), and WP1 records their terms only for engineering use.

---

## 4. Readiness Assessment

### 4.1 MLP 0.1 against a fresh install

| Item | Windows | macOS | Closed by |
|---|---|---|---|
| GUI Dashboard | Partial | No build | WP2, WP4 |
| Chat Interface | Partial | No build | WP4 |
| Text Responses | **Fail** (no provider without env vars) | No build | **WP3** (Ollama-first) + WP5 |
| Animated Avatar / Orb | **Fail** | No build | WP4 (§4.5 bar) |
| Basic Voice Input | **Fail** | No build | WP7 |
| Basic Conversation Memory | Pass | No build | WP3, WP5 |
| User Profiles | Pass, roles unenforceable | No build | WP4, WP6 |
| Service Status Dashboard | Partial | No build | WP4 |

### 4.2 UI, 4.3 macOS

As v0.6.

### 4.4 Household safety and GDPR

As v0.6, with the provider-specific rows updated: moderation is now **local** (§5.3); consent records are now explicit (D25.4).

### 4.5 Orb acceptance criteria (D3 confirmed)

1. Five real states (idle, listening, thinking, speaking, offline/error), each driven by an actual event.
2. A smooth frame rate on the household PC and the M1 Pro (target set in WP4's design).
3. Reduced-motion support, with the state also shown in text.
4. Works identically with no repository present.
5. Matches the look you approve in the prototype.

---

## 5. Provider Strategy for Version 1.0 (new)

### 5.1 The shape

| Tier | Provider | When used | Cost | Her profile (Child) |
|---|---|---|---|---|
| **Default** | **Local Ollama** (on each machine) | Every conversation unless escalated | Free; data never leaves the machine (best GDPR position) | Yes, **with local moderation** (§5.3) |
| **Escalation** | **Anthropic Claude API** | Research, knowledge or harder questions, per D28 | Pay-per-use under a hard cap (D26) | Yes, **with recorded parental consent**, moderation and AI disclosure |
| Removed | OpenAI API | - | - | - (D25) |
| Removed | Google Gemini API | - | - | - (D27 - terms) |

Removed adapters are **unregistered, not deleted**, as with Piper at ESR-0053. The code and tests stay, so the decisions can be reversed.

### 5.2 Can we use VS Code / Claude Code / Copilot / Codex / Antigravity instead of APIs?

**For the product: no. For engineering: yes, as today.**

| Reason | Detail |
|---|---|
| **Terms (verified)** | Claude subscriptions: users must be 18+; automated access is barred "except… via an Anthropic API Key"; you may not make your account "available to anyone else". Routing her chats through your Claude subscription would breach all three. |
| **It takes capacity from engineering** | Copilot's monthly quota is the project's independent-review capacity, already the main bottleneck. Spending it on household chat would stall engineering. |
| **Security** | These tools are coding agents with file and shell access. Putting one behind a 15-year-old's chat box exposes the machine to prompt-injection-driven commands. |
| **GDPR** | Consumer subscriptions have different data-use terms from APIs. For her data (D23), API terms or local processing are the defensible choice. |
| **Doesn't work for Version 1.0 users** | Other households can't use your subscriptions. The product needs local models plus bring-your-own API key. |
| **Practical** | It would need VS Code and the CLIs installed and signed in on her Mac. Each turn would start a heavyweight agent session (EBG-0090's own recorded finding). |

**Where subscriptions do belong: your own engineering.** That covers Copilot as reviewer, the Gemini CLI second reviewer (D19), and Claude Code doing the implementation. That use is unchanged. **EBG-0090 closes with this answer.**

### 5.3 What Anthropic requires for minors, and how JARVIS meets it

| Anthropic requirement | JARVIS mechanism | WP |
|---|---|---|
| Access control: "only intended users can access" | Administrator PIN; roles assigned by the Administrator; Child cannot switch profile or change settings | WP6 |
| "Content moderation and filtering" | **Local moderation model via Ollama** (a Llama Guard-class safety classifier; exact model chosen in WP6's design) on Child input **and** output, for both local and Claude replies, plus a child-safety system prompt layer | WP6 |
| Regulatory compliance documented publicly | A public "Children and privacy" page in the user guide: what is collected, where it goes, consent, retention, erasure (UK GDPR) | WP8 |
| Tell users they are talking to an AI | Persistent in-UI disclosure, plus a first-run explanation on Child profiles | WP4/WP6 |
| (Your D25.4) parental consent | An Administrator records consent, with timestamp and scope, before a Child profile may use Claude escalation; her own plain-language acknowledgement is recorded too | WP6 |

Local moderation also closes the gap where a **local** model on its own has no safety filter (raised in v0.5). The earlier plan's reliance on OpenAI/Gemini moderation is gone.

### 5.4 What the hardware has to carry

Ollama-first means each machine runs a chat model, plus a small moderation model for Child profiles.

| Machine | Spec | Assessment | WP3 approach |
|---|---|---|---|
| **Household PC** | i7-7700K, 32 GB RAM, **RTX 4060 8 GB VRAM** | **Strong for local AI.** A 7-8B-class instruction model at 4-bit quantisation (about 5 GB) fits entirely in VRAM with room for a ~1B moderation model; GPU inference gives conversational speed. The CPU is older but is not on the hot path. | Default to a 7-8B Q4 model, GPU-resident. **Keep Ollama's model store on an SSD** - the PC has several HDDs, and loading models from them would be slow. Note: `faster-whisper` can also use the GPU, so check VRAM headroom with chat + moderation + speech loaded together. |
| **Daughter's Mac** | M1 Pro, **16 GB** unified memory | **Workable but tight.** The chat model, moderation model, Kokoro/Whisper and macOS all share the same 16 GB. A 7-8B Q4 model is feasible; a 3-4B model is the fallback if memory pressure or speed suffers. | Start with the larger model; measure in real use on Mac visit 1. Fall back to the smaller model automatically if memory is low, and let the Administrator choose. |

**WP3 acceptance:**
- Measured response time and memory use on **both** machines with the Child-profile moderation path active, against a target set in WP3's EIP.
- The model choice is recorded per machine.
- Specific model names are chosen in WP3/WP6 from current benchmarks and licences, not fixed by this report.

---

## 5A. Local Model as a Backup Reviewer (Continue / LM Studio) - evaluation in progress

**Question (Sponsor, 2 October 2026):** can Continue with LM Studio in VS Code serve as a backup reviewer?

**What is installed:**
- The LM Studio server is running on port 1234, serving `qwen2.5-7b-instruct` and `google/gemma-4-e4b`.
- The `lms` command-line tool is present.
- The Continue extension 2.0.0 is installed.
- The `cn` command-line tool is not.

So Continue itself is an interactive panel and cannot be driven by the bridge. **LM Studio's local API can be**, and is the route for any automated review.

**Blind probe:** the real pre-fix code of EBG-0155 (case-sensitive `JARVIS_PRIMARY_PROVIDER`), which Copilot rated High and reproduced at ESR-0060, given to each model with a neutral review prompt.

| Model | Found the High bug? | False findings | Partly valid | Time |
|---|---|---|---|---|
| gemma-4-e4b (default settings) | No | - (vague) | Unknown names silently ignored | ~250 s |
| qwen2.5:7b (via Ollama) | No | Yes - a "KeyError" that cannot occur (the code uses `.get()`) | - | ~275 s |
| gemma-4-e4b (retuned: max context, GPU offload) | No | Yes - "High" blank-model defect is wrong (`"" or default` falls back correctly; only whitespace would slip through, Low at most) | Unknown primary names silently ignored (Medium) | ~70 s plus reasoning |
| qwen2.5-7b-instruct (LM Studio) | Not run | - | - | HTTP 400 "fetch failed": likely VRAM exhaustion with several models loaded at once (Sponsor's diagnosis) |

**Reading:** small (4-7B) general models missed the real High defect and produced confident false findings. As an *independent* reviewer for high-risk work they would add false assurance, which runs against the Sponsor's accuracy-first constraint. This is one sample; a fair decision needs a short scorecard (below).

**Scorecard result (2 October 2026).**

Setup:
- Five cases, with the answer key fixed before running: four historical defects (C1 EBG-0155 High, C2 EBG-0138 High, C3 EBG-0137 High, C4 EBG-0156 Medium) and C5, the fixed EBG-0155 code, as a false-alarm control.
- Same neutral prompt, a one-line purpose per case, one model loaded at a time, 16k context.

| Model | Real defects caught | False / over-rated High-Medium findings | Clean control (C5) | Time per review |
|---|---|---|---|---|
| qwen3-coder-30b-a3b (Q4_K_M) | **1/4** (C2) | ~7, incl. invented SQL injection; repeatedly called the configured model "non-existent" (training cut-off) | 1 false High + 2-3 false Mediums; wrongly claimed the fixed code doesn't normalise | 3-5 min |
| gpt-oss-20b (MXFP4) | **2/4** (C1, C2 - **both under-rated as Medium**); missed C3 consent and C4 deadline-as-fault | 1 false High (claimed `isinstance(x, list \| tuple)` crashes; valid since Python 3.10); 1 over-rated High (thread-safety in a single-worker design) | **0 false High/Medium.** Found a **genuine, previously unknown defect** (below). Also independently raised the raw-`str(exc)` leak already tracked as EBG-0157 item (2) | 7-13 min (CPU-bound: 12 GB model on an 8 GB GPU; GPU ~4% utilised) |

**New genuine defect found by gpt-oss-20b, verified on current `main`:**
- `jarvis/interfaces/stdio_rpc.py:293`, `model = environ.get(spec["model_env_var"]) or spec["default_model"]`.
- A whitespace-only `OPENAI_MODEL`/`GEMINI_MODEL` (e.g. `"   "`) is truthy, so it is used as the model name instead of the default. Verified: the expression yields `'   '`.
- Low/Medium. Folded into **WP3** (the new Anthropic adapter must not inherit the pattern). To be registered as a new EBG in WP1.

**Verdict:**
- **Neither model is fit to act as an *independent* reviewer**, even for low-risk WPs. The best caught half the real defects, under-rated both of the Highs it found, and still produced a false High.
- **gpt-oss-20b earns a role as a free, local, advisory pre-screen:**
  - strong on false-alarm discipline (clean control: nothing false);
  - found a real defect our reviews missed;
  - zero cost and zero data egress.
- **Its findings are never counted as independent review**, and each is verified by the Engineering Implementer before being acted on.
- **qwen3-coder is not recommended** - its false-alarm rate would cost more review time than it saves.

**D29 - DECIDED 2 October 2026 (approved as recommended):**
1. Add **gpt-oss-20b as an optional pre-screen** in the bridge (tooling in WP1, alongside the Gemini CLI reviewer). Run it before Copilot on code WPs when time allows; review is not time-critical.
2. Independent review stays **Copilot + Gemini CLI (D19)**.
3. qwen3-coder can be deleted (frees 18.6 GB on E:).
4. Optional speed tuning (LM Studio's MoE expert-offload setting; closing GPU-heavy apps) - test, don't assume.

**Original proposed next step (now executed):**
1. Evaluate one or two **larger, code-specialised models** sized to this PC (8 GB VRAM + 32 GB RAM). Mixture-of-experts models suit it because only a fraction of their weights is active per token. Candidates to check for current availability and licence: **Qwen3-Coder-30B-A3B-Instruct (Q4)** and **gpt-oss-20b**, a different model family, for independence.
2. Load **one model at a time**.
3. Score each against **3-5 historical defects** with known answers (EBG-0155, EBG-0156, EBG-0137, plus one known-clean diff to measure false positives).

**Proposed role, set by the result:**
- **If it fails the scorecard:** use it only as a **pre-screen** before Copilot (cheap checklist-style first pass, saving Copilot runs), never counted as independent review.
- **If it passes:** use it as the **quota-exhaustion fallback for low-risk and docs-only WPs**.
- **Either way, high-risk WPs keep Copilot plus Gemini CLI (D19).**

Benefit regardless of outcome: free, unlimited, and fully local - nothing leaves the machine (GDPR).

---

## 6. Bottleneck Reductions

R1 (Tue-Fri), R2 (second reviewer, high-risk), R5/R12 (approval rules A1-A7), R6 (milestone sessions) and R9 (pipelined design) are **decided**. R3, R4, R7, R8, R10 and R11 are delivered in WP1. Unchanged otherwise from v0.6.

---

## 7. Work Package Plan (9 WPs)

Template per WP: EIP with evidence pack → Copilot design review (+ Gemini CLI on **high-risk** WPs: WP2, WP3, WP5, WP6) → **your design approval** (chat) → implement → `submit-response` → CI on Linux/Windows/macOS → script pre-check + post-commit review → **your `~/approve`**. Docs-only WPs need one approval (A5).

**Dependencies:**
- WP3 → WP2.
- WP4 → WP2 (its design is drafted during WP3, per D22).
- WP5 → WP3 + WP4.
- WP6 → WP5.
- WP7 → WP5.
- WP8's guide → WP3-WP7.
- WP9 → all.

| WP | Title | Backlog folded in / key scope | Effort | Runs |
|---|---|---|---|---|
| **WP1** | Release Gate, Governance, Streamlining | 0130, 0134, 0066, 0008, 0052, 0016, 0029, 0067, 0053, 0118, 0015/0059. PBK-0001/UAM-0001/product-architecture amendments (D2, D9); A1-A7; R3/R4/R7/R8/R10/R11 tooling; **Gemini CLI reviewer set up (your sign-in)**; provider-terms record | 3.75-4.75 d | 6-8 |
| **WP2** | Platform Foundation: Hardening, Freeze, macOS | 0158, 0149, 0157 (1-5, 7, 8), 0054; arm64 sidecar; Unix process-tree; `macos` CI; WebKit; `.dmg`; plist; GIA | 4.75-6.25 d | 8-10 |
| **WP3** | **Provider Strategy: Ollama-First + Claude Escalation** (new) | **0090** (closed with §5.2); **0157 (6)** (deadline-capped timeout in adapters, closes 0157); **0110** (backend half: per-profile memory-to-cloud control). New `sentinel/anthropic_provider.py`, matching the existing adapters' retry/circuit/deadline semantics and system-prompt structure. Ollama as the default route, with detection, guided install, in-app model pull and a hardware-based model recommendation. Escalation routing with a visible "answered by Claude" indicator. OpenAI and Gemini unregistered. Spend cap honoured (D26) | 4-5 d | 8-10 |
| **WP4** | Guardian Experience Redesign | 0150; redesign and Orb EBGs; §4.5 Orb criteria; role-aware UI; AI disclosure element | 6-7.5 d | 8-10 |
| **WP5** | Setup, Settings, Privacy and Data Rights | **0110** (UI half, closes it); `keyring` for the Claude key; STD-0006; first-run (Ollama-first); profile erasure, per-profile export, retention limits, privacy notice | 4.5-5.5 d | 8-10 |
| **WP6** | Household Safety: PIN, Child Role, Moderation, Consent | GAM-0001 §8.2 implementation; local moderation model; child-safety prompt layer; consent records; Child disclosure; D23 safety events | 4.25-5.25 d | 8-10 |
| **WP7** | Voice Provisioning (Windows + macOS) | New EBG | 2-3 d | 4-6 |
| **WP8** | Smoke Gates and Documentation | 0133, 0151, 0040, 0011+0061, 0146; user guide; parents' guide; **public "Children and privacy" page** (Anthropic requirement); data map | 4.5-5 d | 5-6 |
| **WP9** | Release Candidate and Go-Live (`v1.0.0`) | 0046; RC on Windows Sandbox, the household PC and her Mac; soak; publish on your instruction | 2-3 d + soak | 3-4 |

**Total:** about 36-45 days before reductions; **about 30-38 after.**

---

## 8. Backlog Allocation - All 29 Open Items

- **WP1:** 0008, 0015, 0016, 0029, 0052, 0053, 0059, 0066, 0067, 0118, 0130, 0134.
- **WP2:** 0054, 0149, 0157 (1-5, 7, 8), 0158.
- **WP3:** 0090, 0157 (6), 0110 (backend).
- **WP4:** 0150.
- **WP5:** 0110 (closes).
- **WP8:** 0011, 0040, 0061, 0133, 0151, 0146 (conditional).
- **WP9:** 0046.
- **Post-launch:** 0022, 0111, 0128, 0159, 0160.

**Added 4 October 2026 (outside a session):** EBG-0159 (Echo devices as a remote voice front-end via a private Alexa skill and Cloudflare Tunnel) and EBG-0160 (JARVIS room voice satellites, local "Hey Jarvis" wake word) were registered after this allocation was made and placed post-launch by Programme Sponsor decision. They are outside MLP 0.1 and are not folded into WP7. WP1 should recount the open items (now 31).

**25 of 29 closed by go-live.**

---

## 9. What I Still Need From You

**Nothing outstanding.** All decisions D1-D28 and the hardware details were provided on 2 October 2026 (§1).

**Sponsor actions:**
1. Anthropic API key ready and **£30/month spend limit set** in the Anthropic Console - **done** (Sponsor-reported, 2 October 2026). WP3 still verifies the limit's behaviour before relying on it, and JARVIS enforces its own cap regardless.
2. One-time **Google sign-in for Gemini CLI** - **during WP1** (D19), about 5 minutes.
3. **Mac visits booked** for the weeks of 20 October and 8 December - **done** (Sponsor-reported, 2 October 2026).

---

## 10. Timings (Tuesday-Friday, from Tuesday 6 October; milestone sessions)

| Week | Dates | Work | Notes |
|---|---|---|---|
| 1 | 6-9 Oct | WP1 | Your Google sign-in for the second reviewer; A1-A7 in force |
| 2 | 13-16 Oct | WP2; WP3 design drafted | |
| 3 | 20-23 Oct | WP2 complete; WP3; WP4 design/prototype drafted | **Mac visit 1**; **Session A** closes (WP1-WP2) |
| 4 | 27-30 Oct | WP3 complete; **your WP4 design approval** | Copilot quota checkpoint |
| 5 | 3-6 Nov | WP4 build | Quota reset 1 Nov |
| 6 | 10-13 Nov | WP4 complete | **Session B** closes (WP3-WP4) |
| 7 | 17-20 Nov | WP5 | |
| 8 | 24-27 Nov | WP5 complete; WP6 | |
| 9 | 1-4 Dec | WP6 complete; WP7 | Quota reset 1 Dec; **Session C** closes (WP5-WP7) |
| 10 | 8-11 Dec | WP8; WP9 RC; soak starts | **Mac visit 2** |
| 11 | 15-18 Dec | Soak ends; go/no-go; **publish** | **Session D** closes (WP8-WP9) |

**Target:** Friday 11 December, only if the soak can start a week earlier with no slips. **Planning date: Friday 18 December. Risk-adjusted: January 2027.**

The milestone sessions are regrouped from v0.6: A = WP1-2, B = WP3-4, C = WP5-7, D = WP8-9.

**Critical path:** WP2 → WP3 (Ollama/Claude) → WP4 (your design approval, week 4) → WP5 → WP6 → WP9 (Mac visit 2).

**Top risks:**
1. Local model too slow on the household PC (HW-1 answered early mitigates).
2. Copilot quota.
3. Design needs a third round.
4. Mac process-tree or voice issues.
5. Christmas.

---

## 11. After Go-Live

Post-launch order (to be set in JRM-0001 at WP9):
1. EBG-0128 Action faculty (+0111).
2. Cross-device sync.
3. Credentialed authentication beyond the PIN.
4. EBG-0022.
4a. Voice reach beyond the desktop: EBG-0160 (room satellites, preferred), with EBG-0159 (Alexa skill bridge) as an optional low-cost trial. Both depend on the Child-role enforcement from WP6 and on EBG-0128.
5. Session/Shared-Family memory.
6. Optional Linux build.
7. Re-assess other escalation providers whose terms permit family/minor use.

The Family AI OS (MLP 0.2-0.8) is an order of magnitude of 15-25 further sessions.

---

## 12. PBK-0001 Health Review Sections

**Backlog Validation:**
- 29 rows reviewed in full; 24 valid.
- EBG-0053 complete but unmarked; EBG-0118 superseded; EBG-0015/0059 recommended superseded; EBG-0110 has stale text; no duplicates.
- New candidates N1-N12 as v0.6, plus **N13 Provider Strategy (Ollama-first, Claude API escalation, OpenAI/Gemini unregistered)** and **N14 local moderation + consent records**.
- EBR-0001 update in WP1. Not modified by this review.

**JARVIS Development Readiness:** AIEMS sufficiently mature for full JARVIS Engineering. The constraint is throughput, not maturity.

**Handover:** Session A opens **Tuesday 6 October** with WP1 (done: [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]]). Its first steps:
1. WP0A synchronisation and a Copilot quota probe.
2. Register this report as a Working Report (`WR-ESR####-001`) and route it through the bridge for the Engineering Reviewer's review (Working Report Lifecycle step 2). As a docs-only commit, it takes a single `~/approve` (A5).
3. WP1's EIP.

All prerequisite decisions are taken.


---

## Appendix A. Content Carried Forward from Earlier Drafts

Sections 4.2, 4.3, 4.4 and 6 above say "as v0.6". Earlier drafts were never committed, so the carried-forward content is reproduced here so the report can be reviewed on its own. **Work Package numbers below are the current (v0.7+) numbers**: v0.6's WP3 Redesign is now WP4, WP4 Setup/Privacy is WP5, WP5 Household Safety is WP6, WP6 Voice is WP7, WP7 Docs is WP8, WP8 RC is WP9. Rows superseded by D25-D27 (moderation is now local; the provider-terms check was done on 2 October) are marked.

### A.1 UI against UAM-0001 (v0.4)

| Area | Finding |
|---|---|
| Layout | Long scrolling page; composer below the fold at 1280x820; three repeated status surfaces |
| Orb | Bound to repository data, so it fails on installs (EBG-0148). **Decoupled by direction (D11).** |
| Capability awareness | Stale static labels (Agents "No execution") - a UAM-0001 §10 breach |
| Polish | Scaffolding text; 9 dead controls |
| Unified look | Fonts not bundled; **two rendering engines to match** (WebView2 = Chromium on Windows; WKWebView = Safari engine on macOS) |

### A.2 macOS - Apple M1 Pro, macOS Tahoe 26 (v0.5)

| Area | Work | Effort | WP |
|---|---|---|---|
| Sidecar | `aarch64-apple-darwin` only (D14), built on GitHub's Apple-Silicon runner; consider onedir mode for startup time | 0.75 d | WP2 |
| Process-tree termination | Real Unix implementation (own process group + group kill + backend orphan watchdog), so EBG-0154's guarantee holds on the Mac | 1-1.5 d | WP2 |
| CI / release | `macos` pytest and cargo jobs; Playwright WebKit project; `.dmg` + checksum in `release.yml` (macOS runners are free for public repositories) | 1 d | WP2 |
| Bundle config | `NSMicrophoneUsageDescription`; minimum macOS version | 0.25 d | WP2 |
| Gatekeeper (D15) | Unsigned/ad-hoc: a one-time "Open Anyway" in System Settings > Privacy & Security. Notarisation needs the **paid** Apple Developer Program | 0.25 d (docs) | WP8 |
| Credentials | `keyring` to the macOS Keychain | - | WP5 |
| Voice | Verify `kokoro-onnx`/espeak and `faster-whisper`/CTranslate2 in the arm64 sidecar; verify `audio/mp4` from WKWebView | 0.5-1 d | WP7 |
| GIA | macOS process names, or an honest "not applicable" | 0.25 d | WP2 |
| Real-device acceptance | Mac visit 1 (week of 20 October: process-tree live check, model measurement) and Mac visit 2 (week of 8 December: RC + soak) | 0.5-1 d | WP2, WP9 |

JARVIS on the Mac has its own profiles and memory, with **no sync** to the household PC (DRA-0001 sync is future scope). Data moves between machines by backup/restore only.

### A.3 Household safety and GDPR-aligned privacy (v0.6, renumbered)

GDPR principles are the design standard for all household data (D23). UK GDPR Art. 2(2)(c) technically exempts purely household processing, but the standard is right regardless: cloud providers are controllers/processors, and Version 1.0 is a public release other households will rely on. The ICO Age Appropriate Design Code is a reference for the Child profile's defaults, not a claim that it legally applies to a locally-run app.

| Requirement | Today | Delivered in |
|---|---|---|
| Enforceable roles | Anyone can switch to Administrator | **WP6** - Administrator PIN (`hashlib.scrypt`, rate-limited) gating Settings, adult profiles, role changes, backup/restore |
| Child conversation boundary | None (GAM-0001 §8.2 principle only) | **WP6** - local moderation model on Child input and output (§5.3; supersedes v0.6's provider-side moderation); child-safety prompt layer |
| Data minimisation in logs | Content already excluded from audit/logs (ESR-0059) | Kept. **WP6** safety events = category + time only (D23) |
| Right to erasure | Per-item memory revocation only | **WP5** - "delete this profile and all its data", Administrator-confirmed |
| Access / portability | Whole-store backup, Administrator-only | **WP5** - per-profile export in a readable format; a Child's export is run by an Administrator |
| Retention limits | Audit log rotation by size | **WP5** - time-based retention for audit and safety logs (proposed 90 days, configurable) |
| Transparency | None in-app | **WP5** privacy notice at provider/key setup; **WP6** plain-language explanation for Child profiles |
| Cloud sharing of retained memory | Always shared when a cloud provider is used (EBG-0110) | **WP3** backend control; **WP5** per-profile UI; **WP6** default **off** for Child |
| Third-party processing of her data | Assessed 2 October 2026 (§3, §5) | Child restricted to local Ollama and the Anthropic API with recorded consent (D25 option A); Gemini and OpenAI unregistered (D25, D27) |
| Record of what goes where | None | **WP8** - "what data JARVIS holds and where it goes" in the user guide |

### A.4 Bottleneck reductions R1-R12 (v0.4 detail, v0.6 status)

| # | Reduction | Oversight / accuracy effect | Status |
|---|---|---|---|
| R1 | Fixed session calendar | None | **Decided (D18): Tuesday-Friday** |
| R2 | Second, free, independent reviewer (Gemini CLI, personal sign-in) | **Increases** oversight: removes the single point of failure | **Decided (D19): high-risk WPs and Copilot quota exhaustion**; set up in WP1 |
| R3 | Pre-submission evidence pack for every design review: affected-API facts checked against source, platform coverage (Windows *and* macOS), CI jobs that will run it, test list, new dependencies | **Increases** accuracy (built from ESR-0060 WP2's misses) | WP1, with EBG-0008 |
| R4 | Single source of truth for "current baseline" in PST-0001; other artefacts point to it; the validator flags hard-coded current-baseline claims; README's per-ESR rows replaced by a pointer | **Increases** accuracy (removes a known staleness defect class) | WP1 |
| R5 | Fold record-only commits (CI result, post-commit verdict, session-open record) into the next gated commit | None - same evidence, committed under an approved gate | **Decided (D20 = A3)** |
| R6 | One session per milestone (A = WP1-2, B = WP3-4, C = WP5-7, D = WP8-9), each with WP0, session-wide review and a baseline decision | Per-commit reviews unchanged | **Decided (D21)** |
| R7 | Script REG-0001 sync from each artefact's Document Control, verified by the validator | **Increases** accuracy | WP1 |
| R8 | Deterministic post-commit pre-check: a script proves the committed tree matches the reviewed tree, re-runs the suites and checks commit-message claims; the Copilot post-commit review **still runs**, given the script's output. Fix the bridge's reviewer tool permissions so validations can run | **Increases** accuracy | WP1 |
| R9 | Pipelined design drafting: while WP *n* awaits review/approval, draft WP *n+1*'s EIP and design; no code, no commit | None for code | **Decided (D22)** |
| R10 | Triage the 333 validator warnings: fix, downgrade with reason, or suppress with a justification record | **Increases** accuracy | WP1 |
| R11 | Tabular ESR WP entries (commit, CI run, review verdicts, decisions, deviations); detail stays in the EIP and bridge transcript | None - same facts, less prose | WP1 |
| R12 | Approval economy, rules A1-A7 (A.5) | None - every gate kept | **Decided (D24)** |

**Not adopted, because each reduces oversight:** dropping post-commit review; self-verification as a normal path; one approval covering both design and built code for code WPs; letting the reviewer write to the repository.

### A.5 Approval rules A1-A7 (D24, approved 2 October 2026)

| Rule | Effect |
|---|---|
| **A1. One act per decision.** When a commit is needed, the approval is requested once, via the Sponsor Approval Service. No parallel chat "Approved" is asked for. Chat approval is used only for decisions that produce no commit. | Removes duplicate approvals |
| **A2. The Sponsor's instruction is the approval.** If the Sponsor instructs an action that needs a commit (e.g. closure), it is given as `~/approve` with the instruction in the note. The Engineering Implementer never asks the Sponsor to confirm what they just instructed. Closure convention: `~/approve CLOSE "establish"` (or `"retain"`), then "close it". | Closure = one act |
| **A3. No approval for record-keeping alone.** Session-open records, review results, CI results and post-commit verdicts go into the bridge transcript immediately (primary evidence) and are committed with the next approved commit. | Same evidence, committed under an approved gate |
| **A4. Front-load known asks into the design approval.** New dependencies, crate/OS features and CI changes are listed in the EIP evidence pack (R3); a mid-WP ask is only for genuine surprises, which are still flagged. | Fewer mid-WP asks |
| **A5. Documentation-only WPs: one approval.** When the EIP contains the exact text to be committed, approving it via the service authorises that exact commit. | Docs WPs: one act instead of two |
| **A6. Code WPs keep two genuine gates:** design ("build this") and result ("commit what was built, after independent review"). | Kept deliberately |
| **A7. The approved plan authorises the sequence.** Opening a session to run the next WP in the approved plan needs no separate objective approval; each WP's design approval is still required. | Deviations from the plan still need the Sponsor |

Kept, not reduced: the ADR-0022 per-commit service gate (fail-closed, cannot be self-approved), independent review, and Sponsor-only baseline and go/no-go decisions. `~/approve` captures the repository state at the moment it is run, so nothing is committed between asking for an approval and receiving it.

---

## 13. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.11 | 6 October 2026 | Claude Engineering Implementer | Registered as WR-ESR0061-001 at ESR-0061 WP0B and routed to the Engineering Reviewer (Working Report Lifecycle step 2). Content unchanged apart from Document Control, the handover pointer, removal of an empty table header in §9, and a new Appendix A reproducing the earlier-draft content that §4.2-4.4 and §6 refer to as "as v0.6" (never committed, so otherwise unreviewable), renumbered to the current WPs. |
| 0.10 | 4 October 2026 | Claude Engineering Implementer | Outside a session: EBG-0159 and EBG-0160 (Alexa skill bridge; JARVIS room voice satellites) registered in EBR-0001 1.217 and allocated post-launch by Programme Sponsor decision (§8, §11). Not folded into WP7: outside MLP 0.1, with Child-role and D23 implications. |
| 0.9 | 2 October 2026 | Claude Engineering Implementer | §5A local-reviewer evaluation completed (5-case scorecard: gpt-oss-20b 2/4 with a clean control and one genuine new defect at stdio_rpc.py:293, folded into WP3; qwen3-coder 1/4 with ~7 false findings). D29 approved: gpt-oss-20b as an advisory pre-screen only, set up in WP1. |
| 0.8 | 2 October 2026 | Claude Engineering Implementer | Final decisions recorded: D26 (£30/month Claude cap - an explicit exception to the no-budget rule), D27 (Gemini API unregistered), D28 (suggested-then-confirmed escalation), D4-D8/D13/D15 confirmed as recommended. Hardware assessed (§5.4): PC with an RTX 4060 8 GB is strong for GPU-resident 7-8B Q4 models (keep models on SSD); M1 Pro 16 GB is workable but tight (measure on Mac visit 1, smaller-model fallback). No open decisions; ready for Engineering Reviewer review at Session A. |
| 0.7 | 2 October 2026 | Claude Engineering Implementer | Recorded D3, D19 (high-risk only), D21, D24 and D25 (UK; OpenAI removed; Ollama-first with escalation; APIs; consent; option A). Verified provider terms against live pages: Claude consumer terms (18+, no automated access except API key, no account sharing) rule out subscription/VS Code backends; Anthropic API permits minors with safeguards, mapped to WP6/WP8; Gemini API bars apps likely used by under-18s → D27. New WP3 Provider Strategy; 9 WPs; 30-38 d; target 11 Dec, planning 18 Dec. D26-D28 and hardware questions added. |
| 0.6 | 2 October 2026 | Claude Engineering Implementer | D1/D2/D3/D18/D23 recorded; §8 Sponsor asks; GDPR data rights. |
| 0.5 | 2 October 2026 | Claude Engineering Implementer | Household safety WP; approval-gate analysis. |
| 0.4 | 2 October 2026 | Claude Engineering Implementer | macOS; bottleneck analysis. |
| 0.3 | 2 October 2026 | Claude Engineering Implementer | Sponsor direction; backlog allocation. |
| 0.2 | 2 October 2026 | Claude Engineering Implementer | UI redesign. |
| 0.1 | 2 October 2026 | Claude Engineering Implementer | Initial draft. |
