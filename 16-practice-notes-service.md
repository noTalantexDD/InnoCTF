# 16. Практика A/D на локальных «Заметках»

[Оглавление](./README.md) · [Чтение сервиса](./09-read-a-service.md) · [Бэкапы](./08-backup-and-restore.md) · [Приложение InnoCTF](./17-innoctf-notes.md)

За одно упражнение ты поднимешь сервис, запишешь его исходное поведение, сделаешь проверяемую копию, поправишь правило чтения и восстановишься после неверной настройки БД. Результат можно проверить по конкретным HTTP-кодам.

**Что нужно:** Bash, Python 3, `curl`, `cp` и `sha256sum`. Достаточно обычного терминала Linux или WSL. Код использует стандартную библиотеку Python. Сервер слушает только `127.0.0.1`. Используй новый временный каталог и одноразовые учебные данные. Учебная аутентификация Basic здесь нужна для двух локальных ролей, а учётные данные сохранены только для этого упражнения.

## 1. Подготовь стенд

В терминале A создай новую папку. Все файлы ниже должны лежать именно в ней. Скопируй вывод `pwd` во второй терминал, чтобы потом можно было открыть тот же каталог.

```bash
umask 077
lab_dir=$(mktemp -d)
test -n "$lab_dir" && cd -- "$lab_dir" && pwd
```

Создай учебную БД, настройки и два случайных пароля. Этот блок предназначен для **нового** каталога:

```bash
python3 - <<'PY'
from contextlib import closing
from pathlib import Path
import json
import secrets
import sqlite3

with Path("config.json").open("x", encoding="utf-8") as file:
    json.dump({"database": "notes.sqlite3"}, file)

users = {name: secrets.token_urlsafe(24) for name in ("alice", "bob")}
with Path("lab-users.json").open("x", encoding="utf-8") as file:
    json.dump(users, file)

with closing(sqlite3.connect("notes.sqlite3")) as db, db:
    db.execute("""CREATE TABLE notes (
        id INTEGER PRIMARY KEY,
        owner TEXT NOT NULL,
        title TEXT NOT NULL,
        archived INTEGER NOT NULL CHECK (archived IN (0, 1))
    )""")
    db.executemany("INSERT INTO notes VALUES (?, ?, ?, ?)", [
        (1, "alice", "Обычная заметка Алисы", 0),
        (2, "alice", "Старая заметка Алисы", 1),
        (3, "bob", "Заметка Бориса", 0),
    ])
print("Готово: config.json, lab-users.json и notes.sqlite3")
PY
```

`config.json` хранит путь к базе. В базе три учебные записи, `archived = 1` обозначает старую архивную заметку. Пароли в `lab-users.json` можно посмотреть у себя в редакторе и вводить в запрос `curl --user alice`, когда он спросит. Файл остаётся в закрытой учебной папке.

## 2. Сохрани код в notes_lab.py и запусти

Создай файл `notes_lab.py` в этой же папке. Заметь: путь к базе берётся из конфигурации при запуске, а сама база открывается только на чтение. Поэтому неверный путь не создаст новую пустую БД.

