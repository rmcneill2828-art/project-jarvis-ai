# ADR-0022 - Sponsor Approval Service

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0022 |
| Title | Sponsor Approval Service |
| Version | 1.1 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 19 July 2026 |
| Review Trigger | Any future proposal to change how `programme_sponsor_authorisation` is set or checked in the AIEMS Exchange Bridge |

---

# Purpose

Record the decision to replace `scripts/aiems_bridge.py`'s file-based `sponsor-decision` command with a remote Sponsor Approval Service that Programme Sponsor authorisation can only be written to, never read *and* written by the same party - closing a real, confirmed self-approval gap in the AIEMS Exchange Bridge (EBG-0057), resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0084.

---

# Scope

This decision covers the architecture, security requirements and operational practice change a future implementation must satisfy. It does not implement the service, `sponsor_client.py`, or the `aiems_bridge.py` diff - none exist today and none are authorised by this decision. It does not change `submit-to-review`, `return-findings`, the transcript format for those two handover types, the work-package locking mechanism, or the repository-ref drift check's underlying logic (Section 4 preserves it, does not redesign it).

---

# Engineering Authority

Proposed directly by the Programme Sponsor at ESR-0029 WP5, with a fully-specified client-side sketch (`fetch_latest_decision`, `cmd_submit_response` changes). Investigated and drafted by the Engineering Implementer against direct evidence from reading the real, current `scripts/aiems_bridge.py`, per Principle 1/2 (Engineering Before Implementation, Evidence Before Conclusion) - not accepted on the proposal's own framing alone.

---

# Evidence Sources

- `scripts/aiems_bridge.py` (current implementation, read directly, not assumed) - `cmd_sponsor_decision` (lines 375-401) is a plain CLI subcommand with no code-level gate distinguishing who may invoke it; any process with repository access can run it. The transcript file `sponsor-decision` writes to (`append_transcript`) is unsigned, human-readable plaintext - appendable by anything with filesystem write access, independent of the CLI entirely.
- `cmd_submit_response` (lines 404-468) - confirmed to already implement the two properties this ADR must preserve: a valid-approving-decision check and a repository-ref drift check, both inside the Work Package lock. Confirmed by direct review this session that despite this code existing and being correct, it has not actually been the code path used to gate any real commit across ESR-0029's five Work Packages to date - the Engineering Implementer read the local transcript directly and ran `git commit` via Bash in every case, never invoking `submit-response`.
- `EIP-ESR0025-001` (original bridge MVP) and its three post-implementation Engineering Reviewer findings (path-traversal, unchecked validation exit codes, a TOCTOU race on the authorisation check) - establishes the precedent that this bridge's security properties have repeatedly needed a second, adversarial look beyond the first design, which this ADR continues.
- `EIP-ESR0028-001`'s and this project's repeated no-discretionary-spend constraint (`project_jarvis_no_discretionary_budget` context) - Tailscale's free/personal tier is confirmed sufficient for this use case (private tailnet, `tailscale serve`/`funnel`), no paid infrastructure required.

---

# Main Content

## 1. Problem Statement

`cmd_sponsor_decision` is the only code path permitted to write `programme_sponsor_authorisation: true`, and `cmd_submit_response` is designed to refuse unless that field is set by a genuine Sponsor action. In practice, neither half of that design is actually enforced by anything other than convention: (a) nothing prevents an agent from invoking `sponsor-decision` itself, since it is an ordinary CLI subcommand available in the same environment the agent runs in; (b) nothing prevents an agent (or anything else with filesystem access) from hand-editing the plaintext transcript file to fabricate an approving entry; (c) even where the design is sound, `submit-response` - the one command that actually checks it - has not been used as the real gate in practice, since committing directly via `git` after reading the transcript locally produces the same visible outcome without ever exercising the check.

## 2. Background

Raised directly by the Programme Sponsor at ESR-0029 WP5 with a concrete proposed architecture: a small HTTP service holding the authoritative decision record, an `AGENT_TOKEN` that can only `GET /decisions/latest`, a `SPONSOR_TOKEN` that never exists in any agent-reachable environment and is used only from a host-side `sponsor_client.py`, and Tailscale as the network boundary. The Engineering Implementer's review confirmed the proposal's motivating concern is real (Section 1(a)/(b)) and surfaced an additional gap the proposal's code sketch alone does not close (Section 1(c)) - recorded here as part of the same decision rather than left implicit.

