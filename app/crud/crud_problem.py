from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.training_result_problem import TrainingResultProblem
from app.schemas.training_result_problem import ProblemCreate


class CRUDProblem(CRUDBase[TrainingResultProblem, ProblemCreate]):
    def create(
        self, db: Session, *, obj_in: ProblemCreate, stage_id: int
    ) -> TrainingResultProblem:
        db_obj = TrainingResultProblem(
            stage_id=stage_id,
            spatial_position=obj_in.spatial_position,
            is_correct=obj_in.is_correct,
            response_time_ms=obj_in.response_time_ms,
            selection_count=obj_in.selection_count,
        )
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj


problem = CRUDProblem(TrainingResultProblem)
