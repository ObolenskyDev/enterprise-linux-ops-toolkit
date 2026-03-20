from __future__ import annotations

import urllib.request
from urllib.error import HTTPError, URLError


def run(urls: list[str], timeout: float = 5.0) -> int:
    print("--- [ROUTINE] Health check ---")
    if not urls:
        print("[error] No URLs provided.")
        return 2

    any_ok = False
    for url in urls:
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = getattr(resp, "status", 200)
                if code == 200:
                    any_ok = True
                    print(f"[OK] 200 {url}")
                else:
                    print(f"[WARN] {code} {url}")
        except HTTPError as e:
            print(f"[FAIL] {e.code} {url}")
        except URLError:
            print(f"[FAIL] UNREACHABLE {url}")
        except Exception as e:
            print(f"[FAIL] ERROR {url}: {e}")

    return 0 if any_ok else 1

