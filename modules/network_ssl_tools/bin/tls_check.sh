#!/bin/bash
# Проверка поддерживаемых версий TLS (1.2, 1.3).
# Необходим для диагностики проблем совместимости старых клиентов (Legacy) и новых серверов.

HOST=$1
PORT=${2:-443}

if [ -z "$HOST" ]; then
    echo "Использование: $0 <хост> [порт]"
    exit 1
fi

echo "--- [TLS] Анализ протоколов для $HOST:$PORT ---"

echo -n "TLS 1.2: "
if echo | timeout 3 openssl s_client -connect "$HOST:$PORT" -servername "$HOST" -tls1_2 2>/dev/null | grep -q "Cipher"; then
    echo "✅ ПОДДЕРЖИВАЕТСЯ"
else
    echo "❌ Отключен или не поддерживается"
fi

echo -n "TLS 1.3: "
if echo | timeout 3 openssl s_client -connect "$HOST:$PORT" -servername "$HOST" -tls1_3 2>/dev/null | grep -q "Cipher"; then
    echo "✅ ПОДДЕРЖИВАЕТСЯ"
else
    echo "❌ Отключен или не поддерживается"
fi

