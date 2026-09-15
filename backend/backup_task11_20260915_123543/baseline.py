from __future__ import annotations
from typing import List, Dict
from .features import FeatureExtractor
class BaselineForecaster:
    """
    Damped linear-trend forecasting model.
    This is intentionally conservative. It prevents a strong historical
    trend from producing unrealistic infinite extrapolation.
    """
    def __init__(self, damping: float = 0.85):
        self.damping = damping
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> Dict:
        if not values:
            return {
                "forecast": [],
                "slope": 0.0,
                "last_value": None,
            }
        if len(values) == 1:
            return {
                "forecast": [values[-1]] * horizon_days,
                "slope": 0.0,
                "last_value": values[-1],
            }
        slope = FeatureExtractor.slope(values)
        last_value = values[-1]
        forecast = []
        for day in range(1, horizon_days + 1):
            damped_step = day * self.damping
            predicted = last_value + (slope * damped_step)
            forecast.append(predicted)
        return {
            "forecast": forecast,
            "slope": slope,
            "last_value": last_value,
        }
