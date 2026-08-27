# RBL-0033 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0033 |
| Title | ESR-0053 Repository Baseline (Active Backlog View Generation; Kokoro Production Voice Wiring) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0053_ENGINEERING_SESSION_REPORT|ESR-0053]] |
| Previous Baseline | [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 27 August 2026 |
| HEAD at baseline creation | `1db5547` |

---

# 2. Purpose

RBL-0033 records the repository baseline accepted by the Programme Sponsor at ESR-0053 WP7, superseding [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]]. ESR-0053 opened at the Programme Sponsor's direct request following ESR-0052's formal closure. It ran two Work Packages: WP1 (resolved EBG-0106 - retired EBR-0001 Section 5A's hand-maintained, theme-grouped "Active Backlog View" snapshot, which had drifted stale twice, most recently still listing EBG-0115/EBG-0111 as open after ESR-0052 resolved both, in favour of a view generated on demand directly from Section 5's own Status/Priority columns) and WP2 (resolved EBG-0125, Kokoro Production Voice Wiring - a genuine, live product-capability change). Guardian's actual production speech-synthesis provider changed from Piper to Kokoro (`bm_george` primary voice, `bf_isabella` automatic runtime fallback), following a real live listening comparison the Programme Sponsor personally judged.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session for WP2's Guardian voice-provider delivery, flagged as a documentation-staleness item for a future session's Documentation Debt sync, matching the same disclosed pattern prior baselines have carried forward. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0053 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation, including a Documentation-Debt Priority check (PBK-0001) that found EBR-0001 Section 5A live-stale - a second instance of the exact drift EBG-0106 was registered to fix. The Programme Sponsor selected clearing EBG-0106 as WP1, ahead of new capability work.

**WP1 design review (Codex, `codex exec -s workspace-write`)**: [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] v0.1 reviewed Conditional Pass with corrections (a backward-compatibility overclaim, and validation wording that didn't distinguish unchanged behaviour from necessarily-changed test wiring) - both folded into v0.2.

**WP2 design review**: [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]] v0.1 reviewed Conditional Pass with correction (EBG-0125's own register row still read "no implementation, provider selection or voice choice is authorised," stale relative to the Programme Sponsor's actual decision) - folded into v0.2 with a dated authorisation note.

**Pre-implementation approval gates**: Programme Sponsor approval-to-implement obtained and verified via `submit-response` directly against the real Sponsor Approval Service for both WP1 and WP2, before any code was written.

**WP1 post-commit review**: genuine independent Codex review of the real committed diff (`b46c296..274a6b9`) - **Pass, no findings**. Confirmed exactly the six expected files changed, `pytest`/`validate_repository.py` matching, EBG-0106 genuinely `Completed`, Section 5A genuinely no longer a static table.

**WP2 post-commit review**: genuine independent Codex review of the real committed diff (`248924a..061c914`) - **Pass, no findings**. Confirmed exactly the nine expected files changed, no unexpected `src/`/`src-tauri/` path; independently read the fallback logic and the Piper-to-Kokoro production substitution directly against source rather than trusting the commit message; confirmed `sentinel/piper_provider.py` untouched.

**Session-wide WP6 Independent Repository Verification**: covering the full session range `b46c296..HEAD` (WP1 and WP2 combined, 4 commits, `b46c296` independently self-confirmed by Codex as ESR-0052's own final closure commit before reviewing - learning directly from ESR-0052 WP6's own diff-boundary mistake). **Pass, no findings** - confirmed exactly the expected 12 changed paths, no scope creep; `sentinel/piper_provider.py`, `sentinel/policy.py` and `GAM-0001` byte-identical/untouched across the whole session; every governance "Completed" claim backed by real evidence; REG-0001/EBR-0001/ESR-0053 version-history entries internally consistent with the actual diff. Codex's own advisory assessment: Establish - WP2 is a genuine live product-capability change.

**Push approval**: Programme Sponsor approval-to-implement gates verified via `submit-response` against the real Sponsor Approval Service for both Work Packages before implementation began; commits and pushes proceeded under that same authorisation.

**The Programme Sponsor's determination**: **establish a new baseline**, since WP2 delivered a genuine, live product-capability change - Guardian's actual production speech-synthesis provider changed from Piper to Kokoro, live-verified against the real engine (both the primary voice and a genuine automatic-fallback trigger) - matching the same threshold applied at RBL-0025/RBL-0027/RBL-0028/RBL-0029/RBL-0030/RBL-0031/RBL-0032 rather than the Retain threshold applied at process/tooling-only sessions such as ESR-0052.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `scripts/session_launcher.py` | `read_high_priority_backlog()` refactored into `read_open_backlog(ebr_path, priority=None)` with a backward-compatible wrapper; new `generate_active_backlog_view()` groups open items by Priority; `read_active_backlog_snapshot()`/`ActiveBacklogItem` removed. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] Section 5A | Retired hand-maintained theme-grouped snapshot; replaced with a pointer to the on-demand generator. EBG-0106 and EBG-0125 both marked `Completed`. |
| `sentinel/kokoro_provider.py` | Dual-voice automatic-fallback support - `VoiceSynthesizer` seam changed to `(text, voice)`-parameterised; new optional `fallback_voice` metadata key; `synthesize()` retries once on primary-voice failure. |
| `jarvis/interfaces/stdio_rpc.py` | `_build_speech_provider()` constructs `KokoroProvider` (`bm_george` primary, `bf_isabella` fallback, `en-gb`) instead of `PiperProvider`, gated on `JARVIS_KOKORO_MODEL_PATH`/`JARVIS_KOKORO_VOICES_PATH`. |
| `pyproject.toml` | `kokoro-onnx`/`espeakng-loader`/`phonemizer-fork` promoted from the (now-removed) `voice-eval` optional group to base `dependencies`. |
| `jarvis/tests/test_kokoro_provider.py`, `test_stdio_rpc.py`; `scripts/tests/test_session_launcher.py` | Seam/wiring tests updated; 7 new tests added across both Work Packages. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session for WP2's Guardian voice-provider delivery - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync.

