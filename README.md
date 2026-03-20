# 🚀 **Enterprise Linux Ops Toolkit**

Этот набор утилит — ваш надежный помощник в мире Linux-операций. Забудьте о часах, потраченных на поиск нужного скрипта или команды. Здесь все собрано в одном месте: от быстрой диагностики системы до тонкой настройки и рутинного обслуживания. **Установите один раз и получите швейцарский нож для админа!**

## Что внутри? (Коротко и ясно)

*   **Linux Triage**: Быстрый аудит системы, поиск самых “тяжелых” файлов, мониторинг процессов (через `/proc`).
*   **KESL Logs**: Анализ больших логов KESL без нагрузки на память.
*   **Network/SSL**: Проверка доступности портов без `netcat`, а также набор скриптов для работы с OpenSSL.
*   **DB Helper**: Проверка состояния баз данных и выявление медленных SQL-запросов из логов.
*   **Routine**: Мелкие, но важные регламентные операции: проверка доступности URL, очистка логов, бэкап конфигураций.
*   **Logs Maintenance**: Единая команда для архивирования старых логов и удаления совсем устаревших.

## Быстрый старт

### Для Windows / PowerShell

```powershell
cd c:\Users\N7\Documents\GitHub\enterprise-linux-ops-toolkit
py -m pip install -e .
py -m elotoolkit.cli --help
```

### Для Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
elot --help
```

## Примеры команд для реальной работы

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

## Если нужен “старый добрый” способ

Оригинальные shell-скрипты на месте, их можно запускать напрямую:

```bash
sudo bash modules/linux_triage/bin/quick_audit.sh
bash modules/linux_triage/bin/find_heavy_files.sh /var/log
sudo bash modules/kesl_log_analyzer/bin/log_rotate.sh
```

## Структура проекта

```
enterprise-linux-ops-toolkit/
  modules/                 # Оригинальные скрипты (bash/python)
  src/elotoolkit/          # Python-пакет с CLI-интерфейсом
  pyproject.toml