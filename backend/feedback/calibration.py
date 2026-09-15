from __future__ import annotations
from typing import Dict, List
class ConfidenceCalibration:
    @staticmethod
    def analyze(
        confidences: List[float],
        correct: List[bool],
    ) -> Dict:
        if not confidences or not correct:
            return {
                "count": 0,
                "average_confidence": 0.0,
                "actual_accuracy": 0.0,
                "calibration_error": 0.0,
                "status": "insufficient_data",
            }
        n = min(
            len(confidences),
            len(correct),
        )
        confidences = confidences[:n]
        correct = correct[:n]
        average_confidence = (
            sum(confidences) / n
        )
        actual_accuracy = (
            sum(
                1
                for value in correct
                if value
            )
            / n
        )
        calibration_error = abs(
            average_confidence
            - actual_accuracy
        )
        if calibration_error <= 0.05:
            status = "well_calibrated"
        elif calibration_error <= 0.15:
            status = "moderately_calibrated"
        else:
            status = "poorly_calibrated"
        return {
            "count": n,
            "average_confidence":
                average_confidence,
            "actual_accuracy":
                actual_accuracy,
            "calibration_error":
                calibration_error,
            "status": status,
        }
