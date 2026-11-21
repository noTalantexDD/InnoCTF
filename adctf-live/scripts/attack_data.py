#!/usr/bin/env python3
"""
Тянет attack_data из ForcAD. python3 attack_data.py [service_name]
Адрес уточнить на /serp.
"""
import sys, json, requests

URL = "http://<host>/api/client/attack_data"

def main():
    data = requests.get(URL, timeout=8).json()
    if len(sys.argv) > 1:
        print(json.dumps(data.get(sys.argv[1], {}), ensure_ascii=False, indent=2))
    else:
        for svc in data:
            print(svc, "->", len(data[svc]), "teams")

if __name__ == "__main__":
    main()
