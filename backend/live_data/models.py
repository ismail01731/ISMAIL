from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
@dataclass
class LiveData:
    topic: str
    value: Any
    source: str
    source_type: str = "api"
    timestamp: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )
    reliability: float = 0.50
    metadata: dict[str, Any] = field(
        default_factory=dict
    )
    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "value": self.value,
            "source": self.source,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "reliability": self.reliability,
            "metadata": self.metadata,
        }
