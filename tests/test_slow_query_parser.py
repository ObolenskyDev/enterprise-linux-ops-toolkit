import os
import tempfile

from ops_toolkit.modules.db_incident_helper.slow_query_parser import run


def _write_log(directory: str, lines: list[str]) -> str:
    path = os.path.join(directory, "pg.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def test_finds_slow_query(capsys):
    with tempfile.TemporaryDirectory() as d:
        log = _write_log(d, [
            "2026-01-01 10:00:00 LOG:  duration: 2500.0 ms  statement: SELECT * FROM hosts;",
            "2026-01-01 10:00:01 LOG:  duration: 200.0 ms  statement: SELECT 1;",
        ])
        rc = run(filepath=log, threshold_ms=1000)
        assert rc == 0
        out = capsys.readouterr().out
        assert "2500.0" in out
        assert "200.0" not in out


def test_no_slow_queries(capsys):
    with tempfile.TemporaryDirectory() as d:
        log = _write_log(d, [
            "2026-01-01 10:00:00 LOG:  duration: 50.0 ms  statement: SELECT 1;",
        ])
        rc = run(filepath=log, threshold_ms=1000)
        assert rc == 0
        out = capsys.readouterr().out
        assert "No slow queries" in out


def test_file_not_found():
    rc = run(filepath="/tmp/nonexistent_pg_elot.log")
    assert rc == 1


def test_custom_threshold(capsys):
    with tempfile.TemporaryDirectory() as d:
        log = _write_log(d, [
            "LOG:  duration: 300.0 ms  statement: SELECT 1;",
            "LOG:  duration: 1500.0 ms  statement: SELECT * FROM big;",
        ])
        rc = run(filepath=log, threshold_ms=200)
        assert rc == 0
        out = capsys.readouterr().out
        assert "300.0" in out
        assert "1500.0" in out
