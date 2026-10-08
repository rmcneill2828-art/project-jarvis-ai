"""End-to-end tests of confirmed escalation through the JSON-RPC server
(ESR-0061 WP3b, EIP-ESR0061-003 6.3-6.8).

Everything real except the network: `urllib.request.urlopen` is replaced, so
no request leaves the machine, and the tests can see exactly which URL was
called, with what headers and body.
"""

import json
import urllib.error

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.escalation import CAP_REACHED_RESPONSE, EscalationOffers
from jarvis.interfaces.sentinel_conversation import (
    PROVIDER_DECLINED_RESPONSE,
    PROVIDER_UNAVAILABLE_RESPONSE,
)
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime

KEY = "test-key-not-a-real-credential"
OLLAMA_URL_PREFIX = "http://127.0.0.1:1"
ANTHROPIC_HOST = "api.anthropic.com"
CLAUDE_REPLY = "Claude says: here is a considered answer."


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def read(self) -> bytes:
        return self._body


class _Network:
    """Fakes both services and records what was sent to each."""

    def __init__(self) -> None:
        self.local_answer: str | None = None  # None = Ollama is unreachable
        self.claude_payload: dict = {
            "model": "claude-sonnet-5-5",
            "content": [{"type": "text", "text": CLAUDE_REPLY}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 1_000, "output_tokens": 200},
        }
        self.claude_calls: list[dict] = []
        self.other_calls: list[str] = []

    def urlopen(self, request, timeout):
        url = request.full_url
        if ANTHROPIC_HOST in url:
            self.claude_calls.append(
                {
                    "url": url,
                    "headers": {key.lower(): value for key, value in request.header_items()},
                    "body": json.loads(request.data),
                }
            )
            return _FakeResponse(self.claude_payload)
        self.other_calls.append(url)
        if url.startswith(OLLAMA_URL_PREFIX) and self.local_answer is not None:
            return _FakeResponse({"response": self.local_answer, "done": True})
        raise urllib.error.URLError("connection refused")


@pytest.fixture
def network(monkeypatch):
    fake = _Network()
    monkeypatch.setattr("urllib.request.urlopen", fake.urlopen)
    return fake


def _build(tmp_path, monkeypatch, *, key=True, offers=None, **env):
    if key:
        monkeypatch.setenv("ANTHROPIC_API_KEY", KEY)
    else:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    environ = {
        "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
        "JARVIS_OLLAMA_ENDPOINT": OLLAMA_URL_PREFIX,
        "JARVIS_LOG_DIR": str(tmp_path / "logs"),
        **({"ANTHROPIC_API_KEY": KEY} if key else {}),
        **env,
    }
    runtime = build_default_runtime(environ=environ)
    return StdioRpcServer(
        runtime,
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
        escalation_offers=offers,
    )


class _Client:
    def __init__(self, server: StdioRpcServer) -> None:
        self.server = server
        self._next = 1

    def call(self, method: str, **params) -> dict:
        self._next += 1
        return self.server.handle_line(
            json.dumps({"jsonrpc": "2.0", "id": self._next, "method": method, "params": params})
        )

    def result(self, method: str, **params) -> dict:
        response = self.call(method, **params)
        assert "result" in response, response
        return response["result"]

    def as_profile(self, name: str, role: str) -> str:
        created = self.result("profile.create", displayName=name, role=role)
        self.result("profile.select", profileId=created["id"])
        return created["id"]

    def select(self, profile_id: str) -> None:
        self.result("profile.select", profileId=profile_id)

    def ask(self, message: str) -> dict:
        return self.result("guardian.converse", message=message)


def _client(tmp_path, monkeypatch, **kwargs) -> _Client:
    return _Client(_build(tmp_path, monkeypatch, **kwargs))


def _error_text(response: dict) -> str:
    assert "error" in response, response
    return response["error"]["message"]


# --- the happy path: offer, confirm, answer -----------------------------------------------------------------------


