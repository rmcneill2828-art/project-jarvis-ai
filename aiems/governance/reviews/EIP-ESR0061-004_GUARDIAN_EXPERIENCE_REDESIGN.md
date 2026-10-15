# EIP-ESR0061-004 - Guardian Experience Redesign and Presence Orb

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-004 |
| Title | Engineering Implementation Package: WP4 Guardian Experience Redesign and Presence Orb |
| Version | 0.17 |
| Status | Draft - design approved (prototype and decisions W1-W10 as recommended, 8 October 2026), committed 6081425; WP4a committed b3693cb and post-commit reviewed (Conditional Pass, one High fixed in WP4a-fix, one Medium withdrawn); WP4a-fix committed 936949e and post-commit reviewed (Pass); WP4b committed a4bbceb (implementation review Conditional Pass, one Medium fixed; CI green; post-commit review Pass); WP4c committed 247f6da (implementation review Conditional Pass, all findings fixed, then Pass; CI green apart from the informational WebKit job; post-commit review Pass); WP4d built (axe, modal focus, layout on both sizes, Orb frame measurement, the inventory gate), committed b15499d, implementation review Pass, post-commit review Pass; **WP4d-fix** committed 9ab8032 (pre-check PASS, CI green apart from the informational WebKit job, one Claude-dialog test still failing there); **WP4d-fix2** (Tab handled by hand in the dialog; the pre-check's dotfile parsing, at the Programme Sponsor's request) committed da0368e (pre-check PASS, CI green apart from the five known microphone tests in the informational WebKit job, post-commit review Pass). **WP4 is complete** |
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
| 0.17 | 13 October 2026 | Claude Engineering Implementer | WP4d-fix2 post-commit record (da0368e): pre-check PASS, CI green apart from the five known microphone tests, post-commit review Pass. WP4 complete (Section 37). |
| 0.16 | 13 October 2026 | Claude Engineering Implementer | WP4d-fix2 review recorded: post-commit of 9ab8032 Pass, implementation review Pass (Section 36). |
| 0.15 | 13 October 2026 | Claude Engineering Implementer | WP4d-fix post-commit record (9ab8032) and WP4d-fix2: Tab handled by hand in the Claude dialog; pre-check dotfile parsing fixed at the Programme Sponsor's request (Sections 34 and 35). |
| 0.14 | 13 October 2026 | Claude Engineering Implementer | WP4d post-commit record (b15499d, CI green, reviews Pass; pre-check FAIL from a dotfile parsing defect in the script) and WP4d-fix for two WebKit focus failures (Sections 32 and 33). |
| 0.13 | 13 October 2026 | Claude Engineering Implementer | WP4d implementation review Pass (two Info notes dispositioned, Section 31). |
| 0.12 | 13 October 2026 | Claude Engineering Implementer | WP4d built: axe checks on every view (one violation fixed), modal focus for the Claude dialog, layout and screenshots on both sizes, Orb frame measurement, inventory signed off (Sections 29 and 30). |
| 0.11 | 13 October 2026 | Claude Engineering Implementer | WP4c committed 247f6da; pre-check PASS, CI green apart from the informational WebKit job (5 microphone tests, down from 7), post-commit review Pass (Section 28). |
| 0.10 | 13 October 2026 | Claude Engineering Implementer | WP4c implementation review: Conditional Pass (one Medium, rail note named Claude to a Child; fixed) then Pass; reviewer model changed to Gemini 3.8 Flash High (Section 27). |
| 0.9 | 13 October 2026 | Claude Engineering Implementer | WP4c built: role-aware views, honest capability list, Guardian availability column, stale memory list fixed (Sections 25 and 26). |
| 0.8 | 13 October 2026 | Claude Engineering Implementer | WP4b post-commit record: a4bbceb, CI run 37850375579 green, post-commit review Pass (Section 24); Orb test delays replaced by held promises (test support only). |
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

# 24. WP4b Post-Commit Record (13 October 2026)

