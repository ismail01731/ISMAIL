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
        values: list[float],
        window: int = 5,
    ) -> dict:
        clean_values = [
            float(value)
            for value in values
            if value is not None
        ]
        if not clean_values:
            return {
                "success": False,
                "reason": "No numeric data available.",
            }
        moving_average = (
            self.statistics
            .moving_average(
                clean_values,
                window,
            )
        )
        trend = self.trend.analyze(
            clean_values
        )
        anomalies = (
            self.anomaly.detect(
                clean_values
            )
        )
        quality = (
            self.quality.score(
                clean_values
            )
        )
        return {
            "success": True,
            "data": {
                "count": len(
                    clean_values
                ),
                "latest": clean_values[-1],
                "mean": round(
                    self.statistics.mean(
                        clean_values
                    ),
                    6,
                ),
                "median": round(
                    self.statistics.median(
                        clean_values
                    ),
                    6,
                ),
                "standard_deviation":
                    round(
                        self.statistics
                        .standard_deviation(
                            clean_values
                        ),
                        6,
                    ),
                "moving_average":
                    moving_average,
                "momentum":
                    round(
                        self.statistics
                        .momentum(
                            clean_values
                        ),
                        6,
                    ),
            },
            "trend": trend,
            "anomalies": anomalies,
            "quality": quality,
        }
