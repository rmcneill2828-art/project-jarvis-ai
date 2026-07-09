# ESR-0017 WP2 - Engineering Review Package

**Status:** Working Report - not a controlled artefact (per PBK-0001 Working Report Lifecycle), not registered in REG-0001.

---

# 1. Purpose

This package hands ESR-0017 WP2 to the Engineering Reviewer (ChatGPT) for independent review, per the EE-0001 Lead/Reviewer trial. ESR-0017 is the trial's designated Cold Start Validation Session (Claude Lead, ChatGPT Reviewer, Section 3.4).

WP1 (ADR-0019, UXP&harr;Backend Integration Architecture) has already been reviewed and closed - 0 Blocking, 0 Major, 1 Minor (accepted and fixed). This package covers **WP2 only**. WP3 (Gemini provider adapter) is half-implemented and paused; WP4 (five-session roadmap) has not started. Both remain on hold until WP2 is reviewed.

---

# 2. Session Context

ESR-0017 is open (`aiems/governance/sessions/ESR-0017_ENGINEERING_SESSION_REPORT.md`), with four Programme-Sponsor-approved Work Packages:

1. **WP1** (reviewed, closed) - UXP&harr;Backend Integration Architecture Decision.
2. **WP2** (this package) - Connect Guardian Runtime through Sentinel.
3. **WP3** (paused, half-implemented) - Gemini provider adapter.
4. **WP4** (not started) - Five-session backlog progression roadmap.

---

# 3. Problem WP2 Addresses

Before this change, `jarvis/guardian/runtime.py`'s `GuardianRuntime` held no reference to Sentinel at all: its `"Guardian Provider Boundary"` service was hard-coded `ServiceStatus.UNAVAILABLE` with capability `"future-provider-selection"`, permanently. Meanwhile `jarvis/interfaces/sentinel_conversation.py`'s `SentinelGatedConversationProvider` already existed and was proven live in ESR-0015 (a working Sentinel-gated conversation path) - but nothing in `GuardianRuntime` ever used it.

This is also the literal next step named in `aiems/architecture/CURRENT_ARCHITECTURE.md`'s own roadmap: item 6, "Connect Guardian through Sentinel," immediately preceding item 7, "Deliver Guardian's first interactive conversation." `CURRENT_ARCHITECTURE.md` also states explicitly: "JARVIS/Guardian may depend on Sentinel. Sentinel must remain product-agnostic and must not depend on Guardian/JARVIS" - confirming a direct `GuardianRuntime` -> Sentinel dependency is architecturally sanctioned, one-directional.

---

# 4. Change Made

**Design constraint that shaped this implementation:** existing tests (`jarvis/tests/test_guardian_runtime.py`) assert `runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE` both at construction and after `start()`, for a `GuardianRuntime()` built with no arguments. Any change had to preserve this exactly - zero regressions was the hard requirement (144 tests passing baseline going in, 152 passing coming out).

**Approach:** `GuardianRuntime.__init__` gained a new optional parameter, `conversation_provider: ConversationProvider | None = None` (the existing `ConversationProvider` Protocol from `jarvis/interfaces/conversation.py` - `SentinelGatedConversationProvider` already implements it, so no new type was needed). Default is `None`, so `GuardianRuntime()` with no arguments is byte-for-byte behaviourally identical to before.

When a provider *is* supplied:
- `start()` flips `"Guardian Provider Boundary"` to `ServiceStatus.ONLINE` / `ServiceHealth.HEALTHY` and records a new `"guardian.provider_connected"` diagnostic event - mirroring exactly how the existing `"Guardian Runtime"` service already does this on `start()`.
- `stop()` flips it back to `OFFLINE`, again mirroring the existing `"Guardian Runtime"` service's own `stop()` pattern.
- A new `converse(message: str) -> ConversationResponse` method was added: returns an honest boundary message (not an exception) if no provider is connected, or if the runtime isn't currently `RUNNING`; otherwise delegates to the provider's `generate()`. The "return a message, don't raise" choice matches the existing pattern in `SentinelGatedConversationProvider.generate()` (e.g. its own "Sentinel did not allow this request to proceed" / "JARVIS could not reach an AI provider right now" responses).

No changes were made to `sentinel/` itself, to `SentinelGatedConversationProvider`, or to `ConversationProvider`'s Protocol definition. This is additive-only to `GuardianRuntime`.

---

# 5. What to Review

Please assess, independently:

