from typing import Protocol

from app.schemas.insights import GroupPayStats, InsightsParams, PayStats


class InsightsRepository(Protocol):
    def overall(self, params: InsightsParams) -> PayStats: ...

    def by_group(self, params: InsightsParams) -> list[GroupPayStats]: ...
