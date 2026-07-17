"""Tests for the Ollama local-fallback provider adapter (EBG-0075, EIP-ESR0025-002)."""

import json

import pytest

from sentinel.ollama_provider import DEFAULT_ENDPOINT, OllamaProvider
from sentinel.provider_config import CredentialReference, ProviderConfiguration
from sentinel.providers import ProviderRequest


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {"provider_name": "ollama", "default_model": "qwen3.5:2b"}
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_rejects_configuration_with_a_credential():
    with pytest.raises(ValueError, match="must not carry a credential"):
        OllamaProvider(
            _configuration(credential=CredentialReference(environment_variable="SHOULD_NOT_EXIST"))
        )


def test_requires_default_model():
    with pytest.raises(ValueError):
        OllamaProvider(_configuration(default_model=None))


def test_execute_returns_content_on_success():
    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body)
        captured["headers"] = headers
        captured["timeout"] = timeout
        return json.dumps({"response": "pong", "done": True}).encode("utf-8")

    provider = OllamaProvider(_configuration(timeout_seconds=90.0), transport=fake_transport)
    response = provider.execute(ProviderRequest(prompt="ping"))

    assert response.content == "pong"
    assert response.provider_name == "ollama"
    assert response.metadata["model"] == "qwen3.5:2b"
    assert captured["timeout"] == 90.0
    assert captured["body"] == {"model": "qwen3.5:2b", "prompt": "ping", "stream": False}
    assert captured["url"] == f"{DEFAULT_ENDPOINT}/api/generate"
    assert captured["headers"]["Content-Type"] == "application/json"


def test_thinking_field_is_never_surfaced_in_content():
    """Reasoning-capable models (e.g. qwen3.5) return an extra 'thinking' field
    alongside 'response' - confirmed via a real call during EIP-ESR0025-002
    scoping. It must never leak into ProviderResponse.content."""

    provider = OllamaProvider(
        _configuration(),
        transport=lambda *a: json.dumps(
            {"response": "pong", "thinking": "the user said ping, I should reply pong", "done": True}
        ).encode("utf-8"),
    )

    response = provider.execute(ProviderRequest(prompt="ping"))

    assert response.content == "pong"
    assert "thinking" not in response.content
    assert "the user said ping" not in response.content


def test_endpoint_override_is_respected():
    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        return json.dumps({"response": "ok"}).encode("utf-8")

    provider = OllamaProvider(
        _configuration(endpoint="http://example-host:11434"),
        transport=fake_transport,
    )
    provider.execute(ProviderRequest(prompt="hello"))

    assert captured["url"] == "http://example-host:11434/api/generate"


def test_execute_raises_on_missing_response_field():
    provider = OllamaProvider(_configuration(), transport=lambda *a: b'{"done": true}')

    with pytest.raises(RuntimeError, match="Unexpected Ollama response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_raises_on_non_string_response_field():
    provider = OllamaProvider(_configuration(), transport=lambda *a: json.dumps({"response": 123}).encode("utf-8"))

    with pytest.raises(RuntimeError, match="Unexpected Ollama response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


@pytest.mark.parametrize("body", [b"null", b"[]", b'"just a string"', b"42"])
def test_execute_raises_on_valid_json_that_is_not_an_object(body):
    """Engineering Reviewer finding (ESR-0026 WP1 post-implementation review):
    valid JSON that isn't a dict (null, an array, a bare string/number) has no
    .get method - without a type check this raised AttributeError instead of
    the intended RuntimeError, breaking the adapter's conservative
    error-handling contract."""
    provider = OllamaProvider(_configuration(), transport=lambda *a: body)

    with pytest.raises(RuntimeError, match="Unexpected Ollama response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_raises_on_invalid_json():
    provider = OllamaProvider(_configuration(), transport=lambda *a: b"not-json")

    with pytest.raises(RuntimeError, match="response was not valid JSON"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_wraps_transport_error_without_leaking_message():
    def failing_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        raise RuntimeError("connection refused: some internal detail")

    provider = OllamaProvider(_configuration(), transport=failing_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "connection refused" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_execute_surfaces_http_status_code_without_leaking_body():
    import urllib.error

    def failing_transport(url: str, body: bytes, headers: dict[str, str], timeout: float):
        raise urllib.error.HTTPError(url, 500, "internal server detail", hdrs=None, fp=None)

    provider = OllamaProvider(_configuration(), transport=failing_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "status 500" in str(excinfo.value)
    assert "internal server detail" not in str(excinfo.value)


def test_capabilities_and_name_reflect_configuration():
    provider = OllamaProvider(_configuration(default_capability="text-generation"))

    assert provider.name == "ollama"
    assert provider.capabilities == ("text-generation",)


