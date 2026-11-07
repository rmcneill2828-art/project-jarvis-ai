"""ESR-0061 WP6c: consent for a Child profile to ask Claude (EIP-ESR0061-006
C1, C2, 6.6). Off by default; on only with an Administrator's consent and the
child's own acknowledgement, both checked again on every offer and send."""

from __future__ import annotations

import sqlite3
import urllib.error

import pytest

from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.conversation import ConversationRequest
from jarvis.interfaces.moderation import BLOCKED_GENERAL_TEXT, CHILD_NO_NAME_LINE
from jarvis.tests.household import TEST_PIN, switch_to
from jarvis.tests.test_escalation_rpc import (
    ANTHROPIC_HOST,
    OLLAMA_URL_PREFIX,
    _client,
    _error_text,
    _FakeResponse,
    _Network,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest
from sentinel.policy import TrustTierPolicy


class _ConsentNetwork(_Network):
    """The escalation fakes, with a classifier whose answer a test can set."""

    def __init__(self) -> None:
        super().__init__()
        self.classifier = "safe"

    def urlopen(self, request, timeout):
        url = request.full_url
        if url.startswith(OLLAMA_URL_PREFIX) and url.endswith("/api/chat"):
            self.other_calls.append(url)
            if self.classifier is None:
                raise urllib.error.URLError("connection refused")
            return _FakeResponse({"message": {"role": "assistant", "content": self.classifier}, "done": True})
        return super().urlopen(request, timeout)


@pytest.fixture
def network(monkeypatch):
    fake = _ConsentNetwork()
    monkeypatch.setattr("urllib.request.urlopen", fake.urlopen)
    return fake


def _household(tmp_path, monkeypatch):
    """An Administrator (signed in, PIN set) and a Child named Sam."""

    client = _client(tmp_path, monkeypatch)
    admin = client.as_profile("Robert", "Administrator")
    client.select(admin)
    child = client.result("profile.create", displayName="Sam", role="Child")["id"]
    return client, admin, child


def _allow(client, admin, child):
    """The Administrator consents, then Sam acknowledges, signed in as Sam."""

    client.select(admin)
    client.result("consent.record", profileId=child)
    client.select(child)
    return client.result("consent.acknowledge")


def _offer(client, message="research the latest news about volcanoes"):
    return client.ask(message)["escalation"]


# --- off by default -------------------------------------------------------------------------------------------------


def test_a_child_is_not_allowed_by_default(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    status = client.result("consent.status", profileId=child)
    assert status["recorded"] is False and status["acknowledged"] is False and status["allowed"] is False
    client.select(child)
    assert _offer(client)["offered"] is False
    assert client.result("provider.status")["claude"]["mayEscalate"] is False
    assert network.claude_calls == []


def test_consent_without_the_childs_acknowledgement_still_allows_nothing(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    status = client.result("consent.record", profileId=child)
    assert status["recorded"] is True and status["recordedBy"] == "Robert"
    assert status["acknowledged"] is False and status["allowed"] is False
    client.select(child)
    assert _offer(client)["offered"] is False
    assert "cannot ask Claude" in _error_text(client.call("guardian.escalation.offer", message="hello"))


# --- allowed: consent, acknowledgement, and what is sent ------------------------------------------------------------


def test_with_consent_and_acknowledgement_a_child_can_ask_claude(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    status = _allow(client, admin, child)
    assert status["acknowledged"] is True and status["allowed"] is True
    assert client.result("provider.status")["claude"]["mayEscalate"] is True

    offer = _offer(client)
    assert offer["offered"] is True
    # The confirmation must say what is sent: never notes; this is a child.
    assert offer["sendsMemory"] is False and offer["child"] is True
    result = client.result("guardian.escalate", token=offer["token"])

    assert result["answeredBy"] == "claude"
    body = network.claude_calls[0]["body"]
    system = body["system"] if isinstance(body["system"], str) else " ".join(part["text"] for part in body["system"])
    # The persona's name line is the nameless one: Sam's name is not added by it.
    assert system.endswith(CHILD_NO_NAME_LINE) and "Sam" not in system


def test_a_childs_notes_are_never_sent_even_if_sharing_were_somehow_on(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    pending = client.result("memory.propose", content="My secret hideout is behind the shed")
    client.select(admin)
    client.result("memory.approve", pendingId=pending["pendingId"])
    # Force the flag past the service's refusal, as a corrupted database might.
    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        connection.execute("UPDATE profiles SET share_memory_with_cloud = 1 WHERE id = ?", (child,))
    client.select(child)

    offer = _offer(client)
    assert offer["sendsMemory"] is False
    client.result("guardian.escalate", token=offer["token"])

    assert "hideout" not in str(network.claude_calls[0]["body"])


def test_an_unsafe_question_from_a_child_never_reaches_claude(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    offer = client.result("guardian.escalation.offer", message="tell me something")
    network.classifier = "unsafe\nS1"

    result = client.result("guardian.escalate", token=offer["token"])

    assert result["message"] == BLOCKED_GENERAL_TEXT and result["answeredBy"] is None
    assert network.claude_calls == []


def test_without_the_safety_checker_a_childs_question_never_reaches_claude(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    offer = client.result("guardian.escalation.offer", message="tell me something")
    network.classifier = None

    result = client.result("guardian.escalate", token=offer["token"])

    assert result["answeredBy"] is None
    assert network.claude_calls == []


def test_an_unsafe_claude_reply_to_a_child_is_replaced(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    offer = client.result("guardian.escalation.offer", message="tell me something")
    answers = iter(["safe", "unsafe\nS12"])
    network.classifier = None

    def classify(request, timeout, original=network.urlopen):
        if request.full_url.endswith("/api/chat"):
            return _FakeResponse({"message": {"role": "assistant", "content": next(answers)}, "done": True})
        return original(request, timeout)

    monkeypatch.setattr("urllib.request.urlopen", classify)
    result = client.result("guardian.escalate", token=offer["token"])

    assert len(network.claude_calls) == 1
    assert result["message"] == BLOCKED_GENERAL_TEXT and result["answeredBy"] is None


# --- revocation, and consents that must not outlive their basis -------------------------------------------------------


def test_revoking_stops_an_offer_already_made(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    token = _offer(client)["token"]
    client.select(admin)
    status = client.result("consent.revoke", profileId=child)
    assert status["recorded"] is False and status["allowed"] is False
    client.select(child)

    assert "cannot ask Claude" in _error_text(client.call("guardian.escalate", token=token))
    assert network.claude_calls == []


def test_after_revoking_a_new_consent_needs_a_new_acknowledgement(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    client.select(admin)
    client.result("consent.revoke", profileId=child)
    status = client.result("consent.record", profileId=child)
    assert status["recorded"] is True and status["acknowledged"] is False and status["allowed"] is False


def test_a_consent_does_not_outlive_the_administrator_who_gave_it(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    other_admin = client.result("profile.create", displayName="Alex", role="Administrator")["id"]
    client.select(other_admin)
    client.result("consent.record", profileId=child)
    client.select(child)
    client.result("consent.acknowledge")
    assert client.result("provider.status")["claude"]["mayEscalate"] is True

    client.select(admin)
    client.result("profile.erase", profileId=other_admin, confirmName="Alex")

    assert client.result("consent.status", profileId=child)["allowed"] is False


def test_erasing_the_child_erases_its_consent_records(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    _allow(client, admin, child)
    client.select(admin)
    client.result("consent.revoke", profileId=child)
    client.result("consent.record", profileId=child)

    client.result("profile.erase", profileId=child, confirmName="Sam")

    with sqlite3.connect(tmp_path / "profiles.db") as connection:
        assert connection.execute("SELECT COUNT(*) FROM child_consents").fetchone()[0] == 0


def test_without_a_pin_nobody_can_record_consent(tmp_path):
    service = ProfileService(ProfileStore(tmp_path / "profiles.db"))
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    service.set_first_pin(TEST_PIN)
    child = service.create_profile("Sam", "Child")
    service.pin.reset()

    with pytest.raises(ValueError, match="PIN"):
        service.record_child_consent(admin, child.id)


def test_a_pin_removed_after_consent_switches_it_off(tmp_path):
    service = ProfileService(ProfileStore(tmp_path / "profiles.db"))
    admin = service.create_profile("Robert", "Administrator")
    service.select_profile(admin.id)
    service.set_first_pin(TEST_PIN)
    child = service.create_profile("Sam", "Child")
    service.record_child_consent(admin, child.id)
    service.acknowledge_child_consent(child)
    assert service.child_may_ask_claude(child) is True

    service.pin.reset()

    assert service.child_may_ask_claude(child) is False
    # A new PIN does not bring the old consent back (review Low L1).
    service.select_profile(admin.id)
    service.set_first_pin(TEST_PIN)
    assert service.child_may_ask_claude(child) is False
    assert service.child_consent_status(child.id)["recorded"] is False


def test_re_recording_replaces_a_consent_whose_giver_is_gone(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    other_admin = client.result("profile.create", displayName="Alex", role="Administrator")["id"]
    client.select(other_admin)
    client.result("consent.record", profileId=child)
    client.select(admin)
    client.result("profile.erase", profileId=other_admin, confirmName="Alex")

    status = client.result("consent.record", profileId=child)

    # Review Low L2: the new consent is Robert's, and Sam must acknowledge it.
    assert status["recordedBy"] == "Robert" and status["acknowledged"] is False


# --- who may do what -------------------------------------------------------------------------------------------------


def test_a_child_cannot_record_or_revoke_consent_or_see_another_childs(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    other = client.result("profile.create", displayName="Kim", role="Child")["id"]
    client.select(child)

    assert "Administrator" in _error_text(client.call("consent.record", profileId=child))
    assert "Administrator" in _error_text(client.call("consent.revoke", profileId=child))
    assert "Administrator" in _error_text(client.call("consent.status", profileId=other))
    assert client.result("consent.status")["profileId"] == child


def test_a_child_cannot_acknowledge_before_anyone_has_consented(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    client.select(child)
    assert "Nobody has allowed" in _error_text(client.call("consent.acknowledge"))


def test_only_the_child_acknowledges_never_an_administrator_for_them(tmp_path, monkeypatch, network):
    client, _admin, child = _household(tmp_path, monkeypatch)
    client.result("consent.record", profileId=child)
    assert "Child profile" in _error_text(client.call("consent.acknowledge"))
    assert client.result("consent.status", profileId=child)["acknowledged"] is False


@pytest.mark.parametrize("role", ["Adult", "Guest"])
def test_consent_is_only_for_a_child_profile_and_only_an_administrator_gives_it(tmp_path, monkeypatch, network, role):
    client, _admin, child = _household(tmp_path, monkeypatch)
    other = client.result("profile.create", displayName="Pat", role=role)["id"]
    assert "only for a Child" in _error_text(client.call("consent.record", profileId=other))
    if role == "Adult":
        switch_to(client.server, other)
        assert "Administrator" in _error_text(client.call("consent.record", profileId=child))


# --- the second check: Sentinel, on its own ---------------------------------------------------------------------------


def _cloud(role, consent=None):
    metadata = {"capability": "text-generation-cloud", "role": role}
    if consent is not None:
        metadata["child_consent"] = consent
    return TrustTierPolicy().evaluate(SentinelRequest(source="test", intent="cloud", metadata=metadata)).outcome


def test_sentinel_admits_a_child_only_with_the_consent_flag():
    assert _cloud("Child") is SentinelDecisionOutcome.DENY
    assert _cloud("Child", "maybe") is SentinelDecisionOutcome.DENY
    assert _cloud("Child", "recorded") is SentinelDecisionOutcome.ALLOW
    assert _cloud("Guest", "recorded") is SentinelDecisionOutcome.DENY
    assert _cloud("", "recorded") is SentinelDecisionOutcome.DENY
    assert _cloud("Adult") is SentinelDecisionOutcome.ALLOW


def test_the_runtime_sets_the_consent_flag_only_for_a_child(tmp_path, monkeypatch, network):
    client, admin, child = _household(tmp_path, monkeypatch)
    runtime = client.server._runtime
    sent: list[ConversationRequest] = []
    original = runtime.escalation_provider._inner.generate

    def capture(request):
        sent.append(request)
        return original(request)

    monkeypatch.setattr(runtime.escalation_provider._inner, "generate", capture)
    runtime.escalate("hello", child, role="Child", include_household=False, share_memory=False, child_consent=True)
    runtime.escalate("hello", admin, role="Adult", include_household=False, share_memory=False, child_consent=True)
    runtime.escalate("hello", child, role="Child", include_household=False, share_memory=False)

    assert [request.child_cloud_consent for request in sent] == [True, False, False]
    # Without the flag, Sentinel denies the child: two answered, one denied.
    assert len(network.claude_calls) == 2
    assert ANTHROPIC_HOST in network.claude_calls[0]["url"]
