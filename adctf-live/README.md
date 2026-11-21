# A/D CTF — боевой комплект (InnoCTF Junior, ForcAD)

Этот репозиторий клонируем на каждую боевую машину и работаем прямо отсюда.
**Мы полные новички — всё разжёвано.** Не понятно — открывай [00_how_it_works.md](00_how_it_works.md).

```bash
git clone https://github.com/mylifeitsbest/adctf-live.git
```

> Два репо: **adctf-kit** — подготовка на вечер (чеклист); **adctf-live** (этот) — боевой, для игры.

## Читать по порядку
1. [START_HERE.md](START_HERE.md) — первые 40 минут по минутам, кто что делает.
2. [00_how_it_works.md](00_how_it_works.md) — что такое A/D, на пальцах.
3. Своя роль — в таблице ниже, личный гайд в [roles/](roles/).

## Команда — личный гайд каждому
| Человек | Роль | Свой гайд |
|--------|------|----------|
| **Рома** | Капитан + Vulnbox/Защита | [roles/roma_captain.md](roles/roma_captain.md) |
| **Глеб** | Эксплойтер | [roles/gleb_exploiter.md](roles/gleb_exploiter.md) |
| **Паша** | Патчер | [roles/pasha_patcher.md](roles/pasha_patcher.md) |
| **Саша Ф** | Дампщик/Трафик | [roles/sasha_f_traffic.md](roles/sasha_f_traffic.md) |
| **Саша А** | Ферма/Сабмит + SLA | [roles/sasha_a_ferma.md](roles/sasha_a_ferma.md) |

## Все файлы
Гайды:
- [START_HERE.md](START_HERE.md) — план первых 40 минут
- [00_how_it_works.md](00_how_it_works.md) — как устроена игра
- [01_setup.md](01_setup.md) — настройка машин + SSH с нуля
- [02_defense.md](02_defense.md) — защита без докера
- [03_find_vulns.md](03_find_vulns.md) — как искать уязвимости
- [04_exploit.md](04_exploit.md) — как писать эксплойты
- [05_patch.md](05_patch.md) — как чинить
- [06_traffic.md](06_traffic.md) — перехват трафика, Tulip, реплей
- [07_roles.md](07_roles.md) — роли общей таблицей
- [cheatsheet.md](cheatsheet.md) — шпаргалка команд
- [resources.md](resources.md) — ссылки от оргов + учебные репо

Ферма и скрипты:
- [farm/README.md](farm/README.md) — ferma флагов (DestructiveFarm, без докера)
- [scripts/sploit_template.py](scripts/sploit_template.py) — шаблон эксплойта
- [scripts/submit_min.py](scripts/submit_min.py) — запасной сабмиттер
- [scripts/attack_data.py](scripts/attack_data.py) — тянет attack_data
- [scripts/capture.sh](scripts/capture.sh) — захват трафика
- [scripts/backup.sh](scripts/backup.sh) — бэкап сервиса
- [scripts/portaudit.sh](scripts/portaudit.sh) — аудит портов

## Железо: 6 ноутов
- 1 Ubuntu = vulnbox (наши сервисы, защищаем, заходим по SSH).
- 5 Kali = рабочие машины (атака + анализ).
- Докера нет, всё локально. Интернет только через прокси, GET.

## Факты про флаги (ForcAD)
- Формат: `[A-Z0-9]{31}=` (уточнить). Живёт 5 раундов (~10 мин). Раунд ~2 мин.
- По 2 флага на уязвимость в сервис за раунд.
- attack_data: `http://<host>/api/client/attack_data`. Сабмит по TCP (в ферме).

## 5 золотых правил
1. Главное — **не лежать и не отдавать флаги** (красный SLA = минус очки).
2. **tcpdump с 10:00** — воруем чужие эксплойты из дампа.
3. **Бэкап всего ДО открытия сети** (железо, отката нет).
4. **Патч, не блокировка** (бан убьёт чекер).
5. **Всё говорим вслух**: нашёл баг / патчу X / ферма сдаёт.
