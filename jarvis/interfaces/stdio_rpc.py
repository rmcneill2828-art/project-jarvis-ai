"""JSON-RPC 2.0 over stdio - the UXP-backend bridge entry point (ADR-0019).

Foundation scope only (ESR-0017 WP9): a persistent, newline-delimited
JSON-RPC 2.0 loop over stdin/stdout, intended to be spawned as a long-lived
child process by the Tauri shell. Wires a zero-config Guardian+Sentinel stack
(SentinelTrustGateway, wired with TrustTierPolicy per EBG-0074/ESR-0024, +
ProviderOrchestrator) by default. The route originally ended in a
deterministic LocalEchoProvider to prove the UXP-to-Guardian-to-Sentinel
path; that fallback was removed from the production route at ESR-0059 WP3
(EBG-0141) because it echoed the user's own message back as if Guardian
had answered. When no provider can answer, the user now gets an honest
failure reply instead.

The JSON-RPC 2.0 envelope is adopted now, even though only synchronous
request/response is implemented, specifically so EBG-0050's later streaming
notifications can be added without a breaking change (Reviewer finding 5).

EIP-ESR0031-002 (Streaming Notifications MVP) exercises that envelope for
the first time: `serve_forever()` now also runs a background heartbeat
thread that periodically writes a `system.heartbeat` JSON-RPC
notification - a message with no `id` key at all, the JSON-RPC 2.0 signal
distinguishing an unsolicited notification from a response (which always
carries `id`, even `null` for certain error cases). A single write lock is
shared between the main loop's response writes and the heartbeat thread's
notification writes so the two can never interleave partial JSON onto one
line.
"""

import base64
import json
import logging
import logging.handlers
import math
import os
import sys
import threading
import traceback
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

from jarvis.agents.contracts import AgentRequest, SpecialistAgent
from jarvis.agents.gia_agent import GiaObservabilityAgent
from jarvis.agents.gia_engineering_agent import GiaEngineeringAgent
from jarvis.agents.home_assistant_agent import HomeAssistantClient, HomeAssistantStateQueryAgent
from jarvis.config.ollama_models import MODELS as OLLAMA_CATALOG
from jarvis.gia.engineering_observability import EngineeringStateObserver
from jarvis.gia.observability import LocalResourceObserver
from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces import knowledge_graph
from jarvis.interfaces.activity_tracker import ActivityTracker
from jarvis.interfaces.escalation import (
    ESCALATION_ROLES,
    REASON_REQUESTED,
    EscalationOffers,
    MeteredCloudConversationProvider,
    allowance_payload,
    offer_reason,
)
from jarvis.interfaces.ollama_setup import DEFAULT_ENDPOINT as OLLAMA_DEFAULT_ENDPOINT
from jarvis.interfaces.ollama_setup import (
    ModelChoice,
    OllamaSetup,
    PullManager,
    read_hardware,
)
from jarvis.interfaces.orphan_watchdog import start_orphan_watchdog
from jarvis.interfaces.sentinel_agent import SentinelGatedAgentService
from jarvis.interfaces.sentinel_conversation import SentinelGatedConversationProvider
from jarvis.interfaces.voice import (
    GuardianSpeechProvider,
    GuardianTranscriptionProvider,
    SentinelGatedSpeechProvider,
    SentinelGatedTranscriptionProvider,
)
from jarvis.memory.service import PersonalMemoryService
from jarvis.memory.store import PersonalMemoryStore
from jarvis.shared.errors import (
    ClientFacingError,
    ClientFacingPermissionError,
    ClientFacingTypeError,
    ClientFacingValueError,
    public_type_name,
)
from jarvis.shared.spend_ledger import MICRO_DOLLARS_PER_DOLLAR, SpendLedger
from sentinel.anthropic_provider import AnthropicProvider
from sentinel.audit import JsonAuditRecorder
from sentinel.core import SentinelTrustGateway
from sentinel.kokoro_provider import KokoroProvider
from sentinel.ollama_provider import OllamaProvider
from sentinel.orchestrator import ProviderOrchestrator, ProviderRoute
from sentinel.policy import TrustTierPolicy
from sentinel.provider_config import CredentialReference, ProviderConfiguration, RetryPolicy
from sentinel.providers import CLOUD_TEXT_GENERATION_CAPABILITY, TEXT_GENERATION_CAPABILITY
from sentinel.whisper_provider import WhisperProvider

JSONRPC_VERSION = "2.0"

logger = logging.getLogger(__name__)

# Methods that can block for seconds to minutes on an external model, voice
# model or agent (EBG-0139, ESR-0059 WP5). serve_forever() runs these on a
# single dedicated worker, so status, memory, profile and knowledge calls
# keep answering while one is in flight instead of queueing behind it. One
# worker, not a pool: slow calls still run one at a time and in arrival
# order, so conversation turns can never overtake each other, and
# GuardianRuntime's conversation state is only ever touched from one thread.
# Responses carry their request id, and the Tauri host already routes
# responses by id, so a fast reply overtaking a slow one is safe.
SLOW_METHODS = frozenset(
    {"guardian.converse", "guardian.escalate", "guardian.speak", "guardian.transcribe", "guardian.agent.invoke"}
)

# Retry policy for the cloud providers (EBG-0140, ESR-0059 WP6): one retry
# after a transient failure (rate limit, server error, network failure),
# after a jittered backoff of about a second. ProviderOrchestrator only
# retries failures the adapter marks transient, and never sleeps past the
# turn deadline. Ollama keeps the default single attempt: it is local, and
# retrying a cold start that already took its full timeout would only
# double the wait.
CLOUD_RETRY_POLICY = RetryPolicy(max_attempts=2, backoff_seconds=1.0)

# Version 1.0 provider strategy (ADR-0023, ESR-0061 WP3a, EIP-ESR0061-003).
# Local Ollama answers every ordinary conversation. The Anthropic Claude API is
# the only cloud provider: it sits on its own capability, reached only by a
# confirmed escalation, never by failover. OpenAI and Gemini are unregistered
# (their adapters and tests stay, so the decision can be reversed - the Piper
# precedent, ESR-0053). The old selector variables below are ignored with one
# logged warning.
LEGACY_PROVIDER_ENV_VARS = ("JARVIS_PRIMARY_PROVIDER", "JARVIS_SECONDARY_PROVIDER")
ANTHROPIC_KEY_ENV_VAR = "ANTHROPIC_API_KEY"
CLAUDE_MODEL_ENV_VAR = "JARVIS_CLAUDE_MODEL"
# Programme Sponsor decision S1 (8 October 2026): Sonnet 5.5 at low effort.
DEFAULT_CLAUDE_MODEL = "claude-sonnet-5-5"
ANTHROPIC_TIMEOUT_SECONDS = 60.0
# Decision S4: a monthly cap of GBP 30, enforced as US dollars at a deliberately
# low fixed rate, with the provider Console's own limit as the hard backstop.
CLAUDE_CAP_GBP_ENV_VAR = "JARVIS_CLAUDE_MONTHLY_CAP_GBP"
USD_PER_GBP_ENV_VAR = "JARVIS_USD_PER_GBP"
DEFAULT_CLAUDE_CAP_GBP = 30.0
DEFAULT_USD_PER_GBP = 1.25
SPEND_DB_FILENAME = "spend.db"
OLLAMA_MODEL_CHOICE_FILENAME = "ollama_model.json"
# Downloading or choosing the local model changes what every profile talks to
# and uses disk and bandwidth, so it is for the household's adults.
MODEL_MANAGER_ROLES = frozenset({"Administrator", "Adult"})
CLOUD_NOT_PERMITTED_MESSAGE = "This profile cannot ask Claude. Ask an Administrator or Adult profile."

# Ollama (EBG-0075, EIP-ESR0025-002): unlike the cloud providers above, this
# has no credential gate - registered unconditionally, since a local, missing
# or unreachable Ollama installation fails over identically to any other
# provider failure via ProviderOrchestrator's existing exception-driven
# failover. Default model is the fastest of the four confirmed-installed
# models at scoping time - latency matters more than peak capability for a
# fallback role. Timeout is 90s, not the 30s default, to accommodate the
# confirmed ~64s cold-start model load.
OLLAMA_MODEL_ENV_VAR = "JARVIS_OLLAMA_MODEL"
OLLAMA_ENDPOINT_ENV_VAR = "JARVIS_OLLAMA_ENDPOINT"
DEFAULT_OLLAMA_MODEL = "qwen3.5:2b"
OLLAMA_TIMEOUT_SECONDS = 90.0


