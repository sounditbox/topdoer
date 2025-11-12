# Incident Tracker API

Минимальный сервис для регистрации, просмотра и обновления статуса инцидентов.

## Быстрый старт

```bash
pip install -e .[dev]
set DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidents  # Windows PowerShell: $env:DATABASE_URL="..."
uvicorn app.main:app --reload
```

Приложение по умолчанию ожидает PostgreSQL c базой `incidents`, пользователем `postgres` и паролем `postgres`. Создайте базу вручную или используйте docker-compose (см. ниже). Переменную `DATABASE_URL` можно переопределить под вашу конфигурацию (значения подставляются из `.env`).

## Docker

```bash
cp .env.example .env  # отредактируйте при необходимости
docker compose up --build
```

Стек docker-compose включает PostgreSQL 16 и API. Все переменные окружения вынесены в `.env` (см. `.env.example`). Для локального запуска `uvicorn` переменная `DATABASE_URL` указывает на `localhost`, а контейнер использует `DATABASE_URL_DOCKER` с хостом `db`. При необходимости скорректируйте значения в `.env`.

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

