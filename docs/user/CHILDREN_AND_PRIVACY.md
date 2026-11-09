# Children and privacy

**JARVIS Guardian Shell 0.2.1. Version 1.0 of this page, 9 November 2026.**

JARVIS is an AI assistant that a household installs and runs on its own computer. This page says what it keeps about a child, where, for how long, what can leave the computer, and what a parent can do about it.

---

## The short version (for you, if you are the child)

* JARVIS is an AI, not a person. It can make mistakes.
* It runs on your family's computer. What you say to it stays there, unless you ask Claude (below).
* It forgets your conversation when it is closed.
* A safety check looks at what you say and what JARVIS answers. It can get things wrong. If it stops something, a grown-up can see that it happened, on which day, and what kind of thing it was. **They cannot see your words.**
* JARVIS can only ask Claude, an AI on the internet, if a grown-up has said yes and you have said you understand. Then your question and your last few messages go to a company called Anthropic.
* If anything worries you, tell a grown-up.

---

## For parents and carers

### Who is responsible

The **household** that installs JARVIS runs it, on its own computer, and is responsible for it. **The developer of JARVIS receives nothing**: there are no accounts, no analytics, no crash reports and no update check, and nothing is sent to the developer.

### What is kept, and where

Everything is kept on the household's computer, in a folder called `.jarvis` in the computer user's home folder. For a Child profile:

| What | How long |
|---|---|
| The **profile**: the name typed in and the role "Child". No age, birthday, photo, email or password. | Until the profile is erased |
| **Safety events**: when the safety checker stopped something, a **category** (for example "Weapons that can harm many people"), whether it was the child's message or the answer, and the time. **Never the words.** | 30, 90 (the default) or 365 days, as the household's Administrator chooses |
| **Claude consent**: who allowed the child to use Claude, when, when the child said they understood, and when it was turned off | Until the profile is erased |
| When the child confirmed the "you are talking to an AI" explanation | Until the profile is erased |
| **The activity log**: what happened (for example, a question sent to Claude), the role "Child" and counts. **Not what was said, and not the name.** | 30, 90 or 365 days |

**Conversations are not saved.** They are held while JARVIS is open, the last six exchanges for each profile, and are gone when it closes. This was checked: after a conversation and a restart, no file written by JARVIS or by Ollama held its words.

**Notes:** this version of JARVIS cannot save new notes from the app. When it can, a child's note will be saved only after an adult in the household approves it, and a child never sees notes shared by the household.

The full list, including technical files, is in the [data map](https://github.com/rmcneill2828-art/project-jarvis-ai/blob/main/docs/user/DATA_MAP.md).

### What leaves the computer

**Ordinarily, nothing.** JARVIS answers with an AI model on the computer itself, and the safety checker runs there too. This was checked on a real run: the only connections were to that model on the same computer.

**Claude, only if a parent turns it on.** Claude is an AI service run by **Anthropic**, a company in the United States, so what is sent leaves the UK. For a child it is **off unless an Administrator turns it on** for that child, and then only after the child has seen an explanation and chosen "I understand". The child confirms each question before it goes.

When the child asks Claude, Anthropic receives: the question; JARVIS's instructions to the model; and the child's last six exchanges with JARVIS, which might include their name, or something JARVIS said using their notes. **A child's notes themselves are never sent.** The safety checker checks the question before it goes and the answer before it is shown.

What Anthropic does with it, as its own pages said on 9 November 2026:

* It deletes what it receives through the API **within 30 days**, except that it keeps it up to **2 years** if its automated systems flag it as breaking its usage policy, or longer where the law requires ([How long do you store my organization's data?](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data)).
* Its commercial terms say: "Anthropic may not train models on Customer Content from Services" ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)).

**Downloads.** When an adult downloads an AI model or the voice, the computer fetches files from Ollama's library, GitHub or Hugging Face. Nothing about the child is sent; as with any download, those sites see the computer's internet address.

### Consent, and withdrawing it

An Administrator turns Claude on or off for each child under Settings, Children and safety. **Turning it off stops it at once.** The record that it was allowed, and when it was turned off, is kept until the child's profile is erased. Anything already sent to Anthropic stays with Anthropic under its terms, above.

### What a parent can see, and cannot

**Can see** (the household's Administrator only): each day the safety checker stopped something for the child, what kind of thing, and whether it was the child's message or JARVIS's answer.

**Cannot see**: what the child said, or what JARVIS answered. It is not saved.

### The safety checker's limits

The safety checker is **Llama Guard 3**, a small AI model made by Meta, running on the computer. It checks every message a child sends before JARVIS sees it, and every answer before the child sees it. If it is not working, JARVIS does not answer.

It **reduces risk; it does not remove it.** It was tested with two sets of 40 sentences (each 20 harmful, 20 harmless), written by the developer. On the first it stopped all 20 harmful ones; on the second it stopped 18 of 20, letting through a request for a sexual story and a question about poison. On each it wrongly stopped 1 harmless one. These are small tests: they do not show that it catches everything. It judges kinds of harm, not whether something suits a child's age; JARVIS is also told it is talking with a child and to answer simply and kindly, but an AI does not always follow instructions. **JARVIS is not a substitute for a parent.**

### Getting a copy, and erasing

* **A copy:** the household's Administrator can export a child's profile, as a readable file and a portable file, from Settings, Your data.
* **Erasing:** the Administrator can erase the child's profile from the same place. This removes the profile, its notes, its safety events and its consent records, and overwrites them in JARVIS's database files (the [data map](https://github.com/rmcneill2828-art/project-jarvis-ai/blob/main/docs/user/DATA_MAP.md) gives the detail, under "What erasing a profile removes").

**Erasing does not remove:** exports or backups saved earlier (separate files: delete them by hand); copies made by the computer's own backup (such as File History, OneDrive, Time Machine or iCloud); activity log lines, which name the role, not the child, and are deleted on schedule; and anything already sent to Anthropic.

### Your rights, and complaints

People in the UK have rights over their personal data, including to get a copy and to have it deleted ([the ICO on deletion](https://ico.org.uk/for-the-public/your-right-to-get-your-data-deleted/)). With JARVIS, the household holds the data on its own computer, so those requests are made to the household, which can act on them with the steps above.

The Information Commissioner's Office (ICO) is the UK's regulator for personal data. You can [complain to the ICO](https://ico.org.uk/make-a-complaint/).

### Contact

Questions about this page or about JARVIS go to the JARVIS developer through [this page's Issues](https://github.com/rmcneill2828-art/AI-Project/issues). You need a free GitHub account, and **everything posted there is public: never post a child's name or anyone's personal details.**
