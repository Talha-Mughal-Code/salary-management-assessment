from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import InsightsServiceDep
from app.api.tags import INSIGHTS
from app.schemas.insights import InsightsParams, PaySummary

router = APIRouter(prefix="/api/v1/insights", tags=[INSIGHTS])


@router.get(
    "/summary",
    summary="Pay summary by group",
    description="Headcount, min, 25th percentile, median, 75th percentile, max "
    "and average of `salary_usd`, for all filtered employees and per group. "
    "Groups are ordered by median, highest first.",
    response_model=PaySummary,
)
def pay_summary(
    params: Annotated[InsightsParams, Query()], service: InsightsServiceDep
) -> PaySummary:
    return service.summary(params)