def _clean_env(environ: Mapping[str, str], name: str) -> str | None:
    """A configuration value, stripped; None when unset or blank.

    A whitespace-only value is truthy, so `environ.get(name) or default` used it
    as the setting (EBG-0161, found by the local pre-screen on 2 October 2026).
    Every model and endpoint variable goes through here instead.
    """

    value = (environ.get(name) or "").strip()
    return value or None

# Kokoro voice model paths (EIP-ESR0053-002, EBG-0125): replaces Piper as
# Guardian's production speech-synthesis provider, per the Programme
# Sponsor's decision following a real live listening comparison among
# Kokoro's four confirmed UK English voices. Unlike OLLAMA_MODEL_ENV_VAR
# above, neither has a sensible default - no voice model file is ever
# committed to the repository or auto-downloaded (a disclosed, one-time
# manual step, mirroring EIP-ESR0040-001 Section 6 item 9's original Piper
# precedent). Both must be present and non-blank for the capability to be
# available - absent either means no speech provider is wired, mirroring
# _build_real_provider()'s absent-credential handling exactly, not Ollama's
# has-a-default pattern. Kokoro's two-file requirement (a `.onnx` model plus
# a companion `voices` `.bin` file) is `sentinel/kokoro_provider.py`'s own
# disclosed deviation from Piper's single-file shape.
KOKORO_MODEL_PATH_ENV_VAR = "JARVIS_KOKORO_MODEL_PATH"
KOKORO_VOICES_PATH_ENV_VAR = "JARVIS_KOKORO_VOICES_PATH"

# Guardian's production voice choice (EIP-ESR0053-002): a genuine Programme
# Sponsor listening verdict, not a default guessed from names alone - four
# real .wav samples of Kokoro's confirmed UK voices were synthesized and
# delivered for comparison before this choice was made. bf_isabella is an
# automatic runtime fallback if bm_george's synthesis fails, not a second
# user-selectable option; language is fixed at British English. None of the
# three is env-var-configurable in this package - a future backlog item, not
# this one, if per-deployment voice configurability is wanted.
KOKORO_VOICE = "bm_george"
KOKORO_FALLBACK_VOICE = "bf_isabella"
KOKORO_LANG = "en-gb"

# Whisper model size or local path (EIP-ESR0047-001, EBG-0117): mirrors
# KOKORO_MODEL_PATH_ENV_VAR's absent-means-invisible pattern exactly, and is
# this capability's own approval gate per EIP-ESR0047-001 Section 5.2 -
# capability availability itself, not a per-request live approval this
# codebase has no mechanism to satisfy. No model is ever auto-downloaded
# without this variable being set first.
WHISPER_MODEL_PATH_ENV_VAR = "JARVIS_WHISPER_MODEL_PATH"

# Home Assistant read-only state-query agent (EBG-0127, WR-ESR0057-001
# Section 5): mirrors KOKORO_MODEL_PATH_ENV_VAR's absent-means-invisible
# pattern - both must be present for the agent to register at all; a
# missing base URL or token means the capability is not available on this
# machine, not a startup failure. The token is a genuine bearer credential
# (STD-0006 named-env-var indirection), read directly rather than wrapped
# in CredentialReference, matching how KOKORO_MODEL_PATH_ENV_VAR's own
# non-ProviderConfiguration-shaped capability reads its env vars directly.
HOME_ASSISTANT_URL_ENV_VAR = "JARVIS_HOME_ASSISTANT_URL"
HOME_ASSISTANT_TOKEN_ENV_VAR = "JARVIS_HOME_ASSISTANT_TOKEN"

# Personal Memory store location (EIP-ESR0027-001). Overridable so tests never
# touch the real store - the exact lesson learned from ESR-0026 WP1's Ollama
# test-isolation defect (a shared test helper making real network calls
# because nothing pointed it away from the real endpoint) applies here too,
# just for a local file instead of a network endpoint.
MEMORY_DB_PATH_ENV_VAR = "JARVIS_MEMORY_DB_PATH"
DEFAULT_MEMORY_DB_PATH = Path.home() / ".jarvis" / "memory" / "personal.db"

# Personal Memory backup destination (BRD-0001, EBG-0023). Same env-var/
# default/test-isolation convention as MEMORY_DB_PATH_ENV_VAR above - kept
# as a sibling directory of the database itself rather than inside it, so a
# backup file is never mistaken for a second live database on directory
# listing.
MEMORY_BACKUP_DIR_ENV_VAR = "JARVIS_MEMORY_BACKUP_DIR"
DEFAULT_MEMORY_BACKUP_DIR = Path.home() / ".jarvis" / "memory" / "backups"

# Log directory for the durable Sentinel audit trail and the backend's own
# log file (EBG-0144, ESR-0059 WP9). Unset, it is the `logs` directory beside
# the Personal Memory store's directory - ~/.jarvis/logs by default - so all
# of Guardian's local data lives under one root, and tests that already
# point JARVIS_MEMORY_DB_PATH at a temporary directory never write logs into
# the real home directory (the same isolation lesson as ESR-0026 WP1).
LOG_DIR_ENV_VAR = "JARVIS_LOG_DIR"
AUDIT_LOG_FILENAME = "audit.jsonl"
BACKEND_LOG_FILENAME = "backend.log"
BACKEND_LOG_MAX_BYTES = 5_000_000
BACKEND_LOG_BACKUP_COUNT = 3

# Identity/profile store location (EIP-ESR0046-001), mirroring the Personal
# Memory store's env-var/default/test-isolation convention exactly.
IDENTITY_DB_PATH_ENV_VAR = "JARVIS_IDENTITY_DB_PATH"
DEFAULT_IDENTITY_DB_PATH = Path.home() / ".jarvis" / "identity" / "profiles.db"

# Streaming Notifications MVP (EIP-ESR0031-002): interval between heartbeat
# notifications, overridable per JARVIS_MEMORY_DB_PATH's established
# test-isolation convention - a real 30-second sleep has no place in a test.
# Input size limits at the RPC boundary (EBG-0143, ESR-0059 WP8). Oversized
# input is refused with a clear error rather than passed on to a provider,
# a voice model or the memory store. MAX_MESSAGE_CHARS also keeps a
# worst-case turn - message, bounded history and memory notes (see
# jarvis/guardian/cognitive_core.py) - inside Ollama's 4096-token context
# (DEFAULT_NUM_CTX), which otherwise silently truncates the prompt.
MAX_MESSAGE_CHARS = 4_000
MAX_SPEAK_CHARS = 5_000
MAX_AUDIO_BASE64_CHARS = 20_000_000  # about 15 MB of audio - minutes of push-to-talk speech
MAX_MEMORY_CHARS = 2_000

# Optional output-token cap for every text provider (EBG-0143, ESR-0059 WP8).
# Off by default, deliberately: on reasoning models (OpenAI's gpt-5 family,
# Gemini 2.5) internal "thinking" tokens can count against the cap, so a cap
# chosen without a live test can leave replies empty. Set it once verified
# against the configured models; an absent, non-integer or non-positive
# value leaves output uncapped.
MAX_OUTPUT_TOKENS_ENV_VAR = "JARVIS_MAX_OUTPUT_TOKENS"

# Overall budget for one conversation turn, every provider tried included
# (EBG-0139, ESR-0059 WP5). Must stay below src-tauri/src/lib.rs's
# BACKEND_CALL_TIMEOUT (120s): past that, the shell stops waiting and the
# user sees a timeout instead of the honest provider-unavailable reply. The
# 20s margin covers Sentinel evaluation, prompt composition and IPC. With
# OpenAI (30s) + Gemini (30s) + Ollama (90s), the unbounded worst case was
# 150s. An absent, blank, non-numeric or non-positive value uses the default
# rather than failing startup.
TURN_DEADLINE_ENV_VAR = "JARVIS_TURN_DEADLINE_SECONDS"
DEFAULT_TURN_DEADLINE_SECONDS = 100.0

HEARTBEAT_INTERVAL_ENV_VAR = "JARVIS_HEARTBEAT_INTERVAL_SECONDS"
DEFAULT_HEARTBEAT_INTERVAL_SECONDS = 30.0

# Standard JSON-RPC 2.0 pre-defined error codes, plus one server-defined code
# in the reserved -32000 to -32099 range for internal handler failures.
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32000


