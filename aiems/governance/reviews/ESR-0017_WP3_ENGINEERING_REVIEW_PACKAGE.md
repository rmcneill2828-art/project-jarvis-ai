# ESR-0017 WP3 - Engineering Review Package

**Status:** Working Report - not a controlled artefact (per PBK-0001 Working Report Lifecycle), not registered in REG-0001.

---

# 1. Purpose

This package hands ESR-0017 WP3 to the Engineering Reviewer (ChatGPT) for independent review, per the EE-0001 Lead/Reviewer trial. ESR-0017 is the trial's designated Cold Start Validation Session (Claude Lead, ChatGPT Reviewer, Section 3.4).

WP1 (ADR-0019) and WP2 (Guardian&harr;Sentinel connection) have both already been reviewed and closed. This package covers **WP3 only**. WP4 (five-session roadmap) has not started and remains on hold until WP3 is reviewed.

---

# 2. Session Context

ESR-0017 is open, with four Programme-Sponsor-approved Work Packages:

1. **WP1** (reviewed, closed) - UXP&harr;Backend Integration Architecture Decision.
2. **WP2** (reviewed, closed) - Connect Guardian Runtime through Sentinel.
3. **WP3** (this package) - Gemini provider adapter.
4. **WP4** (not started) - Five-session backlog progression roadmap.

Note on sequencing: WP3's provider file (`sentinel/gemini_provider.py`) was actually started before the Programme Sponsor's process correction that introduced per-WP review pauses (see WP1/WP2 review packages). It was left half-finished (no tests, unregistered, unvalidated) at that point and only completed - tests written, exported, validated - just before this package was produced, so that what reaches the Reviewer meets the same bar as WP1 and WP2 did (validated, self-reviewed, not a rough draft).

---

# 3. Problem WP3 Addresses

`PEM-001` (`aiems/evaluations/PEM-001_AI_PROVIDER_EVALUATION_MATRIX.md`) recorded its Decision Outcome in ESR-0015: Primary provider OpenAI (implemented that session), **Secondary provider Google Gemini** (not yet implemented), reasoning/coding comparison Anthropic, Gateway OpenRouter (experimentation only), local fallback Ollama. PEM-001's own text states `ProviderConfiguration`/`ProviderRegistry` were "deliberately left extensible for Gemini and Anthropic adapters without requiring changes to `SentinelTrustGateway` or `ProviderOrchestrator`."

Before this WP, Sentinel had exactly one external provider adapter (`sentinel/openai_provider.py`) plus the local deterministic provider - meaning Sentinel's health-aware failover logic (`ProviderOrchestrator`, implemented ESR-0014) had never been exercised against a second real external provider, only tested with stubs.

---

# 4. Change Made

`sentinel/gemini_provider.py`'s `GeminiProvider` mirrors `OpenAIProvider`'s shape and conventions deliberately:

- Same constructor validation (`credential` required, `default_model` required).
- Same transport-injection pattern (`Transport` callable type alias, `_default_transport` using `urllib.request`).
- Same conservative error handling: HTTP status codes are surfaced (diagnostically useful, not sensitive), all other exceptions are collapsed to `type(exc).__name__` only (never `str(exc)`, which could leak credentials or raw response bodies into logs/audit).
- Same `name` / `capabilities` property shape, same `ProviderResponse` construction with `metadata={"model": ...}`.

