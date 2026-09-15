from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
@dataclass
class Evidence:
    content: str
    source: str
    source_type: str = "unknown"
    reliability: float = 0.50
    relevance: float = 0.50
    freshness: float = 1.00
    timestamp: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )
    metadata: dict[str, Any] = field(
        default_factory=dict
    )
    def quality_score(self) -> float:
        score = (
            self.reliability * 0.40
            + self.relevance * 0.35
            + self.freshness * 0.25
        )
        return round(
            min(max(score, 0.0), 1.0),
            4,
        )
    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "source": self.source,
            "source_type": self.source_type,
            "reliability": self.reliability,
            "relevance": self.relevance,
            "freshness": self.freshness,
            "timestamp": self.timestamp,
            "quality_score": self.quality_score(),
            "metadata": self.metadata,
        }
