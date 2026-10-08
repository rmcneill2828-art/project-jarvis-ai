# EIP-ESR0061-004 - Guardian Experience Redesign and Presence Orb

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-004 |
| Title | Engineering Implementation Package: WP4 Guardian Experience Redesign and Presence Orb |
| Version | 0.7 |
| Status | Draft - design approved (prototype and decisions W1-W10 as recommended, 8 October 2026), committed 6081425; WP4a committed b3693cb and post-commit reviewed (Conditional Pass, one High fixed in WP4a-fix, one Medium withdrawn); WP4a-fix committed 936949e and post-commit reviewed (Pass); WP4b built, implementation review Conditional Pass (one Medium fixed), awaiting the Programme Sponsor's approval to commit; WP4c and WP4d not started |
| Session | ESR-0061. WP4 is planned for Session B (WP3-WP4); the design is drafted now under D22 |
| Work Package | WP4 |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 4.5 (Orb criteria) and Section 7, WP4 |
| Architecture | [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] 1.7 (Orb decoupled from the knowledge graph; five-state Orb acceptance criteria) |
| Backlog | EBG-0164 (the redesign); EBG-0150 is allocated here by the plan but is a misfit - see Section 7 |
| Prototype | `aiems/models/WP4_GUARDIAN_EXPERIENCE_PROTOTYPE.html` (also published as a private artifact for the Programme Sponsor to open) |
| Risk class | Not on the plan's high-risk list, but it carries the role-aware UI and the AI disclosure that WP6's child-safety work relies on, so the design review is Antigravity alone while Copilot's quota is out (resets 1 November 2026) |

---

# 2. Purpose

Replace the shell's long scrolling page with one Guardian-centred app that looks and behaves the same on Windows (WebView2) and macOS (WKWebView), as EBG-0164 and the Programme Sponsor's decisions D3 and D9 to D12 require:

* an app shell with views, so the conversation is always on screen;
* a **presence Orb** with five real states, decoupled from the knowledge graph, meeting UAM-0001's acceptance criteria;
* the knowledge graph kept as its own view, with no functionality lost;
* bundled fonts and one set of design tokens, so the look does not depend on what the computer has installed;
* a UI that shows each household role only what that role may use, and always says plainly that the person is talking to an AI and where the answer came from;
* a **functionality-preservation inventory** (Section 6, item 6.12) as the gate: WP4 does not close until every row has a passing test.

**The Programme Sponsor approves the prototype** (plan, WP4): it is what the Orb, the layout and the look are judged against (criterion 5).

---

# 3. Decomposition

| Sub-WP | Content | Effort |
|---|---|---|
| **WP4a** | Foundations: design tokens, bundled fonts, the shell and navigation, the six views created with the **existing panels moved in unchanged**. Behaviour-preserving; the 44 existing Playwright tests are updated for the new locations | 1.5-2 d |
| **WP4b** | The Guardian view: the presence Orb and its five event-driven states, the conversation pane with the composer pinned at the bottom, the AI disclosure and per-reply source labels; two small backend additions (Section 6, item 6.4) | 2 d |
| **WP4c** | Role-aware visibility, the honest capability list, removal of the dead controls and static labels, the Knowledge and AI models views finished | 1.5-2 d |
| **WP4d** | Quality: accessibility (reduced motion, contrast, focus, axe checks), performance measurement on the household PC, cross-engine checks, the functionality-preservation sign-off, documentation and backlog updates | 1-1.5 d |

