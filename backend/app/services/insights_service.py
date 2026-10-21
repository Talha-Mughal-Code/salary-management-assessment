from decimal import ROUND_FLOOR, Decimal

from app.core.fx import CENT
from app.repositories.insights_repository import InsightsRepository
from app.schemas.insights import (
    InsightsFilters,
    InsightsParams,
    PaySummary,
    SalaryBucket,
    SalaryDistribution,
)

TARGET_BUCKETS = 20
NICE_STEPS = (Decimal(1), Decimal(2), Decimal("2.5"), Decimal(5), Decimal(10))


class InsightsService:
    def __init__(self, repository: InsightsRepository) -> None:
        self._repository = repository

    def summary(self, params: InsightsParams) -> PaySummary:
        """Highest median first, so the best and worst paid groups are the ends."""
        groups = sorted(
            self._repository.by_group(params),
            key=lambda group: (-group.median, group.key),
        )
        return PaySummary(
            group_by=params.group_by,
            overall=self._repository.overall(params),
            groups=groups,
        )

    def distribution(self, filters: InsightsFilters) -> SalaryDistribution:
        """Up to about 20 buckets with round edges, each covering [min, max)."""
        salary_range = self._repository.salary_range(filters)
        if salary_range is None:
            return SalaryDistribution(buckets=[])

        low, high = salary_range
        width = nice_width((high - low) / TARGET_BUCKETS)
        start = (low / width).to_integral_value(rounding=ROUND_FLOOR) * width
        bucket_count = int((high - start) // width) + 1
        counts = self._repository.bucket_counts(filters, start, width)
        return SalaryDistribution(
            buckets=[
                SalaryBucket(
                    min=(start + index * width).quantize(CENT),
                    max=(start + (index + 1) * width).quantize(CENT),
                    count=counts.get(index, 0),
                )
                for index in range(bucket_count)
            ]
        )


def nice_width(raw: Decimal) -> Decimal:
    """Smallest 1, 2, 2.5 or 5 times a power of ten that is at least `raw`."""
    raw = max(raw, Decimal(1))
    magnitude = Decimal(10) ** raw.adjusted()
    return next(step * magnitude for step in NICE_STEPS if step * magnitude >= raw)
