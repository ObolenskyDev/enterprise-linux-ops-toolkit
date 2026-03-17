import os
import re
import sys
from collections import deque


def _supports_ansi() -> bool:
    if os.name != "posix":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_ANSI = _supports_ansi()
RED = "\033[91m" if _ANSI else ""
GREEN = "\033[92m" if _ANSI else ""
YELLOW = "\033[93m" if _ANSI else ""
RESET = "\033[0m" if _ANSI else ""


def run(filepath: str, max_duplicates: int = 2) -> int:
    if not os.path.exists(filepath):
        print(f"{RED}[error] File not found: {filepath}{RESET}")
        return 1

    print(f"{GREEN}--- Line-by-line analysis: {filepath} ---{RESET}")

    error_pattern = re.compile(r"(error|fail|critical|exception|denied)", re.IGNORECASE)

    found_count = 0
    buffer = deque(maxlen=2)
    seen_errors: dict[str, int] = {}

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                clean_line = line.lstrip("\ufeff").strip()

                if error_pattern.search(clean_line):
                    parts = clean_line.split()
                    msg_key = " ".join(parts[3:]) if len(parts) > 3 else clean_line
                    seen_errors[msg_key] = seen_errors.get(msg_key, 0) + 1

                    if seen_errors[msg_key] <= max_duplicates:
                        found_count += 1
                        print(f"\n{YELLOW}[Event #{found_count} | Line {i+1}]{RESET}")

                        for b_line in buffer:
                            print(f"  {b_line}")

                        print(f"{RED}>> {clean_line}{RESET}")

                        try:
                            next_line = next(f).strip()
                            print(f"  {next_line}")
                        except StopIteration:
                            pass

                        print("-" * 30)

                buffer.append(clean_line)

        print(f"\n{GREEN}--- Summary ---{RESET}")
        if found_count == 0:
            print(f"{GREEN}[OK] No critical matches found.{RESET}")
        else:
            print(f"Printed unique/rare events: {found_count}")
            print(f"\n{YELLOW}Most frequent (suppressed) messages:{RESET}")
            for msg, count in seen_errors.items():
                if count > max_duplicates:
                    print(f" [SPAM] {count}x: {msg[:100]}...")

        return 0
    except Exception as e:
        print(f"[error] Processing failed: {e}")
        return 2

