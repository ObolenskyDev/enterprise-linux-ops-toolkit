import socket


def _check_port(host: str, port: int, timeout: float) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def run(host: str, ports: list[int], timeout: float = 2.0) -> int:
    print(f"--- [NET] TCP port check for {host} ---")
    any_ok = False

    for port in ports:
        if _check_port(host, port, timeout=timeout):
            any_ok = True
            print(f"Port {port:<5}: [OK] OPEN")
        else:
            print(f"Port {port:<5}: [FAIL] CLOSED/FILTERED")

    return 0 if any_ok else 1

