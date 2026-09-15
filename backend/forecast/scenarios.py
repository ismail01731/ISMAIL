from __future__ import annotations
from typing import List, Dict, Optional
import math
class ScenarioEngine:
    """
    Scenario + uncertainty engine.
    Factors:
    - historical volatility
    - model disagreement
    - trend direction
    - trend strength
    - forecast horizon
    Scenarios:
    - downside
    - base
    - upside
    This engine does not claim certainty.
    Probabilities represent model-based scenario weights.
    """
    def __init__(
        self,
        volatility_weight: float = 0.50,
        disagreement_weight: float = 0.50,
    ):
        self.volatility_weight = float(
            volatility_weight
        )
        self.disagreement_weight = float(
            disagreement_weight
        )
    @staticmethod
    def _clamp(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        return max(
            minimum,
            min(maximum, value),
        )
    @staticmethod
    def _normalize(
        values: Dict[str, float]
    ) -> Dict[str, float]:
        total = sum(
            max(0.0, float(v))
            for v in values.values()
        )
        if total <= 0:
            equal = 1.0 / len(values)
            return {
                key: equal
                for key in values
            }
        return {
            key: max(0.0, float(value)) / total
            for key, value in values.items()
        }
    @staticmethod
    def _model_disagreement(
        model_forecasts: Optional[Dict[str, List[float]]],
        latest: float,
    ) -> float:
        if not model_forecasts:
            return 0.0
        final_values = []
        for forecast in model_forecasts.values():
            if not forecast:
                continue
            final_values.append(
                float(forecast[-1])
            )
        if len(final_values) < 2:
            return 0.0
        mean = sum(final_values) / len(final_values)
        variance = sum(
            (value - mean) ** 2
            for value in final_values
        ) / len(final_values)
        std = math.sqrt(variance)
        scale = max(
            abs(float(latest)),
            1e-9,
        )
        return std / scale
    @staticmethod
    def _volatility_ratio(
        volatility: float,
        latest: float,
    ) -> float:
        scale = max(
            abs(float(latest)),
            1e-9,
        )
        return abs(
            float(volatility)
        ) / scale
    def generate(
        self,
        baseline_forecast: List[float],
        latest: float,
        volatility: float,
        trend_direction: str = "stable",
        trend_strength: float = 0.0,
        model_forecasts: Optional[
            Dict[str, List[float]]
        ] = None,
    ) -> Dict:
        if not baseline_forecast:
            return {
                "probabilities": {
                    "downside": 0.25,
                    "base": 0.50,
                    "upside": 0.25,
                },
                "downside": {
                    "probability": 0.25,
                    "forecast": [],
                },
                "base": {
                    "probability": 0.50,
                    "forecast": [],
                },
                "upside": {
                    "probability": 0.25,
                    "forecast": [],
                },
                "uncertainty": {
                    "level": "high",
                    "volatility_ratio": 0.0,
                    "model_disagreement": 0.0,
                },
            }
        volatility_ratio = self._volatility_ratio(
            volatility,
            latest,
        )
        disagreement = self._model_disagreement(
            model_forecasts,
            latest,
        )
        # Combined uncertainty.
        uncertainty = (
            self.volatility_weight
            * volatility_ratio
            + self.disagreement_weight
            * disagreement
        )
        # Convert uncertainty into a bounded value.
        uncertainty = self._clamp(
            uncertainty,
            0.0,
            1.0,
        )
        # Trend bias.
        strength = self._clamp(
            abs(float(trend_strength)),
            0.0,
            1.0,
        )
        if trend_direction == "upward":
            trend_bias = strength * 0.12
        elif trend_direction == "downward":
            trend_bias = -strength * 0.12
        else:
            trend_bias = 0.0
        # Higher uncertainty increases probability
        # of downside/upside outcomes and reduces
        # confidence in the base scenario.
        base_probability = (
            0.60
            - uncertainty * 0.20
        )
        base_probability = self._clamp(
            base_probability,
            0.35,
            0.60,
        )
        remaining = 1.0 - base_probability
        downside_probability = (
            remaining / 2.0
            - trend_bias
        )
        upside_probability = (
            remaining / 2.0
            + trend_bias
        )
        raw_probabilities = {
            "downside": downside_probability,
            "base": base_probability,
            "upside": upside_probability,
        }
        probabilities = self._normalize(
            raw_probabilities
        )
        # Forecast bands.
        #
        # Uncertainty grows with horizon using sqrt(horizon).
        spread_base = max(
            abs(float(volatility)),
            abs(float(latest)) * 0.01,
            1e-9,
        )
        downside = []
        upside = []
        for index, value in enumerate(
            baseline_forecast
        ):
            horizon_factor = math.sqrt(
                index + 1
            )
            uncertainty_band = (
                spread_base
                * (
                    0.45
                    + uncertainty
                )
                * horizon_factor
            )
            downside.append(
                float(value - uncertainty_band)
            )
            upside.append(
                float(value + uncertainty_band)
            )
        if uncertainty < 0.10:
            uncertainty_level = "low"
        elif uncertainty < 0.25:
            uncertainty_level = "moderate"
        elif uncertainty < 0.50:
            uncertainty_level = "high"
        else:
            uncertainty_level = "very_high"
        return {
            "probabilities": probabilities,
            "downside": {
                "probability": probabilities[
                    "downside"
                ],
                "forecast": downside,
            },
            "base": {
                "probability": probabilities[
                    "base"
                ],
                "forecast": list(
                    baseline_forecast
                ),
            },
            "upside": {
                "probability": probabilities[
                    "upside"
                ],
                "forecast": upside,
            },
            "uncertainty": {
                "level": uncertainty_level,
                "score": round(
                    uncertainty,
                    6,
                ),
                "volatility_ratio": round(
                    volatility_ratio,
                    6,
                ),
                "model_disagreement": round(
                    disagreement,
                    6,
                ),
                "horizon_sensitive": True,
            },
            "method": (
                "volatility + model disagreement "
                "+ trend bias + horizon uncertainty"
            ),
        }
