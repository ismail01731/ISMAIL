from typing import Any
from .models import Evidence
class EvidenceCollector:
    def __init__(self):
        self.items: list[Evidence] = []
    def add(
        self,
        content: str,
        source: str,
        source_type: str = "unknown",
        reliability: float = 0.50,
        relevance: float = 0.50,
        freshness: float = 1.00,
        metadata: dict[str, Any] | None = None,
    ) -> Evidence:
        evidence = Evidence(
            content=content,
            source=source,
            source_type=source_type,
            reliability=self._clamp(reliability),
            relevance=self._clamp(relevance),
            freshness=self._clamp(freshness),
            metadata=metadata or {},
        )
        self.items.append(evidence)
        return evidence
    def get_all(self) -> list[Evidence]:
        return list(self.items)
    def get_quality_sorted(self) -> list[Evidence]:
        return sorted(
            self.items,
            key=lambda item: item.quality_score(),
            reverse=True,
        )
    def clear(self):
        self.items.clear()
    @staticmethod
    def _clamp(value: float) -> float:
        return min(max(float(value), 0.0), 1.0)
