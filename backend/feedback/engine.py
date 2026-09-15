from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Optional
from .calibration import ConfidenceCalibration
from .metrics import AccuracyMetrics
from .storage import FeedbackStorage
class FeedbackEngine:
    def __init__(
        self,
        storage: Optional[FeedbackStorage] = None,
    ):
        self.storage = (
            storage
            or FeedbackStorage()
        )
    def record(
        self,
        prediction_id: int,
        predicted_value: float,
        actual_value: float,
        confidence: float,
        notes: Optional[str] = None,
    ) -> Dict:
        predicted_value = float(
            predicted_value
        )
        actual_value = float(
            actual_value
        )
        confidence = max(
            0.0,
            min(1.0, float(confidence)),
        )
        absolute_error = abs(
            predicted_value - actual_value
        )
        if actual_value == 0:
            percentage_error = 0.0
        else:
            percentage_error = (
                absolute_error
                / abs(actual_value)
            )
        directional_accuracy = (
            (predicted_value >= 0)
            == (actual_value >= 0)
        )
        feedback = {
            "prediction_id": prediction_id,
            "predicted_value": predicted_value,
            "actual_value": actual_value,
            "confidence": confidence,
            "absolute_error": absolute_error,
            "percentage_error": percentage_error,
            "directional_accuracy":
                directional_accuracy,
            "notes": notes,
            "created_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }
        feedback_id = (
            self.storage.insert(feedback)
        )
        feedback["id"] = feedback_id
        return feedback
    def summary(self) -> Dict:
        rows = self.storage.list_all()
        if not rows:
            return {
                "count": 0,
                "accuracy": {
                    "mae": 0.0,
                    "mape": 0.0,
                    "rmse": 0.0,
                    "directional_accuracy": 0.0,
                },
                "calibration": {
                    "status":
                        "insufficient_data"
                },
            }
        predicted = [
            row["predicted_value"]
            for row in rows
        ]
        actual = [
            row["actual_value"]
            for row in rows
        ]
        confidences = [
            row["confidence"]
            for row in rows
        ]
        correct = [
            bool(
                row["directional_accuracy"]
            )
            for row in rows
        ]
        return {
            "count": len(rows),
            "accuracy":
                AccuracyMetrics.summary(
                    predicted,
                    actual,
                ),
            "calibration":
                ConfidenceCalibration.analyze(
                    confidences,
                    correct,
                ),
            "average_absolute_error":
                sum(
                    row["absolute_error"]
                    for row in rows
                ) / len(rows),
            "average_percentage_error":
                sum(
                    row["percentage_error"]
                    for row in rows
                ) / len(rows),
        }
