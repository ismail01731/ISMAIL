from __future__ import annotations
from typing import List, Dict, Any
from .features import FeatureExtractor
from .multi_engine import MultiModelForecaster
from .scenarios import ScenarioGenerator
from .calibrator import ProbabilityCalibrator
class ForecastEngine:
    def __init__(self):
        self.features = FeatureExtractor()
        self.multi_model = MultiModelForecaster()
        self.scenarios = ScenarioGenerator()
        self.calibrator = ProbabilityCalibrator()
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
                "horizon_days": horizon_days,
                "historical_count": 0,
                "models": {},
                "selected_model": None,
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
        features = self.features.extract(clean_values)
        model_forecasts = self.multi_model.forecast(
            clean_values,
            horizon_days,
        )
        # Keep damped trend as the current primary baseline.
        selected_model = "damped_linear_trend_v1"
        baseline_forecast = model_forecasts.get(
            selected_model,
            [],
        )
        if not baseline_forecast:
            selected_model = next(
                (
                    name
                    for name, forecast in model_forecasts.items()
                    if forecast
                ),
                None,
            )
            baseline_forecast = (
                model_forecasts.get(selected_model, [])
                if selected_model
                else []
            )
        recent_slope = features.get("recent_slope", 0.0)
        volatility = features.get("volatility", 0.0)
        if recent_slope > 0:
            direction = "upward"
        elif recent_slope < 0:
            direction = "downward"
        else:
            direction = "stable"
        scale = max(abs(features["latest"]), 1e-9)
        relative_slope = abs(recent_slope) / scale
        trend_strength = min(
            1.0,
            relative_slope * 10.0
        )
        scenarios = self.scenarios.generate(
            baseline_forecast=baseline_forecast,
            volatility=volatility,
            trend_strength=(
                trend_strength
                if direction == "upward"
                else -trend_strength
                if direction == "downward"
                else 0.0
            ),
        )
        try:
            confidence = self.calibrator.calculate(
                values=clean_values,
                evidence=evidence,
                volatility=volatility,
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
            "horizon_days": horizon_days,
            "historical_count": len(clean_values),
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
                for name, forecast in model_forecasts.items()
            },
            "baseline_forecast": baseline_forecast,
            "scenarios": scenarios,
            "confidence": confidence,
            "confidence_percent": round(
                confidence * 100,
                2,
            ),
            "latest_value": clean_values[-1],
            "expected_value": expected_value,
            "limitations": [
                "Multiple forecasting models are provided.",
                "The current selected model is not yet automatically optimized.",
                "Model selection will be improved using historical backtesting.",
                "This is a probabilistic forecast, not a guaranteed prediction.",
                "External events may invalidate historical patterns.",
            ],
        }
