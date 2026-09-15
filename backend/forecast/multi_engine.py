from __future__ import annotations
from typing import List, Dict
from .baseline import BaselineForecaster
from .multiple_models import (
    NaiveForecaster,
    MovingAverageForecaster,
    ExponentialSmoothingForecaster,
)
class MultiModelForecaster:
    """
    Runs multiple independent forecasting models.
    This component does NOT select the best model yet.
    Model selection/backtesting is handled in a later task.
    """
    def __init__(self):
        self.models = {
            "naive_v1": NaiveForecaster(),
            "moving_average_v1": MovingAverageForecaster(window=5),
            "exponential_smoothing_v1": ExponentialSmoothingForecaster(
                alpha=0.35
            ),
            "damped_linear_trend_v1": BaselineForecaster(
                damping=0.85,
                recent_window=5,
                max_relative_change=0.60,
            ),
        }
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> Dict[str, List[float]]:
        if not values:
            return {
                name: []
                for name in self.models
            }
        results = {}
        for name, model in self.models.items():
            try:
                results[name] = model.forecast(
                    values,
                    horizon_days,
                )
            except Exception:
                results[name] = []
        return results
