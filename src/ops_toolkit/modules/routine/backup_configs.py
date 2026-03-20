from __future__ import annotations

import os
import tarfile
import time


def run(source: str, backup_dir: str, name: str | None = None) -> int:
    if not os.path.exists(source):
        print(f"[error] Source not found: {source}")
        return 2

    os.makedirs(backup_dir, exist_ok=True)
    ts = time.strftime("%Y-%m-%d_%H-%M")
    base = name or os.path.basename(os.path.abspath(source)) or "backup"
    archive_name = f"{base}_config_{ts}.tar.gz"
    out_path = os.path.join(backup_dir, archive_name)

    try:
        with tarfile.open(out_path, "w:gz") as tf:
            tf.add(source, arcname=os.path.basename(source))
    except Exception as e:
        print(f"[error] Backup failed: {e}")
        return 1

    print("--- [ROUTINE] Config backup ---")
    print(f"Source: {source}")
    print(f"Output: {out_path}")
    return 0

