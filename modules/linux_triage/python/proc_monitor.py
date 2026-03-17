import sys
import time
import os


def get_page_size_kb():
    """Определяем размер страницы памяти системы в KB."""
    try:
        return os.sysconf("SC_PAGE_SIZE") / 1024
    except (ValueError, AttributeError):
        return 4.0


def get_proc_stats(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as f:
            data = f.read().split()
            utime = int(data[13])
            stime = int(data[14])
            rss_pages = int(data[23])
            return utime + stime, rss_pages
    except FileNotFoundError:
        return None, None


def monitor(pid, interval):
    page_size_kb = get_page_size_kb()

    print(f"[*] Старт мониторинга PID {pid}.")
    print(f"[*] Интервал: {interval} сек. | Размер страницы: {page_size_kb} KB")
    print("-" * 55)
    print(f"{'Время':<10} | {'RSS Память (KB)':<18} | {'CPU (Delta Ticks)':<15}")
    print("-" * 55)

    prev_ticks = -1

    try:
        while True:
            curr_ticks, rss_pages = get_proc_stats(pid)

            if curr_ticks is None:
                print(f"\n[!] Процесс {pid} завершился или исчез.")
                break

            if prev_ticks == -1:
                cpu_delta = 0
            else:
                cpu_delta = curr_ticks - prev_ticks

            prev_ticks = curr_ticks

            rss_kb = int(rss_pages * page_size_kb)
            timestamp = time.strftime("%H:%M:%S")

            print(f"{timestamp:<10} | {rss_kb:<18} | {cpu_delta:<15}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nМониторинг остановлен пользователем.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 proc_monitor.py <PID> [интервал]")
        sys.exit(1)

    target_pid = sys.argv[1]
    interval_sec = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    if not os.path.exists(f"/proc/{target_pid}"):
        print(f"Ошибка: PID {target_pid} не найден.")
        sys.exit(1)

    monitor(target_pid, interval_sec)

