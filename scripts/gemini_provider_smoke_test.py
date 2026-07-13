"""
EBG-0051 live smoke test: first real call through Sentinel's GeminiProvider
against the actual Google Gemini API, equivalent to the OpenAI live validation
performed during ESR-0015 WP5 (scripts/wp5_first_conversation_demo.py).

Manual validation script, not part of the automated pytest suite - requires
a real API key and makes a real, billed network call. Must never run in CI.
Per ESR-0015 WP5 precedent, this script is run by the Programme Sponsor, not
by the AI collaborator, since it is a real billed external call.

Usage:
    Set GEMINI_API_KEY as a persistent environment variable before running.
    Optionally set GEMINI_MODEL to override the default model.

    python scripts/gemini_provider_smoke_test.py

This script never prints, logs, or persists the credential value. The audit
log is written outside the repository (Path.home()/.jarvis/logs/), not into
the working tree, since logs/ is not gitignored in this repository.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jarvis.interfaces.conversation import ConversationOrchestrator, ConversationService
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from sentinel.audit import JsonAuditRecorder
from sentinel.core import SentinelTrustGateway
from sentinel.gemini_provider import GeminiProvider
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.provider_config import CredentialReference, ProviderConfiguration

CREDENTIAL_ENV_VAR = "GEMINI_API_KEY"
MODEL_ENV_VAR = "GEMINI_MODEL"
AUDIT_LOG_PATH = Path.home() / ".jarvis" / "logs" / "gemini_smoke_test.jsonl"


def main() -> int:
    if not os.environ.get(CREDENTIAL_ENV_VAR):
        print(f"ERROR: {CREDENTIAL_ENV_VAR} is not set. Set it as a persistent environment variable before running.")
        return 1

    model = os.environ.get(MODEL_ENV_VAR, "gemini-2.5-flash")

    print("=== EBG-0051 Gemini Live Smoke Test - Confirmation ===")
    print(f"Model:        {model} (set {MODEL_ENV_VAR} to override)")
    print(f"Audit log:    {AUDIT_LOG_PATH}")
    print("This will make a real, billed Gemini API call.")
    confirm = input("Type RUN to continue: ")
    if confirm != "RUN":
        print("Aborted - no call was made.")
        return 1

    audit_recorder = JsonAuditRecorder(AUDIT_LOG_PATH)
    gateway = SentinelTrustGateway(audit_recorder=audit_recorder)

    configuration = ProviderConfiguration(
        provider_name="gemini",
        default_model=model,
        credential=CredentialReference(environment_variable=CREDENTIAL_ENV_VAR),
    )
    orchestrator = ProviderOrchestrator(audit_recorder=audit_recorder)
    orchestrator.register_provider(GeminiProvider(configuration))
    orchestrator.register_route(ProviderRoute(capability="text-generation", providers=("gemini",)))

    sentinel_provider = SentinelGatedConversationProvider(gateway=gateway, orchestrator=orchestrator)
    service = ConversationService(orchestrator=ConversationOrchestrator(provider=sentinel_provider))

    response = service.exchange("In one sentence, what is Project JARVIS AI?")

    # gateway and orchestrator share one audit_recorder; count it once, not
    # via both components' accessors, which would double-count every event.
    audit_event_count = len(audit_recorder.events())

    print()
    print("=== EBG-0051 Gemini Live Smoke Test - Evidence ===")
    print(f"Policy decision:             {gateway.decisions()[-1].decision.outcome.value}")
    print(f"Provider selected:           {response.provider}")
    print(f"Model configured:            {model}")
    print(f"Response:                    {response.message}")
    print(f"Sentinel decisions recorded: {len(gateway.decisions())}")
    print(f"Sentinel audit events:       {audit_event_count}")
    print(f"Orchestrator history:        {len(orchestrator.history())}")
    print(f"Audit log written to:        {AUDIT_LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
