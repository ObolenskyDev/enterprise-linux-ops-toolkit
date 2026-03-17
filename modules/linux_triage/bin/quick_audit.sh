#!/bin/bash
# Скрипт быстрого аудита системы для отчета по инциденту.
# Собирает Load Average, Память, Диски и статус KESL.
# Запускать лучше через sudo.

# Создаем папку для логов
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# Формируем имя файла внутри папки
LOG_FILE="$LOG_DIR/audit_$(date +%Y%m%d_%H%M).txt"

echo "Запуск диагностики..." | tee -a "$LOG_FILE"

# 1. Информация об ОС и Ядре
echo "--- ИНФО О СИСТЕМЕ ---" >> $LOG_FILE
uname -a >> $LOG_FILE
if [ -f /etc/os-release ]; then
    grep PRETTY_NAME /etc/os-release >> $LOG_FILE
fi

# 2. Load Average (Нагрузка)
echo -e "\n--- ЗАГРУЗКА (UPTIME & LOAD) ---" >> $LOG_FILE
uptime >> $LOG_FILE

# 3. Оперативная память
echo -e "\n--- ПАМЯТЬ (MB) ---" >> $LOG_FILE
# Конвертируем KB в MB для читаемости
grep -E 'MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree' /proc/meminfo | awk '{print $1, $2/1024 " MB"}' >> $LOG_FILE

# 4. Дисковая подсистема
echo -e "\n--- ДИСКИ (МЕСТО) ---" >> $LOG_FILE
df -hT | grep -v "tmpfs" >> $LOG_FILE
echo "Иноды (Inodes):" >> $LOG_FILE
df -i | grep -v "tmpfs" >> $LOG_FILE

# 5. Топ процессов по CPU
echo -e "\n--- ТОП 5 ПРОЦЕССОВ (CPU) ---" >> $LOG_FILE
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6 >> $LOG_FILE

# 6. Проверка сервисов Лаборатории Касперского (KESL)
echo -e "\n--- СТАТУС KESL ---" >> $LOG_FILE
# Ищем процессы kesl (обычно kesl, wdserver, klnagent)
if pgrep -f "kesl" > /dev/null; then
    echo "[OK] Процессы KESL обнаружены:" >> $LOG_FILE
    ps -eo pid,user,cmd | grep kesl | grep -v grep >> $LOG_FILE
else
    echo "[ВНИМАНИЕ] Процессы KESL НЕ найдены!" >> $LOG_FILE
fi

# 7. Зомби-процессы
ZOMBIES=$(ps aux | awk '{print $8}' | grep -c 'Z')
echo -e "\n--- ЗОМБИ ПРОЦЕССЫ: $ZOMBIES ---" >> $LOG_FILE
if [ "$ZOMBIES" -gt 0 ]; then
    ps -eo stat,ppid,pid,cmd | grep -w Z >> $LOG_FILE
fi

echo "Аудит завершен. Отчет сохранен в $LOG_FILE"

