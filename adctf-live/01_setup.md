# Настройка машин и SSH с нуля

Для тех, кто никогда не работал с SSH.

## Словарик
- **SSH** — зайти со своей Kali в терминал сервака.
- **сервак** — Ubuntu с сервисами, управляем по SSH.
- **ключ** — приватный + публичный. Безопаснее пароля.

## 1. Софт на Kali
`sudo apt install -y tmux tcpdump tshark ngrep curl jq python3-pip git nmap` ; `pip3 install requests pwntools`

## 2. Сертификат
Открыть `http://<...>/serp`, выполнить скрипт. Интернет только GET.

## 3. SSH с нуля
- IP сервака дадут орги (напр. 10.60.7.2).
- Вход: `ssh ubuntu@10.60.7.2` → yes → пароль. Выйти: `exit`.
- Ключ: `ssh-keygen -t ed25519` (Enter на всё).
- Ключ на сервак: `ssh-copy-id ubuntu@10.60.7.2`.
- scp: `scp -r ubuntu@10.60.7.2:/opt/service1 ./` ; `scp patch.py ubuntu@10.60.7.2:/tmp/`.
- Команды: `ls -la`, `cd`, `cat file`, `nano file`, `grep -rni "x" .`
- tmux: `tmux new -s work`; Ctrl+b d; `tmux attach -t work`.
> Все 5 делают ключ. Потом Рома выключит парольный вход (02_defense.md).

## 4. Софт на сервак (Рома)
`sudo apt install -y tmux tcpdump git nftables`

## 5. Кто что ставит
Все: п.1+серт+ключ. Саша А: DestructiveFarm. Саша Ф: Tulip. Подробно — roles/.
