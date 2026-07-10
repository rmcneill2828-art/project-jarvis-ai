"""Google Gemini direct provider adapter for Sentinel.

Second external provider adapter (after OpenAI, ESR-0015 WP3b), per PEM-001's
approved decision naming Gemini as the Secondary provider. Mirrors
`sentinel/openai_provider.py`'s shape deliberately: same configuration
validation, same transport-injection pattern, same conservative error handling
(surface HTTP status codes, never leak credential or raw response bodies).
"""

import json
import os
import urllib.error
import urllib.request
from typing import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.providers import ProviderRequest, ProviderResponse

Transport = Callable[[str, bytes, dict[str, str], float], bytes]


def _default_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: float) -> bytes:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


def _serialize_metadata(data: dict[str, object], candidate: dict[str, object], model: str) -> dict[str, str]:
    """Map Gemini response metadata into ProviderResponse's string-only contract."""
    metadata = {"model": model}

    finish_reason = candidate.get("finishReason")
    if finish_reason is not None:
        metadata["finish_reason"] = str(finish_reason)

    safety_ratings = candidate.get("safetyRatings")
    if safety_ratings is not None:
        metadata["safety_ratings"] = json.dumps(
            safety_ratings,
            sort_keys=True,
            separators=(",", ":"),
        )

    usage_metadata = data.get("usageMetadata")
    if isinstance(usage_metadata, dict):
        for key, value in usage_metadata.items():
            if value is not None:
                metadata[f"usage_{key}"] = (
                    str(value)
                    if isinstance(value, (str, int, float, bool))
                    else json.dumps(value, sort_keys=True, separators=(",", ":"))
                )

    return metadata


class GeminiProvider:
    """Sentinel execution provider backed by the Google Gemini generateContent API.

    The API key is sent via the `x-goog-api-key` header rather than the `?key=`
    query parameter Google's docs also support - deliberately, so the credential
    never appears in a URL that could end up in logs, consistent with how
    `OpenAIProvider` keeps its credential in an Authorization header rather than
    the request body or URL.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        transport: Transport | None = None,
    ) -> None:
        if configuration.credential is None:
            msg = "Gemini provider configuration requires a credential reference."
            raise ValueError(msg)
        if not configuration.default_model:
            msg = "Gemini provider configuration requires a default model."
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
                "Gemini credential not found in environment variable: "
                f"{self._configuration.credential.environment_variable}."
            )
            raise RuntimeError(msg)

        model = self._configuration.default_model
        endpoint = (
            self._configuration.endpoint
            or f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        )
        payload = {"contents": [{"parts": [{"text": request.prompt}]}]}
        headers = {
            "x-goog-api-key": api_key,
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
            # Mirrors OpenAIProvider: HTTP status codes are plain protocol-level
            # integers, safe to surface and diagnostically useful (429 quota,
            # 401/403 bad credential, 404 bad model name).
            msg = f"Gemini request failed: HTTPError (status {exc.code})."
            raise RuntimeError(msg) from exc
        except Exception as exc:
            # Deliberately expose only the exception type, never str(exc) - see
            # OpenAIProvider for the same rationale (raw transport error
            # messages are not guaranteed safe to surface or persist in audit).
            msg = f"Gemini request failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            msg = "Unexpected Gemini response shape: response was not valid JSON."
            raise RuntimeError(msg) from exc

        prompt_feedback = data.get("promptFeedback")
        if isinstance(prompt_feedback, dict) and prompt_feedback.get("blockReason"):
            reason = prompt_feedback["blockReason"]
            msg = f"Gemini response was safety-blocked ({reason})."
            raise RuntimeError(msg)

        try:
            candidate = data["candidates"][0]
            parts = candidate["content"]["parts"]
        except (KeyError, IndexError, TypeError) as exc:
            msg = "Unexpected Gemini response shape: missing candidates[0].content.parts."
            raise RuntimeError(msg) from exc

        if candidate.get("finishReason") == "SAFETY":
            msg = "Gemini response was safety-blocked (SAFETY)."
            raise RuntimeError(msg)

        if not isinstance(parts, list) or not parts:
            msg = "Unexpected Gemini response shape: candidates[0].content.parts was empty."
            raise RuntimeError(msg)

        if any(isinstance(part, dict) and "functionCall" in part for part in parts):
            msg = "Gemini returned an unsupported tool/function-call response."
            raise RuntimeError(msg)

        text_parts = [part["text"] for part in parts if isinstance(part, dict) and isinstance(part.get("text"), str)]
        if not text_parts:
            msg = "Unexpected Gemini response shape: no usable text parts were present."
            raise RuntimeError(msg)

        content = "".join(text_parts)
        metadata = _serialize_metadata(data, candidate, model)

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata=metadata,
        )
