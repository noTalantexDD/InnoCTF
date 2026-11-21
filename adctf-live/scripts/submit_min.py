#!/usr/bin/env python3
"""
Запасной сабмиттер флагов в ForcAD (TCP). Проверь host/port/протокол на /serp.
Флаги из stdin или файла: cat flags.txt | python3 submit_min.py
"""
import sys, re, socket, time

HOST = "<submit_host>"
PORT = 31337
TEAM_TOKEN = "<TOKEN>"
FLAG_RE = re.compile(r'[A-Z0-9]{31}=')

def read_flags():
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    return list(dict.fromkeys(FLAG_RE.findall(src.read())))

def main():
    flags = read_flags()
    print(f"flags: {len(flags)}", file=sys.stderr)
    try:
        s = socket.create_connection((HOST, PORT), timeout=10)
        # некоторые ForcAD ждут токен первой строкой:
        # s.sendall((TEAM_TOKEN + "\n").encode())
        for f in flags:
            s.sendall((f + "\n").encode()); time.sleep(0.05)
        print(s.recv(65535).decode(errors="replace"), file=sys.stderr)
        s.close()
    except Exception as e:
        print("submit error:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