WP4b was committed as `a4bbceb` ("ESR-0061 WP4b: Presence Orb, AI disclosure and profile-switch clearing") after the Programme Sponsor's approval through the Sponsor Approval Service. **CI, selected by commit SHA:** push run 37850375579, conclusion success. **Post-commit review** (Antigravity, Gemini, 8 October 2026, 22:04:42Z, `sender: reviewer`): **Pass**. The committed tree matches the reviewed tree including the `handleSpeak` epoch guard, the 14 changed files match Section 23, the commit message is true, Sections 20 to 23 are accurate and the counts (25 new, 84 total Playwright tests) are accepted. The evidence pack carried `VALIDATION: PASSED` and a pytest run of 1168 items.

**Test-stability change (uncommitted at the time of this record, WP4c's commit carries it).** Four Orb tests that used a timed mock delay (`sendDelayMs`, `speakDelayMs`) could let a slow runner deliver the answer before the Thinking state was asserted. The mock now holds the call until the test releases it (`holdSend`, `holdSpeak`, `window.__releaseSend`, `window.__releaseSpeak`). Only test support and the tests that used the delays changed; no product code. Re-run on 13 October 2026: the 17 Orb tests pass on Chromium.


# 25. WP4c Build Record (13 October 2026)

Built at the Programme Sponsor's request ("continue ESR-0061", then "yes please" to starting WP4c), under the design approved on 8 October 2026 (Sections 6.5 and 6.7, decisions W1-W10).

| Item | Result |
|---|---|
| Role-aware views | New `src/roles.js` mirrors the backend's role rules (`jarvis/interfaces/stdio_rpc.py`: `ADMINISTRATOR_ROLES`, `REVIEW_APPROVER_ROLES`, `MODEL_MANAGER_ROLES`, `ESCALATION_ROLES`, `_sees_household_notes`). Administrator and Adult see six views; a Child sees Guardian and Memory; a Guest sees Guardian. **No profile selected, or a role the app does not know, sees the conversation only** - a decision of mine, not in the design: the backend refuses most calls without a profile, and showing less is the safe way to be wrong. A view the new role may not use is replaced by the conversation at a profile switch (`currentView`), never left on screen |
| Memory view | The panel is given the role. Administrator: unchanged. Adult: Back Up and Restore shown **disabled with the reason in words** ("Only an Administrator can back up or restore memory."), which is what the backend does. Child: the list is readable; no Delete, no Back Up, no Restore. A shared household note (profile id null) shows Delete only to an Administrator, as the backend requires; an Adult previously saw a button that always failed. Guest has no Memory view |
| Honest capability list | New `src/capabilities.js` (pure, no I/O) builds eight rows - Conversation, AI model on this computer, Claude (over the internet), Memory, Speaking to JARVIS, JARVIS speaking aloud, Agents, Safety gateway - each Ready, Preparing, Not available, Offline or Unknown, from `platform.status`, `ollama_status`, `provider_status`, `list_agents`, `memory_status` and the two voice flags. A read that failed is Unknown. New `src/CapabilityPanel.jsx` shows each state as an icon **and** a word. "Not available yet" names three things that are not built (seeing images or the camera, searching the internet, controlling smart-home devices) and is the only place they appear |
| Static claims removed | `platformStatus.js` is reduced to the `STATUS` words. The three static status cards (including "Core Services: All core services healthy" and "Core platform online", which were never read from anything), the static Capabilities panel ("Placeholder" rows) and the Diagnostics panel ("Interface shell only", "No execution") are gone from the System view, along with "JARVIS v0.1.0, shell edition". The System view is now System Health plus the capability list |
| Guardian view column | The "What is available" column deferred from WP4b: shown from 1100 pixels, hidden below. It lists the local model, speech in and out, and - only for a role that may ask Claude - Claude, and - only for a role with a Memory view - Memory. A Child's screen still never mentions Claude (a test asserts the whole `main` element) |
| **A real defect found and fixed** | The Memory panel kept its opened list when the profile changed, so the next profile on the same screen saw the previous profile's memories until it closed the list. The panel is now keyed by profile (it remounts) and the stored-memory count is read again at a switch. New test |
| Test-support changes | The Playwright mock now defaults to a signed-in Administrator (a role decides which views exist; a test about having no profile passes `profiles: [], activeProfile: null`); an `ollamaFails` option; `animationScheduler.spec.js` installs a minimal profile-only mock so it still reaches a view with no animation. Test changes in `app.spec.js`: the Agents capability assertion moved to the new list; the Child AI-models test now asserts the view does not exist; the disk-space test now makes the recommended model not the one in use (previously both buttons were disabled only because there was no profile) |
| Tests | **97 Playwright tests pass** (Chromium; 84 before, 13 added, one rewritten). Vite build clean. No backend change, so the Python suite is unchanged from WP4b |
| **Disclosed, not done** | (1) The design table's "Change memory sharing with Claude" row has no screen to gate: that UI is the UI half of EBG-0110 in WP5, so it is not built here. (2) A Child can still create a profile (WP6's PIN work); none of this is a security boundary. (3) The packaged window and the Mac look are not seen by me. (4) The WebKit job (informational) has not been run locally; CI will |

