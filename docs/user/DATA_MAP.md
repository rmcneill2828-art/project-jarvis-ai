# JARVIS Data Map

**Version 1.0, 9 November 2026, for JARVIS Guardian Shell 0.2.1.**

This is the full list of what JARVIS keeps, where it is kept, how long, how it is deleted, and whether it ever leaves the computer. The user guide, the parents' guide and the "Children and privacy" page are written from it. A test in the code (`jarvis/tests/test_data_map.py`) fails if a new table, added column, named file or folder, or `https://` address appears in the code without being named here; the test's own description lists what it does not scan.

`~/.jarvis` means the `.jarvis` folder in the computer user's home folder:

* **Windows:** `C:\Users\<your user name>\.jarvis`
* **macOS:** `/Users/<your user name>/.jarvis`

Each computer has its own copy. Nothing is shared between computers, and nothing is sent to the developer of JARVIS.

---

## 1. Profiles and safety: `~/.jarvis/identity/profiles.db`

| Table | What it holds | How long | Deleted by |
|---|---|---|---|
| `profiles` | Each profile's name (as typed), role (Administrator, Adult, Child or Guest), when it was made, and whether its notes may go with a Claude question (`share_memory_with_cloud`, off unless an Administrator turns it on). **No age, birthday, photo, email or password.** | Until the profile is erased | Erasing the profile |
| `active_profile` | Which profile is selected now | Until another is chosen, JARVIS restarts or the idle lock signs out | Automatic |
| `admin_pin` | The Administrator PIN as a **scrypt hash** with its salt, never the PIN itself; when it was set; the count of wrong tries and any lock-out time | Until the PIN is changed or reset | Changing or resetting the PIN |
| `pin_notices` | That the PIN was set or reset, and how many wrong tries there were, for the next Administrator to see. A "PIN set" notice holds **the name of the Administrator who set it** | Until an Administrator signs in and sees them | Shown once, then removed. Erasing that Administrator's profile does not remove a notice not yet shown |
| `safety_events` | When the safety checker stopped something: **a category label** (stored as a code such as `indiscriminate_weapons`, shown as "Weapons that can harm many people"), whether it was the message or the answer, the time, and the profile. **Never the words.** | The activity log setting: 30, 90 (the default) or 365 days | Automatically after that; erasing the profile |
| `child_consents` | That an Administrator allowed a Child profile to ask Claude: who allowed it, when, when the child said they understood, and when it was turned off (kept as history) | Until the child's profile is erased | Erasing the child's profile |
| `child_disclosures` | When a Child profile said it understood the "You are talking to JARVIS, an AI" explanation | Until the profile is erased | Erasing the profile |

## 2. Notes (memory): `~/.jarvis/memory/personal.db`

| Table | What it holds | How long | Deleted by |
|---|---|---|---|
| `personal_memory` | Notes JARVIS was allowed to keep, each **only after the person agreed**, for one profile (`profile_id`) or, if an Adult or Administrator chose, for the whole household (no `profile_id`). **This version of the app cannot save a new note**: notes arrive only by restoring a backup | Until deleted | Deleting the note in Memory; erasing the profile (its own notes, not household notes) |
| `consent_decisions` | The record that each note was agreed: what kind of request, yes or no, when, a label, and the safety layer's reason. **No profile and no note text.** | Kept | Not deleted when a profile is erased |

## 3. Other files in `~/.jarvis`

| File or folder | What it holds | How long | Deleted by |
|---|---|---|---|
| `memory/backups/` (or the folder chosen) | Memory backups an Administrator made: **every note at that time, including notes of profiles erased since** | Until deleted by hand | Deleting the files |
| `memory/settings.json` | Settings, such as how many days the activity log is kept | Kept | Uninstalling and deleting `~/.jarvis` |
| `memory/spend.db` | Claude spending for each month (table `spend`): totals in money and requests. **No profile and no text.** | Kept | Deleting `~/.jarvis` |
| `memory/ollama_model.json` | Which local AI model was chosen | Kept | Choosing another |
| `logs/audit.jsonl`, and up to 3 older copies (`audit.jsonl.1` to `.3`, 5 MB each) | The activity log: what happened (a safety decision, which AI answered, a question sent to Claude), when, the outcome, the role and counts. **Not what was said.** | 30, 90 (default) or 365 days | Automatically after that, in every copy |
| `logs/backend.log` | Technical messages for fixing problems, such as an error type | Up to 4 files of 5 MB, the oldest replaced | Automatic |
| `models/` | The voice files (Kokoro for speaking, Whisper for listening) and `verified.json`, the record that they were checked | Until deleted | Deleting the folder |
| `transcripts/` | **Only the old developer window ("First Light")**, which is not in the installer, saves transcripts here. The installed app never does. | - | - |

## 4. Outside `~/.jarvis`

