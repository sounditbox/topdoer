from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import IncidentStatus
from app.schemas import (
    IncidentCreate,
    IncidentList,
    IncidentRead,
    IncidentStatusUpdate,
)
from app.services import (
    IncidentNotFoundError,
    create_incident,
    list_incidents,
    update_incident_status,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident_endpoint(
    payload: IncidentCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IncidentRead:
    incident = await create_incident(
        session,
        description=payload.description,
        source=payload.source,
        status=payload.status,
    )
    return IncidentRead.model_validate(incident)


@router.get("/", response_model=IncidentList)
async def list_incidents_endpoint(
    session: Annotated[AsyncSession, Depends(get_session)],
    status_filter: Annotated[IncidentStatus | None, Query(alias="status")] = None,
) -> IncidentList:
    incidents = await list_incidents(session, status=status_filter)
    return IncidentList(items=[IncidentRead.model_validate(obj) for obj in incidents])


@router.patch("/{incident_id}", response_model=IncidentRead)
async def update_incident_status_endpoint(
    incident_id: int,
    payload: IncidentStatusUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IncidentRead:
    try:
        incident = await update_incident_status(
            session,
            incident_id=incident_id,
            status=payload.status,
        )
    except IncidentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found",
        ) from None
    return IncidentRead.model_validate(incident)

