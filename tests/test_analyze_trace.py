import os
import tempfile

from ops_toolkit.modules.kesl_log_analyzer.analyze_trace import run


def _write_log(directory: str, lines: list[str]) -> str:
    path = os.path.join(directory, "kesl.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def test_finds_error_lines(capsys):
    with tempfile.TemporaryDirectory() as d:
        log = _write_log(d, [
            "2026-01-01 10:00:00 INFO  Service started",
            "2026-01-01 10:00:01 ERROR fanotify: failed to add watch",
            "2026-01-01 10:00:02 INFO  Retrying",
        ])
        rc = run(filepath=log)
        assert rc == 0
        out = capsys.readouterr().out
        assert "fanotify" in out


def test_no_errors_reports_ok(capsys):
    with tempfile.TemporaryDirectory() as d:
        log = _write_log(d, [
            "2026-01-01 10:00:00 INFO  Service started",
            "2026-01-01 10:00:01 INFO  Update complete",
        ])
        rc = run(filepath=log)
        assert rc == 0
        out = capsys.readouterr().out
        assert "No critical" in out


def test_dedup_suppresses_spam(capsys):
    with tempfile.TemporaryDirectory() as d:
        repeated = "2026-01-01 10:00:0{i} ERROR same error message repeated"
        lines = [f"2026-01-01 10:00:0{i} ERROR same error message repeated" for i in range(9)]
        log = _write_log(d, lines)
        rc = run(filepath=log, max_duplicates=2)
        assert rc == 0
        out = capsys.readouterr().out
        assert "SPAM" in out or "suppressed" in out.lower() or "frequent" in out.lower()


def test_file_not_found(capsys):
    rc = run(filepath="/tmp/nonexistent_kesl_elot.log")
    assert rc == 1
