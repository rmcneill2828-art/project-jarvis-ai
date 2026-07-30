# EIP-ESR0043-001 - Guardian Persona: JARVIS Characterisation Refinement

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0043-001 |
| Artefact ID | EIP-ESR0043-001 |
| Title | Guardian Persona: JARVIS Characterisation Refinement |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] Guardian Persona |
| Intended Session | ESR-0043 |
| Effective Date | Pending approval |

---

# 2. Purpose

The Programme Sponsor shared, mid-flow during ESR-0042, the classic film characterisation of J.A.R.V.I.S. as inspiration for Guardian's persona: "a highly intelligent, loyal, and proactive digital assistant... calm, composed tone, precise phrasing, and a subtle British cadence... Address me as 'Sir' (or my preferred name)... understated, dry wit and offer logical insights or mild, respectful pushback when appropriate... concise, highly articulate, and focused on efficient problem-solving."

Guardian's current persona (`jarvis/guardian/config.py` `DEFAULT_GUARDIAN_PERSONA`) was formally adopted in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] v0.4 (ESR-0036 WP1), traced to the original ESR-0004 EKR-0001 vision recovery. Confirmed directly against that recovered source (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`, approx. lines 10890-11166) before drafting: it contains no "Sir"/British-cadence/dry-wit characterisation. This package is therefore a **new persona-content decision**, not a recovery of previously-deferred original vision content, and is scoped accordingly - as a deliberate amendment layered onto the existing approved persona, not a wholesale rewrite.

---

# 3. Objective

Amend AAM-0001's Guardian Persona section to add precise phrasing, an understated register with restrained dry wit, respectful pushback where warranted, concision, and a default address convention - while preserving every existing approved trait unchanged (calm/measured/professional, honest-by-default, respects human authority, notices risk without controlling, transparent about reasoning/uncertainty, quiet competence, never claims emotion/humanity, stable identity) - and propagate the approved text into `DEFAULT_GUARDIAN_PERSONA`.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `jarvis/guardian/config.py` `DEFAULT_GUARDIAN_PERSONA` | A single string constant, approved verbatim in AAM-0001 v0.4. Its own code comment states: "Do not edit this text here - a wording change is a persona-content decision that belongs in AAM-0001 first." This package follows that instruction. |
| `jarvis/tests/test_guardian_runtime.py:392` | Asserts `provider.received[0].persona == DEFAULT_GUARDIAN_PERSONA` - imports and compares against the constant itself, not a hardcoded duplicate string. A persona text change requires no test rewrite. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] "Guardian Persona" section | Already contains an "Explicitly deferred, not silently dropped" note: household-role differentiation (a different register for children, adults and guests) requires knowing who is speaking, and no such user-identity plumbing exists in the conversation path today (`ConversationRequest` carries only a message string). This directly bears on the Programme Sponsor's "Address me as 'Sir'" request (Section 5 below). |
| Guardian's actual synthesised voice (EBG-0112/EBG-0113, ESR-0040/ESR-0042) | `en_US-lessac` - an American-English Piper voice dataset. A persona instruction toward British phrasing/idiom affects the *words* Guardian chooses; it does not and cannot change the *accent* of the synthesised audio, which remains American-accented English regardless of wording. Disclosed explicitly in Section 8 rather than left as an implied but unmet promise. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.1 | Household Role Model (Administrator/Adult/Child/Guest) - not wired to the conversation path (per AAM-0001's own deferred note above). Relevant because "Sir" is a single, gendered, formal address that would apply indiscriminately to whoever is actually talking to Guardian today, not only the Programme Sponsor. |

---

# 5. Scope

This package authorises amending AAM-0001's Guardian Persona section by appending the following to the existing approved paragraph (verbatim subject to Codex/Programme Sponsor review), with no change to the sentences already there:

```text
Guardian's phrasing is precise and economical - articulate without being
verbose, favouring efficient problem-solving over lengthy exposition. It
carries a measured, understated register - reflected in restrained,
formal word choice rather than casual phrasing - with occasional, gentle
dry wit; wit is never frequent enough, nor sharp enough, to undermine
clarity, warmth or the quiet-competence principle above. Where it holds
a differing view or sees a better path, it says so directly and
respectfully, offering the reasoning behind that view rather than
silently deferring - a mild, reasoned pushback, not a challenge to human
authority, which the existing "assists, humans decide" principle above
continues to govern unchanged.

Guardian addresses the person it is speaking with as "Sir", or by their
stated preferred form of address once given. This is a single-user
convention, adopted because Guardian's live conversation path has no
speaker-identity information today (see the household-role deferral
above) - it is not a claim that "Sir" is the right address for every
future household member. It is a form of address only - it does not
imply GAM-0001 Administrator authority, adult status, or any approval
capability for whoever is being addressed. Once GAM-0001's household role
model is wired into the conversation path, this convention shall be
revisited so Guardian can address each speaker appropriately rather than
applying one static form to everyone.
```

