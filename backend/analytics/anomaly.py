from .statistics import StatisticsEngine
class AnomalyDetector:
    def detect(
        self,
        values: list[float],
        threshold: float = 2.5,
    ) -> list[dict]:
        if len(values) < 3:
            return []
        avg = StatisticsEngine.mean(
            values
        )
        std = StatisticsEngine.standard_deviation(
            values
        )
        if std == 0:
            return []
        anomalies = []
        for index, value in enumerate(
            values
        ):
            z_score = (
                (value - avg)
                / std
            )
            if abs(z_score) >= threshold:
                anomalies.append(
                    {
                        "index": index,
                        "value": value,
                        "z_score": round(
                            z_score,
                            4,
                        ),
                    }
                )
        return anomalies
