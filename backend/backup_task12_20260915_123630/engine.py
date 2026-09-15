from __future__ import annotations
from typing import List, Dict, Optional
from .features import FeatureExtractor
from .baseline import BaselineForecaster
from .scenarios import ScenarioGenerator
from .calibrator import ProbabilityCalibrator
class ForecastEngine:
    """
    Main quantitative forecasting engine.
    It combines:
    - historical features
    - trend
    - momentum
    - volatility
    - baseline projection
    - scenario generation
    - evidence quality
    - confidence estimation
    """
    def __init__(self):
        self.baseline = BaselineForecaster()
        self.scenarios = ScenarioGenerator()
    def _detect_anomalies(
        self,
        values: List[float],
        threshold: float = 2.5,
    ) -> List[int]:
        if len(values) < 3:
            return []
        features = FeatureExtractor.extract(values)
        std = features["volatility"]
        mean = features["mean"]
        if std == 0:
            return []
        anomalies = []
        for index, value in enumerate(values):
            z = abs((value - mean) / std)
            if z >= threshold:
                anomalies.append(index)
        return anomalies
    def predict(
        self,
        values: List[float],
        horizon_days: int = 30,
        evidence: Optional[List[Dict]] = None,
    ) -> Dict:
        if not values:
            raise ValueError("Historical values cannot be empty.")
        if horizon_days < 1:
            raise ValueError("horizon_days must be >= 1.")
        values = [float(value) for value in values]
        features = FeatureExtractor.extract(values)
        baseline = self.baseline.forecast(
            values,
            horizon_days=horizon_days,
        )
        slope = features["slope"]
        latest = features["latest"]
        # Trend strength normalized around latest value.
        if latest and latest != 0:
            trend_strength = slope / abs(latest)
        else:
            trend_strength = 0.0
        trend_strength = max(
            -1.0,
            min(1.0, trend_strength),
        )
        anomalies = self._detect_anomalies(values)
        scenarios = self.scenarios.generate(
            forecast=baseline["forecast"],
            volatility=(
                features["volatility"] / abs(latest)
                if latest not in (None, 0)
                else features["volatility"]
            ),
            trend_strength=trend_strength,
        )
        confidence = ProbabilityCalibrator.confidence(
            count=len(values),
            volatility=features["volatility"],
            anomalies=len(anomalies),
            evidence=evidence,
        )
        direction = "stable"
        if trend_strength > 0.01:
            direction = "upward"
        elif trend_strength < -0.01:
            direction = "downward"
        return {
            "model": "damped_linear_trend_v1",
            "horizon_days": horizon_days,
            "historical_count": len(values),
            "features": features,
            "trend": {
                "direction": direction,
                "strength": trend_strength,
                "slope": slope,
            },
            "anomalies": anomalies,
            "baseline_forecast": baseline["forecast"],
            "scenarios": scenarios,
            "confidence": confidence,
            "confidence_percent": round(confidence * 100, 2),
            "latest_value": latest,
            "expected_value": baseline["forecast"][-1],
            "limitations": [
                "This is a probabilistic forecast, not a guaranteed prediction.",
                "Forecast quality depends on historical data quality.",
                "External events may invalidate historical patterns.",
                "Longer horizons generally increase uncertainty.",
            ],
        }
