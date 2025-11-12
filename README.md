# Incident Tracker API

Минимальный сервис для регистрации, просмотра и обновления статуса инцидентов.

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e .[dev]
uvicorn app.main:app --reload
```

По умолчанию данные сохраняются в `SQLite` файле `incidents.db` в корне проекта. Переопределить можно переменной окружения `DATABASE_URL`, например:

```bash
set DATABASE_URL=sqlite+aiosqlite:///./dev.db
```

## API

- `POST /incidents`

  ```http
  POST /incidents
  Content-Type: application/json

  {
    "description": "Scooter offline",
    "source": "operator",
    "status": "in_progress"
  }
  ```

- `GET /incidents?status=<status>`

  ```http
  GET /incidents?status=new
  Accept: application/json
  ```

- `PATCH /incidents/{id}`

  ```http
  PATCH /incidents/1
  Content-Type: application/json

  {
    "status": "resolved"
  }
  ```

Доступные источники: `operator`, `monitoring`, `partner`.
Доступные статусы: `new`, `in_progress`, `resolved`, `closed`.

## Тесты

```bash
.venv\Scripts\activate
pytest
```

