#!/bin/bash
# Поиск самых тяжелых файлов в указанной директории.
# Помогает быстро найти разросшиеся логи (KSC, System) или кор-дампы.
# Использование: ./find_heavy_files.sh <путь>

SEARCH_PATH=${1:-/var/log}

echo "--- Анализ дискового пространства в: $SEARCH_PATH ---"
echo "Топ-10 самых больших файлов:"

if [ ! -d "$SEARCH_PATH" ]; then
    echo "Ошибка: Директория $SEARCH_PATH не существует."
    exit 1
fi

# find: ищем только файлы (-type f)
# du -ah: показываем размер в читаемом виде
# sort -hr: сортируем (h-human numeric, r-reverse)
# head: берем топ 10
# 2>/dev/null: скрываем ошибки доступа

find "$SEARCH_PATH" -type f -exec du -ah {} + 2>/dev/null | sort -hr | head -n 10

echo "---------------------------------------------------"
echo "Совет: Для очистки логов используйте logrotate или > file.log"

