"""Anthropic Claude direct provider adapter for Sentinel.

Version 1.0's escalation provider (ADR-0023, ESR-0061 WP3a, EIP-ESR0061-003):
Claude answers only when the user has been offered it and confirmed - it is
never part of the default route. Mirrors `sentinel/gemini_provider.py`'s shape
deliberately: the same configuration validation, injectable transport,
conservative error handling (HTTP status codes only, never credential or raw
response bodies), `urllib` rather than an SDK (no new dependency in the
packaged sidecar, and the orchestrator alone owns retries).

Messages API facts this adapter relies on (re-confirmed live in WP3a):
`POST /v1/messages` with `x-api-key` and `anthropic-version`; `max_tokens` is
required; a safety decline is HTTP 200 with `stop_reason: "refusal"`;
overload is HTTP 529. On the default model (Sonnet 5.5) thinking cannot be
switched off, non-default sampling parameters are rejected and assistant
prefill is rejected, so none of those is ever sent; reply depth is steered
with `output_config.effort`.
"""

import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration, RetryPolicy
from sentinel.providers import (
    TRANSIENT_HTTP_STATUSES,
    DeadlineExceededError,
    ProviderDeclinedError,
    ProviderError,
    ProviderRequest,
    ProviderResponse,
    framed_prompt,
    is_timeout,
    remaining_timeout_budget,
)

Transport = Callable[[str, bytes, dict[str, str], float], bytes]

DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
# `max_tokens` is mandatory on this API. Used when the configuration sets no
# cap; it also bounds the worst-case cost the spend ledger reserves.
DEFAULT_MAX_TOKENS = 1024
DEFAULT_EFFORT = "low"
EFFORT_LEVELS = frozenset({"low", "medium", "high", "xhigh", "max"})
# Usage fields passed on to the ledger, as strings (ProviderResponse metadata
# is string-only).
_USAGE_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def _default_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


def _usage_metadata(data: dict) -> dict[str, str]:
    """The response's token counts as string metadata (empty if absent)."""

    usage = data.get("usage")
    found: dict[str, str] = {}
    if isinstance(usage, dict):
        for key in _USAGE_FIELDS:
            value = usage.get(key)
            if isinstance(value, int) and not isinstance(value, bool):
                found[f"usage_{key}"] = str(value)
    return found


class AnthropicProvider:
    """Sentinel execution provider backed by the Anthropic Messages API.

    The API key is sent only in the `x-api-key` header - never in a URL or the
    body - so it cannot reach a log through either.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        transport: Transport | None = None,
        effort: str | None = DEFAULT_EFFORT,
    ) -> None:
        if configuration.credential is None:
            msg = "Anthropic provider configuration requires a credential reference."
            raise ValueError(msg)
        if not configuration.default_model:
            msg = "Anthropic provider configuration requires a default model."
            raise ValueError(msg)
        if effort is not None and effort not in EFFORT_LEVELS:
            msg = f"Anthropic effort must be one of {sorted(EFFORT_LEVELS)}, got {effort!r}."
            raise ValueError(msg)
        self._configuration = configuration
        self._transport = transport or _default_transport
        self._effort = effort

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

    @property
    def model(self) -> str:
        """The model every request names (priced by the spend ledger)."""

        return self._configuration.default_model

    @property
    def max_tokens(self) -> int:
        """The output cap sent with every request (also the spend ledger's
        worst-case output)."""

        return self._configuration.max_output_tokens or DEFAULT_MAX_TOKENS

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        api_key = (os.environ.get(self._configuration.credential.environment_variable) or "").strip()
        if not api_key:
            msg = (
                "Anthropic credential not found in environment variable: "
                f"{self._configuration.credential.environment_variable}."
            )
            raise RuntimeError(msg)

        model = self._configuration.default_model
        endpoint = self._configuration.endpoint or DEFAULT_ENDPOINT
        # Earlier turns in their own roles; retained notes (when the caller
        # allows them at all) framed inside the current user message
        # (EBG-0142, ESR-0059 WP7).
        messages: list[dict[str, str]] = [{"role": turn.role, "content": turn.content} for turn in request.history]
        messages.append({"role": "user", "content": framed_prompt(request)})
        payload: dict[str, object] = {
            "model": model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }
        if request.system_prompt:
            payload["system"] = request.system_prompt
        if self._effort is not None:
            payload["output_config"] = {"effort": self._effort}
        headers = {
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }

        # Capped by the request's overall deadline, if any (EBG-0139).
        timeout_seconds, deadline_capped = remaining_timeout_budget(self._configuration.timeout_seconds, request)

        try:
            raw_response = self._transport(endpoint, json.dumps(payload).encode("utf-8"), headers, timeout_seconds)
        except urllib.error.HTTPError as exc:
            # Plain protocol-level integers: safe to surface (401 bad key, 402
            # billing, 429 rate limit, 529 overloaded), unlike response bodies.
            msg = f"Anthropic request failed: HTTPError (status {exc.code})."
            raise ProviderError(msg, transient=exc.code in TRANSIENT_HTTP_STATUSES) from exc
        except Exception as exc:
            # A timeout the turn deadline caused is the turn running out of time,
            # not this provider failing (EBG-0157 item 6).
            if deadline_capped and is_timeout(exc):
                msg = "Anthropic call hit the request deadline."
                raise DeadlineExceededError(msg) from exc
            # Exception type only, never str(exc): see GeminiProvider.
            msg = f"Anthropic request failed: {type(exc).__name__}."
            raise ProviderError(msg, transient=True) from exc

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            msg = "Unexpected Anthropic response shape: response was not valid JSON."
            raise RuntimeError(msg) from exc
        if not isinstance(data, dict):
            msg = "Unexpected Anthropic response shape: response was not a JSON object."
            raise RuntimeError(msg)  # noqa: TRY004 - RuntimeError is this provider's established public error contract

        stop_reason = data.get("stop_reason")
        if stop_reason == "refusal":
            # Safety classifiers decline with HTTP 200. The category is a short
            # protocol value (for example "cyber"), safe to name.
            details = data.get("stop_details")
            category = details.get("category") if isinstance(details, dict) else None
            suffix = f" ({category})" if isinstance(category, str) and category.isidentifier() else ""
            msg = f"Anthropic declined to answer this request{suffix}."
            raise ProviderDeclinedError(msg, _usage_metadata(data))
        if stop_reason == "tool_use":
            msg = "Anthropic returned an unsupported tool-use response."
            raise RuntimeError(msg)

        blocks = data.get("content")
        if not isinstance(blocks, list):
            msg = "Unexpected Anthropic response shape: missing content list."
            raise RuntimeError(msg)  # noqa: TRY004 - RuntimeError is this provider's established public error contract
        # Only text blocks are the answer. Thinking blocks (empty by default on
        # this model) are never shown.
        texts = [
            block["text"]
            for block in blocks
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str)
        ]
        content = "".join(texts)
        if not content.strip():
            msg = "Unexpected Anthropic response shape: no usable text blocks were present."
            raise RuntimeError(msg)

        metadata = {"model": str(data.get("model") or model)}
        if isinstance(stop_reason, str):
            metadata["stop_reason"] = stop_reason
        metadata.update(_usage_metadata(data))

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata=metadata,
        )
