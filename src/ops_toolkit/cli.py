import argparse
import os
import sys

from elotoolkit.modules.kesl_log_analyzer import analyze_trace
from elotoolkit.modules.linux_triage import proc_monitor
from elotoolkit.modules.network_ssl_tools import tcp_ping
from elotoolkit.modules.db_incident_helper import slow_query_parser
from elotoolkit.modules.routine import backup_configs, clear_logs, health_check
from elotoolkit.modules.log_maintenance import rotate as log_rotate


def _add_triage(subparsers: argparse._SubParsersAction) -> None:
    triage = subparsers.add_parser("triage", help="Linux incident triage utilities")
    triage_sub = triage.add_subparsers(dest="triage_cmd", required=True)

    pm = triage_sub.add_parser("proc-monitor", help="Monitor RSS/CPU ticks for a PID via /proc")
    pm.add_argument("pid", type=int)
    pm.add_argument("--interval", type=float, default=1.0)


def _add_kesl(subparsers: argparse._SubParsersAction) -> None:
    kesl = subparsers.add_parser("kesl", help="KESL trace/log utilities")
    kesl_sub = kesl.add_subparsers(dest="kesl_cmd", required=True)

    analyze = kesl_sub.add_parser("analyze", help="Analyze a large log file line-by-line")
    analyze.add_argument("path")
    analyze.add_argument("--max-duplicates", type=int, default=2)

def _add_net(subparsers: argparse._SubParsersAction) -> None:
    net = subparsers.add_parser("net", help="Network/SSL support utilities")
    net_sub = net.add_subparsers(dest="net_cmd", required=True)

    ping = net_sub.add_parser("tcp-ping", help="Check TCP ports (telnet/nc replacement)")
    ping.add_argument("host")
    ping.add_argument("ports", nargs="+", type=int)
    ping.add_argument("--timeout", type=float, default=2.0)


def _add_db(subparsers: argparse._SubParsersAction) -> None:
    db = subparsers.add_parser("db", help="Database incident helper utilities")
    db_sub = db.add_subparsers(dest="db_cmd", required=True)

    slow = db_sub.add_parser("slow-queries", help="Parse PostgreSQL logs for slow queries")
    slow.add_argument("path")
    slow.add_argument("--threshold-ms", type=int, default=1000)

def _add_routine(subparsers: argparse._SubParsersAction) -> None:
    routine = subparsers.add_parser("routine", help="Routine maintenance utilities")
    routine_sub = routine.add_subparsers(dest="routine_cmd", required=True)

    hc = routine_sub.add_parser("health-check", help="HTTP health check for one or more URLs")
    hc.add_argument("urls", nargs="+")
    hc.add_argument("--timeout", type=float, default=5.0)

    cl = routine_sub.add_parser("clear-logs", help="Delete old log files by suffix and age")
    cl.add_argument("dir")
    cl.add_argument("--days", type=int, default=7)
    cl.add_argument("--suffix", default=".log")

    bc = routine_sub.add_parser("backup-configs", help="Create tar.gz backup of a directory/file")
    bc.add_argument("source")
    bc.add_argument("backup_dir")
    bc.add_argument("--name", default=None)

def _add_logs(subparsers: argparse._SubParsersAction) -> None:
    logs = subparsers.add_parser("logs", help="Log maintenance utilities")
    logs_sub = logs.add_subparsers(dest="logs_cmd", required=True)

    rot = logs_sub.add_parser("rotate", help="Compress old logs and delete old .gz archives")
    rot.add_argument("--dir", required=True, dest="dir")
    rot.add_argument("--compress-after-days", type=int, default=7)
    rot.add_argument("--delete-after-days", type=int, default=30)
    rot.add_argument("--exclude-contains", action="append", default=[])
    rot.add_argument("--dry-run", action="store_true", default=False)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    parser = argparse.ArgumentParser(prog="elot", description="Enterprise Linux Ops Toolkit")
    subparsers = parser.add_subparsers(dest="module", required=True)

    _add_triage(subparsers)
    _add_kesl(subparsers)
    _add_net(subparsers)
    _add_db(subparsers)
    _add_routine(subparsers)
    _add_logs(subparsers)

    args = parser.parse_args(argv)

    if args.module == "triage" and args.triage_cmd == "proc-monitor":
        if os.name != "posix":
            print("[error] proc-monitor requires Linux (/proc).", file=sys.stderr)
            return 2
        return proc_monitor.run(pid=args.pid, interval=args.interval)

    if args.module == "kesl" and args.kesl_cmd == "analyze":
        return analyze_trace.run(filepath=args.path, max_duplicates=args.max_duplicates)

    if args.module == "net" and args.net_cmd == "tcp-ping":
        return tcp_ping.run(host=args.host, ports=args.ports, timeout=args.timeout)

    if args.module == "db" and args.db_cmd == "slow-queries":
        return slow_query_parser.run(filepath=args.path, threshold_ms=args.threshold_ms)

    if args.module == "routine" and args.routine_cmd == "health-check":
        return health_check.run(urls=args.urls, timeout=args.timeout)

    if args.module == "routine" and args.routine_cmd == "clear-logs":
        return clear_logs.run(log_dir=args.dir, days=args.days, pattern_suffix=args.suffix)

    if args.module == "routine" and args.routine_cmd == "backup-configs":
        return backup_configs.run(source=args.source, backup_dir=args.backup_dir, name=args.name)

    if args.module == "logs" and args.logs_cmd == "rotate":
        return log_rotate.run(
            log_dir=args.dir,
            compress_after_days=args.compress_after_days,
            delete_after_days=args.delete_after_days,
            exclude_contains=args.exclude_contains,
            dry_run=args.dry_run,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

