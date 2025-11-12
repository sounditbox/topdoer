from __future__ import annotations

import os
from collections.abc import AsyncIterator
from typing import Any

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import create_app
from app.models import IncidentStatus


@pytest.fixture
async def client(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[AsyncClient]:
    test_engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_session_factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async def _init_db() -> None:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def _get_session() -> AsyncIterator[AsyncSession]:
        async with test_session_factory() as session:
            yield session

    monkeypatch.setattr("app.db.session.engine", test_engine)
    monkeypatch.setattr("app.db.session.SessionFactory", test_session_factory)
    monkeypatch.setattr("app.db.session.init_db", _init_db)
    monkeypatch.setattr("app.db.session.get_session", _get_session)
    monkeypatch.setattr("app.db.init_db", _init_db)
    monkeypatch.setattr("app.db.get_session", _get_session)
    monkeypatch.setattr("app.api.incidents.get_session", _get_session)
    monkeypatch.setattr("app.main.init_db", _init_db)

    await _init_db()
    app = create_app()

    transport = ASGITransport(app=app)
    await app.router.startup()
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as test_client:
            yield test_client
    finally:
        await app.router.shutdown()

    await test_engine.dispose()


async def _create_incident(client: AsyncClient, **payload: Any) -> dict[str, Any]:
    response = await client.post("/incidents/", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


@pytest.mark.anyio
async def test_create_incident_defaults_status(client: AsyncClient) -> None:
    payload = {
        "description": "Scooter offline",
        "source": "operator",
    }
    response = await client.post("/incidents/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["description"] == payload["description"]
    assert body["source"] == payload["source"]
    assert body["status"] == IncidentStatus.NEW
    assert "id" in body and "created_at" in body


@pytest.mark.anyio
async def test_list_incidents_filter_by_status(client: AsyncClient) -> None:
    await _create_incident(
        client,
        description="Monitoring alert",
        source="monitoring",
        status="in_progress",
    )
    await _create_incident(
        client,
        description="Partner issue",
        source="partner",
        status="resolved",
    )

    response = await client.get("/incidents/", params={"status": "in_progress"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["status"] == "in_progress"


@pytest.mark.anyio
async def test_update_incident_status(client: AsyncClient) -> None:
    incident = await _create_incident(
        client,
        description="Battery low",
        source="operator",
    )
    response = await client.patch(
        f"/incidents/{incident['id']}",
        json={"status": "resolved"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "resolved"
    assert body["id"] == incident["id"]


@pytest.mark.anyio
async def test_update_missing_incident_returns_404(client: AsyncClient) -> None:
    response = await client.patch("/incidents/9999", json={"status": "resolved"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident 9999 not found"