# 26. WP4c Commit Contents (expected)

Changed: `src/App.jsx`, `src/Shell.jsx`, `src/MemoryManagementPanel.jsx`, `src/platformStatus.js`, `src/shell.css`, `src/panels.css`, `scripts/run_reviewer.py`, `tests/e2e/app.spec.js`, `tests/e2e/animationScheduler.spec.js`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `src/roles.js`, `src/capabilities.js`, `src/CapabilityPanel.jsx`.

The WP4b close-out records (Section 24, the ESR-0061 0.24 row, REG-0001 sync) ride in this commit under rule A3, and so does the Orb-test stability change in `tests/e2e/app.spec.js`.

# 27. WP4c Implementation Review Record (13 October 2026)

**Reviewer model change, disclosed.** The first run failed at start: Antigravity no longer lists `gemini-3.1-pro-high`, the model named in `scripts/run_reviewer.py`. The only Gemini models it now offers are Gemini 3.8 Flash (Low, Medium, High). The Programme Sponsor chose Gemini 3.8 Flash (High) (chat, 13 October 2026), which keeps PBK-0001's rule (a Gemini model, never a Claude model) but is a smaller model than the one it replaces: **a weaker signal than the earlier reviews, and read as such.** `ANTIGRAVITY_MODEL` was changed, and the `--effort` flag dropped because the level is part of the model name; the 58 reviewer-script tests pass.

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`; 13 October 2026, 08:52:57Z, `sender: reviewer`): **Conditional Pass.** Disclosed deferrals accepted. Findings and dispositions:

| Rating | Finding | Disposition |
|---|---|---|
| Medium | The rail's note "Everything stays on this computer unless you ask Claude." showed to a Child and a Guest; it sits outside `main`, where my test looked | **Fixed**: `NavRail` takes `mentionClaude`, true only when the role may ask Claude; otherwise the note stops at "on this computer". The tests now assert the whole `.app-shell`, and a new test walks Child, Guest and Administrator. **This was a real miss of mine**: the WP4b test and the first WP4c test both scoped the assertion to `main` |
| Low | Four unused role imports in `src/App.jsx` | **Fixed** |
| Low | Dead CSS from the removed status cards, capability stack and diagnostics | **Fixed** (and their selectors in the shared card rules) |
| Low | Agent result, error and busy state were not cleared at a profile switch, and a late agent answer was not dropped | **Fixed**: cleared in the profile-switch effect; `handleInvokeAgent` checks the epoch; new test |
| Info | `scripts/run_reviewer.py` missing from Section 26 | **Fixed** (Section 26 now also lists `src/Shell.jsx` and `src/panels.css`) |
| Info | Unused `STATUS` words | **Fixed** (only the four in use remain) |

**Re-check** (resume, 08:59:08Z): **Pass**, "all five review findings resolved and verified in the working tree." A first attempt to record it was refused by the reviewer's own tool rules (a long message with escaped quotes) and recorded nothing; a second, short message was recorded. The first attempt's text is not in the transcript and is not relied on.

**Caveats, disclosed:** a single reviewer, smaller than before, judging by reading with no browser; Playwright is 99 passed on Chromium; the WebKit job and the packaged window have not been seen.

# 28. WP4c Post-Commit Record (13 October 2026)

WP4c was committed as `247f6da` ("ESR-0061 WP4c: Role-aware views, honest capability list and availability column") after the Programme Sponsor's approval through the Sponsor Approval Service (`submit-response` 09:04:32Z); the push was done by the Programme Sponsor. **Pre-check** (`post_commit_precheck.py`, with `--contents-heading "26. WP4c Commit Contents"`): **PASS** on every hard check - tree clean, on origin/main, the 15 changed files equal Section 26, gated against the parent, pytest 1164 passed and 4 skipped, ruff clean, validator 0 errors.

**CI, selected by commit SHA:** push run 38374093952, conclusion success: `frontend-build`, `playwright`, `python`, `python-macos`, `rust`, `rust-macos` and `rust-windows` all succeeded. The informational `playwright-webkit` job: **94 passed, 5 failed**, against 77 passed and 7 failed on WP4b's run. The two that no longer fail are the Orb Thinking and reduced-motion tests, whose timed mock delays the held-promise change replaced. **The five that remain are all microphone or recording tests** (the two known microphone tests, plus three Orb and profile-switch tests that start a recording): the same WKWebView difference already carried to WP7. It is a test-environment difference until it is seen on the real Mac at visit 1, not a finding about the product.

**Post-commit review** (Antigravity, Gemini 3.8 Flash High, 13 October 2026, `sender: reviewer`): **Pass**, no findings: all 15 changed files match Section 26, the tree is clean, the commit message is true, the records and registers are consistent. Its first run was stopped by its own tool rules on a `git grep -c` (a count it did not need) and resumed. A weaker signal than the Pro-model reviews, as disclosed in Section 27.

# 29. WP4d Build Record (13 October 2026)

Built at the Programme Sponsor's request ("Please start", 13 October 2026), under the design approved on 8 October 2026 (items 6.9 to 6.12). **The one new dependency, `@axe-core/playwright` 4.13.0 (dev only, pinned exactly, published 11 August 2026), was named in item 6.10 of the approved design (rule A4).** One CI change, listed here as A4 asks: both Playwright jobs upload `layout-screenshots/` as an artifact with `actions/upload-artifact` pinned by commit SHA (v4.6.2), `if: always()`.

| Item | Result |
|---|---|
| Accessibility checks (6.10) | New `tests/e2e/accessibility.spec.js`: axe (WCAG 2.0 and 2.1, levels A and AA) on each of the six views as an Administrator, on a Child's Guardian and Memory views, and on every view at 960 x 640; the test fails on any **serious or critical** violation. **One real violation found and fixed:** `scrollable-region-focusable` on the scrolling area of the Knowledge and System views (a keyboard user could not scroll it). The scrolling area is now focusable (`tabIndex=0`) with a visible focus ring inset so it is not clipped |
| The dialog (6.10) | `ClaudeConfirmDialog` was `aria-modal` with no focus handling. Now: focus moves to Cancel (the safe default) on open, Tab and Shift+Tab stay inside, Escape cancels (not while a request is in flight), and focus returns to the control that opened it, however the dialog closes. Three tests |
| Layout on both sizes (6.9) | Every view at 1280 x 820 and 960 x 640: no horizontal overflow, and the composer is in the viewport in the Guardian view; a screenshot of each is written to `layout-screenshots/<project>/` and uploaded by CI (a passing test's attachments are not kept, so a plain attachment would not have survived). Run on the Chromium and WebKit projects; **Playwright's WebKit is not the Mac's WKWebView** (item 6.9) |
| Orb frames (6.11) | Five tests (one per Orb state) behind `JARVIS_PERF=1` (not a CI gate: headless timing is not stable enough to fail a build). **Measured on the household PC, Chromium, the development build, 5 seconds a state: idle 30.0 draws a second, offline 10.0, thinking 60.4, listening 60.2, speaking 60.4; worst gap between animation frames 16.8 ms in every state** (no dropped frame in the window). That meets W3's target of at least 50 frames a second in the active states and holds the frame budget exactly. **Not measured: CPU use** (the target is under 5 percent total CPU while idle) - that is read by the Programme Sponsor in Task Manager on the packaged app, and the Mac at visit 1 and visit 2. The Orb's per-frame array allocation (the WP4b Low) shows no jank at 240 points; it is left as is |
| Inventory gate (6.12) | Table below. **Two rows changed form and are recorded as such:** the Diagnostics panel was removed, not re-pointed (its rows were static text; the real status is in the capability list), and the "Platform, Core Services and External Providers" cards were removed for the same reason. The footer row is met by the System view's lede, which now reads the app version from the shell (`getVersion`) and says times are local; it shows nothing if the version cannot be read |
| Other | `package.json` and `package-lock.json` (the dev dependency), `.gitignore` (`layout-screenshots/`). Tests: **117 passed and 5 skipped** (the five skipped are the Orb frame measurement, run on request) on Chromium; Python 1164 passed and 4 skipped; ruff, validator and the Vite build clean |
| **Disclosed, not done** | CPU use of the Orb (by hand, packaged app); the Mac look and measurements (visit 1 and visit 2); the real WKWebView (Playwright's WebKit stands in, with its five known microphone failures); the axe checks run on the mocked app, so they judge the markup and the contrast tokens, not the packaged window; the confirmation dialog is not itself axe-scanned (its focus behaviour is tested directly) |

**Functionality-preservation inventory, signed off row by row (item 6.12).** Every row has a passing test in its new location:

| Row | Test (tests/e2e/app.spec.js unless noted) |
|---|---|
| Overall platform status chip | "the top bar chip says JARVIS PLATFORM when running, and the platform's state when not"; "...says OFFLINE when the platform call fails". **The chip's connecting state has no test of its own** (a call held open would need a mock option); disclosed |
| Platform, Core Services, External Providers cards; sidebar rows | **Removed as static claims**; replaced by "the capability list is built from real status..." and "a status that cannot be read is Unknown, never Ready" |
| Knowledge Orb with cluster illumination; no-repository case | "a cluster reported active by knowledge.graph's pull field renders as illuminated"; "a cluster with no reported activity renders without the illumination class"; "the Orb draws on its canvas, and does not need a repository" |
| Knowledge Metrics and Active Clusters | "the Knowledge view shows the graph figures" |
| Conversation, send, local reply | "sending a message renders the mocked response in the conversation log" |
| Speak this response | "speak button plays synthesized audio..."; "...shows an inline note when Guardian has no speech provider connected"; "Orb: reply audio playing is Speaking..."; "Orb: audio that errors ends Speaking and says so" |
| Microphone and transcript | "mic button populates the composer with the transcript without auto-sending"; "mic button does not render when transcription is not available"; "...shows an inline note when Guardian has no transcription provider connected" |
| Ask Claude, offers, confirmation, badge | "an offer is shown after a local failure and sends nothing until it is confirmed"; "confirming sends the offer's token once and labels the answer as Claude's"; "Ask Claude opens the confirmation for the last message even after a good local answer"; "every reply is labelled with where it came from" |
| 80 percent warning in the confirmation | "the dialog says when saved memory notes will be sent and warns near the cap" |
| Previous profile's conversation not shown | "switching profile clears the conversation, the draft, the offer, the dialog and the Claude labels" |
| Profile create, switch, active | "profile create form appears when no profile is active..."; "selecting a profile from the picker switches the active profile"; "the active profile is in the top bar with its initial and role" |
| System Health and heartbeat | "app launches and shows JARVIS branding with live system health" and the heartbeat assertion in the System view tests |
| Agent Framework panel | "the Agents view shows no agents when none are registered"; "running an agent renders its real returned payload"; "a denied agent outcome renders inline rather than silently failing" |
| Memory count, show, forget, back up, restore | "memory management panel shows the real stored record count"; "stored memory text is hidden until the list is explicitly opened"; "deleting a memory needs confirmation..."; "backing up memory shows the real returned backup path"; "restoring into a non-empty store requires an explicit overwrite confirmation" |
| "(Household)" marker | "a shared household note carries the (Household) marker" (new) |
| Local AI panel, all of it | the WP3c tests, re-pointed (status, install steps, download, progress, cancel, switch, disk warning, override note, role limits) and "a computer below the usual minimum is told that answers may be slow" (new) |
| Diagnostics panel | **Removed as static text**; replaced by the capability list (as above) |
| Footer: edition, local times | "the System view shows the app version the shell reports, and the local-time note" (new) |
| The 11 controls that did nothing | "the controls that used to do nothing are gone" |

# 30. WP4d Commit Contents (expected)

Changed: `src/App.jsx`, `src/ClaudeEscalation.jsx`, `src/shell.css`, `tests/e2e/app.spec.js`, `package.json`, `package-lock.json`, `.gitignore`, `.github/workflows/ci.yml`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `tests/e2e/accessibility.spec.js`.

The WP4c post-commit records (Section 28, ESR-0061 0.27, REG-0001 sync) ride in this commit under rule A3.

# 31. WP4d Implementation Review Record (13 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`; 13 October 2026, `sender: reviewer`): **Pass.** It found the axe checks real and faithfully mocked with no rule or region excluded, the focusable scroll area and the dialog's trap and focus return correct (the dialog checks that the opener is still connected before restoring focus), the layout tests and artifact upload sound, the frame measurement and version display truthful and permitted, and every inventory row backed by a real test. A single reviewer, smaller than the Pro model of earlier reviews, judging by reading (Section 27's caveat applies). Findings and dispositions:

