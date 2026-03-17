#!/bin/bash
# Утилита для сверки пары "Сертификат + Приватный ключ".
# Сравнивает MD5 хеши модулей файлов.
# Если хеши разные — веб-сервер или KSC не запустится с ошибкой SSL.

CERT=$1
KEY=$2

if [ -z "$CERT" ] || [ -z "$KEY" ]; then
    echo "Использование: $0 <certificate.crt> <private.key>"
    exit 1
fi

echo "--- [PKI] Сверка пары ключей ---"

CRT_MOD=$(openssl x509 -noout -modulus -in "$CERT" 2>/dev/null | openssl md5)
KEY_MOD=$(openssl rsa -noout -modulus -in "$KEY" 2>/dev/null | openssl md5)

if [ -z "$CRT_MOD" ] || [ -z "$KEY_MOD" ]; then
    echo "[ОШИБКА] Не удалось прочитать файлы. Проверьте пути и формат."
    exit 1
fi

echo "MD5 Сертификата: $CRT_MOD"
echo "MD5 Ключа:       $KEY_MOD"

if [ "$CRT_MOD" == "$KEY_MOD" ]; then
    echo "✅ РЕЗУЛЬТАТ: Файлы СООТВЕТСТВУЮТ друг другу."
else
    echo "⛔ РЕЗУЛЬТАТ: Хеши НЕ СОВПАДАЮТ! Ключ не подходит к сертификату."
fi

