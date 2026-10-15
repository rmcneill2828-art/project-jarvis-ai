# EIP-ESR0061-005 - Setup, Settings, Privacy and Data Rights

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-005 |
| Title | Engineering Implementation Package: WP5 Setup, Settings, Privacy and Data Rights |
| Version | 0.13 |
| Status | Draft - design drafted 13 October 2026 at the Programme Sponsor's request ("Please start WP5"); design review Conditional Pass (two High, three Medium, one Low), all addressed in v0.2, re-check Pass; design approved as recommended 15 October 2026; WP5a committed 8cb21e7 (implementation review Pass, Info only; pre-check PASS; CI green apart from the five known microphone tests in the informational WebKit job; post-commit review Pass); WP5b (note sharing screen, closes EBG-0110; audit retention) committed 262b7f6 (implementation review Pass, Info only; pre-check PASS; CI green apart from the five known microphone tests in the informational WebKit job; post-commit review Pass); WP5c (per-profile export and erasure) committed 289124a (implementation review Pass, one gap found by the Engineer and fixed; pre-check PASS; CI green apart from the five known microphone tests; post-commit review Pass); WP5d (first-run flow, EBG-0165 closed) built, implementation review Pass (Info only), awaiting the Programme Sponsor's approval to commit |
| Session | ESR-0061 (the plan puts WP5 in Session C; the Programme Sponsor directed it to start under this session, as WP3 and WP4 did) |
| Work Package | WP5 |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 7 (WP5) and Appendix A.3 (privacy requirements) |
| Decisions it rests on | D23 (GDPR principles as the design standard), D25 and D26 (Child provider restriction, spend cap), S1-S6 (WP3), W1-W10 (WP4) |
| Backlog | EBG-0110 (UI half, **closes it**); the `keyring` item for the Claude key; STD-0006 amendment; first-run flow; profile erasure, per-profile export, retention limits, privacy notice (plan A.3) |
| Risk class | **High-risk** (plan Section 7: WP2, WP3, WP5, WP6): it stores a credential, deletes household data and exports it. Antigravity reviews the design and the built result; Copilot's quota is out until 1 November 2026 |

---

# 2. Purpose

Make a fresh install usable by a household member who is not an engineer, and give the household the data rights the plan commits to: a first-run flow that ends with a working local assistant; the Claude key held in the operating system's credential store instead of an environment variable; a Settings view where an Administrator controls what Claude may receive, how long logs are kept, and what JARVIS holds about each profile; and a plain-language privacy notice at the point of choice.

It is the UI and storage half of work WP3 began. WP3 delivered the backend control for memory sharing and the Claude adapter; WP4 delivered the shell and the role table (item 6.5 of EIP-ESR0061-004). This package builds on both and adds one view to the shell.

---

# 3. Decomposition

| Sub-WP | Content | Effort |
|---|---|---|
| **WP5a** | The Claude key in the credential store (`keyring`); the backend methods to set, remove and report it; Settings view with the key section and the privacy notice; STD-0006 amendment | 1.25-1.5 d |
| **WP5b** | EBG-0110 UI half (per-profile memory sharing, closes the item); time-based retention for the audit log, configurable | 1-1.25 d |
| **WP5c** | Per-profile export (readable and portable); profile erasure with its confirmation | 1.25-1.5 d |
| **WP5d** | First-run flow (Ollama first, optional Claude); the setup stepper; tests across roles; documentation and backlog updates | 1-1.25 d |

