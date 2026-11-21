#!/usr/bin/env bash
# Что торчит наружу. Сервис (оставить) / внутреннее (на localhost).
set -euo pipefail
echo "=== Слушающие сокеты ==="
ss -tulpn 2>/dev/null || sudo ss -tulpn
echo; echo "=== systemd-сервисы ==="
systemctl list-units --type=service --state=running | head -40
echo
echo " - 0.0.0.0:<БД/redis/mongo> -> перебиндить на 127.0.0.1"
echo " - порт сервиса -> оставить"
echo " - SSH (22) -> только своей сети"
