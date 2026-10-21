from app.repositories.insights_repository import InsightsRepository
from app.schemas.insights import InsightsParams, PaySummary


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