Total 4.5-5.5 days, as the plan estimates. Each sub-WP is a gated commit (rule A6: design approval first, then the built result, then the Programme Sponsor's real `~/approve`). WP5a is the largest risk (a credential and the sidecar build) and goes first.

---

# 4. Repository Context Investigated

| Fact | Where | Why it matters |
|---|---|---|
| The Claude key is read only from the `ANTHROPIC_API_KEY` environment variable, at sidecar start; the Claude provider is registered only if it is present and non-blank | `jarvis/interfaces/stdio_rpc.py` (`ANTHROPIC_KEY_ENV_VAR`, `build_default_runtime`) | There is no way to set it from the app, and a change needs a restart |
| `keyring` is not a dependency of the sidecar or the repository today | `pyproject.toml`, `requirements*.txt`, `src-tauri/Cargo.toml` | A new dependency (rule A4: named here) |
| Memory sharing with Claude is a profile field, set by `ProfileService.set_cloud_memory_sharing` (Administrator or Adult profiles only), exposed as an RPC that requires an Administrator caller | `jarvis/identity/service.py`, `stdio_rpc.py` line 884 onward | The backend half exists and is tested; WP5b is the screen |
| A profile is one row in `profiles.db`; its memory notes are rows in `personal.db` with `profile_id`; household notes have `profile_id` NULL; each note links to a consent decision row | `jarvis/identity/store.py`, `jarvis/memory/store.py` | Defines exactly what an erasure and an export must touch |
| Recent conversation is held **in memory only**, one Cognitive Core per profile id; it is not persisted | `jarvis/guardian/runtime.py` (`_cognitive_core_for`) | Erasure clears it; nothing on disk to delete |
| The spend ledger is **monthly aggregate** (month, spend, request and token counts) with no profile column | `jarvis/shared/spend_ledger.py` | Nothing in it identifies a profile; erasure does not touch it |
| Audit events carry type, outcome, summary and a small string metadata map (role, counts, capability); content is excluded by design (ESR-0059) and no profile id is written | `sentinel/audit.py`, `escalation.py` line 293 | Retention applies to the file as a whole; erasure needs no audit rewrite (the design review found no profile identifier in the events it read) |
| A consent decision row has no profile column, and its `approver_label` is the constant `LOCAL_USER_APPROVER_LABEL`; the existing per-item revocation keeps the decision "as audit history" by design (MDS-0001 Section 7.4) | `jarvis/memory/store.py`, `service.py` line 163 onward | A consent decision cannot be tied to a profile and names no one; erasure keeps them, as revocation already does |
| A proposed memory awaiting a decision is held **in memory only**, with its `profile_id`, in `PersonalMemoryService._pending` | `jarvis/memory/service.py` | Erasure must discard that profile's pending proposals, or an approval could re-create a note for an erased profile |
| The Anthropic adapter reads its key with `os.environ.get(<variable name>)` at **each call**; the route is built once at start and the `GuardianRuntime` holds the metered provider for its lifetime (None when no key) | `sentinel/anthropic_provider.py` line 127; `stdio_rpc.py` `_build_anthropic_provider`, `_build_escalation_provider` | A key set later is not seen today; see 6.2 for the smallest change that makes it work |
| `ProviderOrchestrator` can replace a provider and set its health (`register_provider`, `set_health`), and only HEALTHY or DEGRADED providers are eligible; it has no unregister | `sentinel/orchestrator.py` | The route can be switched on and off through health, with no new orchestrator method |
| `JsonAuditRecorder` writes and rotates under a `threading.Lock`; `events()` reads without it | `sentinel/audit.py` | A prune must take the same lock, and the reader must too |
| The audit log rotates by size (5 MB, 3 backups) and never by age | `sentinel/audit.py` (`JsonAuditRecorder`) | Time-based retention is new |
| STD-0006 (v1.0) records environment variables as the credential route and says it formalises existing practice | `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md` | Must be amended, not worked around |
| The AI models view already lets an Administrator or Adult check Ollama, download and switch a model (WP3c, WP4) | `src/LocalAiPanel.jsx` | First-run reuses it rather than duplicating it |
| The role table for the UI (WP4 item 6.5) already lists "Change memory sharing with Claude": Administrator yes, Adult disabled with the reason, Child and Guest no | EIP-ESR0061-004 6.5 | Approved; this package builds that row |
| No PIN or authentication exists: roles are chosen, not proved (WP6) | `GAM-0001` 8.2, plan A.3 | Settings and erasure are role-gated, not authenticated; stated in Section 7 |

---

# 5. Decisions Needed From the Programme Sponsor

Each has a recommendation. If the Programme Sponsor approves the design "as recommended", all are taken as recommended.

| # | Decision | Recommendation | Alternative |
|---|---|---|---|
| **K1** | **Where the key store lives.** The Python `keyring` package in the sidecar (Windows Credential Manager, macOS Keychain), or the Rust `keyring` crate in the shell with the key handed to the sidecar at start | **Python `keyring` in the sidecar.** One code path, tested in Python, the provider can be (re)built the moment the key is set with no restart, and the key never has to cross the Rust boundary at start | Rust crate: no new Python dependency, but a restart to apply a change and a second place that handles the secret |
| **K2** | **When no usable store exists** (a Linux machine without a secret service, or a build without the backend) | **Say so and keep the environment variable route.** The key section reports "this computer has no secure store; set ANTHROPIC_API_KEY instead". **No plaintext file, ever** | A plaintext file under `~/.jarvis` (rejected: it is the leak STD-0006 exists to prevent) |
| **K3** | **Precedence.** If both a stored key and the environment variable exist | **The environment variable wins**, as `JARVIS_OLLAMA_MODEL` already does, and the screen says so ("set by the ANTHROPIC_API_KEY setting, which overrides this screen"). This keeps every existing test and developer setup working | The store wins (surprises anyone who set the variable on purpose) |
| **K4** | **Never show the key back.** The screen shows "set" or "not set" and where it comes from; it cannot read the key. Setting is a one-way entry; removing deletes it | **As stated.** The key travels UI to Rust to the sidecar's standard input once, is never logged, never in an error message, never in the audit log | A masked display of the last four characters (rejected: unnecessary exposure) |
| **K5** | **Checking a key.** Format check on entry (`sk-ant-` prefix, a sane length) and an **explicit "Test this key" button** that makes one tiny real call after a confirmation, counted in the spend ledger (a fraction of a cent) | **Format check always; test on request only.** A wrong key is otherwise found at the first real question | No test button (a bad key is found late); automatic test on save (spends without being asked) |
| **R1** | **Retention.** Time-based retention for the audit log: default **90 days** (the plan's proposal), choices 30, 90, 365 days; pruning at start and once a day while running; size rotation stays as the backstop | **As stated.** Stored in a small settings file next to the data, written only by an Administrator. "Keep for ever" is **not** offered, so there is always a limit | Offer "never delete" (rejected: it is the case retention limits exist to prevent) |
| **E1** | **Erasure.** "Delete this profile and all its data", Administrator only, typed-name confirmation; it deletes the profile row and that profile's memory notes, discards that profile's pending memory proposals, and clears its in-memory conversation. **Consent decisions are kept** (no profile column, a constant approver label, no content: the same rule per-item revocation already follows, MDS-0001 7.4). **Refused for** the active profile (switch first) and the **last Administrator**. Household notes (profile id NULL) are **not** the profile's and are kept. **Earlier backup files are not touched and the screen says so** | **As stated** | Also offer "erase everything" (a factory reset): a separate decision, not in the plan |
| **X1** | **Export.** One folder per export with two files: a readable Markdown summary and a JSON file. Contents: the profile record, that profile's own memory notes, and for each note when it was agreed (read through the note's own consent decision id, never by listing decisions). **Not** other profiles' data, **not** household notes (they are not the profile's), **not** the key. Administrator-run for any profile; an Adult may export their own **only: the backend compares the target to the active profile and refuses otherwise** | **As stated.** Written through the same native folder picker as backup | A single JSON file; or include household notes marked as shared |
| **F1** | **First run.** Shown when no profile exists: (1) welcome and creating the first profile, as an Administrator with that said plainly; (2) the local AI check and model choice (the existing panel), **with a "Do this later" on the step so a missing Ollama or a failed download never traps anyone**; (3) an **optional** Claude step with the privacy notice, skippable; (4) done, which says plainly what is still missing. Never shown again once a profile exists; the same steps stay reachable from Settings | **As stated** | A one-page setup (rejected: the Ollama install steps need room) |
| **P1** | **Privacy notice.** One plain-language page, in Settings and shown at the Claude step, stating what JARVIS keeps on this computer, what leaves it and only when you confirm, what Claude receives (the question, recent conversation, and notes only if sharing is on for that profile), what it costs, who the cloud provider is, and the rights to export and erase. Written for an adult reader; **the Child-facing wording is WP6** | **As stated.** The text is in this package's evidence pack for the reviewer and the Programme Sponsor to read before approval | Defer the notice to WP8 (rejected: the plan places it at key setup) |
| **S1** | **Settings view.** A seventh view, "Settings", in the rail. Administrator: everything. Adult: their own export, and the memory-sharing row shown disabled with the reason; the key section and retention are not shown to an Adult | **As stated** | Fold into the System view (rejected: it mixes reading status with changing it) |

---

# 6. Design

**6.1 Credential store (WP5a).** New `jarvis/shared/secret_store.py` with three operations behind one small interface: `get(name)`, `set(name, value)`, `delete(name)`, over `keyring` with a fixed service name (`jarvis-guardian`) and a fixed entry name (`anthropic-api-key`). It reports its own availability (a backend that is a `fail` or `null` backend counts as unavailable). Nothing else in the code imports `keyring`.

**6.2 Applying a change without a restart (revised after the design review).** The first draft re-registered the Claude route at run time; the review (High) found the runtime holds the metered provider for its lifetime and the orchestrator has no unregister. The revised design needs **no re-registration**:

