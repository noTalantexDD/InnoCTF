# Шпаргалка команд

## SSH / файлы
```bash
ssh ubuntu@10.60.7.2                 # зайти на сервак
ssh-keygen -t ed25519                # ключ
ssh-copy-id ubuntu@10.60.7.2         # ключ на сервак
scp -r ubuntu@10.60.7.2:/opt/svc ./  # скачать с сервака
scp f.py ubuntu@10.60.7.2:/tmp/      # закинуть на сервак
```
## Защита
```bash
ss -tulpn
systemctl list-units --type=service
sudo sshd -T | grep -i password
./scripts/backup.sh /opt/svc svc
```
## Трафик
```bash
sudo ./scripts/capture.sh "port 80 or port 5000"
tcpdump -r d.pcap -A | grep -E '[A-Z0-9]{31}='
```
## Поиск багов
```bash
grep -rniE "exec|system|eval|pickle|subprocess" .
grep -rniE "secret|token|password|admin" .
```
## attack_data / ферма
```bash
curl -s http://<host>/api/client/attack_data | jq .
```
## tmux
```bash
tmux new -s work   # Ctrl+b d — отцепиться ; tmux attach -t work
```
## Патч
```bash
cd /opt/svc && git add -A && git commit -m "patch"
sudo systemctl restart <сервис>   # потом проверь чекер!
```
Флаг: `[A-Z0-9]{31}=` (уточнить на /serp)
