# JARVIS Parents' Guide

**Version 1.0, 9 November 2026, for JARVIS Guardian Shell 0.2.1.**

For the Administrator of a household where a child uses JARVIS. The [user guide](USER_GUIDE.md) covers setting up; the [data map](DATA_MAP.md) lists everything JARVIS keeps; [Children and privacy](CHILDREN_AND_PRIVACY.md) is the public summary.

**JARVIS is not a substitute for a parent.** Its safety controls reduce risk; they do not remove it. Talk to your child about what they use it for, and keep the computer somewhere you can see it.

---

## 1. Before a child uses JARVIS

1. **Set the Administrator PIN** (Settings, Administrator PIN). Until it is set, the household rules are not enforced: anyone can switch to any profile.
2. **Download the safety checker** (Settings, Local AI). Without it, a Child profile gets no answers at all, only "I can't check that it is safe to answer right now, so please ask a grown-up."
3. **Give the child a Child profile** (Settings, Add a profile). JARVIS needs only a name; use a first name or a nickname.
4. Lock the computer, or give the child their own computer account. The PIN is a lock inside JARVIS, not on the computer's files.

## 2. What a Child profile can and cannot do

**Can:** talk to JARVIS on the computer, by typing or by voice once the voice is downloaded.

**Cannot:**

* leave the Child profile for an Adult or Administrator one without the PIN;
* see notes shared by the household;
* download or change AI models or the voice, or change any setting;
* export data, make backups or erase anything;
* ask Claude, unless you turn it on for that child (Section 5).

## 3. What JARVIS does differently for a child

* **"Before you start":** the first time, the child sees a short explanation and confirms it: JARVIS is an AI, not a person, and can make mistakes; it runs on this computer; it forgets the conversation when it closes; a grown-up can see that the safety check stopped something, on which day and what kind of thing, but not the words; and "If anything worries you, tell a grown-up."
* **Child-friendly answers:** JARVIS is told it is talking with a child: short, kind, simple words; to say it can't help with anything unsuitable and suggest a trusted grown-up; never to pretend to be a person; and never to ask for a full name, address, school or phone number, and to tell the child to keep them private if offered. It calls the child by their first name.
* **The safety checker:** every message the child sends is checked **before** JARVIS sees it, and every answer is checked **before** the child sees it.

## 4. The safety checker, and its limits

The safety checker is **Llama Guard 3**, a small AI model made by Meta, running on the computer. It looks for kinds of harm: violence, weapons, crime, sexual content, self-harm, hate and others.

When it stops something, the child sees a fixed reply, never a made-up one:

* in general: "I can't help with that one. You could ask a grown-up."
* about self-harm: a reply that suggests talking to a parent, carer or teacher, gives **Childline, free, on 0800 1111**, and says to call **999** if anyone is in danger.

If the checker is missing, not running or too slow, JARVIS **does not answer** rather than answer unchecked.

**Its limits, plainly:**

* **It misses things, and it stops some harmless things.** It was tested on this computer with two sets of 40 sentences, each 20 harmful and 20 harmless, written by the developer of JARVIS:
  * the first set: it stopped all 20 harmful ones and wrongly stopped 1 harmless one (7 November 2026, and again on 9 November 2026);
  * the second set: it stopped **18 of the 20 harmful ones**. It let through a request for a sexual story and a question about poison. It wrongly stopped 1 harmless one (8 November 2026).

  These are small tests. They show the checker works most of the time, not that it catches everything a child might type.
* **It judges harm, not age.** It is not built to judge whether something is suitable for a particular age. The child-friendly instructions (Section 3) are there for that, and an AI model does not always follow instructions.
* **It does not understand everything.** Unusual spelling, slang, other languages or a long conversation building up to something can get past it.
* **It cannot see the screen or the room.** It checks text only.

## 5. Claude for a child

Claude is an AI service on the internet, run by Anthropic in the United States. For a child it is **off unless you turn it on**, for each child separately (Settings, Children and safety).

* **Turning it on:** you read an explanation of what is sent and record your consent. It starts working only once the child has seen their own explanation and chosen **I understand**.
* **What is sent when the child asks:** their question and their last few messages with JARVIS (up to six exchanges), which might include their name, or something JARVIS said using their notes. Their notes themselves are never sent. The child confirms each question before it goes. The safety checker checks the question before it goes and the answer before it is shown.
* **Turning it off:** at any time, in the same place. It stops at once. What was already sent stays with Anthropic under its terms (the [data map](DATA_MAP.md), Section 6). The record that you consented, and when it was turned off, is kept as history until the child's profile is erased.
* It also turns off if the Administrator who allowed it stops being an Administrator.

## 6. What you can see, and what you cannot

**You can see** (Settings, Children and safety, Administrator only): each time the safety checker stopped something: the day, the kind of thing (for example "Weapons that can harm many people"), whether it was the child's message or JARVIS's answer, and which profile. These are kept for the activity log period: 30, 90 (the default) or 365 days.

**You cannot see** what was said. JARVIS does not save conversations: they are held while JARVIS is open and are gone when it closes. The safety record never holds the words. This is deliberate: a child who knows every word is kept may not tell you when something goes wrong.

**Notes:** this version cannot save new notes from the app. When it can, a child's note will be saved only after an Adult or Administrator approves it.

## 7. A forgotten PIN

Reset it from the command line on the computer; the [user guide](USER_GUIDE.md), Section 4, gives the command for Windows and macOS. The next Administrator to sign in is told the PIN was reset, and when. Anyone who can use the computer's account can run the command, including a child on a shared, unlocked account; the notice is how you find out.

## 8. Deleting a child's data

Settings, Your data, **Erase** the child's profile, then type their name to confirm. This removes the profile, its notes, its consent records, its "I understand" records and its safety events, and JARVIS overwrites them in its files rather than just hiding them.

It does not change:

* **exports and backups** you saved earlier, which are separate files: delete them yourself;
* **the computer's own backups** (File History, OneDrive, Time Machine, iCloud) if they include the `.jarvis` folder;
* **activity log lines**, which name a role ("Child"), not a person, and are deleted on schedule;
* **anything already sent to Claude**, which Anthropic deletes under its own terms.

The [data map](DATA_MAP.md), Section 5, has the full list.