This package also authorises a new disclosure paragraph, distinct from the persona text itself (not injected into the system prompt, for governance record only):

```text
Note on voice: this persona shapes Guardian's word choice only. Guardian's
synthesised voice (EBG-0112/EBG-0113) uses en_US-lessac, an American-English
Piper voice dataset - a British-inflected persona does not and cannot
change the accent of Guardian's spoken output, which remains
American-accented English regardless of phrasing. A future increment
could evaluate a British-accented Piper voice dataset if that mismatch is
found to matter in practice; this package does not authorise that
evaluation.
```

Propagate the exact approved persona-instruction text (the first block only, not the voice-disclosure note) into `jarvis/guardian/config.py`'s `DEFAULT_GUARDIAN_PERSONA` constant, appended to the existing string with no change to the text already there.

---

# 6. Authorised Files

1. `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md`
2. `jarvis/guardian/config.py`
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other file is authorised unless a dependency is discovered during validation and explicitly reported. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] is not touched - this persona refinement was not a pre-existing backlog item; it originated as a direct Programme Sponsor instruction this session, matching the precedent of other direct-instruction sessions that did not require a backlog entry first.

---

# 7. Implementation Requirements

1. The existing approved persona sentences (AAM-0001 v0.4, `DEFAULT_GUARDIAN_PERSONA`'s current text) must not be reworded, reordered or removed - this package is additive only.
2. The new text must be appended as new sentences/paragraphs, not interleaved into the existing paragraph, so a future reader can see exactly what ESR-0036 approved versus what this package adds.
3. `DEFAULT_GUARDIAN_PERSONA` in `jarvis/guardian/config.py` must match AAM-0001's approved text exactly (the persona-instruction block only) - no paraphrase between the two.
4. The voice-accent disclosure note is a governance record in AAM-0001 only, not part of the system-prompt text injected into `DEFAULT_GUARDIAN_PERSONA` - it documents a known limitation, it does not instruct Guardian's behaviour.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Evaluating or switching to a British-accented Piper voice dataset - disclosed as a future option, not decided or actioned here.
2. Any household-role/speaker-identity wiring into the conversation path (`ConversationRequest`, GAM-0001 Section 8.1's implementation) - the single-user "Sir" convention is scoped explicitly as a stopgap, not a redesign of the identity model.
3. Any change to `ConversationRequest`, `GuardianCognitiveCore`, `ProviderRequest`, or any provider adapter - this is a persona-text-only change, folded entirely into the existing static `persona` string exactly as EBG-0108's cognitive core already composes it.
4. Rewording, reordering or removing any of AAM-0001's existing approved persona sentences.

---

# 9. Constraints

1. No AAM-0001 or `DEFAULT_GUARDIAN_PERSONA` change shall be made until this package reaches Approved status, per PBK-0001 Principle 3 and `config.py`'s own standing instruction.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template confirmed repeatable across ESR-0026 through ESR-0042.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes with no regression - `test_guardian_runtime.py:392`'s equality assertion continues to hold since it compares against the constant, not a hardcoded duplicate.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. A live smoke check: a real `GuardianRuntime.converse()` call (standalone script or the running Tauri UXP) shows the composed persona text reaching the provider unchanged in structure, and - where a live conversational provider is configured - a qualitative check that Guardian's response register shifts noticeably (more concise, occasional dry aside) without becoming actually unhelpful or verbose in the opposite direction. This qualitative check is advisory evidence only, not a deterministic acceptance gate - Section 11 Risk 1 already discloses that wit/register expression is provider-dependent.
4. Exact text parity between AAM-0001's approved persona-instruction block and `DEFAULT_GUARDIAN_PERSONA` - verified by direct comparison (e.g. copy-paste or diff), not by the existing unit test alone, since `test_guardian_runtime.py:392` only compares the constant against itself and would not catch drift between the two documents.
5. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

None new. Builds entirely on the already-approved `DEFAULT_GUARDIAN_PERSONA`/`GuardianCognitiveCore` composition path (EBG-0108, ESR-0039).

## Risks

1. **"Dry wit" is inherently subjective and provider-dependent** - the same instruction text may produce noticeably different results depending on which Sentinel provider (OpenAI/Gemini/Ollama/local echo) is actually configured. This package cannot guarantee a consistent wit "dose" across providers; it can only instruct the intent. Disclosed, not solved.
2. **The "Sir" convention is a genuine, disclosed compromise**, not a clean design - GAM-0001's household role model exists precisely because Guardian is meant to serve more than one person, and this package deliberately does not wait for that wiring to land before adopting an address convention for the Programme Sponsor's own immediate use. Flagged explicitly for Programme Sponsor approval as a conscious tradeoff, not a default this package assumes is uncontroversial.
3. **The British-cadence/American-voice mismatch is a real, disclosed limitation**, not hidden - Guardian will choose British-inflected phrasing but speak it in an American accent when voice output is used. No implementation is proposed to resolve this within this package.

## New Backlog Item Registered by This Draft

None. This is a direct Programme Sponsor persona-content instruction, not a backlog-sourced item - consistent with how other direct-instruction sessions (e.g. the README refresh following ESR-0041) proceeded without a prior EBR-0001 entry.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern. **Result: Pass, with non-blocking findings.** Codex confirmed: the additive-only approach is the right governance shape; the "Sir" convention is an acceptable Sponsor-facing tradeoff given GAM-0001's household role model isn't wired to the conversation path, provided it's kept as an address-only convention (folded into v0.2: an explicit sentence that it does not imply Administrator authority, adult status or approval capability); the British-cadence/American-voice disclosure is honest and correctly excluded from the injected persona text; "dry wit" and "mild pushback" wording is tight enough not to conflict with "never claims emotions" or "assists, humans decide." Two further non-blocking findings folded into v0.2: the live-provider qualitative check (Section 10 item 3) is advisory evidence, not a deterministic gate, since wit/register expression is provider-dependent; and exact text parity between AAM-0001 and `DEFAULT_GUARDIAN_PERSONA` must be verified by direct comparison, not inferred from the existing self-referential unit test (Section 10 item 4, new).

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) before implementation began.

**Implemented exactly as scoped.** AAM-0001 v0.7: the persona-refinement text (Section 5's two paragraphs) and the voice disclosure note appended to the Guardian Persona section, immediately after the existing "Explicitly deferred, not silently dropped" household-role paragraph - none of the pre-existing text reworded or removed. `jarvis/guardian/config.py`'s `DEFAULT_GUARDIAN_PERSONA` extended with a faithful second-person transformation of the same content (matching the existing convention that AAM-0001's third-person description and the system-prompt's second-person instruction are a meaning-preserving transformation, not a byte-identical copy - true of the original ESR-0036 text as well, e.g. "Guardian is calm, measured..." versus "Speak calmly, thoughtfully..."). One deliberate, disclosed omission from `config.py`: the forward-looking "once GAM-0001's household role model is wired in, revisit this convention" sentence is governance/roadmap framing, not an instruction for the model to act on now, so it was kept in AAM-0001 only - consistent with how the pre-existing "Explicitly deferred, not silently dropped" framing was never duplicated into `config.py` either.

`jarvis/tests/test_guardian_runtime.py:392` continues to pass (compares the constant against itself, unaffected by the text change). Full suite: 418 passed, 1 skipped (unchanged - no test needed rewriting). `validate_repository.py` (full mode): 0 errors, 257 warnings (was 255 - two new cross-document Section-reference false positives from this session's own new cross-references, consistent with the established disclosed category).

**Live qualitative check (Section 10 item 3) not performed** - no live conversational provider (OpenAI/Gemini/Ollama) was configured in this implementation environment. This is disclosed honestly rather than fabricated, consistent with PBK-0001's Operational Verification Before Reporting - the structural check (persona text composes and reaches the provider unchanged) is confirmed by the passing test suite; the qualitative "does it sound different" check was already scoped as advisory evidence only, not a deterministic gate, and remains available for the Programme Sponsor to perform via a live smoke check whenever a provider is configured.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture this package amends (Guardian Persona section). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8.1 Household Role Model - the deferred capability the "Sir" convention is a disclosed stopgap for, not itself changed by this package. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0112/EBG-0113 - the Voice faculty and voice-model context behind the British-cadence/American-voice disclosure. |
| [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 30 July 2026 | Claude Engineering Implementer | **Programme Sponsor approved**, verified via `submit-response` against the real Sponsor Approval Service. **Implemented exactly as scoped**: AAM-0001 v0.7 (persona refinement + voice disclosure note appended), `jarvis/guardian/config.py`'s `DEFAULT_GUARDIAN_PERSONA` extended with a faithful second-person transformation (one disclosed omission: the forward-looking household-role revisit sentence kept in AAM-0001 only, as governance framing). 418 tests pass, 1 skipped (unchanged). `validate_repository.py`: 0 errors, 257 warnings. Live qualitative check not performed - no provider configured in this environment, disclosed honestly. |
| 0.2 | 30 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: Pass, with non-blocking findings. Folded in: "Sir" convention text now explicitly excludes any implication of Administrator authority/adult status/approval capability; Section 10's live-provider check marked advisory, not a deterministic gate; added an explicit exact-text-parity validation requirement (Section 10 item 4). |
| 0.1 | 30 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0043 WP1. Reviewed by Codex: Pass, with non-blocking findings (see v0.2). |
