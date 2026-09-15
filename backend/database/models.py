from dataclasses import dataclass, field
from typing import Any
@dataclass
class HistoricalRecord:
    topic: str
    value: str
    source: str = ""
    source_type: str = "unknown"
    timestamp: str = ""
    reliability: float = 0.50
    metadata: dict[str, Any] = field(
        default_factory=dict
    )
@dataclass
class PredictionRecord:
    question: str
    horizon_days: int
    prediction: dict[str, Any]
    confidence: float = 0.0
