from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from datetime import datetime, UTC

from app.models.training_result_stage import TrainingResultStage
from app.models.training_result_problem import TrainingResultProblem
from app.core.enums import StageStatus
from app.crud import stage as crud_stage
from app.crud import problem as crud_problem
from app.schemas.training_result_stage import StageCreate
from app.schemas.training_result_problem import ProblemCreate


class TrainingResultService:
    def create_stage(self, db: Session, stage_in: StageCreate) -> TrainingResultStage:
        return crud_stage.create(db, obj_in=stage_in)

    def create_problem(
        self, db: Session, stage_id: int, problem_in: ProblemCreate
    ) -> TrainingResultProblem:
        return crud_problem.create(db, obj_in=problem_in, stage_id=stage_id)

    def get_stage(self, db: Session, stage_id: int) -> Optional[TrainingResultStage]:
        return crud_stage.get(db, stage_id)

    def complete_stage(
        self, db: Session, stage_id: int
    ) -> Optional[TrainingResultStage]:
        stage = crud_stage.get(db, stage_id)
        if not stage:
            return None

        result = db.execute(
            select(
                func.sum(case((TrainingResultProblem.is_correct == True, 1), else_=0)).label("correct_count"),
                func.avg(TrainingResultProblem.response_time_ms).label("avg_response_time"),
            ).where(TrainingResultProblem.stage_id == stage_id)
        )
        stats = result.one()

        stage.ended_at = datetime.now(UTC)
        stage.correct_problem_count = stats.correct_count if stats.correct_count else 0
        stage.average_response_time_ms = (
            int(stats.avg_response_time) if stats.avg_response_time else None
        )
        stage.status = StageStatus.COMPLETED

        db.flush()
        db.refresh(stage)
        return stage


training_result_service = TrainingResultService()
