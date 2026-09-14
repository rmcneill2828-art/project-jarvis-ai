# WR-ESR0057-001 - Home Assistant and Smart Home Integration Assessment

**Status:** Working Report per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]'s Working Report Lifecycle - **not a controlled artefact**, not registered in REG-0001. Produced at the Programme Sponsor's direction (ESR-0057 WP3), resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0025's assessment mandate. Advisory only; does not itself authorise any implementation.

**Author:** Claude Engineering Implementer
**Date:** 14 September 2026
**Purpose:** Assess Home Assistant and smart-home integration options, per EBG-0025's exact registered text ("Assess Home Assistant and smart-home integration options before any smart-home implementation package is approved... No implementation is authorised by this backlog entry"), and evaluate that assessment against this project's real, current authority model (GAM-0001) rather than treating it as a generic technology comparison.
**Next step:** Programme Sponsor review and decision - whether this closes EBG-0025 Complete, and whether either candidate identified in Section 5 warrants its own future backlog registration.
**Independent review:** none available this session - Codex is retired ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0126) and a genuine Antigravity CLI substitute remains blocked by Claude Code's own harness. This report has not been independently cross-checked; the Programme Sponsor is reviewing it directly, consistent with WP1/WP2 this same session.

---

## 1. Headline

Home Assistant is the right platform if/when JARVIS integrates smart-home control - it is the only major ecosystem whose local-first, self-hosted, no-mandatory-cloud posture matches this project's own standing constraints (self-hosted/free-first, no discretionary tooling budget, privacy-first architecture). But **the real gate is not Home Assistant at all - it is GAM-0001's own `LOCAL_AGENT_ACTION` boundary**, which classifies any device-control action as `DENY` today, independent of which smart-home platform is chosen. A read-only tier (querying sensor/device *state*, not controlling anything) is plausibly buildable sooner, following the exact precedent GIA's read-only observability already established, but that is a materially smaller and different scope than "smart-home integration" as commonly understood.

---

## 2. Ecosystem Comparison

| Platform | Local/self-hosted | Cloud dependency | Device compatibility | Fit for this project |
|---|---|---|---|---|
| **Home Assistant** | Yes - runs entirely on owned hardware (Raspberry Pi, NAS, home server); functions fully offline after setup | None required; cloud features are optional add-ons, not load-bearing | Very broad - 1,500+ integrations across Wi-Fi, Zigbee, Z-Wave, MQTT, Thread, Matter | Best match - the only option matching the project's self-hosted-first, no-discretionary-budget default |
| **Apple HomeKit** | Partial - most commands process locally, but some Siri/advanced requests still route through Apple servers | Yes, for advanced requests | Narrower (HomeKit-certified devices only) | Strong privacy story but not fully self-hosted, and Apple-ecosystem-locked |
| **Google Home** | No - cloud-dependent by design | Yes, required for most functionality | Broad, but ecosystem-locked | Poor fit - the opposite of this project's local-first posture |
| **Samsung SmartThings** | No - cloud hub model | Yes | Very broad, most interoperable across brands | Strong device compatibility but conflicts with self-hosted/no-cloud default |

Home Assistant is the clear fit on architectural grounds alone, before any project-specific consideration - it is the only platform in this table matching JARVIS's own existing self-hosted defaults (Piper/Kokoro TTS, faster-whisper STT, local Ollama fallback, SQLite-backed local memory).

---

## 3. Integration Architecture Options

Home Assistant exposes three integration surfaces, none of which require any cloud component:

- **REST API** - simple request/response: read entity states, call services (e.g. `light.turn_on`), pull history. Best fit for occasional, discrete queries or actions - the shape a JARVIS RPC-method wrapper would most naturally use.
- **WebSocket API** - real-time event streaming (state-change notifications as they happen). Better fit for anything wanting to react to smart-home events live, rather than poll.
- **MQTT** - the integration layer Home Assistant itself recommends for DIY/custom devices without a first-party integration; requires running a broker (e.g. Mosquitto) locally, adding one more self-hosted service to operate, but keeping the whole chain cloud-free.

Authentication is via a long-lived access token (Bearer token in the request header), generated once through the Home Assistant web UI or WebSocket `auth/long_lived_access_token` command, and persisting until explicitly revoked - the same "named env-var credential, no code-embedded secret" shape [[STD-0006_CONFIGURATION_AND_SECRETS_STANDARD|STD-0006]] already mandates for every other credential this project holds (`OPENAI_API_KEY`, `AIEMS_AGENT_TOKEN`, etc.), so no new credential-handling pattern would be needed.

