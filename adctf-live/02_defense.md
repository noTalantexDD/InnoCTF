# Защита без докера (всё локально)

Докера нет — сервисы это локальные процессы/systemd и файлы. Делает Рома на серваке.

## 1. Закрыть вход (пароль + SSH)
```bash
passwd; sudo passwd root
rm -f ~/.ssh/authorized_keys /root/.ssh/authorized_keys
# добавить публичные ключи всех пятерых в ~/.ssh/authorized_keys
sudo nano /etc/ssh/sshd_config   # PasswordAuthentication no ; PermitRootLogin prohibit-password
sudo grep -rniE 'passwordauth|permitroot' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
sudo systemctl restart ssh
sudo sshd -T | grep -i passwordauthentication   # должно: no
```

## 2. Найти сервисы
```bash
ss -tulpn
systemctl list-units --type=service
ls -la /opt /srv /home /var/www
cat /etc/systemd/system/*.service
```

## 3. Бэкап каждого сервиса (ДО сети!)
```bash
./scripts/backup.sh /opt/service1 service1
scp -r /backups <ты>@<своя_kali>:~/backups
sudo -u postgres pg_dumpall > /backups/pg.sql        # postgres
mysqldump -u root -p --all-databases > /backups/mysql.sql  # mysql
```

## 4. Закрыть БД на localhost
```
Postgres  postgresql.conf : listen_addresses = 'localhost'
MySQL     *.cnf           : bind-address = 127.0.0.1
Redis     redis.conf      : bind 127.0.0.1
Mongo     mongod.conf     : bindIp: 127.0.0.1
```
`sudo systemctl restart postgresql` (или mysql/redis/mongod).

## 5. Фаервол (nftables)
НЕ блокируй атакующих (чекер с того же диапазона). Закрывай только служебное:
```
#!/usr/sbin/nft -f
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    iif lo accept
    ct state established,related accept
    tcp dport 22 ip saddr 10.0.0.0/8 accept
    tcp dport { 80, 443, 5000 } accept
    ip protocol icmp accept
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output  priority 0; policy accept; }
}
```
`sudo nft -f /etc/nftables.conf`. Не отрежь себе SSH.

## 6. Дефолтные креды
admin/admin — поменять, НО сначала проверь, не ходит ли чекер под ними.

## Чеклист
- [ ] пароли/ключи/парольный SSH off (проверен)
- [ ] бэкап всех + копия на Kali
- [ ] БД на localhost, фаервол, чекеры зелёные