```python
from contextlib import closing
from pathlib import Path
from wsgiref.simple_server import make_server
import base64
import json
import re
import secrets
import sqlite3

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
users = json.loads((ROOT / "lab-users.json").read_text(encoding="utf-8"))
db_uri = (ROOT / config["database"]).resolve().as_uri() + "?mode=ro"


def reply(start_response, status, payload, headers=()):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    start_response(status, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Cache-Control", "no-store"),
        *headers,
    ])
    return [body]


def get_user(header):
    scheme, _, encoded = header.partition(" ")
    if scheme.lower() != "basic":
        return None
    try:
        user, sep, password = base64.b64decode(encoded, validate=True).partition(b":")
        name = user.decode("utf-8")
    except ValueError:
        return None
    expected = users.get(name)
    if sep and expected is not None and secrets.compare_digest(password, expected.encode()):
        return name
    return None


def app(environ, start_response):
    if environ["REQUEST_METHOD"] != "GET":
        return reply(start_response, "405 Method Not Allowed", {"error": "method"}, [
            ("Allow", "GET"),
        ])

    path = environ["PATH_INFO"]
    if path == "/health":
        try:
            with closing(sqlite3.connect(db_uri, uri=True)) as db:
                db.execute("SELECT id FROM notes LIMIT 1").fetchone()
        except sqlite3.Error:
            return reply(start_response, "503 Service Unavailable", {"error": "database"})
        return reply(start_response, "200 OK", {"status": "ready"})

    match = re.fullmatch(r"/notes/([0-9]{1,12})", path)
    if match is None:
        return reply(start_response, "404 Not Found", {"error": "not found"})

    user = get_user(environ.get("HTTP_AUTHORIZATION", ""))
    if user is None:
        return reply(start_response, "401 Unauthorized", {"error": "sign in"}, [
            ("WWW-Authenticate", 'Basic realm="Notes lab"'),
        ])

    note_id = int(match[1])
    try:
        with closing(sqlite3.connect(db_uri, uri=True)) as db:
            note = db.execute(
                "SELECT id, title FROM notes WHERE id = ? AND owner = ? AND archived = 0",
                (note_id, user),
            ).fetchone()
    except sqlite3.Error:
        return reply(start_response, "503 Service Unavailable", {"error": "database"})
    if note is None:
        return reply(start_response, "404 Not Found", {"error": "not found"})

    return reply(start_response, "200 OK", {"id": note[0], "title": note[1]})


if __name__ == "__main__":
    with make_server("127.0.0.1", 18080, app) as server:
        print("Notes lab: http://127.0.0.1:18080", flush=True)
        server.serve_forever()
```

В терминале A:

```bash
python3 notes_lab.py
```

Если порт занят, выбери другой только для своего теста и подставь его и в `make_server`, и в запросы. Ctrl+C останавливает именно этот процесс в терминале A. Терминал B используй для проверок.

