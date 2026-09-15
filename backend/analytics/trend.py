from .statistics import StatisticsEngine
class TrendEngine:
    def analyze(
        self,
        values: list[float],
    ) -> dict:
        if len(values) < 2:
            return {
                "direction": "unknown",
                "strength": 0.0,
                "change_rate": 0.0,
            }
        first = values[0]
        last = values[-1]
        change = (
            StatisticsEngine
            .percentage_change(
                first,
                last,
            )
        )
        absolute_change = abs(
            change
        )
        if change > 0.02:
            direction = "upward"
        elif change < -0.02:
            direction = "downward"
        else:
            direction = "stable"
        strength = min(
            absolute_change,
            1.0,
        )
        return {
            "direction": direction,
            "strength": round(
                strength,
                4,
            ),
            "change_rate": round(
                change,
                4,
            ),
        }
