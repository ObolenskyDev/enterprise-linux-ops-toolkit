import os
import time


def _get_page_size_kb() -> float:
    try:
        return os.sysconf("SC_PAGE_SIZE") / 1024
    except (ValueError, AttributeError):
        return 4.0


def _get_proc_stats(pid: int) -> tuple[int | None, int | None]:
    try:
        with open(f"/proc/{pid}/stat", "r", encoding="utf-8", errors="ignore") as f:
            data = f.read().split()
            utime = int(data[13])
            stime = int(data[14])
            rss_pages = int(data[23])
            return utime + stime, rss_pages
    except FileNotFoundError:
        return None, None


def run(pid: int, interval: float = 1.0) -> int:
    if not os.path.exists(f"/proc/{pid}"):
        print(f"Ошибка: PID {pid} не найден.")
        return 1

    page_size_kb = _get_page_size_kb()

    print(f"[*] Старт мониторинга PID {pid}.")
    print(f"[*] Интервал: {interval} сек. | Размер страницы: {page_size_kb} KB")
    print("-" * 55)
    print(f"{'Время':<10} | {'RSS Память (KB)':<18} | {'CPU (Delta Ticks)':<15}")
    print("-" * 55)

    prev_ticks = -1
    try:
        while True:
            curr_ticks, rss_pages = _get_proc_stats(pid)
            if curr_ticks is None:
                print(f"\n[!] Процесс {pid} завершился или исчез.")
                return 0

            cpu_delta = 0 if prev_ticks == -1 else curr_ticks - prev_ticks
            prev_ticks = curr_ticks

            rss_kb = int((rss_pages or 0) * page_size_kb)
            timestamp = time.strftime("%H:%M:%S")
            print(f"{timestamp:<10} | {rss_kb:<18} | {cpu_delta:<15}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nМониторинг остановлен пользователем.")
        return 0

