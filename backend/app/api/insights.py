from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import InsightsServiceDep
from app.api.tags import INSIGHTS
from app.schemas.insights import (
    InsightsFilters,
    InsightsParams,
    PaySummary,
    SalaryDistribution,
)

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


@router.get(
    "/distribution",
    summary="Salary distribution",
    description="Counts of filtered employees per `salary_usd` range, for a "
    "histogram. Up to about 20 buckets with round edges; each covers `min` up to but "
    "not including `max`. Empty when no employee matches.",
    response_model=SalaryDistribution,
)
def salary_distribution(
    filters: Annotated[InsightsFilters, Query()], service: InsightsServiceDep
) -> SalaryDistribution:
    return service.distribution(filters)
