from __future__ import annotations
from typing import List
class BaselineForecaster:
    """
    More conservative baseline forecaster.
    Uses:
    - recent trend instead of blindly extrapolating the full history
    - damping that increases with forecast horizon
    - optional growth cap based on historical volatility
    """
    def __init__(
        self,
        damping: float = 0.85,
        recent_window: int = 5,
        max_relative_change: float = 0.60,
    ):
        self.damping = float(damping)
        self.recent_window = int(recent_window)
        self.max_relative_change = float(max_relative_change)
    @staticmethod
    def _slope(values: List[float]) -> float:
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
    def forecast(
        self,
        values: List[float],
        horizon_days: int = 30,
    ) -> List[float]:
        if not values:
            return []
        if horizon_days <= 0:
            return []
        clean = [float(v) for v in values]
        latest = clean[-1]
        if len(clean) < 2:
            return [latest for _ in range(horizon_days)]
        recent = clean[-min(self.recent_window, len(clean)):]
        slope = self._slope(recent)
        forecasts = []
        for day in range(1, horizon_days + 1):
            # Damping increases with horizon.
            horizon_damping = self.damping ** (day / 5.0)
            projected_change = slope * horizon_damping
            # Prevent runaway extrapolation.
            max_total_change = max(
                abs(latest) * self.max_relative_change,
                1e-9,
            )
            total_change = projected_change * day
            if total_change > max_total_change:
                total_change = max_total_change
            elif total_change < -max_total_change:
                total_change = -max_total_change
            projected = latest + total_change
            forecasts.append(float(projected))
        return forecasts
