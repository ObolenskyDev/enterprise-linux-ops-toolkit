from __future__ import annotations

import gzip
import os
import shutil
import time


def _iter_files(root: str) -> list[str]:
    out: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            out.append(os.path.join(dirpath, fn))
    return out


def run(
    log_dir: str,
    compress_after_days: int = 7,
    delete_after_days: int = 30,
    exclude_contains: list[str] | None = None,
    dry_run: bool = False,
) -> int:
    if not os.path.isdir(log_dir):
        print(f"[error] Directory not found: {log_dir}")
        return 2

    exclude_contains = exclude_contains or []
    now = time.time()
    compress_cutoff = now - compress_after_days * 86400
    delete_cutoff = now - delete_after_days * 86400

    gzipped = 0
    deleted = 0

    print("--- [LOG] Maintenance ---")
    print(f"Dir: {log_dir}")
    print(f"Compress after (days): {compress_after_days}")
    print(f"Delete .gz after (days): {delete_after_days}")
    if dry_run:
        print("[info] Dry run: no changes will be made.")

    for path in _iter_files(log_dir):
        base = os.path.basename(path)
        if any(x in base for x in exclude_contains):
            continue

        try:
            st = os.stat(path)
        except FileNotFoundError:
            continue

        # delete old .gz
        if base.endswith(".gz") and st.st_mtime < delete_cutoff:
            if dry_run:
                print(f"[DRY] delete {path}")
            else:
                try:
                    os.remove(path)
                    deleted += 1
                except Exception as e:
                    print(f"[warn] Failed to delete {path}: {e}")
            continue

        # compress old non-gz
        if not base.endswith(".gz") and st.st_mtime < compress_cutoff:
            gz_path = path + ".gz"
            if dry_run:
                print(f"[DRY] gzip {path} -> {gz_path}")
                continue

            try:
                with open(path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                os.remove(path)
                gzipped += 1
            except Exception as e:
                print(f"[warn] Failed to gzip {path}: {e}")

    print(f"Gzipped: {gzipped}")
    print(f"Deleted .gz: {deleted}")
    return 0