def _build_anthropic_provider(environ: Mapping[str, str]) -> AnthropicProvider | None:
    """Build the Claude escalation provider, or None if no key is configured.

    An absent or whitespace-only key means "not available on this machine", not
    a startup failure: escalation is simply never offered, and the local route is
    unaffected (the honest-degradation pattern of ESR-0017 WP9; EBG-0141). A
    whitespace-only key is absent, not present (ESR-0059 WP4): treating it as
    present would offer an escalation that fails on every call.
    """

    if _clean_env(environ, ANTHROPIC_KEY_ENV_VAR) is None:
        return None
    configuration = ProviderConfiguration(
        provider_name="anthropic",
        default_capability=CLOUD_TEXT_GENERATION_CAPABILITY,
        default_model=_clean_env(environ, CLAUDE_MODEL_ENV_VAR) or DEFAULT_CLAUDE_MODEL,
        credential=CredentialReference(environment_variable=ANTHROPIC_KEY_ENV_VAR),
        timeout_seconds=ANTHROPIC_TIMEOUT_SECONDS,
        retry_policy=CLOUD_RETRY_POLICY,
        max_output_tokens=_max_output_tokens(environ),
    )
    return AnthropicProvider(configuration)


def _build_speech_provider(
    gateway: SentinelTrustGateway, environ: Mapping[str, str]
) -> GuardianSpeechProvider | None:
    """Build a Sentinel-gated Kokoro speech provider, or None if unconfigured.

    Mirrors `_build_real_provider()`'s absent-credential handling: an absent
    or blank `JARVIS_KOKORO_MODEL_PATH` or `JARVIS_KOKORO_VOICES_PATH` means
    the capability is not available on this machine, not a startup failure -
    `GuardianRuntime.speak()` already returns the honest `not_connected`
    outcome for a None provider. A present-but-invalid path is a deliberate
    exception, not softened here (EIP-ESR0044-001 Section 8 item 2, carried
    over unchanged from Piper) - `KokoroProvider`'s own constructor already
    raises `RuntimeError` on an unloadable model.

    Reuses the caller's `gateway` instance rather than constructing a second
    one, so conversation, memory and speech all share one trust boundary and
    audit trail (matching how `memory_service` already reuses it).
    """

    model_path = environ.get(KOKORO_MODEL_PATH_ENV_VAR)
    voices_path = environ.get(KOKORO_VOICES_PATH_ENV_VAR)
    if not model_path or not voices_path:
        return None
    kokoro_provider = KokoroProvider(
        ProviderConfiguration(
            provider_name="kokoro",
            endpoint=model_path,
            metadata={
                "voices_path": voices_path,
                "voice": KOKORO_VOICE,
                "fallback_voice": KOKORO_FALLBACK_VOICE,
                "lang": KOKORO_LANG,
            },
        )
    )
    return SentinelGatedSpeechProvider(gateway=gateway, provider=kokoro_provider)


def _build_transcription_provider(
    gateway: SentinelTrustGateway, environ: Mapping[str, str]
) -> GuardianTranscriptionProvider | None:
    """Build a Sentinel-gated Whisper transcription provider, or None if unconfigured.

    Mirrors `_build_speech_provider()` exactly, for the opposite data
    direction: an absent or blank `JARVIS_WHISPER_MODEL_PATH` means speech
    input is not available on this machine, not a startup failure -
    `GuardianRuntime.transcribe()` already returns the honest
    `not_connected` outcome for a None provider. Per EIP-ESR0047-001
    Section 5.2, setting this variable is itself the deployment-level
    enablement act this capability is gated on.
    """

    model_path = environ.get(WHISPER_MODEL_PATH_ENV_VAR)
    if not model_path:
        return None
    whisper_provider = WhisperProvider(
        ProviderConfiguration(provider_name="whisper", endpoint=model_path)
    )
    return SentinelGatedTranscriptionProvider(gateway=gateway, provider=whisper_provider)


def _build_home_assistant_agent(environ: Mapping[str, str]) -> HomeAssistantStateQueryAgent | None:
    """Build the Home Assistant read-only state-query agent, or None if unconfigured.

    Mirrors `_build_speech_provider()`'s absent-credential handling: an
    absent or blank base URL or token means the capability is not
    available on this deployment, not a startup failure - it simply does
    not appear in `available_agents()`. No network call is made here;
    `HomeAssistantClient` only calls out when an actual query is executed.
    """

    base_url = environ.get(HOME_ASSISTANT_URL_ENV_VAR)
    token = environ.get(HOME_ASSISTANT_TOKEN_ENV_VAR)
    if not base_url or not token:
        return None
    return HomeAssistantStateQueryAgent(HomeAssistantClient(base_url=base_url, token=token))


def _memory_db_path(environ: Mapping[str, str]) -> Path:
    return Path(environ[MEMORY_DB_PATH_ENV_VAR]) if environ.get(MEMORY_DB_PATH_ENV_VAR) else DEFAULT_MEMORY_DB_PATH


def _log_dir(environ: Mapping[str, str]) -> Path:
    """Return the log directory - see LOG_DIR_ENV_VAR (EBG-0144)."""

    explicit = (environ.get(LOG_DIR_ENV_VAR) or "").strip()
    if explicit:
        return Path(explicit)
    return _memory_db_path(environ).parent.parent / "logs"


def _configure_backend_log_file(environ: Mapping[str, str]) -> Path:
    """Also write the backend's log records to a rotating file (EBG-0144,
    ESR-0059 WP9). The packaged sidecar's stderr is not captured by the
    Tauri host, so without this a release build kept no logs at all.
    stdout is never used - it carries the JSON-RPC stream."""

    log_path = _log_dir(environ) / BACKEND_LOG_FILENAME
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=BACKEND_LOG_MAX_BYTES, backupCount=BACKEND_LOG_BACKUP_COUNT, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    return log_path


def _turn_deadline_seconds(environ: Mapping[str, str]) -> float:
    """Return the configured per-turn deadline, or the default for any
    absent or unusable value (EBG-0139, ESR-0059 WP5)."""

    raw = (environ.get(TURN_DEADLINE_ENV_VAR) or "").strip()
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_TURN_DEADLINE_SECONDS
    # math.isfinite also rejects nan and inf - an infinite deadline would
    # silently remove the bound this setting exists to enforce.
    return value if math.isfinite(value) and value > 0 else DEFAULT_TURN_DEADLINE_SECONDS


def _positive_float(environ: Mapping[str, str], name: str, default: float) -> float:
    """A finite number above zero from the environment, or `default` for any
    absent or unusable value."""

    raw = (environ.get(name) or "").strip()
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if math.isfinite(value) and value > 0 else default


def _build_escalation_provider(
    environ: Mapping[str, str],
    gateway: SentinelTrustGateway,
    orchestrator: ProviderOrchestrator,
    audit_recorder: JsonAuditRecorder,
) -> MeteredCloudConversationProvider:
    """The metered provider for the cloud route. Only called when the Claude
    provider is registered, so the spend database exists only for people who
    set a key."""

    usd_per_gbp = _positive_float(environ, USD_PER_GBP_ENV_VAR, DEFAULT_USD_PER_GBP)
    cap_gbp = _positive_float(environ, CLAUDE_CAP_GBP_ENV_VAR, DEFAULT_CLAUDE_CAP_GBP)
    cap_micro = round(cap_gbp * usd_per_gbp * MICRO_DOLLARS_PER_DOLLAR)
    ledger = SpendLedger(_memory_db_path(environ).parent / SPEND_DB_FILENAME, cap_micro)
    inner = SentinelGatedConversationProvider(
        gateway=gateway,
        orchestrator=orchestrator,
        capability=CLOUD_TEXT_GENERATION_CAPABILITY,
        source="jarvis.escalation",
        turn_deadline_seconds=_turn_deadline_seconds(environ),
        intent="conversation.escalate",
    )
    return MeteredCloudConversationProvider(inner, ledger, audit_recorder, usd_per_gbp=usd_per_gbp)


def _warn_about_legacy_provider_settings(environ: Mapping[str, str]) -> None:
    """One logged warning when an old OpenAI/Gemini selector is still set.

    The value is configuration, never a credential, and is not logged; only the
    variable names are.
    """

    present = [name for name in LEGACY_PROVIDER_ENV_VARS if _clean_env(environ, name) is not None]
    if present:
        logger.warning(
            "%s is no longer used: Version 1.0 answers locally with Ollama and offers Claude only by confirmed escalation.",
            ", ".join(present),
        )


