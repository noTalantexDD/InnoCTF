# Ресурсы (от оргов + учёба)

Это ссылки, которые дали организаторы + что из них реально полезно. Клонируйте нужное СЕГОДНЯ (GET работает).

## Платформа
- **ForcAD**: https://github.com/pomo-mondreganto/ForcAD — на ней играем. Нам важны: формат флага `[A-Z0-9]{31}=`, attack_data `/api/client/attack_data`, сабмит по TCP. (`./control.py` — это для оргов, нам не нужно.)

## Фермы флагов
- **DestructiveFarm** (НАШ основной, без докера): https://github.com/DestructiveVoice/DestructiveFarm
- **S4DFarm** (запасной, только через Docker): https://github.com/C4T-BuT-S4D/S4DFarm
- **CookieFarm** (ещё альтернатива): https://github.com/ByteTheCookies/CookieFarm
- Настройка — в [farm/README.md](farm/README.md).

## Анализ трафика
- **Tulip**: https://github.com/CzechCyberTeam/tulip-public — flow-анализатор, сам генерит Python-сниппеты для реплея атак. Очень полезно дампщику.
- **Shovel**: https://github.com/ANSSI-FR/shovel — веб-интерфейс над Suricata, для A/D.
- Если не успели поставить Tulip — хватит tcpdump + tshark + grep ([06_traffic.md](06_traffic.md)).

## Учебные репо C4T-BuT-S4D (РЕАЛЬНЫЕ сервисы/чекеры/сплойты прошлых игр)
Очень ценно: посмотреть, как выглядят настоящие сервисы и готовые сплойты.
- https://github.com/C4T-BuT-S4D (организация)
- https://github.com/C4T-BuT-S4D/ctfcup-2023-ad — сервисы + чекеры + сплойты
- https://github.com/C4T-BuT-S4D/ctfcup-2024-igra — финал CTFCUP 2024
- https://github.com/C4T-BuT-S4D/stay-home-ctf-2020 — сервисы + чекеры + сплойты
- **Совет:** сегодня откройте 1–2 сплойта оттуда и прочитайте — увидите, как реально пишется эксплойт под ферму.
- neo (https://github.com/C4T-BuT-S4D/neo) — система распространения эксплойтов. **Для нас избыточно** — хватит одной фермы, не тратьте время.

## Статьи для новичков (прочитать сегодня, 20 мин)
- A primer on Attack-Defense (Maple Bacon): https://maplebacon.org/2025/09/maple-attack-defense-primer/
- Attack/Defense for Beginners (FAUST): https://2024.faustctf.net/information/attackdefense-for-beginners/
- Гайд для новичков (Codeby, на рус): https://codeby.school/blog/informacionnaya-bezopasnost/attack-defence-ctf-gayd-dlya-novichkov
- Видео: https://vkvideo.ru/video-215805549_456239028
