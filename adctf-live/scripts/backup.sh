#!/usr/bin/env bash
# Бэкап сервиса (без докера): код + дамп БД. На серваке ДО сети.
# Использование: ./backup.sh <путь_к_сервису> <имя>
set -euo pipefail
SRC="${1:?путь к сервису}"; NAME="${2:?имя}"
DEST="/backups/${NAME}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEST"
tar czf "$DEST/code.tgz" -C "$(dirname "$SRC")" "$(basename "$SRC")"
if command -v pg_dumpall >/dev/null 2>&1; then sudo -u postgres pg_dumpall > "$DEST/pg.sql" 2>/dev/null || true; fi
if command -v mysqldump >/dev/null 2>&1; then mysqldump -u root --all-databases > "$DEST/mysql.sql" 2>/dev/null || true; fi
echo "[OK] бэкап в $DEST"
echo "!!! Скопируй на свою Kali через scp"
