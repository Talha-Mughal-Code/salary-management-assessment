from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from app.schemas.employee import CountryCode
from app.schemas.employee_list import FilterText

GroupBy = Literal["country", "job_title", "department"]


class InsightsFilters(BaseModel):
    country: CountryCode | None = None
    job_title: FilterText | None = None
    department: FilterText | None = None


class InsightsParams(InsightsFilters):
    group_by: GroupBy


class PayStats(BaseModel):
    headcount: int
    min: Decimal | None
    p25: Decimal | None
    median: Decimal | None
    p75: Decimal | None
    max: Decimal | None
    average: Decimal | None


class GroupPayStats(PayStats):
    key: str


class PaySummary(BaseModel):
    group_by: GroupBy
    currency: Literal["USD"] = "USD"
    overall: PayStats
    groups: list[GroupPayStats]


class SalaryBucket(BaseModel):
    min: Decimal
    max: Decimal
    count: int


class SalaryDistribution(BaseModel):
    currency: Literal["USD"] = "USD"
    buckets: list[SalaryBucket]
