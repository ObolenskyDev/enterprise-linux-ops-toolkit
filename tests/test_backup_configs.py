import os
import tarfile
import tempfile

from ops_toolkit.modules.routine.backup_configs import run


def test_creates_archive():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
        with open(os.path.join(src, "nginx.conf"), "w") as f:
            f.write("server {}")
        rc = run(source=src, backup_dir=dst)
        assert rc == 0
        archives = os.listdir(dst)
        assert len(archives) == 1
        assert archives[0].endswith(".tar.gz")


def test_archive_contains_source_files():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
        with open(os.path.join(src, "app.conf"), "w") as f:
            f.write("key=value")
        run(source=src, backup_dir=dst)
        archive = os.path.join(dst, os.listdir(dst)[0])
        with tarfile.open(archive, "r:gz") as tf:
            names = tf.getnames()
        assert any("app.conf" in n for n in names)


def test_custom_archive_name():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
        with open(os.path.join(src, "f.conf"), "w") as f:
            f.write("x")
        run(source=src, backup_dir=dst, name="mybackup")
        archives = os.listdir(dst)
        assert archives[0].startswith("mybackup_")


def test_source_not_found():
    with tempfile.TemporaryDirectory() as dst:
        rc = run(source="/tmp/nonexistent_elot_src", backup_dir=dst)
        assert rc == 2
