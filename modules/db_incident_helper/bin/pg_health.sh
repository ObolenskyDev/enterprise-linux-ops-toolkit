#!/bin/bash
# Скрипт проверки состояния СУБД (PostgreSQL/MariaDB).
# Выполняет диагностику: статус сервиса, доступность портов, место на диске.

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "--- [DB] Диагностика СУБД ---"

SERVICE=$(systemctl list-units --type=service --state=running | grep -E 'postgres|mariadb|mysql' | awk '{print $1}' | head -n 1)

if [ -z "$SERVICE" ]; then
    echo -e "${RED}❌ [СЕРВИС] Активный сервис БД не найден!${NC}"
    echo "   Совет: Проверьте вывод 'systemctl list-units --all | grep postgres'"
else
    echo -e "${GREEN}✅ [СЕРВИС] Обнаружен сервис: $SERVICE${NC}"
    systemctl status "$SERVICE" --no-pager | grep "Active:" | xargs
fi

echo -e "\n--- [СЕТЬ] Проверка портов ---"
if ss -tuln | grep -E ':5432|:3306' > /dev/null; then
    echo -e "${GREEN}✅ Порт доступен (5432/3306)${NC}"
    ss -tuln | grep -E ':5432|:3306' | awk '{print "   " $5}'
else
    echo -e "${RED}❌ Стандартные порты (5432/3306) недоступны.${NC}"
fi

DATA_DIR="/var/lib/postgresql"

echo -e "\n--- [ДИСК] Проверка хранилища ($DATA_DIR) ---"
if [ -d "$DATA_DIR" ]; then
    df -h "$DATA_DIR" | awk 'NR==2 {print "Всего: " $2 " | Занято: " $3 " | Доступно: " $4}'
    SIZE=$(du -sh "$DATA_DIR" 2>/dev/null | awk '{print $1}')
    echo "   Размер директории БД: $SIZE"
else
    echo "⚠️  Каталог $DATA_DIR не найден (возможно, используется нестандартный путь)."
fi

