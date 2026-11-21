# Рома — Капитан + Vulnbox/Защита (личный гайд с нуля)

Ты владеешь Ubuntu-серваком (vulnbox). Задача — чтобы сервисы не падали. Окно 10:00–10:40 — твоё главное время.

## Что скачать (на серваке)
```bash
sudo apt update && sudo apt install -y tmux tcpdump git nftables
```

## Шаги 10:00–10:40 (подробно — ../02_defense.md)
### 1. Закрыть вход
```bash
passwd; sudo passwd root
rm -f ~/.ssh/authorized_keys /root/.ssh/authorized_keys
```
Собери публичные ключи всех пятерых (каждый делает ssh-keygen и шлёт тебе ~/.ssh/id_ed25519.pub) и добавь в ~/.ssh/authorized_keys.
### 2. Выключить парольный SSH (ГЛАВНОЕ)
```bash
sudo nano /etc/ssh/sshd_config   # PasswordAuthentication no ; PermitRootLogin prohibit-password
sudo grep -rniE 'passwordauth|permitroot' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
sudo systemctl restart ssh
sudo sshd -T | grep -i passwordauthentication   # должно: no
```
### 3. Найти сервисы и БЭКАП (до сети!)
```bash
ss -tulpn; systemctl list-units --type=service; ls -la /opt /srv /home
./scripts/backup.sh /opt/service1 service1
scp -r /backups <ты>@<своя_kali>:~/backups
```
### 4. Закрыть БД на localhost (../02_defense.md)
### 5. Сервисы под git
```bash
cd /opt/service1 && git init -q && git add -A && git commit -qm round0
```

## Во время игры
- Принимаешь патчи от Паши, следишь что чекеры зелёные.
- Сервис упал — поднимаешь (из бэкапа если надо).
- Координируешь: кто что патчит.

## Чеклист
- [ ] пароли, ключи, парольный SSH off (проверен)
- [ ] бэкап всех сервисов + копия на Kali
- [ ] БД на localhost, чекеры зелёные
