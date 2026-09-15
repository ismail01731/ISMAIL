from __future__ import annotations
from typing import List, Dict, Any
from .features import FeatureExtractor
from .multi_engine import MultiModelForecaster
from .scenarios import ScenarioEngine
from .calibrator import ProbabilityCalibrator
from .selector import AutomaticModelSelector
from .registry import ModelRegistry
class ForecastEngine:
    def __init__(self):
        self.features = FeatureExtractor()
        self.multi_model = (
            MultiModelForecaster()
        )
        self.scenarios = ScenarioEngine()
        self.calibrator = (
            ProbabilityCalibrator()
        )
        self.selector = (
            AutomaticModelSelector(
                minimum_history=8,
                validation_size=3,
            )
        )
        self.registry = ModelRegistry()
    def predict(
        self,
        values: List[float],
        horizon_days: int = 30,
        evidence=None,
    ) -> Dict[str, Any]:
        clean_values = [
            float(v)
            for v in values
            if v is not None
        ]
        if not clean_values:
            return {
                "model": "none",
                "selected_model": None,
                "horizon_days": horizon_days,
                "historical_count": 0,
                "models": {},
                "selection": {},
                "baseline_forecast": [],
                "scenarios": {},
                "confidence": 0.0,
                "confidence_percent": 0.0,
                "latest_value": None,
                "expected_value": None,
                "limitations": [
                    "Insufficient historical data."
                ],
            }
        features = self.features.extract(
            clean_values
        )
        model_forecasts = (
            self.multi_model.forecast(
                clean_values,
                horizon_days,
            )
        )
        selection = (
            self.selector.select(
                clean_values
            )
        )
        selected_model = selection.get(
            "selected_model"
        )
        if not selected_model:
            selected_model = (
                "damped_linear_trend_v1"
                if
                "damped_linear_trend_v1"
                in model_forecasts
                else next(
                    (
                        name
                        for name, forecast
                        in model_forecasts.items()
                        if forecast
                    ),
                    None,
                )
            )
            selection["fallback"] = True
            selection["fallback_reason"] = (
                "Automatic selection requires "
                "more historical data."
            )
        baseline_forecast = (
            model_forecasts.get(
                selected_model,
                [],
            )
        )
        if not baseline_forecast:
            baseline_forecast = (
                self.registry.forecast(
                    selected_model,
                    clean_values,
                    horizon_days,
                )
            )
        recent_slope = features.get(
            "recent_slope",
            0.0,
        )
        volatility = features.get(
            "volatility",
            0.0,
        )
        if recent_slope > 0:
            direction = "upward"
        elif recent_slope < 0:
            direction = "downward"
        else:
            direction = "stable"
        scale = max(
            abs(features["latest"]),
            1e-9,
        )
        relative_slope = (
            abs(recent_slope)
            / scale
        )
        trend_strength = min(
            1.0,
            relative_slope * 10.0,
        )
        signed_strength = (
            trend_strength
            if direction == "upward"
            else -trend_strength
            if direction == "downward"
            else 0.0
        )
        scenario_result = (
            self.scenarios.generate(
                baseline_forecast=baseline_forecast,
                latest=clean_values[-1],
                volatility=volatility,
                trend_direction=direction,
                trend_strength=signed_strength,
                model_forecasts=model_forecasts,
            )
        )
        try:
            confidence = (
                self.calibrator.calculate(
                    values=clean_values,
                    evidence=evidence,
                    volatility=volatility,
                )
            )
        except Exception:
            confidence = 0.50
        expected_value = (
            baseline_forecast[-1]
            if baseline_forecast
            else clean_values[-1]
        )
        return {
            "model": selected_model,
            "selected_model": selected_model,
            "selection": selection,
            "horizon_days": horizon_days,
            "historical_count": len(
                clean_values
            ),
            "features": features,
            "trend": {
                "direction": direction,
                "strength": trend_strength,
                "slope": recent_slope,
            },
            "models": {
                name: {
                    "forecast": forecast,
                    "final_value": (
                        forecast[-1]
                        if forecast
                        else None
                    ),
                }
                for name, forecast
                in model_forecasts.items()
            },
            "baseline_forecast":
                baseline_forecast,
            "scenarios":
                scenario_result,
            "uncertainty":
                scenario_result.get(
                    "uncertainty",
                    {},
                ),
            "confidence":
                confidence,
            "confidence_percent":
                round(
                    confidence * 100,
                    2,
                ),
            "latest_value":
                clean_values[-1],
            "expected_value":
                expected_value,
            "limitations": [
                "Scenario probabilities are model-based estimates.",
                "Uncertainty increases with forecast horizon.",
                "Model disagreement is included in scenario uncertainty.",
                "Small datasets can produce unstable probabilities.",
                "External events may invalidate historical patterns.",
                "This is a probabilistic forecast, not a guaranteed prediction.",
            ],
        }
