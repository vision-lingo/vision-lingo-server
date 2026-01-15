from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from app.core.enums import StageStatus


class StageCreate(BaseModel):
    user_id: UUID = Field(..., description="User identifier")
    started_at: datetime = Field(..., description="When the training stage started")


class StageResponse(BaseModel):
    stage_id: int = Field(..., description="Created stage ID")

    model_config = {"from_attributes": True}


class StageCompleteResponse(BaseModel):
    stage_id: int
    user_id: UUID
    started_at: datetime
    ended_at: datetime
    correct_problem_count: int
    average_response_time_ms: Optional[int]
    status: StageStatus

    model_config = {"from_attributes": True}