| Rating | Finding | Disposition |
|---|---|---|
| Info | A count in Section 29 did not match the code (it said eight Orb frame tests; there are five, one per state) | **Fixed** in Section 29 |
| Info | The focusable scroll areas have no accessible name of their own | **Accepted**: each sits inside a section already labelled with the view's name, and axe reports nothing; a second landmark with the same name would repeat it to a screen reader |

# 32. WP4d Post-Commit Record and WP4d-fix (13 October 2026)

WP4d was committed as `b15499d` ("ESR-0061 WP4d: Accessibility checks, modal focus, layout on both sizes and the inventory gate") after the Programme Sponsor's approval through the Sponsor Approval Service (`submit-response` 10:21:35Z); the push was the Programme Sponsor's.

**Pre-check: FAIL on one hard check, and the failure is the script's, not the commit's.** `post_commit_precheck.py` (with `--contents-heading "30. WP4d Commit Contents"`) reported "changed files equal the EIP's Commit Contents - not listed: ['.gitignore']". The commit changed exactly 12 files and Section 30 lists all 12 including `.gitignore`. The cause is `_PATH_TOKEN` (line 35), which only matches a backticked path that ends in a known extension, so an extensionless dotfile is never read as a listed path. The other six checks passed (tree clean, on origin/main, gated against the parent, pytest 1164 passed and 4 skipped, ruff, validator 0 errors). **Not fixed here**: it is a change to a controlled script outside WP4d's approved scope, so it is flagged to the Programme Sponsor for a decision (a one-line change plus a test, WP1c's R8 tooling).

