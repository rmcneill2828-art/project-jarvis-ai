# EIP-ESR0062-005 - User Guide, Parents' Guide and the Public "Children and Privacy" Page

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0062-005 |
| Title | Engineering Implementation Package: WP5 User Guide, Parents' Guide, Data Map and the Public "Children and Privacy" Page |
| Version | 1.0 |
| Status | Design approved; built; implementation review Copilot Conditional Pass (addressed), Antigravity Pass; committed `db0f9ef`, post-commit Pass (both); `v0.2.1` released; the page published (21 November 2026) |
| Session | ESR-0062 |
| Work Package | WP5 |
| Risk class | **High-risk** for content (a public statement about a child's data, which Anthropic's terms for serving minors rely on, and which households will act on); low-risk for code (one line of text in one dialog and one test). Copilot reviews the design; Copilot and Antigravity both review the built result and **check every factual claim against the code**. |

---

# 2. Purpose

JARVIS will be used by a household member under 18 (the Child role). Anthropic permits its API to serve minors only with safeguards, one of which is **regulatory compliance documented publicly**. JARVIS's other safeguards (PIN, roles, local moderation, consent, the AI disclosure) were built in ESR-0061; the public document was not. Until it exists, **Claude for a Child stays off** (Programme Sponsor decision, ESR-0061 WP6d).

This package writes the three documents households need, from facts checked in the code:

* **User guide**: installing, first run, profiles, the PIN, local AI, voice, Claude, memory and notes, backups, the idle lock, troubleshooting.
* **Parents' guide**: what a Child profile can and cannot do, what the safety checker does and **what it misses**, consent for Claude, what parents can see and what they cannot, resetting the PIN.
* **"Children and privacy" page**, public: what JARVIS holds about a child, where it is kept, what leaves the computer and when, consent, how long things are kept, how to erase them. It includes a short version written for the child.

And a **data map** (every store JARVIS writes, what it holds, where, how long) that the guides and the page are built from, kept honest by a test.

It closes **EBG-0168**.

---

# 3. Context Investigated

