# Саша Ф — Дампщик/Трафик (личный гайд с нуля)

Ты смотришь трафик и приносишь команде готовые атаки и дыры. Это «дешёвая» атака для новичков. Читай ../06_traffic.md.

## Что скачать
```bash
sudo apt install -y tcpdump tshark ngrep
```
Tulip (опционально, сегодня с интернетом): https://github.com/CzechCyberTeam/tulip-public — сам находит флаги и генерит Python для реплея.

## Шаги
- [ ] 10:00 — на серваке запустить захват (в tmux):
```bash
sudo ./scripts/capture.sh "port 80 or port 5000"
```
- [ ] искать флаги в ИСХОДЯЩЕМ (это нас воруют):
```bash
tcpdump -r /data/pcap/d_*.pcap -A | grep -E '[A-Z0-9]{31}='
```
- [ ] нашёл флаг → смотри ЗАПРОС перед ним (это эксплойт):
```bash
tshark -r d.pcap -Y 'tcp contains "ФЛАГ"' -T fields -e tcp.stream
tshark -r d.pcap -q -z follow,tcp,ascii,<номер>
```
- [ ] отдаёшь эксплойт Глебу (реплей) и Паше (патч)

## Разведка чекера
```bash
tshark -r d.pcap -Y 'http.request' -T fields -e ip.src -e http.user_agent -e http.request.uri | sort | uniq -c | sort -rn
```
Чекер: стабильный User-Agent, ходит по расписанию. Атака — всплеск к уязвимой ручке.

## Дисциплина
Дампы с первой минуты. Нашёл эксплойт → кричишь: Глебу сплойт, Паше дыру.
