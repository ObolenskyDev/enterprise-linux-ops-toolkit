import re
import sys
import os


def parse_log(filepath, threshold_ms=1000):
    print(f"--- [LOG] Анализ файла: {filepath} ---")
    print(f"--- Поиск запросов длительностью более {threshold_ms} ms ---\n")

    if not os.path.exists(filepath):
        print(f"Ошибка: Файл {filepath} не найден.")
        return

    regex = re.compile(r"duration:\s+(\d+\.\d+)\s+ms")

    slow_queries = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = regex.search(line)
                if match:
                    duration = float(match.group(1))
                    if duration > threshold_ms:
                        slow_queries.append((duration, line.strip()))
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    slow_queries.sort(key=lambda x: x[0], reverse=True)

    count = len(slow_queries)
    if count == 0:
        print("✅ Медленных запросов не обнаружено.")
    else:
        print(f"⚠️  Найдено {count} медленных запросов. Топ-5 самых длительных:")
        print("-" * 60)
        for dur, text in slow_queries[:5]:
            clean_text = text[:120] + "..." if len(text) > 120 else text
            print(f"⏱️  {dur} ms | {clean_text}")
        print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_dir = "logs"
        demo_file = os.path.join(log_dir, "demo_pg.log")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        print(f"[DEMO] Файл не указан. Генерация тестового лога '{demo_file}'...")
        with open(demo_file, "w") as f:
            f.write("2026-02-15 10:00:01 LOG:  duration: 40.0 ms  statement: SELECT 1;\n")
            f.write(
                "2026-02-15 10:00:05 LOG:  duration: 5400.12 ms  statement: "
                "SELECT * FROM klnag_events WHERE id LIKE '%error%';\n"
            )
            f.write("2026-02-15 10:01:00 LOG:  duration: 1200.0 ms  statement: UPDATE hosts SET status='offline';\n")

        parse_log(demo_file)
    else:
        threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        parse_log(sys.argv[1], threshold)

