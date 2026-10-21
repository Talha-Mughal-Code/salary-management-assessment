from decimal import Decimal

from sqlalchemy import Numeric, cast, func, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.repositories.employee_filters import apply_employee_filters
from app.schemas.insights import (
    GroupPayStats,
    InsightsFilters,
    InsightsParams,
    PayStats,
)


def _percentile(fraction: float):
    """percentile_cont returns a float, so cast back to cents."""
    ordered = func.percentile_cont(fraction).within_group(Employee.salary_usd)
    return cast(ordered, Numeric(12, 2))


STAT_COLUMNS = (
    func.count().label("headcount"),
    func.min(Employee.salary_usd).label("min"),
    _percentile(0.25).label("p25"),
    _percentile(0.5).label("median"),
    _percentile(0.75).label("p75"),
    func.max(Employee.salary_usd).label("max"),
    func.round(func.avg(Employee.salary_usd), 2).label("average"),
)


class SqlAlchemyInsightsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def overall(self, params: InsightsParams) -> PayStats:
        query = apply_employee_filters(select(*STAT_COLUMNS), params)
        row = self._session.execute(query).one()
        return PayStats.model_validate(row._asdict())

    def by_group(self, params: InsightsParams) -> list[GroupPayStats]:
        group_column = getattr(Employee, params.group_by)
        query = apply_employee_filters(
            select(group_column.label("key"), *STAT_COLUMNS), params
        ).group_by(group_column)
        return [
            GroupPayStats.model_validate(row._asdict())
            for row in self._session.execute(query)
        ]

    def salary_range(self, filters: InsightsFilters) -> tuple[Decimal, Decimal] | None:
        query = apply_employee_filters(
            select(func.min(Employee.salary_usd), func.max(Employee.salary_usd)),
            filters,
        )
        low, high = self._session.execute(query).one()
        return None if low is None else (low, high)

    def bucket_counts(
        self, filters: InsightsFilters, start: Decimal, width: Decimal
    ) -> dict[int, int]:
        bucket = func.floor((Employee.salary_usd - start) / width).label("bucket")
        query = apply_employee_filters(select(bucket, func.count()), filters).group_by(
            "bucket"
        )
        return {int(index): count for index, count in self._session.execute(query)}