def build_default_runtime(environ: Mapping[str, str] | None = None) -> GuardianRuntime:
    """Build and start the production Guardian+Sentinel stack.

    Version 1.0 provider strategy (ADR-0023, ESR-0061 WP3a, EIP-ESR0061-003):
    the ordinary `text-generation` route holds the local Ollama provider only,
    so when Ollama fails the user gets `PROVIDER_UNAVAILABLE_RESPONSE`, marked
    `is_model_reply=False` - never a silent call to a cloud service (before
    this the route began with OpenAI and Gemini and failed over automatically;
    until ESR-0059 WP3, EBG-0141, a LocalEchoProvider ended it and echoed the
    user's own message back as Guardian's answer; `LocalEchoProvider` itself
    remains in `sentinel/` for tests and tooling). The Anthropic Claude provider
    is registered on its own `text-generation-cloud` route, and only when
    `ANTHROPIC_API_KEY` is present and non-blank; nothing in this function
    sends a request to it - WP3b's confirmed escalation does. OpenAI and Gemini
    are unregistered; their adapters and tests remain.

    Also wires Guardian's Voice faculty (EIP-ESR0044-001, EBG-0114; Kokoro
    replacing Piper as of EIP-ESR0053-002, EBG-0125) - a Sentinel-gated
    Kokoro speech provider (`bm_george` primary voice, `bf_isabella`
    automatic fallback) is constructed only when both `JARVIS_KOKORO_MODEL_PATH`
    and `JARVIS_KOKORO_VOICES_PATH` are present and non-blank; otherwise
    `GuardianRuntime.speak()` honestly reports `not_connected`, exactly like
    an absent OpenAI/Gemini credential already degrades the conversation
    path. No voice model is ever auto-downloaded.

    Voice Faculty Increment B (EIP-ESR0047-001, EBG-0117) mirrors this
    exactly for speech input: a Sentinel-gated Whisper transcription
    provider is constructed only when `JARVIS_WHISPER_MODEL_PATH` is present
    and non-blank; otherwise `GuardianRuntime.transcribe()` honestly reports
    `not_connected`. No Whisper model is ever auto-downloaded.

    `environ` defaults to `os.environ`. Tests must pass an explicit mapping
    (e.g. `{}`) rather than relying on the default, so test runs stay
    deterministic and never depend on - or accidentally exercise - real
    credentials that happen to be set on the host machine.
    """

    environ = os.environ if environ is None else environ

    # EBG-0144 (ESR-0059 WP9): one durable, rotating audit trail shared by the
    # gateway and the orchestrator, replacing in-memory recorders that lost
    # every decision on restart. Audit events carry decision outcomes,
    # provider names and status codes - never conversation or memory text.
    audit_recorder = JsonAuditRecorder(_log_dir(environ) / AUDIT_LOG_FILENAME)
    gateway = SentinelTrustGateway(policy_engine=TrustTierPolicy(), audit_recorder=audit_recorder)
    orchestrator = ProviderOrchestrator(audit_recorder=audit_recorder)

    _warn_about_legacy_provider_settings(environ)

    # ESR-0061 WP3a (EIP-ESR0061-003 6.1): the ordinary route holds Ollama only,
    # so a local failure never reaches a cloud service. Claude has its own
    # capability, used only by a confirmed escalation.
    ollama_model = _clean_env(environ, OLLAMA_MODEL_ENV_VAR) or DEFAULT_OLLAMA_MODEL
    ollama_configuration = ProviderConfiguration(
        provider_name="ollama",
        default_model=ollama_model,
        endpoint=_clean_env(environ, OLLAMA_ENDPOINT_ENV_VAR),
        timeout_seconds=OLLAMA_TIMEOUT_SECONDS,
        max_output_tokens=_max_output_tokens(environ),
    )
    # The model is chosen per request: the environment variable if set, else the
    # one saved from the app's model setup, else the default (ESR-0061 WP3c).
    model_choice = ModelChoice(
        _memory_db_path(environ).parent / OLLAMA_MODEL_CHOICE_FILENAME,
        default_model=DEFAULT_OLLAMA_MODEL,
        environment_model=_clean_env(environ, OLLAMA_MODEL_ENV_VAR),
        catalog_tags=[model.tag for model in OLLAMA_CATALOG],
    )
    ollama_provider = OllamaProvider(ollama_configuration, model_source=model_choice.current)
    orchestrator.register_provider(ollama_provider)
    orchestrator.register_route(ProviderRoute(capability=TEXT_GENERATION_CAPABILITY, providers=(ollama_provider.name,)))

    anthropic_provider = _build_anthropic_provider(environ)
    escalation_provider: MeteredCloudConversationProvider | None = None
    if anthropic_provider is not None:
        orchestrator.register_provider(anthropic_provider)
        orchestrator.register_route(
            ProviderRoute(capability=CLOUD_TEXT_GENERATION_CAPABILITY, providers=(anthropic_provider.name,))
        )
    conversation_provider = SentinelGatedConversationProvider(
        gateway=gateway,
        orchestrator=orchestrator,
        turn_deadline_seconds=_turn_deadline_seconds(environ),
    )

    memory_db_path = _memory_db_path(environ)
    memory_store = PersonalMemoryStore(memory_db_path)
    # Reuses the same gateway instance conversation requests are evaluated
    # against - one trust boundary, not two (EIP-ESR0027-001 Section 4).
    memory_service = PersonalMemoryService(gateway=gateway, store=memory_store)

    speech_provider = _build_speech_provider(gateway, environ)
    transcription_provider = _build_transcription_provider(gateway, environ)

    # Agent Framework Phase 3 (EIP-ESR0049-001): unlike speech/transcription,
    # the GIA observability agent has no external credential or model
    # dependency, so it is always registered, reusing the same shared
    # `gateway` every other capability above already shares - not a freshly
    # constructed one (MOD-0001's mandatory-shared-gateway requirement).
    agents: dict[str, SpecialistAgent] = {
        GiaObservabilityAgent.name: GiaObservabilityAgent(LocalResourceObserver()),
        # GIA Phase 3a (EIP-ESR0054-002): reuses the same shared `gateway`
        # instance every other capability above already shares, matching
        # `GiaObservabilityAgent`'s own precedent immediately above.
        GiaEngineeringAgent.name: GiaEngineeringAgent(EngineeringStateObserver()),
    }
    # EBG-0127 (ESR-0058 WP4): unlike the two GIA agents above, this one has
    # a genuine external dependency (a configured Home Assistant instance)
    # and is therefore optional, mirroring speech/transcription's own
    # absent-credential-means-invisible pattern rather than GIA's
    # always-registered one.
    home_assistant_agent = _build_home_assistant_agent(environ)
    if home_assistant_agent is not None:
        agents[home_assistant_agent.name] = home_assistant_agent

    agent_service = SentinelGatedAgentService(gateway=gateway, agents=agents)

    if anthropic_provider is not None:
        escalation_provider = _build_escalation_provider(environ, gateway, orchestrator, audit_recorder)

    ollama_endpoint = _clean_env(environ, OLLAMA_ENDPOINT_ENV_VAR) or OLLAMA_DEFAULT_ENDPOINT
    ollama_setup = OllamaSetup(
        endpoint=ollama_endpoint,
        choice=model_choice,
        pulls=PullManager(
            ollama_endpoint,
            OLLAMA_CATALOG,
            disk_free=lambda: read_hardware(environ).free_disk_bytes,
        ),
        environ=environ,
        hardware_reader=lambda: read_hardware(environ),
    )

    runtime = GuardianRuntime(
        conversation_provider=conversation_provider,
        memory_service=memory_service,
        speech_provider=speech_provider,
        transcription_provider=transcription_provider,
        agent_service=agent_service,
        escalation_provider=escalation_provider,
        ollama_setup=ollama_setup,
    )
    runtime.start()
    return runtime