1. `AnthropicProvider` takes an optional **credential source**: a function returning the key or None, called at each request in place of the direct `os.environ` read. The default is the existing environment read, so nothing else changes. The sidecar passes one that reads the environment variable first (K3) and then the secret store. The key is **never placed in the process environment**, so a child process or crash report cannot inherit it.
2. The Anthropic provider and the metered wrapper are **always built** and the provider is **registered always**; its health is set `UNAVAILABLE` when no key is found and `HEALTHY` when one is. `escalation_available` already follows eligibility, so the existing offers, role gate and labels need no change. Setting or removing the key in the screen calls `set_health` after the store write. A new key also clears a circuit-opened `DEGRADED` state, which is wanted.
3. **In flight:** a request already running has its key in hand and finishes; the next request sees the new state. `set_health` is a single dictionary assignment and each request resolves its key once, so there is no partial state. The spend ledger and policy gate are untouched.
4. **One consequence, disclosed:** the spend database (`spend.db`) is now created at start for every household, not only those that set a key. It is empty until a question is escalated and holds only monthly totals.

**6.3 RPC surface (WP5a-c).** All additive:

| Method | Caller | Result |
|---|---|---|
| `provider.claudeKeyStatus` | Administrator | `{ configured, source: "environment" | "store" | "none", storeAvailable }`. Never the key |
| `provider.setClaudeKey` | Administrator | `{ configured: true }`; format-checked; a malformed key is refused with a client-facing message that does not echo it |
| `provider.removeClaudeKey` | Administrator | `{ configured, source }` (the environment variable, if any, still applies) |
| `provider.testClaudeKey` | Administrator | One minimal call, only after the UI's confirmation; result is ok or a client-facing failure; recorded in the spend ledger |
| `settings.get`, `settings.setRetentionDays` | Administrator | `{ auditRetentionDays }`; 30, 90 or 365 only |
| `profile.export` | Administrator, or Adult for their own | Writes the two files to a given directory; returns paths and counts, never content |
| `profile.erase` | Administrator | `{ erased: true, notesRemoved, decisionsRemoved }`; refuses the active profile and the last Administrator |

The existing `profile.setCloudMemorySharing` is reused unchanged by WP5b. Roles are enforced in the backend by the same `_require_role` helper the other methods use; the UI only mirrors them.

**6.4 Retention (WP5b).** `JsonAuditRecorder` gains `prune_older_than(days)`, which **takes the recorder's own lock** (the one `record` already holds for writing and rotating), writes the kept events to a temporary file in the same directory and replaces the live file with `os.replace`; rotated backups whose newest event is older than the cut-off are deleted. `events()` is changed to read under the same lock, so a reader never sees a half-replaced file (the review's Medium). Run once at start and once a day while the sidecar runs. Events whose timestamp cannot be read are **kept** (a prune must not lose a log it cannot judge) and counted in the result. The setting lives in `settings.json` beside the databases, written atomically (temporary file then replace).

**6.5 Export (WP5c).** Reads that profile's rows only. Markdown file: a heading, the profile's name and role, and a dated list of notes with, per note, when it was agreed. JSON file: the same, structured, with a `schemaVersion`. Filenames carry the date, not the display name. The export function never opens the key store and never reads household notes; both are asserted by tests.

**6.6 Erasure (WP5c).** In order: refuse if the target is the active profile or the last Administrator (in the backend); discard that profile's **pending** memory proposals (a new `PersonalMemoryService.discard_pending_for_profile`, so a later approval cannot re-create a note); delete the profile's memory notes (`profile_id` equal to the target; household notes untouched); drop the in-memory Cognitive Core for that profile id; delete the profile row. Each database change is one transaction. **Consent decisions are kept** (see E1); the review's High on deleting "unreferenced" decisions is resolved by not deleting any. The UI requires the person to type the profile's display name, then shows what was removed. **What erasure does not do, said on the screen:** it does not alter earlier backup files, it keeps the content-free consent record and audit log (which hold no profile name), and it cannot recall anything already sent to Claude, which is subject to Anthropic's own retention (stated in the privacy notice with the link to its terms).

**6.7 First run (WP5d).** A stepper component shown over the shell when `list_profiles` returns none. Step 1 creates the first profile (role fixed to Administrator and explained), step 2 embeds the existing local AI panel, step 3 is the optional Claude step (notice, key entry, skip), step 4 is "ready" with what to try. State is derived from real data (profile exists, model installed, key configured), never from a stored "done" flag, so it cannot be wrong after a restore. **Every step but the first has a skip**, and the last step lists what is still missing instead of refusing to finish. The first step cannot be skipped because nothing else works without a profile. The same stepper opens from Settings as "Run setup again".

**6.8 STD-0006 amendment.** A new section: the credential store is the preferred route for a secret a person supplies in the app; environment variables remain supported and win; no plaintext file; the key is never returned, logged or placed in an error or audit event; unavailable store means environment only. Version 1.1.

**6.9 Role table for the new view.** Extends EIP-ESR0061-004 item 6.5:

| Control | Administrator | Adult | Child | Guest |
|---|---|---|---|---|
| Settings view | yes | yes (reduced) | no | no |
| Claude key: set, remove, test | yes | not shown | no | no |
| Memory sharing with Claude, per profile | yes | shown disabled with the reason | no | no |
| Audit retention | yes | not shown | no | no |
| Privacy notice | yes | yes | WP6 wording | WP6 wording |
| Export a profile | any profile | own only | no (an Administrator runs it) | no |
| Erase a profile | yes | no | no | no |
| Run setup again | yes | no | no | no |

---

# 7. Cross-Work-Package Flags

* **WP6 (PIN).** Until WP6, "Administrator" is a role someone selects, not one they prove. The key, retention, export and especially **erasure** are therefore role-gated and confirmed by typing, but not authenticated. The design records this and does not claim otherwise. If the Programme Sponsor wants erasure held back until the PIN exists, WP5c can move after WP6 with no other change. **Flagged for decision.**
* **WP6 (Child).** Child defaults for memory sharing (off, already enforced by the backend) and the Child-facing privacy wording are WP6.
* **WP8.** The public "Children and privacy" page and the data map are WP8; this package supplies the facts they will state.
* **WP2/WP7 (macOS).** The macOS Keychain backend cannot be exercised on the Windows PC; it is built into the arm64 sidecar and checked at Mac visit 1. The CI `python-macos` job can import it but not read a Keychain.
* **Not in scope, named so it is not assumed:** a setting for the monthly spend cap (the cap stays the environment variable and the Console limit; the allowance is already shown), a factory reset, any change to the Claude model choice, and any account or sign-in.
* **Rail count.** The rail goes from six views to seven, so the tests that assert six names change; this is a deliberate edit, not a weakened test.

---

# 8. Evidence Pack (TPL-0001 Section 6)

