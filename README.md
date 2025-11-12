# Incident Tracker API

Минимальный сервис для регистрации, просмотра и обновления статуса инцидентов.

## Быстрый старт

```bash
pip install -e .[dev]
uvicorn app.main:app --reload
```

По умолчанию данные сохраняются в `SQLite` файле `incidents.db` в корне проекта. Переопределить можно переменной окружения `DATABASE_URL`

## Docker

```bash
docker build -t incident-tracker .
docker run --rm -p 8000:8000 incident-tracker
```

или

```bash
docker compose up --build
```

Для проброса нестандартного подключения задайте `DATABASE_URL` в `.env` или через переменные окружения.

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
pytest
```

