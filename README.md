# Incident Tracker API

Асинхронный сервис (FastAPI + SQLAlchemy) для регистрации инцидентов, просмотра списка и обновления статусов. В качестве основного хранилища используется PostgreSQL.

## Требования

- Python 3.11
- PostgreSQL (локально или в контейнере)
- Утилиты: `pip`, `docker`/`docker compose` (опционально)

## Установка и запуск локально

```bash
python -m venv .venv
.venv\Scripts\activate      # PowerShell: .\.venv\Scripts\Activate.ps1, Linux/macOS: source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env        # отредактируйте под свою БД
uvicorn app.main:app --reload
```

По умолчанию приложение ожидает PostgreSQL с параметрами из `.env`:

- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`
- `POSTGRES_DB=incidents`
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidents`
- `DATABASE_URL_DOCKER=postgresql+asyncpg://postgres:postgres@db:5432/incidents`

При запуске вне docker используйте `DATABASE_URL`; для контейнеров пригодится `DATABASE_URL_DOCKER`.

### Ручное создание БД

```bash
createdb incidents
```

или выполните команды в psql:

```sql
CREATE DATABASE incidents;
```

## Запуск в Docker

```bash
cp .env.example .env
docker compose up --build
```

Compose поднимает два сервиса:

- `db` — PostgreSQL 16 с постоянным volume `db-data`
- `api` — FastAPI-приложение на порту `8000`

После старта документация доступна по адресу <http://localhost:8000/docs>.

## API

- `POST /incidents` — создать инцидент
- `GET /incidents?status=<status>` — получить список инцидентов (опциональный фильтр по статусу)
- `PATCH /incidents/{id}` — обновить статус инцидента

Доступные источники: `operator`, `monitoring`, `partner`.  
Доступные статусы: `new`, `in_progress`, `resolved`, `closed`.

## Тестирование

```bash
.venv\Scripts\activate
pytest
```

Тесты используют in-memory SQLite с подменой зависимостей, поэтому внешняя БД не требуется.

## Структура проекта (упрощённо)

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

