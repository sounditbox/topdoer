# Incident Tracker API

Асинхронный сервис (FastAPI + SQLAlchemy) для регистрации инцидентов, просмотра списка и обновления статусов. В качестве основного хранилища используется PostgreSQL.

## Требования

- Python 3.11+
- PostgreSQL (локально или в контейнере)
- Poetry 1.8+
- Docker / Docker Compose (для контейнерного запуска)

## Запуск в Docker

```bash
cp .env.example .env        # отредактируйте при необходимости
docker compose up --build
```

Compose поднимает два сервиса:

- `db` — PostgreSQL 16 с постоянным volume `db-data`
- `api` — FastAPI-приложение на порту `8000`

После старта документация доступна по адресу <http://localhost:8000/docs>.

## Локальная разработка (Poetry)

```bash
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload
```

По умолчанию приложение ожидает PostgreSQL с параметрами из `.env`:

- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`
- `POSTGRES_DB=incidents`
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidents`
- `DATABASE_URL_DOCKER=postgresql+asyncpg://postgres:postgres@db:5432/incidents`

При запуске вне docker используйте `DATABASE_URL`; для контейнеров пригодится `DATABASE_URL_DOCKER`.
## API

- `POST /incidents` — создать инцидент
- `GET /incidents?status=<status>` — получить список инцидентов (опциональный фильтр по статусу)
- `PATCH /incidents/{id}` — обновить статус инцидента

Доступные источники: `operator`, `monitoring`, `partner`.  
Доступные статусы: `new`, `in_progress`, `resolved`, `closed`.

## Тестирование
В рабочей директории:
```bash
poetry run pytest
```

Тесты используют in-memory SQLite с подменой зависимостей, поэтому внешняя БД не требуется.

## Структура проекта

- `app/core` — настройки приложения
- `app/db` — подключение к БД и базовые модели
- `app/models` — ORM-модели SQLAlchemy
- `app/schemas` — Pydantic-схемы
- `app/services` — бизнес-логика
- `app/api` — маршруты FastAPI
- `tests/` — асинхронные тесты API

## Полезные ссылки

- Swagger UI: <http://localhost:8000/docs>
- JSON-schema: <http://localhost:8000/openapi.json>

