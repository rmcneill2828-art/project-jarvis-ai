# EIP-ESR0062-002 - Household Safety Follow-ups: Notes, Idle Lock, Backend Hardening

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0062-002 |
| Title | Engineering Implementation Package: WP2 Household Safety Follow-ups - Household Notes Hidden from a Child, Idle Lock, Backend Hardening |
| Version | 0.5 |
| Status | Implemented - committed `765b5f6`; CI green apart from a macOS test defect fixed in the WP3 commit; post-commit review Pass (Copilot, Antigravity) |
| Session | ESR-0062 |
| Work Package | WP2 |
| Risk class | Elevated (changes who sees what, and when a signed-in Adult or Administrator is signed out). Copilot for design; both reviewers for the built result. |

---

# 2. Purpose

Closes the household-safety items [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] Section 6A carried to go-live:

* **EBG-0171, option A** (Programme Sponsor decision at ESR-0062 opening): shared household notes are hidden from a Child.
* **The idle lock** (EIP-ESR0061-006 P4, deferred there; [[WR-ESR0061-002_TECHNOLOGY_AND_SECURITY_LANDSCAPE_REVIEW|WR-ESR0061-002]] F6): an Adult or Administrator left signed in is signed out after a period without use.
* **EBG-0172**, brought forward from go-live WP9: F1 (export, backup and restore paths), F3 (endpoint schemes), F4 (speech text).
* **EBG-0178** (registered with this EIP, folded in at the Programme Sponsor's agreement): the Copilot reviewer's standing rules say which command forms its allow-list accepts.

Also carries the WP1 completion records (ESR-0062 0.3, EIP-ESR0062-001 0.4, PST-0001 3.48), which ride with this WP's commit.

---

# 3. Repository Context Investigated

| Item | Finding |
|---|---|
| Household notes | One function decides: `_sees_household_notes(active)` in `jarvis/interfaces/stdio_rpc.py`, today `active is None or active.role != "Guest"`. It feeds `include_household` at four places: `guardian.converse`, `guardian.escalate`, `memory.list` and `memory.status`. Shared notes are records with `profile_id` None (EBG-0132); only an Administrator may delete one. |
| Signed-in profile | Stored in the identity database (`ProfileStore.set_active` / `clear_active`). `ProfileService.begin_app_session()` (ESR-0061 WP7, F6) already clears an Adult or Administrator session at backend start once a PIN is set; no profile selected is the lowest privilege, moderated as a Guest, and moving up needs the PIN (`pin_required_to_switch`). |
| Screen on a profile change | `App.jsx` clears the conversation, any open offer, recording, playback and in-flight work whenever `activeProfile.id` changes, including to none (WP4b); the memory panel is keyed by profile; views not allowed for the role fall back to the conversation. A lock can reuse all of this by setting the active profile to none. |
| Backend to screen | JSON-RPC notifications on `jarvis://notification` (heartbeat, Ollama pulls). Every request is handled on the backend's main loop (`handle_line`). |
| F1 paths | `profile.export` takes `params.directory`, `memory.backup` an optional `params.backupDir`, `memory.restore` `params.backupPath`; each is used as given. The screens fill them from the native dialog (`SettingsView.jsx`, `MemoryManagementPanel.jsx`). Role checks already apply (Administrator; an Adult for their own export). |
| F3 endpoints | URLs come from environment variables or defaults: Home Assistant (`HomeAssistantClient`), the classifier (`ModerationService`), Ollama (`OllamaSetup`, `PullManager`, `sentinel/ollama_provider.py`). None checks the scheme; `urllib` would open `file://`. |
| F4 speech | `guardian.speak` speaks any text up to 5,000 characters. The screen calls it only from the speak button on a Guardian reply, with that reply's exact text (`response.message` from converse, `result.message` from escalate); nothing else is spoken. |
| Reviewer tooling | `scripts/run_reviewer.py` `TOOL_RULES["copilot"]` names the allowed commands but not their form. At ESR-0062 WP1 post-commit, Copilot was refused every command and recorded no verdict; a re-run with a plain-commands instruction worked. |

---

# 4. Scope

## 4.1 Changes

| # | Item | Change |
|---|---|---|
| **H1** | EBG-0171 option A (revised after the design review's High) | `_sees_household_notes` returns True **only for an Adult or Administrator**, and for the setup state in which **no profile exists at all** (mirroring `_moderation_role`). So a Child, a Guest, and **no profile selected while profiles exist** - the state a restart and the idle lock both leave - never receive a household note in converse, escalate, memory list or memory count. v0.1 left "no profile selected" seeing household notes; the review showed a Child at a locked or freshly started screen could then read them. |
| **L1** | Idle lock: rule | In `ProfileService`: an **Adult or Administrator** session, **once a PIN is set**, is signed out (active profile cleared, as `begin_app_session` does) after **15 minutes** without activity (D-1). Child and Guest sessions are never locked (already the lowest level); with no PIN set nothing is locked (P3). |
| **L2** | Idle lock: activity | Activity is recorded by a new RPC `session.activity`, which the screen sends at most once a minute while a person is using it: on pointer, key, wheel or touch input, **and while recording or playing speech** (so a long read-aloud is not cut off). A successful `profile.select`, and **setting or changing the PIN**, also count. Nothing in the background counts. **The due check runs before an activity is recorded**: a `session.activity` arriving when the session is already due locks it, never revives it. **A missing timestamp is stamped "now" the first time it is seen** (for example an Adult session carried over a restart when no PIN was set, before the PIN is set), so the lock can never fail open. The timestamp lives in memory (a restart already signs out). |
| **L3** | Idle lock: enforcement | Three ways in, one function (`lock_if_idle`), **under a mutex** so the clear and the `profile.locked` notification happen **exactly once** however many threads ask (the main loop, the slow-lane worker and the timer): (a) **before handling every request**, so no request ever runs as an idle Adult or Administrator; (b) a **backend timer**: a daemon thread checks every 5 seconds and sends `profile.locked` when it locks, so the screen locks even when the window is minimised or covered and its own timers are throttled; (c) `session.idleCheck`, which the screen calls when the window **regains focus or becomes visible**, and every 30 seconds while an Adult or Administrator is signed in (never counts as activity). **Elapsed time is the larger of wall-clock and monotonic elapsed**, so a laptop closed for hours is locked on waking (monotonic clocks on Linux and macOS stop during sleep) and a clock set back cannot hold a session open. Both clocks are injectable for tests. A request already running on the slow lane when the lock fires completes; the screen discards its reply through the existing conversation epoch. Recorded as accepted. |
| **L4** | Idle lock: screen | On `profile.locked` (or an `idleCheck` reply saying locked) the screen sets the active profile to none - clearing the conversation and everything in flight through the existing switch path - and shows "Signed out after 15 minutes without use. Choose a profile to continue." Moving back up needs the PIN, as at start. **The clearing effect also runs on a change from none to a profile** (review Low): today it returns early when the previous profile was none, so anything typed with no profile signed in would carry into the next person's conversation. |
| **F1** | Paths (revised after the design review) | One backend check for a caller-supplied path, used by `profile.export`, `memory.backup` and `memory.restore`: the path must be **absolute**; **extended-length and device prefixes** (`\\?\`, `\\.\`) and **UNC paths to this computer** (`localhost`, `127.0.0.1`, this computer's name - which would reach the administrative shares) are refused; it must **exist** (a directory for export and backup, a regular file for restore); the final part must not be a symbolic link or junction (`os.path.islink`, `os.path.isjunction`); the path is resolved with `os.path.realpath`, and **both the given and the resolved path** are tested against the system locations, compared case-insensitively on Windows (`os.path.normcase`) and macOS (case-folded). System locations: Windows - the Windows folder, both Program Files folders, `ProgramData`, and the whole per-user and all-users Start Menu; macOS - `/System`, `/Library`, `/Applications`, `/usr`, `/bin`, `/sbin`, `/etc`, `/private/etc`, `/private/var/db`, and `~/Library/LaunchAgents` (not the whole of `/private`, which holds `/var` and `/tmp` and every temporary folder); Linux - `/etc`, `/usr`, `/bin`, `/sbin`, `/boot`, `/proc`, `/sys`, `~/.config/autostart`. v0.1's ban on a link anywhere in the parents is dropped: it would refuse mapped and `subst` drives, `/var` on macOS and Fedora's `/home`, while the resolved-path test already catches a link into a system location. The default backup folder under the user's JARVIS data folder stays acceptable. A NUL character, an over-long path or any `OSError` becomes a client-facing error naming the reason, never the path. The gap between the check and the write is accepted: the file names written are fixed by JARVIS, so this is defence in depth. The default and environment-configured backup folder are not caller-supplied and are unchanged. |
| **F3** | Endpoints | A shared check: scheme `http` or `https` and a non-empty **hostname**, else refused. Each URL is **checked once, in its builder** in `stdio_rpc.py`, and the checked value reused: a bad one is logged by **variable name only, never its value** (it may hold a user name and password), with the hint "include http:// or https://", and the service is treated as **not configured** - the Home Assistant agent is absent; the classifier is unavailable, which already fails closed for a Child or Guest (`_moderate` returns unchecked when there is no classifier); Ollama setup reports it cannot be reached. The constructors of `HomeAssistantClient`, `ModerationService`, `OllamaSetup` and `PullManager` also refuse a bad URL, as a second line. `sentinel` stays independent of `jarvis` (it is designed for extraction), so `sentinel/ollama_provider.py`, `sentinel/openai_provider.py` and `sentinel/gemini_provider.py` (configurable endpoints) and `sentinel/anthropic_provider.py` (defensive only; its endpoint is not set from the environment) get the same small check inside `sentinel`, refusing the request with a provider error. |
| **F4** | Speech (revised after the design review) | `guardian.speak` speaks only text the backend itself returned in a reply to `guardian.converse` or `guardian.escalate` **for the currently active profile** (or for no profile, which has its own slot) during this run - **every message string returned**, model reply or not (the "not connected" and "not running" notices, an escalation failure's text, a moderation refusal's safe reply). The backend keeps the SHA-256 of up to **500** such replies per profile, in memory, dropped when that profile is erased. Anything else is refused: "Guardian can speak only its own replies." For every role (D-3). |
| **M5** | Activity tracker | `session.activity` and `session.idleCheck` are added to the dispatched methods but **explicitly excluded** from `METHOD_CLUSTERS` in `jarvis/interfaces/activity_tracker.py`, so they never light the Orb or send `knowledge.cluster_activity`; `test_method_clusters_covers_every_dispatched_rpc_method` is changed to allow a named exclusion list (these two) rather than require exact equality. |
| **R1** | EBG-0178 | `TOOL_RULES["copilot"]` gains the command-form rule: one plain command at a time; the git subcommand directly after `git`, with no global options such as `-C` or `--no-pager`; no `cd`, `;`, `&&`, pipes, redirections or environment-variable prefixes; `python scripts/validate_repository.py` takes no arguments; the working directory is the repository root. A small test checks the Copilot rules contain it. |

## 4.2 Programme Sponsor decisions

| # | Question | Recommendation |
|---|---|---|
| **D-1** | The idle time | **15 minutes, fixed in v1.0** (the figure P4 and F6 both named). Making it an Administrator setting is a small follow-on if it proves annoying; an "off" choice is not offered, because a family computer is the case it exists for. |
| **D-2** | F1 approach | **Backend validation** as in F1, rather than moving the file dialog into Rust so the screen never supplies a path. The Rust route is stronger in principle but changes the dialog flow just after `rfd` moved to 0.17, needs the Mac to check, and the review found no way for a child to reach these RPCs in the packaged app (Administrator or Adult only). Backend validation is testable on all three CI platforms. |
| **D-3** | F4 for every role, or only Child and Guest | **Every role**: one rule, no role branching, and the screen's behaviour is identical. |

---

# 4A. Commit Contents

| Area | Files |
|---|---|
| H1, L1-L3, F1, F4 | `jarvis/interfaces/stdio_rpc.py` (household rule, `session.activity`, `session.idleCheck`, the check before every request, the timer thread, speech binding, path checks), `jarvis/identity/service.py` (`lock_if_idle`, activity, mutex, clocks), a new small module for the path and URL checks under `jarvis/shared/` |
| M5 | `jarvis/interfaces/activity_tracker.py`, `jarvis/tests/test_activity_tracker.py` |
| F3 | `jarvis/agents/home_assistant_agent.py`, `jarvis/interfaces/moderation.py`, `jarvis/interfaces/ollama_setup.py`, `sentinel/ollama_provider.py`, `sentinel/openai_provider.py`, `sentinel/gemini_provider.py`, `sentinel/anthropic_provider.py` |
| L2-L4 | `src-tauri/src/lib.rs` (two commands, `session_activity` and `session_idle_check`, registered in `generate_handler!`), `src/App.jsx` (input, recording and playback activity; focus, visibility and 30-second checks; the notification; the signed-out notice; clearing on none to a profile) |
| R1 | `scripts/run_reviewer.py`, its test |
| Tests | New and changed tests in `jarvis/tests/`: household notes for a Child, a Guest, no profile selected (after a lock and after a restart) and no profiles at all; the idle lock with injected wall and monotonic clocks - Adult, Administrator, Child, Guest, no PIN, missing timestamp, PIN set or changed, activity arriving when due, select, the check before every request, the timer, a sleep jump, two threads asking at once (one lock, one notification); path checks with real temporary folders, a junction or link at the leaf where the platform allows, a UNC path to this computer, prefixes, case, each system location, and an ordinary folder accepted; URL schemes in each builder and client, the logged message without the value; speech binding including notices and another profile's reply. `tests/e2e/app.spec.js` and `tests/e2e/accessibility.spec.js`: the new commands stubbed in both mocks; the screen locks on `profile.locked`, clears the conversation and shows the notice; activity sent on input and throttled; no poll with no Adult or Administrator signed in. |
| Records | This EIP; ESR-0062; PST-0001; EBR-0001 (EBG-0171, EBG-0172, EBG-0178 dispositions); REG-0001; EIP-ESR0062-001 0.4 (WP1 completion, already written) |

---

# 5. Evidence Pack

Windows pytest; Linux pytest, ruff and validator in `python:3.12-slim` Docker; `cargo fmt --check`, clippy and `cargo test`; `vite build`; Playwright (Chromium); pip-audit. A manual check on the PC: sign in as an Administrator with a PIN set, leave JARVIS for 15 minutes, confirm it signs out and asks for the PIN to sign back in. The same check joins the Mac visit list (WP4).

---

# 6. Explicitly Out of Scope

* An Administrator-set idle time, or an "off" choice (D-1).
* Moving the file dialog into Rust (D-2).
* Letting an Administrator mark a household note child-visible (EBG-0171 option B, not chosen).
* Any change to Adult or Administrator visibility of household notes, or to Guest behaviour.
* The nine Dependabot pull requests #41 to #49 (session-wide verification, Programme Sponsor decision).
* EBG-0176 camera design (may be drafted later in the session, D22).

---

# 7. Validation Requirements

1. A Child's, a Guest's, and a no-profile-selected (while profiles exist) converse, escalate, memory list and memory count never include a household note; an Adult's and an Administrator's still do, as does the no-profiles-at-all setup state.
2. An Adult or Administrator session with a PIN set is cleared after 15 minutes without activity - by the timer, and before any request once due - including after a sleep; an activity arriving when due locks rather than revives; a missing timestamp cannot hold a session open; Child, Guest and no-PIN sessions are never locked; `session.idleCheck` never counts as activity; `profile.locked` is sent exactly once per lock, however many threads ask.
3. The screen, on a lock, clears the conversation and anything in flight and shows the notice; moving back up needs the PIN.
4. Export, backup and restore refuse a relative path, a missing path, a device or extended prefix, a UNC path to this computer, a link or junction at the leaf, and each listed system location (given or resolved, any case); they still accept an ordinary folder or file the dialog would return, including a temporary folder on macOS and the default backup folder.
5. Each listed client refuses a `file://`, `ftp://` or host-less URL; the app still starts with such a setting, with that service not configured.
6. `guardian.speak` speaks any message the backend returned to the active profile in converse or escalate (model reply or notice) and refuses any other text, including another profile's reply.
7. All existing tests pass, changed only where they assumed a Child sees household notes.

---

# 8. Questions for the Engineering Reviewer

1. Is checking the idle lock before every request, plus a 30-second poll that does not count as activity, sufficient - or does a lock need a backend timer as well?
2. Is "activity = `session.activity` from input, and `profile.select`" the right definition; anything a person does that would not count?
3. Is the F1 check (absolute, exists, no link in the path, not in the listed system locations) sound on Windows, macOS and Linux, including junctions and case-insensitive paths on Windows and macOS?
4. F3: is treating a bad URL as "not configured" at start-up right, rather than refusing to start?
5. F4: is binding speech to the last 50 replies per active profile correct and sufficient; any reply path it would wrongly refuse?
6. H1: should no profile selected also stop seeing household notes? (Answered yes by the design review; v0.2 does so.)
7. Anything rated Medium or higher.

---

# 9. Review Record

**Design review, Copilot CLI (bridge `ESR-0062`/`WP2`, 8 November 2026, `sender: reviewer`): Conditional Pass.** It verified the Section 3 facts against the code: "Design may proceed once H-1 and M-1 to M-6 are folded into v0.2." Each finding and what v0.2 does:

| Finding | Rating | Disposition in v0.2 |
|---|---|---|
| H-1: with no profile selected the backend still returns household notes, and the screen leaves the chat usable then; the lock and every restart land there, so a Child would get household-note text | High | **Accepted**: H1 revised - household notes only for an Adult or Administrator, or with no profiles at all; tests for the locked and restarted states |
| M-1: a lock needs a backend timer (the screen's timers are throttled when minimised); exactly-once needs a mutex across the main loop and slow lane | Medium | **Accepted**: L3 - a 5-second timer thread, focus and visibility checks, one mutex-guarded `lock_if_idle` |
| M-2: a missing timestamp fails open; activity must not revive a due session | Medium | **Accepted**: L2 - stamped at first sight and on PIN set or change; due check before recording |
| M-3: monotonic clocks stop during sleep on Linux and macOS | Medium | **Accepted**: L3 - the larger of wall and monotonic elapsed, both injected in tests |
| M-4: F1 both over-refuses (mapped and subst drives, case, macOS `/private`, Fedora `/home`) and under-protects (UNC admin shares, extended prefixes) | Medium | **Accepted**: F1 rewritten as recommended, adding `ProgramData` and the whole Start Menu; the check-then-use gap recorded as accepted |
| M-5: `METHOD_CLUSTERS` exact-equality test; two e2e mocks; tests for a Child at the none state, the slow-lane race, Rust command registration | Medium | **Accepted**: M5 row; Section 4A and its tests |
| M-6: a 50-reply bound would refuse legitimate speaks (the screen keeps every message), and non-model replies have a speak button too | Medium | **Accepted**: F4 - 500 hashes per profile, every message returned, a no-profile slot, dropped on erase |
| L-1: F3 - log the variable name not the value; check once in the builder; include `sentinel/openai_provider.py`; hostname not netloc; hint to include `http://` | Low | **Accepted** in F3 |
| L-2: count recording and playback as activity; skip the poll with no Adult or Administrator; record the in-flight slow-lane reply | Low | **Accepted** in L2, L3 and the screen tests |
| L-3: the clearing effect skips a change from none to a profile | Low | **Accepted** in L4 |
| L-4: R1 - no git global options, no arguments to the validator, no env prefixes; a test | Low | **Accepted** in R1 |
| Info: D-1 15 minutes and D-2 backend validation acceptable; D-3 agreed | Info | Noted |

---

# 11. Implementation (v0.3)

**Design approved** by the Programme Sponsor, 8 November 2026 (direct chat: "Design Approved"), on v0.2, whose Section 4.2 recommendations stand as the decisions: **D-1** 15 minutes, fixed; **D-2** backend validation; **D-3** the speech rule for every role.

## 11.1 Deviations and clarifications

| # | Item | What was built | Why |
|---|---|---|---|
| 1 | F3, a bad Ollama address | The bad value is **ignored as if unset**, so the default local address (`http://localhost:11434`) is used, with the warning logged by variable name. v0.2 said Ollama setup "reports it cannot be reached" | "Not configured" for Ollama already means the default address; keeping that meaning means the safety checker, which shares the address, keeps working rather than failing closed for every Child and Guest. Home Assistant (absent when unset) and the sentinel providers (refused request) behave as written |
| 2 | L3c, the screen's check | `session.activity` and `session.idleCheck` both return `activeProfileId` (and `idleLockMinutes`); the screen treats any answer naming a different profile from the one it shows as a lock | The same rule as "an `idleCheck` reply saying locked", stated as data: it also catches a session cleared some other way |
| 3 | F1, the folder must exist | As designed. **Nine existing tests** passed a folder that did not exist yet (the old code created it); they now create it first, as the dialog's choice always exists. One test, which checks a refused non-Administrator creates no folder, was left unchanged: the role is checked before the path | Disclosed: test changes, no product change beyond the design |
| 4 | F4, existing tests | Four existing tests spoke text JARVIS had not replied with; they now record the reply first (`_remember_reply`) | Disclosed |
| 5 | Linux portability | The Linux run (Docker) caught the Windows case comparison using `os.path.normcase`, which only lowercases on Windows, so the per-platform test failed on Linux. Fixed to `ntpath.normcase`, which applies Windows rules anywhere | Found before review by the standing Linux check |
| 6 | `realpath` on Windows | An extended-length form returned by `os.path.realpath` is read as the ordinary path before the checks (`_strip_extended_prefix`), so a long but ordinary folder is not refused as a device path | Implementation detail of F1 |

## 11.2 What was built

| Item | Where |
|---|---|
| H1 | `StdioRpcServer._sees_household_notes` (a method now, so it can see whether any profile exists); `HOUSEHOLD_NOTE_ROLES` = Adult, Administrator; the module-level function removed |
| L1-L3 | `ProfileService.lock_if_idle`, `record_activity`, one `threading.Lock`, injectable wall and monotonic clocks, `IDLE_LOCK_SECONDS` = 900; stamped on select, PIN set and PIN change. `StdioRpcServer`: the check at the top of every dispatched request in `handle_line`, a `jarvis-idle-lock` daemon thread every 5 seconds, `session.activity`, `session.idleCheck`, the `profile.locked` notification `{reason, minutes}` |
| L4 | `App.jsx`: input events (pointer, key, wheel, touch) reported at most once a minute; recording and playback reported each minute while they last; checks on focus, on becoming visible and every 30 seconds - all only while an Adult or Administrator is signed in; the notice; the clearing effect now also runs from none to a profile. `shell.css`: `.lock-notice` |
| F1 | `jarvis/shared/safe_locations.py` `checked_user_path`, used by `profile.export`, `memory.backup` (after the role check) and `memory.restore` |
| F3 | `checked_http_url` in the same module; `_checked_env_url` in `stdio_rpc.py` for the Ollama and Home Assistant variables; the four `jarvis` constructors; `sentinel/endpoints.py` `require_http_endpoint` in the Ollama, OpenAI, Gemini and Anthropic providers |
| F4 | `_remembering_reply` wraps `guardian.converse` and `guardian.escalate`; SHA-256 of up to 500 replies per profile (a slot for none); dropped on `profile.erase`; `guardian.speak` refuses anything else |
| M5 | `UNTRACKED_METHODS` in `activity_tracker.py`; the coverage test allows exactly that list |
| R1 | `TOOL_RULES["copilot"]` command-form paragraph; `test_copilot_rules_name_the_accepted_command_form` |
| Rust | `session_activity`, `session_idle_check` commands, registered in `generate_handler!` |

## 11.3 Evidence

| Check | Result |
|---|---|
| New tests | `jarvis/tests/test_household_safety_followups.py`: **83 passed** on Windows (the junction test ran, not skipped), covering every Section 7 item, including eight threads asking at once (one lock, one notification), the backend timer, sleep and clock-set-back, and the logged message without the value |
| Windows pytest | **1545 passed, 4 skipped** (1461 before WP2) |
| Linux (`python:3.12-slim` Docker) | ruff clean; version check agrees; pytest **1544 passed, 5 skipped** (the five Windows-only device-path cases skip); validator 0 errors; pip-audit no known vulnerabilities |
| Rust (Windows) | `cargo fmt --check` clean; `cargo clippy --all-targets -D warnings` clean; `cargo test` 19 passed, 1 ignored |
| Frontend | `vite build` succeeds; Playwright (Chromium) **197 passed, 5 skipped** (192 before; five new idle-lock tests: the lock clears the screen and says why; a lock missed in the background is caught on focus; activity is reported at most once a minute; a Child's screen sends nothing; none to a profile clears the draft) |
| Validator | 0 errors, 311 warnings |
| Manual check on the PC | Not yet run: sign in as an Administrator with the PIN set, leave JARVIS for 15 minutes, confirm the screen signs out and asks for the PIN. Offered to the Programme Sponsor; also on the Mac visit list (WP4) |

## 11.4 Implementation review (v0.4)

**Copilot CLI (bridge `ESR-0062`/`WP2`, 8 November 2026, `sender: reviewer`): Pass**, no High or Medium; it ran pytest (1545 passed), ruff and the validator, and confirmed H1, the idle lock (every request path, the mutex, no revival, no fail-open timestamp), F1 (role before path everywhere), F3 (no start failure, no value logged), F4 and deviation 1 ("acceptable ... cannot send data off the machine"), and that the changes to existing tests are legitimate.

| Finding | Rating | Disposition |
|---|---|---|
| L-1: select, PIN set and PIN change ignored `record_activity`'s result, so a lock in the milliseconds after the request's own check would go unannounced | Low | **Fixed**: those three now only stamp (`_touch`); the request passed the due check just before |
| L-2: the screen compared an in-flight answer with whichever profile was shown when it arrived, so a switch at that moment could show a false sign-out | Low | **Fixed**: an answer is compared only with the profile shown when it was asked (`askSession`) |
| L-3: a UNC path to this computer by LAN address or full name is not detected; the Linux list omits `/lib`, `/dev`, `/run` and home dotfiles | Low | **Accepted**: matches the approved list; the callers are Administrator or Adult only, and F1 is defence in depth |
| L-4: after a backend restart, a Child or Guest screen still showing old replies cannot speak them (the reply memory is in memory only) | Low | **Accepted**: a backend restart without the app restarting is rare (a crash), and the reply can be asked again |
| L-5: no direct test that `guardian.escalate` passes the household rule | Low | **Fixed**: four tests, Child, Guest, Adult, Administrator |
| L-6: two formatting slips in existing tests | Low | **Fixed** |
| Info: a bad Ollama address was logged twice (checked twice) | Info | **Fixed**: checked once and reused |

**Antigravity CLI (second reviewer, after the fixes; same bridge): Pass**, no High or Medium; it ran pytest (1549 passed), ruff and the validator and confirmed items 1 to 7 of its brief, including the concurrency tests and the test adjustments.

**After the fixes:** Windows pytest **1549 passed, 4 skipped**; Linux (Docker) **1548 passed, 5 skipped**, ruff clean, version check agrees, validator 0 errors, pip-audit no known vulnerabilities; Playwright (Chromium) **197 passed, 5 skipped**; `vite build` succeeds; Rust unchanged since the Section 11.3 run.

## 11.5 Approval, commit and post-commit (v0.5)

| Step | Record |
|---|---|
| Built-result approval | **Approved** by the Programme Sponsor through the Sponsor Approval Service on parent `a21984e`; `submit-response ESR-0062 WP2` accepted (8 November 2026, 19:16 UTC), its own pytest and validator run clean. The optional 15-minute manual idle-lock check on the PC was not run; it is on the Mac visit 1 list (WP4) |
| Commit | **`765b5f6`**, 32 files, carrying the WP1 completion records; pushed by the Programme Sponsor |
| CI | Run 42515310482: python, frontend-build, playwright, rust, rust-windows and rust-macos passed. playwright-webkit (allowed to fail) failed the same 5 microphone tests as before WP1. **python-macos failed two new WP2 tests**: they used `/etc` as the system folder, which on macOS is a link to `/private/etc`, so `checked_user_path` refused it with the link message, not the system-folder message the tests expected. The folder was still refused; the tests named the wrong folder. Fixed in the WP3 commit: macOS uses `/usr`, `/USR` and `/Library`, plus a test that `/etc` is still refused |
| Post-commit review | **Copilot Pass** (no High or Medium): the commit is the reviewed tree, 32 expected paths, nothing revealing the private sentence set; the macOS failure a test defect only. Low: CI stays red on python-macos until the WP3 commit lands. Info: note that a link to a system folder reports the link message - it does, because a link at the leaf is refused before any location test, whatever it points to. **Antigravity Pass** (no High or Medium), the same conclusions |

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.5 | 8 November 2026 | Claude Engineering Implementer | Approved and committed (`765b5f6`); CI green apart from a macOS-only test defect (`/etc` is a link there), fixed in the WP3 commit; post-commit review Pass from Copilot and Antigravity (Section 11.5). |
| 0.4 | 8 November 2026 | Claude Engineering Implementer | Implementation review: Copilot Pass (L-1, L-2, L-5, L-6 and an Info fixed; L-3, L-4 accepted), Antigravity Pass after the fixes (Section 11.4). |
| 0.3 | 8 November 2026 | Claude Engineering Implementer | Design approved (D-1 15 minutes, D-2 backend validation, D-3 every role). Built (Section 11): six deviations and clarifications disclosed, including a bad Ollama address falling back to the default and a Linux-only case-folding bug found and fixed before review; evidence on Windows, Linux, Rust and the frontend. |
| 0.2 | 8 November 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot): H-1 accepted (household notes only for an Adult or Administrator, or with no profiles at all); M-1 to M-6 and L-1 to L-4 accepted (backend timer and mutex, fail-closed timestamp, sleep-safe clock, F1 rewritten, activity-tracker exclusion and e2e mocks, F4 bound and scope, OpenAI provider added to F3, command-form detail). |
| 0.1 | 8 November 2026 | Claude Engineering Implementer | Drafted at ESR-0062 WP2: EBG-0171 option A, the idle lock, EBG-0172 (F1, F3, F4) and EBG-0178; three decisions for the Programme Sponsor (idle time, F1 approach, F4 scope). |
