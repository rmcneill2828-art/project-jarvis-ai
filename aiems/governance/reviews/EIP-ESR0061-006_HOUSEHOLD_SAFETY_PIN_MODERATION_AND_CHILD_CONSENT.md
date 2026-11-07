# EIP-ESR0061-006 - Household Safety: Administrator PIN, Child Moderation and Consent

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-006 |
| Title | Engineering Implementation Package: WP6 Household Safety, Administrator PIN, Child Moderation and Consent |
| Version | 0.8 |
| Status | Approved design - drafted 15 October 2026 at the Programme Sponsor's request ("please draft"); design review **Fail** (two High, four Medium, two Low, two Info), all addressed in v0.2, re-check Pass; **design approved as recommended 7 November 2026** (Section 10B); WP6a built and independently reviewed (Section 10C: Copilot Conditional Pass with its Medium fixed, Antigravity Pass); awaiting the Programme Sponsor's approval of the built result |
| Session | ESR-0061 (the plan puts WP6 in Session C; started under this session as WP3 to WP5 were) |
| Work Package | WP6 |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 5.3 (what Anthropic requires for minors), Section 5.4 (hardware), Section 7 (WP6) and Appendix A.3 (privacy requirements) |
| Architecture | [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 (the Household Role Model) and Section 8.2 (the Child-Safe Assistance Boundary) |
| Decisions it rests on | D23 (safety events are category and time, never content), D25 (Child restricted to compliant providers, parental consent), D26 (spend cap), D27 (Gemini unregistered), S6 (Child escalation denied until WP6), W1-W10 (WP4) |
| Backlog | No open item is allocated here by the plan beyond "GAM-0001 8.2 implementation"; EBG-0074 (`SimpleApprovalPolicy` is the core default) is adjacent and **not** closed by this package |
| Risk class | **High-risk** (plan Section 7: WP2, WP3, WP5, WP6): it governs what a child can say and be told, and what leaves the house on a child's behalf. Antigravity reviews the design and the built result; Copilot's quota is out until 1 November 2026 |

---

# 2. Purpose

Make the household roles real. Today a role is something a person picks: anyone can switch to the Administrator profile, create an Administrator, change every setting and ask Claude. And a Child profile's conversation has no safety layer at all: the local model's own tuning is the only filter. WP6 makes the roles enforceable with an Administrator PIN, puts a local moderation model on a Child's input and output, and delivers the consent records that decision D25 requires before a Child may reach Claude.

It builds directly on WP5: the Settings view, the first-run flow and the role-gated methods already exist and this package turns their "role-gated, not authenticated" into "authenticated".

---

# 3. Decomposition

| Sub-WP | Content | Effort |
|---|---|---|
| **WP6a** | The Administrator PIN: storage, rate limiting, the **elevation rule** (switching to a more privileged profile needs the PIN), PIN set at first run and changeable in Settings, profile creation made Administrator-only | 1.5-1.75 d |
| **WP6b** | Moderation: the classifier service on Ollama, Child input and output checked, fixed replies, fail closed, the child-safety prompt layer, safety events (category and time) | 1.5-2 d |
| **WP6c** | Child consent and Claude for a Child: consent and acknowledgement records, the gate, the moderated Claude reply, revocation | 1-1.25 d |
| **WP6d** | The Child disclosure and first-use explanation, the Administrator's Safety and Children section, final measurements on both machines, documentation and backlog updates | 0.5-0.75 d |

Total 4.5-5.75 days against the plan's 4.25-5.25: the upper end is a little over, because the PIN's rate limiting and the elevation rule need their own tests. Each sub-WP is a gated commit (rule A6). WP6a goes first because WP6c's consent is only meaningful once roles are enforceable.

---

# 4. Repository Context Investigated

| Fact | Where | Why it matters |
|---|---|---|
| `profile.select` and `profile.create` have **no role check at all**: any caller can select any profile and create a profile of any role, an Administrator included | `jarvis/interfaces/stdio_rpc.py` `_profile_select`, `_profile_create`; `jarvis/identity/service.py` | The whole role model can be bypassed in two calls; this is the gap the PIN closes |
| Every Administrator-only method (Claude key, settings, erase, memory backup and restore, note sharing) checks the **active profile's role** server-side | `stdio_rpc.py` `_require_role` use | Once switching up needs the PIN, all of these become authenticated with no change of their own |
| The active profile is held by the **server** (`active_profile` table), never taken from a request | `jarvis/identity/store.py` | The elevation rule can be enforced in one place, `profile.select` |
| Child escalation is **denied** by a role gate (`ESCALATION_ROLES` is Administrator and Adult) and by Sentinel's cloud rule; the Child's offer is never made | `jarvis/interfaces/escalation.py`, `sentinel/policy.py` line 92 | WP6c replaces a hard no with "no, unless a recorded consent exists" |
| `sentinel/policy.py`'s cloud rule reads `request.metadata["role"]` and is the second of two role checks | `sentinel/policy.py` line 153 | The consent gate must be added to the same two places |
| The conversation provider takes the approved **persona** as the system prompt, "verbatim" (AAM-0001 v0.4); history and notes travel separately | `jarvis/guardian/cognitive_core.py`, `GuardianRuntime.converse` | A child-safety layer is a **new system-prompt text**, which touches an approved persona: see Section 7 |
| `GuardianRuntime.converse` receives the profile id and household visibility but **not the role**; the RPC layer knows the role | `jarvis/guardian/runtime.py`, `stdio_rpc.py` `_guardian_converse` | Moderation needs the role passed down, as `escalate` already does |
| Ollama is reached with `urllib` against `/api/generate`; the only options sent are `num_ctx` and `num_predict`; per-request `num_gpu` is supported by Ollama but unused | `sentinel/ollama_provider.py` | The classifier can be told to run on the processor with one option |
| **Measured (WP3c, 8 October 2026, household PC, RTX 4060 8 GB):** `llama-guard3:1b` loaded beside the chat model: the 4B (4.3 GB) and the 2B (3.5 GB) **stayed resident**; the **9B did not** (the classifier made Ollama unload it, even at a 2048 context). The recommendation for this card is the 4B | EIP-ESR0061-003 Section 26 | The conflict exists only if an Administrator chooses the 9B; it is the reason for decision M1 |
| **Not measured:** the classifier's latency on the processor, on either machine; anything on the Mac | - | WP6d takes the figures; the targets in Section 5 (M1) are proposed, not known to be met |
| Audit events hold type, outcome, summary and role/counts; no profile id | `sentinel/audit.py`, `escalation.py` | Safety events that name a child must **not** go in the audit log (erasure and retention are designed around it holding no profile id): they get their own table, M5 |
| Profile erasure (WP5c) deletes the profile row, its notes, pending proposals, open offers and conversation; it knows nothing of consent or safety records | `stdio_rpc.py` `_profile_erase` | Both new tables must be erased with the profile |

---

# 5. Decisions Needed From the Programme Sponsor

Each has a recommendation. If the Programme Sponsor approves the design "as recommended", all are taken as recommended. Items marked **(wording)** produce text a child will read and need the Programme Sponsor's own approval of that text before the build is committed.

| # | Decision | Recommendation | Alternative |
|---|---|---|---|
| **P1** | **The PIN's shape.** A numeric PIN of **6 to 12 digits**, stored only as an `hashlib.scrypt` hash with a random salt in the identity database; compared in constant time; never logged, returned or placed in an error. **Rate limited**: after 5 wrong tries in a row the PIN is refused for 30 seconds, doubling each further batch up to **10 minutes**; the count and the lock time are persisted so a restart does not reset them. **A child can therefore delay the Administrator by guessing; the design accepts that, and makes it visible**: the next successful Administrator sign-in shows "N wrong PIN tries since you last signed in, the last at (time)" | **As stated.** 6 digits is 1,000,000 possibilities, and with the lock-out a guess cannot be brute-forced by a child in any useful time | 4 digits (10,000 possibilities: the lock-out still bounds it, but a determined child's tries add up over days); alphanumeric (stronger, harder on a keypad) |
| **P2** | **What the PIN guards: the elevation rule (revised after the design review's High).** The first draft used a straight privilege order, which let a Child step *down* to Guest with no PIN and so reach an unmoderated conversation. **Revised: a Child or Guest session is a locked session.** From a Child or Guest profile, switching to **any profile that is not a Child or Guest profile needs the PIN**; switching between Child and Guest profiles is free (both are moderated, M6). From an Adult profile, switching to an Administrator profile needs the PIN; to anything else is free. So a parent can step into a Child's profile freely, and a Child cannot reach an Adult or Administrator profile without the PIN, nor an unmoderated conversation by any route. `profile.create` becomes **Administrator-only** (and so, in practice, PIN-authenticated), except the very first profile. Every Administrator-only method is then authenticated because only an authenticated session can be the Administrator | **As stated.** One rule, enforced in one place (`profile.select`), covers every guarded method | A PIN prompt per sensitive action (more prompts, easier to forget one); idle auto-lock (see P4) |
| **P3** | **When there is no PIN yet** (an existing household upgrading, or an install that skipped it). Elevation stays open exactly as today, and the screen says plainly that **safety features are not enforced until a PIN is set**; the Child's moderation is on regardless; **a Child cannot be allowed to use Claude and a new profile cannot be created while no PIN is set** (a consent given with nothing protecting it is not consent). The first-run flow sets the PIN in its first step. **Residual risk, named (the review's High):** while no PIN exists, anyone can select the Administrator and **set the first PIN**, which would lock the real Administrator out until the command-line reset (P5). That is the same exposure the household has today (anyone can already become the Administrator and change everything), with one new harm: a lock-out. It is bounded by: the PIN's setting is **recorded and shown** to the next Administrator ("a PIN was set on (date) from the (name) profile"); the reset (P5) exists and is also shown; and the first-run flow, which is where a new household sets it, is not affected | **As stated** | Refuse all elevation until a PIN is set (breaks an existing household without warning) |
| **P4** | **Locking again.** The Administrator "locks" by switching to another profile, as today; **no idle timer in v1.0** | **As stated**: an idle lock is a behaviour change with real annoyance cost and no evidence yet that it is needed; named as a follow-on | Auto-lock after 15 minutes idle |
| **P5** | **A forgotten PIN.** No in-app reset (that would be a backdoor for the person the PIN exists to stop). A documented command-line reset, `python -m jarvis.tools.reset_admin_pin`, run on the computer by someone who can already open its files, removes the PIN, **logs that it did so and records a notice that the next Administrator sign-in shows** ("the PIN was reset on (date)"); the user guide (WP8) explains it. Nobody can reset it from the app. **Limit, stated (the review's Medium):** anyone who can run a command as the household's operating-system user can do this, including a child on a shared, unlocked account. The PIN is a control within the app, not a defence against a person with the operating system account; the privacy notice and the guide say so, and the notice on the next sign-in is the detection | **As stated.** The same trust as owning the computer | No recovery (a forgotten PIN means a reinstall and loss of every note) |
| **M1** | **Where the classifier runs, and the model that shares the card.** The classifier runs **on the processor** (`num_gpu: 0` on its requests), always, so it never competes with the chat model for the 8 GB card and can never evict a 9B. **Every request also sets `num_ctx` to 4096** (the review's Medium: left at the model's default, Llama Guard allocates a 131,072-token context and well over 5 GB). The cost is latency, with proposed targets: **median one check at most 2 seconds on the PC and 3 seconds on the Mac**, measured in WP6d. **The text is never truncated to meet a target** (the review's Medium: checking only the tail lets a message hide an unsafe start behind harmless text). A Child's message is limited to **1,000 characters** in the screen and in the backend, and a reply is checked whole (the model's reply is capped at roughly 4,000 characters); if a target is missed the Programme Sponsor decides between a slower check and a smaller chat answer limit | **As stated.** The conflict is then removed for every chat model choice, not only the recommended one | Classifier on the card when it fits (a measurement and a branch to maintain); a smaller chat model for Child profiles only (inconsistent answers); a bigger card |
| **M2** | **The classifier model.** `llama-guard3:1b` (Meta's Llama Guard 3, 1 billion parameters, an MLCommons hazard classifier), already measured as the stand-in. **Limit, stated honestly:** it classifies hazards (violence, self-harm, sexual content and so on); it is not tuned to *age-appropriateness*, so mild profanity or frightening-but-not-hazardous content can pass, which is what the child-safety prompt layer (S1) is for. Licence terms to be confirmed at build | **As stated** | `shieldgemma:2b` (a Google licence; larger); a bigger Llama Guard (does not fit beside any useful chat model) |
| **M3** | **Fail closed.** If the classifier is not installed, not running or errors, a **Child's** message gets a fixed "I can't check that is safe to answer right now, so please ask a grown-up" and **no answer is generated or shown**. Moderation applies to the **Child and Guest roles** (see M6); an Adult or Administrator conversation is unchanged | **As stated** | Fail open for a Child (a safety control that vanishes when it breaks is not one) |
| **M4** | **What a blocked turn looks like. (wording)** Fixed, non-generated text; **no category name is shown to the child**. Two texts: a gentle general one ("I can't help with that one. You could ask a grown-up.") and one for self-harm, which is not a refusal but points to a trusted adult and to Childline (UK, free, 0800 1111), **and says to tell a grown-up straight away or call 999 if someone is in danger** (the review's Low). Draft wording is in Section 6.4 | **As stated**, for the Programme Sponsor to edit | Generated refusals (unpredictable for a child; no) |
| **M5** | **Safety events.** A new table in the identity database: **category, direction (input or output), time and the profile id**. **Never content.** Shown to an Administrator as counts and times in Settings; pruned by the same retention days as the activity log; **deleted with the profile on erasure**. Not the audit log, so the audit log's "no profile id" property that erasure relies on stays true. D23 says "category and time": including the profile id is an addition, because a parent cannot act on "an event happened" | **As stated** | No profile id (a parent cannot tell which child); content (excluded by D23) |
| **M6** | **Guest is moderated like Child (the review's High).** A Guest can reach a child-visible conversation as easily as a Child profile can, and nothing proves a visitor is an adult. So a Guest conversation gets the same input and output checks and the same fixed replies. A Guest still cannot ask Claude (the role gate), has no household notes, and gets no consent path. The plan said "Child"; this widens it by one role, on the reviewer's finding | **As stated** | Leave Guest unmoderated and close the hole only by the locked-session rule (P2): sufficient for the switching route, but a visiting child on the Guest profile would be unprotected |
| **C1** | **Claude for a Child: build it in this package, off by default.** D25 option A allows the Anthropic API for a Child with recorded parental consent. It needs the consent records, an extra gate in the two role checks, moderation of the Claude reply, and revocation: about a day | **Build it** (it is decided), **default off**, and only once a PIN is set (P3) | Defer to after 1.0 and keep S6's hard no: lower risk, a smaller WP6, and the Child profile is local-only at launch. A reasonable choice if time is the constraint |
| **C2** | **The consent record.** Two records per Child: the **Administrator's consent** (who, when, scope "this profile may ask Claude, with its question and recent conversation, never its notes") and the **Child's own acknowledgement** in plain language (**wording**), recorded when they first use the feature. Both are revocable; revoking the Administrator's consent switches Claude off for that child at once. Memory sharing with Claude stays **off and cannot be turned on** for a Child (the backend already refuses it) | **As stated** | A single parental tick-box (the plan asked for both) |
| **S1** | **The child-safety prompt layer. (wording)** A short passage added to the system prompt **for a Child profile only** (be kind and simple, decline unsuitable subjects, suggest a trusted adult, never pretend to be a person, never ask for personal details). It touches the approved persona, so it needs the Programme Sponsor's approval of the exact text **and a versioned amendment to AAM-0001**, not a silent addition. Draft text is in Section 6.5 | **As stated** | No layer (the classifier alone does not catch age-inappropriateness: see M2) |
| **D1** | **The Child's explanation and disclosure. (wording)** On a Child profile's first use: a short plain-language page ("You are talking to JARVIS, which is an AI, not a person. It can make mistakes. It runs on this computer. JARVIS does not keep what you say once it is closed, except notes a grown-up has agreed to save. A grown-up can see that a safety check stopped something, and can see the notes saved for you.") shown once and acknowledged, and the existing permanent "you are talking to an AI" line stays. **Revised after the review's Low:** the first draft said a grown-up "cannot see what you said", which a shared family computer does not guarantee, so the wording now says only what is true of the code | **As stated** | Show every time (annoying); never (the plan requires it) |

---

# 6. Design

**6.1 The PIN (WP6a).** New `jarvis/identity/admin_pin.py` over the identity database (a new migration adds one table, `admin_pin`: salt, hash, parameters, `failed_count`, `locked_until`, `set_at`; at most one row). `hashlib.scrypt` with `n=2**14, r=8, p=1` and a 16-byte salt; compare with `hmac.compare_digest`. Failures are counted and the lock-out persisted. No method returns, logs or echoes a PIN; error messages are fixed ("That PIN is not right. Try again in N seconds."). Methods: `pin.status` (any caller: `{set, locked, lockedForSeconds}`), `pin.set` (first PIN: needs the Administrator role and no PIN set; at first run, the first profile), `pin.change` (needs the current PIN), `pin.verify` is not a public method: verification happens inside `profile.select`.

**6.2 The elevation rule (WP6a).** `profile.select` takes an optional `pin`. The PIN is required when the active profile is a Child or Guest and the target is not, or when the active profile is not an Administrator and the target is (the locked-session rule of P2); it is checked and the lock-out accounted; a wrong or missing one is refused with the lock-out accounted. No active profile (a fresh start with profiles but none selected) is treated as the lowest privilege, so choosing an Administrator at start needs the PIN; the first profile of a fresh install is created and selected with no PIN because none exists (P3). `profile.create` requires an active Administrator (or no profiles at all). Both rules live in `ProfileService` so every caller shares them. **A backend restart is not an elevation**: the stored active profile persists as today, which means a computer left on an Administrator profile stays one (P4).

**6.3 The screen for the PIN (WP6a).** A PIN prompt appears when switching up (the picker says why), a "Set an Administrator PIN" step in first run and a banner in Settings when none is set (P3), "Change PIN" in Settings, and lock-out wording that says how long to wait. The PIN field is a password input, cleared on submit, never stored in state beyond the prompt.

**6.4 Moderation (WP6b).** New `jarvis/interfaces/moderation.py`: `ModerationService.check(text, direction)` sends the text to Ollama's chat endpoint with the classifier model and `options: {"num_gpu": 0, "num_ctx": 4096}`, parses Llama Guard's `safe` or `unsafe` plus category codes, and returns an allow or a block with a **category label** (never the text). Applied by `GuardianRuntime` when the role is Child: the **input** before any model is called (an unsafe input never reaches a chat model or Claude); the **output** of whichever model answered, local or Claude, before it is shown or recorded in history. A blocked turn returns fixed text and records a safety event; **a blocked input or output is not added to the conversation history**. The classifier model is added to the local AI setup (checked, installable and removable like the chat model; the hardware recommendation notes the extra 1 GB). Draft fixed texts (for the Programme Sponsor to edit):

* General: "I can't help with that one. You could ask a grown-up."
* Self-harm: "That sounds like something to talk about with someone you trust, like a parent, a carer or a teacher. If you want to talk to someone right now, you can call Childline for free on 0800 1111. If you or someone else is in danger, tell a grown-up straight away or call 999."
* Moderation unavailable: "I can't check that it is safe to answer right now, so please ask a grown-up."

**6.5 The child-safety layer (WP6b).** Draft text, appended to the persona for a Child profile only and shown to the Programme Sponsor verbatim for approval: "You are talking with a child. Use short, kind, simple words. If a question is about something unsuitable for a child, or about hurting someone or themselves, say you can't help with that and suggest they ask a trusted grown-up. Never pretend to be a person. Never ask for their full name, address, school or phone number, and if they offer them, tell them to keep them private." Held in one named constant and tested; **the AAM-0001 amendment is part of the same commit** (Section 7).

**6.6 Consent and Claude for a Child (WP6c).** New tables `child_consents`: profile id, `consented_by` (the Administrator's profile id), `scope`, `recorded_at`, `acknowledged_at` (the child's own, set separately), `revoked_at`. Methods: `consent.record` (Administrator, PIN set, target is a Child), `consent.revoke` (Administrator), `consent.acknowledge` (the Child, for themselves, only once consent exists), `consent.status`. The Child's offer to ask Claude exists only when the consent is recorded, acknowledged and unrevoked **and** the classifier is available. The escalation role gate and Sentinel's cloud rule each gain the same check, so neither a changed UI nor a forged request can skip it. The spend cap and the one-time confirmation token are unchanged; **notes are never sent for a Child** (the existing refusal). A Claude reply is moderated before it is shown.

**6.7 The Administrator's view and the Child's disclosure (WP6d).** Settings gains **Children and safety**: per Child profile, whether Claude is allowed and when consent was recorded and acknowledged, with Record and Revoke; counts of safety events by category and day (no content); the classifier's state. A Child profile's first use shows the explanation page (D1), recorded as acknowledged; the existing permanent disclosure line stays.

**6.8 Measurements (WP6d).** On both machines, with the real classifier: the classifier's latency (median and worst of 20 checks on the processor), the chat model's answer time with the classifier resident, memory use, and a pass over a fixed list of 40 test sentences (20 unsafe, 20 safe, written for this) to **record how many it gets right, as a fact and not a promise**. The 40 sentences are kept out of the repository's public tree if the Programme Sponsor prefers.

---

# 7. Cross-Work-Package Flags

* **AAM-0001 (the persona).** S1 changes what the approved persona says to a child. It needs the Programme Sponsor's explicit approval of the text and a versioned amendment to AAM-0001, committed with WP6b. **Flagged for decision.**
* **Child-facing wording.** M4, C2, S1 and D1 are text a child will read. I have drafted it; the Programme Sponsor must approve or edit it. I am not a safe judge of what is right for a particular fifteen-year-old.
* **WP8.** The public "Children and privacy" page, the parents' guide and the PIN-reset instructions (P5) are WP8; this package supplies the facts.
* **The Mac.** `hashlib.scrypt` is in the standard library and platform-independent. The classifier's latency on the Mac processor is unmeasured and may be slower than the PC; that is why the target is stated as a target (Mac visit 1 or 2).
* **EBG-0074 stays open.** `SimpleApprovalPolicy` as the core default is a Sentinel matter, not closed by WP6.
* **What a PIN is not.** It stops a child switching up in the app. It does not stop someone with operating-system access opening the data files, or using a different computer. The privacy notice and the guide must say so, and WP6 does not claim more.
* **Not in scope, named so it is not assumed:** age verification, an idle lock (P4), moderation of Adult or Administrator conversations (a Guest is moderated, M6), any parental reporting by email or message, and any change to the Claude model choice.
* **Rail and tests.** The Settings view gains sections, not a new view; tests that count views do not change.

---

# 8. Evidence Pack (TPL-0001 Section 6)

* **New dependencies (rule A4):** none in Python or npm. `hashlib.scrypt` and `hmac` are the standard library. **A new model download** (`llama-guard3:1b`, about 1 GB) for Child profiles, from Ollama's registry, initiated by an Administrator.
* **CI changes:** none planned.
* **Tests (planned):** Python: PIN set, change, wrong PIN, lock-out growth and persistence across a restart, constant-time path, never in a log or reply; the elevation rule across every pair of roles; profile create gating; moderation with a fake classifier (safe, unsafe by category, malformed output, unavailable, timeout, fail closed), a blocked turn leaves no history and no content in any log, output moderation of a Claude reply, the safety events table (category, direction, time, profile id, retention, erasure); consent record, acknowledge and revoke, the double gate, notes never sent for a Child; the child-safety layer present for a Child and absent for others. Playwright: the PIN prompt on switching up, lock-out wording, first-run PIN step, Settings sections by role, the Child explanation page, blocked-turn display, a Child never sees the word Claude until consent and acknowledgement.
* **Live checks, by the Engineering Implementer on this PC:** the real classifier through the packaged sidecar on a fixed list of sentences; latency on the processor; the lock-out with real timing; a Child blocked on unsafe input and on an unsafe output.
* **Not checkable here:** the Mac (visit 1 or 2): classifier latency and memory with the chat model, the PIN in the WKWebView.

---

# 9. Commit Contents (expected, per sub-WP; finalised at build)

**WP6a:** `jarvis/identity/admin_pin.py` (new), `jarvis/identity/store.py`, `jarvis/identity/service.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tools/reset_admin_pin.py` (new), `src-tauri/src/lib.rs`, `src/` (the PIN prompt, first-run step, Settings section), tests. **WP6b:** `jarvis/interfaces/moderation.py` (new), `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/interfaces/ollama_setup.py` (the classifier model), the safety-events table, `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md` (the amendment), tests. **WP6c:** the consent tables and methods, `jarvis/interfaces/escalation.py`, `sentinel/policy.py`, `src/`, tests. **WP6d:** `src/` (Children and safety, the explanation page), `scripts/` measurement tooling, tests, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, documentation. Each with the record files (this EIP, ESR-0061, REG-0001), listed by name in the sub-WP's own Commit Contents section when it is built.

---

# 10. Questions for the Engineering Reviewer

1. **The elevation rule (P2).** Is there any path to a more privileged profile that does not go through `profile.select`'s PIN check: the stored active profile at start, `profile.create` followed by select, a profile whose role is changed, the first-profile exception (P3), or a race between two calls? Is the privilege order right for Guest relative to Child?
2. **The PIN's storage and limits (P1).** Are the scrypt parameters and the persisted lock-out sound? Can the lock-out counter be reset by a restart, by deleting the table through any RPC, or by switching profile? Can the rate limit be used to lock the Administrator out (a child spamming wrong PINs): is that acceptable, and what does the Administrator see?
3. **Fail closed (M3).** Is there any path by which a Child's message reaches a chat model or Claude without the input check, or a reply is shown without the output check (history replay, the escalation path, a cached reply, speech)? Is a blocked turn really absent from history and logs?
4. **The classifier (M1, M2).** Is forcing it to the processor with `num_gpu: 0` honoured by the Ollama version in use; is the parse of Llama Guard's output robust to extra text, a refusal, or a prompt-injection attempt in the child's own message (the text under test is attacker-controlled)? What happens with a very long message, or an empty one?
5. **Consent (C2).** Can a Child record or acknowledge their own consent, or revoke an Administrator's? Can a consent outlive the Administrator who gave it, or the erasure of the profile? Does revoking take effect for a request in flight?
6. **Safety events (M5).** Does any path put content, the classifier's raw output, or the message in the table, a log or an error? Are the events deleted on erasure and pruned by retention?
7. **Wording.** Read 6.4, 6.5 and the Section 5 texts as a parent. Is anything harmful, misleading or beyond what the build delivers (for example, an implication that the child is fully protected)?
8. **Anything rated Medium or higher.**

---

# 10A. Design Review Record (15 October 2026)

**Review** (Antigravity, Gemini 3.8 Flash High, `sender: reviewer`, submitted 15:15:49Z): **Fail**, two High and the rest below, all addressed in this version. The design is better for it; the first High is a real hole I had drawn myself.

| Rating | Finding | Disposition |
|---|---|---|
| High | Under the linear privilege order a Child can switch to Guest with no PIN and get an unmoderated conversation | **Fixed**: a Child or Guest session is locked (P2) and Guest is moderated like Child (M6) |
| High | With no PIN set, anyone can select the Administrator and set the first PIN, locking the real Administrator out | **Accepted with mitigation and named** (P3): it is the exposure the household already has, with a lock-out as the new harm; the PIN's setting and any reset are recorded and shown to the next Administrator. It cannot be removed without refusing elevation (which breaks an existing household), and the first-run flow is unaffected |
| Medium | `num_gpu 0` without `num_ctx` lets Llama Guard allocate a 131,072-token context | **Fixed** (M1): `num_ctx` 4096 on every request |
| Medium | The lock-out has no in-app recovery and lets a child delay the Administrator | **Accepted, capped at 10 minutes and made visible** (P1) |
| Medium | The command-line reset lets a minor on the same operating-system account clear the PIN | **Accepted, stated plainly and made detectable** (P5): the PIN is not a defence against operating-system access |
| Medium | Shortening the checked window to the last 1,500 characters lets unsafe text hide behind benign text | **Fixed** (M1): never truncate; a Child's message is capped at 1,000 characters and checked whole |
| Low | The Child disclosure overclaims that a grown-up cannot see what was said | **Fixed** (D1) |
| Low | The self-harm text omits emergency guidance for acute crises | **Fixed** (M4): tell a grown-up straight away or call 999 |
| Info | The prompt layer needs an AAM-0001 amendment, and the role must be passed into converse | Already in Sections 7 and 4 |
| Info | Deferring Claude for a Child to after 1.0 would de-risk 1.0 | **Left as the Programme Sponsor's choice** (C1): I still recommend building it, last in the order (WP6c) so it can be dropped without touching anything else; the reviewer's view is recorded here |

**Re-check of v0.2** (resume, 15 October 2026, 15:24:32Z): **Pass.** The locked session and the moderated Guest close the unmoderated route; the no-PIN and operating-system-access risks are honestly stated and bounded; `num_ctx` 4096 with no truncation is sound. One note, applied in v0.3: the Section 7 out-of-scope bullet still listed Guest as unmoderated. Same caveat as always: a smaller single reviewer, judging by reading.

---

# 10B. Programme Sponsor Design Approval (7 November 2026)

**Approved as recommended** (direct chat "WP6 Approved", rule A6 gate 1, after the session resumed following the PC rebuild). Under Section 5's rule, every decision is taken as recommended:

* P1-P5, M1-M6 and C2 as stated.
* **C1: Claude for a Child is built**, last in the order (WP6c), **off by default**, and only once a PIN is set. The reviewer's preference to defer it stays recorded in Section 10A.
* **Wording is not yet approved.** M4, C2, S1 and D1 carry text a child will read; the drafts in Sections 5, 6.4 and 6.5 are presented again for the Programme Sponsor's approval of the exact text before WP6b, WP6c and WP6d respectively are committed. S1's AAM-0001 amendment is part of WP6b.

**Changes of fact since the design, none of which changes a decision:**

* **The PC was rebuilt** (AMD Ryzen 5 5600, 32 GB; the same RTX 4060 8 GB). The WP3c finding that the 9B cannot sit beside the classifier on the card still holds (same card); the processor latency target in M1 (2 seconds) is measured in WP6d on the new processor.
* **The Mac is being replaced.** A new Mac, replacing the M1 Pro, arrives in about two weeks. M1's 3-second Mac target applies to the new Mac and is measured on it. ESR-0061 closes after WP6 without waiting for it (Programme Sponsor decision, 7 November 2026), so **the Mac measurements of Section 6.8 move to the next session as a named carried item**, and WP6d records the PC figures only.

---

# 10C. WP6a Build Record (7 November 2026)

**Built as designed** (Sections 5 P1-P5, 6.1-6.3). What the code does:

* **The PIN** (`jarvis/identity/admin_pin.py`, migration 3 in `jarvis/identity/store.py`): 6-12 ASCII digits (`[0-9]`, so other scripts' digits are refused); `hashlib.scrypt` n=2^14, r=8, p=1, 16-byte salt, 32-byte hash; `hmac.compare_digest`. Lock-out: the fifth wrong try in a row locks for 30 s, doubling per further batch of 5 to a 600 s cap; during a lock-out a PIN is refused **without being checked or counted**. The read-check-update runs in one `BEGIN IMMEDIATE` transaction. Refusals are plain `PermissionError` replies with fixed text.
* **The elevation rule** (`pin_required_to_switch` in `jarvis/identity/service.py`, the one place it lives): exactly P2, with no profile signed in treated as the lowest privilege and staying on the same profile not counted as a switch. `select_profile` enforces it; `profile.switchRequirements` lets the screen ask only when needed.
* **Profile creation**: the first profile can be created by anyone; every later one needs an Administrator signed in and a PIN set (P2, P3).
* **Notices** (P1, P3, P5): "PIN set (by profile name)", "PIN reset" and "N wrong tries, the last at" are handed to the next Administrator signing in, in the `profile.select` reply, once.
* **Reset** (P5): `python -m jarvis.tools.reset_admin_pin`, reading the backend's own database setting.
* **Screens**: the PIN prompt (a modal like the Claude dialog: focus in, Tab kept inside by hand, Escape cancels, focus returns), a lock-out countdown, the notices banner, an Administrator PIN section in Settings (warning and set form with no PIN; change form with one), and a first-run PIN step after the profile step that can be put off with the plain warning; the Ready summary has a PIN line.

**Decisions made while building, none of which changes an approved decision; each is named for the reviewer:**

1. **The first profile must be an Administrator.** The design said the first profile is created without a PIN; it did not say what role. If it could be a Child, no Administrator could ever be added (adding needs an Administrator). The first-run flow already creates an Administrator, so this changes nothing a person can do in the app.
2. **Adding a profile no longer switches into it.** Before, the screen created and then selected the new profile. Under the rule, an Administrator who adds a Child and is moved into it would need the PIN to come back. Only the household's first profile is now selected on creation.
3. **A fresh start with profiles but none signed in shows a chooser** instead of the create form, which the backend would now refuse. Choosing an Administrator or Adult asks for the PIN.
4. **The reset tool reads the backend's path settings** (`stdio_rpc`) rather than its own copy, found by a failing test: with a copy, the test sandbox pointed the backend at a temporary folder while the tool still pointed at the real home folder.
5. **Existing tests set up households the real way** through a shared helper, `jarvis/tests/household.py` (an Administrator, a PIN, then the member), because the old setup (any profile creating any profile) is now refused. No test's assertion was weakened; three tests were updated for facts that changed (schema version 3, the `pinNotices` field, profiles listed by id rather than position).

**Flag (scope, PBK-0001 Scope-Creep rule): there is no screen for adding a profile once one is signed in.** This predates WP6 (the only create form is the first-run one and the no-profile card), so today a household cannot add a Child profile from the app at all, which WP6's safety features presuppose. It is **not** built here. Proposed disposition: a small "Household profiles: add a profile" section in Settings (Administrator only, PIN set), about 0.25 day, either folded into WP6a before commit or done as WP6a-2. **The Programme Sponsor's decision.**

**The scope flag was decided: the add-profile screen is in WP6a** (Programme Sponsor, direct chat "yes in WP6a", 7 November 2026). Built: Settings gains **Add a profile** (Administrator only; the form appears only once a PIN is set, with a plain note before then; any role can be chosen, Child by default; the Administrator stays signed in). This also makes the PIN section's sentence "only an Administrator can add profiles" true on screen (Copilot Low). 4 new Playwright tests.

**Implementation review, round 1:**

* **Copilot** (the Engineering Reviewer, quota back from 1 November; `sender: reviewer`, 2026-11-07T09:28:57Z): **Conditional Pass, no High.** It confirmed the elevation rule for all 16 pairs and no-profile, only `select_profile` sets the active profile, the PIN storage and lock-out schedule, no leaks, and the five build decisions as reasonable. **Medium M1, fixed:** notices were delivered only in the `profile.select` reply, so an Administrator already signed in when the app starts never saw them, weakening P5's detection. Now a new Administrator-only method `pin.takeNotices` (Tauri `take_pin_notices`) is called at startup when the stored profile is an Administrator; 1 new Python and 2 new Playwright tests. **Low, accepted:** notices are deleted as they are handed over, so a reply lost in transit loses them; the reset tool reports to the console only; a person who can change the computer's clock can shorten a lock-out (inside the accepted operating-system-access limit). **Low, resolved** by the add-profile screen above. **Info:** select reads then sets the active profile without one transaction; no privilege-gaining sequence found. Copilot could not run pytest or ruff (its shell was refused) and relied on the recorded results.
* **Antigravity** (second reviewer, high-risk): the first run **recorded no verdict**. It stopped while waiting on a background pytest run, and `scripts/run_reviewer.py` reported Copilot's verdict as its own, because both runs started in the same second and shared an output file name. **A defect in `run_reviewer.py`, recorded as an observation, not fixed in WP6a**; reviewers are run one after the other until it is. Re-run on its own, including the M1 fix.
* **Antigravity re-run** (Gemini 3.8 Flash High, `sender: reviewer`, started 09:37Z): **Pass, no High or Medium.** It reviewed the tree including the M1 fix and the add-profile screen, ran `test_admin_pin.py`, ruff and the validator, and confirmed P1-P5, no bypass of the PIN check, no leaks, the five build decisions and the scope flag's resolution, and that no assertion was weakened. **Low L1** (notices deleted on retrieval) and **Low L2** (reset reported on the console only) are the two Lows already accepted from Copilot; **Info:** `pin.status` answers any caller so the screen can count a lock-out down (by design, 6.1).

**Both independent reviews are complete with no open High or Medium finding.** WP6a waits for the Programme Sponsor's approval of the built result (rule A6, gate 2).

**Evidence (final, 7 November 2026):**

* Python (Windows): **1337 passed, 4 skipped**; **Linux in Docker** (`python:3.12-slim`, the CI steps): ruff clean, version sync clean, **1341 passed**, validator 0 errors. Earlier figure while building: 1336 passed, 4 skipped (84 new in `test_admin_pin.py`, including the elevation rule for all 16 role pairs, a search showing a Child reaches only Child and Guest by free switches, the lock-out at every batch to the cap, persistence across a restart, and that the PIN appears in no reply, log or database byte). Ruff clean.
* Playwright (Chromium): **175 passed** at the end (168 while building, then 3 for the M1 fix and 4 for the add-profile screen), including 19 new WP6a tests in all and an axe check of the PIN prompt (with and without a refusal), the first-run PIN step and the Settings PIN section. `vite build` clean.
* Rust: `cargo test` 19 passed, clippy `-D warnings` and `cargo fmt --check` clean.
* **Live check on this PC** (the real backend process over stdio, a throwaway database): no profile can be added before a PIN; five wrong tries lock for 30 s and the right PIN is then refused; the lock-out survives a backend restart; after 31 s of real time the right PIN works and the notices report the PIN set and the 5 wrong tries; `python -m jarvis.tools.reset_admin_pin` removes the PIN and the next Administrator sign-in reports the reset; the PIN is in no reply, log or database byte.
* **Not run:** the packaged app window (not launched); WebKit (CI runs it, informational).

**Commit Contents (WP6a, expected):** `jarvis/identity/admin_pin.py` (new), `jarvis/identity/service.py`, `jarvis/identity/store.py`, `jarvis/interfaces/activity_tracker.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tools/__init__.py` (new), `jarvis/tools/reset_admin_pin.py` (new), `jarvis/tests/household.py` (new), `jarvis/tests/test_admin_pin.py` (new), `jarvis/tests/test_audit_retention.py`, `jarvis/tests/test_claude_key_rpc.py`, `jarvis/tests/test_escalation_rpc.py`, `jarvis/tests/test_household_roles.py`, `jarvis/tests/test_identity_service.py`, `jarvis/tests/test_memory_revocation.py`, `jarvis/tests/test_ollama_setup.py`, `jarvis/tests/test_profile_data_rights.py`, `jarvis/tests/test_profile_scoped_memory.py`, `jarvis/tests/test_schema_migrations.py`, `jarvis/tests/test_stdio_rpc.py`, `src-tauri/src/lib.rs`, `src/AdminPin.jsx` (new), `src/App.jsx`, `src/FirstRun.jsx`, `src/SettingsView.jsx`, `src/roles.js`, `tests/e2e/accessibility.spec.js`, `tests/e2e/app.spec.js`; and the records riding with it (rule A3): this EIP, `aiems/governance/reviews/EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS.md` (the WP5d post-commit record), `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

---

**WP6a approval and commit (7 November 2026):** approved by the Programme Sponsor through the Sponsor Approval Service (decision 2026-11-07T13:54:38Z on d5428a1); `submit-response` passed at 14:12:17Z; committed as **ef17f1d** (32 files, as listed above). Not pushed: pushing is the Programme Sponsor's.

**WP6a post-commit review** (Copilot, the real committed diff, 14:12Z): **Pass, no High or Medium.** The commit is exactly the Commit Contents list; the M1 fix is present; nothing slipped in (no debug code, secret or WP6b change, no weakened assertion). Low L1: a household upgraded from before WP6a whose profiles include no Administrator can never add one, because creation needs an Administrator signed in and the first-profile rule only covers an empty household. Low L2: the command-line reset deletes the PIN row, so a pending count of wrong tries is lost (the reset notice is still left). Both carried to WP6d for disposition.

# 10D. WP6b Build Record (7 November 2026, built while WP6a's approval is held)

**Context.** The Programme Sponsor went out for about four hours and asked for work to continue automatically, with every approval held until their return. WP6a had completed both independent reviews, so WP6b was built (design approved 7 November 2026, Section 10B) **in a separate git worktree** (`I:\tmp\wp6b-work`) carrying WP6a's uncommitted files byte for byte, so the WP6a tree the reviewers checked is untouched. Nothing was committed at that point; WP6b moved into the main tree after WP6a was committed (ef17f1d) and was itself committed as 5ef3637 (see the end of this section).

**Built as designed** (M1-M6, S1, 6.4-6.5):

* `jarvis/interfaces/moderation.py`: `ModerationService` over Ollama `/api/chat` with `llama-guard3:1b`, `num_gpu` 0, `num_ctx` 4096, temperature 0; a strict reader (only a first line exactly "safe" allows; "unsafe" blocks by category, self-harm first; anything else fails closed); the fixed replies (M4) and the child-safety layer (S1) as named constants (draft wording at build; **approved 7 November 2026**, see the decisions below).
* `GuardianRuntime.converse` (and `escalate`, ready for WP6c) takes the role: for Child or Guest the message is checked before any model is called and the reply before it is returned; a block returns the fixed reply, is not a model reply and never enters history; no classifier means fail closed. The layer is appended for a Child only.
* Safety events (M5): migration 4 adds `safety_events` (profile, category, input/output, time; never text) to the identity database; recorded by the RPC layer on a block, deleted with the profile on erasure, pruned by the audit retention days (the retention service gained a pruner hook).
* RPC: a Child's or Guest's message is limited to 1,000 characters (M1); a blocked turn carries `blocked: true` and no offer to ask Claude.
* The safety checker in the local AI setup: downloadable through the same allow-listed pull but never selectable as the chat model; status and the recommendation report it; the Local AI panel offers "Download safety checker" and says what happens without it. A Child's or Guest's message box stops at 1,000 characters.
* AAM-0001 0.10: the amendment for S1 (draft text at build, with the Sir point open; both settled 7 November 2026, see below).

**Decisions made while building, named for the reviewers and the Programme Sponsor:**

1. **No profile signed in is moderated as a Guest once the household has any profile** (the lowest privilege, as in WP6a 6.2), so "no profile" is never an unmoderated route. Before any profile exists (a fresh install before setup), it is not moderated.
2. **A Guest's message is also limited to 1,000 characters** (M1 named the Child; M6 moderates a Guest like a Child, and the checker must read it whole).
3. **An unreadable classifier answer fails closed** with the "can't check" reply, the same as no classifier.
4. **The escalation path already moderates a Child or Guest** (input and output), so WP6c only has to open the gate.
5. **The classifier is not in the chat-model catalog**; its licence entry is the Llama 3.2 Community License, **confirmed by the Programme Sponsor on 7 November 2026** (M2). Carried to WP6d: the disclosure page should name the safety checker as Meta's Llama Guard 3 ("Built with Llama") and link the licence and Meta's acceptable use policy.

**Wording for the Programme Sponsor to approve before WP6b is committed (Section 5, "(wording)"):**

| Where | Draft text |
|---|---|
| M4 general block | "I can't help with that one. You could ask a grown-up." |
| M4 self-harm | "That sounds like something to talk about with someone you trust, like a parent, a carer or a teacher. If you want to talk to someone right now, you can call Childline for free on 0800 1111. If you or someone else is in danger, tell a grown-up straight away or call 999." |
| M3 checker unavailable | "I can't check that it is safe to answer right now, so please ask a grown-up." |
| Guest general block | "I can't help with that on this computer." |
| Guest self-harm | "If you're struggling, you don't have to deal with it alone. You can call Samaritans for free, any time, on 116 123. If you or someone else is in danger, call 999." |
| Guest checker unavailable | "I can't check that it is safe to answer right now, so I can't reply. Please try again later." |
| S1 child-safety layer | as in 6.5 and AAM-0001 0.10, plus the name line below |
| S1 name line | Local model: "Call them {first name}, not Sir." (the profile's display name, made one line, at most 40 characters). Claude (WP6c): "Do not call them Sir." with no name, so the child's name is never sent to Anthropic through this layer. |

**Programme Sponsor decisions, 7 November 2026:** (1) a child is called by their first name, not Sir: built as the name line above; (2) a Guest gets a neutral set: built, Guest texts above (draft, for approval); (3) the safety checker's licence is confirmed. **Still open:** adding "Nothing was sent anywhere." to the "can't check" reply. Not added: it is true when the question itself could not be checked (nothing reached any model), but **not** when the reply could not be checked, because then the question had already gone to the chat model, and in WP6c possibly to Claude. Recommendation: leave it out, or add it to the question-side reply only, which would mean two "can't check" texts. **Settled the same day:** the three Guest texts approved as drafted; "Nothing was sent anywhere." left out (the Programme Sponsor took the recommendation); WP6b approved through the Sponsor Approval Service (decision 2026-11-07T14:23:03Z on ef17f1d), which approves the wording table above as built: every Child and Guest text, the S1 layer and the name line. The code comments' "DRAFT" markers were replaced to say so (comments only, no behaviour change).

**Evidence:**

* Python (worktree, after the round-1 fixes): **1404 passed, 4 skipped** on Windows. **Linux in Docker** (before the fixes): ruff clean, 1392 passed, 1 failed, validator 0 errors; the failure was `test_frontend_message_limit_matches_the_backend`, which reads `App.jsx` and had not been updated for the 1,000-character limit; it now checks both limits against the backend (stricter, not weaker) and passes. (Docker needed a container-local git repository: a worktree's `.git` is a pointer to a Windows path.) Earlier figure: 1387 passed before the setup tests; `test_moderation.py` 52 tests (the reader, the request sent, fail-closed cases, the runtime both ways and history, the layer for a Child only, safety events with no text, the 1,000 limit by role, no-profile sessions, erasure, retention, the checker in setup).
* Playwright (Chromium, worktree): 177 passed including 3 new WP6b tests; **1 failure, the bundled-fonts test**, which passed in the main tree today and is attributed to the worktree's `node_modules` being a junction to the main tree (WP6b touches no fonts); to be re-run in the main tree.
* **Measured on the rebuilt PC (Ryzen 5 5600, 6 cores)**, the checker on the processor: first check 3.4 s (loading), then about 0.6 s for a new sentence, 0.09 s median for a repeated one; uses **no graphics memory** (`size_vram` 0) beside `qwen3.5:4b` (3.1 GB on the card). Within M1's 2 s target. WP6d repeats this formally.
* **Live check** (real backend, real Ollama, a Child profile): a safe question answered by `qwen3.5:4b`; a weapons question blocked in 0.7 s with the fixed reply; a self-harm sentence given the Childline reply; a 1,001-character message refused; two safety events recorded (violent_crimes, self_harm, input) for the child, with none of the text in the database or logs. **Observation for WP6d:** the first answer took 70 s, the 4B model's first load on this PC.
* **Not yet:** the packaged window.

**Implementation review, WP6b round 1 (Copilot, `sender: reviewer`, verdict starting "WP6b:", 7 November 2026; its first attempt read nothing because the worktree's review folder was a link outside its permitted folder, so the folder was made a real copy and the verdict copied back to the main transcript):** **Conditional Pass, no High**, conditional on M-1. It confirmed every model call is preceded by the input check and every model reply followed by the output check, blocked turns never reach history, speech and transcription feed only `converse`, no-profile sessions are moderated as Guest, num_gpu/num_ctx/temperature are sent on every request, the strict reader, no text in safety events, logs or replies, erasure and retention, all five build decisions reasonable, and no assertion weakened.

| Rating | Finding | Disposition |
|---|---|---|
| **Medium M-1** | No reply cap exists (num_predict is set only if a setting asks), so a long reply (a long story) could overflow the classifier's 4096-token context, which Ollama silently shortens: an unsafe part could go unchecked | **Fixed**: text longer than 4,000 characters is checked in overlapping 4,000-character pieces (400 overlap) covering every character; any piece unchecked fails the whole closed; any unsafe piece blocks, self-harm first; the question shown with a reply is context only, limited to 1,000 characters. 4 new tests, including an unsafe ending 10,800 characters in. The design's "reply capped at roughly 4,000 characters" was not true of the code; this replaces it |
| Low L-1 | The Claude offer path allowed 4,000 characters for a moderated role | **Fixed** (1,000 for Child/Guest, as in conversation); 1 test |
| Low L-2 | `converse`/`escalate` default `role` to None, which is unmoderated: a future caller that forgets the role fails open | **Accepted, recorded**: the only callers (the RPC layer) always pass it, from server-held state; making it required changes every existing caller and test. Revisit if a second caller appears |
| Low L-3 | `escalate` sent the plain persona, so a Child asking Claude (WP6c) would miss the S1 layer | **Fixed** (`_persona_for(role)`); 1 test |
| Low L-4 | Wording: the Childline and grown-up replies are also shown to a Guest, who may be an adult; the "can't check" reply does not say nothing was sent to a model; the Sir point | **Added to the wording questions below for the Programme Sponsor** |

**Antigravity** (second reviewer, high-risk; `sender: reviewer`, started 10:19Z; its first run stopped on a refused `return-findings --help` and was resumed with the exact command): **Pass, no High or Medium.** It ran the 67 moderation tests and the validator, confirmed fail-closed for Child, Guest and no-profile sessions, the request options, the strict reader, **Copilot's M-1 fix (verified)**, safety events with no text, erasure and retention, the five build decisions, S1 for a Child only with an accurate AAM-0001 amendment, the wording safe with the open points correctly left to the Programme Sponsor, and no weakened assertion.

**Both WP6b independent reviews are complete with no open High or Medium.** WP6b waits for: WP6a's commit, the Programme Sponsor's approval of the wording (below and the table above), any wording changes, a re-run in the main tree (including Playwright's fonts test and Linux), then the Programme Sponsor's approval of the built result.

**Wording questions added by the review (for the Programme Sponsor):** (a) a Guest sees the child replies; keep one set for both, or a neutral Guest set (for example "I can't help with that one."); (b) add to the "can't check" reply "Nothing was sent anywhere."? **Answered 7 November 2026:** (a) a neutral Guest set, built; (b) still open, see the recommendation above the evidence.

**Main tree, after the WP6a commit (7 November 2026):** WP6b moved from the worktree into the main tree (checked first: every shared file differs from the committed WP6a only by additions). Windows 1412 Python passed, 4 skipped; Linux in Docker (python:3.12-slim) 1416 passed, ruff, the version check and the validator clean; Playwright (chromium) 178 passed, 5 skipped (the JARVIS_PERF timing tests), including the bundled-fonts test that failed only in the worktree.


**WP6b commit and post-commit review (7 November 2026):** committed as **5ef3637** after `submit-response` (decision 14:23:03Z on ef17f1d). Copilot's review of the real diff: **Pass, no High or Medium.** Low L1: a 40-character display name could still carry a short instruction into the local persona (display names are set by an Administrator; letters-only names would close it; carried to WP6d). Low L2: when a Child may ask Claude (WP6c), the recent conversation and any notes sent with the question may contain the child's name, which the nameless persona line does not cover; **the Programme Sponsor decided 7 November 2026 to disclose this, not scrub it** (built in WP6c, Section 10E). Low L3: stale "draft" wording in this section and the AAM-0001 0.10 history row; corrected.

---

# 10E. WP6c Build Record (7 November 2026)

**Built as designed** (C1, C2, 6.6), after WP6b's post-commit review:

* **Consent records** (`jarvis/identity/child_consent.py`, migration 5 `child_consents`): profile, the Administrator who consented, the fixed scope `question_and_recent_conversation`, recorded, acknowledged and revoked times. Revoked rows are kept (who allowed what, when); all are deleted with the child's profile.
* **The rule, in one place** (`ProfileService.child_may_ask_claude`): a Child may ask Claude only while its consent is recorded, **acknowledged by the child**, unrevoked, given by a profile that is **still an Administrator here**, and the **PIN is set**. It is evaluated on every offer and every send, so revoking, erasing the Administrator who consented, or a PIN reset switches it off at once.
* **RPC** (`consent.status`, `consent.record`, `consent.revoke`, `consent.acknowledge`): record and revoke are Administrator only, and record needs the PIN set; acknowledge is the signed-in Child for itself only; a Child sees only its own status. The role is always the server-held active profile's. Revoking discards the child's open offer.
* **The two independent checks** (6.8): the RPC layer's check (`_may_escalate`, used by the offer, the explicit "Ask Claude" offer, the send and `provider.status`), re-checked at send time; and **Sentinel's cloud rule**, which now admits a Child only when the request carries `child_consent: recorded`, set by the runtime from the server's own records (`ConversationRequest.child_cloud_consent`), never from the client. A Guest or no role is still refused whatever the flag says.
* **Never a Child's notes:** the offer says `sendsMemory: false` for a Child, the RPC passes `share_memory` false, and the runtime refuses notes for a Child whatever it is passed (tested with the database flag forced on).
* **Moderated both ways** (already built in WP6b): the question is checked before it is sent and Claude's answer before it is shown; with no checker, nothing is sent.
* **Screens:** Settings gains **Claude for a child** (Administrator only, one row per Child, Allow / Turn off, with the parent's explanation); a Child's conversation screen shows a one-time **You can ask Claude** card until they press **I understand**; the "Send this question to Claude?" confirmation gains a line for a child; a child's note-sharing row now says notes are never sent even when the child may ask Claude. Four Tauri commands.

**Build decisions, named for the reviewers and the Programme Sponsor:**

1. **No separate classifier probe before the offer.** The design said the offer exists only when the classifier is available. Instead, the question is checked before anything is sent and that check fails closed, so with no checker the child gets the "can't check" reply and nothing reaches Claude (tested). A probe on every turn would add a network call for no extra protection.
2. **A consent does not outlive its giver or the PIN:** checked at use, not by deleting rows, so the history stays.
3. **Re-recording while a consent is current keeps it** (and its acknowledgement); after a revoke, a new consent needs a new acknowledgement.
4. **The Children and safety view (6.7) is still WP6d.** The Settings section here is the minimum needed to record and revoke; WP6d folds it into that view.

**Disclosure of the child's name (Programme Sponsor decision, 7 November 2026: disclose, not scrub).** The parent's explanation, the child's card and the child's confirmation line each say the conversation sent may include the child's name.

**Wording, approved by the Programme Sponsor 7 November 2026** (direct chat "Approved", before WP6c was committed):

| Where | Approved text |
|---|---|
| Settings, parent's explanation | "This is off unless you turn it on, for each child separately. When it is on, the child can choose to send a question to Claude, a service run by Anthropic, and confirms each time. Their question and their recent conversation with JARVIS (the last few messages, up to six) are sent, and that conversation might include their name. Their saved notes are not sent themselves, but something JARVIS said using them may be part of that conversation. Anthropic handles what is sent under its own privacy terms. The safety checker checks each question before it goes and each answer before it is shown. It only starts working once the child has said they understand, and you can turn it off at any time: it stops at once." |
| Child's card (C2 acknowledgement) | Heading "You can ask Claude". "A grown-up has said you can ask Claude. Claude is an AI made by a company called Anthropic. It is not a person, and it can make mistakes. When you choose to ask Claude, your question and your last few messages with JARVIS are sent to Anthropic over the internet. They might include your name, or something JARVIS said using your notes. Your notes themselves are never sent. If anything Claude says worries you, tell a grown-up." Button "I understand". |
| Child's confirmation line | "Your recent conversation might include your name, or something JARVIS said using your notes. Claude is an AI, not a person, and it can make mistakes." |
| Child's note-sharing row | "A child's notes are never sent to Claude themselves. When the child may ask Claude, something JARVIS said using them can be part of the recent conversation that is sent." |

**Implementation review: Copilot** (`sender: reviewer`, 14:50Z): **Conditional Pass, no High.** It confirmed every path to Claude goes through the consent rule, re-checked at send; Sentinel is a real second check the client cannot set; a Child cannot record, revoke or acknowledge for another, and an Administrator cannot acknowledge for a child; moderation fails closed both ways (56 tests run).

| Finding | Summary | Disposition |
|---|---|---|
| Medium M1 | A Child's notes reach Claude indirectly: a local reply that used a note is in the recent conversation sent | **Programme Sponsor decision, 7 November 2026: disclose** (option B; option A, send only the question for a Child, was recommended and not taken). All four texts now say the notes are not sent themselves but something JARVIS said using them may be |
| Low L1 | After a PIN reset and a new PIN, an old consent came back with no Administrator action | **Fixed**: the PIN reset revokes every current consent in the same transaction; test extended |
| Low L2 | Re-recording kept a consent whose giver was no longer an Administrator | **Fixed**: such a consent is revoked and replaced, so the new one is this Administrator's and needs a new acknowledgement; 1 test |
| Low L3 | The parent's text did not say what "recent" means or what Anthropic does with the data | **Fixed in the wording**: "the last few messages, up to six" and "Anthropic handles what is sent under its own privacy terms" (no specific retention claim made, because not verified) |
| Note | Decision 1 (no classifier probe before the offer) is a deviation the Programme Sponsor should note: with no checker a child can see the offer and then the "can't check" reply | **Named to the Programme Sponsor**, 7 November 2026 |

**Antigravity** (second reviewer, high-risk; `sender: reviewer`, after Copilot's fixes): **Pass, no High or Medium.** It verified the default-off rule on every path, Sentinel as a genuine second check the client cannot forge, the consent lifecycle (giver, PIN reset, erasure, revocation of an open offer), the L1 and L2 fixes, and that the option B disclosure is accurate on every screen; it judged all four build decisions sound. Info: with the checker down, a child can see the offer and then the "can't check" reply (decision 1, already named).

**Evidence (main tree):** Linux in Docker (python:3.12-slim) 1436 passed, ruff, the version check and the validator clean (re-run after the review fixes: 1437 passed). Python 1433 passed, 4 skipped after the review fixes (21 in `jarvis/tests/test_child_consent.py`); ruff clean; Playwright (chromium, both specs) 184 passed, 5 skipped (4 new app tests and 2 new axe checks; one existing text updated on purpose); Rust 19 passed.

**Approval:** the four texts above approved by the Programme Sponsor in direct chat; **WP6c approved through the Sponsor Approval Service** (decision 2026-11-07T18:23:50Z on 5ef3637); the DRAFT markers in `src/ChildConsent.jsx` and `src/ClaudeEscalation.jsx` replaced with the approval note.

**Commit Contents (WP6c):** `jarvis/identity/child_consent.py` (new), `jarvis/identity/store.py`, `jarvis/identity/service.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/interfaces/activity_tracker.py`, `jarvis/interfaces/conversation.py`, `jarvis/interfaces/sentinel_conversation.py`, `jarvis/interfaces/escalation.py`, `jarvis/guardian/runtime.py`, `sentinel/policy.py`, `jarvis/tests/test_child_consent.py` (new), `jarvis/tests/test_schema_migrations.py`, `src-tauri/src/lib.rs`, `src/ChildConsent.jsx` (new), `src/App.jsx`, `src/SettingsView.jsx`, `src/ClaudeEscalation.jsx`, `src/shell.css`, `tests/e2e/app.spec.js`, `tests/e2e/accessibility.spec.js`; records: this EIP, `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md` (L3 wording), ESR-0061, REG-0001.
---

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.8 | 7 November 2026 | Claude Engineering Implementer | WP6b post-commit review recorded (Pass; L2 decided: disclose the child's name). WP6c built (Section 10E): consent records, the rule, both checks, screens; reviews (Copilot Conditional Pass, M1 decided: disclose; Antigravity Pass); wording approved and WP6c approved through the Sponsor Approval Service (decision 2026-11-07T18:23:50Z on 5ef3637). |
| 0.7 | 7 November 2026 | Claude Engineering Implementer | WP6b approved (14:23:03Z) and committed with the wording table approved; earlier the same day, Programme Sponsor decisions applied: a child is called by their first name (local model only, never sent to Claude), a neutral Guest wording set, classifier licence confirmed. "Nothing was sent anywhere" left open with a recommendation. |
| 0.6 | 7 November 2026 | Claude Engineering Implementer | WP6a implementation reviews recorded (Copilot Conditional Pass, Medium M1 fixed; Antigravity Pass after a first run lost to a run_reviewer.py defect); add-profile screen built on the Programme Sponsor's decision; final evidence incl. Linux 1341 passed. Awaiting approval of the built result. |
| 0.5 | 7 November 2026 | Claude Engineering Implementer | WP6a built (Section 10C): PIN, elevation rule, creation gating, notices, reset tool, screens; five build decisions named; one scope flag (no add-profile screen) for the Programme Sponsor. Awaiting independent implementation review. |
| 0.4 | 7 November 2026 | Claude Engineering Implementer | Design approved as recommended (Section 10B): C1 built, last and off by default; child-facing wording still to be approved per sub-WP. PC rebuild and Mac replacement recorded; Mac measurements carried to the next session. |
| 0.3 | 15 October 2026 | Claude Engineering Implementer | WP6 design re-check recorded (Pass); out-of-scope bullet corrected for Guest moderation. |
| 0.2 | 15 October 2026 | Claude Engineering Implementer | Design review (Fail: two High, four Medium, two Low, two Info) addressed: a Child or Guest session is locked and Guest is moderated (P2, M6); the no-PIN residual risk named and mitigated (P3); lock-out capped and visible (P1); reset made detectable (P5); `num_ctx` set and no truncation (M1); wording corrected (M4, D1). Section 10A. |
| 0.1 | 15 October 2026 | Claude Engineering Implementer | Initial design for WP6, drafted at the Programme Sponsor's request. Thirteen decisions with recommendations (P1-P5, M1-M5, C1, C2, S1, D1); four sub-WPs. Nothing built. |