For a future implementation, REST API + a long-lived token is the lowest-friction starting point; WebSocket and MQTT are refinements once a basic integration exists, not prerequisites.

---

## 4. Fit Against This Project's Real Authority Model

This is the assessment's substantive finding, and the reason a generic "Home Assistant is good, proceed" conclusion would be incomplete.

[[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 6.3/8A classifies smart-home *device control* (turning on lights, locking doors, adjusting thermostats) as `LOCAL_AGENT_ACTION` - a Sentinel trust category that is `DENY` for every request today, by explicit design, with no exception carved out for any specific platform or use case. Building the Local Agent module that could ever action such a request is JRM-0001 Track B **Phase 3**, itself gated on Phase 1 (Guardian Cognitive Core, delivered) and Phase 2 (the boundary definition, delivered) - and Phase 3 **has no backlog item yet authorising its build at all**, independent of Home Assistant. In other words: even a flawless, fully-scoped Home Assistant integration package could not control a single device today, because the authority layer beneath it categorically refuses that class of action, and that refusal predates and is independent of which smart-home platform is chosen.

There is a narrower, genuinely different possibility worth naming separately: **read-only smart-home state queries** ("what's the temperature in the living room," "is the front door locked"). GAM-0001 Section 8.3 already establishes that observation/monitoring capabilities (camera access, security monitoring) are distinct from `LOCAL_AGENT_ACTION` and do not open that boundary - and the Agent Framework already has a live precedent for exactly this shape: GIA's read-only observability agent, classified `ROUTINE_INTERACTION`, reachable through the mandatory Sentinel gate (ESR-0049/ESR-0050). A future "Home Assistant state query" specialist agent, read-only, could plausibly follow that same precedent - a materially smaller, nearer-term possibility than "smart-home integration" as EBG-0025 poses the question, and one that would not need Phase 3's Action faculty to exist first.

---

## 5. Recommendation

1. **Close EBG-0025 as the assessment it asked for** - Home Assistant identified as the right platform choice if/when smart-home work proceeds, with the authority-model gate (Section 4) now made explicit rather than left implicit.
2. **Do not register a "build Home Assistant device control" backlog item now** - it would sit blocked behind Track B Phase 3 (Action faculty) with no path to progress until that phase has its own backlog item, which JRM-0001 itself notes does not yet exist.
3. **Consider registering a narrower, distinct candidate**: a read-only Home Assistant state-query specialist agent, mirroring GIA's `ROUTINE_INTERACTION` precedent - genuinely buildable independent of Phase 3, but a materially different (and smaller) scope than what EBG-0025 asked to have assessed. Left as the Programme Sponsor's call whether this is worth a new backlog entry or premature until there is an actual case for JARVIS to answer questions about the physical home.

---

## 6. Evidence

Web research conducted directly (Codex unavailable for delegation, per EBG-0126):

- Home Assistant's local-first architecture, REST/WebSocket API shape and long-lived-token authentication model.
- Ecosystem comparison against Apple HomeKit, Google Home and Samsung SmartThings on privacy/local-control/device-compatibility grounds.
- MQTT's role as the recommended integration path for devices without a first-party Home Assistant integration.

Repository evidence read directly, not inferred: [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Sections 6.3, 8.3, 8A (the `LOCAL_AGENT_ACTION` boundary, confirmed still `DENY` for every request); [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Section 7.3 Phase 3 (Action faculty, no backlog item yet); [[STD-0006_CONFIGURATION_AND_SECRETS_STANDARD|STD-0006]] (credential-handling pattern a Home Assistant token would follow); the Agent Framework's real GIA precedent (`jarvis/agents/`, ESR-0049/ESR-0050) for what a read-only integration agent would look like in this codebase.

Sources: [Home Assistant long-lived access tokens](https://community.home-assistant.io/t/long-lived-access-token-using-websocket-api-or-rest-api/404755), [Home Assistant Authentication API](https://developers.home-assistant.io/docs/auth_api/), [Home Assistant vs Apple HomeKit vs Google Home](https://datawiresolutions.com/blog/home-assistant-vs-apple-homekit-vs-google-home), [Smart Home Ecosystems Compared 2026](https://smarthomedigest.com/articles/smart-home-ecosystems-compared-2026-alexa-vs-google-home-vs-homekit-vs-home-assistant), [Local-First Smart Home with Home Assistant](https://zediot.com/blog/home-assistant-local-first-smart-home-architecture/)
