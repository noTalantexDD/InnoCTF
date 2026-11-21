# Как чинить уязвимости (шаблоны)

Главное: **маленький дифф + не ломать работу сервиса**. После патча — чекер зелёный.

## Общий порядок
```bash
cd /opt/service1
git init -q && git add -A && git commit -qm round0   # один раз
# ...правишь код...
git add -A && git commit -m "patch: закрыл IDOR в /note"
sudo systemctl restart <сервис>
# проверь: сервис отвечает? чекер зелёный?
```
Сломал — откат: `git reset --hard round0 && sudo systemctl restart <сервис>`.

## Патчи по классам

### IDOR (отдаёт чужой объект без проверки) — самое частое
```python
@app.get("/note/<id>")
def note(id):
    n = db.get_note(id)
    if n.owner != current_user(): abort(403)   # <-- добавил
    return n
```

### Path traversal
```python
import os
name = os.path.basename(name)          # убирает ../
path = os.path.join(SAFE_DIR, name)
if not os.path.realpath(path).startswith(os.path.realpath(SAFE_DIR)): abort(403)
```

### SQL-инъекция
```python
# было: f"SELECT * FROM t WHERE q='{q}'"
cur.execute("SELECT * FROM t WHERE q=%s", (q,))
```

### Командная инъекция
Убери `os.system`/`shell=True`; если надо — `shlex.quote` + белый список.

### Десериализация
`pickle.loads` → `json.loads`. `yaml.load` → `yaml.safe_load`.

### Дефолтные секреты / debug
Смени пароль/ключ; выключи debug/admin-ручки или закрой проверкой.

## Чего НЕ делать
- Не блокировать по IP (убьёшь чекер).
- Не менять формат ответов, которые проверяет чекер.
- Не трогать, как чекер кладёт/читает флаг.

## Приоритет
Сначала закрывай дыры, которые УЖЕ эксплуатируют (от Саши Ф и Глеба).
