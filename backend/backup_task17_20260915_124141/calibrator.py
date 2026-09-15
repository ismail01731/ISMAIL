from __future__ import annotations
from typing import Any, Dict, List, Optional
import math
class ConfidenceCalibrator:
    """
    Confidence calibration based on:
    1. Historical data quantity
    2. Backtest model accuracy
    3. Model agreement
    4. Forecast uncertainty
    5. Historical volatility
    This is a heuristic calibration layer.
    It does not claim statistically calibrated probabilities.
    """
    def __init__(
        self,
        minimum_confidence: float = 0.20,
        maximum_confidence: float = 0.92,
    ):
        self.minimum_confidence = (
            float(minimum_confidence)
        )
        self.maximum_confidence = (
            float(maximum_confidence)
        )
    @staticmethod
    def _clamp(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        return max(
            minimum,
            min(maximum, value),
        )
    @staticmethod
    def _safe_float(
        value: Any,
        default: float = 0.0,
    ) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    def data_score(
        self,
        count: int,
    ) -> float:
        if count <= 0:
            return 0.0
        # Saturates gradually instead of
        # giving huge confidence to small datasets.
        return self._clamp(
            math.log1p(count) / math.log1p(100),
            0.0,
            1.0,
        )
    def accuracy_score(
        self,
        ranking: Optional[List[Dict[str, Any]]],
        selected_model: Optional[str],
    ) -> float:
        if not ranking:
            return 0.50
        selected = None
        for item in ranking:
            if item.get("model") == selected_model:
                selected = item
                break
        if selected is None:
            selected = ranking[0]
        mae = self._safe_float(
            selected.get("mae"),
            0.0,
        )
        mape = self._safe_float(
            selected.get("mape"),
            0.0,
        )
        directional = self._safe_float(
            selected.get(
                "directional_accuracy"
            ),
            0.50,
        )
        # MAPE is converted into an accuracy score.
        #
        # 0% error  -> 1.00
        # 10% error -> ~0.50
        # 25% error -> ~0.29
        mape_score = 1.0 / (
            1.0 + max(mape, 0.0) / 10.0
        )
        directional_score = self._clamp(
            directional,
            0.0,
            1.0,
        )
        accuracy = (
            mape_score * 0.55
            + directional_score * 0.45
        )
        return self._clamp(
            accuracy,
            0.0,
            1.0,
        )
    def agreement_score(
        self,
        disagreement: float,
    ) -> float:
        disagreement = max(
            0.0,
            self._safe_float(
                disagreement
            ),
        )
        # Lower disagreement = higher confidence.
        return self._clamp(
            1.0 / (
                1.0
                + disagreement * 10.0
            ),
            0.0,
            1.0,
        )
    def uncertainty_score(
        self,
        uncertainty: float,
    ) -> float:
        uncertainty = self._clamp(
            self._safe_float(
                uncertainty
            ),
            0.0,
            1.0,
        )
        return 1.0 - uncertainty
    def volatility_score(
        self,
        volatility_ratio: float,
    ) -> float:
        ratio = max(
            0.0,
            self._safe_float(
                volatility_ratio
            ),
        )
        return self._clamp(
            1.0 / (
                1.0
                + ratio * 8.0
            ),
            0.0,
            1.0,
        )
    def calibrate(
        self,
        data_count: int,
        ranking: Optional[
            List[Dict[str, Any]]
        ] = None,
        selected_model: Optional[str] = None,
        uncertainty: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        uncertainty = (
            uncertainty or {}
        )
        uncertainty_score = (
            self.uncertainty_score(
                uncertainty.get(
                    "score",
                    0.0,
                )
            )
        )
        agreement_score = (
            self.agreement_score(
                uncertainty.get(
                    "model_disagreement",
                    0.0,
                )
            )
        )
        volatility_score = (
            self.volatility_score(
                uncertainty.get(
                    "volatility_ratio",
                    0.0,
                )
            )
        )
        data_score = self.data_score(
            data_count
        )
        accuracy_score = (
            self.accuracy_score(
                ranking,
                selected_model,
            )
        )
        # Weighted confidence.
        #
        # Backtest accuracy receives the highest weight.
        raw_confidence = (
            accuracy_score * 0.40
            + data_score * 0.15
            + agreement_score * 0.15
            + uncertainty_score * 0.20
            + volatility_score * 0.10
        )
        # Avoid overconfidence.
        confidence = self._clamp(
            raw_confidence,
            self.minimum_confidence,
            self.maximum_confidence,
        )
        if confidence >= 0.75:
            level = "high"
        elif confidence >= 0.55:
            level = "moderate"
        elif confidence >= 0.35:
            level = "low"
        else:
            level = "very_low"
        return {
            "score": round(
                confidence,
                6,
            ),
            "percent": round(
                confidence * 100,
                2,
            ),
            "level": level,
            "components": {
                "data": round(
                    data_score,
                    6,
                ),
                "backtest_accuracy": round(
                    accuracy_score,
                    6,
                ),
                "model_agreement": round(
                    agreement_score,
                    6,
                ),
                "uncertainty": round(
                    uncertainty_score,
                    6,
                ),
                "volatility": round(
                    volatility_score,
                    6,
                ),
            },
            "method": (
                "backtest accuracy + data quality "
                "+ model agreement + uncertainty "
                "+ volatility"
            ),
            "calibrated": True,
            "warning": (
                "Heuristic calibration; "
                "not statistically calibrated."
            ),
        }
