# Attack-Defense CTF · шпаргалка на старт (9:00–10:40)

Сводная версия: игровые параметры с инструктажа (адреса, ForcAD, прокси, тайминг) + дисциплина бэкап→правка→проверка→откат + таблица диагностики.

`X` — номер вашей команды. `LOGIN` — логин на vulnbox. Заглавные слова в примерах — заменить реальными значениями.

## Карта сети и параметры игры

| Что | Значение |
|---|---|
| Командная сеть | `10.2.X.0/24` |
| Свой vulnbox | `10.2.X.2` |
| Командный шлюз (с него идут все атаки) | `10.2.X.1` |
| Jury / ForcAD | `10.10.10.10:80` |
| Данные для атак (ForcAD) | `10.10.10.10/api/client/attack_data` |
| HTTP-прокси площадки | `10.10.10.10:8080` (только GET, ограниченный список сайтов) |
| Сертификат прокси | `10.10.10.10:8080/cert` |
| Длина раунда | 2 минуты |
| Flag lifetime | 5 раундов (~10 минут) |
| Флагов на уязвимость | 2 |

**Важно:** трафик атак идёт со шлюза `10.2.X.1` — не блокировать его и `10.10.10.10`. Не ломать работоспособность своих сервисов ради обороны — упавший сервис стоит очков больше, чем пропущенная атака.

## Тайминг дня

| Время | Фаза |
|---|---|
| 9:00–10:00 | Настройка рабочих ПК |
| 10:00–10:40 | Выдача vulnbox, сеть закрыта |
| 10:40–13:00 | Сеть открыта |
| 13:00–14:00 | Сеть закрыта, обед |
| 14:00–16:30 | Сеть открыта |
| 16:30–17:00 | Скорборд закрыт |
| 17:00 | Конец игры |

## Если осталось 5 минут

- [ ] Новая SSH-сессия по ключу + `sudo -v`, старую не закрывать.
- [ ] Штатный `curl` по каждому сервису из таблицы — сверить с ответом "до правок".
- [ ] Хеши бэкапов сверены, копии лежат и на vulnbox, и локально.
- [ ] Открыт Jury, назначен ответственный за первый красный статус.
- [ ] Если последняя правка что-то сломала — откатить именно её, не всё подряд.

---

## 9:00–10:00. Рабочий ПК (Kali)

```bash
passwd
systemctl is-active ssh          # должно быть inactive — свой SSH-сервер не нужен
ssh-keygen -t ed25519 -f ~/.ssh/ctf_ed25519 -C "$(whoami)-ctf"
ssh -V; curl --version
```

- Собрать `.pub`-ключи всех участников в один файл `team_keys.pub`.
- Прокси и сертификат:
  ```bash
  curl -o proxy-ca.crt http://10.10.10.10:8080/cert
  sudo cp proxy-ca.crt /usr/local/share/ca-certificates/ctf-proxy.crt
  sudo update-ca-certificates
  ```
  Firefox/Burp используют своё хранилище сертификатов — туда ставить отдельно.
- Скачать заранее пакеты и колёса для vulnbox (сеть там закрыта до 10:40): `tmux git rsync tcpdump tcpflow ripgrep python3-pip`, нужные Python-библиотеки (`pip download -d ./wheels ...`).
- Распределить роли:
  - ответственный за SSH/доступ — держит откатную сессию;
  - ответственный(е) за инвентарь сервисов и бэкапы;
  - остальные сразу читают исходники сервисов на уязвимости и готовят эксплойты/раннер для атаки.

---

## 10:00–10:12. SSH — без потери доступа

**Сохранить рабочую сессию, не закрывать:**
```bash
ssh LOGIN@10.2.X.2
whoami; id; passwd; sudo -v
```

**Добавить ключи, проверить, потом чистить лишние:**
```bash
ssh-copy-id -i ~/.ssh/ctf_ed25519.pub LOGIN@10.2.X.2
# в НОВОМ терминале, старый не закрывать:
ssh -i ~/.ssh/ctf_ed25519 -o IdentitiesOnly=yes -o PreferredAuthentications=publickey LOGIN@10.2.X.2
```

Перед чисткой `authorized_keys` — обязательно копия:
```bash
sudo cp -a ~/.ssh/authorized_keys ~/.ssh/authorized_keys.before
```
Сверить отпечатки, чтобы не выкинуть чужой легитимный ключ команды:
```bash
ssh-keygen -lf ~/.ssh/ctf_ed25519.pub     # у себя
ssh-keygen -lf authorized_keys            # на сервере
```

**Отключить пароли, с учётом Match-блоков:**
```bash
sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.before
sudo sshd -T | grep -Ei 'passwordauth|pubkeyauth|kbdinter|permitroot'
sudo grep -ni -E '^\s*(include|match)\b' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null
```
```bash
sudo tee /etc/ssh/sshd_config.d/00-hardening.conf <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
EOF
sudo sshd -t && sudo systemctl reload ssh
```
Если найден `Match` — проверить итог именно для своего пользователя/IP:
```bash
sudo sshd -T -C user=LOGIN,addr=<IP_вашего_ПК>,laddr=10.2.X.2,lport=22 | grep -Ei 'passwordauth|pubkeyauth'
```

