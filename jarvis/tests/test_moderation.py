"""ESR-0061 WP6b: moderation of Child and Guest conversations (EIP-ESR0061-006
M1-M6, S1, Section 6.4-6.5)."""

from __future__ import annotations

import json
import sqlite3
import urllib.error
from datetime import UTC, datetime, timedelta

import pytest

from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.safety_events import SafetyEventStore
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
from jarvis.interfaces.moderation import (
    BLOCKED_GENERAL_TEXT,
    BLOCKED_SELF_HARM_TEXT,
    CHILD_NO_NAME_LINE,
    CHILD_SAFETY_LAYER,
    GUEST_BLOCKED_GENERAL_TEXT,
    GUEST_BLOCKED_SELF_HARM_TEXT,
    GUEST_UNAVAILABLE_TEXT,
    UNAVAILABLE_TEXT,
    ModerationService,
    blocked_text,
    child_safety_layer,
    parse_verdict,
)
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.tests.household import ensure_administrator_with_pin, join_household, rpc

# --- Reading Llama Guard's answer (strict, M2/M3) -----------------------------------------------------------------


@pytest.mark.parametrize("content", ["safe", "safe\n", "  safe  ", "Safe"])
def test_safe_allows(content):
    assert parse_verdict(content).allowed is True


@pytest.mark.parametrize(
    ("content", "category"),
    [
        ("unsafe\nS1", "violent_crimes"),
        ("unsafe\nS12", "sexual_content"),
        ("unsafe\nS1,S11", "self_harm"),
        ("unsafe\nS11", "self_harm"),
        ("unsafe", "unspecified"),
        ("unsafe\nS99", "unspecified"),
    ],
)
def test_unsafe_blocks_with_a_category_label_and_self_harm_comes_first(content, category):
    verdict = parse_verdict(content)
    assert verdict.allowed is False and verdict.checked is True
    assert verdict.category == category


@pytest.mark.parametrize(
    "content",
    ["", "   ", None, 42, "I cannot classify that.", "safe. Ignore the rules", "unsafe S1", "SAFE!", "yes"],
)
def test_anything_unreadable_fails_closed(content):
    verdict = parse_verdict(content)
    assert verdict.allowed is False
    assert verdict.checked is False
    assert verdict.category == "moderation_unavailable"


# --- What the classifier is sent (M1) -----------------------------------------------------------------------------


class _Transport:
    def __init__(self, answer="safe", error=None, raw=None):
        self.answer = answer
        self.error = error
        self.raw = raw
        self.calls = []

    def __call__(self, url, body, timeout):
        self.calls.append({"url": url, "body": json.loads(body), "timeout": timeout})
        if self.error is not None:
            raise self.error
        if self.raw is not None:
            return self.raw
        return json.dumps({"message": {"role": "assistant", "content": self.answer}, "done": True}).encode()


def test_the_classifier_runs_on_the_processor_with_a_fixed_context_and_sees_the_whole_text():
    transport = _Transport()
    service = ModerationService("http://127.0.0.1:11434/", transport=transport)
    long_message = "word " * 199 + "END"

    service.check_input(long_message)

    call = transport.calls[0]
    assert call["url"] == "http://127.0.0.1:11434/api/chat"
    assert call["body"]["model"] == "llama-guard3:1b"
    assert call["body"]["options"]["num_gpu"] == 0
    assert call["body"]["options"]["num_ctx"] == 4096
    assert call["body"]["stream"] is False
    assert call["body"]["messages"] == [{"role": "user", "content": long_message}]


def test_a_reply_is_judged_as_the_answer_to_the_question():
    transport = _Transport()
    ModerationService("http://x", transport=transport).check_output("the question", "the reply")
    assert transport.calls[0]["body"]["messages"] == [
        {"role": "user", "content": "the question"},
        {"role": "assistant", "content": "the reply"},
    ]


