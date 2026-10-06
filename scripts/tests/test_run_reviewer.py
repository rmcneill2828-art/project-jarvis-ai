"""Tests for scripts/run_reviewer.py (ESR-0061 WP1c, R8)."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime

import pytest

from scripts import run_reviewer

ALLOWED = [
    "git log --oneline -1",
    "git show --stat 23e95bd",
    "git diff e153874 1978070 -- aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md",
    'git show 1978070:aiems/x.md | grep "REG-0001 | Register"',
    'git grep -n -i "current accepted repository baseline" -- "*.md" | grep -v -E "PST-0001|History" | wc -l',
    "git ls-files src/ jarvis/",
    'cat aiems/x.md | grep -A 10 "6.6 JRM"',
    'grep -n "JRM" aiems/governance/reviews/x.md',
    "head -n 20 scripts/run_reviewer.py",
    "wc -l scripts/run_reviewer.py",
    "python -m pytest -q",
    "python -m pytest -q scripts/tests",
    "python -m ruff check scripts",
    "python scripts/validate_repository.py",
    'python scripts/aiems_bridge.py return-findings ESR-0061 WP1c --message "Pass. No findings."',
]

REFUSED = [
    "git clean -fdx",
    "git reset --hard",
    "git add .",
    "git commit -m x",
    "git push",
    "git branch evil",
    "git checkout main",
    "git diff --output x.patch a b",
    "git log --output=x",
    "git grep -Ovim x",
    "git grep -O vim x",
    "python -m ruff check --fix",
    "python -m ruff check . --fix",
    "python -m pytest --junitxml x.xml",
    "python -m pytest -p evil",
    'python -c "print(1)"',
    "cat a.md > b.md",
    "git log; rm x",
    "git log && rm x",
    "grep x a | sh",
    "git show x | wc -l | sh",
    'python scripts/aiems_bridge.py return-findings ESR-0061 WP1c --message "ok"; rm x',
    "python scripts/aiems_bridge.py submit-response ESR-0061 WP1c --message x",
    "rm -rf scripts",
]


@pytest.fixture(scope="module")
def rules():
    return run_reviewer.load_allowlist()


@pytest.mark.parametrize("command", ALLOWED)
def test_allowlist_permits_read_only_review_commands(rules, command):
    assert run_reviewer.command_allowed(rules, command)


@pytest.mark.parametrize("command", REFUSED)
def test_allowlist_refuses_writing_pushing_or_arbitrary_code(rules, command):
    assert not run_reviewer.command_allowed(rules, command)


def test_allowlist_has_no_deny_rules_and_scopes_reads_to_the_repository(rules):
    data = json.loads(run_reviewer.ALLOWLIST_PATH.read_text(encoding="utf-8"))
    assert set(data["permissions"]) == {"allow"}
    assert [r for r in rules if r.startswith("read_file(")] == [f"read_file({run_reviewer.REPO_ROOT.as_posix()})"]


def test_launcher_instruction_is_shell_safe():
    path = run_reviewer.REVIEWS_DIR / "ESR-0061-WP1c-20261006T100000Z-prompt.md"
    instruction = run_reviewer.launcher_instruction(path)
    assert not set(instruction) & set("\"'`$;&|<>%^")
    assert ".aiems-exchange/reviews/ESR-0061-WP1c-20261006T100000Z-prompt.md" in instruction


def test_build_command_for_antigravity_uses_a_gemini_model_never_claude():
    command = run_reviewer.build_command("antigravity", "Read the file x", None)
    model = command[command.index("--model") + 1]
    assert model.startswith("gemini-") and "claude" not in model
    assert "-c" not in command


def test_build_command_resume_continues_the_conversation():
    assert run_reviewer.build_command("antigravity", "Read the file x", "carry on")[:2] == ["agy", "-c"]


def test_build_command_for_copilot_is_narrowly_scoped():
    command = run_reviewer.build_command("copilot", "Read the file x", None)
    allowed = [command[i + 1] for i, part in enumerate(command) if part == "--allow-tool"]
    assert "shell(git:*)" not in allowed and "shell(python:*)" not in allowed
    assert command[-2:] == ["--deny-tool", "write"]


def test_compose_prompt_appends_tool_rules_and_the_verdict_command():
    text = run_reviewer.compose_prompt("antigravity", "ESR-0061", "WP1c", "Review this.")
    assert text.startswith("Review this.")
    assert "Never: python -c" in text
    assert "return-findings ESR-0061 WP1c" in text


def _patch_run(monkeypatch, tmp_path, output: str, transcript: str | None = None):
    monkeypatch.setattr(run_reviewer, "REVIEWS_DIR", tmp_path / ".aiems-exchange/reviews")
    monkeypatch.setattr(run_reviewer, "TRANSCRIPT_DIR", tmp_path / ".aiems-exchange/transcript")
    monkeypatch.setattr(run_reviewer, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(run_reviewer, "ANTIGRAVITY_BRAIN", tmp_path / "brain")
    monkeypatch.setattr(run_reviewer.shutil, "which", lambda name: f"/bin/{name}")
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if transcript is not None:
            tdir = tmp_path / ".aiems-exchange/transcript"
            tdir.mkdir(parents=True, exist_ok=True)
            (tdir / "ESR-0061-WP1c.md").write_text(transcript, encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

    monkeypatch.setattr(run_reviewer.subprocess, "run", fake_run)
    return calls


def _reviewer_block(verdict: str) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"\n===\nsession: ESR-0061\nsender: reviewer\ntimestamp: {now}\n---\n{verdict}\n"


def test_run_review_reports_a_recorded_verdict(monkeypatch, tmp_path):
    calls = _patch_run(monkeypatch, tmp_path, "done", transcript=_reviewer_block("Verdict: Pass."))
    assert run_reviewer.run_review("antigravity", "ESR-0061", "WP1c", "Review.", None) == run_reviewer.EXIT_OK
    command, kwargs = calls[0]
    assert kwargs["stdin"] is subprocess.DEVNULL and "shell" not in kwargs
    assert "Review." not in " ".join(command)  # the prompt travels in a file, not on the command line


def test_run_review_detects_copilot_quota(monkeypatch, tmp_path):
    _patch_run(monkeypatch, tmp_path, "You have exceeded your monthly quota (Request ID: x)")
    assert run_reviewer.run_review("copilot", "ESR-0061", "WP1c", "Review.", None) == run_reviewer.EXIT_QUOTA


def test_run_review_detects_an_antigravity_refusal_and_names_the_command(monkeypatch, tmp_path, capsys):
    _patch_run(monkeypatch, tmp_path, 'jetski: no output produced - ... so it was auto-denied.')
    log = tmp_path / "brain/conv1/.system_generated/logs/transcript.jsonl"
    log.parent.mkdir(parents=True)
    error = 'permission check failed for command "git grep x | wc -l": user denied permission'
    log.write_text(json.dumps({"step_index": 3, "status": "ERROR", "error": error}) + "\n", encoding="utf-8")

    assert run_reviewer.run_review("antigravity", "ESR-0061", "WP1c", "Review.", None) == run_reviewer.EXIT_REFUSED
    assert "git grep x | wc -l" in capsys.readouterr().out


def test_run_review_reports_a_missing_verdict(monkeypatch, tmp_path):
    _patch_run(monkeypatch, tmp_path, "I reviewed it.")
    assert run_reviewer.run_review("antigravity", "ESR-0061", "WP1c", "Review.", None) == run_reviewer.EXIT_NO_VERDICT


def test_reviewer_entries_ignore_entries_older_than_the_run(monkeypatch, tmp_path):
    monkeypatch.setattr(run_reviewer, "TRANSCRIPT_DIR", tmp_path)
    (tmp_path / "ESR-0061-WP1c.md").write_text(
        "\n===\nsender: reviewer\ntimestamp: 2026-10-06T08:00:00Z\n---\nOld verdict.\n", encoding="utf-8"
    )
    since = datetime(2026, 10, 6, 9, 0, tzinfo=UTC)
    assert run_reviewer.reviewer_entries_since("ESR-0061", "WP1c", since) == []


def test_install_settings_merges_without_removing_or_denying(monkeypatch, tmp_path):
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"theme": "dark", "permissions": {"allow": ["mcp(x/*)"]}}), encoding="utf-8")
    monkeypatch.setattr(run_reviewer, "ANTIGRAVITY_SETTINGS", settings)

    added = run_reviewer.install_settings()

    data = json.loads(settings.read_text(encoding="utf-8"))
    assert data["theme"] == "dark" and "mcp(x/*)" in data["permissions"]["allow"]
    assert "deny" not in data["permissions"]
    assert added == len(run_reviewer.load_allowlist())
    assert run_reviewer.check_settings() == []