---

# 7. Architecture Outcomes

- Guardian's production speech-synthesis provider changes from Piper to Kokoro for the first time - a real, live-verified behaviour change, not merely a new adapter's existence (Kokoro has existed as a tested, unregistered adapter since ESR-0052).
- EBR-0001's own Active Backlog View mechanism moves from a hand-maintained, twice-stale-drifted snapshot to a mechanically generated, on-demand view - directly resolving EBG-0106's own diagnosis of the second-source-of-truth problem.
- `sentinel/piper_provider.py`, `sentinel/policy.py` and `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remain completely untouched throughout this session.
- No change to `src/`/`src-tauri/` - `guardian.speak`'s UXP call site was already provider-agnostic, confirmed by direct search rather than assumed.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- Kokoro's voice/fallback-voice/language selection (`bm_george`/`bf_isabella`/`en-gb`) is hardcoded in `jarvis/interfaces/stdio_rpc.py`, not env-var-configurable - a disclosed simplification, not a completed configurability feature;
- `sentinel/piper_provider.py` remains fully intact and testable - unregistered from production, not removed; `piper-tts` remains a base dependency unchanged;
- EBR-0001 Section 5A's retired Theme grouping is not reproduced by the new generator - Section 5 carries no `Theme` column; only Priority grouping is generated;
- no change to `sentinel/provider_config.py`'s `ProviderConfigurationRegistry`/text-generation route machinery - speech continues to use the single-provider-plus-gateway pattern it always has;
- no change to the Whisper/transcription (speech-input) path.

---

# 9. Verification

Repository validation performed across ESR-0053's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`b46c296..HEAD`, 4 commits) pushed to `origin/main`.
- 537 Python tests passing plus 1 correctly-skipped test - up from 530/1 at RBL-0032 (7 new tests: 2 net new in `test_session_launcher.py`, 4 fallback-behaviour tests in `test_kokoro_provider.py`, 1 both-paths-required test in `test_stdio_rpc.py`).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout, 298 warnings (unchanged, all pre-existing).
- WP1 design review (Codex): v0.1 Conditional Pass with corrections, both folded into v0.2.
- WP2 design review (Codex): v0.1 Conditional Pass with correction, folded into v0.2.
- WP1 post-commit review (Codex): Pass, no findings.
- WP2 post-commit review (Codex): Pass, no findings.
- Session-wide WP6 (Codex): Pass, no findings, covering the full session diff against RBL-0032.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`) - approval-to-implement verified for real before implementation began on both Work Packages, including a genuine drift-refusal-and-retry on one recording-only commit where the Sponsor's chat "Approved" had not yet been backed by a fresh real service decision.
- Live end-to-end verification against the real Kokoro engine, not fake test seams: a genuine `build_default_runtime()` + `runtime.speak()` call returned synthesized `bm_george` audio; a second real call with a deliberately invalid primary voice confirmed the automatic fallback genuinely engages, producing genuine `bf_isabella` audio. Model files never committed, deleted after each use.
- The Programme Sponsor's own live listening comparison verdict (four genuine `.wav` files, all four Kokoro UK voices) directly selected the production voice/fallback choice.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0032 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh for this session's Kokoro production-voice delivery - not yet reflected there.
5. Env-var-configurable voice/fallback-voice/language selection for Kokoro, if per-deployment configurability is wanted (deliberately out of this session's scope).
6. If a Theme-grouped view is wanted again for EBR-0001's Active Backlog View, a `Theme` column would need adding to Section 5 itself and maintaining alongside Status/Priority - a separate future backlog item.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0053_ENGINEERING_SESSION_REPORT|ESR-0053]] | Session this baseline is drawn from. |
| [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] | Approved Engineering Implementation Package WP1's deliverables were built against. |
| [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] | Built and tested the `KokoroProvider` adapter WP2 wired into production. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0106 and EBG-0125 both closed this session. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 27 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0032, following Codex design reviews (WP1 v0.1 Conditional Pass with corrections; WP2 v0.1 Conditional Pass with correction, both folded in before implementation), verified pre-implementation approval gates, post-commit Codex reviews (both Pass, no findings), session-wide WP6 Independent Repository Verification (Pass, no findings), and the Programme Sponsor's explicit WP7 decision to cut a new baseline: WP2's real, live-verified Kokoro production-voice delivery warrants a new baseline. |
