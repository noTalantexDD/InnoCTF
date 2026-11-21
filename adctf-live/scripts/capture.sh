#!/usr/bin/env bash
# Ротационный захват трафика. На серваке в 10:00, в tmux.
# Использование: sudo ./capture.sh "port 80 or port 5000"
set -euo pipefail
FILTER="${1:-tcp and not port 22}"
OUT=/data/pcap
mkdir -p "$OUT"
echo "[*] tcpdump -> $OUT, фильтр: $FILTER"
exec tcpdump -i any -s 0 -Z root -w "$OUT/d_%Y%m%d_%H%M%S.pcap" -G 300 -W 288 $FILTER
