from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.services.training_result import training_result_service
from app.schemas.training_result_stage import (
    StageCreate,
    StageResponse,
    StageCompleteResponse,
)
from app.schemas.training_result_problem import (
    ProblemCreate,
    ProblemResponse,
)

router = APIRouter()


@router.post(
    "/stages",
    response_model=StageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 훈련 결과 스테이지 생성",
    description="새로운 훈련 스테이지를 기록",
)
def create_stage(
    stage_in: StageCreate,
    db: Session = Depends(get_db),
) -> StageResponse:
    db_stage = training_result_service.create_stage(db, stage_in)
    return StageResponse(stage_id=db_stage.id)


@router.post(
    "/stages/{stage_id}/problems",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="문제 풀이 결과 기록",
    description="특정 스테이지에 대한 문제 결과를 기록",
)
def create_problem(
    stage_id: int,
    problem_in: ProblemCreate,
    db: Session = Depends(get_db),
) -> ProblemResponse:
    existing_stage = training_result_service.get_stage(db, stage_id)
    if not existing_stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"스테이지 ID {stage_id}를 찾을 수 없습니다",
        )

    db_problem = training_result_service.create_problem(db, stage_id, problem_in)
    return ProblemResponse(problem_id=db_problem.id)


@router.put(
    "/stages/{stage_id}/complete",
    response_model=StageCompleteResponse,
    summary="훈련 스테이지 완료 처리",
    description="스테이지를 완료 상태로 변경하고 정답률 및 평균 응답 시간을 계산",
)
def complete_stage(
    stage_id: int,
    db: Session = Depends(get_db),
) -> StageCompleteResponse:
    db_stage = training_result_service.complete_stage(db, stage_id)
    if not db_stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"스테이지 ID {stage_id}를 찾을 수 없습니다",
        )

    return StageCompleteResponse(
        stage_id=db_stage.id,
        user_id=UUID(db_stage.user_id),
        started_at=db_stage.started_at,
        ended_at=db_stage.ended_at,
        correct_problem_count=db_stage.correct_problem_count,
        average_response_time_ms=db_stage.average_response_time_ms,
        status=db_stage.status,
    )
