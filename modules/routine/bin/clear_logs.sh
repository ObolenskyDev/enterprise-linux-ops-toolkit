#!/bin/bash
# ==========================================
# Script: Log Cleaner (Enterprise Edition)
# Description: Removes old logs with path flexibility.
# ==========================================

if [[ $EUID -ne 0 ]]; then
   echo "⛔ Ошибка: Запустите скрипт через sudo"
   exit 1
fi

LOG_DIR=${1:-"/var/log/myapp"}
DAYS=${2:-7}

echo "[INFO] Cleaning logs in $LOG_DIR older than $DAYS days..."

if [ ! -d "$LOG_DIR" ]; then
    echo "❌ Ошибка: Директория $LOG_DIR не найдена."
    exit 1
fi

COUNT=$(find "$LOG_DIR" -name "*.log" -mtime +$DAYS | wc -l)

if [ "$COUNT" -gt 0 ]; then
    find "$LOG_DIR" -name "*.log" -mtime +$DAYS -delete
    echo "✅ Успех: Удалено файлов: $COUNT"
else
    echo "ℹ️ Старых логов не обнаружено."
fi