| Where | What | How long | Deleted by |
|---|---|---|---|
| Windows Credential Manager or macOS Keychain, entry for JARVIS | The Claude API key, if one was saved in Settings | Until removed | Settings, Claude, **Remove key**; or the system's own tool |
| A folder the person chooses | **Profile exports**: a readable file (Markdown) and a portable file (JSON) holding that profile's notes and household-safety records | Until deleted by hand | Deleting the files |
| Ollama's own folder (`~/.ollama`) | The local AI models, downloaded and stored by Ollama, a separate program | Until removed in Ollama | Ollama |
| The JARVIS app's memory while it runs | The **conversation**: the last six exchanges for each profile | Gone when JARVIS closes, or the profile is erased | Closing JARVIS |
| Environment variables (developers only) | `ANTHROPIC_API_KEY` (a key instead of the keychain), `JARVIS_HOME_ASSISTANT_TOKEN` and `JARVIS_HOME_ASSISTANT_URL`, `JARVIS_OLLAMA_ENDPOINT`, `JARVIS_*_PATH` and `JARVIS_LOG_DIR` (other folders), `JARVIS_CLAUDE_MONTHLY_CAP_GBP` | As set | Removing the setting |

## 5. What erasing a profile removes, and what it leaves

An Administrator erases a profile under Settings, Your data.

**Removed:** the profile; its own notes; its conversation; its pending note proposals and open Claude offers; its Claude consent records and its "I understand" record; its safety events.

**Overwritten, not just hidden:** when a profile is erased or a note is deleted, JARVIS overwrites the deleted data in the database files and rebuilds them, so no copy is left inside `profiles.db` or `personal.db` or their `-wal` files. This was checked on a real run: after erasing a profile, neither its name nor its notes could be found anywhere in the two files. If another part of JARVIS is reading the database at that moment, the last step (emptying the `-wal` file) can wait until SQLite next does it on its own, at the latest when JARVIS closes; older copies may sit in that file until then. Other deletions (the activity log's daily clean-up, replacing notes from a backup) are overwritten the same way, with that same wait.

**Left, and how to remove it:**

| Left | Why | To remove it |
|---|---|---|
| Household notes | They belong to the household, not the profile | An Administrator deletes them in Memory |
| `consent_decisions` rows | They hold no name or text: they record that a note was agreed | Not needed: nothing in them identifies the person |
| Earlier memory backups | A backup is a copy made at a time; JARVIS does not change copies | Delete the backup files made before the erasure |
| Profile exports | They are files the person saved | Delete them from where they were saved |
| Activity log lines | They hold a role, not a name; deleted on schedule | Wait for the chosen number of days |
| Monthly Claude spending | Totals only, no profile | Not needed |
| The Claude key | It belongs to the household, not a profile | Settings, Claude, **Remove key** |
| Anything already sent to Claude | It is with Anthropic | Anthropic deletes it under its own terms (Section 6) |
| Copies made by the computer's own backup (File History, OneDrive, Time Machine, iCloud) | JARVIS cannot see or change those copies | Remove them with that backup tool, or keep `~/.jarvis` out of it |

## 6. What leaves the computer

| Destination | When | What is sent |
|---|---|---|
| **Nowhere** | An ordinary question | Nothing. JARVIS answers with the local AI model through Ollama at `http://localhost:11434` (on the same computer). The safety checker also runs there. |
| **Anthropic, `https://api.anthropic.com`** (the Claude API, model Claude Sonnet 5.5) | Only when JARVIS offers to ask Claude, a person allowed to use it **confirms that one question**, and the monthly allowance has room | The question; JARVIS's instructions to the model; **that profile's last six exchanges**, including ones answered on the computer, which may contain a name; the profile's notes **only if** sharing is on for that profile, and **never for a Child**. A Guest can never ask Claude; a Child only with an Administrator's consent and their own "I understand". |
| Ollama's library, through Ollama | An Adult or Administrator downloads a local AI model | A download request. Nothing personal. |
| `https://github.com` and `https://huggingface.co` | An Adult or Administrator downloads the voice | Download requests, marked `JARVIS-voice-setup`. Nothing personal. As with any download, the site sees the computer's internet address. |
| `https://ollama.com` | Someone presses the button to get Ollama | The page opens in the web browser |
| `https://rmcneill2828-art.github.io/AI-Project/` | Never by JARVIS: the Claude-for-a-child screen shows this page's address as text to copy | Nothing |
| The household's Home Assistant, if a developer set it up | A question about the home | The request goes to that address on the household's own network |

**Not contacted:** JARVIS has no analytics, no crash reports and no update check. Code for two other AI services (`https://api.openai.com`, `https://generativelanguage.googleapis.com`) is still in the project from earlier versions but is **not switched on** in the app, which never contacts them. A developer setting, `JARVIS_OLLAMA_ENDPOINT`, can point JARVIS at Ollama on another computer; the installed app uses this computer's.

**Anthropic's handling** (read from Anthropic's own pages on 9 November 2026): Anthropic deletes API inputs and outputs within 30 days, except that it keeps them up to 2 years if its automated systems flag them as breaking its usage policy, or longer where the law requires ([How long do you store my organization's data?](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), updated 1 July 2026). Its commercial terms say: "Anthropic may not train models on Customer Content from Services" ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)). Anthropic is a company in the United States, so what is sent leaves the UK.

## 7. Uninstalling

Uninstalling JARVIS removes the app, not `~/.jarvis`. To remove everything: uninstall, then delete `~/.jarvis`, any exports and backups saved elsewhere, and the JARVIS entry in Credential Manager or Keychain Access. Ollama and its models are removed with Ollama.
