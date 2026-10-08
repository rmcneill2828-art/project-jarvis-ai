"""OpenAI direct provider adapter for Sentinel."""

import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration, RetryPolicy
from sentinel.providers import (
    TRANSIENT_HTTP_STATUSES,
    DeadlineExceededError,
    ProviderError,
    ProviderRequest,
    ProviderResponse,
    framed_prompt,
    is_timeout,
    remaining_timeout_budget,
)

Transport = Callable[[str, bytes, dict[str, str], float], bytes]


def _default_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


def _response_metadata(data: dict, choice: dict, model: str) -> dict[str, str]:
    """Model, finish reason and token usage as ProviderResponse's
    string-only metadata - matching what GeminiProvider already records
    (EBG-0140, ESR-0059 WP6), so token spend is visible for both providers."""

    metadata = {"model": model}
    finish_reason = choice.get("finish_reason")
    if finish_reason is not None:
        metadata["finish_reason"] = str(finish_reason)
    usage = data.get("usage")
    if isinstance(usage, dict):
        for key, value in usage.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[f"usage_{key}"] = str(value)
    return metadata


class OpenAIProvider:
    """Sentinel execution provider backed by the OpenAI Chat Completions API.

    Chat Completions is used deliberately rather than the newer Responses API:
    its request/response shape is stable, well-documented and verifiable, which
    matters more for a first adapter than using OpenAI's newest surface. This is
    a conservative starting point, not a permanent architecture decision.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        transport: Transport | None = None,
    ) -> None:
        if configuration.credential is None:
            msg = "OpenAI provider configuration requires a credential reference."
            raise ValueError(msg)
        if not configuration.default_model:
            msg = "OpenAI provider configuration requires a default model."
            raise ValueError(msg)
        self._configuration = configuration
        self._transport = transport or _default_transport

    @property
    def name(self) -> str:
        return self._configuration.provider_name

    @property
    def capabilities(self) -> tuple[str, ...]:
        return (self._configuration.default_capability,)

    @property
    def retry_policy(self) -> RetryPolicy:
        """This provider's configured retry policy, read by
        `ProviderOrchestrator` (EBG-0140, ESR-0059 WP6)."""

        return self._configuration.retry_policy

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        api_key = os.environ.get(self._configuration.credential.environment_variable)
        if not api_key:
            msg = (
                "OpenAI credential not found in environment variable: "
                f"{self._configuration.credential.environment_variable}."
            )
            raise RuntimeError(msg)

        endpoint = self._configuration.endpoint or "https://api.openai.com/v1/chat/completions"
        messages: list[dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        # EBG-0142 (ESR-0059 WP7): earlier turns in their own roles, and
        # retained notes framed inside the current user message - the system
        # message carries only the persona.
        messages.extend({"role": turn.role, "content": turn.content} for turn in request.history)
        messages.append({"role": "user", "content": framed_prompt(request)})
        payload: dict[str, object] = {
            "model": self._configuration.default_model,
            "messages": messages,
        }
        # `max_completion_tokens`, not the older `max_tokens`, which the
        # gpt-5 model family rejects (EBG-0143, ESR-0059 WP8).
        if self._configuration.max_output_tokens is not None:
            payload["max_completion_tokens"] = self._configuration.max_output_tokens
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Capped by the request's overall deadline, if any (EBG-0139).
        timeout_seconds, deadline_capped = remaining_timeout_budget(self._configuration.timeout_seconds, request)

        try:
            raw_response = self._transport(
                endpoint,
                json.dumps(payload).encode("utf-8"),
                headers,
                timeout_seconds,
            )
        except urllib.error.HTTPError as exc:
            # HTTP status codes are plain protocol-level integers, not sensitive -
            # safe to surface, and far more diagnostically useful than the
            # exception type alone (429 means exhausted quota, 401 means a bad
            # credential, 404 means a bad model name). Confirmed necessary in
            # practice: an early WP5 live run failed with a bare "HTTPError" and
            # required manually querying the OpenAI models endpoint to determine
            # the cause (exhausted API credit, HTTP 429) was a billing issue and
            # not a bad model identifier.
            msg = f"OpenAI request failed: HTTPError (status {exc.code})."
            # Retryable only for rate limits and server errors (EBG-0140).
            raise ProviderError(msg, transient=exc.code in TRANSIENT_HTTP_STATUSES) from exc
        except Exception as exc:
            # Deliberately expose only the exception type, never str(exc) - a raw
            # transport error message is not guaranteed safe to surface, and this
            # message can end up in ProviderOrchestrator's persisted audit trail.
            # A timeout the turn deadline caused is the turn running out of time,
            # not this provider failing (EBG-0157 item 6, ESR-0061 WP3a).
            if deadline_capped and is_timeout(exc):
                msg = "OpenAI call hit the request deadline."
                raise DeadlineExceededError(msg) from exc
            msg = f"OpenAI request failed: {type(exc).__name__}."
            # Network failures and timeouts are retryable (EBG-0140).
            raise ProviderError(msg, transient=True) from exc

        try:
            data = json.loads(raw_response)
            choice = data["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            msg = "Unexpected OpenAI response shape: missing choices[0].message.content."
            raise RuntimeError(msg) from exc

        # EBG-0140 (ESR-0059 WP6): `content` is null or empty for a refusal,
        # a tool call or a length cut-off with no text. Previously that
        # surfaced as an AttributeError from ProviderResponse's validation;
        # now it is this adapter's own clear, non-retryable failure. Only
        # finish_reason is surfaced - never the refusal or tool-call text.
        if not isinstance(content, str) or not content.strip():
            finish_reason = choice.get("finish_reason") if isinstance(choice, dict) else None
            msg = f"OpenAI returned no text content (finish_reason: {finish_reason})."
            raise RuntimeError(msg)

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata=_response_metadata(data, choice, self._configuration.default_model),
        )