* **New dependency (rule A4):** `keyring`, pinned exactly, runtime, in the sidecar's requirements. Its Windows and macOS backends need PyInstaller hidden imports in the sidecar spec; a build check (the sidecar starts and reports the store's availability) is part of WP5a.
* **CI changes:** none planned beyond the new tests; the sidecar build job is the check for the hidden imports.
* **Tests (planned):** Python - secret store (fake backend, unavailable backend, never logged), key RPCs by role, runtime re-registration on set and remove, retention pruning (kept, pruned, unreadable timestamp kept), export contents and exclusions, erasure (rows, consent decisions, in-memory conversation, refusals), the first-run state derivation. Playwright - the Settings view per role, the key section states, sharing toggle by role, retention choice, export and erase flows with the typed confirmation, the first-run stepper end to end, the rail count.
* **Live checks, by the Engineering Implementer on this PC:** set, test and remove a real key in the Windows Credential Manager through the packaged sidecar; one real export and one real erase on a throwaway profile.
* **Not checkable here:** the macOS Keychain (Mac visit 1).

---

# 9. Commit Contents (expected, per sub-WP; finalised at build)

**WP5a:** `jarvis/shared/secret_store.py` (new) and its tests, `jarvis/interfaces/stdio_rpc.py` and its tests, `jarvis/guardian/runtime.py` if the re-registration needs it, `src-tauri/src/lib.rs` for the new commands, the sidecar requirements and spec, `src/` Settings view and privacy notice, `tests/e2e/`, `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md`. **WP5b:** `sentinel/audit.py`, `jarvis/shared/settings.py` (new), `src/` sharing and retention controls, tests, `EBR-0001` (EBG-0110 closed). **WP5c:** `jarvis/identity/` and `jarvis/memory/` erasure and export methods, `stdio_rpc.py`, `src/`, tests. **WP5d:** `src/` first-run stepper, tests, documentation and backlog updates. Each with the record files (this EIP, ESR-0061, REG-0001), listed by name in the sub-WP's own Commit Contents section when it is built.

---

# 10. Questions for the Engineering Reviewer

1. **Key handling.** Is there any path by which the key could reach a log, an error message, the audit log, a traceback, the UI or a test snapshot? Check the proposed RPC shapes (6.3) and the format-check error message.
2. **Re-registration (6.2).** Is rebuilding the Claude route at run time safe against a request in flight, the spend ledger, and the policy gate? Is anything about the Sentinel wiring assumed at start that this breaks?
3. **Erasure completeness (6.6).** Is anything that identifies a profile left behind - in the audit log, the spend ledger, the consent decisions, a cache, or the Ollama model-choice file? Section 4 claims none; please verify rather than accept.
4. **Export exclusions (6.5).** Are household notes, other profiles' data and the key all provably absent?
5. **Retention (6.4).** Is rewriting the live audit file safe against a concurrent write by the recorder? Is "keep what cannot be judged" the right default?
6. **Role enforcement.** Does every new method have a backend role check, so the UI is a mirror and not the gate?
7. **First-run (6.7).** Can the stepper trap a person (no way past a failing step), or show again after a restore?
8. **The privacy notice.** Read the text in 6.3/P1's list against the code: is every statement true today? Is any promise made that the build does not keep?
9. **Anything rated Medium or higher.**

---

# 10A. Design Review Record (15 October 2026)

**Review** (Antigravity, Gemini 3.8 Flash High, `sender: reviewer`, submitted 13 October 2026 12:51:22Z, verdict recorded 15 October 2026 after one resume): **Conditional Pass**, six findings, all addressed in this version:

| Rating | Finding | Disposition |
|---|---|---|
| High | Erasure that deletes "unreferenced" consent decisions would delete denied decisions of every profile and the history of revoked notes | **Fixed**: no consent decision is deleted (E1, 6.6). Verified: the table has no profile column and the approver label is a constant |
| High | Re-registering the cloud route lacks runtime wiring, has no orchestrator unregister, and races an in-flight escalation | **Fixed**: no re-registration; a credential source in the adapter and a health switch (6.2), with the in-flight behaviour stated |
| Medium | Pending memory proposals of an erased profile are not purged | **Fixed**: discarded first (6.6); a test is planned |
| Medium | Pruning the audit file needs locking across the recorder and its reader | **Fixed**: same lock, atomic replace, reader under the lock (6.4) |
| Medium | The first-run local AI step must have a skip path | **Fixed**: every step but the first can be skipped (6.7, F1) |
| Low | Export must verify an Adult exports only their own profile | **Fixed**: enforced in the backend (X1) |

A single reviewer, smaller than the Pro model of earlier reviews, judging by reading. Its first run stopped before recording a verdict and was resumed once.

**Re-check of v0.2** (resume, 15 October 2026): **Pass.** It confirmed consent decisions are kept as content-free history with no profile identifier, that a credential source plus the health switch needs no new orchestrator method and is safe for an in-flight request, that an empty spend database at start is acceptable, and that pending proposals, audit locking, the skip paths and the Adult-export limit are in the design.

---

# 12. Design Approval Record (15 October 2026)

