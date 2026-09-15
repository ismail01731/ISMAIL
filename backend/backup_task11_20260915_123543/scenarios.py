from __future__ import annotations
from typing import List, Dict
class ScenarioGenerator:
    """Generate probabilistic future scenarios."""
    @staticmethod
    def _normalize(probabilities: Dict[str, float]) -> Dict[str, float]:
        total = sum(probabilities.values())
        if total <= 0:
            count = len(probabilities)
            return {
                key: 1.0 / count
                for key in probabilities
            }
        return {
            key: value / total
            for key, value in probabilities.items()
        }
    def generate(
        self,
        forecast: List[float],
        volatility: float,
        trend_strength: float,
    ) -> Dict:
        if not forecast:
            return {
                "downside": {"probability": 0.33, "forecast": []},
                "base": {"probability": 0.34, "forecast": []},
                "upside": {"probability": 0.33, "forecast": []},
            }
        last = forecast[-1]
        # Volatility controls scenario spread.
        spread = max(abs(last) * volatility * 0.50, 0.000001)
        if abs(last) < 1:
            spread = max(volatility * 0.50, 0.000001)
        # Trend influences probabilities.
        trend_bias = max(-0.15, min(0.15, trend_strength * 0.50))
        probabilities = {
            "downside": 0.25 - trend_bias,
            "base": 0.50,
            "upside": 0.25 + trend_bias,
        }
        probabilities = self._normalize(probabilities)
        downside = []
        base = []
        upside = []
        for value in forecast:
            base.append(value)
            downside.append(value - spread)
            upside.append(value + spread)
        return {
            "downside": {
                "probability": probabilities["downside"],
                "forecast": downside,
            },
            "base": {
                "probability": probabilities["base"],
                "forecast": base,
            },
            "upside": {
                "probability": probabilities["upside"],
                "forecast": upside,
            },
        }
