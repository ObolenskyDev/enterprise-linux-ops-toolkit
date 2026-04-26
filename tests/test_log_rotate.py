import gzip
import os
import time
import tempfile

from ops_toolkit.modules.log_maintenance.rotate import run


def _make_file(directory: str, name: str, age_days: int) -> str:
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write("log line\n" * 10)
    old_mtime = time.time() - age_days * 86400
    os.utime(path, (old_mtime, old_mtime))
    return path


def test_compresses_old_log():
    with tempfile.TemporaryDirectory() as d:
        old = _make_file(d, "app.log", age_days=10)
        assert run(log_dir=d, compress_after_days=7, delete_after_days=30) == 0
        assert not os.path.exists(old)
        assert os.path.exists(old + ".gz")


def test_gz_is_valid_after_compression():
    with tempfile.TemporaryDirectory() as d:
        old = _make_file(d, "app.log", age_days=10)
        run(log_dir=d, compress_after_days=7, delete_after_days=30)
        with gzip.open(old + ".gz", "rt") as f:
            content = f.read()
        assert "log line" in content


def test_deletes_old_gz():
    with tempfile.TemporaryDirectory() as d:
        gz_path = os.path.join(d, "old.log.gz")
        with gzip.open(gz_path, "wt") as f:
            f.write("archived\n")
        old_mtime = time.time() - 40 * 86400
        os.utime(gz_path, (old_mtime, old_mtime))
        assert run(log_dir=d, compress_after_days=7, delete_after_days=30) == 0
        assert not os.path.exists(gz_path)


def test_dry_run_no_changes():
    with tempfile.TemporaryDirectory() as d:
        old = _make_file(d, "app.log", age_days=10)
        assert run(log_dir=d, compress_after_days=7, delete_after_days=30, dry_run=True) == 0
        assert os.path.exists(old)
        assert not os.path.exists(old + ".gz")


def test_exclude_contains_skips_file():
    with tempfile.TemporaryDirectory() as d:
        kept = _make_file(d, "kesl_trace.log", age_days=10)
        assert run(log_dir=d, compress_after_days=7, delete_after_days=30, exclude_contains=["kesl"]) == 0
        assert os.path.exists(kept)


def test_nonexistent_directory():
    assert run(log_dir="/tmp/nonexistent_elot_rotate_xyz") == 2
