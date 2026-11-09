# JARVIS User Guide

**Version 1.0, 9 November 2026, for JARVIS Guardian Shell 0.2.1.**

JARVIS is an AI assistant that runs on your own computer. It answers with an AI model on the computer itself. It can also ask Claude, a service on the internet, but only when you confirm one question at a time. The [data map](DATA_MAP.md) lists everything JARVIS keeps; the [parents' guide](PARENTS_GUIDE.md) covers children.

---

## 1. Install

Download the installer from the release page and check it before running it. Each installer has a `.sha256` file beside it holding its checksum.

| | Windows | macOS (Apple silicon) |
|---|---|---|
| File | `JARVIS.Guardian.Shell_0.2.1_x64-setup.exe` | `JARVIS.Guardian.Shell_0.2.1_aarch64.dmg` |
| Check it | In PowerShell: `Get-FileHash .\JARVIS.Guardian.Shell_0.2.1_x64-setup.exe` | In Terminal: `shasum -a 256 JARVIS.Guardian.Shell_0.2.1_aarch64.dmg` |
| | The result must match the `.sha256` file. If it does not, do not run it. | The same |
| Install | Run the installer | Open the `.dmg` and drag JARVIS to Applications |
| The first warning | JARVIS is not signed with a paid certificate, so Windows SmartScreen warns. Choose **More info**, then **Run anyway**. | The first time, macOS refuses to open it. Open **System Settings, Privacy & Security**, find JARVIS near the bottom and choose **Open Anyway**. It does not ask again. macOS 13 or later is needed. |

JARVIS also needs **Ollama**, a separate free program that runs AI models on the computer. JARVIS tells you if it is missing and has a button to open its download page.

## 2. First run

A short setup runs the first time:

1. **Your profile.** The first person is the **Administrator**, who manages JARVIS for the household. Type a name; nothing else is asked (no age, email or password).
2. **Administrator PIN.** Choose 6 to 12 digits. You can do this later, but until a PIN is set, the household safety rules are not enforced (see Section 4).
3. **AI on this computer.** JARVIS checks Ollama and recommends a model that suits the computer.
4. **Claude.** Optional; see Section 7.
5. **Ready.** What is set up and what is still missing.

## 3. Profiles and roles

Each person has their own profile. Only an Administrator can add one, under **Settings, Add a profile**, once a PIN is set.

| | Administrator | Adult | Child | Guest |
|---|---|---|---|---|
| Talk to JARVIS | Yes | Yes | Yes, with the safety checker and child-friendly answers | Yes, with the safety checker |
| Download AI models and the voice | Yes | Yes | No | No |
| Ask Claude | Yes | Yes | Only if an Administrator allows it and the child says they understand | Never |
| See household notes | Yes | Yes | No | No |
| Export data | Any profile | Their own | No | No |
| Back up, restore, erase profiles, set the PIN, see safety events | Yes | No | No | No |

To change profile, use the profile button at the top. Switching **to** an Administrator needs the PIN, and so does leaving a Child or Guest profile for an Adult one.

## 4. The Administrator PIN

* It is stored only as a scrambled hash, never as the PIN itself.
* After 5 wrong tries it locks for 30 seconds, then twice as long after each further 5, up to 10 minutes. The next Administrator to sign in is told how many wrong tries there were.
* Change it under **Settings, Administrator PIN**.
* **The idle lock:** once a PIN is set, an Adult or Administrator left idle for 15 minutes is signed out.
* It is a lock inside JARVIS, not on the computer. Anyone who can open the computer's files can still reach JARVIS's data, so give each person their own computer account, or lock the computer when you leave it.

**If the PIN is forgotten**, reset it from the command line on the computer. Close JARVIS first.

* **Windows** (PowerShell): `& "$env:LOCALAPPDATA\JARVIS Guardian Shell\jarvis-backend.exe" --reset-admin-pin` (this is the installer's usual folder; if you chose another when installing, use that)
* **macOS** (Terminal): `"/Applications/JARVIS Guardian Shell.app/Contents/MacOS/jarvis-backend" --reset-admin-pin`

This removes the PIN; set a new one in Settings. The next Administrator to sign in is told the PIN was reset, so a reset is never silent. Anyone who can use the computer's account can run this command, which is why the notice exists.

**If the household has no Administrator** (only possible in a household set up with an early version), the same program adds one: use `--add-administrator "Name"` in place of `--reset-admin-pin`. It refuses if there is already an Administrator.

## 5. AI on this computer

Under **Settings, Local AI**, JARVIS shows whether Ollama is running, which model is in use, and the model it recommends for this computer. An Adult or Administrator can download and switch models. The same screen downloads the **safety checker** (Llama Guard 3), which Child and Guest profiles need: without it, they get no answers.

The first answer after starting can take longer while the model loads.

## 6. Voice

Under **Settings, Voice**, an Adult or Administrator downloads two voice files once: **Kokoro** (JARVIS reads its replies aloud) and **Whisper** (you can speak a question instead of typing). They come from GitHub and Hugging Face. Speech and listening both happen on the computer; nothing you say is sent anywhere to be heard.

To hear a reply, use its speaker button. To speak, use the microphone button; the computer may ask for permission the first time.

## 7. Claude

Claude is an AI service run by Anthropic, a company in the United States. JARVIS never sends anything to Claude unless you confirm.

* **The key:** an Administrator saves a Claude API key under **Settings, Claude**. It is kept in Windows Credential Manager or the macOS Keychain, not in a file. **Remove key** deletes it.
* **Asking:** JARVIS offers Claude when its own model could not answer or when Claude may give a more thorough answer, and there is an **Ask Claude** button. Either way, a screen shows what will be sent, and nothing goes until you confirm. Answers from Claude carry a **Claude** label.
* **What is sent:** your question, JARVIS's instructions to the model, and your last six exchanges with JARVIS, which may include your name. Your notes are sent only if an Administrator has turned on sharing for your profile under **Settings, Notes and Claude**, and never for a Child.
* **Cost:** asking Claude costs money. The monthly allowance is £30 unless changed, and what is left is shown before you confirm. When it is used up, JARVIS stops asking until the next month.
* **What Anthropic keeps:** see the [data map](DATA_MAP.md), Section 6.

## 8. Notes

**This version cannot save a new note from the app.** The **Memory** view shows notes restored from a backup, and you can remove any of your own. An Administrator can also remove notes shared by the whole household. Saving notes from a conversation, each one only after a person agrees, is planned for a later version.

## 9. Your data: export, backup, restore, erase

* **Export** (Settings, Your data): a profile's notes and its household-safety records, as a readable file (Markdown) and a portable file (JSON), saved to a folder you choose. An Adult can export their own; an Administrator any profile.
* **Backup and restore** (Memory, Memory Management, Administrator only): a backup is a copy of every note at that moment. Restoring replaces the notes with those in the backup, and asks first if there are notes already.
* **Erase a profile** (Settings, Your data, Administrator only, typing the profile's name to confirm): removes the profile and everything of its own. JARVIS overwrites the erased data in its files, not just hides it. Exports and earlier backups are separate files and are **not** changed; delete them yourself. The [data map](DATA_MAP.md), Section 5, lists exactly what stays.
* **The activity log** (Settings, Activity log) records what happened, never what was said, and is deleted after 30, 90 (the default) or 365 days.

## 10. Uninstalling

Uninstalling removes the app, not your data. To remove everything, also delete the `.jarvis` folder in your home folder, any exports and backups, and the JARVIS entry in Credential Manager or Keychain Access. Ollama is removed separately.

## 11. When something goes wrong

| What you see | What to do |
|---|---|
| "Ollama is not installed" | Install Ollama from its download page (the button in Settings, Local AI), then check again |
| "Ollama is installed but not running" | Open Ollama, then check again |
| A Child or Guest is told "I can't check that it is safe to answer right now" | The safety checker is missing or not running. Download it in Settings, Local AI, and make sure Ollama is running |
| Voice says "The files are damaged" or "Could not start" | Choose **Download again** in Settings, Voice |
| The microphone does nothing | Allow JARVIS to use the microphone: Windows Settings, Privacy & security, Microphone; or macOS System Settings, Privacy & Security, Microphone |
| "The monthly allowance for asking Claude has been used up" | Wait for the next month; JARVIS still answers on the computer |
| The PIN is forgotten | Section 4 |
