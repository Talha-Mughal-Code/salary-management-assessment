from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from app.schemas.employee import CountryCode
from app.schemas.employee_list import FilterText

GroupBy = Literal["country", "job_title", "department"]


class InsightsParams(BaseModel):
    group_by: GroupBy
    country: CountryCode | None = None
    job_title: FilterText | None = None
    department: FilterText | None = None


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
