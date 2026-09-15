from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
@dataclass
class PredictionFeedback:
    prediction_id: int
    predicted_value: float
    actual_value: float
    confidence: float
    created_at: str
    notes: Optional[str] = None
    @property
    def absolute_error(self) -> float:
        return abs(
            self.predicted_value - self.actual_value
        )
    @property
    def percentage_error(self) -> float:
        if self.actual_value == 0:
            return 0.0
        return (
            self.absolute_error
            / abs(self.actual_value)
        )
    @property
    def directional_accuracy(self) -> bool:
        return (
            (self.predicted_value >= 0)
            == (self.actual_value >= 0)
        )
    def to_dict(self):
        return {
            "prediction_id": self.prediction_id,
            "predicted_value": self.predicted_value,
            "actual_value": self.actual_value,
            "confidence": self.confidence,
            "absolute_error": self.absolute_error,
            "percentage_error": self.percentage_error,
            "directional_accuracy": self.directional_accuracy,
            "created_at": self.created_at,
            "notes": self.notes,
        }
