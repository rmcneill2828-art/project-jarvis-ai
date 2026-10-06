"""Tests for scripts/local_prescreen.py (ESR-0061 WP1c, D29)."""

from __future__ import annotations

import urllib.error

from scripts import local_prescreen as lp


def test_skips_cleanly_when_lm_studio_is_not_running(monkeypatch, capsys):
    def refuse(url, timeout):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(lp, "_get_json", refuse)

    assert lp.main([]) == 0
    out = capsys.readouterr().out
    assert lp.HEADER in out and "skipped" in out


def test_find_model_picks_the_gpt_oss_model(monkeypatch):
    monkeypatch.setattr(
        lp, "_get_json", lambda url, timeout: {"data": [{"id": "qwen2.5-7b-instruct"}, {"id": "openai/gpt-oss-20b"}]}
    )
    assert lp.find_model(None) == "openai/gpt-oss-20b"
    assert lp.find_model("qwen2.5-7b-instruct") == "qwen2.5-7b-instruct"
    assert lp.find_model("not-served") is None


def test_truncate_marks_a_long_diff():
    text, truncated = lp.truncate("x" * 50, limit=10)
    assert truncated and text.startswith("x" * 10) and "truncated" in text
    assert lp.truncate("short", limit=10) == ("short", False)


def test_report_is_headed_advisory_and_saved_outside_the_transcript(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(lp, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(lp, "OUTPUT_DIR", tmp_path / ".aiems-exchange/prescreen")
    monkeypatch.setattr(lp, "find_model", lambda explicit: "openai/gpt-oss-20b")
    monkeypatch.setattr(lp, "get_diff", lambda base, head: "diff --git a/x b/x\n+bug\n")
    monkeypatch.setattr(lp, "ask", lambda model, diff: "1. Medium - x:1 - a finding")

    assert lp.main([]) == 0

    saved = list((tmp_path / ".aiems-exchange/prescreen").glob("prescreen-*.md"))
    assert len(saved) == 1
    text = saved[0].read_text(encoding="utf-8")
    assert text.startswith(f"# {lp.HEADER}") and "Never counted as independent review" in text
    assert not (tmp_path / ".aiems-exchange/transcript").exists()


def test_a_failed_model_call_is_a_skip_not_a_failure(monkeypatch, capsys):
    monkeypatch.setattr(lp, "find_model", lambda explicit: "openai/gpt-oss-20b")
    monkeypatch.setattr(lp, "get_diff", lambda base, head: "diff --git a/x b/x\n+x\n")

    def boom(model, diff):
        raise urllib.error.URLError("timed out")

    monkeypatch.setattr(lp, "ask", boom)

    assert lp.main([]) == 0
    assert "did not answer" in capsys.readouterr().out
