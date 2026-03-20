from __future__ import annotations

import os
import time


def run(log_dir: str, days: int = 7, pattern_suffix: str = ".log") -> int:
    if not os.path.isdir(log_dir):
        print(f"[error] Directory not found: {log_dir}")
        return 2

    cutoff = time.time() - days * 86400
    deleted = 0
    scanned = 0

    for root, _dirs, files in os.walk(log_dir):
        for name in files:
            if pattern_suffix and not name.endswith(pattern_suffix):
                continue
            scanned += 1
            path = os.path.join(root, name)
            try:
                st = os.stat(path)
                if st.st_mtime < cutoff:
                    os.remove(path)
                    deleted += 1
            except FileNotFoundError:
                continue
            except PermissionError:
                print(f"[warn] Permission denied: {path}")
            except Exception as e:
                print(f"[warn] Failed to delete {path}: {e}")

    print(f"--- [ROUTINE] Log cleanup ---")
    print(f"Dir: {log_dir}")
    print(f"Days: {days}")
    print(f"Matched files: {scanned}")
    print(f"Deleted: {deleted}")
    return 0

