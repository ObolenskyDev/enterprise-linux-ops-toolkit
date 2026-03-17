#!/bin/bash
# ==========================================
# Script: Config Backup Utility
# Description: Creates versioned archives of configs.
# ==========================================

if [[ $EUID -ne 0 ]]; then
   echo "⛔ Ошибка: Для бэкапа /etc/ необходимы права sudo"
   exit 1
fi

SOURCE=${1:-"/etc/nginx"}
BACKUP_DIR=${2:-"$HOME/backups"}
DATE=$(date +%Y-%m-%d_%H-%M)
NAME=$(basename "$SOURCE")
ARCHIVE_NAME="${NAME}_config_$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "[INFO] Archiving $SOURCE to $BACKUP_DIR..."

if tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" "$SOURCE" 2>/dev/null; then
    echo "✅ Бэкап создан: $ARCHIVE_NAME"
    echo "📍 Путь: $BACKUP_DIR"
else
    echo "❌ Ошибка при создании бэкапа. Проверьте путь: $SOURCE"
    exit 1
fi

