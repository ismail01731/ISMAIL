from __future__ import annotations
import math
from typing import List, Dict
class FeatureExtractor:
    """Extract statistical features from historical numeric data."""
    @staticmethod
    def mean(values: List[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
    @staticmethod
    def slope(values: List[float]) -> float:
        """Calculate least-squares linear regression slope."""
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2
        y_mean = FeatureExtractor.mean(values)
        numerator = 0.0
        denominator = 0.0
        for i, value in enumerate(values):
            dx = i - x_mean
            dy = value - y_mean
            numerator += dx * dy
            denominator += dx * dx
        if denominator == 0:
            return 0.0
        return numerator / denominator
    @staticmethod
    def volatility(values: List[float]) -> float:
        """Population standard deviation."""
        if not values:
            return 0.0
        avg = FeatureExtractor.mean(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    @staticmethod
    def momentum(values: List[float], periods: int = 5) -> float:
        if len(values) < 2:
            return 0.0
        periods = min(periods, len(values) - 1)
        previous = values[-periods - 1]
        latest = values[-1]
        if previous == 0:
            return 0.0
        return (latest - previous) / abs(previous)
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
    def z_score(value: float, values: List[float]) -> float:
        if not values:
            return 0.0
        avg = FeatureExtractor.mean(values)
        std = FeatureExtractor.volatility(values)
        if std == 0:
            return 0.0
        return (value - avg) / std
    @classmethod
    def extract(cls, values: List[float]) -> Dict:
        if not values:
            return {
                "count": 0,
                "latest": None,
                "mean": 0.0,
                "slope": 0.0,
                "volatility": 0.0,
                "momentum": 0.0,
                "percentage_change": 0.0,
                "latest_z_score": 0.0,
            }
        return {
            "count": len(values),
            "latest": values[-1],
            "mean": cls.mean(values),
            "slope": cls.slope(values),
            "volatility": cls.volatility(values),
            "momentum": cls.momentum(values),
            "percentage_change": cls.percentage_change(values),
            "latest_z_score": cls.z_score(values[-1], values),
        }
