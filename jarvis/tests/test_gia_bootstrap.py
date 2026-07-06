from jarvis import (
    EngineeringReadinessContext,
    EngineeringRequest,
    GiaBootstrap,
    ReadinessState,
)


def test_gia_bootstrap_reports_ready_for_minimum_approved_request() -> None:
    request = EngineeringRequest(
        identifier="EIP-0001",
        objective="Implement GIA-BOOT v1.",
        scope=("Create the minimum GIA package structure.",),
    )

    context = GiaBootstrap().boot(request)

    assert context.request == request
    assert context.state == ReadinessState.READY
    assert context.ready is True
    assert context.findings == ()


def test_gia_bootstrap_reports_not_ready_without_required_request_inputs() -> None:
    request = EngineeringRequest(
        identifier=" ",
        objective=" ",
        scope=(),
    )

    context = GiaBootstrap().evaluate(request)

    assert context.state == ReadinessState.NOT_READY
    assert context.ready is False
    assert context.findings == (
        "Engineering request identifier is required.",
        "Engineering request objective is required.",
        "Approved engineering scope is required.",
    )


def test_engineering_request_normalises_scope_items() -> None:
    request = EngineeringRequest(
        identifier="EIP-0001",
        objective="Implement GIA-BOOT v1.",
        scope=(" readiness evaluation ", ""),
        out_of_scope=(" GIA-ENG ", " "),
    )

    assert request.scope == ("readiness evaluation",)
    assert request.out_of_scope == ("GIA-ENG",)


def test_public_gia_context_interface_is_available() -> None:
    request = EngineeringRequest(
        identifier="EIP-0001",
        objective="Implement GIA-BOOT v1.",
        scope=("Export public interfaces.",),
    )

    context = EngineeringReadinessContext(
        request=request,
        state=ReadinessState.READY,
    )

    assert context.ready is True
