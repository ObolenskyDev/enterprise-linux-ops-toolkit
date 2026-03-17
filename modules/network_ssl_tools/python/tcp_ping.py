import socket
import sys


def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python3 tcp_ping.py <хост> <порт1> [порт2...]")
        sys.exit(1)

    target_host = sys.argv[1]
    ports = sys.argv[2:]

    print(f"--- [NET] Проверка портов для {target_host} ---")

    for p in ports:
        try:
            port_num = int(p)
            if check_port(target_host, port_num):
                print(f"Порт {port_num:<5}: ✅ ОТКРЫТ (OPEN)")
            else:
                print(f"Порт {port_num:<5}: ❌ НЕДОСТУПЕН (CLOSED/FILTERED)")
        except ValueError:
            print(f"Ошибка: {p} не является номером порта")

