# Перехват и анализ трафика — главный приём

Делает Саша Ф. Две пользы: 1) видишь кто тебя ломает → патч; 2) берёшь чужой эксплойт из дампа и реплеишь по всем.

## 1. Запустить захват в 10:00 (на серваке, в tmux)
```bash
sudo mkdir -p /data/pcap
sudo ./scripts/capture.sh "port 80 or port 5000"
```
`capture.sh` крутит tcpdump с ротацией каждые 5 мин. Чисти старые pcap.

## 2. Найти, что у нас воруют (флаги в ИСХОДЯЩЕМ)
```bash
tcpdump -r /data/pcap/d_*.pcap -A | grep -E '[A-Z0-9]{31}='
tshark -r /data/pcap/d_*.pcap -Y 'frame contains "="' -T fields -e ip.src -e ip.dst -e http.request.uri
```

## 3. Достать сам эксплойт
Нашёл флаг → смотри ЗАПРОС перед ним в той же TCP-сессии:
```bash
tshark -r d.pcap -Y 'tcp contains "<кусок_флага>"' -T fields -e tcp.stream
tshark -r d.pcap -q -z follow,tcp,ascii,<номер>
```
Берёшь: метод, URI, заголовки, тело. Параметр с flag_id → подставляешь flag_id из attack_data для каждой команды.

## 4. Реплей = атака
Оформляешь как sploit_<svc>.py (scripts/sploit_template.py), отдаёшь Глебу/в ферму. Параллельно Паша патчит.

## 5. Tulip (если поставили)
Сам раскладывает потоки, ищет флаги, генерит Python для реплея. Нет — хватает tcpdump+tshark+grep.

## 6. Разведка чекера
```bash
tshark -r d.pcap -Y 'http.request' -T fields -e ip.src -e http.user_agent -e http.request.uri | sort | uniq -c | sort -rn
```
Чекер: стабильный UA, по расписанию. Атака: всплеск к уязвимой ручке. Патч надёжнее фильтра.

## Дисциплина
Дампы с первой минуты. Нашёл эксплойт → Глебу сплойт, Паше дыру.
