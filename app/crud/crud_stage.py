from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.training_result_stage import TrainingResultStage
from app.schemas.training_result_stage import StageCreate
from app.core.enums import StageStatus


class CRUDStage(CRUDBase[TrainingResultStage, StageCreate]):
    def create(self, db: Session, *, obj_in: StageCreate) -> TrainingResultStage:
        db_obj = TrainingResultStage(
            user_id=str(obj_in.user_id),
            started_at=obj_in.started_at,
            status=StageStatus.IN_PROGRESS,
        )
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj


stage = CRUDStage(TrainingResultStage)
