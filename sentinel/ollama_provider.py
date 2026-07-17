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
from typing import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.providers import ProviderRequest, ProviderResponse

Transport = Callable[[str, bytes, dict[str, str], float], bytes]

DEFAULT_ENDPOINT = "http://localhost:11434"


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

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        endpoint = self._configuration.endpoint or DEFAULT_ENDPOINT
        payload = {
            "model": self._configuration.default_model,
            "prompt": request.prompt,
            "stream": False,
        }
        headers = {"Content-Type": "application/json"}

        try:
            raw_response = self._transport(
                f"{endpoint}/api/generate",
                json.dumps(payload).encode("utf-8"),
                headers,
                self._configuration.timeout_seconds,
            )
        except urllib.error.HTTPError as exc:
            # Mirrors OpenAIProvider/GeminiProvider: HTTP status codes are
            # plain protocol-level integers, safe to surface and diagnostically
            # useful, unlike raw response bodies or exception messages.
            msg = f"Ollama request failed: HTTPError (status {exc.code})."
            raise RuntimeError(msg) from exc
        except Exception as exc:
            # Deliberately expose only the exception type, never str(exc) -
            # same rationale as the cloud provider adapters.
            msg = f"Ollama request failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            msg = "Unexpected Ollama response shape: response was not valid JSON."
            raise RuntimeError(msg) from exc

        content = data.get("response")
        if not isinstance(content, str):
            msg = "Unexpected Ollama response shape: missing or non-string 'response' field."
            raise RuntimeError(msg)

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata={"model": self._configuration.default_model},
        )
