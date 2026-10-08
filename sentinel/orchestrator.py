"""Sentinel provider orchestration and resilience primitives."""

import logging
import random
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from sentinel.audit import DEFAULT_MAX_MEMORY_EVENTS, AuditEvent, AuditRecorder, MemoryAuditRecorder
from sentinel.core import SentinelDecisionOutcome, SentinelResponse
from sentinel.provider_config import RetryPolicy
from sentinel.providers import (
    DeadlineExceededError,
    ExecutionProvider,
    ProviderDeclinedError,
    ProviderRequest,
    ProviderResponse,
    execute_with_sentinel_decision,
)

logger = logging.getLogger(__name__)

# How long a provider that just failed is skipped before being tried again
# (EBG-0140, ESR-0059 WP6). Long enough to stop a dead provider costing its
# timeout on every turn of a conversation, short enough to notice recovery
# within a minute.
DEFAULT_CIRCUIT_COOLDOWN_SECONDS = 30.0


class ProviderHealth(Enum):
    """Provider runtime health states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"


@dataclass(frozen=True)
class ProviderRoute:
    """Ordered provider route for a capability."""

    capability: str
    providers: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability.strip():
            msg = "Provider route capability must not be empty."
            raise ValueError(msg)
        if not self.providers:
            msg = "Provider route must contain at least one provider."
            raise ValueError(msg)
        if any(not provider.strip() for provider in self.providers):
            msg = "Provider route provider names must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class ProviderExecutionRecord:
    """Record of a Sentinel provider orchestration attempt."""

    capability: str
    attempted_providers: tuple[str, ...]
    selected_provider: str | None
    succeeded: bool
    reason: str


@dataclass(frozen=True)
class OrchestratedProviderResponse:
    """Provider response with orchestration metadata."""

    provider_response: ProviderResponse
    execution_record: ProviderExecutionRecord


class ProviderOrchestrator:
    """Health-aware Sentinel provider orchestrator with failover."""

    def __init__(
        self,
        audit_recorder: AuditRecorder | None = None,
        circuit_cooldown_seconds: float = DEFAULT_CIRCUIT_COOLDOWN_SECONDS,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        random_fraction: Callable[[], float] = random.random,
    ) -> None:
        if circuit_cooldown_seconds < 0:
            msg = "Circuit cooldown seconds must not be negative."
            raise ValueError(msg)
        self._providers: dict[str, ExecutionProvider] = {}
        self._health: dict[str, ProviderHealth] = {}
        self._routes: dict[str, ProviderRoute] = {}
        # Most recent executions only (EBG-0144, ESR-0059 WP9).
        self._history: deque[ProviderExecutionRecord] = deque(maxlen=DEFAULT_MAX_MEMORY_EVENTS)
        self._audit_recorder = audit_recorder or MemoryAuditRecorder()
        # Circuit breaker state (EBG-0140, ESR-0059 WP6): provider name to the
        # clock time until which it is skipped after a failure. Only failures
        # open a circuit - a health set by an operator via set_health() is
        # unaffected. clock/sleep/random_fraction are injectable for tests.
        self._open_until: dict[str, float] = {}
        self._circuit_cooldown_seconds = circuit_cooldown_seconds
        self._clock = clock
        self._sleep = sleep
        self._random = random_fraction

    def register_provider(
        self,
        provider: ExecutionProvider,
        health: ProviderHealth = ProviderHealth.HEALTHY,
    ) -> ExecutionProvider:
        """Register or replace a provider and its health state."""

        if not provider.name.strip():
            msg = "Execution provider name must not be empty."
            raise ValueError(msg)
        if not provider.capabilities:
            msg = "Execution provider must expose at least one capability."
            raise ValueError(msg)
        self._providers[provider.name] = provider
        self._health[provider.name] = health
        return provider

    def set_health(self, provider_name: str, health: ProviderHealth) -> None:
        """Set provider health."""

        if provider_name not in self._providers:
            msg = f"Provider is not registered: {provider_name}."
            raise LookupError(msg)
        self._health[provider_name] = health

    def health(self, provider_name: str) -> ProviderHealth:
        """Return provider health."""

        if provider_name not in self._providers:
            msg = f"Provider is not registered: {provider_name}."
            raise LookupError(msg)
        return self._health[provider_name]

    def register_route(self, route: ProviderRoute) -> ProviderRoute:
        """Register an ordered route for a capability."""

        for provider_name in route.providers:
            if provider_name not in self._providers:
                msg = f"Provider route references unregistered provider: {provider_name}."
                raise LookupError(msg)
            if route.capability not in self._providers[provider_name].capabilities:
                msg = (
                    f"Provider {provider_name} does not support capability: "
                    f"{route.capability}."
                )
                raise ValueError(msg)
        self._routes[route.capability] = route
        return route

    def eligible_providers(self, capability: str) -> tuple[ExecutionProvider, ...]:
        """Return healthy or degraded providers eligible for a capability."""

        if not capability.strip():
            msg = "Provider capability must not be empty."
            raise ValueError(msg)

        if capability in self._routes:
            provider_names = self._routes[capability].providers
        else:
            provider_names = tuple(
                provider.name
                for provider in self._providers.values()
                if capability in provider.capabilities
            )

        return tuple(
            self._providers[name]
            for name in provider_names
            if self._health[name] in (ProviderHealth.HEALTHY, ProviderHealth.DEGRADED)
        )

    def execute(
        self,
        sentinel_response: SentinelResponse,
        request: ProviderRequest,
    ) -> OrchestratedProviderResponse:
        """Execute a provider request using route order, retry and failover.

        EBG-0140 (ESR-0059 WP6):

        * A non-ALLOW Sentinel decision raises `PermissionError` before any
          provider is touched. Previously it was caught as a provider
          failure and degraded every provider on the route.
        * Each provider gets up to its `retry_policy.max_attempts`, retrying
          only failures marked transient (rate limits, server errors,
          network failures), with exponential backoff and jitter - and never
          sleeping past the request's deadline.
        * A provider that fails is skipped for `circuit_cooldown_seconds`
          (its circuit is open), so a provider that is down stops costing
          its full timeout on every turn. After the cooldown it is tried
          again; a success closes the circuit and restores HEALTHY.
        """

        if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
            msg = "Sentinel decision does not allow provider execution."
            raise PermissionError(msg)

        attempted: list[str] = []
        cooling_down: list[str] = []
        last_error: Exception | None = None
        deadline_reached = False
        declined: ProviderDeclinedError | None = None

        for provider in self.eligible_providers(request.capability):
            # EBG-0139 (ESR-0059 WP5): once the request's overall deadline has
            # passed, stop - never start another provider call. A provider
            # skipped this way did not fail, so its health is left untouched.
            if request.deadline is not None and time.monotonic() >= request.deadline:
                deadline_reached = True
                break
            if self._circuit_is_open(provider.name):
                cooling_down.append(provider.name)
                continue
            attempted.append(provider.name)
            try:
                provider_response, attempts = self._execute_with_retry(sentinel_response, provider, request)
            except DeadlineExceededError:
                # EBG-0156 (ESR-0060 WP1b): the deadline passed between the
                # check above and the provider's own - the same "out of time,
                # not a fault" case, so health and circuit stay untouched.
                deadline_reached = True
                break
            except ProviderDeclinedError as exc:
                # ESR-0061 WP3a: the provider answered - it declined, on safety
                # grounds. Not a fault (health and circuit untouched) and not a
                # reason to ask another provider, which would let a decline be
                # evaded by failover.
                declined = exc
                break
            except Exception as exc:  # noqa: BLE001 - any provider failure must fail over, not just known exception types
                last_error = exc
                self._health[provider.name] = ProviderHealth.DEGRADED
                self._open_until[provider.name] = self._clock() + self._circuit_cooldown_seconds
                continue

            self._health[provider.name] = ProviderHealth.HEALTHY
            self._open_until.pop(provider.name, None)
            record = ProviderExecutionRecord(
                capability=request.capability,
                attempted_providers=tuple(attempted),
                selected_provider=provider.name,
                succeeded=True,
                reason="Provider execution succeeded.",
            )
            self._history.append(record)
            self._audit_recorder.record(
                AuditEvent(
                    event_type="provider_execution",
                    outcome="succeeded",
                    summary=(
                        f"Provider {provider.name} executed capability "
                        f"{request.capability}."
                    ),
                    metadata={
                        "capability": request.capability,
                        "selected_provider": provider.name,
                        "attempted_providers": ",".join(attempted),
                        "attempts": str(attempts),
                    },
                )
            )
            return OrchestratedProviderResponse(
                provider_response=provider_response,
                execution_record=record,
            )

        reason = "No healthy provider could execute the request."
        if declined is not None:
            reason = f"Provider declined the request: {attempted[-1]}."
        elif last_error is not None:
            # ESR-0061 WP2a (EBG-0157 item 2): the durable audit record and
            # the raised error name the failure's type (and, for a
            # ProviderError, whether it was transient) - never its free text,
            # which is safe today only because every adapter keeps content
            # out of its messages. The message goes to the local log.
            transient = getattr(last_error, "transient", None)
            kind = type(last_error).__name__ + {True: " (transient)", False: " (permanent)"}.get(transient, "")
            reason = f"Provider execution failed: {kind}"
            logger.warning("Provider execution failed: %s: %s", type(last_error).__name__, last_error)
        elif cooling_down:
            reason = f"Every eligible provider is cooling down after a recent failure: {', '.join(cooling_down)}."
        if deadline_reached and declined is None:
            reason = f"Request deadline reached after attempting: {', '.join(attempted) or 'no provider'}."
        record = ProviderExecutionRecord(
            capability=request.capability,
            attempted_providers=tuple(attempted),
            selected_provider=None,
            succeeded=False,
            reason=reason,
        )
        self._history.append(record)
        self._audit_recorder.record(
            AuditEvent(
                event_type="provider_execution",
                outcome="failed",
                summary=reason,
                metadata={
                    "capability": request.capability,
                    "attempted_providers": ",".join(attempted),
                    "cooling_down": ",".join(cooling_down),
                },
            )
        )
        if declined is not None:
            raise ProviderDeclinedError(reason, declined.metadata) from declined
        raise RuntimeError(reason)

    def _circuit_is_open(self, provider_name: str) -> bool:
        open_until = self._open_until.get(provider_name)
        return open_until is not None and self._clock() < open_until

    def _execute_with_retry(
        self,
        sentinel_response: SentinelResponse,
        provider: ExecutionProvider,
        request: ProviderRequest,
    ) -> tuple[ProviderResponse, int]:
        """Run one provider with its retry policy; return the response and the
        number of attempts it took, or raise the last failure."""

        policy = getattr(provider, "retry_policy", None) or RetryPolicy()
        attempt = 1
        while True:
            try:
                return execute_with_sentinel_decision(sentinel_response, provider, request), attempt
            except Exception as exc:
                if attempt >= policy.max_attempts or not getattr(exc, "transient", False):
                    raise
                # Exponential backoff with +/-50% jitter, so concurrent
                # clients do not retry in lockstep.
                delay = policy.backoff_seconds * (2 ** (attempt - 1)) * (0.5 + self._random())
                if request.deadline is not None and time.monotonic() + delay >= request.deadline:
                    raise
                self._sleep(delay)
                attempt += 1

    def history(self) -> tuple[ProviderExecutionRecord, ...]:
        """Return provider orchestration history."""

        return tuple(self._history)

    def audit_events(self) -> tuple[AuditEvent, ...]:
        """Return recorded Sentinel audit events."""

        return self._audit_recorder.events()
