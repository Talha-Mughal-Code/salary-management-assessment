from sqlalchemy import Numeric, cast, func, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.repositories.employee_filters import apply_employee_filters
from app.schemas.insights import GroupPayStats, InsightsParams, PayStats


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