1. **Zero-regression claim** - confirm `GuardianRuntime()` with no arguments really is unaffected. (`test_guardian_runtime_without_provider_leaves_provider_boundary_unavailable_after_start` is the regression guard - worth checking it actually tests what it claims.)
2. **`converse()` before-`start()` semantics** - is returning `NOT_RUNNING_RESPONSE` when a provider exists but the runtime hasn't been started the right behaviour, or should the provider be reachable regardless of runtime lifecycle state? (Lead's reasoning: Guardian shouldn't process conversation if its own runtime says `STOPPED`/`STARTING`, even if the plumbing beneath it would technically work.)
3. **Type coupling** - `GuardianRuntime` depends on `jarvis.interfaces.conversation.ConversationProvider` (a `Protocol`), not directly on `sentinel.*` types. Is that the right boundary, or should it be more explicit that this exists to connect to Sentinel?
4. **Test quality** - one test (`test_guardian_runtime_converse_end_to_end_through_real_sentinel_gateway`) exercises real `SentinelTrustGateway` + `ProviderOrchestrator`, not just a `ConversationProvider`-level stub. Confirm this is a meaningful proof of the Guardian&harr;Sentinel wiring and not redundant with the stub-based tests.
5. **Scope discipline** - confirm no Sentinel-side files were touched (only `jarvis/guardian/runtime.py` and `jarvis/tests/test_guardian_runtime.py` - see Section 6).
6. **Diagnostic event naming** - `"guardian.provider_connected"` - consistent enough with the existing `"guardian.initialised"` / `"guardian.starting"` / `"guardian.running"` / `"guardian.stopped"` / `"guardian.service_registered"` naming convention?

---

# 6. Full File List and Diff

**Modified files (2 total, both already existed):**
- `jarvis/guardian/runtime.py` - added `conversation_provider` parameter, `converse()` method, provider-boundary lifecycle wiring.
- `jarvis/tests/test_guardian_runtime.py` - added 8 new tests plus two test-double classes (`_StubConversationProvider`, `_StubSentinelProvider`).

No other files were touched.

```diff
--- a/jarvis/guardian/runtime.py
+++ b/jarvis/guardian/runtime.py
@@ -8,17 +8,35 @@ from jarvis.guardian.config import GuardianRuntimeConfig
 from jarvis.guardian.diagnostics import GuardianDiagnosticEvent
 from jarvis.guardian.state import GuardianRuntimeState
 from jarvis.guardian.status import GuardianRuntimeStatus
+from jarvis.interfaces.conversation import (
+    ConversationProvider,
+    ConversationRequest,
+    ConversationResponse,
+)
 from jarvis.services import JarvisService, ServiceHealth, ServiceStatus
 
 logger = logging.getLogger(__name__)
 
+NOT_CONNECTED_RESPONSE = "Guardian has no conversation provider connected."
+NOT_RUNNING_RESPONSE = "Guardian runtime is not running."
+
 
 class GuardianRuntime:
     """Minimum executable runtime boundary for Guardian."""
 
-    def __init__(self, config: GuardianRuntimeConfig | None = None) -> None:
+    def __init__(
+        self,
+        config: GuardianRuntimeConfig | None = None,
+        conversation_provider: ConversationProvider | None = None,
+    ) -> None:
         self._config = config or GuardianRuntimeConfig()
+        self._conversation_provider = conversation_provider
         self._state = GuardianRuntimeState.STOPPED
+        provider_capabilities = (
+            ("guardian.conversation",)
+            if conversation_provider is not None
+            else ("future-provider-selection",)
+        )
         self._services: dict[str, JarvisService] = {
             "Guardian Runtime": JarvisService(
                 name="Guardian Runtime",
@@ -36,7 +54,7 @@ class GuardianRuntime:
                 name="Guardian Provider Boundary",
                 status=ServiceStatus.UNAVAILABLE,
                 health=ServiceHealth.UNKNOWN,
-                capabilities=("future-provider-selection",),
+                capabilities=provider_capabilities,
             ),
         }
         self._diagnostics: list[GuardianDiagnosticEvent] = [
@@ -62,6 +80,14 @@ class GuardianRuntime:
         runtime_service = self._services["Guardian Runtime"]
         runtime_service.status = ServiceStatus.ONLINE
         runtime_service.health = ServiceHealth.HEALTHY
+        if self._conversation_provider is not None:
+            provider_service = self._services["Guardian Provider Boundary"]
+            provider_service.status = ServiceStatus.ONLINE
+            provider_service.health = ServiceHealth.HEALTHY
+            self._record(
+                "guardian.provider_connected",
+                f"Guardian provider boundary connected: {self._conversation_provider.name}.",
+            )
         self._state = GuardianRuntimeState.RUNNING
         self._record("guardian.running", "Guardian runtime foundation running.")
         logger.info("Guardian runtime foundation started.")
@@ -71,6 +97,8 @@ class GuardianRuntime:
         """Stop the Guardian runtime foundation."""
 
         self._services["Guardian Runtime"].stop()
+        if self._conversation_provider is not None:
+            self._services["Guardian Provider Boundary"].stop()
         self._state = GuardianRuntimeState.STOPPED
         self._record("guardian.stopped", "Guardian runtime foundation stopped.")
         logger.info("Guardian runtime foundation stopped.")
@@ -81,6 +109,21 @@ class GuardianRuntime:
 
         return self._state
 
+    def converse(self, message: str) -> ConversationResponse:
+        """Route a message through the connected conversation provider.
+
+        Returns a boundary response, rather than raising, when no provider is
+        connected or the runtime is not running - matching this codebase's
+        existing pattern of returning an honest message instead of a hidden
+        failure (see `SentinelGatedConversationProvider`).
+        """
+
+        if self._conversation_provider is None:
+            return ConversationResponse(message=NOT_CONNECTED_RESPONSE, provider="guardian-boundary")
+        if self._state is not GuardianRuntimeState.RUNNING:
+            return ConversationResponse(message=NOT_RUNNING_RESPONSE, provider="guardian-boundary")
+        return self._conversation_provider.generate(ConversationRequest(message=message))
+
     def register_service(self, service: JarvisService) -> JarvisService:
         """Register or replace a Guardian runtime service."""
```