**CI, selected by commit SHA:** push run 38382876635, conclusion success on `frontend-build`, `playwright`, `python`, `python-macos`, `rust`, `rust-macos` and `rust-windows`; both layout-screenshot artifacts were uploaded (`layout-screenshots-chromium` 2.1 MB, `layout-screenshots-webkit` 12.4 MB), so the new upload step works. (Two Dependabot runs share the same SHA and were not mistaken for the push run.) The informational `playwright-webkit` job: **110 passed, 7 failed, 5 skipped.** Five are the known microphone and recording tests. **Two were new and were mine: the Claude dialog focus tests.**

**Cause and fix (WP4d-fix).** Safari and WebKit do not focus a button when it is clicked, so at the moment the dialog opened the focused element was the page body and focus could not return to the opener. A mistake in my design of the return, found only because the job ran: my Chromium-only checks could not see it. The app now records the clicked button (`event.currentTarget`) as `dialogOpenerRef` for the Ask Claude and Review buttons, and `ClaudeConfirmDialog` takes it as `returnFocusRef` and focuses it on close if it is still in the page, else the previous active element. Also fixed, found by running WebKit locally (installed with `npx playwright install webkit`; this PC's Windows WebKit is not the CI Mac's): the four rail assertions read the navigation straight after load, before the profile had arrived, and failed intermittently; they now poll.

