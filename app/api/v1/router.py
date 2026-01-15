from fastapi import APIRouter

from app.api.v1.endpoints import training_result

api_router = APIRouter()

api_router.include_router(
    training_result.router,
    prefix="/training-result",
    tags=["훈련 결과"],
)
