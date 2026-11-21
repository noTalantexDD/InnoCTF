# Ферма флагов — DestructiveFarm (без докера)

Держит Саша А. Ферма запускает эксплойты по всем командам, собирает флаги из stdout и сдаёт пачками в ForcAD.

## Почему DestructiveFarm
S4DFarm — только через Docker, а докера нет. DestructiveFarm запускается без докера. ForcAD поддерживается.

## Установка (сегодня, с интернетом)
```bash
git clone https://github.com/DestructiveVoice/DestructiveFarm
cd DestructiveFarm/server
python3 -m pip install -r requirements.txt
```
> Перед игрой удали старую базу: `rm -f flags.sqlite`.

## Запуск (в tmux!)
```bash
tmux new -s farm
cd DestructiveFarm/server
./start_server.sh            # веб-морда обычно http://127.0.0.1:5000
# Ctrl+b затем d — отцепиться
```

## Конфиг (server/config.py) — ВПИСАТЬ НА ИГРЕ
- протокол ForcAD (в `server/protocols/` есть forcad; сабмит по TCP — нужен host и port сервера жюри).
- team token вашей команды.
- формат флага: `[A-Z0-9]{31}=`.
- SUBMIT_PERIOD (2–5 сек), SUBMIT_FLAG_LIMIT (напр. 100).
- FLAG_LIFETIME = 5 раундов (~10 мин).
- SERVER_PASSWORD — сменить с дефолта.
> Точные имена полей короткие — смотри сам файл server/config.py. Адрес/порт и token — у оргов / на /serp.

## Запуск эксплойта под фермой
```bash
cd DestructiveFarm
python3 client/start_sploit.py path/to/sploit.py -u http://127.0.0.1:5000
```
Контракт: argv[1] = IP жертвы; флаги в stdout с flush.

## Контроль
Веб-морда: флаги ACCEPTED. INVALID → проверь токен/протокол/формат. Упала — перезапуск в tmux. Запасной: ../scripts/submit_min.py.
