from typing import Optional

from sqlalchemy import BigInteger, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from app.db.base import Base
from app.core.enums import SpatialPosition


class TrainingResultProblem(Base):
    __tablename__ = "training_result_problem"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    stage_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    spatial_position: Mapped[SpatialPosition] = mapped_column(
        SQLEnum(SpatialPosition), nullable=False
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    selection_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
