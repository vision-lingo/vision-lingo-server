from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import SpatialPosition


class ProblemCreate(BaseModel):
    spatial_position: SpatialPosition = Field(..., description="Position in 3D space")
    is_correct: bool = Field(..., description="Whether the answer was correct")
    response_time_ms: Optional[int] = Field(None, ge=0, description="Response time in milliseconds")
    selection_count: int = Field(..., ge=1, description="Number of selections made")


class ProblemResponse(BaseModel):
    problem_id: int = Field(..., description="Created problem ID")

    model_config = {"from_attributes": True}
