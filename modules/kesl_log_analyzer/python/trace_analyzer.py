import sys
import re
import os
from collections import deque


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def analyze_trace(filepath, max_duplicates=3):
    if not os.path.exists(filepath):
        print(f"{RED}[Ошибка] Файл {filepath} не найден.{RESET}")
        return

    print(f"{GREEN}--- Построчный анализ: {filepath} ---{RESET}")

    error_pattern = re.compile(r"(error|fail|critical|exception|denied)", re.IGNORECASE)

    found_count = 0
    buffer = deque(maxlen=2)  # Храним 2 предыдущие строки для контекста
    seen_errors = {}  # Для борьбы со спамом одинаковых ошибок

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                clean_line = line.strip()

                if error_pattern.search(clean_line):
                    msg_key = " ".join(clean_line.split()[3:]) if len(clean_line.split()) > 3 else clean_line

                    seen_errors[msg_key] = seen_errors.get(msg_key, 0) + 1

                    if seen_errors[msg_key] <= max_duplicates:
                        found_count += 1
                        print(f"\n{YELLOW}[Событие #{found_count} | Строка {i+1}]{RESET}")

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

        print(f"\n{GREEN}--- Итоги анализа ---{RESET}")
        if found_count == 0:
            print(f"{GREEN}✅ Критических ошибок не обнаружено.{RESET}")
        else:
            print(f"Всего уникальных/редких событий выведено: {found_count}")
            print(f"\n{YELLOW}Топ повторяющихся ошибок (спам):{RESET}")
            for msg, count in seen_errors.items():
                if count > max_duplicates:
                    print(f" 🔁 {count} раз: {msg[:100]}...")

    except Exception as e:
        print(f"Ошибка обработки: {e}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "logs/kesl_trace.log"
    analyze_trace(path, max_duplicates=2)

