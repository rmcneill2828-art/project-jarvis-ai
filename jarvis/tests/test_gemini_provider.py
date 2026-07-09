"""Tests for the Gemini direct provider adapter."""

import json
import urllib.error

import pytest

from sentinel.gemini_provider import GeminiProvider
from sentinel.provider_config import CredentialReference, ProviderConfiguration
from sentinel.providers import ProviderRequest


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "gemini",
        "default_model": "gemini-2.5-flash",
        "credential": CredentialReference(environment_variable="TEST_GEMINI_API_KEY"),
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_requires_credential_reference():
    with pytest.raises(ValueError):
        GeminiProvider(
            ProviderConfiguration(provider_name="gemini", default_model="gemini-2.5-flash")
        )


def test_requires_default_model():
    with pytest.raises(ValueError):
        GeminiProvider(
            _configuration(default_model=None)
        )


def test_execute_raises_when_environment_variable_missing(monkeypatch):
    monkeypatch.delenv("TEST_GEMINI_API_KEY", raising=False)
    provider = GeminiProvider(_configuration(), transport=lambda *a: b"{}")

    with pytest.raises(RuntimeError, match="not found in environment variable"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_returns_content_on_success(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-key")

    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body)
        captured["headers"] = headers
        captured["timeout"] = timeout
        return json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "hello back"}], "role": "model"}}]}
        ).encode("utf-8")

    provider = GeminiProvider(_configuration(timeout_seconds=12.5), transport=fake_transport)
    response = provider.execute(ProviderRequest(prompt="hello"))

    assert response.content == "hello back"
    assert response.provider_name == "gemini"
    assert response.metadata["model"] == "gemini-2.5-flash"
    assert captured["timeout"] == 12.5
    assert captured["body"]["contents"] == [{"parts": [{"text": "hello"}]}]
    assert captured["headers"]["x-goog-api-key"] == "test-gemini-key"
    assert "gemini-2.5-flash:generateContent" in captured["url"]


def test_execute_does_not_put_credential_in_url(monkeypatch):
    """Credential must travel via header, never appear in the request URL -
    unlike Google's docs-supported `?key=` query-parameter alternative, which
    this adapter deliberately does not use (see GeminiProvider docstring)."""

    monkeypatch.setenv("TEST_GEMINI_API_KEY", "sk-should-not-appear-in-url")

    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        return json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}
        ).encode("utf-8")

    provider = GeminiProvider(_configuration(), transport=fake_transport)
    provider.execute(ProviderRequest(prompt="hello"))

    assert "sk-should-not-appear-in-url" not in captured["url"]


def test_execute_wraps_transport_error_without_leaking_message(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-super-secret-key")

    def failing_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        raise RuntimeError("HTTP 401: test-gemini-super-secret-key rejected")

    provider = GeminiProvider(_configuration(), transport=failing_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "test-gemini-super-secret-key" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_execute_surfaces_http_status_code_without_leaking_body(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-key")

    def rate_limited_transport(url: str, body: bytes, headers: dict[str, str], timeout: float):
        raise urllib.error.HTTPError(
            url, 429, "RESOURCE_EXHAUSTED: test-gemini-key quota exceeded", hdrs=None, fp=None
        )

    provider = GeminiProvider(_configuration(), transport=rate_limited_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "status 429" in str(excinfo.value)
    assert "test-gemini-key" not in str(excinfo.value)
    assert "RESOURCE_EXHAUSTED" not in str(excinfo.value)


def test_execute_raises_on_malformed_response(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-key")
    provider = GeminiProvider(_configuration(), transport=lambda *a: b'{"unexpected": true}')

    with pytest.raises(RuntimeError, match="Unexpected Gemini response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_raises_on_empty_candidates(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-key")
    provider = GeminiProvider(_configuration(), transport=lambda *a: b'{"candidates": []}')

    with pytest.raises(RuntimeError, match="Unexpected Gemini response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_capabilities_and_name_reflect_configuration(monkeypatch):
    provider = GeminiProvider(_configuration(default_capability="text-generation"))

    assert provider.name == "gemini"
    assert provider.capabilities == ("text-generation",)


def test_endpoint_override_is_respected(monkeypatch):
    monkeypatch.setenv("TEST_GEMINI_API_KEY", "test-gemini-key")

    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        return json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}
        ).encode("utf-8")

    provider = GeminiProvider(
        _configuration(endpoint="https://example-proxy.internal/gemini"),
        transport=fake_transport,
    )
    provider.execute(ProviderRequest(prompt="hello"))

    assert captured["url"] == "https://example-proxy.internal/gemini"