Total 6-7.5 days, as the plan estimates. Each sub-WP is a gated commit (rule A6: design approval first, then the built result, then the Programme Sponsor's real `~/approve`).

---

# 4. Repository Context Investigated

* **Layout today** (screenshot at 1280 x 820, 8 October 2026): a long scrolling page of nine stacked surfaces; the composer sits below the fold; the Orb is a small canvas in the middle of empty space; three surfaces repeat platform status.
* **Dead and static things** - found in `src/App.jsx`: Notifications, Settings, Minimize, Maximize and Close buttons in the header do nothing (the window already has the operating system's own title bar); "View all capabilities", "View diagnostics" and the four shortcut buttons (Platform Status, View Capabilities, Run Diagnostics, Show Roadmap) do nothing; the sidebar is titled "Platform Placeholders" and its Agents row says "No execution" even though an agent runs. Each is a UAM-0001 Section 10 (capability awareness) breach.
* **The Orb today** is `GuardianOrbGraph.jsx` (614 lines): a Canvas 2D force-directed drawing of the repository's knowledge graph, shown whether or not a repository exists. Its drawing and the shared frame clock (`animationScheduler.js`, EBG-0081 item 1) are sound and are **kept for the Knowledge view**; the new Orb is a different component.
* **Fonts** - the CSS names Inter but bundles nothing, so macOS falls back to the system font and the two platforms already differ.
* **Constraints** - the Tauri content security policy allows only `'self'` styles, scripts and images (`data:` images allowed): bundled fonts and canvas drawing are fine; no remote fonts or scripts. The window's minimum size is 960 x 640.
* **What the UI calls** (25 commands): `platform_status`, `knowledge_graph`, `list_profiles`, `active_profile`, `create_profile`, `select_profile`, `send_message`, `speak_message`, `transcribe_audio`, `list_agents`, `invoke_agent`, `memory_status`, `list_memory`, `delete_memory`, `backup_memory`, `restore_memory`, and (WP3) `provider_status`, `offer_escalation`, `escalate_message`, `ollama_status`, `ollama_recommendation`, `ollama_pull`, `ollama_cancel_pull`, `ollama_use_model`, `open_ollama_download_page`. Backend notifications reach the UI as `jarvis://notification`: `system.heartbeat`, `knowledge.cluster_activity`, `ollama.pullProgress`, `ollama.pullFinished`.
* **Real events the Orb can use** - recording (`isRecording`), a request in flight (`sending`, `escalating`, and a transcription in flight), the platform status, and the outcome of the last turn exist today. **Speaking is not tracked**: `speak_message` returns audio the app plays, but nothing records that it is playing.
* **Tests** - 44 Playwright tests drive the UI through a mocked Tauri layer. A WebKit project runs in CI as an informational job; two microphone tests fail there (a WKWebView difference, for WP7).
* **Role enforcement** - the backend refuses what a role may not do for memory approval, memory sharing, model downloads and escalation. It does **not** yet stop a Child profile creating an Administrator profile (WP6's PIN work). The UI hiding things is therefore a courtesy and a safety net for honesty, **not security**, and the design says so.

---

# 5. Decisions Needed From the Programme Sponsor

Each has a recommendation, so a bare "approved" settles it. Open the prototype first: it shows the look, the layout, the Orb's states, the four roles and the Ask Claude confirmation. The amber **Prototype controls** pill at the bottom right switches Orb state, role and reduced motion.

| # | Decision | Recommendation |
|---|---|---|
| W1 | **The look** | Keep the reference mock-up's Obsidian character - near-black ground, violet and cyan light - as **one dark theme for v1** (no light theme). Bundle **Manrope** for the interface and **JetBrains Mono** for figures, both under the SIL Open Font Licence, installed from npm so nothing is fetched at run time |
| W2 | **Navigation** | A left rail with six views: Guardian, Memory, Knowledge, Agents, AI models, System. The window's own title bar stays. A Settings view arrives with WP5 and is not shown until it does |
| W3 | **The Orb and its performance target** | Five states from real events (item 6.3), drawn on Canvas 2D (ADR-0021) with a **frame budget by state**: active states up to 60 frames a second, idle 30, offline 10. Target, measured in WP4d on the household PC: **active states sustain at least 50 frames a second, and idle uses under 5 percent total CPU**. If a target is missed, a quality ladder applies before any redesign: fewer points (240, 120, 60), then a lower idle rate. **The Mac is checked early:** at Mac visit 1 the prototype is opened on the household Mac and its on-screen frame rate and CPU are read, so the ladder is set before WP4b is built; the built Orb is measured at visit 2. Paused when the window is hidden; reduced motion shows one still frame per state |
| W4 | **What each role sees** | The matrix in item 6.5. Child and Guest see no model management, no Claude and no agents, and are not told Claude exists |
| W5 | **AI disclosure** | A permanent line above the composer ("You are talking to JARVIS, an AI. Replies come from ...") and a label on every reply naming where it was produced. The first-run explanation for Child profiles stays in WP6 |
| W6 | **Remove the dead controls and the static text** | Remove everything listed in Section 4. Nothing is lost: none of it did anything |
| W7 | **Knowledge graph** | Its own view with today's canvas, metrics and clusters unchanged. Where no repository is present it says so plainly; this is checked against a packaged build, not assumed |
| W8 | **New dependencies** | Runtime: the two font packages (OFL 1.1; the files are bundled by the build). Development only: `@axe-core/playwright` (MPL-2.0) for automated accessibility checks. No new crate; no new run-time permission |
| W9 | **The Orb status readout of UAM-0001 8.3** (Mode, Confidence, Autonomy, Permission) | **Not built.** The platform has no real source for confidence or autonomy, and 8.3 forbids decorative values. Revisit when it has |
| W10 | **Backlog misfit** | EBG-0150 (move the composition root out of `stdio_rpc.py`) is a backend refactor the redesign does not need. Recommend a separate small package **before WP5**, which adds more RPCs to that file |

---

# 6. Design

**6.1 Shell and navigation (WP4a).** A top bar (brand, one overall status chip, the profile switcher), a left rail of views, and a main area. One status surface replaces the three repeated ones. The rail is a `nav` landmark; the current view is marked `aria-current`; every control is reachable by keyboard in reading order. Below 900 pixels the rail shrinks to icons; below 640 it becomes a bottom bar (the packaged window cannot go below 960 x 640, so the narrow layouts serve tests and future use). A role that may not use a view does not see its entry.

**6.2 The Guardian view (WP4b).** The Orb and its one-line readout above; the conversation below in its own scrolling pane; the composer **pinned to the bottom**, with the disclosure line above it, so that at 960 x 640 and at 1280 x 820 it is never below the fold (tested). A "What is available" column at the side from 1100 pixels up, collapsing away below that. The quick-action buttons are gone; Ask Claude, the microphone and Send sit in the composer. The offer to ask Claude (WP3b) appears as a line above the composer; the confirmation dialog is unchanged in meaning. **The conversation belongs to the profile that had it:** switching profile clears the on-screen conversation, the open offer and any open dialog (the backend already keeps each profile's history separate; today the screen keeps the previous profile's messages, which would show a household member's conversation, and any Claude labels in it, to the next profile - found by the design review in the prototype and confirmed in the current code, and fixed in WP4b with a test).

**6.3 The presence Orb (WP4b).** Five states, each driven by a real event and never by a timer or script (a test asserts the state from each event):

| State | Real event | Look |
|---|---|---|
| Listening | Recording is on (`isRecording`) | Green-cyan, rings drawing inwards |
| Speaking | The reply audio is playing (new: the app records play, end and error of the audio it plays) | Amber-cyan, the sphere pulses, rings drawing outwards |
| Thinking | A request is in flight: a turn, an escalation or a transcription | Violet-magenta, fast rotation, a travelling ripple |
| Offline | The platform status is not running, no provider is online, or the last turn failed because no provider answered; clears on the next success | Grey with a red core, no motion |
| Idle | None of the above | Cyan-violet, slow rotation and breathing |

Priority when several apply: **speaking, thinking, offline, listening, idle** (changed in v0.2 after the design review: Offline outranks Listening so the Orb never looks ready to hear a question the system cannot answer). While offline and recording, the Orb stays Offline and the readout says the microphone is on but JARVIS cannot answer until an AI model is reachable; the person can still send the transcript, which gets the honest "could not reach an AI provider" reply and, for an Administrator or Adult, the offer to ask Claude. The drawing is a 240-point sphere on Canvas 2D, time-based, on the existing shared clock, on a frame budget by state - up to 60 frames a second when active (a 120 Hz Mac is not driven twice as hard), 30 when idle, 10 when offline - device pixel ratio capped at 2, paused while hidden. **Reduced motion** (the operating system setting) draws one still frame per state with a ring marking active states; **the state is always also written as text** in a live region ("Ready", "Listening", "Thinking", "Speaking", "Offline: JARVIS cannot reach an AI model on this computer"). The Orb reads nothing from the repository, so it looks the same with no repository present. **Prototype measurements:** 54-60 frames a second in headless Chromium on the household PC with no errors in Chromium; this is the prototype, not the product, and says nothing about the Mac or about CPU use.

**6.4 Two small backend additions (WP4b).** (a) `platform.status` gains `speechAvailable`, as `transcriptionAvailable` already exists, so Voice output can be shown as available or not instead of guessed. (b) `guardian.converse` returns the `model` that answered, so each reply can say "On this computer, qwen3.5:4b" or "Claude". Both are additive; both get tests.

**6.5 What each role sees (WP4c).** The UI mirrors what the backend enforces and adds nothing the backend does not check:

| View or control | Administrator | Adult | Child | Guest |
|---|---|---|---|---|
| Guardian (chat, voice, disclosure) | yes | yes | yes | yes |
| Ask Claude and the offer | yes | yes | not shown, not mentioned | not shown, not mentioned |
| Memory (list, forget) | yes | yes | list only, no forget | no |
| Memory back up and restore | yes | disabled with the reason | no | no |
| Knowledge | yes | yes | no | no |
| Agents | yes | yes | no | no |
| AI models (view) | yes | yes | no | no |
| Download, cancel, switch model | yes | yes | no | no |
| Change memory sharing with Claude | yes | disabled with the reason | no | no |
| System | yes | yes | no | no |

A control that is shown but unavailable says why in words. Profile creation and switching stay as they are until WP6's PIN work; the design records that a Child can still create a profile today, so none of this is a security boundary.

**6.6 AI disclosure and source labels (WP4b).** The line above the composer is always present and names the source of replies in the current conversation ("the model on this computer (qwen3.5:4b)" or "Claude, over the internet"). Each reply carries a label: "On this computer" with the model, or "Claude" with "answered over the internet". The existing Claude badge (WP3b) becomes this label.

**6.7 Honest capability list (WP4c).** Replaces "Platform Placeholders". Each row is built from real status (`platform_status`, `provider_status`, `ollama_status`, `list_agents`, `memory_status`, the two voice flags) and shows one of five states, each with an icon **and** a word so colour is never the only signal: Ready, Preparing, Not available, Offline, Unknown. A capability that is not built (vision, internet search, home automation) appears only in the System view's "Not available yet" list. A status that cannot be read shows Unknown, never Ready.

**6.8 Tokens and fonts (WP4a).** One stylesheet of design tokens (the colours, type scale, spacing and radii used in the prototype's `:root`), the existing panels re-based onto them. The two fonts are installed as npm packages and imported by the build, so the files ship inside the app and satisfy the content security policy. Text colours are tested for a contrast ratio of at least 4.5 to 1 against their grounds.

**6.9 One look on two engines (WP4d).** The Chromium and WebKit Playwright projects both render every view at 1280 x 820 and 960 x 640; the screenshots are kept as CI artifacts for review, and layout assertions (the composer is visible; nothing overflows horizontally) run on both. **Playwright's WebKit is not the same as the Mac's WKWebView**, so the real comparison happens on the household Mac at Mac visit 1 (a first look) and visit 2 (the release candidate).

**6.10 Accessibility (WP4d).** Keyboard reach and a visible focus ring everywhere; the conversation log and the Orb readout are live regions; reduced motion honoured; `@axe-core/playwright` checks every view in CI and must report no serious or critical violations; the dialog traps focus and returns it on close.

**6.11 Performance measurement (WP4d).** A scripted run records frame times in each Orb state on the household PC (Chromium, and the packaged WebView2 app by hand with Task Manager for CPU); the Mac is looked at early (the prototype's frame rate and CPU at visit 1) and measured on the built Orb at visit 2. Results go in this package. The prototype shows an on-screen frame rate for the Programme Sponsor's own look at smoothness.

**6.12 Functionality-preservation inventory (the gate).** Every row needs a passing test in the new location before WP4d closes.

| Today | Where it goes | Test |
|---|---|---|
| Overall platform status badge | Top bar chip | status shown for running, connecting, offline |
| Platform, Core Services and External Providers cards | The "What is available" list and the System view | list reflects real status; unreadable shows Unknown |
| Sentinel, Platform Services, Memory, Providers and Agent Framework sidebar rows | The same list, built from real status | each row from mocked status |
| Guardian Orb drawing the knowledge graph, with cluster illumination | Knowledge view, unchanged | graph draws; cluster lights on notification; no-repository message |
| Knowledge Metrics and Active Clusters panels | Knowledge view | figures shown |
| Conversation, send, local reply | Guardian view | send shows the reply |
| Speak this response | Guardian view, per reply | audio plays; Orb speaks; failure shown |
| Microphone, transcript into the composer | Guardian view composer | transcript fills the composer, not auto-sent; hidden when unavailable |
| Ask Claude, offers, the confirmation, the Claude badge | Guardian view, labels per item 6.6 | the WP3b tests, re-pointed |
| The warning in the Claude confirmation once 80 percent of the month's allowance is used | The same dialog | warning shown at 80 percent, absent below |
| The previous profile's conversation is not shown to the next profile | Guardian view (new behaviour, item 6.2) | switch profile, conversation and offer cleared |
| Profile create, switch, show active | Top bar profile switcher | create and switch tests |
| System Health panel and heartbeat | System view | health rows; heartbeat time |
| Agent Framework panel (list, run, result, errors) | Agents view | list, run, denied, error |
| Memory count, show, forget, back up, restore with overwrite confirmation | Memory view, unchanged logic | the existing memory tests, re-pointed |
| The "(Household)" marker on a shared note | Memory view | a shared note shows the marker |
| Local AI panel (status, install steps, download, progress, cancel, switch, disk warning, the below-the-usual-minimum warning, override note, role limits) | AI models view | the WP3c tests, re-pointed, with the below-minimum warning added |
| Diagnostics panel (implementation boundary) | System view, with static text replaced by real status | rows from real status |
| Footer (edition, "all times are local") | System view and top bar | version shown |
| Notifications, Settings, window buttons, shortcuts, "View all ..." (11 controls that did nothing) | **Removed** (decision W6) | test that none remain |

---

# 7. Cross-Work-Package Flags

* **EBG-0150 is a misfit** for WP4 (decision W10): it is a backend refactor. Proposed disposition: its own small package before WP5.
* **WP5** builds the Settings view, first-run flow, the keychain for the Claude key and the per-profile memory-sharing screen on this shell. WP4 leaves a place for Settings in the rail but does not show it.
* **WP6** owns the PIN, Child consent, moderation and the Child first-run explanation. WP4's role-aware hiding is not enforcement. The finding from WP3c also lands there: on the 8 GB card a 9B chat model cannot stay loaded beside a moderation model.
* **WP7** owns voice. Two microphone tests fail on WebKit today; WP4 keeps the microphone control working in the new composer and does not try to fix the WKWebView difference.
* **WP8** needs screenshots of the finished UI for the user guide and the parents' guide.
* **Mac visits.** First look at the look and the Orb on the household Mac at visit 1; frame rate and the unified-look comparison at visit 2.
* **Open from WP3** (carried, not part of WP4): the Claude Console spend-limit check, the live refusal and overload checks, and the Mac model measurements.

---

# 8. Evidence Pack (TPL-0001 Section 6)

| Item | Content |
|---|---|
| Prototype | The clickable HTML prototype; checked in Chromium at 1280 x 820, 960 x 640 and 400 x 800 and with reduced motion, all five Orb states, four roles, no script errors |
| Platform coverage | The UI is web code, identical on both platforms except the engine; the WebKit CI project and the Mac visits cover the second engine |
| CI | Existing jobs plus an axe accessibility step in the Playwright job; the WebKit job stays informational until its two known microphone failures are fixed in WP7 |
| Tests | Per row of the inventory; the Orb state from each real event; role matrix for every view and control; the composer visible at both window sizes; contrast of every text token; axe per view; reduced motion |
| New dependencies | Two OFL font packages (run time, bundled) and one MPL-2.0 development tool |
| Privacy (D23) | No new data is collected or sent. The disclosure line and source labels make the cloud path visible |

---

# 9. Commit Contents (expected, per sub-WP; finalised at build)

**WP4a:** `package.json` and lock file, `src/` shell, tokens, view files, the moved panels, `src/styles.css`, `tests/e2e/`. **WP4b:** `src/` Guardian view, Orb and disclosure, `jarvis/interfaces/stdio_rpc.py` and its tests, `src-tauri/src/lib.rs` if a command changes. **WP4c:** `src/` role-aware views and capability list, tests. **WP4d:** CI workflow, accessibility and performance tests, records. Each with the record files.

---

# 10. Questions for the Engineering Reviewer

1. Is the Orb state model (item 6.3) complete and honest - is each state really driven by an event the app can observe, and is the priority order right (for example, a person recording while the provider is offline)?
2. Is hiding by role (item 6.5) described honestly as not being security, given that profile creation is unguarded until WP6?
3. Does the functionality-preservation inventory (item 6.12) miss anything the current UI does?
4. Is the performance target (decision W3) measurable and fair, and is it right to defer the Mac figure to visit 2?
5. Is Playwright WebKit an acceptable stand-in for WKWebView in CI, given the limits stated in item 6.9?
6. Are the two backend additions (item 6.4) the smallest that make the disclosure and the capability list truthful?
7. Is the split into four gated commits sound?

---

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.7 | 8 October 2026 | Claude Engineering Implementer | WP4a-fix committed (`936949e`) and its post-commit review recorded (Section 20). WP4b built: the presence Orb, the Guardian view, the AI disclosure and reply labels, the profile-switch clearing, two small backend additions (Section 21); implementation review Conditional Pass, one Medium fixed (Section 22). Section 23 is the expected commit contents. |
| 0.6 | 8 October 2026 | Claude Engineering Implementer | WP4a committed (`b3693cb`) and its post-commit review recorded (Section 17), with a correction to my own mistake in the review brief (I read a Dependabot CI run, not the push run). WP4a-fix built for the review's High finding: the switch to a downloaded model now happens in the app, not the panel (Section 18). |
| 0.5 | 8 October 2026 | Claude Engineering Implementer | WP4a implementation review Conditional Pass (Gemini; one Medium, one Low; two resumes). Both fixed with tests: the Guardian view's heading is now the level-1 heading; the choice to switch to a model when its download ends now survives a visit to another view. Section 16 review record; test counts updated (57); `src/LocalAiPanel.jsx` added to the file list. |
| 0.4 | 8 October 2026 | Claude Engineering Implementer | Design commit `6081425` recorded (Section 13) with its post-commit review (Conditional Pass: one Medium, fixed). WP4a built (Programme Sponsor approved the design; WP4a started at once): tokens and bundled fonts, the app shell, the six views with the existing panels moved in, the controls that did nothing removed. Section 14 build record, Section 15 commit contents. |
| 0.3 | 8 October 2026 | Claude Engineering Implementer | Programme Sponsor approved the prototype and decisions W1-W10 as recommended (chat, 8 October 2026). This is the design approval of rule A6; nothing is built. |
| 0.2 | 8 October 2026 | Claude Engineering Implementer | Design review (Conditional Pass: one High, two Medium, one prototype privacy leak) addressed: Offline outranks Listening in the Orb priority; a frame budget by state with a quality ladder and an early Mac look at Mac visit 1; three behaviours added to the inventory; the on-screen conversation clears when the profile changes (a real defect in the current app, now in scope). Prototype updated to match. Section 12 review record. |
| 0.1 | 8 October 2026 | Claude Engineering Implementer | Initial design and clickable prototype, drafted ahead of Session B under D22 at the Programme Sponsor's request: app shell with six views, the five-state presence Orb, role-aware visibility, AI disclosure, the honest capability list, bundled fonts, and the functionality-preservation inventory as the gate. Ten Programme Sponsor decisions with recommendations. Nothing built. |

---

# 12. Design Review Record

**Review 1** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T19:1xZ, `sender: reviewer`, no resumes): **Conditional Pass.** It checked the design's claims about the current code and confirmed them: the eleven listed controls are static with no handler; `GuardianOrbGraph.jsx` is the repository-graph Orb; fonts are named but not bundled; the content security policy and the 960 x 640 minimum are as stated; all 25 commands are called; recording, sending and escalating have state flags and speaking has none; `_require_role` guards escalation, memory sharing, model management and memory approval while `profile.create` has no check, so the role matrix and its honesty note are right. Its findings and what was done:

| Rating | Finding | Disposition |
|---|---|---|
| **High** | The priority listening-above-offline lets a person speak to a system that cannot answer | **Accepted and changed** (item 6.3): Offline now outranks Listening; while recording offline the readout says the microphone is on but JARVIS cannot answer, and the transcript can still be sent for the honest failure reply and the offer |
| Medium | The inventory omitted the "(Household)" marker on shared notes, the 80 percent allowance warning and the below-minimum hardware warning | **Accepted**: three rows added to item 6.12 |
| Medium | 5 percent CPU is tight for a continuous 60 frames a second, and leaving the Mac to visit 2 risks late changes | **Accepted** (decision W3): a frame budget by state (60 active, 30 idle, 10 offline), a quality ladder before any redesign, and the prototype's frame rate and CPU read on the Mac at visit 1 |
| Prototype | Switching from an Adult who asked Claude to a Child left the chat log, the disclosure line and the Claude labels on screen | **Accepted and found to be a real defect in the current app**, not only the prototype: the app keeps the previous profile's messages on the screen when the profile changes. Item 6.2 now requires clearing the conversation, offer and dialog on a profile change, with a test; the prototype does so |
| Info | Security honesty acceptable; WebKit acceptable for layout checks with the Mac visits as the gate; the two backend additions sufficient; the four-commit split sound | None needed |

**Caveats, disclosed:** a single reviewer with no web access, which judged the written design and the prototype's source, not how it feels to use; **the Programme Sponsor's own look at the prototype is the real test of the look and the Orb's smoothness**. The prototype's frame rates (54 to 60 frames a second in headless Chromium on the household PC) say nothing about CPU use or the Mac. The reviewer's conditions are addressed in v0.2 and the changed prototype was re-checked by the Engineering Implementer, not re-reviewed.

# 13. Design Commit Record (8 October 2026)

The design was committed as `6081425` (documentation only) after the Programme Sponsor's approval of the prototype and decisions W1 to W10 in chat and then their real `~/approve` (`submit-response` refused the first attempt and accepted the second, as designed). Its six files: this EIP, `aiems/models/WP4_GUARDIAN_EXPERIENCE_PROTOTYPE.html`, and edits to EIP-ESR0061-003, ESR-0061, REG-0001 and EBR-0001. **The deterministic pre-check failed its file-list check on that commit**, because this EIP had no Commit Contents section for a design commit (Section 9 lists the future build commits); every other hard check passed and CI was green. This section is the remedy. Post-commit review (Antigravity, Gemini, one resume for a refused `--format` option): **Conditional Pass.** It confirmed the six files, the four design-review conditions present and consistent, and the records consistent; it accepted the missing section as a remediable gap. **One Medium:** the prototype's Memory view printed the sentence about memory going to Claude to every role, so a Child saw Claude mentioned, against decision W4. **Fixed** in this commit (the sentence shows only to Administrator and Adult) and the artifact republished; a test walked every view as Child and Guest and found no mention of Claude.

# 14. WP4a Build Record (8 October 2026)

| Item | Result |
|---|---|
| Tokens and fonts (item 6.8) | `src/tokens.css`: the design tokens (surfaces, text, five light colours, type scale, radii, spacing) from the prototype, one dark theme. **Manrope** (variable, Latin and Latin Extended) and **JetBrains Mono** (400 and 500, Latin) installed from npm (`@fontsource-variable/manrope`, `@fontsource/jetbrains-mono`, both SIL Open Font Licence 1.1) and declared with `@font-face` from the package files, so the build bundles them: four files, about 83 KB, nothing fetched at run time (a test records every request and finds none outside the app). A reduced-motion rule stops animations system-wide |
| The shell (item 6.1) | `src/Shell.jsx` and `src/shell.css`: a top bar (brand, one platform status chip, the profile switcher), a left rail of six views as a `nav` landmark with `aria-current`, and a main area; the rail shrinks to icons below 900 pixels and becomes a bottom bar below 640. The old stylesheet `src/styles.css` is replaced by `tokens.css`, `shell.css` and `panels.css`; the panels' markup and class names are unchanged, their styles re-based on the tokens and freed of their fixed heights |
| The six views | Guardian (heading, conversation, pinned composer), Memory, Knowledge (the graph canvas with its metrics and clusters), Agents, AI models (the Local AI panel), System (status cards, health, the capability rows, diagnostics, version). The panels were **moved, not changed**; the 44 existing Playwright tests needed only a step to open the right view. The conversation and its state live in the app, so they survive switching views (tested) |
| Controls that did nothing | **Removed here, earlier than the design's WP4c** (decision W6 was approved; removing them with the header, sidebar and shortcuts they lived in was simpler than carrying them): Notifications, Settings, Minimize, Maximize, Close, View all capabilities, View diagnostics and the four shortcuts; and the "Platform Placeholders" heading. A test walks every view and finds none of them |
| Profile | The active profile is a top-bar button showing the initial, name and role, with the existing picker as a popover; with no profile the existing create form shows as a banner above the views, as before |
| Composer never below the fold | The conversation scrolls inside its own pane and the composer is pinned at the bottom; tested after twelve turns at 1280 x 820 and at 960 x 640, and the page itself never scrolls |
| Tests | 44 updated, **13 new** (six views and the current one marked; keyboard reach; composer visible at both sizes; no sideways overflow in any view at 960 x 640; conversation survives view switches; dead controls gone; profile in the top bar; fonts bundled with no outside requests; every text token at least 4.5 to 1 on every surface). **57 Playwright tests pass** (the last three came from the implementation review's findings, Section 16; the mock now supports backend notifications, so the app's real listener is exercised) |
| Evidence | Playwright 57 passed (Chromium); Vite build clean. No Python or Rust changed in this sub-WP, so the pytest, ruff and cargo figures are unchanged from the WP3c commit and CI re-runs them |
| **Intermediate state, disclosed** | **The Guardian view has no Orb until WP4b**: the knowledge graph, the old Orb, now lives in the Knowledge view, so the Guardian view shows a heading and the conversation only. The "Capabilities" panel in System still shows the old static rows (including "Platform Services: Placeholder" and "Agents: No execution") until WP4c replaces it with the honest list; and role-aware hiding is WP4c, so every role still sees every view. The graph canvas's accessible label now reads "Repository knowledge graph" |
| **Not done** | The WebKit project was not run locally (no WebKit browser on this PC); CI's informational job runs it. **Not looked at by me in the real Tauri window** - the screenshots are from the Vite page with a mocked backend; the Programme Sponsor's first look at the shell in the real app is the check that the WebView2 rendering matches. The Docker Linux check is skipped for this sub-WP because no Python changed |

# 15. WP4a Commit Contents (expected)

New: `src/tokens.css`, `src/shell.css`, `src/panels.css`, `src/Shell.jsx`. Removed: `src/styles.css`. Changed: `package.json`, `package-lock.json`, `src/App.jsx`, `src/main.jsx`, `src/GuardianOrbGraph.jsx`, `src/LocalAiPanel.jsx`, `tests/e2e/app.spec.js`, `aiems/models/WP4_GUARDIAN_EXPERIENCE_PROTOTYPE.html`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`.

# 16. WP4a Implementation Review Record

**Review 1** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T20:0xZ, `sender: reviewer`, two resumes - it first piped `tail` into `head`, which its allow-list refuses): **Conditional Pass.** It found functionality preserved (all 25 backend commands still reachable, the removed controls truly inert), the fonts bundled by Vite and compatible with the content security policy, every class used in the JSX defined with no overlap at 960 x 640, the records accurate and the prototype's Child view free of any mention of Claude. Findings and dispositions:

| Rating | Finding | Disposition |
|---|---|---|
| Medium | The Guardian view used a level-2 heading where every other view has a level-1 heading | **Fixed**: the heading is a level-1 `h1` with the same look; a test asserts exactly one level-1 heading in each of the six views |
| Low | Switching view unmounts a panel, so the Local AI panel lost its "switch to this model when the download ends" choice, and the list opened in the Memory view is also lost | **Local AI fixed** - the choice is held by the app, and a finished-download notification that arrives while the panel is away is acted on when it is shown again (a test starts a download, visits System, pushes the finished notification and returns; **mutation-checked**: with the fix removed the test fails). **Memory list state is accepted as lost on a view switch**: the list is deliberately closed until the person opens it (a privacy choice, EBG-0131), so returning to a closed list is the intended state |

**Caveats, disclosed:** a single reviewer with no web access, judging by reading (it cannot run Playwright). The fixes were made after the review and are confirmed by their tests, not re-reviewed before commit; the post-commit review will see them. The test mock was extended to deliver backend notifications, which also removed a class of unhandled-rejection noise in the test log. The Programme Sponsor's first look at the shell in the real Tauri window remains the check on WebView2 rendering.

# 17. WP4a Post-Commit Record (8 October 2026)

WP4a was committed as `b3693cb` after the Programme Sponsor's real approval. **The first two attempts at `submit-response` were refused for a mistake of mine**: the approval is filed under the bridge's work-package name `WP4`, and I had told the Programme Sponsor to approve `WP4a`; the gate held only the earlier `WP4` approval, made before the design commit, and reported the repository as drifted. With `~/approve WP4` it passed. The deterministic pre-check passed every hard check (clean tree, on origin/main, changed files equal Section 15, gated against the parent, pytest 1160 passed and 4 skipped, ruff, validator 0 errors). **CI, correctly read:** the push run (37839937931) ran every job and all succeeded except the informational `playwright-webkit`, which reported 55 passed and 2 failed - the two known microphone tests (a WKWebView difference, WP7). That is the first WebKit run of the new shell: its layout, composer, overflow, font and contrast tests all pass on WebKit. **A mistake of mine, disclosed:** when I first looked at CI I read a Dependabot pull-request run (its macOS, Windows and WebKit jobs are skipped on pull requests), saw them skipped, and passed that wrong statement to the reviewer.

Post-commit review (Antigravity, Gemini, no resumes): **Conditional Pass.** The Guardian heading fix correct; the 17 changed files match Section 15; Sections 13 to 16 consistent. **High:** the use-when-done fix had a hole - the Local AI panel unmounts on a view switch, so a download that finished while the person was on another view did not switch the model until they came back. **Accepted and fixed** (Section 18). **Medium:** the reviewer judged skipping the WebKit job inappropriate; that finding rested on my wrong statement, and the reviewer **withdrew it** when told the real facts.

# 18. WP4a-fix (8 October 2026)

| Item | Result |
|---|---|
| The fix | The app's `jarvis://notification` listener now acts on `ollama.pullFinished` itself: when the finished model is the one the person asked to use (`useWhenDoneRef`, set by the panel when the download starts and cleared on cancel), it calls `ollama_use_model` whichever view is showing, then tells the panel, so the panel's refresh sees the switch. The panel no longer calls `ollama_use_model`; it refreshes and then shows the failure messages ("The download did not finish", and "The model downloaded, but JARVIS could not switch to it") - after the refresh, because refreshing clears the error (found when the first version of the new test failed) |
| Tests | Three new Playwright tests: the switch happens while the person is still on another view (this replaced the earlier test, which only checked it on return); a finished download the person did not ask to use is not switched to; a failed switch is reported. **59 Playwright tests pass** |
| Review (pre-commit) | Antigravity (Gemini, no resumes): **Pass.** It retracted the WebKit finding, confirmed the High resolved, that a finished event is handled exactly once, the reference cleared on cancel and failure, consecutive downloads work, a stale failure message is not shown on a later visit, and the three tests are not vacuous. It raised no Medium or High finding |
| **Not done** | The real Tauri window has still not been looked at by me; the Docker Linux check is skipped (no Python changed) |

# 19. WP4a-fix Commit Contents (expected)

Changed: `src/App.jsx`, `src/LocalAiPanel.jsx`, `tests/e2e/app.spec.js`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

# 20. WP4a-fix Post-Commit Record (8 October 2026)

WP4a-fix was committed as `936949e` after the Programme Sponsor's real `~/approve WP4` (the gate accepted the first submit once the approval was filed under the bridge's work-package name `WP4`). The deterministic pre-check passed every hard check (clean tree, on origin/main, the six changed files equal Section 19, gated against the parent, pytest 1160 passed and 4 skipped, ruff, validator 0 errors). One slip of mine, in the pre-check call and not in the commit: `--eip` takes the file path, not the document number; the first run failed with a file-not-found and was repeated correctly. **CI, selected by commit SHA as the earlier mistake required:** push run 37844187664 ran every job and all succeeded except the informational `playwright-webkit`, which reported 57 passed and 2 failed - the same two known microphone tests (WP7). Post-commit review (Antigravity, Gemini): **Pass**, no findings: the committed tree matches what it reviewed, the six files match Section 19, the commit message is true, Sections 17 and 18 are accurate including the two disclosed mistakes.

# 21. WP4b Build Record (8 October 2026)

| Item | Result |
|---|---|
| The presence Orb | New `src/PresenceOrb.jsx` (Canvas 2D, 240 points, time-based, on the shared clock, device pixel ratio capped at 2, paused while hidden, reduced motion draws one still frame per state and follows the setting live) and `src/orbState.js` (the state priority, the offline rule, the words for each state, the frame budget). It reads nothing from the repository. The knowledge-graph Orb (`GuardianOrbGraph.jsx`) is untouched and stays in the Knowledge view |
| States from real events | Listening: `isRecording`. Thinking: a turn, an escalation or a transcription in flight (a transcription in flight is new state). Speaking: the app records play, end and error of the audio it plays (new: the audio object is held, a newer reply replaces an older one). Offline: the platform call failed, the platform is not Running, the provider is not Online, or the last turn was not answered by a model (cleared by the next success); a failed Claude escalation is deliberately **not** treated as offline, because the local model may be fine. Priority speaking, thinking, offline, listening, idle. While the platform status has not yet arrived the readout says Connecting and the Orb is idle: nothing is known, so nothing is claimed |
| Guardian view | The Orb and its readout (a polite live region: Ready, Listening, Thinking, Speaking, Offline) above the conversation; the composer still pinned at the bottom (tested at 960 x 640 after eight turns, with the disclosure line) |
| AI disclosure and labels | A permanent line above the composer ("You are talking to JARVIS, an AI. Replies come from the AI model on this computer (model).") that adds "Some replies in this conversation came from Claude, over the internet." only after Claude has answered. Each reply carries a label: "On this computer · model", the existing Claude badge with "answered over the internet", or "No AI model answered" for the platform's own messages. A profile that cannot ask Claude can never get a Claude reply, so the word never appears for it |
| Profile switch | New: switching profile clears the on-screen conversation, the draft, errors, any offer and dialog, any audio playing and any recording, and every request that was in flight (send, offer, escalate, transcribe, speak) drops its answer if the profile changed (an epoch counter). A recording in progress still releases the microphone but is never transcribed. **Deliberate limit:** the first profile load (no profile before) does not clear, so a message typed before the profile arrives is kept; a conversation that began with no profile is carried into the first profile selected |
| Backend (item 6.4) | `platform.status` gains `speechAvailable` (new `GuardianRuntime.speech_available`); `guardian.converse` returns `answered` (whether a model produced the reply) and `model` (from the provider's own metadata, only for a model reply). **A difference from the design, disclosed:** the design said `model` only; I added `answered` as well, because a reply can come from a model that names none, and the Orb and the labels must not treat that as a failure. Both additive; tests for each. The frontend does not yet use `speechAvailable`: the honest capability list in WP4c is its reader |
| Tests | **25 new Playwright tests** (the Orb from each real event; the priority; the frame budget; the canvas draws with no repository; reduced motion; the live region; the composer on screen at 960 x 640; the disclosure; the labels; profile switch clearing; a Child screen never mentions Claude; a late answer, late audio, a recording and playing audio at a profile switch; the Medium from the review). **84 Playwright tests pass** (Chromium). Four new backend tests plus two exact-shape tests updated: **1164 passed, 4 skipped** on Windows and **1168 passed** in a Linux container; ruff clean; Vite build clean; validator 0 errors. Mutation-checked: with the profile-switch effect removed, all five profile-switch tests fail; with the speak guard removed, the new speak test fails |
| Test-support changes | The mock gained an `orbMock` option, a fake `Audio`, and now models the backend rule that only an Administrator or Adult may ask Claude (it did not before; the first run of the Child test found this). `animationScheduler.spec.js` now opens the System view first, because the Guardian view's Orb keeps the shared clock running and those tests are about the scheduler alone |
| **Deferred, disclosed** | The Guardian view's side column of what is available (design item 6.2) moves to **WP4c**, where the honest capability list it would show is built. The Orb's measured frame rate and CPU, and the packaged window's look, are WP4d and the Programme Sponsor's own look. The Orb's drawing creates small arrays each frame (the reviewer's Low): at 240 points this is judged tolerable and will be measured in WP4d |
| **Not done** | The real Tauri window has not been looked at by me; the Mac look is at Mac visit 1 |

# 22. WP4b Implementation Review Record

**Review** (Antigravity CLI, Gemini, through `run_reviewer.py`; 8 October 2026, `sender: reviewer`): **Conditional Pass.** It found the five states driven by real events with the required priority, the profile-switch epoch correct on send, offer, escalate and transcribe, the disclosure and labels correct and Claude absent for a Child, the backend change additive, and the two deferrals acceptable. Findings and dispositions:

| Rating | Finding | Disposition |
|---|---|---|
| Medium | `handleSpeak` ignored the profile epoch: audio being made when the profile changed would have played for the next profile | **Fixed**: `handleSpeak` notes the epoch and drops the result (and a failure) if the profile changed; a new test fails with the guard removed |
| Low | `drawOrb` creates arrays each frame | **Accepted**, disclosed in Section 21, to be measured in WP4d |

Re-check of the fix (resume): **Pass.** It confirmed the Medium fixed (the epoch is checked in both the success and failure paths of the speak call) and the new test passing; the Low accepted, no further change.

**Caveats, disclosed:** a single reviewer with no web access, judging by reading; the first review was of the build before the Medium's fix, the re-check covered the fix.

# 23. WP4b Commit Contents (expected)

Changed: `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_guardian_runtime.py`, `jarvis/tests/test_stdio_rpc.py`, `src/App.jsx`, `src/PresenceOrb.jsx` (new), `src/orbState.js` (new), `src/panels.css`, `src/shell.css`, `tests/e2e/animationScheduler.spec.js`, `tests/e2e/app.spec.js`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.
