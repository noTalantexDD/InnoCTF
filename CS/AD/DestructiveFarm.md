# настройка
```bash
cd server
python3 -m venv .venv
source .venv/bin/activate # выйти из окружения deactivate
python3 -m pip install -r requirements.txt
```
на innoctf такой шаблон
```python
CONFIG = {
    'TEAMS': {'Team #{}'.format(i): '10.2.{}.2'.format(i)
              for i in range(1, 16+1) if i != 1337}, # уточнение
    'FLAG_FORMAT': r'FLAG{[A-Z0-9a-z]*}', # уточнение

    'SYSTEM_PROTOCOL': 'forcad_tcp',
    'SYSTEM_HOST': '10.10.10.10',
    'SYSTEM_PORT': 80, # уточнение
    'TEAM_TOKEN': 'YOUR_TEAM_TOKEN', # уточнение

    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 2 * 60,

    'SERVER_PASSWORD': 'CHANGE_ME_PASSWORD',

    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}
```
# Запуск
```bash
rm -f flags.sqlite
./start_server.sh
```
Веб-интерфейс со статистикой и очередью флагов поднимется по умолчанию на порту `5000`. Конфиг `config.py` можно править на лету во время игры — сервер подхватывает изменения автоматически
```bash
cd DestructiveFarm/client
chmod +x ../path/to/sploit.py
python3 start_sploit.py ../path/to/sploit.py -u http://<IP_сервера>:5000 --token <ВАШ_ПАРОЛЬ> --attack-period 60
```

- `--attack-period` — раз в сколько секунд запускать новый раунд атак (обычно ставят равным длительности раунда/тика или чуть меньше).
- на inno ставим 60