## 3. Options Considered

| Option | Assessment |
|--------|------------|
| Leave `sponsor-decision` as a local file-based command, rely on convention/instruction not to self-invoke it | Already shown insufficient by direct code review - no technical barrier exists today; both this and the plaintext-transcript-editing path are open regardless of instruction-following. |
| Add a local technical safeguard (e.g. an OS-level file permission, a separate local credential check) without a remote service | Does not close the plaintext-transcript-editing path, since the agent process runs with the same filesystem permissions as any local safeguard could be checked against; does not achieve genuine separation between the party requesting approval and the party granting it, since both still run on infrastructure the agent's own process can reach. |
| A remote Sponsor Approval Service: agents hold a read-only token that cannot write regardless of payload; the only writing credential never exists in any agent-reachable environment; deployed behind Tailscale, not the open internet | Achieves genuine separation - the write capability is structurally absent from every environment an agent process can read, not merely undocumented or discouraged. Matches the existing `return-findings` design principle (Codex's command has no file-path argument, so it is structurally incapable of writing outside `.aiems-exchange/` - the same "structurally incapable, not merely instructed" property, applied to approvals). |

---

## 4. Decision

The AIEMS Exchange Bridge's approval gate **shall move from a local, transcript-file-based `sponsor-decision` command to a remote Sponsor Approval Service**, with the following binding requirements for the implementation that builds it:

1. **`cmd_sponsor_decision` and its `argparse` subparser are deleted entirely from `scripts/aiems_bridge.py`.** No code path in any agent-accessible environment (container or host, Claude Code or Codex CLI) may set `programme_sponsor_authorisation: true`.
2. **The service exposes exactly two capabilities:**
   - `GET /decisions/latest?session=...&work_package=...` - gated on `AGENT_TOKEN`, returns the latest decision record for that Work Package (or none). Read-only; the route implementation must be structurally incapable of accepting or acting on a write regardless of request payload, mirroring `return-findings`' existing "no file-path argument to exploit" property.
   - `POST /decisions` - gated on `SPONSOR_TOKEN`, the only route that can create a decision record. `SPONSOR_TOKEN` must never be present in any environment variable, file, or process reachable by Claude Code or Codex CLI - it exists only in the Programme Sponsor's own credential store, entered manually into a host-side terminal running `sponsor_client.py`.
3. **`cmd_submit_response` fetches the decision from the service, not the local transcript**, and preserves exactly the two checks it already implements today: refuse unless the fetched decision approves, and refuse unless `current_repository_ref == decision.repository_ref` (the drift check is unchanged in substance, only its data source changes).
4. **Fail closed.** If the service is unreachable, `submit-response` must refuse, never fall back to a local or offline approval path. This is a deliberate availability-for-security tradeoff for this specific gate, not an oversight - approval should not be easier to obtain when the one thing that can grant it is unreachable.
5. **The service's persistence must be durable across restarts** (e.g. SQLite or an append-only store on the service's own host) - an in-memory-only store would silently lose all decision history on a restart, a real regression from today's durable transcript file. Specific technology is implementation-level detail, not decided here.
6. **Deployment**: the service runs on the Programme Sponsor's own trusted host, reachable only via a private Tailscale address (`tailscale serve` or `funnel`), never exposed to the open internet. `SPONSOR_URL` may be committed (a private address is not itself a secret); `SPONSOR_TOKEN` must never be committed or held on any machine the agents run on.
7. **Operational practice change, binding on the Engineering Implementer**: once implemented, `submit-response` (or an equivalent service-checked call) becomes the actual required step before any commit in future sessions. Reading the local transcript directly and running `git commit` via Bash - the pattern used throughout ESR-0029 WP1-WP4 - is no longer sufficient once this decision is implemented, since it would bypass the very check this ADR exists to make load-bearing. This requirement is recorded here so it is verifiable in future session review, not left as an unstated assumption.
8. **`.aiems-exchange/transcript/*.md` files remain the durable record for `submit-to-review` and `return-findings` handovers exactly as today** - only the `sponsor-decision` handover type moves off this file. `submit-response`'s own existing behaviour of appending to the transcript once a decision is validated is unchanged, preserving audit continuity for what was found and validated at commit time, even though the decision itself now lives elsewhere.