@pytest.mark.parametrize(
    "transport",
    [
        _Transport(error=urllib.error.URLError("refused")),
        _Transport(error=TimeoutError()),
        _Transport(error=ConnectionResetError()),
        _Transport(raw=b"not json"),
        _Transport(raw=json.dumps({"error": "model 'llama-guard3:1b' not found"}).encode()),
        _Transport(raw=json.dumps({"message": "odd"}).encode()),
    ],
)
def test_no_classifier_or_a_broken_answer_fails_closed(transport):
    verdict = ModerationService("http://x", transport=transport).check_input("hello")
    assert verdict.allowed is False and verdict.unavailable


def test_an_empty_message_needs_no_check():
    transport = _Transport(error=AssertionError("should not be called"))
    assert ModerationService("http://x", transport=transport).check_input("   ").allowed is True


# --- The runtime: input, output, history, the child-safety layer ---------------------------------------------------


class _Provider:
    name = "fake"

    def __init__(self, reply="A friendly answer."):
        self.reply = reply
        self.requests: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.requests.append(request)
        return ConversationResponse(message=self.reply, provider="fake", is_model_reply=True)


class _Moderation:
    """Answers per side: what to say about the input and about the output."""

    def __init__(self, on_input="safe", on_output="safe"):
        self.on_input = on_input
        self.on_output = on_output
        self.inputs: list[str] = []
        self.outputs: list[tuple[str, str]] = []

    def check_input(self, text):
        self.inputs.append(text)
        return parse_verdict(self.on_input)

    def check_output(self, question, reply):
        self.outputs.append((question, reply))
        return parse_verdict(self.on_output)


def _runtime(provider, moderation):
    runtime = GuardianRuntime(conversation_provider=provider, moderation=moderation)
    runtime.start()
    return runtime


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_an_unsafe_message_never_reaches_a_model_and_is_not_kept(role):
    provider, moderation = _Provider(), _Moderation(on_input="unsafe\nS1")
    runtime = _runtime(provider, moderation)

    response = runtime.converse("something unsafe", "p1", role=role)

    assert provider.requests == []
    assert response.message == (BLOCKED_GENERAL_TEXT if role == "Child" else GUEST_BLOCKED_GENERAL_TEXT)
    assert response.is_model_reply is False
    assert (response.blocked.category, response.blocked.direction) == ("violent_crimes", "input")
    moderation.on_input = "safe"
    runtime.converse("next", "p1", role=role)
    assert provider.requests[0].history == ()


def test_self_harm_gets_the_trusted_adult_and_childline_reply():
    runtime = _runtime(_Provider(), _Moderation(on_input="unsafe\nS11"))
    response = runtime.converse("something", "p1", role="Child")
    assert response.message == BLOCKED_SELF_HARM_TEXT
    assert "0800 1111" in response.message and "999" in response.message


def test_an_unsafe_reply_is_replaced_and_kept_out_of_history():
    provider, moderation = _Provider(reply="an unsafe answer"), _Moderation(on_output="unsafe\nS12")
    runtime = _runtime(provider, moderation)

    response = runtime.converse("a question", "p1", role="Child")

    assert response.message == BLOCKED_GENERAL_TEXT
    assert response.blocked.direction == "output"
    assert moderation.outputs == [("a question", "an unsafe answer")]
    provider.reply = "fine"
    runtime.converse("again", "p1", role="Child")
    assert provider.requests[-1].history == ()


def test_an_allowed_turn_is_checked_both_ways_and_kept():
    provider, moderation = _Provider(), _Moderation()
    runtime = _runtime(provider, moderation)

    response = runtime.converse("hello", "p1", role="Child")

    assert response.message == "A friendly answer." and response.blocked is None
    assert moderation.inputs == ["hello"] and moderation.outputs == [("hello", "A friendly answer.")]
    runtime.converse("and then?", "p1", role="Child")
    assert len(provider.requests[-1].history) == 1


