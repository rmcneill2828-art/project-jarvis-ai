# ADR-0023 - Version 1.0 Provider Strategy

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ADR-0023 |
| Title | Version 1.0 Provider Strategy |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Decision Date | 2 October 2026 (recorded at ESR-0061 WP1a) |
| Related | [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] (principle unchanged), [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Sections 3 and 5 |

---

# 1. Context

Version 1.0 will be used in a UK household by adults and by a 15-year-old under the Child role, on Windows and macOS, and then released publicly. Today a fresh install has no working provider unless API keys are set in environment variables. Each provider's own terms decide whether a family app with a minor may use it.

# 2. Decision

| Tier | Provider | When | Child role |
|---|---|---|---|
| Default | **Local Ollama** on each machine | Every conversation unless escalated | Yes, with local moderation |
| Escalation | **Anthropic Claude API** (user's own API key) | Research, knowledge or harder questions - **suggested by JARVIS and confirmed by the user, never automatic** (D28) | Yes, only with recorded parental consent, moderation and AI disclosure |
| Unregistered | OpenAI API | - | - (D25) |
| Unregistered | Google Gemini API | - | - (D27) |

1. Claude escalation spend is capped at **£30 per month** (D26): set in the Anthropic Console and also enforced by JARVIS, which falls back to local Ollama at the cap. This is the plan's only recurring cost and an explicit exception to the no-discretionary-budget rule.
2. Unregistered adapters are kept, with their tests, but not wired into the runtime (the Piper precedent, ESR-0053), so these decisions can be reversed.
3. Subscription and coding-agent tools (Claude Code, GitHub Copilot, Codex, Antigravity) are **not** product backends. They remain engineering tools only.
4. ADR-0008's hybrid local-plus-cloud principle is unchanged; this ADR selects the concrete Version 1.0 providers.

# 3. Evidence - provider terms, read 2 October 2026

| Source | Relevant text (quoted) | Consequence |
|---|---|---|
| Anthropic Consumer Terms (anthropic.com/legal/consumer-terms) | "You must be at least 18 years old to use the Services." Prohibited: "Except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services through automated or non-human means". "You may not share your Account login information, Anthropic API key, or Account credentials with anyone else or make your Account available to anyone else." | A Claude subscription cannot power JARVIS for anyone else, least of all a minor. API key only. |
| Anthropic - organisations serving minors (support.claude.com article 9307344) | Permitted with safeguards: "Age verification systems to ensure only intended users can access the product"; "Content moderation and filtering to block inappropriate or harmful content"; regulatory compliance documented publicly; users informed "they are interacting with an AI system rather than a human". | The Claude API may serve the Child role if these safeguards exist: Administrator PIN (WP6), local moderation (WP6), a public "Children and privacy" page (WP8), AI disclosure (WP4/WP6). |
| Gemini API Terms (ai.google.dev/gemini-api/terms) | "You must be 18 years of age or older to use the APIs." "You also will not use the Services as part of a website, application, or other service... that is directed towards or is likely to be accessed by individuals under the age of 18." | A family app with a Child role is likely to be accessed by under-18s, so the Gemini API leaves the product (D27). Gemini **CLI** for engineering review is a separate question (PBK-0001 Independent Reviewers). |

Not verified: GitHub Copilot, OpenAI Codex and Google Antigravity product terms. They are excluded as product backends on practical and security grounds regardless: they are coding agents with file and shell access, they would consume the engineering review quota, and other households cannot use the Programme Sponsor's subscriptions.

# 4. Consequences

* Go-live plan WP3 builds `sentinel/anthropic_provider.py` (matching the existing adapters' retry, circuit and deadline semantics), makes Ollama the default route with detection, guided install, in-app model pull and a hardware-based model recommendation, adds suggested-then-confirmed escalation with a visible "answered by Claude" indicator, enforces the spend cap, and unregisters OpenAI and Gemini.
* WP6 delivers the safeguards Anthropic requires for minors; WP8 publishes the "Children and privacy" page.
* Household data follows UK GDPR principles as the design standard (D23): local processing by default is the strongest position.
* Review trigger: any change of escalation provider, a material change to any cited terms, or the cap proving insufficient.

# Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 6 October 2026 | Claude Engineering Implementer | Created at ESR-0061 WP1a per EIP-ESR0061-001, recording Programme Sponsor decisions D25-D28 of 2 October 2026 and the provider terms read that day. |
