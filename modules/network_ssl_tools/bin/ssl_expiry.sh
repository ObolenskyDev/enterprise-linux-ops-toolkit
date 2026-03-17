#!/bin/bash
# Проверка срока действия SSL/TLS сертификата на удаленном хосте.
# Используется для диагностики проблем подключения агентов KSC и консолей.
#
# Использование: ./ssl_expiry.sh <host> <port>

HOST=$1
PORT=${2:-443}

if [ -z "$HOST" ]; then
    echo "Использование: $0 <хост> [порт]"
    echo "Пример: $0 ksc.server.local 13291"
    exit 1
fi

echo "--- [SSL] Проверка сертификата: $HOST:$PORT ---"

END_DATE=$(timeout 5 openssl s_client -servername "$HOST" -connect "$HOST:$PORT" 2>/dev/null | openssl x509 -noout -enddate)

if [ -z "$END_DATE" ]; then
    echo "[ОШИБКА] Не удалось получить сертификат."
    echo "Возможные причины: порт закрыт, сервис остановлен или это не SSL порт."
    exit 1
fi

DATE_STR=$(echo "$END_DATE" | cut -d= -f2)
echo "Дата истечения: $DATE_STR"

EXP_EPOCH=$(date -d "$DATE_STR" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXP_EPOCH - $NOW_EPOCH) / 86400 ))

if [ "$DAYS_LEFT" -lt 30 ]; then
    echo "[ВНИМАНИЕ] ⚠️ Сертификат истекает через $DAYS_LEFT дней! Требуется обновление."
else
    echo "[OK] ✅ Сертификат валиден еще $DAYS_LEFT дней."
fi