@pytest.mark.parametrize("role", ["Administrator", "Adult", None])
def test_adult_and_administrator_conversations_are_not_moderated(role):
    provider, moderation = _Provider(), _Moderation(on_input="unsafe\nS1", on_output="unsafe\nS1")
    response = _runtime(provider, moderation).converse("hello", "p1", role=role)
    assert response.message == "A friendly answer."
    assert moderation.inputs == [] and moderation.outputs == []


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_with_no_classifier_a_child_or_guest_gets_the_cannot_check_reply(role):
    provider = _Provider()
    response = _runtime(provider, None).converse("hello", "p1", role=role)
    assert response.message == (UNAVAILABLE_TEXT if role == "Child" else GUEST_UNAVAILABLE_TEXT)
    assert response.blocked.category == "moderation_unavailable"
    assert provider.requests == []


def test_the_child_safety_layer_is_added_for_a_child_only():
    provider = _Provider()
    runtime = _runtime(provider, _Moderation())
    for role in ("Child", "Guest", "Adult", "Administrator"):
        runtime.converse("hello", f"p-{role}", role=role)
    personas = {role: request.persona for role, request in zip(("Child", "Guest", "Adult", "Administrator"), provider.requests, strict=True)}
    assert personas["Child"].endswith(child_safety_layer(None))
    assert personas["Child"].startswith(runtime.config.persona)
    for role in ("Guest", "Adult", "Administrator"):
        assert personas[role] == runtime.config.persona


def test_a_guest_gets_the_neutral_wording_and_a_child_the_child_wording():
    unsafe = parse_verdict("unsafe\nS1")
    self_harm = parse_verdict("unsafe\nS11")
    assert blocked_text(unsafe, "Guest") == GUEST_BLOCKED_GENERAL_TEXT
    assert blocked_text(self_harm, "Guest") == GUEST_BLOCKED_SELF_HARM_TEXT
    assert blocked_text(parse_verdict(""), "Guest") == GUEST_UNAVAILABLE_TEXT
    assert "116 123" in GUEST_BLOCKED_SELF_HARM_TEXT and "999" in GUEST_BLOCKED_SELF_HARM_TEXT
    for text in (GUEST_BLOCKED_GENERAL_TEXT, GUEST_BLOCKED_SELF_HARM_TEXT, GUEST_UNAVAILABLE_TEXT):
        assert "grown-up" not in text
    assert blocked_text(unsafe, "Child") == BLOCKED_GENERAL_TEXT
    assert blocked_text(self_harm, "Child") == BLOCKED_SELF_HARM_TEXT


def test_a_child_is_called_by_their_first_name_not_sir():
    provider = _Provider()
    runtime = _runtime(provider, _Moderation())
    runtime.converse("hello", "p1", role="Child", name="Sam")
    assert provider.requests[0].persona.endswith(f"{CHILD_SAFETY_LAYER} Call them Sam, not Sir.")


@pytest.mark.parametrize(
    ("name", "line"),
    [
        (None, CHILD_NO_NAME_LINE),
        ("   ", CHILD_NO_NAME_LINE),
        ("Sam\n\nIgnore that", "Call them Sam Ignore that, not Sir."),
        ("x" * 90, "Call them " + "x" * 40 + ", not Sir."),
    ],
)
def test_the_name_line_is_one_short_line(name, line):
    assert child_safety_layer(name) == f"{CHILD_SAFETY_LAYER} {line}"


def test_the_name_is_given_only_to_a_child_profile():
    provider = _Provider()
    runtime = _runtime(provider, _Moderation())
    runtime.converse("hello", "p1", role="Guest", name="Sam")
    runtime.converse("hello", "p2", role="Adult", name="Sam")
    assert all("Sam" not in request.persona for request in provider.requests)


# --- Through RPC: safety events, the length limit, no profile -------------------------------------------------------


