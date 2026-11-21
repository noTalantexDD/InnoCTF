# файлы и директории

- **Конфигурационный файл:** `/etc/suricata/suricata.yaml`

- **Логи и отчеты:** `/var/log/suricata/`
    - `fast.log` — краткий текстовый лог срабатываний.
    - `eve.json` — подробный лог в формате JSON (удобен для отправки в ELK, Grafana).
    - `stats.log` — статистика работы движка.

- **Правила (сигнатуры):** `/var/lib/suricata/rules/`

# первичная настройка
sudo nano /etc/suricata/suricata.yaml -> Укажите ваш сетевой интерфейс, который нужно прослушивать в секции af-packet -> interface

sudo suricata -T -v -c /etc/suricata/suricata.yaml -> Notice: suricata: Configuration provided was successfully loaded. Exiting.  -> если так, то всё норм

Warning: detect: No rule files match the pattern /var/lib/suricata/rules/suricata.rules -> sudo suricata-update

# как пишутся правила