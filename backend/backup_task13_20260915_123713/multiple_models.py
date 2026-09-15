from __future__ import annotations
from typing import List
class NaiveForecaster:
    """
    Last-value baseline.
    Assumes the next values remain close to the latest observation.
    """
    name = "naive_v1"
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> List[float]:
        if not values or horizon_days <= 0:
            return []
        latest = float(values[-1])
        return [latest for _ in range(horizon_days)]
class MovingAverageForecaster:
    """
    Forecasts using the recent moving average.
    """
    name = "moving_average_v1"
    def __init__(self, window: int = 5):
        self.window = max(2, int(window))
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> List[float]:
        if not values or horizon_days <= 0:
            return []
        recent = values[-min(self.window, len(values)):]
        average = sum(recent) / len(recent)
        return [float(average) for _ in range(horizon_days)]
class ExponentialSmoothingForecaster:
    """
    Simple exponential smoothing.
    Higher alpha reacts faster to recent changes.
    """
    name = "exponential_smoothing_v1"
    def __init__(self, alpha: float = 0.35):
        self.alpha = max(0.01, min(0.99, float(alpha)))
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> List[float]:
        if not values or horizon_days <= 0:
            return []
        level = float(values[0])
        for value in values[1:]:
            level = (
                self.alpha * float(value)
                + (1.0 - self.alpha) * level
            )
        return [float(level) for _ in range(horizon_days)]
