from __future__ import annotations
from typing import List, Dict, Any
from .backtesting import BacktestingEngine
class AutomaticModelSelector:
    """
    Selects the forecasting model using historical backtesting.
    Primary metric:
        MAE
    Secondary metrics:
        RMSE
        MAPE
        Directional Accuracy
    The selector deliberately keeps the decision transparent.
    """
    def __init__(
        self,
        minimum_history: int = 8,
        validation_size: int = 3,
    ):
        self.minimum_history = max(
            5,
            int(minimum_history),
        )
        self.validation_size = max(
            1,
            int(validation_size),
        )
        self.backtester = BacktestingEngine()
    def select(
        self,
        values: List[float],
    ) -> Dict[str, Any]:
        clean = [
            float(v)
            for v in values
            if v is not None
        ]
        if len(clean) < self.minimum_history:
            return {
                "success": False,
                "selected_model": None,
                "reason": (
                    f"At least {self.minimum_history} "
                    "historical values are recommended."
                ),
                "backtest": None,
            }
        result = self.backtester.evaluate(
            values=clean,
            validation_size=min(
                self.validation_size,
                len(clean) - 2,
            ),
        )
        if not result.get("success"):
            return {
                "success": False,
                "selected_model": None,
                "reason": result.get(
                    "message",
                    "Backtesting failed.",
                ),
                "backtest": result,
            }
        ranking = result.get("ranking", [])
        if not ranking:
            return {
                "success": False,
                "selected_model": None,
                "reason": "No usable forecasting models.",
                "backtest": result,
            }
        selected = ranking[0]["model"]
        return {
            "success": True,
            "selected_model": selected,
            "selection_method": "backtest_mae",
            "reason": (
                "Selected the model with the lowest "
                "validation MAE."
            ),
            "ranking": ranking,
            "backtest": result,
        }
