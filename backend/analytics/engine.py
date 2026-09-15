from __future__ import annotations
from typing import List, Dict, Any
from .statistics import StatisticsEngine
from .trend import TrendEngine
from .anomaly import AnomalyDetector
from .quality import DataQualityEngine
class HistoricalAnalytics:
    def __init__(self):
        self.statistics = (
            StatisticsEngine()
        )
        self.trend = (
            TrendEngine()
        )
        self.anomaly = (
            AnomalyDetector()
        )
        self.quality = (
            DataQualityEngine()
        )
    def analyze(
        self,
        values: List[float],
        window: int = 5,
    ) -> Dict[str, Any]:
        clean_values = [
            float(v)
            for v in values
            if v is not None
        ]
        if not clean_values:
            return {
                "count": 0,
                "latest": None,
                "mean": None,
                "median": None,
                "standard_deviation": 0.0,
                "moving_average": [],
                "momentum": 0.0,
                "trend": {
                    "direction": "unknown",
                    "strength": 0.0,
                    "change_rate": 0.0,
                },
                "anomalies": [],
                "quality": self.quality.score(
                    []
                ),
            }
        return {
            "count": len(
                clean_values
            ),
            "latest":
                clean_values[-1],
            "mean":
                self.statistics.mean(
                    clean_values
                ),
            "median":
                self.statistics.median(
                    clean_values
                ),
            "standard_deviation":
                self.statistics.standard_deviation(
                    clean_values
                ),
            "moving_average":
                self.statistics.moving_average(
                    clean_values,
                    window,
                ),
            "momentum":
                self.statistics.momentum(
                    clean_values,
                    window,
                ),
            "trend":
                self.trend.analyze(
                    clean_values
                ),
            "anomalies":
                self.anomaly.detect(
                    clean_values
                ),
            "quality":
                self.quality.score(
                    values
                ),
        }
