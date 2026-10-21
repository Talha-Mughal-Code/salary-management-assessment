from fastapi import APIRouter

from app.api.tags import HEALTH
from app.schemas.health import HealthResponse

router = APIRouter(tags=[HEALTH])


@router.get(
    "/health",
    summary="Check the API is running",
    description="Returns ok when the process is up. Does not check the database.",
    response_model=HealthResponse,
)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
