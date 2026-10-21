from decimal import Decimal
from typing import Protocol

from app.schemas.insights import (
    GroupPayStats,
    InsightsFilters,
    InsightsParams,
    PayStats,
)


class InsightsRepository(Protocol):
    def overall(self, params: InsightsParams) -> PayStats: ...

    def by_group(self, params: InsightsParams) -> list[GroupPayStats]: ...

    def salary_range(
        self, filters: InsightsFilters
    ) -> tuple[Decimal, Decimal] | None: ...

    def bucket_counts(
        self, filters: InsightsFilters, start: Decimal, width: Decimal
    ) -> dict[int, int]: ...
