from __future__ import annotations
from typing import List, Dict, Any
from .multi_engine import MultiModelForecaster
class BacktestingEngine:
    """
    Walk-forward style backtesting for the forecasting models.
    The model predicts future values using only data available
    before the validation point.
    Metrics:
    - MAE
    - RMSE
    - MAPE
    - directional accuracy
    """
    def __init__(self):
        self.multi_model = MultiModelForecaster()
    @staticmethod
    def mae(actual: List[float], predicted: List[float]) -> float:
        pairs = list(zip(actual, predicted))
        if not pairs:
            return 0.0
        return sum(
            abs(a - p)
            for a, p in pairs
        ) / len(pairs)
    @staticmethod
    def rmse(actual: List[float], predicted: List[float]) -> float:
        pairs = list(zip(actual, predicted))
        if not pairs:
            return 0.0
        mse = sum(
            (a - p) ** 2
            for a, p in pairs
        ) / len(pairs)
        return mse ** 0.5
    @staticmethod
    def mape(actual: List[float], predicted: List[float]) -> float:
        errors = []
        for a, p in zip(actual, predicted):
            if a == 0:
                continue
            errors.append(
                abs((a - p) / abs(a))
            )
        if not errors:
            return 0.0
        return sum(errors) / len(errors)
    @staticmethod
    def directional_accuracy(
        training: List[float],
        actual: List[float],
        predicted: List[float],
    ) -> float:
        if not actual or not predicted or len(training) < 1:
            return 0.0
        previous = float(training[-1])
        correct = 0
        total = 0
        for a, p in zip(actual, predicted):
            actual_direction = (
                1 if a > previous
                else -1 if a < previous
                else 0
            )
            predicted_direction = (
                1 if p > previous
                else -1 if p < previous
                else 0
            )
            if actual_direction == predicted_direction:
                correct += 1
            total += 1
            previous = a
        if total == 0:
            return 0.0
        return correct / total
    def evaluate(
        self,
        values: List[float],
        validation_size: int = 3,
    ) -> Dict[str, Any]:
        clean = [
            float(v)
            for v in values
            if v is not None
        ]
        if len(clean) < 5:
            return {
                "success": False,
                "message": "At least 5 historical values are recommended for backtesting.",
                "data_count": len(clean),
            }
        validation_size = max(
            1,
            min(
                int(validation_size),
                len(clean) - 2,
            ),
        )
        split = len(clean) - validation_size
        training = clean[:split]
        actual = clean[split:]
        forecasts = self.multi_model.forecast(
            training,
            validation_size,
        )
        models = {}
        for name, predicted in forecasts.items():
            if not predicted:
                continue
            predicted = predicted[:validation_size]
            models[name] = {
                "mae": round(
                    self.mae(actual, predicted),
                    6,
                ),
                "rmse": round(
                    self.rmse(actual, predicted),
                    6,
                ),
                "mape": round(
                    self.mape(actual, predicted),
                    6,
                ),
                "mape_percent": round(
                    self.mape(actual, predicted) * 100,
                    2,
                ),
                "directional_accuracy": round(
                    self.directional_accuracy(
                        training,
                        actual,
                        predicted,
                    ),
                    6,
                ),
                "directional_accuracy_percent": round(
                    self.directional_accuracy(
                        training,
                        actual,
                        predicted,
                    ) * 100,
                    2,
                ),
                "predicted": predicted,
                "actual": actual,
            }
        ranked = sorted(
            models.items(),
            key=lambda item: (
                item[1]["mae"],
                item[1]["rmse"],
            ),
        )
        ranking = [
            {
                "rank": index + 1,
                "model": name,
                "mae": result["mae"],
                "rmse": result["rmse"],
                "mape_percent": result["mape_percent"],
                "directional_accuracy_percent": result[
                    "directional_accuracy_percent"
                ],
            }
            for index, (name, result)
            in enumerate(ranked)
        ]
        return {
            "success": True,
            "data_count": len(clean),
            "training_count": len(training),
            "validation_count": len(actual),
            "training_values": training,
            "actual_values": actual,
            "models": models,
            "ranking": ranking,
            "best_model": (
                ranking[0]["model"]
                if ranking
                else None
            ),
            "metric_priority": [
                "mae",
                "rmse",
                "mape",
                "directional_accuracy",
            ],
        }
