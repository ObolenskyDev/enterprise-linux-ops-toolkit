#!/bin/bash
# Скрипт ротации и очистки старых логов KESL.
# Сжимает логи старше 7 дней, удаляет архивы старше 30 дней.

LOG_DIR="./logs" # Работаем в локальной папке для безопасности теста

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}--- [MAINTENANCE] Обслуживание логов ---${NC}"

# Проверка директории
if [ ! -d "$LOG_DIR" ]; then
    echo "Папка $LOG_DIR не найдена. Создаю демо-структуру..."
    mkdir -p "$LOG_DIR"
    # Создаем фейковые старые логи для теста
    touch "$LOG_DIR/trace.log"
    touch "$LOG_DIR/old_trace.log.2025-12-01"
fi

# 1. Архивация
echo "📦 Сжатие старых логов..."
count=0
# В боевой среде тут было бы: find $LOG_DIR -mtime +7 ...
for file in "$LOG_DIR"/*; do
    if [[ -f "$file" && "$file" != *.gz && "$file" != *"kesl_trace.log"* ]]; then
        echo "   Gzipping: $file"
        gzip -f "$file"
        ((count++))
    fi
done
echo -e "${GREEN}✅ Сжато файлов: $count${NC}"

# 2. Очистка
echo "🗑️  Удаление старых архивов (>30 дней)..."
# Демонстрация команды (Dry Run)
echo "   [DRY RUN] find $LOG_DIR -name '*.gz' -mtime +30 -delete"

echo -e "${GREEN}✅ Ротация завершена.${NC}"