**Differences, driven by the actual Gemini API shape (not stylistic):**
- Request body: `{"contents": [{"parts": [{"text": prompt}]}]}` (Gemini's `generateContent` shape) vs. OpenAI's `{"model": ..., "messages": [{"role": "user", "content": prompt}]}`.
- Response parsing: `data["candidates"][0]["content"]["parts"][0]["text"]` vs. OpenAI's `data["choices"][0]["message"]["content"]`.
- Auth: `x-goog-api-key` header, not `Authorization: Bearer`. Deliberately **not** using Google's also-supported `?key=` query-parameter alternative, specifically so the credential never appears in a URL that could end up in logs - matching the reasoning already established for `OpenAIProvider`'s own header-based auth choice.
- Default endpoint is model-parameterised: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`, but respects `configuration.endpoint` as an override, same as `OpenAIProvider`.

`GeminiProvider` is exported from `sentinel/__init__.py` (added to `__all__`), matching `OpenAIProvider`'s existing export. It is **not** wired into any default `ProviderOrchestrator` construction or route - consistent with how `OpenAIProvider` itself is only ever manually registered (in `scripts/wp5_first_conversation_demo.py` and tests), never auto-registered in production code. `GeminiProvider` follows the same additive-but-unwired pattern already established for `TrustTierPolicy` in ESR-0016.

---

# 5. What to Review

Please assess, independently:

1. **API shape accuracy** - does the Gemini `generateContent` request/response shape (`contents`/`parts`/`text`, `candidates[0].content.parts[0].text`) match your knowledge of the actual API? This is the one place this WP couldn't mirror OpenAI's adapter mechanically - it had to get Gemini's real shape right.
2. **Credential handling** - confirm the `x-goog-api-key` header choice (over the `?key=` query parameter) is sound, and that `test_execute_does_not_put_credential_in_url` actually proves what it claims.
3. **Error-message hygiene** - same standard as `OpenAIProvider`: check `test_execute_wraps_transport_error_without_leaking_message` and `test_execute_surfaces_http_status_code_without_leaking_body` actually prevent credential/quota-message leakage, not just superficially.
4. **Test coverage parity** - `test_openai_provider.py` has 6 tests; `test_gemini_provider.py` has 11 (6 direct mirrors + `test_execute_does_not_put_credential_in_url`, `test_execute_raises_on_empty_candidates`, `test_endpoint_override_is_respected`, plus 2 more). Confirm the extra tests are genuinely additive coverage, not padding.
5. **Unwired-by-default claim** - confirm `GeminiProvider` is not reachable from any production code path without explicit registration (i.e. this WP does not change Sentinel's live behaviour for any existing user).
6. **Scope discipline** - confirm no changes to `SentinelTrustGateway`, `PolicyEngine`, `ProviderOrchestrator`, or `OpenAIProvider` itself.

---

# 6. Full File List and Diff

**New files:**
- `sentinel/gemini_provider.py` (113 lines - full text below)
- `jarvis/tests/test_gemini_provider.py` (11 tests - full text below)

**Modified file:**
- `sentinel/__init__.py` - added `GeminiProvider` import and `__all__` entry (diff below)

No other files were touched. `sentinel/openai_provider.py`, `sentinel/orchestrator.py`, `sentinel/core.py`, `sentinel/policy.py` are all unchanged.

## `sentinel/gemini_provider.py` (new file, full text)

```python
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
            content = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            msg = "Unexpected Gemini response shape: missing candidates[0].content.parts[0].text."
            raise RuntimeError(msg) from exc

        return ProviderResponse(
            provider_name=self.name,
            content=content,
            capability=request.capability,
            metadata={"model": model},
        )
```

## `jarvis/tests/test_gemini_provider.py` (new file, full text)

```python
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
```

## `sentinel/__init__.py` (diff)

```diff
--- a/sentinel/__init__.py
+++ b/sentinel/__init__.py
@@ -13,6 +13,7 @@ from sentinel.core import (
     SentinelResponse,
     SentinelTrustGateway,
 )
+from sentinel.gemini_provider import GeminiProvider
 from sentinel.local_provider import LocalEchoProvider, create_local_provider_registry
 from sentinel.openai_provider import OpenAIProvider
 from sentinel.policy import (
@@ -42,6 +43,7 @@ __all__ = [
     "AuditRecorder",
     "CredentialReference",
     "ExecutionProvider",
+    "GeminiProvider",
     "JsonAuditRecorder",
     "LocalEchoProvider",
     "MemoryAuditRecorder",
```

---

# 7. Validation Performed

- `pytest jarvis/tests/test_gemini_provider.py -v`: 11/11 passing.
- Full suite `pytest`: 163/163 passing (152 baseline going into WP3 + 11 new; zero regressions).
- `python scripts/validate_repository.py`: no new errors or warnings attributable to WP3 (WP3 touched no Markdown files, only Python source/tests).
- No live API call was made against Google's real Gemini endpoint - all tests use transport injection (fake/stub transports), same as `test_openai_provider.py`. This adapter has not been proven against the real Gemini API, only against its documented response shape as understood by the Lead.

---

# 8. Explicit Non-Claims

- This does not register `GeminiProvider` with any `ProviderOrchestrator` instance or route - it exists and is tested, but nothing in production code currently constructs or calls it. Wiring it into a live conversation path (the way `scripts/wp5_first_conversation_demo.py` did for `OpenAIProvider`) is not part of this WP.
- This does not verify the adapter against Google's real API - only against the response shape as documented/understood, via injected fake transports. A live smoke test (like ESR-0015 WP5's live OpenAI conversation, run by the Programme Sponsor) has not been done for Gemini.
- This does not change PEM-001, `ProviderConfigurationRegistry`, `ProviderOrchestrator`, or any other Sentinel file.
- This does not claim feature parity with `OpenAIProvider` beyond what's tested - e.g. no streaming, no multi-turn context, no function/tool calling.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| ESR-0017 | Parent session report for this Work Package. |
| ESR-0017 WP1/WP2 Review Packages | Prior Work Packages in this session, already reviewed and closed. |
| EE-0001 | Lead/Reviewer trial governing this review's process. |
| PEM-001 | Source of the "Gemini is the Secondary provider, next adapter to implement" decision this WP executes. |
| `sentinel/openai_provider.py` | The adapter this WP's shape and conventions were mirrored from. |

---

# 10. Reviewer Findings and Disposition

ChatGPT Engineering Reviewer returned: **0 Blocking, 0 Major, 3 Minor Observations**, all explicitly flagged by the Reviewer as not a WP3 issue / no action required now.

| # | Observation | Disposition |
|---|---|---|
| 1 | Response parsing assumes `candidates[0]` contains usable text; future Gemini responses may be safety-blocked, have empty `parts`, be tool responses, or structured output | **Accepted, deferred.** Correctly scoped by the Reviewer as not a WP3 issue. Folded into new EBG-0051 (Gemini Provider Production Readiness). |
| 2 | Only `{"model": ...}` metadata is returned; future providers may benefit from finish reason, token usage, safety ratings | **Accepted, deferred.** No action required now, per the Reviewer. Folded into EBG-0051. |
| 3 | Before Gemini becomes an enabled production provider, a live smoke test (equivalent to ESR-0015 WP5's live OpenAI validation) is required - this is deployment validation, not implementation validation | **Accepted.** Matches this package's own Section 8 non-claim that the adapter has not been proven against the real API. Folded into EBG-0051 as a required precondition, not optional, before any future EIP wires `GeminiProvider` into a production route. |

All three were bundled into one new backlog item (EBR-0001 1.15 to 1.16, EBG-0051) rather than three separate items, since they share the same trigger condition (before Gemini is wired into a production `ProviderOrchestrator` route).

WP3 is now considered reviewed and closed, pending Programme Sponsor acceptance of this disposition.