**Local results after the fix:** Chromium 117 passed and 5 skipped; WebKit (Windows build) 115 passed, then the two rail failures fixed and re-run with the dialog tests, 8 of 8 passed on both engines; the five microphone tests pass on this PC's WebKit but failed on CI's macOS WebKit, so those five remain a Mac-only difference to be seen at visit 1.

**Reviews** (Antigravity, Gemini 3.8 Flash High, 13 October 2026, `sender: reviewer`, one run): **Part A, post-commit review of `b15499d`: Pass** - the 12 files match Section 30, the tree matches what was reviewed, the commit message is true, and the pre-check failure was verified as the regex limitation. **Part B, implementation review of the fix: Pass** - the opener tracking is safe (connection checks), handles the asynchronous offer, keeps Chromium behaviour, and the polling removes the race. Same caveat as before: a smaller single reviewer, judging by reading.

# 33. WP4d-fix Commit Contents (expected)

Changed: `src/App.jsx`, `src/ClaudeEscalation.jsx`, `tests/e2e/app.spec.js`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

# 34. WP4d-fix Post-Commit Record, and WP4d-fix2 (13 October 2026)

**WP4d-fix `9ab8032`.** Approved through the Sponsor Approval Service (`submit-response` 10:52:49Z); pushed by the Programme Sponsor. **Pre-check: PASS on every hard check**, run on the commit with the working tree stashed so that the uncommitted fix below did not fail the clean-tree check (tree clean, on origin/main, the six changed files equal Section 33, gated against the parent, pytest 1164 passed and 4 skipped, ruff, validator 0 errors). **CI, by commit SHA:** push run 38387211875, success on every job except the informational `playwright-webkit`: **111 passed, 6 failed, 5 skipped** - the five known microphone or recording tests, plus **one of the two dialog tests I added**. The cancel-by-button test now passes (the focus-return fix worked); the Tab and Escape test still fails on CI's macOS WebKit: after Tab, "Send to Claude" was not focused. Cause: Safari and WebKit skip buttons on Tab unless full keyboard access is on, and my trap only acted at the first and last item, so from Cancel the browser's own next stop was outside the dialog. A second mistake of mine in the same dialog, found by the same job. The post-commit review of this commit is part of the single run in Section 34's review paragraph below.

