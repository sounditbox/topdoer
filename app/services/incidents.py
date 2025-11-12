from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Incident, IncidentStatus


class IncidentNotFoundError(Exception):
    def __init__(self, incident_id: int) -> None:
        super().__init__(f"Incident {incident_id} not found")
        self.incident_id = incident_id


async def create_incident(
    session: AsyncSession,
    *,
    description: str,
    source: str,
    status: IncidentStatus | None = None,
) -> Incident:
    incident = Incident(
        description=description,
        source=source,
        status=status or IncidentStatus.NEW,
    )
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    return incident


async def list_incidents(
    session: AsyncSession,
    *,
    status: IncidentStatus | None = None,
) -> list[Incident]:
    stmt = select(Incident).order_by(Incident.created_at.desc())
    if status:
        stmt = stmt.where(Incident.status == status)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_incident_status(
    session: AsyncSession,
    *,
    incident_id: int,
    status: IncidentStatus,
) -> Incident:
    stmt = select(Incident).where(Incident.id == incident_id)
    result = await session.execute(stmt)
    incident = result.scalar_one_or_none()
    if incident is None:
        raise IncidentNotFoundError(incident_id)
    incident.status = status
    await session.commit()
    await session.refresh(incident)
    return incident

