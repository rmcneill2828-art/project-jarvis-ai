"""OpenAI direct provider adapter for Sentinel."""

import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.providers import ProviderRequest, ProviderResponse

Transport = Callable[[str, bytes, dict[str, str], float], bytes]


def _default_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


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

    def execute(self, request: ProviderRequest) -> ProviderResponse:
        api_key = os.environ.get(self._configuration.credential.environment_variable)
        if not api_key:
            msg = (
                "OpenAI credential not found in environment variable: "
                f"{self._configuration.credential.environment_variable}."
            )
            raise RuntimeError(msg)

        endpoint = self._configuration.endpoint or "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self._configuration.default_model,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            raw_response = self._transport(
                endpoint,
                json.dumps(payload).encode("utf-8"),
                headers,
                self._configuration.timeout_seconds,
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
            raise RuntimeError(msg) from exc
        except Exception as exc:
            # Deliberately expose only the exception type, never str(exc) - a raw
            # transport error message is not guaranteed safe to surface, and this
            # message can end up in ProviderOrchestrator's persisted audit trail.
            msg = f"OpenAI request failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        try:
            data = json.loads(raw_response)
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            msg = "Unexpected OpenAI response shape: missing choices[0].message.content."
            raise RuntimeError(msg) from exc

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata={"model": self._configuration.default_model},
        )