**WP4d-fix2 (two things, working tree).**

1. **Tab inside the dialog is now handled by hand every time** (`src/ClaudeEscalation.jsx`): the handler stops the browser's default, moves to the next or previous focusable item itself with wrap-around, and puts focus on the first or last item if it was outside. It no longer depends on the browser's tab order or the operating system's keyboard setting. The Tab and Escape test passes on Chromium and on this PC's Windows WebKit; **whether it passes on the Mac's WebKit is shown only by the next CI run.**
2. **The pre-check's dotfile parsing, at the Programme Sponsor's request** ("Please fix the pre-check script", 13 October 2026). `_PATH_TOKEN` in `scripts/post_commit_precheck.py` now also reads the extensionless dotfiles `.gitignore`, `.gitattributes`, `.editorconfig`, `.npmrc`, `.nvmrc`, `.prettierrc`, `.eslintrc` and `.dockerignore`, with or without a directory prefix; a bare extension in prose (`.py`, `.env`) is still not a path. Two new tests in `scripts/tests/test_post_commit_precheck.py` (17 pass). Re-running the check against `b15499d`'s Section 30 now passes "changed files equal the EIP's Commit Contents". The scope is exactly the defect; the explicit list is a decision of mine, so a different dotfile named in a later EIP will need adding.