This ADR authorises the decision and these requirements only. Implementation - the service itself, `sponsor_client.py`, and the `aiems_bridge.py` diff - is separate, future, scoped work (see Consequences).

---

## 5. Rationale

- Direct code review, not the proposal's own framing, is what actually established the problem is real: `cmd_sponsor_decision` has no technical gate today, and the transcript file it writes to is separately editable by anything with filesystem access - two distinct gaps, both closed by moving the write capability to a credential that structurally does not exist in any agent-reachable environment.
- The design mirrors `return-findings`' already-proven pattern (a command structurally incapable of the thing it must not do, not merely instructed not to do it) - consistent internal security language across the bridge, not a new paradigm.
- The repository-ref drift check (already correct, already implemented) is preserved exactly, not redesigned - this decision changes where the decision record lives, not the logic that already correctly prevents a stale approval being replayed against a changed repository state.
- Fail-closed (Decision item 4) is the only choice consistent with this being a security gate rather than a convenience feature - an approval mechanism that becomes more permissive when degraded would be a worse design than today's, not an improvement.
- Recording the operational practice change (Decision item 7) explicitly, rather than leaving it as an implied consequence of the code change, is itself evidence-based: this session directly demonstrated that a correctly-coded gate (`submit-response`) can exist and still not be the actual mechanism protecting real commits, because a human/AI convention (reading the transcript, committing directly) developed alongside it and never got questioned until this review. Naming the practice requirement here makes it checkable in a future session, the same way this project already checks code against its own EIPs.

---

## 6. Consequences

- **Not implemented by this ADR.** A future EIP must scope and build: the Sponsor Approval Service itself (technology choice, persistence, the two routes' concrete implementation and auth enforcement); `sponsor_client.py`; the `aiems_bridge.py` diff (deleting `cmd_sponsor_decision` and its subparser, changing `cmd_submit_response` to call the service via a new `requests` dependency - disclosed now as a new dependency this project does not currently have); and a live end-to-end verification (agent-side `GET` succeeding and `POST` failing with 403 using `AGENT_TOKEN`; `sponsor_client.py` successfully `POST`ing with `SPONSOR_TOKEN` from a host terminal; `submit-response` correctly refusing when no decision exists, when the decision rejects, when the repository has drifted, and when the service is unreachable).
- Until implemented, `scripts/aiems_bridge.py` continues to run exactly as today - `sponsor-decision` remains a local file-based command, and this ADR does not require or imply any immediate change to it.
- Multi-machine use becomes straightforward once implemented: every machine's environment gets `AGENT_TOKEN`/`SPONSOR_URL`; `SPONSOR_TOKEN` lives only in the Programme Sponsor's own credential store, used from whichever host terminal is approving that day.
- The operational practice change (Decision item 7) applies to all future sessions once implemented, not only the session that implements it - a standing requirement, not a one-time note.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0084 (the backlog item whose service-architecture question this ADR resolves), also cross-references EBG-0057 (the original AIEMS Exchange Bridge this ADR amends the approval mechanism of). |
| [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] | The original bridge implementation and its three post-implementation Engineering Reviewer findings - the precedent that this bridge's security properties have repeatedly warranted a second, adversarial look. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0084's remaining implementation (the service, `sponsor_client.py`, the `aiems_bridge.py` diff) remains separate, future, scoped work, not authorised by this ADR. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Approved by the Programme Sponsor via the bridge (`sponsor-decision`, `repository_ref: bac6ba9ffa7df14c41bdea12d024684965fe907d`, 19 July 2026 13:03:28Z), following Engineering Reviewer (Codex) confirmation via the AIEMS Exchange Bridge: no findings - decision requirements are complete and internally consistent, correctly scoped as decision-only, and the operational-practice requirement (Decision item 7) is adequately binding. Status promoted Draft to Approved. |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP5, following the Programme Sponsor's proposal to replace file-based sponsor-decision with a remote approval service. Investigated and confirmed the motivating self-approval gap directly against the current `scripts/aiems_bridge.py` (not assumed from the proposal's own framing), and identified an additional gap the proposal alone does not close: `submit-response` has not actually been the real gate used in practice this session. Records both the architecture decision and the operational practice change as binding requirements. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