The Programme Sponsor approved the design in chat, **as recommended** (K1 to K5, R1, E1, X1, F1, P1, S1), with two answers: erasure **stays in WP5** (Section 7's first flag; it is role-gated and confirmed by typing, not authenticated, until WP6), and the registration of this EIP in REG-0001 with a "design awaiting approval" status line is fine. This is gate 1 of rule A6.

# 13. WP5a Build Record (15 October 2026)

| Item | Result |
|---|---|
| The store (K1, K2) | New `jarvis/shared/secret_store.py`: `get`, `set`, `delete` over `keyring`, with the platform backend chosen explicitly (Windows Credential Manager, macOS Keychain) rather than by entry-point discovery, which a one-file PyInstaller build cannot be relied on to carry. An inert `fail` or `null` backend counts as unavailable. Every failure raises one fixed message with no cause chained, so a backend's own text (which could hold the value) is never reported; only the exception type is logged. `SecretStore.unavailable()` is the inert store used by tests and by any run with an explicit environment |
| The manager (K3, K4) | New `jarvis/interfaces/claude_key.py`: `resolve()` reads the environment variable first, then the store, at each call; `status()` returns only `configured`, `source` and `storeAvailable`; `set_key` format-checks (`sk-ant-` then 16 to 400 URL-safe characters) and refuses with wording that does not echo the input; `remove_key`; and `apply()`, which tells the route whether a key exists |
| No restart (design 6.2) | `AnthropicProvider` takes an optional `credential_source`, called at each request; the default keeps the old environment read. `build_default_runtime` now **always builds and registers** the Anthropic provider and the metered wrapper, and the manager switches that provider's health (`HEALTHY` or `UNAVAILABLE`) through the orchestrator's existing `set_health`, so no new orchestrator method was needed. The key is never placed in the process environment. `build_default_runtime(environ, secret_store=None)`: an explicit environment gets the inert store, so no test can read the host's credentials |
| RPC (6.3) | `provider.claudeKeyStatus`, `provider.setClaudeKey`, `provider.removeClaudeKey`, `provider.testClaudeKey`: Administrator only, enforced in the backend with `_require_role`, and added to the activity tracker's method map. The test method makes one tiny request through the same metered, gated route, so it is in the ledger. Four Tauri commands relay them (`claude_key_status`, `set_claude_key`, `remove_claude_key`, `test_claude_key`); the Rust side logs nothing of a request |
| The screen (S1, P1, K4, K5) | New Settings view (the rail goes to seven): the Claude key section for an Administrator - status in words and where the key comes from, a password field that is cleared after saving and can never show the key again, remove, and a **Test this key** that needs a confirmation naming the cost; the plain-language privacy notice for an Administrator or an Adult. The erasure, export, sharing and retention controls are WP5b and WP5c, and the notice does not promise them |
| STD-0006 | Version 1.1: new Section 6A and a compliance row, and `ANTHROPIC_API_KEY` named among optional-capability credentials |
| Sidecar build | `keyring>=25.6,<26` added; the build now passes `--copy-metadata keyring` and `--collect-submodules keyring.backends`, and `--hidden-import win32ctypes.core` for a Windows target only. **The packaged sidecar was built and run** (below) |
| **Live checks on this PC, the packaged sidecar, the real Windows Credential Manager** | (1) A well-formed throwaway key: status none, set, status "store", `provider.status` configured, remove, status none and `provider.status` not configured. (2) The Programme Sponsor's real key, taken from the user environment variable and given to the sidecar only through `provider.setClaudeKey` with the variable removed from the sidecar's environment: set, **one real test request: ok, US$0.0001 spent**, remove, not configured. In both runs the key appeared in no reply, no line of the sidecar's standard error and no log file |
| Tests | Python **1186 passed and 4 skipped** (20 new in `jarvis/tests/test_claude_key_rpc.py`: store, manager, every role, set and remove with no restart and the right header sent, replace, environment precedence, malformed and never echoed, no store, a failing store, the test call and its ledger entry, and the key absent from every reply, log line and audit file). Playwright **130 passed and 5 skipped** on Chromium (the five skipped are the Orb frame measurements); 12 new tests for the Settings view and the key flows, and the axe checks now cover the Settings view. ruff clean, validator 0 errors |
| Changed tests | The no-key escalation test now asserts that `spend.db` exists but holds no rows (design 6.2, consequence 4). The dead-controls list no longer names "Settings", which was one of the eleven dead controls and is now a real view; its test says so. The "six views" assertions are seven |
| **Disclosed, not done** | The macOS Keychain backend was not exercised (Mac visit 1). Linux has no tested secret service path: it reports "no secure store" unless one is present. The privacy notice names no export or erasure yet (WP5c). The monthly cap is still the environment variable (named out of scope in Section 7) |

# 14. WP5a Commit Contents (expected)

Changed: `sentinel/anthropic_provider.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/interfaces/activity_tracker.py`, `jarvis/guardian/runtime.py`, `jarvis/tests/test_escalation_rpc.py`, `src-tauri/src/lib.rs`, `src/App.jsx`, `src/Shell.jsx`, `src/roles.js`, `src/shell.css`, `tests/e2e/app.spec.js`, `tests/e2e/accessibility.spec.js`, `pyproject.toml`, `scripts/build_backend_sidecar.py`, `aiems/standards/STD-0006_CONFIGURATION_AND_SECRETS_STANDARD.md`, `aiems/governance/reviews/EIP-ESR0061-004_GUARDIAN_EXPERIENCE_REDESIGN.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `jarvis/shared/secret_store.py`, `jarvis/interfaces/claude_key.py`, `jarvis/tests/test_claude_key_rpc.py`, `src/SettingsView.jsx`, `aiems/governance/reviews/EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS.md`.

The EIP-ESR0061-004 record changes (WP4d-fix post-commit, WP4d-fix2 post-commit) and the EIP-ESR0061-005 design records ride in this commit under rule A3.

# 15. WP5a Implementation Review Record (15 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`, 15 October 2026, `sender: reviewer`, submitted 09:46:24Z): **Pass**, eight points all reported as Info and no finding above it: key handling end to end (store or memory only, never in a log, an exception or its cause, the audit log, an RPC reply, the DOM after saving, the environment or a file); precedence and state (the source matches what `resolve` returns, removing a stored key leaves an environment key working, health follows key presence); the no-restart route switching (a registered but unavailable provider is never offered, an in-flight request finishes with the key it resolved, the empty spend database at start is benign); roles (every new method requires an Administrator in the backend, the test method is capped by the ledger); tests (an inert store and an autouse fixture keep the host's credentials out; the screen mock keeps a source flag, never the key); the privacy notice (accurate, promises nothing unbuilt); the sidecar build flags; STD-0006 1.1.

**How much that is worth, said plainly.** This is a high-risk package and a single, smaller reviewer found nothing to fix, as it did for WP3b (disclosed in EIP-ESR0061-003 Section 19): a weak signal that the package is clean. What the Pass does not replace is the evidence in Section 13: the packaged sidecar was run against the real Windows Credential Manager, a real test request was made, and the key was searched for in every reply, the sidecar's standard error and the log files, and was in none of them. **The Mac Keychain and a second reader for the privacy wording remain open**: the Programme Sponsor should read the notice in Settings (the text is in `src/SettingsView.jsx`) before the build is approved.

# 16. WP5a Post-Commit Record (15 October 2026)

`8cb21e7` ("ESR-0061 WP5a: The Claude key in the credential store, Settings view and privacy notice") was approved through the Sponsor Approval Service (`submit-response` 09:58:56Z) and pushed by the Programme Sponsor. **Pre-check: PASS on every hard check**, with `--contents-heading "14. WP5a Commit Contents"`: tree clean, on origin/main, the 23 changed files equal Section 14 (the dotfile fix of WP4d-fix2 in use), gated against the parent, pytest 1186 passed and 4 skipped, ruff, validator 0 errors. **CI, by commit SHA:** push run 38718001555, success on `frontend-build`, `playwright`, `python`, `python-macos`, `rust`, `rust-macos` and `rust-windows`. The informational `playwright-webkit` job: **125 passed, 5 failed, 5 skipped; the five failures are exactly the known microphone and recording tests**, so the new Settings view and key flows pass on the Mac's WebKit. **`python-macos` and `rust-macos` passing is the first evidence that the new `keyring` dependency installs and imports on macOS; it is not evidence that the Keychain works**, which only a Mac can show (visit 1). **Post-commit review** (Antigravity, Gemini 3.8 Flash High, 15 October 2026, `sender: reviewer`): **Pass**, Info only: the 23 files match Section 14, the commit message and records are accurate, and a fresh read found no path for the key to a log, an error, a reply, the audit log or the environment. A smaller single reviewer, judging by reading.

# 17. WP5b Build Record (15 October 2026)

Built at the Programme Sponsor's request ("Please start"), under the design approved on 15 October 2026 (6.4, 6.9, R1, S1).

| Item | Result |
|---|---|
| Retention in the recorder (6.4) | `JsonAuditRecorder.prune_older_than(days)` takes the recorder's own lock, rewrites each file (the live file and every rotated copy) to a temporary file in the same directory and swaps it in with `os.replace`, deletes a rotated copy left empty, and **keeps and counts a line whose time cannot be read** (a naive time is read as UTC). `events()` now reads under the same lock, which the design review required: before, a reader could race a rotation. It returns counts only |
| The setting (R1) | New `jarvis/shared/settings.py`: one JSON file beside the databases holding `auditRetentionDays`, allowed values 30, 90 and 365, **default 90; a missing, damaged or out-of-range file reads as the default**, never an error and never "keep for ever". Atomic write under a lock |
| When it runs | New `jarvis/interfaces/retention.py` (`RetentionService`): once at start and then daily on its own daemon thread (so a slow prune cannot hold up a request), and at once when an Administrator changes the setting. A failure is logged by exception type and never stops the backend |
| RPC | `settings.get` and `settings.setRetentionDays` (Administrator only, in the backend, with the allowed values checked there as well as in the screen); added to the activity tracker's method map; two Tauri commands relay them. The existing `profile.setCloudMemory` is unchanged |
| The screen (EBG-0110 UI half, S1) | Settings gains **Notes and Claude**: a switch per profile. An Administrator sees every profile and may change any that can ask Claude; a Child or Guest profile's row says it cannot ask Claude, so none of its notes are ever sent, and has no usable switch; an Adult sees only their own row, disabled, with "Only an Administrator can change this". And **Activity log**: three choices (30 days, 90 days, One year), a note of the last tidy-up, and no option to keep it for ever. A refused change is shown and the control returns to its true state. The profile list and the signed-in profile update from the reply, so the confirmation dialog's "notes will be sent" line follows at once |
| Tests | Python **1224 passed and 4 skipped** (38 new in `jarvis/tests/test_audit_retention.py`: older and newer events, unreadable and naive times, rotated copies and an emptied one, an emptied live file, writes racing a prune lose nothing, the setting's default, persistence, rejected values and damaged files, the service surviving a failure and stopping when told, and the methods by role and for bad values). Playwright **137 passed and 5 skipped** on Chromium (7 new for sharing and retention). ruff clean, validator 0 errors, cargo check clean |
| Live check | A copy of this PC's real audit log (the live log was untouched) pruned at 365, 90 and 30 days: 2 events, none removed, no error. The log is only two days old, so this shows the code runs on real data, **not** that old entries are removed; that is shown by the tests with controlled times |
| EBR-0001 | EBG-0110 set to Completed, with the account of both halves |
| **Disclosed, not done** | The macOS-specific behaviour of `os.replace` over an open file is not exercised (Mac visit 1); the packaged sidecar was not rebuilt for this sub-WP (no new dependency or build flag), so the retention thread has run only from source; the daily interval is a constant, not a setting |

# 18. WP5b Commit Contents (expected)

Changed: `sentinel/audit.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/interfaces/activity_tracker.py`, `src-tauri/src/lib.rs`, `src/App.jsx`, `src/SettingsView.jsx`, `src/roles.js`, `src/shell.css`, `tests/e2e/app.spec.js`, `tests/e2e/accessibility.spec.js`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/reviews/EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `jarvis/shared/settings.py`, `jarvis/interfaces/retention.py`, `jarvis/tests/test_audit_retention.py`.

The WP5a post-commit record (Section 16) rides in this commit under rule A3.

# 19. WP5b Implementation Review Record (15 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`, 15 October 2026, `sender: reviewer`, submitted 10:30:01Z): **Pass**, seven points all reported as Info: the prune serialises under the recorder's lock with record, rotate and `events()`, replaces atomically, keeps unreadable lines and naive times, and deletes a rotated copy only when this prune emptied it; the setting enforces 30, 90 and 365 with a 90 default, falls back safely and rejects booleans and numeric strings; the retention service runs on its own daemon thread and a failure never stops the server; every settings method and the sharing change require an Administrator in the backend and an Adult sees only their own disabled row; the screen state follows the backend; EBG-0110 is delivered across the backend and the screen; the tests are not vacuous.

**How much that is worth.** The same smaller single reviewer, no finding on a high-risk package: a weak signal, as for WP3b and WP5a. What stands behind this record is the evidence in Section 17, notably the test in which a writer thread records continuously while the prune runs twenty times and every written event is still present afterwards. **EBG-0110's closure is my judgement** of both halves against the item's concern (retained notes reach a provider only on a confirmed escalation, by a profile that may ask Claude and whose sharing is on); the Programme Sponsor may reopen it if the item meant a Sentinel policy distinction in the strict sense (the register row still says that `SimpleApprovalPolicy` is the core default, tracked as EBG-0074).

# 20. WP5b Post-Commit Record (15 October 2026)

`262b7f6` ("ESR-0061 WP5b: Per-profile note sharing screen (closes EBG-0110) and audit retention") was approved through the Sponsor Approval Service (`submit-response` 10:44:46Z) and pushed by the Programme Sponsor. **Pre-check: PASS on every hard check**, with `--contents-heading "18. WP5b Commit Contents"`: tree clean, on origin/main, the 18 changed files equal Section 18, gated against the parent, pytest 1224 passed and 4 skipped, ruff, validator 0 errors. **CI, by commit SHA:** push run 38723101977, success on `frontend-build`, `playwright`, `python`, `python-macos`, `rust`, `rust-macos` and `rust-windows`; the informational `playwright-webkit` job **132 passed, 5 failed, 5 skipped, the five failures being exactly the known microphone and recording tests**. `python-macos` passing includes the audit prune and the retention tests on a non-Windows filesystem; it is not the Mac's real filesystem behaviour over an open file, which is Mac visit 1. **Post-commit review** (Antigravity, Gemini 3.8 Flash High, 15 October 2026, `sender: reviewer`): **Pass**, Info only: the 18 files match Section 18, the commit message and records are accurate, the prune is safe under the recorder's lock and cannot delete outside the audit files, and the sharing screen restricts changes to the Administrator with the backend enforcing it. A smaller single reviewer, judging by reading.

# 21. WP5c Build Record (15 October 2026)

Built at the Programme Sponsor's request ("Please start"), under the design approved on 15 October 2026 (6.5, 6.6, X1, E1, with the design review's fixes).

| Item | Result |
|---|---|
| Export (X1, 6.5) | New `jarvis/memory/profile_export.py` writes two files into the chosen folder: a readable Markdown summary and a JSON file with a `schemaVersion`. Contents: the profile record and **that profile's own notes only** (`PersonalMemoryStore.list_owned`: `profile_id` equal to the profile, never a household note, never another profile), each with when it was saved and when it was agreed (read through the note's own consent decision id, never by listing decisions). Filenames carry the date, never the profile's name. The reply names files and counts and holds no content |
| Export roles (the review's Low) | `profile.export` is **enforced in the backend**: an Administrator may export any profile; an Adult only their own (refused with a plain message and nothing written, not even the folder); a Child or Guest none ("ask an Administrator"). The screen mirrors it |
| Erasure (E1, 6.6) | `profile.erase`: Administrator only; `check_erasable` refuses the signed-in profile and the last Administrator; **the typed name must match the profile's display name in the backend too**, not only in the screen. In order: the profile's **pending proposals are discarded** (so a late approval cannot re-create a note), its own notes are deleted (`delete_owned`), its in-memory conversation is dropped, then the profile row and a stored active pointer to it are deleted. **Consent decisions are kept** (the review's High), as per-item revocation already keeps them, and **household notes and earlier backup files are untouched**; the confirmation says so |
| The screen (S1, 6.9) | Settings gains **Your data**: an Administrator sees every profile with Export and Erase; an Adult sees only their own with Export and no Erase. Export asks for a folder with the native picker and says what was written and how many notes; cancelling the picker does nothing. Erase opens a confirmation that lists what it does not touch and enables its button only for the exact name; Erase is disabled, with the reason, for the profile in use and for the last Administrator. An erased profile disappears from every list on the screen |
| Privacy notice | The notice now names the export and erasure rights that exist, what erasure leaves, and the retention limit (it promised none of this before it was built, per the WP5a review) |
| Tests | Python **1252 passed and 4 skipped** (28 new in `jarvis/tests/test_profile_data_rights.py`: an export holds the profile's notes and not Robert's, the household note or another profile's id; no key and no profile name in any file or filename; replies carry no content; empty export; every role for export; unknown profile and bad parameters; erasure removes only that profile's rows, keeps consent decisions, discards a pending proposal so a late approval fails, drops the in-memory conversation, refuses the active profile, the last Administrator (service rule) and every non-Administrator; a wrong typed name erases nothing; the key and settings are untouched). Playwright **147 passed and 5 skipped**, the previous 137 plus 9 for export and erasure and one for the privacy notice; the mock applies the backend's own rules. ruff, validator and `cargo check` clean |
| **Live check on this PC, the packaged sidecar (rebuilt)** | In a temporary data directory (not the real one), through `jarvis-backend`: two throwaway profiles, notes saved for each; one **real export** of an Adult's data (two notes, none of the Administrator's, two files named by date); erase refused for the signed-in profile and for a wrong name; one **real erase**: the profile and its two notes gone, the Administrator's note kept, the three consent decisions kept. The sidecar's standard error held only five ordinary log lines and no note text; one of them shows the new retention thread running in the packaged build |
| **Disclosed, not done** | The macOS file dialog and file paths were not exercised (Mac visit 1). A backup made before an erasure still holds the erased profile's notes, as stated on the screen; "erase everything" and removing a profile from a backup are not offered. Erasure is not authenticated until WP6's PIN (the Programme Sponsor's decision to keep it here, 15 October 2026) |

# 22. WP5c Commit Contents (expected)

Changed: `jarvis/identity/store.py`, `jarvis/identity/service.py`, `jarvis/memory/store.py`, `jarvis/memory/service.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/interfaces/activity_tracker.py`, `jarvis/interfaces/escalation.py`, `src-tauri/src/lib.rs`, `src/App.jsx`, `src/SettingsView.jsx`, `src/roles.js`, `src/shell.css`, `tests/e2e/app.spec.js`, `aiems/governance/reviews/EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `jarvis/memory/profile_export.py`, `jarvis/tests/test_profile_data_rights.py`.

The WP5b post-commit record (Section 20) rides in this commit under rule A3.

# 23. WP5c Implementation Review Record (15 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`, 15 October 2026, `sender: reviewer`, submitted 11:13:40Z): **Pass**, Info only, across erasure completeness (exactly the profile's own notes; household notes and other profiles untouched; consent decisions kept; pending proposals discarded first; the conversation dropped; no profile identifier left in the audit log, ledger, model-choice file, settings or active pointer), order and failure (a failed profile delete after the notes are gone is safe to retry; the active pointer goes in the same transaction; the typed name is exact and checked before anything changes), refusals, export exclusions, and the screen. Its output was cut off after the export point; the verdict and the first four findings were recorded in full.

**One gap I found myself after the review, and fixed (not a reviewer finding).** An open offer to ask Claude holds the person's question in memory until it expires; erasure dropped the conversation and the pending proposals but not that. `EscalationOffers.discard_profile` now drops a profile's open offers, `profile.erase` calls it, and a test shows the erased profile's token can no longer be redeemed while another profile's still can. Added to the commit contents (`jarvis/interfaces/escalation.py`). The reviewer had said such a token could not be redeemed because the erased profile can never become active, which is true; the point of the fix is that the question text no longer sits in memory.

**How much the Pass is worth:** the same weak signal as for WP5a and WP5b. The evidence behind this record is Section 21: the rebuilt packaged sidecar, in a temporary data directory, performed one real export (the Adult's two notes, none of the Administrator's) and one real erase (the profile and its two notes gone, the Administrator's note and all three consent decisions kept).

# 24. WP5c Post-Commit Record (15 October 2026)

`289124a` ("ESR-0061 WP5c: Per-profile export and profile erasure") was approved through the Sponsor Approval Service (`submit-response` 11:26:24Z) and pushed by the Programme Sponsor. **Pre-check: PASS on every hard check**, with `--contents-heading "22. WP5c Commit Contents"`: the 19 changed files equal Section 22, pytest 1252 passed and 4 skipped, ruff, validator 0 errors. **CI, by commit SHA:** push run 38727426321, success on every job except the informational `playwright-webkit`: **142 passed, 5 failed, 5 skipped, exactly the known microphone and recording tests**, so the Your data section passes on the Mac's WebKit. **Post-commit review** (Antigravity, Gemini 3.8 Flash High, 15 October 2026, `sender: reviewer`): **Pass**, Info only: the 19 files match, erasure removes only the target's notes and drops the open offers and in-memory conversation, export enforces its roles in the backend and holds no household notes or keys, and the records are accurate. A smaller single reviewer, judging by reading.

# 25. WP5d Build Record (15 October 2026)

Built at the Programme Sponsor's request ("Please start"), under the design approved on 15 October 2026 (6.7, F1).

| Item | Result |
|---|---|
| The flow (F1, 6.7) | New `src/FirstRun.jsx`: four steps - (1) the first profile, **created as an Administrator, said plainly, with no role choice**; (2) the local AI model, reusing the existing `LocalAiPanel`; (3) Claude, optional, with the privacy notice and the key section from WP5a; (4) a summary of what is ready and what is still missing. It replaces the main area while open, keeping the top bar |
| Never trapped (the design review's Medium) | Every step but the first has a skip ("Do this later", "Skip for now"), and the last step lists what is missing and always lets the person finish. The first step cannot be skipped because nothing works without a profile. Tested with no Ollama, no secure store and no key: every step moves on |
| State from reality | No "done" flag is stored. The summary reads `ollama.status` and the key status when it is shown, so it is true after a restore; a status that cannot be read says "could not be checked" and is never shown as ready. Setup opens by itself only once the profile list has loaded and is empty (a household with profiles is never flashed it while the list is on its way), and stays open after the first profile is created so the later steps follow |
| Run again | Settings gains **Setup** with "Run setup again" for an Administrator only; it opens at the AI step because a profile exists |
| EBR-0001 | EBG-0165 set to Completed with the account of WP5a to WP5d and the follow-ons that are not part of it |
| Tests | Python unchanged at **1252 passed and 4 skipped**. Playwright **155 passed and 5 skipped** (8 new: the walk, the summary from real state, an unreadable status, no first-run for an existing household, Run setup again, an Adult not seeing it, nothing trapping a person; the first-run steps are in the axe checks). The old "profile create form" test is replaced by a fresh-install test; the role choice it exercised is gone from first run (a second profile still chooses a role in the top-bar picker) |
| Live check (backend half) | Against the packaged sidecar on a clean data directory: no profiles and no active profile; the key methods refuse without a profile; the first profile is created as an Administrator; `ollama.status` answers (installed, not running); the key status and settings answer for it. **The WebView2 window itself was not launched**: the flow was exercised through the mocked IPC in Chromium and, in CI, WebKit |
| **Disclosed, not done** | The packaged window's first run on a clean machine (Windows Sandbox, the plan's WP9) and on the Mac (visit 1). PST-0001 still lists ESR-0060 as the last closed session and the old provider keys: it is updated at session closure by the plan's own rule (R4), not mid-session |

# 26. WP5d Commit Contents (expected)

Changed: `src/App.jsx`, `src/SettingsView.jsx`, `src/shell.css`, `tests/e2e/app.spec.js`, `tests/e2e/accessibility.spec.js`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/reviews/EIP-ESR0061-005_SETUP_SETTINGS_PRIVACY_AND_DATA_RIGHTS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`. New: `src/FirstRun.jsx`.

The WP5c post-commit record (Section 24) rides in this commit under rule A3.

# 27. WP5d Implementation Review Record (15 October 2026)

**Review** (Antigravity CLI, Gemini 3.8 Flash High, through `run_reviewer.py`, 15 October 2026, `sender: reviewer`, submitted 11:46:44Z): **Pass**, nine points all Info: every step after the profile has a skip and the last always finishes; the summary reads live status and never shows an unread or inactive configuration as ready; setup opens only after the list has loaded and is empty and does not reappear once closed; the first profile is an Administrator with a plain explanation and a retry on error; Run setup again is Administrator-only and changes nothing by itself; the reused panels integrate without lifecycle or prop problems; the EBG-0165 closure matches the work and states the follow-ons; the tests and axe checks cover every step. The same weak signal as WP5a to WP5c: a smaller single reviewer, judging by reading, no finding on a high-risk package.

**What I checked myself, because the signal is weak.** (a) The packaged window itself was not launched: the flow runs against the mocked IPC and, in CI, WebKit; the backend half ran on the packaged sidecar (Section 25). (b) A household whose profile list fails to load is not shown setup (the profile banner shows instead); that is a deliberate "do not guess" and is untested. (c) "Run setup again" re-shows the privacy notice and the key section; it cannot erase or overwrite anything. (d) Setup replaces the main area, so while it is open no other view is reachable; the Finish button is the only way out and it is always enabled on the last step.

---

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.13 | 15 October 2026 | Claude Engineering Implementer | WP5d implementation review recorded (Pass, Info only; Section 27). |
| 0.12 | 15 October 2026 | Claude Engineering Implementer | WP5c post-commit record (289124a) and WP5d built: first-run flow (Sections 24 to 26). |
| 0.11 | 15 October 2026 | Claude Engineering Implementer | WP5c implementation review recorded (Pass, Info only) and one gap found and fixed by the Engineer (open Claude offers dropped on erasure); Section 23. |
| 0.10 | 15 October 2026 | Claude Engineering Implementer | WP5c built and live-checked on the rebuilt packaged sidecar: per-profile export and erasure (Sections 21 and 22). |
| 0.9 | 15 October 2026 | Claude Engineering Implementer | WP5b post-commit record (262b7f6): pre-check PASS, CI green apart from the five known microphone tests, post-commit review Pass (Section 20). |
| 0.8 | 15 October 2026 | Claude Engineering Implementer | WP5b implementation review recorded (Pass, Info only; Section 19). |
| 0.7 | 15 October 2026 | Claude Engineering Implementer | WP5b built (note sharing screen, audit retention); build record and commit contents (Sections 17 and 18). |
| 0.6 | 15 October 2026 | Claude Engineering Implementer | WP5a post-commit record (8cb21e7): pre-check PASS, CI green apart from the five known microphone tests, post-commit review Pass (Section 16). |
| 0.5 | 15 October 2026 | Claude Engineering Implementer | WP5a implementation review recorded (Pass, Info only; a weak signal, disclosed) - Section 15. |
| 0.4 | 15 October 2026 | Claude Engineering Implementer | Design approval recorded (Section 12); WP5a built and live-checked (Sections 13 and 14). |
| 0.3 | 15 October 2026 | Claude Engineering Implementer | WP5 design re-check recorded (Pass); status line updated. |
| 0.2 | 15 October 2026 | Claude Engineering Implementer | Design review addressed: no consent decision deleted by erasure; the runtime key change redesigned as a credential source plus a health switch instead of re-registration; pending proposals discarded; audit pruning under the recorder's lock; skip path on every step but the first; Adult export limited to their own in the backend. Section 10A review record. |
| 0.1 | 13 October 2026 | Claude Engineering Implementer | Initial design for WP5, drafted at the Programme Sponsor's request. Eleven decisions with recommendations (K1-K5, R1, E1, X1, F1, P1, S1). Nothing built. |