**Проверка (новая сессия, старую не закрывать):**
```bash
ssh -i ~/.ssh/ctf_ed25519 LOGIN@10.2.X.2
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password LOGIN@10.2.X.2   # должен быть отказ без запроса пароля
```

**Если сломалось:** из старой сессии —
```bash
sudo cp -a /etc/ssh/sshd_config.before /etc/ssh/sshd_config && sudo systemctl reload ssh
sudo cp -a ~/.ssh/authorized_keys.before ~/.ssh/authorized_keys
```

Попутно проверить закладки:
```bash
last -n 20; w
sudo ls -la /etc/cron* /var/spool/cron/crontabs; systemctl list-timers --all
sudo find / -perm -4000 -type f 2>/dev/null
```

---

## 10:12–10:25. Инвентарь сервисов

```bash
sudo ss -lntup
systemctl --type=service --state=running --no-pager
sudo docker ps -a; sudo docker compose ls 2>/dev/null
```

`127.0.0.1` — слушает только локально, `0.0.0.0` / `[::]` — снаружи. Для Docker отдельно смотреть проброшенный порт (`0.0.0.0:8080->80/tcp`).

Таблица на команду — завести сразу, заполнять по ходу:

| Сервис | Порт | Юнит/контейнер | Код/конфиг | Данные | Штатная проверка | Кто отвечает |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Штатная проверка с рабочего ПК (зафиксировать ответ **до** правок):
```bash
curl --noproxy '*' -sS -i --max-time 5 "http://10.2.X.2:PORT/путь"
```

Лишние порты — закрывать `ufw`, но `ufw` не видит Docker-контейнеры, для них `DOCKER-USER`:
```bash
sudo ufw allow 22/tcp && sudo ufw deny <порт>/tcp && sudo ufw enable
sudo iptables -I DOCKER-USER -p tcp --dport <порт> -j DROP   # для контейнерных сервисов
```

---

## 10:25–10:35. Бэкапы и первые правки

```bash
umask 077; mkdir -p ~/ad-backup
archive=~/ad-backup/<сервис>-before.tar.gz
sudo tar -C /opt -czf - <сервис> > "$archive" && tar -tzf "$archive" >/dev/null && sha256sum "$archive"
```

Скачать себе и свериться:
```bash
scp -i ~/.ssh/ctf_ed25519 LOGIN@10.2.X.2:ad-backup/<сервис>-before.tar.gz ./ad-backup/
sha256sum ./ad-backup/<сервис>-before.tar.gz   # сравнить с выводом на сервере
```

БД:
```bash
pg_dump -Fc -d DBNAME > backup.dump && pg_restore -l backup.dump   # проверка, что архив читается
sqlite3 /path/app.db ".backup '/path/backup.db'"                   # не копировать файл напрямую из-за WAL
```

**Порядок правки одного сервиса:**
1. Зафиксировать текущий статус и штатный ответ.
2. Скопировать правимый файл (`*.before`).
3. Одна небольшая правка.
4. Штатная проверка конфига, если есть у сервиса.
5. Применить, перезапустить, проверить с ПК и свежие логи.
6. При сбое — откатить именно эту правку, не всё подряд.

**Параллельно (кто не в обороне):** читать исходники сервисов на уязвимости (инъекции, авторизация, отладочные ручки), готовить эксплойты под чужие vulnbox и раннер, который раз в раунд (2 мин) тянет `10.10.10.10/api/client/attack_data` и атакует все команды. Флаг живёт 5 раундов (~10 минут) — раннер должен быть быстрым и устойчивым к падениям. Точный способ сдачи флагов уточнить у организаторов, не угадывать endpoint заранее.

---

## 10:35–10:40. Финальный прогон

- [ ] Вход по ключу подтверждён в новой сессии у каждого участника.
- [ ] Пароль по SSH отключён и проверен отдельно (с учётом `Match`, если был).
- [ ] Сервисы из таблицы отвечают так же, как до правок.
- [ ] Бэкапы скачаны, хеши сверены.
- [ ] Открыт Jury, назначен ответственный за первый красный статус.

## Диагностика

| Симптом | Что проверить первым |
|---|---|
| SSH таймаутит | сеть/IP/порт, затем `ss -lntup` через консоль |
| `Permission denied (publickey)` | логин, выбранный ключ, права на `authorized_keys`, `AuthorizedKeysFile`/`Match` |
| `sshd -t` ок, но вход после reload пропал | вернуть `.before`-копию, reload, повторить |
| Локально HTTP работает, с ПК — нет | адрес прослушивания, проброс порта Docker |
| HTTP жив, у Jury красный | полный сценарий целиком и логи за время проверки, время последней правки |
| Бэкап есть только на vulnbox | скачать `scp`, сверить хеш, записать локальный путь |