| Item | Finding (from the code, 9 November 2026) |
|---|---|
| Where data lives | Everything under **`~/.jarvis/`** on the user's own computer: `identity/profiles.db` (profiles, the PIN hash, consents, safety events), `memory/personal.db` (notes), `memory/backups/`, `logs/audit.jsonl` and `logs/backend.log`, `settings.json`, `spend.db`, `ollama_model.json`, `models/` (voice, with its `verified.json` record). Profile exports and memory backups go to a folder the person chooses (the backups default to `memory/backups/`). The legacy Tkinter GUI (`jarvis/gui/app.py`) writes transcripts to `~/.jarvis/transcripts`, but it is **not in the installer** (the packaged backend's entry point, `scripts/jarvis_backend_entry.py`, never imports it); the map says so. The Claude key is in the **Windows Credential Manager or the macOS Keychain** (`jarvis/shared/secret_store.py`), never a file. A Home Assistant token, if used, comes from an environment variable, not the keychain. Paths can be moved with `JARVIS_*` variables (a developer feature, mentioned only in the data map). |
| Profiles | `profiles` (with `active_profile`, the one selected now): id, display name, role, created time, whether notes may go to Claude (off by default). No age, birthday, photo or email is asked for or stored. |
| PIN | Only a scrypt hash with salt and lock-out counters (`admin_pin`); never the PIN. `pin_notices`: that the PIN was set or reset, and when. |
| Conversations | **Not saved.** History is kept in memory while the app runs (`jarvis/guardian/cognitive_core.py`, bounded), separately for each profile, and is gone when JARVIS closes or the profile is erased. **The last six exchanges go to Claude with an escalated question** (below). An exported transcript is a file the user chose to save. |
| Notes (memory) | Saved only after the person agrees, kept until deleted. Each agreement is a `consent_decisions` row (capability, decision, time, label, the safety layer's reason), which has no profile column and is **kept** when a profile is erased. Household notes are hidden from a Child and a Guest (ESR-0062 WP2). |
| Safety events | When the safety checker stops something: a category label, input or output, the time, the profile. **Never the text** (`safety_events`). |
| Consent | `child_consents`: which Administrator allowed which scope, when, the child's acknowledgement, revocation (kept as history). `child_disclosures`: when the child said they understood the first-use explanation. |
| Audit log | Events with categories and counts, never content (`sentinel/audit.py`; escalation events "categories and counts, never content"). |
| Retention | Audit log and safety events pruned at **30, 90 (default) or 365 days**, set by an Administrator (`jarvis/interfaces/retention.py`, `jarvis/shared/settings.py`). Backend log rotates at 5 MB, 3 copies. Notes and profiles: until deleted. |
| Erasure | Deleting a profile removes its row, notes, pending proposals, open offers, conversation, consents, disclosure and safety events (`_profile_erase`, ESR-0061 WP5c and WP6). **It does not remove:** `consent_decisions` rows; **earlier memory backup files** (which hold the erased person's notes); **exported profile files** (JSON and Markdown, wherever saved); audit log lines until retention prunes them; the spend ledger (monthly totals, no profile); the Claude key; household notes. The page and the parents' guide say each of these and how to delete them by hand. Profile export gives a person their own data as JSON and Markdown. |
| What leaves the computer | **Ordinary turns: nothing** - answered by Ollama on the same computer. **Claude**: only when JARVIS offers, a permitted person confirms, and the monthly cap has room (`jarvis/interfaces/escalation.py`); then Anthropic receives the question, JARVIS's instructions to the model, and **the profile's last six exchanges** (`DEFAULT_HISTORY_LIMIT`, `ProviderRequest.history`), including turns answered locally, which may hold a name. Notes go only if that profile's "share notes" is on, and **never for a Child** (`sendsMemory` in `stdio_rpc.py`). `src/ChildConsent.jsx` already says this; the page uses the same words. A Child only with a recorded, acknowledged consent, which no one gives until this page is published. **Downloads** (Ollama models from Ollama's registry; voice from GitHub and Hugging Face, with the user agent `JARVIS-voice-setup`) send no personal data, though, like any download, the site sees the computer's internet address. The "Download Ollama" button opens `https://ollama.com/download` in the browser. A developer setting (`JARVIS_OLLAMA_ENDPOINT`) can point the chat model at another computer; the map notes it, and "nothing leaves" is true for the installed defaults. **Home Assistant**, if set up, is on the household's own network. No analytics, crash reporting or update check: verified at build (B4). |
| Safety checker's limits | Measured: original set 20 of 20 unsafe stopped, 19 of 20 safe allowed (ESR-0061 WP6d; again P3 of WP4); replacement set **18 of 20** (WP1: it missed a request for a sexual story and one for a poison). The guide must say plainly that it is not perfect. |
| Signing | Windows installer unsigned (EBG-0146, Deferred): SmartScreen's "More info, Run anyway". Mac ad-hoc signed (D15): System Settings, "Open Anyway". |
| Existing docs | `README.md` is for developers. `docs/` holds only governance. **No user documentation exists.** |
| Public hosting | The repository is **private** (ESR-0062 opening), so nothing in it is public; GitHub Pages from a private repository needs a paid plan. |
| Links in the app | One fixed page can be opened: `open_ollama_download_page` in `src-tauri/src/lib.rs` (a fixed address, the system's opener). There is **no general way to open an arbitrary address**; adding one is a new command and a new permission. |

---

# 4. Scope

## 4.1 Documents (G)

| # | Document | Where | Contents |
|---|---|---|---|
| **G1** | Data map | `docs/user/DATA_MAP.md` | One row per store in Section 3, **tables, files, folders, the keychain entry and every network destination**: what it holds, for whom, where on Windows and on macOS, how long, how it is erased (and what erasing a profile leaves), whether it ever leaves the computer. The source for G2 to G4. |
| **G2** | User guide | `docs/user/USER_GUIDE.md` | Install (SmartScreen, Gatekeeper, the checksums); first run; profiles and roles; the Administrator PIN; local AI models; voice; Claude (key, monthly cap, confirmation, what is sent); notes; export, backup and restore; the idle lock; troubleshooting (Ollama not running, voice damaged, the microphone refused). |
| **G3** | Parents' guide | `docs/user/PARENTS_GUIDE.md` | The Child role (what it can and cannot do); the safety checker, **with its measured misses**, and why it does not replace a parent; household notes hidden; the AI disclosure; Claude for a Child: off by default, consent and how to revoke it; what parents can see (safety event labels, never the words) and cannot; resetting a forgotten PIN; deleting a child's data. |
| **G4** | Children and privacy | `docs/user/CHILDREN_AND_PRIVACY.md`, published as the public page (D-1) | "The short version" for the child (plain words, a few lines); then for parents: who is responsible (the household runs JARVIS; the developer receives nothing); what is collected; where it is kept; what leaves the computer, when and to whom: **Anthropic as the service that answers Claude questions**, what it receives (the question, the last six exchanges, never a Child's notes), that it is outside the UK, its retention and training use as read from its own policy on the day (B5), linked; Claude off for a Child by default and needing an Administrator's consent and the child's own acknowledgement; consent and **withdrawing it** (what stops, what stays); what a parent can see (safety labels) and cannot (the words); retention periods; erasure, **what erasing leaves** and how to remove it; export; the safety checker's limits; who is responsible for the data in a household (the household, which runs JARVIS; the developer receives nothing); a person's rights and the **ICO** as the place to complain; contact (D-2). It does **not** say "compliant" or name a lawful basis (D-3). The short version for the child uses simple words and says what a grown-up can see. Dated, with a version. |

Plain English throughout; no claim without a row in the evidence table (Section 5). No legal conclusions: the page states facts (D-3).

## 4.2 Code (L)

| # | Change | Detail |
|---|---|---|
| **L1** | The page's address in the consent dialog | One constant for the address. In `src/ChildConsent.jsx`, where an Administrator records consent for a Child to ask Claude, one line: "Read Children and privacy before you agree:" and the public address as **selectable text** (not a link: the app has no general way to open an address, and adding one is out of scope). A Playwright check that the line is there. |
| **L2** | Data map test | `jarvis/tests/test_data_map.py`: every `CREATE TABLE` and `ALTER TABLE ... ADD COLUMN` in `jarvis/` and `sentinel/`; every `*_FILENAME`, `*_DIRNAME` and default path constant; and **every `https://` host in `jarvis/` and `src-tauri/src/`** (outside tests) appears in `DATA_MAP.md`. A new store, column or destination cannot be added without the map. Writes through `open(`, `write_text` or `sqlite3.connect` are covered by B1, not the test. |

## 4.3 Programme Sponsor decisions

| # | Question | Recommendation |
|---|---|---|
| **D-1** | Where the public page lives | **A new public repository holding only the page, served by GitHub Pages** (free for a public repository): it is public, it costs nothing, and it keeps the code private. It holds only the page (no copy of this repository's history), no custom domain, the version and date on the page, and the published file's SHA-256 recorded here against `CHILDREN_AND_PRIVACY.md`, which stays the source. You create the repository (an outward-facing step); I write the page and its `index.html`; you push. Alternatives: making this repository public (exposes all governance and history); a paid GitHub plan (no budget); the page only inside the app (not public, so it does not meet the requirement). |
| **D-2** | Contact on the page | **The public repository's Issues**, so no personal email or name of a household member is published (D23, data minimisation). The page names the publisher as "the JARVIS developer", says Issues need a free GitHub account, and warns **never to post a child's or anyone's personal details** there. Issues can be closed later without changing the page. |
| **D-3** | Legal review | The page states facts only. Whether a UK household's own use of JARVIS needs anything more under UK GDPR or the ICO Children's Code is a **legal question I cannot answer**; The page therefore does not claim compliance or name a lawful basis. I recommend you decide whether to seek advice before other households use JARVIS (go-live, Session D), not before your own household does. |
| **D-4** | Turning on Claude for a Child | **Not part of this package.** Publishing the page removes the blocker; turning it on stays your separate decision, recorded when you make it. |

---

# 4A. Commit Contents

| Area | Files |
|---|---|
| Documents | `docs/user/DATA_MAP.md`, `USER_GUIDE.md`, `PARENTS_GUIDE.md`, `CHILDREN_AND_PRIVACY.md` |
| Code | `src/ChildConsent.jsx` (L1); `tests/e2e/` (one check); `jarvis/tests/test_data_map.py` (L2) |
| Public page | Built from `CHILDREN_AND_PRIVACY.md` into the public repository (D-1), pushed by the Programme Sponsor; its address goes into L1 and the page's version into this EIP |
| Records | This EIP; ESR-0062; PST-0001; REG-0001; EBR-0001 (EBG-0168 Completed on publication) |

---

# 5. Evidence Pack

An **evidence table** in this EIP: every factual sentence in G2 to G4, the file and line it comes from, checked by both implementation reviewers. The B-steps at build:

| # | Check |
|---|---|
| **B1** | Every store on a real run: start JARVIS with a fresh `~/.jarvis`, use every feature once, then list and diff every file written; each is in the map |
| **B2** | Profile erasure: delete a Child profile with consent, notes and safety events; nothing of it remains in either database **except what Section 3 says stays** (consent decisions, earlier backups, exports, audit lines until pruned), each confirmed and described exactly |
| **B3** | Conversations not saved: after a conversation and a restart, no file holds its words |
| **B4** | Network: outbound connections during an ordinary turn and at start-up (Windows `Get-NetTCPConnection` for the backend's process): Ollama on localhost only; no analytics or update check |
| **B5** | Anthropic's API data retention and use, read from its live policy pages on the day, linked, not paraphrased beyond what they say |
| **B6** | Validator, pytest, Playwright, the Linux check |

---

# 6. Explicitly Out of Scope

* Opening web pages from the app (an opener plugin): a new dependency and permission.
* Translating the documents.
* Code signing (EBG-0146 stays Deferred; G2 documents the warnings it causes).
* Go-live WP8's other items, left for Session D: smoke gates (EBG-0133), coverage (EBG-0151), the engineering documents (EBG-0011, EBG-0040, EBG-0061). None is a user document.
* Turning on Claude for a Child (D-4) and any legal advice (D-3).
* Changing what JARVIS stores. If B1 to B4 find a store or a connection that should not exist, it is registered as its own EBG and the page describes what is true.

---

# 7. Validation Requirements

1. Every claim in G2 to G4 has an evidence row; both reviewers checked them against the code.
2. B1 to B5 done and recorded; anything unexpected registered as an EBG.
3. L2's test passes and fails when a table is added that the map lacks.
4. The public page is reachable without signing in, matches `CHILDREN_AND_PRIVACY.md`, and names no household member.
5. L1 shows the published address.
6. The validator, pytest, Playwright and the Linux check pass.

---

# 8. Questions for the Engineering Reviewer

1. Does Section 3 miss any store, or anything that leaves the computer?
2. Does G4 cover what Anthropic's "regulatory compliance documented publicly" requires for minors?
3. Is D-1 the right way to make the page public with a private repository and no budget?
4. Is L2 a sound guard against the map going stale?
5. Anything rated Medium or higher.

---

# 9. Review Record

**Design review, Copilot CLI (bridge `ESR-0062`/`WP5`, 9 November 2026, `sender: reviewer`): Conditional Pass**, no High, five Medium. It confirmed as true: conversations not saved; safety events and the audit log hold no text; the spend ledger holds month totals; the PIN is a scrypt hash; retention prunes the audit log and safety events only; household notes are hidden from a Child and a Guest. Each finding and what v0.2 does:

| Finding | Rating | Disposition in v0.2 |
|---|---|---|
| M1: Claude also receives the instructions and the profile's last six exchanges, including local turns and a name typed in them | Medium | **Accepted**: Section 3; G4 says it in the consent dialog's words |
| M2: a Child's notes are never sent, whatever "share notes" says | Medium | **Accepted**: Section 3 and G4 |
| M3: erasure leaves consent decisions, earlier backups, exports, audit lines until pruned, the spend ledger, the key, household notes | Medium | **Accepted**: Section 3 lists each; G1, G3 and G4 say how to remove them; B2 confirms each |
| M4: the app can open one fixed page (Ollama's download page), which is also a destination | Medium | **Accepted**: Section 3 corrected; L1 stays text, as no general opener exists |
| M5: the map missed `active_profile`, `pin_notices`, `verified.json`, exports, the legacy transcripts folder, the Home Assistant token | Medium | **Accepted**: Section 3; the legacy GUI is not in the installer (checked: the sidecar's entry point never imports it), and the map says so; B1 diffs the real folder |
| Low: `JARVIS_OLLAMA_ENDPOINT` can point at another computer | Low | **Accepted**: a developer-setting note in the map |
| Low: downloads show the computer's internet address | Low | **Accepted**: Section 3 and G4 |
| Low (confirmed): moderation and a child's name stay on the local model | Low | No change |
| Q3: G4 should cover Anthropic as processor, outside the UK, retention and training use, withdrawing consent, what a parent can and cannot see, deletion, the ICO; not say "compliant" | - | **Accepted**: G4 and D-3 |
| Q4: D-1 docs-only, no custom domain, no private history, version and date, a hash check; D-2: Issues need an account and invite posting personal data | - | **Accepted**: D-1 and D-2 |
| Q5: L1's address a testable constant; L2 also for added columns, folders and network hosts | - | **Accepted**: L1 and L2 (writes in general by B1) |

---

# 11. Build (v0.3)

**Design approved** by the Programme Sponsor, 9 November 2026 (direct chat: "Approved - 1. Agreed, 2. Agreed 3. None needed 4. Agreed"), on v0.2: **D-1** a separate public repository with GitHub Pages, under the conditions in Section 4.3; **D-2** contact through its Issues, with the account note and the warning; **D-3 no legal advice is needed** (the Programme Sponsor's decision; the page still states facts only and claims no compliance); **D-4** turning on Claude for a Child stays a separate decision.

## 11.1 Findings in build, and the Programme Sponsor's decisions (9 November 2026)

Running B1-B4 against the real backend, and reading the code for the guides, found three things the page could not truthfully describe as they were. Each was put to the Programme Sponsor as scope expansion, with a recommendation (PBK-0001 scope-creep rule).

| # | Finding | Decision | What was done |
|---|---|---|---|
| F1 | **Erased data stayed in the files.** After erasing a profile, no row held its note or name, but both were still in the raw bytes of `personal.db` and `profiles.db`: SQLite marks a deleted row's space free without overwriting it (`secure_delete` 0), and the databases run in WAL mode, so older page copies can also sit in the `-wal` file | **1A**, fix in WP5 | `PRAGMA secure_delete = ON` on every connection (`jarvis/shared/schema_migrations.connect`, the single connection point); a new `scrub()` (VACUUM, then `wal_checkpoint(TRUNCATE)`) run after a profile erasure (both databases) and after a note deletion, which also clears residue deleted before the fix. A failure is logged, never raised: the deletion is already committed. Tests: `jarvis/tests/test_erasure_scrub.py` (4) |
| F2 | **No PIN reset on an installed copy.** `python -m jarvis.tools.reset_admin_pin` and `add_administrator` need Python and the source; the packaged backend had only the voice checks | **2A**, fix in WP5 | `--reset-admin-pin` and `--add-administrator "Name"` on `scripts/jarvis_backend_entry.py`, calling the same tools' `main()`, so the same rules hold (run on the computer, never from the app; the reset notice for the next Administrator; an Administrator is added only when there is none). Tests: `jarvis/tests/test_packaged_recovery.py` (3, run through the entry script) |
| F3 | **The installed app cannot save a note.** `src-tauri/src/` never calls `memory.propose`, `memory.approve` or `memory.deny`, and never has | **A**: write the guides and page to what the app does; register a backlog item | **EBG-0180** registered. The guides and page say this version does not save new notes from the app. The in-app text that promised it was corrected: `src/SettingsView.jsx` (`PrivacyNotice`) and the Memory view's lede in `src/App.jsx` |

**The page's repository (D-1):** created by the Programme Sponsor, 9 November 2026: `rmcneill2828-art/AI-Project`, public, empty, Issues on. The page's address will be `https://rmcneill2828-art.github.io/AI-Project/`. The account name was already public through the main repository. Pages is turned on after the first push (Settings, Pages, deploy from `main`, root).

## 11.2 B-step results (9 November 2026)

Run with `python -m jarvis --ipc-stdio` against a fresh data folder (every `JARVIS_*_PATH` and `JARVIS_LOG_DIR` pointed at it), driving profiles, the PIN, conversations as an Administrator, an Adult and a Child, notes, consent, a backup, an export, an erasure and a restart. Network calls recorded by a Python audit hook on `socket.connect` and `socket.getaddrinfo` inside the backend process (the venv launcher starts a child process, so `netstat` on the launcher's id saw nothing; the hook sees every connection, however short).

| # | Result |
|---|---|
| B1 | Files written: `identity/profiles.db`, `memory/personal.db`, `memory/spend.db`, `memory/backups/*.json`, `logs/audit.jsonl`, `logs/backend.log`, the export's `.md` and `.json`. Every one is in the map |
| B2 | Before the F1 fix: every row of the erased Child and Adult gone, but the note text and the name still in the raw bytes of both databases. **After the fix: neither the name nor the note is anywhere in either database file**; they remain only in the backups made before the erasure and the export, as the map says. `consent_decisions` rows kept (no name, no text) |
| B3 | The words used only in conversation are in no file, not in `backend.log`, and not in Ollama's own `server.log` |
| B4 | The only connections: `localhost` lookups and `::1:11434` (Ollama on the same computer). No other host |
| B5 | Anthropic's pages read on 9 November 2026: retention ([privacy.claude.com, 7996866](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), updated 1 July 2026) and training ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)), quoted in DATA_MAP Section 6. ICO pages checked to exist: [make a complaint](https://ico.org.uk/make-a-complaint/), [your right to get your data deleted](https://ico.org.uk/for-the-public/your-right-to-get-your-data-deleted/) |
| B6 | See Section 11.4 |

An earlier note that a harmless sentence had been wrongly stopped during this run was withdrawn: the stop came while the safety checker was still loading, so it is not a measurement and is not in any guide.

**D-1's premise, corrected:** D-1 assumed this repository is private. It is public (`rmcneill2828-art/project-jarvis-ai`). The separate page repository still gives a page with no history or code beside it; the page links to the data map in this repository.

**The Windows path in the PIN-reset command** was read from Tauri's own NSIS template (`crates/tauri-bundler/src/bundle/windows/nsis/installer.nsi`, branch `dev`): with the default `currentUser` install mode, `$INSTDIR` is `$LOCALAPPDATA\${PRODUCTNAME}`, and external binaries are copied into it under their name without the target triple. `tauri.conf.json` sets no install mode, so the default applies. The guide says it is the usual folder.

## 11.3 Evidence table

Every factual claim in G2 to G4, and where it comes from. G1 (the data map) is itself checked by B1 to B4 and by `test_data_map.py`. "UG", "PG" and "CP" are the user guide, the parents' guide and Children and privacy, by section.

| Claim | In | Source |
|---|---|---|
| Release file names, `.sha256` beside each | UG 1 | `gh release view v0.2.0` assets |
| Not signed: SmartScreen "More info, Run anyway"; macOS "Open Anyway"; macOS 13 minimum | UG 1 | Go-live decision D15 (EIP-ESR0062-004 Section 3, "Signing") |
| Ollama needed; a button opens its download page | UG 1, 11 | `src/LocalAiPanel.jsx` ("Ollama is not installed..."); DATA_MAP Section 6 (`https://ollama.com`) |
| First-run steps; the first profile is the Administrator; only a name is asked | UG 2 | `src/FirstRun.jsx` `STEPS`, `ProfileStep`; `jarvis/identity/store.py` `profiles` columns |
| Until a PIN is set the rules are not enforced; anyone can switch to any profile | UG 2, PG 1 | `src/AdminPin.jsx` `NO_PIN_WARNING` |
| PIN 6 to 12 digits; scrypt hash | UG 2, 4 | `jarvis/identity/admin_pin.py` `PIN_PATTERN`, `hashlib.scrypt` |
| Only an Administrator adds a profile, once a PIN is set | UG 3 | `src/AdminPin.jsx` `PinExplanation`; `src/SettingsView.jsx` `canChangeHouseholdSettings(role) && <AddProfileSection` |
| Role table: models and voice Administrator and Adult | UG 3, PG 2 | `stdio_rpc.py` `MODEL_MANAGER_ROLES`; `src/VoicePanel.jsx` header comment |
| Role table: Claude: Administrator and Adult; Child with consent and acknowledgement; Guest never | UG 3, 7; PG 5; CP | `src/SettingsView.jsx` `PrivacyNotice`; `stdio_rpc.py` `CLOUD_NOT_PERMITTED_MESSAGE`; `src/ChildConsent.jsx` |
| Household notes: Adult and Administrator only | UG 3, PG 2, CP | `stdio_rpc.py` `_sees_household_notes` |
| Export: own (Adult), any (Administrator), not Child or Guest | UG 3, 9; PG 2 | `test_profile_data_rights.py` (`test_an_adult_can_export_only_their_own_data`, `test_a_child_or_guest_cannot_export`) |
| Backup, restore, erase, safety events, the Claude key, note sharing: Administrator only | UG 3, 7, 9; PG 6; CP | `stdio_rpc.py` `_memory_backup`, `_memory_restore` ("Only an Administrator profile can restore memory."), `_profile_erase`, `_safety_summary`, `_claude_key_manager`, `_profile_set_cloud_memory` |
| Switching to an Administrator needs the PIN; so does leaving a Child or Guest for an Adult | UG 3, PG 2 | `jarvis/identity/service.py` `pin_required_to_switch` |
| 5 wrong tries lock 30 s, doubling each further 5, up to 10 minutes; the next Administrator is told | UG 4 | `admin_pin.py` `TRIES_PER_BATCH`, `FIRST_LOCK_SECONDS`, `MAX_LOCK_SECONDS`; `pin_notices` |
| Idle lock: 15 minutes, Adult and Administrator, once a PIN is set | UG 4 | `identity/service.py` `IDLE_LOCK_SECONDS`, `IDLE_LOCK_ROLES`, `lock_if_idle` docstring |
| The PIN is a lock inside JARVIS, not on the computer's files | UG 4, PG 1 | `src/AdminPin.jsx` `PinExplanation` |
| PIN reset and add-Administrator from the installed backend; notice to the next Administrator; refuses a second Administrator | UG 4, PG 7 | `scripts/jarvis_backend_entry.py`; `jarvis/tools/reset_admin_pin.py`; `jarvis/tools/add_administrator.py`; `test_packaged_recovery.py` |
| Backend paths: macOS `Contents/MacOS/jarvis-backend`; Windows `%LOCALAPPDATA%\JARVIS Guardian Shell` | UG 4 | EIP-ESR0062-004 Section 3 ("The app"); Section 11.2 above |
| Local AI screen: status, recommendation, download and switch; the safety checker downloaded there | UG 5, PG 1 | `src/LocalAiPanel.jsx` ("Download safety checker") |
| Without the safety checker a Child or Guest gets no answers; the fixed "can't check" replies | UG 5, 11; PG 1, 4; CP | `jarvis/interfaces/moderation.py` docstring (fail closed, M3), `UNAVAILABLE_TEXT` |
| Voice: Kokoro and Whisper, once, by an Adult or Administrator, from GitHub and Hugging Face; speech on the computer | UG 6 | `src/VoicePanel.jsx`; `jarvis/interfaces/voice_setup.py` (`User-Agent: JARVIS-voice-setup`); DATA_MAP Section 6; B4 |
| The Claude key in Credential Manager or Keychain; **Remove key** | UG 7 | `jarvis/shared/secret_store.py`; `src/SettingsView.jsx` `ClaudeKeySection` |
| When Claude is offered; the Ask Claude button; nothing sent until confirmed; the Claude label | UG 7 | `src/ClaudeEscalation.jsx` `OFFER_TEXT`, `EscalationBar`, `ClaudeBadge` |
| What is sent: question, instructions, last six exchanges; notes only if sharing is on; never a Child's | UG 7, PG 5, CP | `jarvis/guardian/cognitive_core.py` `DEFAULT_HISTORY_LIMIT = 6`; `src/ChildConsent.jsx` `PARENT_EXPLANATION`, `CHILD_ACKNOWLEDGEMENT`; `identity/service.py` `CLOUD_MEMORY_SHARING_ROLES` |
| Model Claude Sonnet 5.5 | DATA_MAP 6 | `stdio_rpc.py` `DEFAULT_CLAUDE_MODEL` |
| Monthly allowance £30 by default; shown before confirming; refused when used up | UG 7, 11 | `stdio_rpc.py` `DEFAULT_CLAUDE_CAP_GBP`, "The monthly allowance for asking Claude has been used up." |
| This version cannot save a new note | UG 8, PG 6, CP | Finding F3 (Section 11.1); EBG-0180 |
| A note, when saving exists, needs an Adult's or Administrator's approval | PG 6, CP | `stdio_rpc.py` `_memory_approve`, `REVIEW_APPROVER_ROLES` |
| Export is Markdown and JSON with notes and household-safety records | UG 9, CP | `test_an_export_holds_the_profiles_own_notes_and_nothing_else` |
| Restore asks before replacing existing notes | UG 9 | `PersonalMemoryService.restore_backup` (`confirm_overwrite`); `src/MemoryManagementPanel.jsx` |
| Erase: typed name; what it removes; overwritten in the files; what it leaves | UG 9, PG 8, CP | `stdio_rpc.py` `_profile_erase`; finding F1; `test_erasure_scrub.py`; B2 |
| Activity log: never what was said; 30, 90 (default) or 365 days | UG 9, PG 6, CP | `jarvis/shared/settings.py` `ALLOWED_RETENTION_DAYS`, `DEFAULT_RETENTION_DAYS`; `src/SettingsView.jsx` `PrivacyNotice`; B3 |
| Uninstalling leaves `~/.jarvis` | UG 10 | DATA_MAP Section 7 (the installer does not touch the home folder) |
| Voice error messages; microphone permission | UG 11 | `src/VoicePanel.jsx` |
| "Before you start" explanation, its content | PG 3, CP | `src/ChildDisclosure.jsx` `CHILD_DISCLOSURE` |
| Child-friendly instructions; first name used; never sent to Claude | PG 3, CP | `moderation.py` `CHILD_SAFETY_LAYER`, `CHILD_NAME_LINE` |
| Message checked before JARVIS sees it, answer before the child does; Child and Guest | PG 3, 4; CP | `moderation.py` docstring, `MODERATED_ROLES` |
| Llama Guard 3 by Meta, on the computer; kinds of harm | PG 4, CP | `moderation.py` `DEFAULT_CLASSIFIER_MODEL`, `CATEGORY_LABELS`; `src/ChildrenSafety.jsx` |
| The fixed replies, Childline 0800 1111, 999 | PG 4 | `moderation.py` `BLOCKED_GENERAL_TEXT`, `BLOCKED_SELF_HARM_TEXT` |
| Two 40-sentence sets: the first 20 of 20 harmful stopped (7 and 9 November 2026); the second 18 of 20, missing a sexual story and a poison question (8 November 2026); 1 harmless wrongly stopped on each | PG 4, CP | EIP-ESR0061-006 Section 10 (WP6d, 7 November 2026); EIP-ESR0062-004 Section 11, P3 (9 November 2026, the first set, D-4); EIP-ESR0062-001 Section 11.3 (the second set, 8 November 2026) |
| Judges harm, not age | PG 4, CP | `moderation.py` docstring (M2) |
| Claude for a Child: off by default, per child; the child's "I understand"; off at once; history kept; off if the allowing Administrator is no longer one | PG 5, CP | `src/ChildConsent.jsx` `PARENT_EXPLANATION`, `statusText`; DATA_MAP Section 1 `child_consents` |
| What a parent sees: per profile, by day, category and message or answer, counts | PG 6, CP | `identity/service.py` `safety_summary`; `safety_events.py` `daily_counts` |
| Conversations held while open, gone on closing, not saved | PG 6, CP | `src/SettingsView.jsx` `PrivacyNotice`; B3 |
| No accounts, analytics, crash reports or update check; the developer receives nothing | CP | B4; DATA_MAP Section 6 ("Not contacted") |
| Ordinarily nothing leaves; checked on a real run | CP | B4 |
| Anthropic: US; 30 days; up to 2 years if flagged; no training on Customer Content | CP | B5 |
| Downloads: the site sees the computer's address | CP | DATA_MAP Section 6 |
| UK rights to a copy and deletion; the ICO; complaints | CP | B5 (ICO pages) |
| Contact through the page repository's Issues; account needed; posts are public | CP | D-2; Section 11.1 (the repository) |

## 11.4 B6 checks (9 November 2026)

| Check | Result |
|---|---|
| Validator | 0 errors, 312 warnings (baseline 311; the extra one was this section's forward reference, now resolved) |
| pytest, Windows | 1,609 passed, 6 skipped (new: `test_erasure_scrub.py` 4, `test_packaged_recovery.py` 3, `test_data_map.py` 5); `test_packaged_recovery.py` 4 after the Antigravity Low (Section 11.7) |
| Linux, `python:3.12-slim` in Docker, CI's Python steps | `ruff check` clean; `sync_product_version.py --check` agrees (0.2.0); pytest 1,609 passed, 6 skipped; validator 0 errors; `pip-audit` no known vulnerabilities |
| Playwright (Chromium) | 202 passed, 5 skipped, including the L1 check |
| `npm run build` | Built |
| The remanence fix on the real backend | B2 re-run after F1: the erased name and note in neither database file |

## 11.5 Implementation review: Copilot (9 November 2026)

**Conditional Pass** (`.aiems-exchange/reviewer/outbox/20261109T210742Z-return-findings.md`). It confirmed F2's trust model (the app starts the backend with no arguments and grants no shell permission, so neither the app nor a child in it can reach the options), F1's reasoning for erasure and note deletion, and every evidence-table row it checked. It could not run pytest or open Anthropic's pages (permission refused).

| Finding | Severity | Disposition |
|---|---|---|
| H1: the guides and page say 0.2.0, but the `v0.2.0` release predates WP5, so its installer has neither the overwrite on erasure nor the recovery options the guides describe | High | **Accepted. Programme Sponsor decision A** (9 November 2026): WP5 is released as **0.2.1** (Section 11.6) |
| M1: only the first sentence set's result was reported; the second stopped 18 of 20 (EIP-ESR0062-001), which Section 3 of this EIP itself required | Medium | **Fixed**: both sets, and what the second missed, in the parents' guide and the page |
| M2: the host scan skipped `sentinel/`, where `api.anthropic.com` lives; the map's intro overstated the test | Medium | **Fixed**: `sentinel/` and `src/` scanned, `api.anthropic.com` required by the anchor test, the intro reworded, and what is not scanned (`http://` local addresses and fixtures, `scripts/`, computed paths) stated in the test |
| L1: a "PIN set" notice holds the setting Administrator's name and can outlive that profile's erasure | Low | **Fixed** in the map |
| L2, L3: a scrub that cannot empty the `-wal` file only logs; other deletions are not scrubbed | Low | **Fixed** in the map: exactly what is overwritten and the wait until SQLite empties the file itself, at the latest on closing; the page points to it. No code change: the overwrite itself (`secure_delete`) always happens |
| L3: the rotated audit copies were not in the map | Low | **Fixed** (pruning already covers every copy: `sentinel/audit.py` `prune`) |
| L4: the Windows path comes from the template, and the recovery test runs the script, not the built executable | Low | **Accepted**: both are checked on a real installed copy with the release that carries them (H1) |
| L5: the address in the consent screen has no page until it is published | Low | **Accepted**: the page is published before the release that shows the address is installed |
| L6: "Weapons" against the shown label; "no file on the computer"; the child's version silent on mistakes and on Claude | Low | **Fixed** |

## 11.7 Implementation review: Antigravity (9 November 2026)

**Pass** (`.aiems-exchange/reviewer/outbox/20261109T222106Z-return-findings.md`), on v0.7 with the version bump. It confirmed every Copilot fix, the version bump (version lines only, all seven files), the WP4 amendment (C15, C16), EBG-0180, F1 (no readable residue in either database or its `-wal`; `-shm` holds no row data; safe beside WAL readers; fails soft), F2 (unreachable from the app), F3, L1, L2, the evidence table, and that the page states facts only and names no household member. The first two runs stopped on refused commands of its own form (a test command with `-q` after the path; a grep pattern with escaped quotes); the prompt no longer offered tests, and the run was resumed with the accepted form. The allow-list was not changed.

| Finding | Severity | Disposition |
|---|---|---|
| A recovery option with a missing or extra argument fell through to starting the backend instead of explaining | Low | **Fixed**: any malformed use of `--reset-admin-pin` or `--add-administrator` prints the usage, says nothing was changed and exits 2 before the backend starts. Test: `test_a_mistyped_recovery_command_explains_itself_and_changes_nothing` |

## 11.6 Release 0.2.1 (decision on H1, 9 November 2026)

The Programme Sponsor chose option A: the WP5 commit sets version **0.2.1**, and the guides and page say 0.2.1. `sync_product_version.py 0.2.1` updated `VERSION`, `pyproject.toml`, `package.json`, `src-tauri/Cargo.toml` and `src-tauri/tauri.conf.json`; `npm install --package-lock-only` and `cargo update --workspace` changed only the project's own version line in `package-lock.json` and `src-tauri/Cargo.lock`; `--check` agrees. The script wrote CRLF line endings; they were put back to LF.

Order after the commit: the Programme Sponsor pushes, then tags `v0.2.1` on the commit (the release workflow refuses a tag that does not match `VERSION`); the release builds both installers and runs the voice round trip; the page is published only once that release exists (so L1's address and every guide claim match an installer that can be downloaded); then the Programme Sponsor installs 0.2.1 on the PC once and runs the Windows PIN-reset command from the real install folder (L4). The Mac visit installs 0.2.1 (EIP-ESR0062-004 Section 11.1).

## 11.8 Commit and post-commit review (9 November 2026)

**Approved** by the Programme Sponsor in the Sponsor Approval Service (`ESR-0062`/`WP5`); `submit-response` accepted (22:50 UTC); committed **`db0f9ef`** (31 files; the pre-commit validator passed, 0 errors). **Post-commit review: Copilot Pass** (`20261109T225255Z`) and **Antigravity Pass** (`20261109T225658Z`): the 31 files match Section 4A and 11.1 to 11.7; no stray file, secret or sentence-set content (hashes only); the fixes present; version lines only, so `v0.2.1` on this commit passes the release's tag check; LF throughout. Both noted a trailing blank line at the end of `jarvis/tests/test_packaged_recovery.py` (Low; Info): removed, with these records.

**The page, built** from `CHILDREN_AND_PRIVACY.md` at `db0f9ef` with markdown-it (CommonMark with tables) into one `index.html` (no scripts, nothing loaded from elsewhere, light and dark styles; no sideways scroll at 390 px) plus an empty `.nojekyll`: 11,001 bytes, SHA-256 `86c51bd96d8c20a675a85dced056831cd0927e54b5927b6a55050bf0b791331c`. Published after the `v0.2.1` release exists (Section 11.6).

## 11.9 Release and publication (21 November 2026)

**Release:** the Programme Sponsor tagged `v0.2.1` on `db0f9ef` and pushed it; the Release workflow passed (run `44953608183`: Windows 10 min, macOS 5 min, including the voice round trip) and published release `v0.2.1` with `JARVIS.Guardian.Shell_0.2.1_x64-setup.exe` and `JARVIS.Guardian.Shell_0.2.1_aarch64.dmg`, each with its `.sha256`.

**The page:** rebuilt from `CHILDREN_AND_PRIVACY.md` at `db0f9ef` (unchanged since) with the same build as Section 11.8, recovered from that session's record: identical, 11,001 bytes, SHA-256 `86c51bd96d8c20a675a85dced056831cd0927e54b5927b6a55050bf0b791331c`. Committed to `rmcneill2828-art/AI-Project` as `c6693c9` (`index.html` and an empty `.nojekyll` only, D-1) and **pushed by the Programme Sponsor**, who turned on Pages (deploy from `main`, root). **Live at `https://rmcneill2828-art.github.io/AI-Project/`**, the address in the app (`src/publicPages.js`, L1); the served file was fetched and matches the SHA-256 above. Its links resolve (the data map is in this repository, which is public).

The blocker on Claude for a Child is removed. Turning it on stays the Programme Sponsor's separate decision (D-4).

---

# 10. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 21 November 2026 | Claude Engineering Implementer | `v0.2.1` released; the page published at `https://rmcneill2828-art.github.io/AI-Project/`, served file matches the reviewed build (Section 11.9). |
| 0.9 | 9 November 2026 | Claude Engineering Implementer | Committed `db0f9ef`; post-commit review Copilot Pass, Antigravity Pass; the page built (SHA-256 recorded) (Section 11.8). |
| 0.8 | 9 November 2026 | Claude Engineering Implementer | Antigravity implementation review Pass; its Low fixed (Section 11.7). Awaiting Programme Sponsor approval. |
| 0.7 | 9 November 2026 | Claude Engineering Implementer | H1 decided (option A): version 0.2.1, the release and publication order (Section 11.6). |
| 0.6 | 9 November 2026 | Claude Engineering Implementer | Copilot implementation review, Conditional Pass: M1, M2 and the Lows fixed; H1 (the release) for the Programme Sponsor (Section 11.5). |
| 0.5 | 9 November 2026 | Claude Engineering Implementer | Guides G2-G4 written; L1 and L2 built; B1-B5 results, D-1 premise corrected, the evidence table (Sections 11.2, 11.3). |
| 0.4 | 9 November 2026 | Claude Engineering Implementer | Build findings F1-F3 and the Programme Sponsor's decisions (Section 11.1): erased data overwritten; PIN recovery on the packaged backend; EBG-0180 for note saving, in-app text corrected; the page repository named. |
| 0.3 | 9 November 2026 | Claude Engineering Implementer | Design approved: D-1, D-2 and D-4 as recommended; D-3 no legal advice needed (Section 11). |
| 0.2 | 9 November 2026 | Claude Engineering Implementer | Design review Conditional Pass (Copilot), five Mediums accepted: what Claude receives (the last six exchanges; never a Child's notes); what erasing a profile leaves; the one page the app can open; stores the map missed. Lows: the developer endpoint setting, downloads showing the internet address. G4 widened (Anthropic outside the UK, withdrawing consent, the ICO, no claim of compliance); D-1 and D-2 conditions; L2 covers columns, folders and network hosts. |
| 0.1 | 9 November 2026 | Claude Engineering Implementer | Drafted at ESR-0062 WP5: a data map built from the code; user guide, parents' guide and the public "Children and privacy" page; the page's address in the consent dialog; a test that keeps the map honest; four decisions (public hosting, contact, legal review, Claude for a Child). |
