from typing import Optional

from sqlalchemy import BigInteger, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from app.db.base import Base
from app.core.enums import StageStatus


class TrainingResultStage(Base):
    __tablename__ = "training_result_stage"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(CHAR(36), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    correct_problem_count: Mapped[int] = mapped_column(Integer, default=0)
    average_response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[StageStatus] = mapped_column(
        SQLEnum(StageStatus), default=StageStatus.IN_PROGRESS
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
