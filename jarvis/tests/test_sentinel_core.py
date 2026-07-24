from jarvis import GuardianRuntime, GuardianRuntimeState
from sentinel import (
    SentinelDecisionOutcome,
    SentinelRequest,
    SentinelResponse,
    SentinelTrustGateway,
)


def test_sentinel_request_rejects_empty_source() -> None:
    try:
        SentinelRequest(source=" ", intent="provider.request")
    except ValueError as exc:
        assert str(exc) == "Sentinel request source must not be empty."
    else:
        raise AssertionError("Expected empty Sentinel request source to be rejected.")


def test_sentinel_request_rejects_empty_intent() -> None:
    try:
        SentinelRequest(source="Guardian", intent=" ")
    except ValueError as exc:
        assert str(exc) == "Sentinel request intent must not be empty."
    else:
        raise AssertionError("Expected empty Sentinel request intent to be rejected.")


def test_sentinel_allows_basic_trusted_boundary_request() -> None:
    gateway = SentinelTrustGateway()
    request = SentinelRequest(source="Guardian", intent="provider.request")

    response = gateway.evaluate(request)

    assert isinstance(response, SentinelResponse)
    assert response.decision.outcome == SentinelDecisionOutcome.ALLOW
    assert response.decision.requires_human_approval is False
    assert response.request is request
    assert gateway.decisions() == (response,)


def test_sentinel_routes_approval_required_request_for_review() -> None:
    gateway = SentinelTrustGateway()
    request = SentinelRequest(
        source="Guardian",
        intent="execute.high_risk_action",
        requires_approval=True,
    )

    response = gateway.evaluate(request)

    assert response.decision.outcome == SentinelDecisionOutcome.REVIEW
    assert response.decision.requires_human_approval is True
    assert "review" in response.message.lower()


def test_guardian_can_use_sentinel_as_first_client_boundary() -> None:
    guardian = GuardianRuntime()
    gateway = SentinelTrustGateway()

    guardian.start()
    response = gateway.evaluate(
        SentinelRequest(
            source="Guardian",
            intent="provider.request",
            metadata={"guardian_state": guardian.status().value},
        )
    )

    assert guardian.status() == GuardianRuntimeState.RUNNING
    assert response.decision.outcome == SentinelDecisionOutcome.ALLOW
    assert response.request.metadata["guardian_state"] == GuardianRuntimeState.RUNNING.value