Карта сервиса: **ПК → `127.0.0.1:18080` → функция `app` → проверка учётки → запрос с условием владельца → SQLite → HTTP-ответ**. `/health` проверяет, доступна ли таблица для чтения. Работу правила доступа подтверждают отдельные запросы. [Справка wsgiref](https://docs.python.org/3/library/wsgiref.html) · [Справка sqlite3](https://docs.python.org/3/library/sqlite3.html)

## 3. Зафиксируй исходный результат

В терминале B открой тот же каталог. Выполняй запросы по одному. Вводи пароль того пользователя, которого передаёшь через `--user`. Пароль не нужен для `/health`.

```bash
curl --noproxy '*' -sS -i --max-time 5 http://127.0.0.1:18080/health
curl --noproxy '*' -sS -i --max-time 5 --user alice http://127.0.0.1:18080/notes/1
curl --noproxy '*' -sS -i --max-time 5 --user alice http://127.0.0.1:18080/notes/2
curl --noproxy '*' -sS -i --max-time 5 --user bob http://127.0.0.1:18080/notes/2
```

| Проверка | До изменения | После исправления |
|---|---|---|
| Готовность `/health` | `200` | `200` |
| Алиса открывает свою обычную заметку №1 | `200` | `200` |
| Алиса открывает свою архивную заметку №2 | `404` | `200` |
| Борис обращается к учебной заметке №2 Алисы | `404` | `404` |

Представим, что требование задачи — **владелец сохраняет право читать архивные заметки**. Тест Алисы показывает дефект доступности. Запиши исходные коды с временем и оставь тест Бориса как контроль границы доступа.

## 4. Сделай резервную копию и скачай её в отдельную папку

В этом упражнении «оператор» и «сервер» на одном ПК. Две отдельные папки имитируют передачу, а на матче для передачи применяется `scp`. **Терминал B**, каталог стенда:

```bash
umask 077
backup_dir=$(mktemp -d "$PWD/before-XXXXXX")
test -n "$backup_dir" &&
  cp -- notes_lab.py config.json "$backup_dir/" &&
  python3 - "$backup_dir" <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

source = Path("notes.sqlite3").resolve().as_uri() + "?mode=ro"
destination = Path(sys.argv[1]) / "notes.sqlite3"
with closing(sqlite3.connect(source, uri=True)) as src:
    with closing(sqlite3.connect(destination)) as dst:
        src.backup(dst)
        if dst.execute("PRAGMA integrity_check").fetchone() != ("ok",):
            raise SystemExit("Копия SQLite не прошла проверку")
PY
```

Если команда прошла, сформируй контрольные суммы и сделай перенос:

```bash
operator_dir=$(mktemp -d)
test -n "$operator_dir" &&
  (cd "$backup_dir" && sha256sum notes_lab.py config.json notes.sqlite3 > SHA256SUMS) &&
  cp -- "$backup_dir/notes_lab.py" "$backup_dir/config.json" "$backup_dir/notes.sqlite3" "$backup_dir/SHA256SUMS" "$operator_dir/" &&
  (cd "$operator_dir" && sha256sum -c SHA256SUMS)
```

Ожидается три строки `OK`. База скопирована через штатный метод SQLite, файлы после переноса сверены. `lab-users.json` в передаваемую копию не входит. Для запуска восстановленного учебного экземпляра доступ к этому отдельному файлу должен остаться у тебя. Подробнее — [глава 08](./08-backup-and-restore.md).

## 5. Исправь правило и повтори четырёхстрочный тест

В коде выборки сохрани фильтр владельца, а лишнее для этого учебного контракта условие архива убери. Итоговый фрагмент:

```python
note = db.execute(
    "SELECT id, title FROM notes WHERE id = ? AND owner = ?",
    (note_id, user),
).fetchone()
```

Проверь, что изменился только этот запрос: `diff -u "$backup_dir/notes_lab.py" notes_lab.py`. Для `diff` код 1 при обнаруженных отличиях ожидаем. Проверь синтаксис: `python3 -m py_compile notes_lab.py`. Останови процесс в A и запусти снова. Повтори все запросы из раздела 3, включая отказ для Бориса. Результат должен совпасть с колонкой «После исправления».

Что доказано: разрешённое чтение архивной записи восстановилось, а доступ через другую учётку остался ограниченным. Проверка охватывает описанные случаи.

## 6. Вызови сбой конфигурации и верни рабочее состояние

**Только в своём временном каталоге.** В терминале A останови учебный процесс. В B подмени путь к несуществующей базе:

```bash
printf '{"database":"missing.sqlite3"}\n' > config.json
```

Запусти процесс в A снова. В B запроси `/health`. Ожидается **`503`**, хотя TCP и сам HTTP-сервер доступны. Базы `missing.sqlite3` появиться не должно: сервис открывает её только на чтение.

Останови процесс в A. Верни **один** файл из проверенной операторской копии:

```bash
test -n "$operator_dir" && test -f "$operator_dir/config.json" &&
  cp -- "$operator_dir/config.json" config.json
```

Запусти снова. Ожидается `200` у `/health`, Алиса снова видит №2, Борис получает `404`. Поправленный код сохранится. Для репетиции чтения данных из бэкапа отдельно открой файл `"$operator_dir/notes.sqlite3"` через SQLite в режиме чтения и убедись, что есть строки №1–3. Текущую БД для такой проверки заменять не нужно. После упражнения останови локальный сервер.

## 7. Что записать по итогу

| Шаг | Что должно быть в журнале |
|---|---|
| Исходный тест | `200 / 200 / 404 / 404` в порядке таблицы |
| Копирование | Путь, список копий и результат сверки |
| Исправление | Условие владельца сохранено, разрешено чтение архива |
| Контрольный тест | `200 / 200 / 200 / 404` |
| Сбой и откат | `503` из-за пути к БД, восстановлен только конфиг, контрольный тест повторён |

**Самопроверка:** почему «живо» и «готово» расходятся при неправильном пути к БД? Как тест Бориса ограничивает ошибку при правке? Почему возврат одного конфига оставляет полезный патч в коде? Если можешь ответить по своим наблюдениям, упражнение выполнено.

<details>
<summary>Ответы</summary>

- Процесс принимает HTTP, но проверка готовности обращается к таблице и возвращает `503`, когда БД недоступна.
- Запись должна стать доступна Алисе. Повторный отказ Борису проверяет, что при правке не сняли ограничение по владельцу.
- Путь к БД хранится в `config.json`, а правило чтения — в `notes_lab.py`. В упражнении менялся только путь, поэтому для восстановления достаточно вернуть конфиг.

</details>
