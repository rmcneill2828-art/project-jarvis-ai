"""Tests for the OpenAI direct provider adapter."""

import json
import urllib.error

import pytest

from sentinel.openai_provider import OpenAIProvider
from sentinel.provider_config import CredentialReference, ProviderConfiguration
from sentinel.providers import ProviderRequest


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "openai",
        "default_model": "gpt-5.6-luna",
        "credential": CredentialReference(environment_variable="TEST_OPENAI_API_KEY"),
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_requires_credential_reference():
    with pytest.raises(ValueError):
        OpenAIProvider(
            ProviderConfiguration(provider_name="openai", default_model="gpt-5.6-luna")
        )


def test_requires_default_model():
    with pytest.raises(ValueError):
        OpenAIProvider(
            _configuration(default_model=None)
        )


def test_execute_raises_when_environment_variable_missing(monkeypatch):
    monkeypatch.delenv("TEST_OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider(_configuration(), transport=lambda *a: b"{}")

    with pytest.raises(RuntimeError, match="not found in environment variable"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_execute_returns_content_on_success(monkeypatch):
    monkeypatch.setenv("TEST_OPENAI_API_KEY", "sk-test-key")

    captured: dict[str, object] = {}

    def fake_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body)
        captured["headers"] = headers
        captured["timeout"] = timeout
        return json.dumps(
            {"choices": [{"message": {"role": "assistant", "content": "hello back"}}]}
        ).encode("utf-8")

    provider = OpenAIProvider(_configuration(timeout_seconds=12.5), transport=fake_transport)
    response = provider.execute(ProviderRequest(prompt="hello"))

    assert response.content == "hello back"
    assert response.provider_name == "openai"
    assert response.metadata["model"] == "gpt-5.6-luna"
    assert captured["timeout"] == 12.5
    assert captured["body"]["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["headers"]["Authorization"] == "Bearer sk-test-key"


def test_execute_wraps_transport_error_without_leaking_message(monkeypatch):
    monkeypatch.setenv("TEST_OPENAI_API_KEY", "sk-super-secret-key")

    def failing_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:
        raise RuntimeError("HTTP 401: sk-super-secret-key rejected")

    provider = OpenAIProvider(_configuration(), transport=failing_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "sk-super-secret-key" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_execute_surfaces_http_status_code_without_leaking_body(monkeypatch):
    monkeypatch.setenv("TEST_OPENAI_API_KEY", "sk-test-key")

    def rate_limited_transport(url: str, body: bytes, headers: dict[str, str], timeout: float):
        raise urllib.error.HTTPError(
            url, 429, "insufficient_quota: sk-test-key exhausted", hdrs=None, fp=None
        )

    provider = OpenAIProvider(_configuration(), transport=rate_limited_transport)

    with pytest.raises(RuntimeError) as excinfo:
        provider.execute(ProviderRequest(prompt="hello"))

    assert "status 429" in str(excinfo.value)
    assert "sk-test-key" not in str(excinfo.value)
    assert "insufficient_quota" not in str(excinfo.value)


def test_execute_raises_on_malformed_response(monkeypatch):
    monkeypatch.setenv("TEST_OPENAI_API_KEY", "sk-test-key")
    provider = OpenAIProvider(_configuration(), transport=lambda *a: b'{"unexpected": true}')

    with pytest.raises(RuntimeError, match="Unexpected OpenAI response shape"):
        provider.execute(ProviderRequest(prompt="hello"))


def test_capabilities_and_name_reflect_configuration(monkeypatch):
    provider = OpenAIProvider(_configuration(default_capability="text-generation"))

    assert provider.name == "openai"
    assert provider.capabilities == ("text-generation",)
