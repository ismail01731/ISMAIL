from __future__ import annotations
from typing import Dict, List
class AccuracyMetrics:
    @staticmethod
    def mae(
        predicted: List[float],
        actual: List[float],
    ) -> float:
        if not predicted or not actual:
            return 0.0
        n = min(
            len(predicted),
            len(actual),
        )
        errors = [
            abs(predicted[i] - actual[i])
            for i in range(n)
        ]
        return sum(errors) / n
    @staticmethod
    def mape(
        predicted: List[float],
        actual: List[float],
    ) -> float:
        if not predicted or not actual:
            return 0.0
        errors = []
        for p, a in zip(predicted, actual):
            if a == 0:
                continue
            errors.append(
                abs(p - a) / abs(a)
            )
        if not errors:
            return 0.0
        return sum(errors) / len(errors)
    @staticmethod
    def rmse(
        predicted: List[float],
        actual: List[float],
    ) -> float:
        if not predicted or not actual:
            return 0.0
        n = min(
            len(predicted),
            len(actual),
        )
        squared_errors = [
            (predicted[i] - actual[i]) ** 2
            for i in range(n)
        ]
        return (
            sum(squared_errors) / n
        ) ** 0.5
    @staticmethod
    def directional_accuracy(
        predicted: List[float],
        actual: List[float],
    ) -> float:
        if not predicted or not actual:
            return 0.0
        n = min(
            len(predicted),
            len(actual),
        )
        correct = 0
        for i in range(n):
            if (
                (predicted[i] >= 0)
                == (actual[i] >= 0)
            ):
                correct += 1
        return correct / n
    @staticmethod
    def summary(
        predicted: List[float],
        actual: List[float],
    ) -> Dict:
        return {
            "count": min(
                len(predicted),
                len(actual),
            ),
            "mae": AccuracyMetrics.mae(
                predicted,
                actual,
            ),
            "mape": AccuracyMetrics.mape(
                predicted,
                actual,
            ),
            "rmse": AccuracyMetrics.rmse(
                predicted,
                actual,
            ),
            "directional_accuracy":
                AccuracyMetrics.directional_accuracy(
                    predicted,
                    actual,
                ),
        }
