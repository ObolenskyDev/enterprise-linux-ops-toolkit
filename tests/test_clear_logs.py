import os
import time
import tempfile
import pytest

from ops_toolkit.modules.routine.clear_logs import run


def _make_old_file(directory: str, name: str, age_days: int) -> str:
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write("x")
    old_mtime = time.time() - age_days * 86400
    os.utime(path, (old_mtime, old_mtime))
    return path


def test_deletes_old_logs():
    with tempfile.TemporaryDirectory() as d:
        old = _make_old_file(d, "app.log", age_days=10)
        assert run(log_dir=d, days=7) == 0
        assert not os.path.exists(old)


def test_keeps_recent_logs():
    with tempfile.TemporaryDirectory() as d:
        recent = _make_old_file(d, "app.log", age_days=2)
        assert run(log_dir=d, days=7) == 0
        assert os.path.exists(recent)


def test_dry_run_does_not_delete():
    with tempfile.TemporaryDirectory() as d:
        old = _make_old_file(d, "app.log", age_days=10)
        assert run(log_dir=d, days=7, dry_run=True) == 0
        assert os.path.exists(old)


def test_suffix_filter():
    with tempfile.TemporaryDirectory() as d:
        log_file = _make_old_file(d, "app.log", age_days=10)
        txt_file = _make_old_file(d, "app.txt", age_days=10)
        assert run(log_dir=d, days=7, pattern_suffix=".log") == 0
        assert not os.path.exists(log_file)
        assert os.path.exists(txt_file)


def test_nonexistent_directory():
    assert run(log_dir="/tmp/nonexistent_elot_test_xyz") == 2
