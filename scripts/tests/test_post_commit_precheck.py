"""Tests for scripts/post_commit_precheck.py (ESR-0061 WP1c, R8)."""

from __future__ import annotations

from scripts import post_commit_precheck as pc

EIP_TEXT = """\
## 7.3 Evidence Pack

`scripts/not_this.py` is mentioned here.

## 7.4 Commit Contents (expected)

New: `scripts/run_reviewer.py`, `scripts/tests/test_run_reviewer.py`. Changed: `scripts/validate_repository.py`
and `aiems/governance/reviews/EIP-ESR0061-001_X.md`.

## 8. Validation
`scripts/also_not_this.py`
"""


def test_eip_commit_contents_reads_only_the_named_block():
    assert pc.eip_commit_contents(EIP_TEXT, "## 7.4 Commit Contents") == {
        "scripts/run_reviewer.py",
        "scripts/tests/test_run_reviewer.py",
        "scripts/validate_repository.py",
        "aiems/governance/reviews/EIP-ESR0061-001_X.md",
    }


def _block(*body: str) -> str:
    return chr(10).join(["## 8. Commit Contents", "", *body, ""])


def test_eip_commit_contents_reads_lock_and_script_files():
    text = _block("`src-tauri/Cargo.lock`, `scripts/setup.sh`")
    assert pc.eip_commit_contents(text, "## 8. Commit Contents") == {"src-tauri/Cargo.lock", "scripts/setup.sh"}


def test_eip_commit_contents_stops_at_a_not_changed_paragraph():
    text = _block("Changed: `a.py`.", "", "Not changed (listed by the design): `src/lib.rs`.", "", "## 9. Next")
    assert pc.eip_commit_contents(text, "## 8. Commit Contents") == {"a.py"}


def test_eip_commit_contents_reads_a_block_with_no_not_changed_paragraph_whole():
    text = _block("`a.py`", "`b.py`")
    assert pc.eip_commit_contents(text, "## 8. Commit Contents") == {"a.py", "b.py"}


def test_a_leading_not_changed_line_does_not_empty_the_list():
    text = _block("Not changed: nothing.", "`a.py`")
    assert pc.eip_commit_contents(text, "## 8. Commit Contents") == {"a.py"}


def test_parse_pytest_counts_failures_and_errors():
    assert pc.parse_pytest("3 failed, 759 passed, 1 skipped, 2 errors in 51s") == {
        "passed": 759,
        "failed": 3,
        "errors": 2,
        "skipped": 1,
    }


def test_parse_validator_reads_the_summary_line():
    assert pc.parse_validator("Repository validation passed: 0 errors, 348 warning(s).") == (0, 348)
    assert pc.parse_validator("Repository validation failed: 2 error(s), 302 warning(s).") == (2, 302)


def test_latest_submit_response_ref_takes_the_last_gate(monkeypatch, tmp_path):
    monkeypatch.setattr(pc, "TRANSCRIPT_DIR", tmp_path)
    (tmp_path / "ESR-0061-WP1c.md").write_text(
        "\n===\ntype: submit-to-review\nrepository_ref: aaa\n---\nx\n"
        "\n===\ntype: submit-response\nrepository_ref: bbb\n---\nfirst\n"
        "\n===\ntype: return-findings\nrepository_ref: ccc\n---\nverdict\n"
        "\n===\ntype: submit-response\nrepository_ref: ddd\n---\nsecond\n",
        encoding="utf-8",
    )
    assert pc.latest_submit_response_ref("ESR-0061", "WP1c") == "ddd"


def test_advisory_figures_report_differences_without_failing():
    notes = pc.advisory_figures(
        "pytest 759 passed; validator 0 errors, 348 warnings",
        {"passed": 790, "failed": 0, "errors": 0, "skipped": 1},
        (0, 302),
    )
    assert notes == [
        "commit message says 759 passed; actual 790",
        "commit message says 348 warnings; validator reports 302",
    ]


def test_advisory_ignores_cargo_and_linux_figures_but_not_pytest_ones():
    counts = {"passed": 865, "failed": 0, "errors": 0, "skipped": 1}
    assert pc.advisory_figures("cargo test 19 passed; Linux 866 passed; pytest 865 passed", counts, None) == []
    assert pc.advisory_figures("19 passed", counts, None) == []
    assert pc.advisory_figures("pytest 800 passed", counts, None) == ["commit message says 800 passed; actual 865"]


def _fake_git(outputs: dict[tuple[str, ...], str]):
    def fake(*args):
        return outputs.get(args, "")

    return fake


def test_precheck_flags_unlisted_files_and_a_wrong_gate(monkeypatch, tmp_path):
    eip = tmp_path / "EIP.md"
    eip.write_text(EIP_TEXT, encoding="utf-8")
    monkeypatch.setattr(pc, "TRANSCRIPT_DIR", tmp_path)
    (tmp_path / "ESR-0061-WP1c.md").write_text("\n===\ntype: submit-response\nrepository_ref: other\n---\nx\n", encoding="utf-8")
    monkeypatch.setattr(
        pc,
        "git",
        _fake_git(
            {
                ("rev-parse", "HEAD"): "c1",
                ("rev-parse", "HEAD^"): "p1",
                ("status", "--porcelain"): "",
                ("branch", "-r", "--contains", "c1"): "origin/main",
                ("diff-tree", "--no-commit-id", "--name-only", "-r", "c1"): "scripts/run_reviewer.py\nREADME.md",
                ("log", "-1", "--format=%B", "c1"): "WP1c",
            }
        ),
    )

    report = pc.precheck("HEAD", "ESR-0061", "WP1c", eip, "## 7.4 Commit Contents", run_suites=False)

    results = {name: ok for name, ok, _ in report.hard}
    assert results["working tree clean"] and results["commit is on origin/main"]
    assert not results["changed files equal the EIP's Commit Contents"]
    assert not results["submit-response gated against the commit's parent"]
    assert not report.passed
    assert "FAIL" in report.render()


def test_precheck_passes_when_everything_matches(monkeypatch, tmp_path):
    eip = tmp_path / "EIP.md"
    eip.write_text("## 7.4 Commit Contents\n\n`scripts/run_reviewer.py`\n", encoding="utf-8")
    monkeypatch.setattr(pc, "TRANSCRIPT_DIR", tmp_path)
    (tmp_path / "ESR-0061-WP1c.md").write_text("\n===\ntype: submit-response\nrepository_ref: p1\n---\nx\n", encoding="utf-8")
    monkeypatch.setattr(
        pc,
        "git",
        _fake_git(
            {
                ("rev-parse", "HEAD"): "c1",
                ("rev-parse", "HEAD^"): "p1",
                ("branch", "-r", "--contains", "c1"): "origin/main",
                ("diff-tree", "--no-commit-id", "--name-only", "-r", "c1"): "scripts/run_reviewer.py",
            }
        ),
    )

    report = pc.precheck("HEAD", "ESR-0061", "WP1c", eip, "## 7.4 Commit Contents", run_suites=False)

    assert report.passed, report.render()
