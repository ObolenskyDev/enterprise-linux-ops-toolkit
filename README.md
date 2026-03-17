# 🧰 Enterprise Linux Ops Toolkit

Это “одна коробка” с утилитами, которые обычно собираются по разным папкам в момент инцидента: быстро посмотреть систему, дёрнуть сеть/порты, понять что творится в логах, и аккуратно прибраться с ротацией.

Если коротко: **ставишь один раз — используешь как швейцарский нож**.

## Что внутри (по-человечески)

- **Linux triage**: быстрый аудит, поиск разросшихся файлов, мониторинг PID (через `/proc`).
- **KESL logs**: построчный анализ больших логов (без съедания RAM).
- **Network/SSL**: проверить порты без `nc`, плюс набор shell-скриптов под OpenSSL.
- **DB helper**: проверить базу “жива/не жива” и вытащить топ медленных запросов из логов.
- **Routine**: мелкие регламентные штуки (health-check URL, очистка логов, бэкап конфигов).
- **Logs maintenance**: единая команда “сжать старое / удалить совсем старое”.

## Быстрый старт

### Windows / PowerShell (у тебя актуально)

```powershell
cd c:\Users\N7\Documents\GitHub\enterprise-linux-ops-toolkit
py -m pip install -e .
py -m elotoolkit.cli --help
```

### Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
elot --help
```

## Команды, которые реально нужны в жизни

```bash
# 1) Быстро понять “что горит” на сервере (Linux)
elot triage proc-monitor <PID> --interval 1

# 2) Разобрать огромный лог KESL
elot kesl analyze /var/log/kaspersky/kesl/kesl_launcher.log --max-duplicates 2

# 3) Проверить доступность портов (кроссплатформенно)
elot net tcp-ping 10.0.0.5 5432 636 --timeout 2

# 4) Найти медленные запросы по PostgreSQL-логу
elot db slow-queries /var/log/postgresql/postgresql-15-main.log --threshold-ms 2000

# 5) Поджать и подчистить старые логи
elot logs rotate --dir /var/log --compress-after-days 7 --delete-after-days 30 --dry-run
```

## Если нужно “по-старинке”

Оригинальные shell-скрипты оставлены, их можно дергать напрямую:

```bash
sudo bash modules/linux_triage/bin/quick_audit.sh
bash modules/linux_triage/bin/find_heavy_files.sh /var/log
sudo bash modules/kesl_log_analyzer/bin/log_rotate.sh
```

## Структура проекта

```
enterprise-linux-ops-toolkit/
  modules/                 # исходные скрипты (bash/python) “как есть”
  src/elotoolkit/          # общий python-пакет + CLI
  pyproject.toml
```