class StdioRpcServer:
    """Minimal JSON-RPC 2.0 server dispatching Guardian/Sentinel calls over stdio."""

    def __init__(
        self,
        runtime: GuardianRuntime,
        gia_observer: LocalResourceObserver | None = None,
        gia_engineering_observer: EngineeringStateObserver | None = None,
        heartbeat_interval_seconds: float | None = None,
        identity_service: ProfileService | None = None,
        activity_tracker: ActivityTracker | None = None,
        escalation_offers: EscalationOffers | None = None,
    ) -> None:
        self._runtime = runtime
        # Confirmation tokens for escalating a question to Claude (ESR-0061
        # WP3b). Held in memory only; injectable so tests can control time.
        self._escalation_offers = escalation_offers if escalation_offers is not None else EscalationOffers()
        # Guardian Orb Phase 2 (EBG-0121, UAM-0001 Section 8.1): records
        # genuinely-dispatched RPC activity so the Orb/Active Clusters panel
        # can illuminate clusters as they are actually accessed. Injectable
        # (mirroring gia_observer/identity_service) so RPC-layer tests can
        # assert exact recorded activity from a deterministic instance.
        self._activity_tracker = activity_tracker if activity_tracker is not None else ActivityTracker()
        # Streaming Notifications MVP (EIP-ESR0031-002): shared between the
        # main loop's response writes (serve_forever) and the heartbeat
        # thread's notification writes (_heartbeat_loop) so the two can never
        # interleave partial JSON onto the same output line.
        self._write_lock = threading.Lock()
        # Set by serve_forever(); background work (a model download) reports
        # through it. None - as under handle_line() in tests - drops them.
        self._notification_stream: TextIO | None = None
        if heartbeat_interval_seconds is not None:
            self._heartbeat_interval_seconds = heartbeat_interval_seconds
        else:
            self._heartbeat_interval_seconds = float(
                os.environ.get(HEARTBEAT_INTERVAL_ENV_VAR, DEFAULT_HEARTBEAT_INTERVAL_SECONDS)
            )
        # GIA (EBG-0083) is deliberately not constructed from or dependent on
        # `runtime` - per ESR-0011 Section 10, it observes and publishes local
        # resource state independent of Guardian's own lifecycle. This is
        # method-level decoupling only; `gia.status` is still unreachable if
        # `build_default_runtime()` fails before this server is constructed
        # (see `run()`), a disclosed limitation, not fixed by this class.
        # `gia_observer` is injectable (defaulting to the real psutil-backed
        # observer) so RPC-layer tests can assert exact serialization from a
        # deterministic fake snapshot, per EIP-ESR0029-002 Section 4.6/5.5,
        # rather than depending on the actual host machine's live values.
        self._gia_observer = gia_observer or LocalResourceObserver()
        # GIA Phase 3a (EIP-ESR0054-002): identical decoupling/injection
        # rationale as `_gia_observer` immediately above - a distinct data
        # domain (git state, not psutil), so a separate observer instance
        # rather than folding into `GiaSnapshot`.
        self._gia_engineering_observer = gia_engineering_observer or EngineeringStateObserver()
        # Identity/profile storage (EIP-ESR0046-001) is likewise decoupled
        # from `runtime`/`build_default_runtime()`, mirroring the GIA
        # precedent immediately above: profile identity is local-device state
        # independent of Guardian's own conversation lifecycle, not a
        # capability `GuardianRuntime` itself needs to know about (Section 8
        # exclusion 1 - this package deliberately does not scope conversation
        # or memory by profile). `identity_service` is injectable so
        # RPC-layer tests never touch the real `~/.jarvis/identity/` store.
        if identity_service is not None:
            self._identity_service = identity_service
        else:
            identity_db_path = (
                Path(os.environ[IDENTITY_DB_PATH_ENV_VAR])
                if os.environ.get(IDENTITY_DB_PATH_ENV_VAR)
                else DEFAULT_IDENTITY_DB_PATH
            )
            self._identity_service = ProfileService(ProfileStore(identity_db_path))
        setup = self._runtime.ollama_setup
        if setup is not None:
            setup.pulls.set_notifier(self._emit_notification)
        self._methods = {
            "guardian.converse": self._guardian_converse,
            "guardian.escalation.offer": self._guardian_escalation_offer,
            "guardian.escalate": self._guardian_escalate,
            "provider.status": self._provider_status,
            "profile.setCloudMemory": self._profile_set_cloud_memory,
            "ollama.status": self._ollama_status,
            "ollama.recommendation": self._ollama_recommendation,
            "ollama.pull": self._ollama_pull,
            "ollama.pullStatus": self._ollama_pull_status,
            "ollama.cancelPull": self._ollama_cancel_pull,
            "ollama.useModel": self._ollama_use_model,
            "guardian.speak": self._guardian_speak,
            "guardian.transcribe": self._guardian_transcribe,
            "guardian.agent.list": self._guardian_agent_list,
            "guardian.agent.invoke": self._guardian_agent_invoke,
            "platform.status": self._platform_status,
            "knowledge.graph": self._knowledge_graph,
            "memory.propose": self._memory_propose,
            "memory.approve": self._memory_approve,
            "memory.deny": self._memory_deny,
            "memory.list": self._memory_list,
            "memory.status": self._memory_status,
            "memory.delete": self._memory_delete,
            "memory.backup": self._memory_backup,
            "memory.restore": self._memory_restore,
            "profile.list": self._profile_list,
            "profile.create": self._profile_create,
            "profile.select": self._profile_select,
            "profile.active": self._profile_active,
            "gia.status": self._gia_status,
            "gia.engineeringStatus": self._gia_engineering_status,
        }

    def _guardian_converse(self, params: dict[str, Any]) -> dict[str, Any]:
        message = params.get("message")
        if not isinstance(message, str):
            msg = "params.message must be a string."
            raise ClientFacingTypeError(msg)
        _require_max_length(message, MAX_MESSAGE_CHARS, "params.message")
        active = self._identity_service.active_profile()
        response = self._runtime.converse(
            message,
            active.id if active is not None else None,
            include_household=_sees_household_notes(active),
        )
        return {
            "message": response.message,
            "provider": response.provider,
            "escalation": self._escalation_offer(active, message, offer_reason(response, message)),
        }

    def _escalation_offer(self, active, message: str, reason: str | None) -> dict[str, Any]:
        """The offer to ask Claude about `message`, or "not offered".

        Offered only when there is a reason, Claude is configured, the active
        profile's role may use it and the month's cap has room. A profile that
        may not escalate is told nothing about it: no offer, no reason.
        """

        not_offered: dict[str, Any] = {"offered": False, "reason": None, "token": None}
        provider = self._runtime.escalation_provider
        if (
            reason is None
            or provider is None
            or not self._runtime.escalation_available
            or active is None
            or active.role not in ESCALATION_ROLES
        ):
            return not_offered
        snapshot = provider.ledger.snapshot()
        if snapshot.cap_reached:
            return not_offered
        return {
            "offered": True,
            "reason": reason,
            "token": self._escalation_offers.issue(active.id, message),
            "expiresInSeconds": int(self._escalation_offers.ttl_seconds),
            "model": provider.model,
            # What the confirmation must tell the person is being sent.
            "sendsMemory": active.share_memory_with_cloud,
            "allowance": allowance_payload(snapshot, provider.usd_per_gbp),
        }

    def _guardian_escalation_offer(self, params: dict[str, Any]) -> dict[str, Any]:
        """Ask Claude: an offer for a message the person chose, at any time."""

        message = params.get("message")
        if not isinstance(message, str):
            msg = "params.message must be a string."
            raise ClientFacingTypeError(msg)
        if not message.strip():
            msg = "params.message must not be blank."
            raise ClientFacingValueError(msg)
        _require_max_length(message, MAX_MESSAGE_CHARS, "params.message")
        active = self._identity_service.active_profile()
        _require_role(active, ESCALATION_ROLES, CLOUD_NOT_PERMITTED_MESSAGE)
        if not self._runtime.escalation_available:
            msg = "Asking Claude is not set up on this computer."
            raise ClientFacingValueError(msg)
        offer = self._escalation_offer(active, message, REASON_REQUESTED)
        if not offer["offered"]:
            msg = "The monthly allowance for asking Claude has been used up."
            raise ClientFacingValueError(msg)
        return offer

    def _guardian_escalate(self, params: dict[str, Any]) -> dict[str, Any]:
        """Send an offered question to Claude, after the person confirmed.

        First of the two role checks (EIP-ESR0061-003 6.8): the role is the
        server-held active profile's, never a parameter. The second is
        Sentinel's, on the cloud capability, inside the call.
        """

        token = params.get("token")
        if not isinstance(token, str):
            msg = "params.token must be a string."
            raise ClientFacingTypeError(msg)
        active = self._identity_service.active_profile()
        _require_role(active, ESCALATION_ROLES, CLOUD_NOT_PERMITTED_MESSAGE)
        message = self._escalation_offers.redeem(token, active.id)
        if message is None:
            msg = "This offer has expired or was already used. Ask again."
            raise ClientFacingValueError(msg)
        response = self._runtime.escalate(
            message,
            active.id,
            role=active.role,
            include_household=_sees_household_notes(active),
            share_memory=active.share_memory_with_cloud,
        )
        provider = self._runtime.escalation_provider
        return {
            "message": response.message,
            "provider": response.provider,
            "answeredBy": "claude" if response.is_model_reply else None,
            "failure": response.failure,
            "allowance": (
                allowance_payload(provider.ledger.snapshot(), provider.usd_per_gbp) if provider is not None else None
            ),
        }

    def _provider_status(self, params: dict[str, Any]) -> dict[str, Any]:
        active = self._identity_service.active_profile()
        provider = self._runtime.escalation_provider
        configured = self._runtime.escalation_available
        return {
            "claude": {
                "configured": configured,
                "model": provider.model if configured and provider is not None else None,
                "mayEscalate": active is not None and active.role in ESCALATION_ROLES,
                "allowance": (
                    allowance_payload(provider.ledger.snapshot(), provider.usd_per_gbp)
                    if configured and provider is not None
                    else None
                ),
            }
        }

    def _profile_set_cloud_memory(self, params: dict[str, Any]) -> dict[str, Any]:
        """Administrator only: whether a profile's retained memory notes may
        accompany a question escalated to Claude (EBG-0110)."""

        profile_id = params.get("profileId")
        enabled = params.get("enabled")
        if not isinstance(profile_id, str):
            msg = "params.profileId must be a string."
            raise ClientFacingTypeError(msg)
        if not isinstance(enabled, bool):
            msg = "params.enabled must be true or false."
            raise ClientFacingTypeError(msg)
        _require_role(
            self._identity_service.active_profile(),
            frozenset({"Administrator"}),
            "Only an Administrator profile can change whether memory is shared with Claude.",
        )
        return self._serialize_profile(self._identity_service.set_cloud_memory_sharing(profile_id, enabled))

    def _emit_notification(self, method: str, params: dict[str, Any]) -> None:
        """Send a JSON-RPC notification (no `id`) from a background thread."""

        stream = self._notification_stream
        if stream is None:
            return
        try:
            self._write_line(stream, {"jsonrpc": JSONRPC_VERSION, "method": method, "params": params})
        except (OSError, ValueError):
            logger.warning("Could not write a %s notification.", method)

    def _ollama(self) -> OllamaSetup:
        setup = self._runtime.ollama_setup
        if setup is None:
            msg = "Local model setup is not available."
            raise ClientFacingValueError(msg)
        return setup

    def _ollama_status(self, params: dict[str, Any]) -> dict[str, Any]:
        setup = self._ollama()
        return {**setup.status(), "pull": setup.pulls.snapshot()}

    def _ollama_recommendation(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._ollama().recommendation()

    def _require_model_tag(self, params: dict[str, Any]) -> str:
        model = params.get("model")
        if not isinstance(model, str):
            msg = "params.model must be a string."
            raise ClientFacingTypeError(msg)
        return model

    def _require_model_manager(self) -> None:
        _require_role(
            self._identity_service.active_profile(),
            MODEL_MANAGER_ROLES,
            "Only an Administrator or Adult profile can download or change the local model.",
        )

    def _ollama_pull(self, params: dict[str, Any]) -> dict[str, Any]:
        model = self._require_model_tag(params)
        self._require_model_manager()
        return self._ollama().pulls.start(model)

    def _ollama_pull_status(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._ollama().pulls.snapshot()

    def _ollama_cancel_pull(self, params: dict[str, Any]) -> dict[str, Any]:
        self._require_model_manager()
        return {"cancelled": self._ollama().pulls.cancel()}

    def _ollama_use_model(self, params: dict[str, Any]) -> dict[str, Any]:
        model = self._require_model_tag(params)
        self._require_model_manager()
        return self._ollama().use_model(model)

    def _guardian_speak(self, params: dict[str, Any]) -> dict[str, Any]:
        text = params.get("text")
        if not isinstance(text, str):
            msg = "params.text must be a string."
            raise ClientFacingTypeError(msg)
        _require_max_length(text, MAX_SPEAK_CHARS, "params.text")
        outcome = self._runtime.speak(text)
        result: dict[str, Any] = {"status": outcome.status, "message": outcome.message}
        if outcome.status == "synthesized":
            result["audio"] = base64.b64encode(outcome.audio.audio_bytes).decode("ascii")
            result["mimeType"] = outcome.audio.mime_type
        return result

    def _guardian_transcribe(self, params: dict[str, Any]) -> dict[str, Any]:
        audio_base64 = params.get("audioBase64")
        mime_type = params.get("mimeType")
        if not isinstance(audio_base64, str):
            msg = "params.audioBase64 must be a string."
            raise ClientFacingTypeError(msg)
        _require_max_length(audio_base64, MAX_AUDIO_BASE64_CHARS, "params.audioBase64")
        if not isinstance(mime_type, str):
            msg = "params.mimeType must be a string."
            raise ClientFacingTypeError(msg)
        try:
            audio_bytes = base64.b64decode(audio_base64, validate=True)
        except (ValueError, TypeError) as exc:
            msg = "params.audioBase64 must be valid base64."
            raise ClientFacingValueError(msg) from exc
        outcome = self._runtime.transcribe(audio_bytes, mime_type)
        return {"status": outcome.status, "text": outcome.text, "message": outcome.message}

    def _guardian_agent_list(self, params: dict[str, Any]) -> dict[str, Any]:
        return {"agents": list(self._runtime.available_agents())}

    def _guardian_agent_invoke(self, params: dict[str, Any]) -> dict[str, Any]:
        agent_name = params.get("agent")
        task = params.get("task")
        parameters = params.get("parameters", {})
        if not isinstance(agent_name, str):
            msg = "params.agent must be a string."
            raise ClientFacingTypeError(msg)
        if not isinstance(task, str):
            msg = "params.task must be a string."
            raise ClientFacingTypeError(msg)
        if not isinstance(parameters, dict):
            msg = "params.parameters must be an object."
            raise ClientFacingTypeError(msg)
        outcome = self._runtime.invoke_agent(agent_name, AgentRequest(task=task, parameters=parameters))
        result: dict[str, Any] = {"status": outcome.status, "message": outcome.message}
        if outcome.result is not None:
            result["payload"] = dict(outcome.result.payload)
        return result

    def _platform_status(self, params: dict[str, Any]) -> dict[str, Any]:
        snapshot = self._runtime.status_snapshot()
        provider_boundary = snapshot.services.get("Guardian Provider Boundary")
        memory_boundary = snapshot.services.get("Guardian Memory Boundary")
        gateway = self._runtime.sentinel_gateway()
        return {
            "state": snapshot.state.value,
            "runtimeHealth": snapshot.runtime_health.value,
            "providerConnected": provider_boundary.status.value if provider_boundary else "Unknown",
            "memoryConnected": memory_boundary.status.value if memory_boundary else "Unknown",
            "transcriptionAvailable": self._runtime.transcription_available,
            "providers": list(self._runtime.configured_providers()),
            "policyEngine": type(gateway.policy_engine).__name__ if gateway is not None else None,
        }

    def _knowledge_graph(self, params: dict[str, Any]) -> dict[str, Any]:
        graph = knowledge_graph.build_graph()
        # Guardian Orb Phase 2 (EBG-0121): the pull-interface half of cluster
        # illumination - real activity already observed by the time this is
        # fetched, so a session mounting mid-activity is not shown a falsely
        # idle Orb. The push-interface half is serve_forever's
        # knowledge.cluster_activity notification, below.
        graph["active_clusters"] = self._activity_tracker.recent_clusters()
        return graph

    def _gia_status(self, params: dict[str, Any]) -> dict[str, Any]:
        snapshot = self._gia_observer.snapshot()
        return {
            "cpuPercent": snapshot.cpu_percent,
            "memoryPercent": snapshot.memory_percent,
            "memoryUsedMb": snapshot.memory_used_mb,
            "memoryTotalMb": snapshot.memory_total_mb,
            "diskPercent": snapshot.disk_percent,
            "diskUsedGb": snapshot.disk_used_gb,
            "diskTotalGb": snapshot.disk_total_gb,
            "processStatus": snapshot.process_status,
            "processUptimeSeconds": snapshot.process_uptime_seconds,
            "processCpuPercent": snapshot.process_cpu_percent,
            "processMemoryMb": snapshot.process_memory_mb,
            "engineeringToolsRunning": dict(snapshot.engineering_tools_running),
            "capturedAt": snapshot.captured_at.isoformat(),
        }

    def _gia_engineering_status(self, params: dict[str, Any]) -> dict[str, Any]:
        snapshot = self._gia_engineering_observer.snapshot()
        return {
            "gitBranch": snapshot.git_branch,
            "gitUncommittedFiles": snapshot.git_uncommitted_files,
            "gitLastCommitSha": snapshot.git_last_commit_sha,
            "gitLastCommitMessage": snapshot.git_last_commit_message,
            "repositoryValidationErrors": snapshot.repository_validation_errors,
            "repositoryValidationWarnings": snapshot.repository_validation_warnings,
            "currentRepositoryBaseline": snapshot.current_repository_baseline,
            "latestRegisteredSession": snapshot.latest_registered_session,
            "latestRegisteredSessionStatus": snapshot.latest_registered_session_status,
            "capturedAt": snapshot.captured_at.isoformat(),
        }

    def _memory_propose(self, params: dict[str, Any]) -> dict[str, Any]:
        content = params.get("content")
        if not isinstance(content, str):
            msg = "params.content must be a string."
            raise ClientFacingTypeError(msg)
        if not content.strip():
            msg = "params.content must not be blank."
            raise ClientFacingValueError(msg)
        _require_max_length(content, MAX_MEMORY_CHARS, "params.content")
        # EBG-0132 (ESR-0059 WP13), Programme Sponsor's decision: a memory
        # always belongs to a profile, so saving one needs a selected profile.
        profile_id = self._active_profile_id()
        if profile_id is None:
            msg = "Select a profile before saving a memory."
            raise ClientFacingValueError(msg)
        pending = self._runtime.propose_memory(content, profile_id)
        return {"pendingId": pending.id, "content": pending.content}

    def _memory_approve(self, params: dict[str, Any]) -> dict[str, Any]:
        pending_id = self._require_pending_id(params)
        # EBG-0132 (ESR-0059 WP14), GAM-0001 Section 8.1: approving a memory
        # proposal satisfies a Sentinel REVIEW escalation, which only an
        # Administrator or Adult may do.
        _require_role(
            self._identity_service.active_profile(),
            REVIEW_APPROVER_ROLES,
            "Only an Administrator or Adult profile can approve saving a memory.",
        )
        record = self._runtime.approve_memory(pending_id)
        return {
            "id": record.id,
            "content": record.content,
            "createdAt": record.created_at.isoformat(),
            "consentDecisionId": record.consent_decision_id,
        }

    def _memory_deny(self, params: dict[str, Any]) -> dict[str, Any]:
        pending_id = self._require_pending_id(params)
        decision = self._runtime.deny_memory(pending_id)
        return {"decisionId": decision.id, "decision": decision.decision}

    def _memory_list(self, params: dict[str, Any]) -> dict[str, Any]:
        active = self._identity_service.active_profile()
        records = self._runtime.list_memory(
            active.id if active is not None else None, include_household=_sees_household_notes(active)
        )
        return {
            "records": [
                {
                    "id": record.id,
                    "content": record.content,
                    "createdAt": record.created_at.isoformat(),
                    "consentDecisionId": record.consent_decision_id,
                    # null marks a shared household note (EBG-0132).
                    "profileId": record.profile_id,
                }
                for record in records
            ]
        }

    def _memory_delete(self, params: dict[str, Any]) -> dict[str, Any]:
        """EBG-0145 (ESR-0059 WP10): revoke one retained memory by id. An
        unknown id is an error, not a silent success."""

        record_id = params.get("recordId")
        if not isinstance(record_id, str) or not record_id.strip():
            msg = "params.recordId must be a non-empty string."
            raise ClientFacingTypeError(msg)
        active = self._identity_service.active_profile()
        self._runtime.delete_memory(
            record_id,
            active.id if active is not None else None,
            is_administrator=active is not None and active.role == "Administrator",
        )
        return {"recordId": record_id, "deleted": True}

    def _memory_status(self, params: dict[str, Any]) -> dict[str, Any]:
        """EBG-0131 (Memory Management UXP Surface): a lightweight status
        query for the backup/restore panel - just the stored record count,
        never full record content, matching PersonalMemoryStore.count()'s
        own dedicated COUNT(*) query rather than reusing memory.list()."""

        active = self._identity_service.active_profile()
        count = self._runtime.memory_status(
            active.id if active is not None else None, include_household=_sees_household_notes(active)
        )
        return {"recordCount": count}

    def _memory_backup(self, params: dict[str, Any]) -> dict[str, Any]:
        """BRD-0001 (EBG-0023): write a full point-in-time Personal Memory
        backup file. `params.backupDir` may override the default backup
        location for this one call; otherwise `JARVIS_MEMORY_BACKUP_DIR`
        (or its own default) is used, read at call time so tests that set
        the environment variable per-case are respected without needing a
        constructor parameter."""

        backup_dir_param = params.get("backupDir")
        if backup_dir_param is not None and not isinstance(backup_dir_param, str):
            msg = "params.backupDir must be a string when provided."
            raise ClientFacingTypeError(msg)
        if backup_dir_param:
            backup_dir = Path(backup_dir_param)
        else:
            env_value = os.environ.get(MEMORY_BACKUP_DIR_ENV_VAR)
            backup_dir = Path(env_value) if env_value else DEFAULT_MEMORY_BACKUP_DIR
        # EBG-0132 (ESR-0059 WP14): a backup holds every profile's memories.
        _require_role(
            self._identity_service.active_profile(),
            ADMINISTRATOR_ROLES,
            "Only an Administrator profile can back up memory.",
        )
        path = self._runtime.backup_memory(backup_dir)
        return {"path": str(path)}

    def _memory_restore(self, params: dict[str, Any]) -> dict[str, Any]:
        """BRD-0001 (EBG-0023): restore Personal Memory from a backup file.
        `params.confirmOverwrite` defaults to False - restoring into a
        non-empty store without it raises, matching BRD-0001 Section 6's
        "never runs silently" requirement; the caller (UXP/human) must pass
        it explicitly True to proceed."""

        backup_path_param = params.get("backupPath")
        if not isinstance(backup_path_param, str):
            msg = "params.backupPath must be a string."
            raise ClientFacingTypeError(msg)
        confirm_overwrite = params.get("confirmOverwrite", False)
        if not isinstance(confirm_overwrite, bool):
            msg = "params.confirmOverwrite must be a boolean when provided."
            raise ClientFacingTypeError(msg)
        # EBG-0132 (ESR-0059 WP13): backups hold memories but not profiles,
        # so on another installation a restored memory's owner may not exist
        # and nobody could see it. Such memories go to the profile doing the
        # restore - kept private, never turned into shared household notes -
        # so a restore needs a selected profile, like saving a memory does.
        active_profile_id = self._active_profile_id()
        if active_profile_id is None:
            msg = "Select a profile before restoring memory."
            raise ClientFacingValueError(msg)
        # EBG-0132 (ESR-0059 WP14): a restore replaces every profile's memories.
        _require_role(
            self._identity_service.active_profile(),
            ADMINISTRATOR_ROLES,
            "Only an Administrator profile can restore memory.",
        )
        count = self._runtime.restore_memory(Path(backup_path_param), confirm_overwrite=confirm_overwrite)
        known_profile_ids = {profile.id for profile in self._identity_service.list_profiles()}
        reassigned = self._runtime.reassign_unknown_memory_owners(known_profile_ids, active_profile_id)
        return {"recordCount": count, "reassignedToActiveProfile": reassigned}

    def _active_profile_id(self) -> str | None:
        """The selected profile's id, or None (EBG-0132, ESR-0059 WP13)."""

        active = self._identity_service.active_profile()
        return active.id if active is not None else None

    @staticmethod
    def _require_pending_id(params: dict[str, Any]) -> str:
        pending_id = params.get("pendingId")
        if not isinstance(pending_id, str):
            msg = "params.pendingId must be a string."
            raise ClientFacingTypeError(msg)
        return pending_id

    @staticmethod
    def _serialize_profile(record) -> dict[str, Any]:
        return {
            "id": record.id,
            "displayName": record.display_name,
            "role": record.role,
            "createdAt": record.created_at.isoformat(),
            "shareMemoryWithCloud": record.share_memory_with_cloud,
        }

    def _profile_list(self, params: dict[str, Any]) -> dict[str, Any]:
        profiles = self._identity_service.list_profiles()
        return {"profiles": [self._serialize_profile(record) for record in profiles]}

    def _profile_create(self, params: dict[str, Any]) -> dict[str, Any]:
        display_name = params.get("displayName")
        role = params.get("role")
        if not isinstance(display_name, str):
            msg = "params.displayName must be a string."
            raise ClientFacingTypeError(msg)
        if not isinstance(role, str):
            msg = "params.role must be a string."
            raise ClientFacingTypeError(msg)
        record = self._identity_service.create_profile(display_name, role)
        return self._serialize_profile(record)

    def _profile_select(self, params: dict[str, Any]) -> dict[str, Any]:
        profile_id = params.get("profileId")
        if not isinstance(profile_id, str):
            msg = "params.profileId must be a string."
            raise ClientFacingTypeError(msg)
        record = self._identity_service.select_profile(profile_id)
        return self._serialize_profile(record)

    def _profile_active(self, params: dict[str, Any]) -> dict[str, Any]:
        record = self._identity_service.active_profile()
        return {"profile": self._serialize_profile(record) if record is not None else None}

    def handle_line(self, line: str) -> dict[str, Any] | None:
        """Handle one JSON-RPC 2.0 request line, returning the response object."""

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            return self._error(None, PARSE_ERROR, "Parse error: invalid JSON.")

        if not isinstance(request, dict):
            return self._error(None, INVALID_REQUEST, "Invalid request: expected a JSON object.")

        request_id = request.get("id")

        if request.get("jsonrpc") != JSONRPC_VERSION:
            return self._error(request_id, INVALID_REQUEST, 'Invalid request: jsonrpc must be "2.0".')

        method = request.get("method")
        params = request.get("params", {})

        if not isinstance(method, str) or not method:
            return self._error(request_id, INVALID_REQUEST, "Invalid request: method must be a non-empty string.")
        if not isinstance(params, dict):
            return self._error(request_id, INVALID_PARAMS, "Invalid params: expected a JSON object.")

        handler = self._methods.get(method)
        if handler is None:
            return self._error(request_id, METHOD_NOT_FOUND, f"Method not found: {method}.")

        try:
            result = handler(params)
        except ClientFacingError as exc:
            # Written for the person using JARVIS (the UI shows it); named by
            # its builtin type so the text the UI shows is unchanged.
            return self._error(request_id, INTERNAL_ERROR, f"{public_type_name(exc)}: {exc}")
        except Exception as exc:  # noqa: BLE001 - any handler failure must become a JSON-RPC error reply, not crash the loop
            # ESR-0061 WP2a (EBG-0157 item 2): any other message may carry
            # internal detail - or, if built from user data, conversation or
            # memory content - so the client gets only the type, and the local
            # log gets the type and where it was raised, never the message
            # (D23: no conversation or memory content in logs).
            logger.error("RPC method %s failed: %s at %s", method, type(exc).__name__, _raise_location(exc))
            return self._error(request_id, INTERNAL_ERROR, f"Guardian hit an internal error ({type(exc).__name__}).")

        # Guardian Orb Phase 2 (EBG-0121): only a successful dispatch counts as
        # genuine access to that cluster's capability - an errored or
        # malformed request never reaches this line.
        self._activity_tracker.record(method)

        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": {"code": code, "message": message}}

    def _write_line(self, out_stream: TextIO, payload: dict[str, Any]) -> None:
        """Write one JSON-RPC line to out_stream, holding the shared write lock only
        for the write itself - never across a sleep or other blocking operation."""

        with self._write_lock:
            out_stream.write(json.dumps(payload) + "\n")
            out_stream.flush()

    def _heartbeat_loop(self, out_stream: TextIO, stop_event: threading.Event) -> None:
        """Periodically emit a system.heartbeat JSON-RPC notification (no `id` key -
        the JSON-RPC 2.0 signal distinguishing a notification from a response) until
        stop_event is set. Runs as a daemon thread; does not hold the write lock
        while waiting between heartbeats."""

        while not stop_event.wait(self._heartbeat_interval_seconds):
            notification = {
                "jsonrpc": JSONRPC_VERSION,
                "method": "system.heartbeat",
                "params": {"timestamp": datetime.now(UTC).isoformat()},
            }
            self._write_line(out_stream, notification)

    def serve_forever(self, in_stream: TextIO | None = None, out_stream: TextIO | None = None) -> None:
        """Read one JSON-RPC request per line from in_stream, writing responses to
        out_stream, while a background thread periodically writes heartbeat
        notifications to the same stream (EIP-ESR0031-002)."""

        in_stream = in_stream if in_stream is not None else sys.stdin
        out_stream = out_stream if out_stream is not None else sys.stdout
        self._notification_stream = out_stream

        stop_heartbeat = threading.Event()
        heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(out_stream, stop_heartbeat),
            daemon=True,
            name="jarvis-heartbeat",
        )
        heartbeat_thread.start()

        # EBG-0139 (ESR-0059 WP5): a dedicated worker for SLOW_METHODS - see
        # that constant for why it is exactly one thread.
        slow_lane = ThreadPoolExecutor(max_workers=1, thread_name_prefix="jarvis-slow")

        try:
            for raw_line in in_stream:
                line = raw_line.strip()
                if not line:
                    continue
                if _request_method(line) in SLOW_METHODS:
                    slow_lane.submit(self._process_line_logged, line, out_stream)
                else:
                    self._process_line_guarded(line, out_stream)
        finally:
            # stdin closed: let any in-flight or queued slow request finish
            # and write its response before the heartbeat stops and run()
            # stops the runtime - a request accepted is always answered.
            slow_lane.shutdown(wait=True)
            stop_heartbeat.set()

    def _process_line(self, line: str, out_stream: TextIO) -> None:
        """Handle one request line and write its response, then any activity
        notifications recorded since - on whichever thread runs it."""

        response = self.handle_line(line)
        if response is not None:
            self._write_line(out_stream, response)
        # Guardian Orb Phase 2 (EBG-0121): emit one
        # knowledge.cluster_activity notification per genuinely
        # recorded dispatch since the last drain - after the response
        # write, mirroring _heartbeat_loop's own no-`id`-key notification
        # shape and using the same _write_line/lock. ActivityTracker
        # guards its own state, so draining from either thread is safe.
        for method, cluster in self._activity_tracker.pop_pending():
            self._write_line(
                out_stream,
                {
                    "jsonrpc": JSONRPC_VERSION,
                    "method": "knowledge.cluster_activity",
                    "params": {
                        "cluster": cluster,
                        "method": method,
                        "timestamp": datetime.now(UTC).isoformat(),
                    },
                },
            )

    def _process_line_guarded(self, line: str, out_stream: TextIO) -> None:
        """`_process_line()` for the fast lane (ESR-0061 WP2a, EBG-0157 item
        3). A failure to produce or write a reply is logged and the loop goes
        on, as on the slow lane - except broken output (`OSError` from the
        write, such as a closed pipe), which is re-raised to end the loop:
        no reply could ever be delivered, so continuing would only fail again
        on every line."""

        try:
            self._process_line(line, out_stream)
        except OSError:
            raise
        except Exception:
            logger.exception("Fast-lane request could not be completed.")

    def _process_line_logged(self, line: str, out_stream: TextIO) -> None:
        """`_process_line()` for the slow-lane worker. handle_line() already
        turns every handler failure into a JSON-RPC error reply; this only
        catches a failure to *write* (for example a closed stdout), which
        would otherwise vanish silently inside the executor's future."""

        try:
            self._process_line(line, out_stream)
        except Exception:  # must not vanish silently inside an executor thread
            logger.exception("Slow-lane request could not be completed.")


# GAM-0001 Section 8.1 household roles, enforced at the RPC boundary where
# the active profile is known (EBG-0132, ESR-0059 WP14). Profiles are
# unauthenticated, so these rules separate cooperating household members;
# they are not a defence against someone selecting another profile.
ADMINISTRATOR_ROLES = frozenset({"Administrator"})
REVIEW_APPROVER_ROLES = frozenset({"Administrator", "Adult"})


def _raise_location(exc: BaseException) -> str:
    """Where an exception was raised, as `file:line in function` frames -
    enough to find the fault without logging its message."""

    frames = traceback.extract_tb(exc.__traceback__)[-3:]
    return " <- ".join(f"{Path(frame.filename).name}:{frame.lineno} in {frame.name}" for frame in reversed(frames))


def _require_role(active, allowed: frozenset[str], message: str) -> None:
    if active is None:
        msg = "Select a profile first."
        raise ClientFacingPermissionError(msg)
    if active.role not in allowed:
        raise ClientFacingPermissionError(message)


def _sees_household_notes(active) -> bool:
    """A Guest has no access to family-shared memory (GAM-0001 Section 8.1)."""

    return active is None or active.role != "Guest"


def _require_max_length(value: str, limit: int, name: str) -> None:
    """Refuse oversized RPC input (EBG-0143, ESR-0059 WP8)."""

    if len(value) > limit:
        msg = f"{name} is too long ({len(value)} characters; the limit is {limit})."
        raise ClientFacingValueError(msg)


def _max_output_tokens(environ: Mapping[str, str]) -> int | None:
    """Return the configured output-token cap, or None (uncapped) for any
    absent or unusable value (EBG-0143, ESR-0059 WP8)."""

    raw = (environ.get(MAX_OUTPUT_TOKENS_ENV_VAR) or "").strip()
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def _request_method(line: str) -> str | None:
    """Return a request line's `method`, or None if it cannot be read -
    malformed lines take the normal inline path, where handle_line() turns
    them into the proper JSON-RPC error reply."""

    try:
        request = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(request, dict):
        return None
    method = request.get("method")
    return method if isinstance(method, str) else None


def run() -> None:
    """Entry point: build the default runtime and serve JSON-RPC over stdio until stdin closes."""

    log_path = _configure_backend_log_file(os.environ)
    logger.info("JARVIS backend starting; logging to %s.", log_path)
    start_orphan_watchdog()
    try:
        runtime = build_default_runtime()
        server = StdioRpcServer(runtime)
    except Exception:
        # Before WP9 a startup failure in the packaged app vanished with the
        # sidecar's discarded stderr (EBG-0144).
        logger.exception("JARVIS backend failed to start.")
        raise
    try:
        server.serve_forever()
    except Exception:
        logger.exception("JARVIS backend stopped on an unhandled error.")
        raise
    finally:
        runtime.stop()
        logger.info("JARVIS backend stopped.")