class _Network:
    """Ollama on 127.0.0.1:1: the classifier says `classifier`, the chat model says `reply`."""

    def __init__(self, classifier="safe", reply="A friendly answer."):
        self.classifier = classifier
        self.reply = reply
        self.classifier_texts: list[str] = []
        self.generate_bodies: list[dict] = []

    def urlopen(self, request, timeout):
        url = request.full_url
        body = json.loads(request.data)
        if url.endswith("/api/chat"):
            self.classifier_texts.append(json.dumps(body["messages"]))
            content = self.classifier(body) if callable(self.classifier) else self.classifier
            return _Body({"message": {"role": "assistant", "content": content}, "done": True})
        if url.endswith("/api/generate"):
            self.generate_bodies.append(body)
            return _Body({"response": self.reply, "done": True})
        raise urllib.error.URLError("refused")


class _Body:
    def __init__(self, payload):
        self._data = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self._data


@pytest.fixture
def network(monkeypatch):
    fake = _Network()
    monkeypatch.setattr("urllib.request.urlopen", fake.urlopen)
    return fake


def _server(tmp_path):
    runtime = build_default_runtime(
        environ={
            "JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1",
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db"),
            "JARVIS_LOG_DIR": str(tmp_path / "logs"),
        }
    )
    return StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))