```diff
--- a/jarvis/tests/test_guardian_runtime.py
+++ b/jarvis/tests/test_guardian_runtime.py
@@ -9,6 +9,40 @@ from jarvis import (
     ServiceHealth,
     ServiceStatus,
 )
+from jarvis.guardian.runtime import NOT_CONNECTED_RESPONSE, NOT_RUNNING_RESPONSE
+from jarvis.interfaces.conversation import ConversationRequest, ConversationResponse
+from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
+from sentinel.core import SentinelTrustGateway
+from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
+from sentinel.providers import ProviderRequest, ProviderResponse
+
+
+class _StubConversationProvider:
+    """Minimal ConversationProvider double for boundary-behaviour tests."""
+
+    name = "stub-conversation"
+
+    def __init__(self) -> None:
+        self.received: list[ConversationRequest] = []
+
+    def generate(self, request: ConversationRequest) -> ConversationResponse:
+        self.received.append(request)
+        return ConversationResponse(message=f"stub: {request.message}", provider=self.name)
+
+
+class _StubSentinelProvider:
+    name = "stub-sentinel-provider"
+
+    @property
+    def capabilities(self) -> tuple[str, ...]:
+        return ("text-generation",)
+
+    def execute(self, request: ProviderRequest) -> ProviderResponse:
+        return ProviderResponse(
+            provider_name=self.name,
+            content=f"echo: {request.prompt}",
+            capability=request.capability,
+        )
 
 
 def test_guardian_diagnostic_event_requires_timezone_aware_timestamp() -> None:
@@ -212,3 +246,107 @@ def test_guardian_runtime_status_snapshot_contains_event_history() -> None:
 
     assert snapshot.events == runtime.events()
     assert snapshot.events[-1].name == "guardian.running"
+
+
+def test_guardian_runtime_without_provider_leaves_provider_boundary_unavailable_after_start() -> None:
+    """Regression guard: default construction must be unaffected by the new
+    optional conversation_provider parameter."""
+
+    runtime = GuardianRuntime()
+
+    runtime.start()
+
+    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE
+    assert runtime.services()["Guardian Provider Boundary"].health == ServiceHealth.UNKNOWN
+    assert "guardian.provider_connected" not in [event.name for event in runtime.diagnostics()]
+
+
+def test_guardian_runtime_with_provider_connects_boundary_on_start() -> None:
+    provider = _StubConversationProvider()
+    runtime = GuardianRuntime(conversation_provider=provider)
+
+    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.UNAVAILABLE
+
+    runtime.start()
+
+    boundary = runtime.services()["Guardian Provider Boundary"]
+    assert boundary.status == ServiceStatus.ONLINE
+    assert boundary.health == ServiceHealth.HEALTHY
+    assert boundary.supports("guardian.conversation")
+    connected_events = runtime.diagnostics(name="guardian.provider_connected")
+    assert len(connected_events) == 1
+    assert provider.name in connected_events[0].message
+
+
+def test_guardian_runtime_provider_boundary_goes_offline_on_stop() -> None:
+    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())
+
+    runtime.start()
+    runtime.stop()
+
+    boundary = runtime.services()["Guardian Provider Boundary"]
+    assert boundary.status == ServiceStatus.OFFLINE
+    assert boundary.health == ServiceHealth.UNKNOWN
+
+
+def test_guardian_runtime_converse_without_provider_returns_boundary_message() -> None:
+    runtime = GuardianRuntime()
+    runtime.start()
+
+    response = runtime.converse("hello")
+
+    assert response.message == NOT_CONNECTED_RESPONSE
+    assert response.provider == "guardian-boundary"
+
+
+def test_guardian_runtime_converse_before_start_returns_not_running_message() -> None:
+    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())
+
+    response = runtime.converse("hello")
+
+    assert response.message == NOT_RUNNING_RESPONSE
+    assert response.provider == "guardian-boundary"
+
+
+def test_guardian_runtime_converse_after_stop_returns_not_running_message() -> None:
+    runtime = GuardianRuntime(conversation_provider=_StubConversationProvider())
+    runtime.start()
+    runtime.stop()
+
+    response = runtime.converse("hello")
+
+    assert response.message == NOT_RUNNING_RESPONSE
+
+
+def test_guardian_runtime_converse_delegates_to_connected_provider() -> None:
+    provider = _StubConversationProvider()
+    runtime = GuardianRuntime(conversation_provider=provider)
+    runtime.start()
+
+    response = runtime.converse("hello Guardian")
+
+    assert response.message == "stub: hello Guardian"
+    assert response.provider == "stub-conversation"
+    assert provider.received[0].message == "hello Guardian"
+
+
+def test_guardian_runtime_converse_end_to_end_through_real_sentinel_gateway() -> None:
+    """Proves the Guardian<->Sentinel wiring against real Sentinel components
+    (SentinelTrustGateway + ProviderOrchestrator), not just a conversation-level
+    stub - closing the gap flagged in ESR-0017: GuardianRuntime previously held
+    no reference to Sentinel at all."""
+
+    gateway = SentinelTrustGateway()
+    orchestrator = ProviderOrchestrator()
+    orchestrator.register_provider(_StubSentinelProvider())
+    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("stub-sentinel-provider",)))
+    sentinel_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)
+    runtime = GuardianRuntime(conversation_provider=sentinel_provider)
+
+    runtime.start()
+    response = runtime.converse("hello Guardian")
+
+    assert response.message == "echo: hello Guardian"
+    assert response.provider == "stub-sentinel-provider"
+    assert runtime.services()["Guardian Provider Boundary"].status == ServiceStatus.ONLINE
+    assert len(gateway.decisions()) == 1
```

