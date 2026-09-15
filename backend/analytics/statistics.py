from math import sqrt
from statistics import mean, median
class StatisticsEngine:
    @staticmethod
    def mean(values: list[float]) -> float:
        if not values:
            return 0.0
        return float(
            mean(values)
        )
    @staticmethod
    def median(values: list[float]) -> float:
        if not values:
            return 0.0
        return float(
            median(values)
        )
    @staticmethod
    def standard_deviation(
        values: list[float],
    ) -> float:
        if len(values) < 2:
            return 0.0
        avg = mean(values)
        variance = sum(
            (x - avg) ** 2
            for x in values
        ) / len(values)
        return sqrt(variance)
    @staticmethod
    def moving_average(
        values: list[float],
        window: int = 5,
    ) -> list[float]:
        if not values:
            return []
        window = max(
            1,
            min(window, len(values)),
        )
        result = []
        for i in range(
            len(values)
        ):
            start = max(
                0,
                i - window + 1,
            )
            section = values[
                start:i + 1
            ]
            result.append(
                round(
                    mean(section),
                    6,
                )
            )
        return result
    @staticmethod
    def percentage_change(
        first: float,
        last: float,
    ) -> float:
        if first == 0:
            return 0.0
        return (
            (last - first)
            / abs(first)
        )
    @staticmethod
    def momentum(
        values: list[float],
        periods: int = 5,
    ) -> float:
        if len(values) <= periods:
            return 0.0
        old = values[
            -(periods + 1)
        ]
        new = values[-1]
        return StatisticsEngine.percentage_change(
            old,
            new,
        )
