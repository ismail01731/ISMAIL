from __future__ import annotations
from typing import List, Dict
import math
class ScenarioGenerator:
    def generate(
        self,
        baseline_forecast: List[float],
        volatility: float,
        trend_strength: float = 0.0,
    ) -> Dict[str, Dict]:
        if not baseline_forecast:
            return {
                "downside": {"probability": 0.25, "forecast": []},
                "base": {"probability": 0.50, "forecast": []},
                "upside": {"probability": 0.25, "forecast": []},
            }
        # Use a bounded uncertainty band.
        spread = max(volatility * 0.50, 1e-9)
        downside = []
        upside = []
        for index, value in enumerate(baseline_forecast):
            horizon_factor = math.sqrt(index + 1)
            band = spread * horizon_factor
            downside.append(float(value - band))
            upside.append(float(value + band))
        # Strong upward trend slightly favors upside.
        trend_bias = max(-0.10, min(0.10, trend_strength * 0.20))
        base_probability = 0.50
        downside_probability = 0.25 - trend_bias
        upside_probability = 0.25 + trend_bias
        total = (
            downside_probability
            + base_probability
            + upside_probability
        )
        return {
            "downside": {
                "probability": downside_probability / total,
                "forecast": downside,
            },
            "base": {
                "probability": base_probability / total,
                "forecast": list(baseline_forecast),
            },
            "upside": {
                "probability": upside_probability / total,
                "forecast": upside,
            },
        }