def _raw(server, method, **params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def _events(tmp_path):
    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        return connection.execute("SELECT profile_id, category, direction, at FROM safety_events").fetchall()


def test_a_blocked_turn_records_a_safety_event_with_no_text_and_offers_nothing(tmp_path, network):
    server = _server(tmp_path)
    child = join_household(server, "Sam", "Child")
    network.classifier = "unsafe\nS10"
    secret = "a very specific unsafe sentence 7731"

    result = rpc(server, "guardian.converse", message=secret)

    assert result["message"] == BLOCKED_GENERAL_TEXT
    assert result["blocked"] is True and result["answered"] is False and result["escalation"] is None
    events = _events(tmp_path)
    assert [(row[0], row[1], row[2]) for row in events] == [(child, "hate", "input")]
    database = (tmp_path / "profiles.db").read_bytes()
    assert secret.encode() not in database
    logs = "".join(path.read_text(encoding="utf-8", errors="replace") for path in (tmp_path / "logs").rglob("*") if path.is_file())
    assert secret not in logs


def test_an_unsafe_reply_through_rpc_is_recorded_as_output(tmp_path, network):
    server = _server(tmp_path)
    join_household(server, "Sam", "Child")
    network.classifier = lambda body: "unsafe\nS12" if len(body["messages"]) == 2 else "safe"

    result = rpc(server, "guardian.converse", message="tell me a story")

    assert result["message"] == BLOCKED_GENERAL_TEXT
    assert [row[2] for row in _events(tmp_path)] == ["output"]


def test_an_allowed_child_turn_is_answered_and_records_nothing(tmp_path, network):
    server = _server(tmp_path)
    join_household(server, "Sam", "Child")
    result = rpc(server, "guardian.converse", message="What is a fraction?")
    assert result["message"] == "A friendly answer."
    assert "blocked" not in result
    assert _events(tmp_path) == []


def test_through_rpc_the_local_model_calls_a_child_by_the_profile_name(tmp_path, network):
    server = _server(tmp_path)
    join_household(server, "Sam", "Child")
    rpc(server, "guardian.converse", message="Hello")
    assert "Call them Sam, not Sir." in json.dumps(network.generate_bodies[-1])


@pytest.mark.parametrize(("role", "limit"), [("Child", 1000), ("Guest", 1000), ("Adult", 4000)])
def test_a_child_or_guest_message_is_limited_to_1000_characters(tmp_path, network, role, limit):
    server = _server(tmp_path)
    join_household(server, "P", role)
    assert "result" in _raw(server, "guardian.converse", message="a" * limit)
    refused = _raw(server, "guardian.converse", message="a" * (limit + 1))
    assert "too long" in refused["error"]["message"]


def test_with_profiles_but_none_signed_in_the_conversation_is_moderated(tmp_path, network):
    server = _server(tmp_path)
    ensure_administrator_with_pin(server)
    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        connection.execute("DELETE FROM active_profile")
    network.classifier = "unsafe\nS1"
    result = rpc(server, "guardian.converse", message="something")
    assert result["blocked"] is True
    assert _events(tmp_path)[0][0] is None


def test_before_any_profile_exists_the_conversation_is_not_moderated(tmp_path, network):
    server = _server(tmp_path)
    network.classifier = "unsafe\nS1"
    assert rpc(server, "guardian.converse", message="hello")["message"] == "A friendly answer."


def test_erasing_a_profile_erases_its_safety_events_only(tmp_path, network):
    server = _server(tmp_path)
    sam = join_household(server, "Sam", "Child")
    network.classifier = "unsafe\nS1"
    rpc(server, "guardian.converse", message="x")
    bea = join_household(server, "Bea", "Child")
    rpc(server, "guardian.converse", message="y")
    ensure_administrator_with_pin(server)

    rpc(server, "profile.erase", profileId=sam, confirmName="Sam")

    assert [row[0] for row in _events(tmp_path)] == [bea]


def test_safety_events_are_pruned_with_the_activity_log_retention(tmp_path):
    clock_now = datetime(2026, 11, 7, tzinfo=UTC)
    store = SafetyEventStore(ProfileStore(tmp_path / "profiles.db"), clock=lambda: clock_now)
    store.record("p1", "hate", "input")
    clock_now = clock_now + timedelta(days=100)
    store.record("p1", "hate", "input")
    assert store.prune_older_than(90) == 1
    assert store.count() == 1


def test_the_backend_prunes_safety_events_when_retention_runs(tmp_path, network):
    server = _server(tmp_path)
    join_household(server, "Sam", "Child")
    network.classifier = "unsafe\nS1"
    rpc(server, "guardian.converse", message="x")
    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        connection.execute("UPDATE safety_events SET at = '2020-01-01T00:00:00+00:00'")
    server._runtime.retention.run_once()
    assert _events(tmp_path) == []


# --- The safety checker in the local AI setup (WP6b, M1-M2) ---------------------------------------------------------


def test_the_safety_checker_can_be_downloaded_but_never_chosen_to_answer(tmp_path, network):
    server = _server(tmp_path)
    ensure_administrator_with_pin(server)
    setup = server._runtime.ollama_setup

    assert setup.pulls._models["llama-guard3:1b"].min_budget_gb == 0
    refused = _raw(server, "ollama.useModel", model="llama-guard3:1b")
    assert "error" in refused
    assert server._runtime.ollama_setup.choice.current() != "llama-guard3:1b"


def test_status_and_recommendation_report_the_safety_checker(tmp_path, monkeypatch):
    from jarvis.config.ollama_models import CLASSIFIER
    from jarvis.interfaces.ollama_setup import HardwareInfo, ModelChoice, OllamaSetup, PullManager

    tags = {"models": [{"name": "qwen3.5:4b"}, {"name": CLASSIFIER.tag}]}

    def http_get(url, timeout):
        return json.dumps({"version": "0.40.6"} if url.endswith("/api/version") else tags).encode()

    setup = OllamaSetup(
        endpoint="http://x",
        choice=ModelChoice(tmp_path / "choice.json", default_model="qwen3.5:4b", environment_model=None, catalog_tags=["qwen3.5:4b"]),
        pulls=PullManager("http://x", (CLASSIFIER,)),
        environ={},
        http_get=http_get,
        hardware_reader=lambda: HardwareInfo(system="Windows", ram_bytes=32 * 2**30, gpu_bytes=8 * 2**30, unified_memory=False, free_disk_bytes=400 * 2**30),
    )
    assert setup.status()["classifier"] == {"model": "llama-guard3:1b", "installed": True}
    advice = setup.recommendation()["classifier"]
    assert advice["tag"] == "llama-guard3:1b" and advice["installed"] is True and advice["downloadGb"] == 1.5
    tags["models"] = [{"name": "qwen3.5:4b"}]
    assert setup.status()["classifier"]["installed"] is False

# --- WP6b review fixes (Copilot M-1, L-1, L-3) -------------------------------------------------------------------


@pytest.mark.parametrize("length", [0, 1, 3999, 4000, 4001, 7600, 7601, 8000, 12345, 40000])
def test_long_text_is_split_into_overlapping_pieces_that_cover_every_character(length):
    from jarvis.interfaces.moderation import PIECE_CHARS, PIECE_OVERLAP_CHARS, split_for_checking

    text = "".join(chr(65 + index % 26) for index in range(length))
    pieces = split_for_checking(text)
    step = PIECE_CHARS - PIECE_OVERLAP_CHARS
    covered = set()
    for number, piece in enumerate(pieces):
        start = number * step
        assert piece == text[start : start + PIECE_CHARS]
        assert len(piece) <= PIECE_CHARS
        covered.update(range(start, start + len(piece)))
    assert covered == set(range(length))
    if len(pieces) > 1:
        # Neighbouring pieces share PIECE_OVERLAP_CHARS characters.
        assert pieces[0][-PIECE_OVERLAP_CHARS:] == pieces[1][:PIECE_OVERLAP_CHARS]


def test_a_long_reply_is_checked_in_pieces_and_an_unsafe_ending_is_caught():
    long_reply = "Once upon a time. " * 600 + "UNSAFE ENDING"

    def transport(url, body, timeout):
        messages = json.loads(body)["messages"]
        assert len(messages[-1]["content"]) <= 4000
        content = "unsafe\nS1" if "UNSAFE ENDING" in messages[-1]["content"] else "safe"
        return json.dumps({"message": {"content": content}}).encode()

    verdict = ModerationService("http://x", transport=transport).check_output("tell me a long story", long_reply)
    assert verdict.allowed is False and verdict.category == "violent_crimes"


def test_a_long_reply_fails_closed_if_any_piece_cannot_be_checked():
    calls = []

    def transport(url, body, timeout):
        calls.append(1)
        if len(calls) == 2:
            raise TimeoutError
        return json.dumps({"message": {"content": "safe"}}).encode()

    verdict = ModerationService("http://x", transport=transport).check_output("q", "word " * 2000)
    assert verdict.unavailable and len(calls) >= 3


def test_self_harm_in_any_piece_takes_priority():
    def transport(url, body, timeout):
        piece = json.loads(body)["messages"][-1]["content"]
        content = "unsafe\nS11" if "HARM" in piece else ("unsafe\nS1" if "CRIME" in piece else "safe")
        return json.dumps({"message": {"content": content}}).encode()

    reply = "CRIME " + "x" * 9000 + " HARM"
    assert ModerationService("http://x", transport=transport).check_output("q", reply).category == "self_harm"


def test_a_childs_question_to_claude_gets_the_child_safety_layer():
    from jarvis.interfaces.conversation import ConversationResponse as Response

    class _Cloud:
        available = True

        def __init__(self):
            self.requests = []

        def generate(self, request):
            self.requests.append(request)
            return Response(message="ok", provider="claude", is_model_reply=True)

    cloud = _Cloud()
    runtime = GuardianRuntime(conversation_provider=_Provider(), escalation_provider=cloud, moderation=_Moderation())
    runtime.start()
    runtime.escalate("q", "p1", role="Child", include_household=False, share_memory=False)
    runtime.escalate("q", "p2", role="Adult", include_household=False, share_memory=False)
    # Claude never gets the child's name, only the nameless line.
    assert cloud.requests[0].persona.endswith(f"{CHILD_SAFETY_LAYER} {CHILD_NO_NAME_LINE}")
    assert cloud.requests[1].persona == runtime.config.persona


def test_a_moderated_role_offer_to_ask_claude_is_limited_to_1000_characters(tmp_path, network):
    server = _server(tmp_path)
    join_household(server, "Sam", "Child")
    refused = _raw(server, "guardian.escalation.offer", message="a" * 1001)
    assert "too long" in refused["error"]["message"]