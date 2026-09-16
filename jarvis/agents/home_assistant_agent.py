"""`HomeAssistantStateQueryAgent`: a read-only Home Assistant specialist agent.

EBG-0127 ([[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT]]
Section 5): read-only smart-home state queries ("what's the temperature in
the living room", "is the front door locked") - never device control.
Mirrors `GiaObservabilityAgent`'s `ROUTINE_INTERACTION` classification
exactly: this agent only reads and reports a Home Assistant entity's state,
touching no device, matching the same "observation is not control"
distinction GAM-0001 Section 8.3 already draws. It never approaches
`TrustCategory.LOCAL_AGENT_ACTION`.

`HomeAssistantClient` wraps Home Assistant's REST API (`GET
/api/states/<entity_id>`) directly via `urllib` - no new third-party HTTP
dependency, matching this project's own minimal-runtime-dependency practice
(`scripts/aiems_bridge.py`'s `fetch_latest_decision` uses the same approach).
A long-lived access token authenticates via a Bearer header, per STD-0006's
named-env-var credential-indirection pattern.
"""

import json
import urllib.error
import urllib.request

from jarvis.agents.contracts import AgentRequest, AgentResult

STATUS_REPORTED = "reported"


class HomeAssistantClient:
    """Thin, real REST client for Home Assistant's `/api/states` endpoint."""

    def __init__(self, base_url: str, token: str, timeout_seconds: float = 10.0) -> None:
        if not base_url.strip():
            msg = "Home Assistant base_url must not be empty."
            raise ValueError(msg)
        if not token.strip():
            msg = "Home Assistant token must not be empty."
            raise ValueError(msg)
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout_seconds = timeout_seconds

    def get_state(self, entity_id: str) -> dict[str, object]:
        """Return the named entity's current state as Home Assistant reports it.

        Raises `RuntimeError` on any non-2xx response or connection failure -
        never fabricates a value, matching this project's no-mock-fallback
        rule.
        """

        request = urllib.request.Request(
            f"{self._base_url}/api/states/{entity_id}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            msg = f"Home Assistant request for entity {entity_id!r} failed: {exc}"
            raise RuntimeError(msg) from exc


class HomeAssistantStateQueryAgent:
    """Specialist agent reporting a single Home Assistant entity's real state."""

    name = "home-assistant-state-query"

    def __init__(self, client: HomeAssistantClient) -> None:
        # Constructor-injected, matching every existing agent/provider's
        # dependency-injection pattern - keeps this agent unit-testable
        # with a fake client, never a real network call in tests.
        self._client = client

    def execute(self, request: AgentRequest) -> AgentResult:
        """Return the requested entity's current state.

        `request.parameters["entityId"]` names the Home Assistant entity to
        query (e.g. `"sensor.living_room_temperature"`,
        `"lock.front_door"`) - required, no default: this agent reports
        exactly what is asked, never a guessed or "most relevant" entity.
        """

        entity_id = request.parameters.get("entityId")
        if not entity_id:
            msg = "Home Assistant state query requires an 'entityId' parameter."
            raise ValueError(msg)

        state = self._client.get_state(entity_id)
        payload = {
            "entityId": entity_id,
            "state": str(state.get("state", "")),
            "lastChanged": str(state.get("last_changed", "")),
        }
        return AgentResult(status=STATUS_REPORTED, payload=payload)
