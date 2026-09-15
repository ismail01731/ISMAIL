from __future__ import annotations
from typing import List, Dict, Any
from .multiple_models import (
    NaiveForecaster,
    MovingAverageForecaster,
    ExponentialSmoothingForecaster,
)
from .baseline import BaselineForecaster
class ModelRegistry:
    def __init__(self):
        self.models = {
            "naive_v1": NaiveForecaster(),
            "moving_average_v1":
                MovingAverageForecaster(
                    window=5
                ),
            "exponential_smoothing_v1":
                ExponentialSmoothingForecaster(
                    alpha=0.35
                ),
            "damped_linear_trend_v1":
                BaselineForecaster(
                    damping=0.85,
                    recent_window=5,
                    max_relative_change=0.60,
                ),
        }
    def get(self, name: str):
        return self.models.get(name)
    def forecast(
        self,
        name: str,
        values: List[float],
        horizon_days: int,
    ) -> List[float]:
        model = self.get(name)
        if model is None:
            return []
        return model.forecast(
            values,
            horizon_days,
        )
    def names(self):
        return list(self.models.keys())
