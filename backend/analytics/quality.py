from __future__ import annotations
from typing import Any, Dict, List
import math
class DataQualityEngine:
    """
    Historical data quality evaluator.
    Quality considers:
    - valid values
    - missing values
    - sample size
    - variation
    - anomalies
    Score is always normalized between 0 and 1.
    """
    def __init__(
        self,
        minimum_usable_points: int = 8,
    ):
        self.minimum_usable_points = (
            int(minimum_usable_points)
        )
    @staticmethod
    def _is_valid(value: Any) -> bool:
        if value is None:
            return False
        try:
            number = float(value)
            return math.isfinite(number)
        except (
            TypeError,
            ValueError,
        ):
            return False
    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 1.0,
    ) -> float:
        return max(
            minimum,
            min(maximum, value),
        )
    def score(
        self,
        values: List[Any],
    ) -> Dict[str, Any]:
        total = len(values)
        valid_values = [
            float(v)
            for v in values
            if self._is_valid(v)
        ]
        valid_count = len(
            valid_values
        )
        missing_count = (
            total - valid_count
        )
        if total == 0:
            return {
                "score": 0.0,
                "level": "very_low",
                "count": 0,
                "valid": 0,
                "missing": 0,
                "missing_ratio": 0.0,
                "sample_score": 0.0,
                "validity_score": 0.0,
                "variation_score": 0.0,
                "anomaly_score": 0.0,
                "usable": False,
                "issues": [
                    "No data provided."
                ],
            }
        validity_score = (
            valid_count / total
        )
        missing_ratio = (
            missing_count / total
        )
        # Sample size score.
        #
        # 1 point around minimum_usable_points,
        # gradually saturating around 50 observations.
        if valid_count <= 0:
            sample_score = 0.0
        else:
            sample_score = self._clamp(
                math.log1p(valid_count)
                / math.log1p(50),
            )
        # Variation score.
        #
        # Completely constant series are less informative
        # for trend prediction.
        if valid_count <= 1:
            variation_score = 0.0
        else:
            mean = sum(
                valid_values
            ) / valid_count
            variance = sum(
                (x - mean) ** 2
                for x in valid_values
            ) / valid_count
            std = math.sqrt(
                variance
            )
            scale = max(
                abs(mean),
                1e-9,
            )
            coefficient = (
                std / scale
            )
            if coefficient < 1e-9:
                variation_score = 0.25
            else:
                variation_score = self._clamp(
                    0.50
                    + min(
                        coefficient,
                        1.0,
                    )
                    * 0.50
                )
        # Basic anomaly score.
        #
        # We don't punish a dataset heavily for a few
        # genuine extreme observations.
        if valid_count < 4:
            anomaly_score = 0.75
        else:
            mean = sum(
                valid_values
            ) / valid_count
            variance = sum(
                (x - mean) ** 2
                for x in valid_values
            ) / valid_count
            std = math.sqrt(
                variance
            )
            if std <= 1e-12:
                anomaly_score = 1.0
            else:
                anomaly_count = sum(
                    1
                    for x in valid_values
                    if abs(
                        (x - mean) / std
                    ) > 3.0
                )
                anomaly_ratio = (
                    anomaly_count
                    / valid_count
                )
                anomaly_score = self._clamp(
                    1.0
                    - anomaly_ratio
                    * 2.0
                )
        # Weighted final score.
        #
        # Validity is the most important factor.
        score = (
            validity_score * 0.40
            + sample_score * 0.25
            + variation_score * 0.15
            + anomaly_score * 0.20
        )
        score = self._clamp(
            score
        )
        if score >= 0.90:
            level = "excellent"
        elif score >= 0.75:
            level = "good"
        elif score >= 0.55:
            level = "moderate"
        elif score >= 0.35:
            level = "low"
        else:
            level = "very_low"
        issues = []
        if valid_count < self.minimum_usable_points:
            issues.append(
                "Historical sample is small."
            )
        if missing_count > 0:
            issues.append(
                f"{missing_count} missing or invalid values detected."
            )
        if variation_score <= 0.25:
            issues.append(
                "Data has little or no variation."
            )
        if anomaly_score < 0.75:
            issues.append(
                "Potential extreme observations detected."
            )
        usable = (
            valid_count >= 3
            and validity_score >= 0.75
        )
        return {
            "score": round(
                score,
                6,
            ),
            "level": level,
            "count": total,
            "valid": valid_count,
            "missing": missing_count,
            "missing_ratio": round(
                missing_ratio,
                6,
            ),
            "sample_score": round(
                sample_score,
                6,
            ),
            "validity_score": round(
                validity_score,
                6,
            ),
            "variation_score": round(
                variation_score,
                6,
            ),
            "anomaly_score": round(
                anomaly_score,
                6,
            ),
            "usable": usable,
            "issues": issues,
        }
