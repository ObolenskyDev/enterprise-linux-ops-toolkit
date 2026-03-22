# ops-core-utils

Набор CLI-утилит для Linux-операций: триаж, разбор логов KESL, проверка портов, разбор медленных SQL, рутина и ротация логов. Команда в консоли по-прежнему **`elot`**.

## Что внутри

* **Linux Triage**: мониторинг процесса по `/proc` (только Linux).
* **KESL Logs**: разбор больших trace-логов построчно.
* **Network**: TCP-проверка портов без `nc`.
* **DB Helper**: медленные запросы из лога PostgreSQL.
* **Routine**: HTTP health-check, очистка старых логов, tar-бэкап каталога.
* **Logs**: сжатие старых логов и удаление устаревших `.gz`.

## Быстрый старт

### Windows (PowerShell)

```powershell
cd путь\к\ops-core-utils
py -m pip install -e .
py -m ops_toolkit.cli --help
```

После установки скрипт `elot` появится в каталоге Scripts Python (при необходимости добавьте его в `PATH`).

### Linux

```bash
cd /path/to/ops-core-utils
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
elot --help
```

## Примеры

```bash
# Linux: мониторинг PID
elot triage proc-monitor <PID> --interval 1

# KESL
elot kesl analyze /var/log/kaspersky/kesl/kesl_launcher.log --max-duplicates 2

# Порты
elot net tcp-ping 10.0.0.5 5432 636 --timeout 2

# Медленные запросы в логе PostgreSQL
elot db slow-queries /var/log/postgresql/postgresql-15-main.log --threshold-ms 2000

# Ротация логов (сначала dry-run)
elot logs rotate --dir /var/log --compress-after-days 7 --delete-after-days 30 --dry-run
```

## Структура репозитория

```
ops-core-utils/
  src/ops_toolkit/
    cli.py              # точка входа CLI (argparse)
    modules/            # triage, kesl, net, db, routine, log_maintenance
  pyproject.toml
  LICENSE
  README.md
```

Вся логика — в Python под `src/ops_toolkit/`; отдельных shell-скриптов в репозитории нет.