def test_when_the_local_model_fails_an_adult_is_offered_claude_and_nothing_is_sent_yet(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")

    result = client.ask("hello")

    assert result["message"] == PROVIDER_UNAVAILABLE_RESPONSE
    offer = result["escalation"]
    assert offer["offered"] is True
    assert offer["reason"] == "local_unavailable"
    assert offer["token"]
    assert offer["model"] == "claude-sonnet-5-5"
    assert offer["sendsMemory"] is False
    assert offer["expiresInSeconds"] == 600
    assert offer["allowance"]["capGbp"] == 30.0
    assert offer["allowance"]["capUsd"] == 37.5
    assert network.claude_calls == []


def test_confirming_the_offer_sends_the_same_message_to_claude_and_labels_the_answer(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello there")["escalation"]["token"]

    result = client.result("guardian.escalate", token=token)

    assert result["message"] == CLAUDE_REPLY
    assert result["answeredBy"] == "claude"
    assert result["provider"] == "anthropic"
    assert result["failure"] is None
    (call,) = network.claude_calls
    assert call["url"] == "https://api.anthropic.com/v1/messages"
    assert call["headers"]["x-api-key"] == KEY
    assert call["body"]["model"] == "claude-sonnet-5-5"
    assert call["body"]["messages"][-1] == {"role": "user", "content": "hello there"}
    assert call["body"]["output_config"] == {"effort": "low"}


def test_the_answer_reports_the_allowance_after_the_real_cost(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]

    allowance = client.result("guardian.escalate", token=token)["allowance"]

    assert allowance["spentUsd"] == 0.004  # 1000 input at $2/M + 200 output at $10/M
    assert allowance["remainingUsd"] == 37.496
    assert allowance["requests"] == 1


def test_a_token_works_once(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]
    client.result("guardian.escalate", token=token)

    replay = client.call("guardian.escalate", token=token)

    assert "expired or was already used" in _error_text(replay)
    assert len(network.claude_calls) == 1


def test_an_expired_token_is_refused(tmp_path, monkeypatch, network):
    clock = {"now": 0.0}
    offers = EscalationOffers(clock=lambda: clock["now"])
    client = _client(tmp_path, monkeypatch, offers=offers)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]
    clock["now"] += 601

    response = client.call("guardian.escalate", token=token)

    assert "expired or was already used" in _error_text(response)
    assert network.claude_calls == []


def test_a_claude_answer_joins_the_conversation_so_a_follow_up_has_context(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    client.result("guardian.escalate", token=client.ask("first question")["escalation"]["token"])

    client.result("guardian.escalate", token=client.ask("second question")["escalation"]["token"])

    second = network.claude_calls[1]["body"]["messages"]
    assert [m["content"] for m in second] == ["first question", CLAUDE_REPLY, "second question"]


def test_a_question_already_answered_locally_is_not_sent_twice(tmp_path, monkeypatch, network):
    network.local_answer = "a quick local answer"
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    offer = client.ask("research the latest on solar panels")["escalation"]
    assert offer["reason"] == "research_cue"

    client.result("guardian.escalate", token=offer["token"])

    messages = network.claude_calls[0]["body"]["messages"]
    assert [m["content"] for m in messages] == ["research the latest on solar panels"]


# --- when JARVIS offers -------------------------------------------------------------------------------------------


def test_a_good_local_answer_to_an_ordinary_question_makes_no_offer(tmp_path, monkeypatch, network):
    network.local_answer = "four"
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")

    result = client.ask("what is two plus two")

    assert result["message"] == "four"
    assert result["escalation"] == {"offered": False, "reason": None, "token": None}


def test_ask_claude_can_be_requested_for_any_message(tmp_path, monkeypatch, network):
    network.local_answer = "four"
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Adult")

    offer = client.result("guardian.escalation.offer", message="what is two plus two")

    assert offer["offered"] is True
    assert offer["reason"] == "requested"
    answer = client.result("guardian.escalate", token=offer["token"])
    assert answer["answeredBy"] == "claude"
    assert network.claude_calls[0]["body"]["messages"][-1]["content"] == "what is two plus two"


@pytest.mark.parametrize("message", ["", "   "])
def test_ask_claude_needs_a_message(tmp_path, monkeypatch, network, message):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Adult")

    assert "must not be blank" in _error_text(client.call("guardian.escalation.offer", message=message))


def test_without_a_key_claude_is_never_offered(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch, key=False)
    client.as_profile("Robert", "Administrator")

    result = client.ask("research the latest news")

    assert result["escalation"]["offered"] is False
    assert "not set up" in _error_text(client.call("guardian.escalation.offer", message="hello"))
    status = client.result("provider.status")["claude"]
    assert status["configured"] is False
    assert status["allowance"] is None
    assert not (tmp_path / "spend.db").exists()


# --- who may escalate: every path a Child, a Guest or nobody could try ---------------------------------------------


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_is_never_offered_claude_and_is_told_nothing_of_it(tmp_path, monkeypatch, network, role):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Young", role)

    result = client.ask("research the latest news")

    assert result["message"] == PROVIDER_UNAVAILABLE_RESPONSE
    assert result["escalation"] == {"offered": False, "reason": None, "token": None}
    assert network.claude_calls == []


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_cannot_ask_for_an_offer_or_use_the_escalate_rpc(tmp_path, monkeypatch, network, role):
    client = _client(tmp_path, monkeypatch)
    admin_id = client.as_profile("Robert", "Administrator")
    adult_token = client.ask("hello")["escalation"]["token"]
    client.as_profile("Young", role)

    offer = client.call("guardian.escalation.offer", message="hello")
    escalate = client.call("guardian.escalate", token=adult_token)

    assert "cannot ask Claude" in _error_text(offer)
    assert "cannot ask Claude" in _error_text(escalate)
    assert network.claude_calls == []
    # The refused attempt did not spend the Administrator's token.
    client.select(admin_id)
    assert client.result("guardian.escalate", token=adult_token)["answeredBy"] == "claude"


def test_nobody_selected_means_no_escalation(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)

    assert "Select a profile" in _error_text(client.call("guardian.escalate", token="anything"))
    assert "Select a profile" in _error_text(client.call("guardian.escalation.offer", message="hello"))
    assert client.ask("research the latest")["escalation"]["offered"] is False
    assert network.claude_calls == []


def test_a_role_sent_as_a_parameter_is_ignored(tmp_path, monkeypatch, network):
    """The role comes from the server-held active profile, never the request."""

    client = _client(tmp_path, monkeypatch)
    client.as_profile("Young", "Child")

    response = client.call("guardian.escalation.offer", message="hello", role="Administrator", profileId="x")

    assert "cannot ask Claude" in _error_text(response)
    assert network.claude_calls == []


def test_a_forged_token_is_refused(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")

    for forged in ["", "forged", "A" * 32]:
        assert "expired or was already used" in _error_text(client.call("guardian.escalate", token=forged))
    assert network.claude_calls == []


def test_a_token_from_another_profile_is_refused_and_stays_valid_for_its_owner(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    first = client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]
    client.as_profile("Pat", "Adult")

    assert "expired or was already used" in _error_text(client.call("guardian.escalate", token=token))

    client.select(first)
    assert client.result("guardian.escalate", token=token)["answeredBy"] == "claude"
    assert len(network.claude_calls) == 1


def test_switching_profile_between_offer_and_confirmation_does_not_carry_the_offer_over(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("a private question")["escalation"]["token"]
    client.as_profile("Young", "Child")

    assert client.call("guardian.escalate", token=token)["error"]
    assert network.claude_calls == []


def test_the_ordinary_path_never_reaches_claude_even_for_an_administrator(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")

    for message in ["hello", "research the latest news", "look up https://example.com"]:
        client.ask(message)

    assert network.claude_calls == []
    assert network.other_calls and all(url.startswith(OLLAMA_URL_PREFIX) for url in network.other_calls)


def test_sentinel_denies_the_cloud_route_to_a_child_even_if_the_rpc_check_were_bypassed(tmp_path, monkeypatch, network):
    """Layer two on its own: call the runtime directly, past the RPC layer."""

    server = _build(tmp_path, monkeypatch)

    for role in ["Child", "Guest", None]:
        response = server._runtime.escalate("hello", "profile", role=role, include_household=False, share_memory=False)
        assert response.is_model_reply is False
        assert response.failure == "denied"
    assert network.claude_calls == []
    adult = server._runtime.escalate("hello", "profile", role="Adult", include_household=False, share_memory=False)
    assert adult.is_model_reply is True


# --- memory: off by default, controlled by an Administrator --------------------------------------------------------


def _remember(client: _Client, content: str) -> None:
    pending = client.result("memory.propose", content=content)
    client.result("memory.approve", pendingId=pending["pendingId"])


def test_retained_memory_does_not_travel_by_default(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    _remember(client, "My daughter's school is Greenfield Primary")

    client.result("guardian.escalate", token=client.ask("hello")["escalation"]["token"])

    body = json.dumps(network.claude_calls[0]["body"])
    assert "Greenfield" not in body


def test_retained_memory_travels_once_an_administrator_allows_it_and_the_offer_says_so(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")
    _remember(client, "My daughter's school is Greenfield Primary")
    updated = client.result("profile.setCloudMemory", profileId=admin, enabled=True)
    assert updated["shareMemoryWithCloud"] is True

    offer = client.ask("hello")["escalation"]
    client.result("guardian.escalate", token=offer["token"])

    assert offer["sendsMemory"] is True
    assert "Greenfield" in json.dumps(network.claude_calls[0]["body"])


def test_turning_memory_sharing_off_again_stops_it(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")
    _remember(client, "The garage code is 4411")
    client.result("profile.setCloudMemory", profileId=admin, enabled=True)
    client.result("profile.setCloudMemory", profileId=admin, enabled=False)

    client.result("guardian.escalate", token=client.ask("hello")["escalation"]["token"])

    assert "4411" not in json.dumps(network.claude_calls[0]["body"])


def test_only_an_administrator_can_change_memory_sharing(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")
    adult = client.as_profile("Pat", "Adult")

    refused = client.call("profile.setCloudMemory", profileId=adult, enabled=True)

    assert "Only an Administrator" in _error_text(refused)
    client.select(admin)
    profiles = {p["id"]: p for p in client.result("profile.list")["profiles"]}
    assert profiles[adult]["shareMemoryWithCloud"] is False


def test_memory_sharing_cannot_be_enabled_for_a_child(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    child = client.result("profile.create", displayName="Young", role="Child")["id"]

    assert "cannot share memory" in _error_text(client.call("profile.setCloudMemory", profileId=child, enabled=True))


def test_memory_sharing_needs_a_real_boolean(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")

    assert "true or false" in _error_text(client.call("profile.setCloudMemory", profileId=admin, enabled="yes"))


# --- declines, the cap and the audit trail -------------------------------------------------------------------------


def test_a_claude_decline_is_answered_honestly_and_billed_but_no_other_model_is_asked(tmp_path, monkeypatch, network):
    network.claude_payload = {
        "model": "claude-sonnet-5-5",
        "content": [],
        "stop_reason": "refusal",
        "stop_details": {"category": "cyber"},
        "usage": {"input_tokens": 500, "output_tokens": 0},
    }
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]
    other_calls_before = len(network.other_calls)

    result = client.result("guardian.escalate", token=token)

    assert result["message"] == PROVIDER_DECLINED_RESPONSE
    assert result["answeredBy"] is None
    assert result["failure"] == "declined"
    assert result["allowance"]["spentUsd"] == 0.001
    assert len(network.claude_calls) == 1
    assert len(network.other_calls) == other_calls_before


def test_a_failing_claude_call_costs_nothing_and_says_so(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    token = client.ask("hello")["escalation"]["token"]
    network.claude_payload = {"unexpected": "shape"}

    result = client.result("guardian.escalate", token=token)

    assert result["message"] == PROVIDER_UNAVAILABLE_RESPONSE
    assert result["answeredBy"] is None
    assert result["allowance"]["spentUsd"] == 0
    assert result["allowance"]["requests"] == 0


def test_once_the_cap_is_used_up_nothing_more_is_offered_or_sent(tmp_path, monkeypatch, network):
    # A cap of US$0.02: the first call (worst case about US$0.013, real cost
    # US$0.012) fits, the second cannot.
    client = _client(
        tmp_path, monkeypatch, JARVIS_CLAUDE_MONTHLY_CAP_GBP="0.02", JARVIS_USD_PER_GBP="1"
    )
    client.as_profile("Robert", "Administrator")
    network.claude_payload["usage"] = {"input_tokens": 1_000, "output_tokens": 1_000}
    first = client.ask("hello")["escalation"]
    client.result("guardian.escalate", token=first["token"])
    second_offer = client.ask("hello again")["escalation"]

    # Offered while there is any room, refused when the call itself is made.
    assert second_offer["offered"] is True
    result = client.result("guardian.escalate", token=second_offer["token"])

    assert result["message"] == CAP_REACHED_RESPONSE
    assert result["failure"] == "cap_reached"
    assert result["allowance"]["spentUsd"] == 0.012
    assert len(network.claude_calls) == 1
    assert client.result("provider.status")["claude"]["allowance"]["requests"] == 1


def test_a_spent_cap_stops_the_offers_themselves(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Robert", "Administrator")
    ledger = client.server._runtime.escalation_provider.ledger
    ledger.settle(ledger.reserve(ledger.cap_micro), ledger.cap_micro)

    assert client.ask("hello again")["escalation"]["offered"] is False
    assert "allowance" in _error_text(client.call("guardian.escalation.offer", message="hello"))
    assert client.result("provider.status")["claude"]["allowance"]["capReached"] is True
    assert network.claude_calls == []


def test_the_cap_and_rate_come_from_settings_and_fall_back_when_unusable(tmp_path, monkeypatch, network):
    custom = _client(tmp_path / "a", monkeypatch, JARVIS_CLAUDE_MONTHLY_CAP_GBP="10", JARVIS_USD_PER_GBP="1.5")
    broken = _client(tmp_path / "b", monkeypatch, JARVIS_CLAUDE_MONTHLY_CAP_GBP="lots", JARVIS_USD_PER_GBP="-2")

    assert custom.result("provider.status")["claude"]["allowance"]["capUsd"] == 15.0
    assert broken.result("provider.status")["claude"]["allowance"]["capUsd"] == 37.5


def test_provider_status_reports_the_month_and_whether_this_profile_may_ask(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    client.as_profile("Young", "Child")

    status = client.result("provider.status")["claude"]

    assert status["configured"] is True
    assert status["model"] == "claude-sonnet-5-5"
    assert status["mayEscalate"] is False
    assert status["allowance"]["capUsd"] == 37.5
    assert len(status["allowance"]["month"]) == 7


def test_every_escalation_leaves_an_audit_event_with_counts_and_never_content(tmp_path, monkeypatch, network):
    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")
    _remember(client, "the secret garage code is 4411")
    client.result("profile.setCloudMemory", profileId=admin, enabled=True)
    client.result("guardian.escalate", token=client.ask("my secret question")["escalation"]["token"])

    audit_text = "\n".join(path.read_text(encoding="utf-8") for path in (tmp_path / "logs").glob("*audit*"))

    assert '"cloud_escalation"' in audit_text
    assert '"answered"' in audit_text
    assert "input_tokens" in audit_text
    for private in ["secret", "4411", "garage", CLAUDE_REPLY, KEY]:
        assert private not in audit_text
