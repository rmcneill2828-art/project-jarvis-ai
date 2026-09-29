"""Ollama local-fallback provider adapter for Sentinel.

Implements EBG-0075 per EIP-ESR0025-002. Mirrors `sentinel/openai_provider.py`
and `sentinel/gemini_provider.py`'s shape (configuration validation, injectable
`transport`, conservative error handling) with one deliberate difference:
Ollama's local HTTP API has no authentication, so this adapter must never
accept a `CredentialReference` - a future accidental copy-paste from the
cloud-provider pattern must fail loudly, not silently ignore a supplied
credential pointed at an unauthenticated local endpoint.
"""

import json
import urllib.error
import urllib.request
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration, RetryPolicy
from sentinel.providers import (
    TRANSIENT_HTTP_STATUSES,
    ProviderError,
    ProviderRequest,
    ProviderResponse,
    framed_prompt,
    history_transcript,
    remaining_timeout,
)

Transport = Callable[[str, bytes, dict[str, str], float], bytes]

DEFAULT_ENDPOINT = "http://localhost:11434"

# EBG-0109 Finding 1: reasoning-capable models (e.g. qwen3.5) default to a very
# large context window and an internal "thinking" pass when neither is bounded,
# which measured 3m15s for a trivial prompt against this project's own default
# model - comfortably exceeding OLLAMA_TIMEOUT_SECONDS (90s). Both are disabled
# unconditionally rather than only for models believed to be reasoning-capable,
# since Ollama ignores unrecognised/inapplicable options for other models.
DEFAULT_NUM_CTX = 4096


def _default_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


class OllamaProvider:
    """Sentinel execution provider backed by a local Ollama `/api/generate` server.

    Reasoning-capable models (e.g. qwen3.5) return an additional `thinking`
    field alongside `response` - confirmed via a real call during EIP-ESR0025-002
    scoping. That field must never be surfaced as conversation content, so only
    `response` is ever read.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        transport: Transport | None = None,
    ) -> None:
        if configuration.credential is not None:
            msg = "Ollama provider configuration must not carry a credential - the local API is unauthenticated."
            raise ValueError(msg)
        if not configuration.default_model:
            msg = "Ollama provider configuration requires a default model."
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
        endpoint = self._configuration.endpoint or DEFAULT_ENDPOINT
        payload: dict[str, object] = {
            "model": self._configuration.default_model,
            # EBG-0142 (ESR-0059 WP7): /api/generate takes one prompt, so
            # earlier turns go in as a delimited transcript ahead of the
            # framed current message - in the prompt, never in `system`.
            "prompt": "\n\n".join(
                part for part in (history_transcript(request), framed_prompt(request)) if part
            ),
            "stream": False,
            "think": False,
            "options": {"num_ctx": DEFAULT_NUM_CTX},
        }
        if request.system_prompt:
            payload["system"] = request.system_prompt
        headers = {"Content-Type": "application/json"}

        # Capped by the request's overall deadline, if any (EBG-0139).
        timeout_seconds = remaining_timeout(self._configuration.timeout_seconds, request)

        try:
            raw_response = self._transport(
                f"{endpoint}/api/generate",
                json.dumps(payload).encode("utf-8"),
                headers,
                timeout_seconds,
            )
        except urllib.error.HTTPError as exc:
            # Mirrors OpenAIProvider/GeminiProvider: HTTP status codes are
            # plain protocol-level integers, safe to surface and diagnostically
            # useful, unlike raw response bodies or exception messages.
            msg = f"Ollama request failed: HTTPError (status {exc.code})."
            # Retryable only for rate limits and server errors (EBG-0140).
            raise ProviderError(msg, transient=exc.code in TRANSIENT_HTTP_STATUSES) from exc
        except Exception as exc:
            # Deliberately expose only the exception type, never str(exc) -
            # same rationale as the cloud provider adapters.
            msg = f"Ollama request failed: {type(exc).__name__}."
            # Network failures and timeouts are retryable (EBG-0140).
            raise ProviderError(msg, transient=True) from exc

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            msg = "Unexpected Ollama response shape: response was not valid JSON."
            raise RuntimeError(msg) from exc

        # Valid JSON is not guaranteed to be an object - null, an array, or a
        # bare string/number would all parse successfully but have no `.get`
        # method, raising AttributeError instead of the intended RuntimeError
        # (Engineering Reviewer finding, ESR-0026 WP1 post-implementation review).
        if not isinstance(data, dict):
            msg = "Unexpected Ollama response shape: response was not a JSON object."
            raise RuntimeError(msg)  # noqa: TRY004 - RuntimeError is this provider's established public error contract, asserted by test_ollama_provider.py

        content = data.get("response")
        if not isinstance(content, str):
            msg = "Unexpected Ollama response shape: missing or non-string 'response' field."
            raise RuntimeError(msg)  # noqa: TRY004 - same established RuntimeError contract as above

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata={"model": self._configuration.default_model},
        )
