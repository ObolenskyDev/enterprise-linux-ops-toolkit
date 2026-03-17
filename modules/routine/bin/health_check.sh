#!/bin/bash
# ==========================================
# Script: API Health Check
# Description: L7 uptime monitoring for services.
# ==========================================

URLS=(
    "https://google.com"
    "http://localhost:8080/api/v1/status"
)

echo "--- [MONITORING] Starting Health Check ---"

for URL in "${URLS[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$URL")

    if [ "$STATUS" -eq 200 ]; then
        echo -e "✅ [200 OK] $URL"
    elif [ "$STATUS" -eq 000 ]; then
        echo -e "❌ [TIMEOUT/DNS] $URL is unreachable"
    else
        echo -e "⚠️ [ERROR] $URL returned status: $STATUS"
    fi
done

echo "--- Check Finished ---"

