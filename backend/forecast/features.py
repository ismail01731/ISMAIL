from __future__ import annotations
from typing import List, Dict
import math
class FeatureExtractor:
    @staticmethod
    def mean(values: List[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
    @staticmethod
    def slope(values: List[float]) -> float:
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        numerator = sum(
            (i - x_mean) * (value - y_mean)
            for i, value in enumerate(values)
        )
        denominator = sum(
            (i - x_mean) ** 2
            for i in range(n)
        )
        if denominator == 0:
            return 0.0
        return numerator / denominator
    @staticmethod
    def volatility(values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = FeatureExtractor.mean(values)
        variance = sum(
            (value - mean) ** 2
            for value in values
        ) / len(values)
        return math.sqrt(variance)
    @staticmethod
    def momentum(values: List[float], periods: int = 3) -> float:
        if len(values) <= periods:
            return 0.0
        old = values[-periods - 1]
        new = values[-1]
        if old == 0:
            return 0.0
        return (new - old) / abs(old)
    @staticmethod
    def percentage_change(values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        first = values[0]
        last = values[-1]
        if first == 0:
            return 0.0
        return (last - first) / abs(first)
    @staticmethod
    def z_score(values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = FeatureExtractor.mean(values)
        std = FeatureExtractor.volatility(values)
        if std == 0:
            return 0.0
        return (values[-1] - mean) / std
    @staticmethod
    def recent_slope(values: List[float], window: int = 5) -> float:
        if len(values) < 2:
            return 0.0
        recent = values[-min(window, len(values)):]
        return FeatureExtractor.slope(recent)
    @classmethod
    def extract(cls, values: List[float]) -> Dict[str, float]:
        return {
            "count": len(values),
            "latest": values[-1] if values else 0.0,
            "mean": cls.mean(values),
            "slope": cls.slope(values),
            "recent_slope": cls.recent_slope(values),
            "volatility": cls.volatility(values),
            "momentum": cls.momentum(values),
            "percentage_change": cls.percentage_change(values),
            "latest_z_score": cls.z_score(values),
        }
