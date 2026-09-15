from __future__ import annotations
from typing import Dict, Optional
class ProbabilityCalibrator:
    """Adjust confidence/probabilities using data quality and evidence."""
    @staticmethod
    def evidence_score(evidence=None) -> float:
        if not evidence:
            return 0.50
        scores = []
        for item in evidence:
            if isinstance(item, dict):
                score = item.get("quality_score")
                if score is None:
                    reliability = float(item.get("reliability", 0.5))
                    relevance = float(item.get("relevance", 0.5))
                    freshness = float(item.get("freshness", 0.5))
                    score = (
                        reliability * 0.40
                        + relevance * 0.35
                        + freshness * 0.25
                    )
                scores.append(float(score))
        if not scores:
            return 0.50
        return max(0.0, min(1.0, sum(scores) / len(scores)))
    @classmethod
    def confidence(
        cls,
        count: int,
        volatility: float,
        anomalies: int = 0,
        evidence=None,
    ) -> float:
        # More history = more confidence, with diminishing returns.
        data_score = min(1.0, count / 50.0)
        # High volatility reduces confidence.
        volatility_penalty = min(0.40, volatility / 100.0)
        # Anomalies reduce confidence.
        anomaly_penalty = min(0.25, anomalies * 0.05)
        evidence_score = cls.evidence_score(evidence)
        score = (
            data_score * 0.40
            + evidence_score * 0.35
            + (1.0 - volatility_penalty) * 0.25
        )
        score -= anomaly_penalty
        return max(0.0, min(1.0, score))
