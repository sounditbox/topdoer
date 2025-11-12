from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.models import IncidentSource, IncidentStatus


StatusField = Annotated[IncidentStatus, Field(examples=[IncidentStatus.NEW])]
SourceField = Annotated[IncidentSource, Field(examples=[IncidentSource.OPERATOR])]


class IncidentBase(BaseModel):
    description: Annotated[str, Field(min_length=1, max_length=10_000)]
    source: SourceField


class IncidentCreate(IncidentBase):
    status: StatusField | None = None


class IncidentRead(IncidentBase):
    id: int
    status: StatusField
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentList(BaseModel):
    items: list[IncidentRead]


class IncidentStatusUpdate(BaseModel):
    status: StatusField