# 35. WP4d-fix2 Commit Contents (expected)

Changed: `src/ClaudeEscalation.jsx`, `scripts/post_commit_precheck.py`, `scripts/tests/test_post_commit_precheck.py`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

The WP4d-fix post-commit record rides in this commit under rule A3.

# 36. WP4d-fix2 Review Record (13 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, 13 October 2026, `sender: reviewer`, one run, `submit-to-review` 11:20:41Z): **Part A, post-commit review of `9ab8032`: Pass** - the six files match Section 33, the commit message is true, Section 34 is accurate. **Part B, implementation review of the working tree: Pass** - the manual Tab wrap-around is safe and correct for Shift+Tab, a disabled button, a single item and focus outside the dialog; Escape still cancels and the container takes focus when the dialog is empty, so there is no keyboard trap; the dotfile pattern has no catastrophic backtracking and no new false positive, the two new tests are real, and an explicit list is acceptable; Sections 34 and 35 are accurate. No findings. Same caveat as before: a smaller single reviewer, judging by reading. **Local results:** `scripts/tests` 223 passed and 2 skipped; Playwright Chromium 117 passed and 5 skipped; the dialog tests pass on this PC's Windows WebKit; **the Mac's WebKit result is shown only by the next CI run.**

# 37. WP4d-fix2 Post-Commit Record (13 October 2026)

`da0368e` ("ESR-0061 WP4d-fix2: Tab handled by hand in the Claude dialog; pre-check dotfile parsing") was approved through the Sponsor Approval Service (`submit-response` 11:44:30Z) and pushed by the Programme Sponsor. **Pre-check: PASS on every hard check, including the file-list check that failed on `b15499d`** - the six changed files equal Section 35, which is the first run with the dotfile fix in place (pytest 1166 passed and 4 skipped, ruff, validator 0 errors). **CI, by commit SHA:** push run 38393036411, success on `frontend-build`, `playwright`, `python`, `python-macos`, `rust`, `rust-macos` and `rust-windows`; the informational `playwright-webkit` job: **112 passed, 5 failed, 5 skipped. The five failures are exactly the known microphone and recording tests; both Claude dialog tests now pass on the Mac's WebKit**, so the Tab fix did what it was meant to. **Post-commit review** (Antigravity, Gemini 3.8 Flash High, 13 October 2026, `sender: reviewer`): **Pass**, no findings - the tree matches what was reviewed, the six files match Section 35, the commit message is true, the records are accurate. A smaller single reviewer, judging by reading.

**WP4 summary.** WP4a (`b3693cb`, `936949e`), WP4b (`a4bbceb`), WP4c (`247f6da`), WP4d (`b15499d`, `9ab8032`, `da0368e`): the shell, the presence Orb, the role-aware views, the honest capability list, the accessibility checks, the modal dialog, the layout checks and the inventory gate, 117 Playwright tests on Chromium. **Still owed, none of it testable here:** Orb CPU use on the packaged app (Task Manager); the Mac look and measurements (visits 1 and 2); the five microphone tests on the Mac's real WKWebView (WP7); the connecting state of the status chip has no test of its own.