---

# 7. Validation Performed

- `pytest jarvis/tests/test_guardian_runtime.py -v`: 24/24 passing (16 pre-existing + 8 new).
- Full suite `pytest`: 152/152 passing (144 baseline + 8 new; zero regressions).
- `python scripts/validate_repository.py`: no new errors or warnings attributable to WP2 (WP2 touched no Markdown files, only Python source/tests).

---

# 8. Explicit Non-Claims

- This does not implement or expose `converse()` through any UXP surface - per WP1/ADR-0019, that requires a backend bridge that doesn't exist yet (EBG-0050, not authorised for implementation).
- This does not change `SimpleApprovalPolicy` as Sentinel's production default, or any Sentinel-side policy/trust behaviour.
- This does not claim Guardian's conversation capability is "done" - only that the wiring between `GuardianRuntime` and Sentinel now exists and is tested, where before there was none.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| ESR-0017 | Parent session report for this Work Package. |
| ESR-0017 WP1 Review Package | Prior Work Package in this session, already reviewed and closed. |
| EE-0001 | Lead/Reviewer trial governing this review's process. |
| CURRENT_ARCHITECTURE.md | Names "Connect Guardian through Sentinel" as roadmap item 6, immediately preceding "Deliver Guardian's first interactive conversation" (item 7) - this WP implements item 6. |

---

# 10. Reviewer Findings and Disposition

ChatGPT Engineering Reviewer returned: **0 Blocking, 0 Major, 2 Minor Observations**, both explicitly flagged by the Reviewer as not required now / not a WP2 concern.

| # | Observation | Disposition |
|---|---|---|
| 1 | `NOT_CONNECTED_RESPONSE` / `NOT_RUNNING_RESPONSE` are becoming part of Guardian's external behaviour; if more boundary responses appear later, consider consolidating into a response catalogue | **Acknowledged, no action.** Two constants doesn't yet justify an abstraction - would be premature scaffolding for a pattern that doesn't exist yet. Revisit only if a third or fourth boundary response actually appears. |
| 2 | `converse()` is synchronous; ADR-0019 chose duplex JSON-RPC partly for async notifications; when EBG-0050 is implemented, consider whether Guardian should eventually expose a streaming conversation interface rather than replacing `converse()` | **Accepted.** Correctly scoped by the Reviewer as EBG-0050 implementation-time, not WP2. Folded into EBG-0050's backlog note (EBR-0001 1.14 to 1.15) so it isn't lost before that work begins. |

WP2 is now considered reviewed and closed, pending Programme Sponsor acceptance of this disposition.
