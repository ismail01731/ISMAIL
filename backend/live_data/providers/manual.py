from datetime import datetime, timezone
from typing import Any
from .base import LiveDataProvider
from ..models import LiveData
class ManualProvider(LiveDataProvider):
    name = "manual"
    reliability = 0.50
    def fetch(
        self,
        topic: str,
        value: Any = None,
        **kwargs: Any,
    ) -> list[LiveData]:
        if value is None:
            return []
        return [
            LiveData(
                topic=topic,
                value=value,
                source="manual",
                source_type="manual",
                timestamp=datetime.now(
                    timezone.utc
                ).isoformat(),
                reliability=self.reliability,
            )
        ]
