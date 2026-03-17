import os
import re


def run(filepath: str, threshold_ms: int = 1000) -> int:
    print(f"--- [DB] Log parse: {filepath} ---")
    print(f"--- Finding queries slower than {threshold_ms} ms ---\n")

    if not os.path.exists(filepath):
        print(f"[error] File not found: {filepath}")
        return 1

    regex = re.compile(r"duration:\s+(\d+\.\d+)\s+ms")
    slow_queries: list[tuple[float, str]] = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = regex.search(line)
                if match:
                    duration = float(match.group(1))
                    if duration > threshold_ms:
                        slow_queries.append((duration, line.strip()))
    except Exception as e:
        print(f"[error] Read failed: {e}")
        return 2

    slow_queries.sort(key=lambda x: x[0], reverse=True)
    if not slow_queries:
        print("[OK] No slow queries found.")
        return 0

    print(f"[WARN] Found {len(slow_queries)} slow queries. Top 5:")
    print("-" * 60)
    for dur, text in slow_queries[:5]:
        clean_text = text[:120] + "..." if len(text) > 120 else text
        print(f"{dur} ms | {clean_text}")
    print("-" * 60)
    return 0

