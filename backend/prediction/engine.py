from dataclasses import dataclass, field
from typing import Any
from .probability import normalize_probabilities
from .confidence import calculate_confidence
from .scenario import build_scenarios
@dataclass
class PredictionResult:
    question: str
    scenarios: list[dict[str, Any]]
    confidence: str
    confidence_score: float
    assumptions: list[str] = field(default_factory=list)
class FuturePredictionEngine:
    def predict(
        self,
        question: str,
        evidence: list[dict[str, Any]] | None = None,
        horizon_days: int = 30,
        context: dict[str, Any] | None = None,
    ) -> PredictionResult:
        evidence = evidence or []
        context = context or {}
        scenarios = build_scenarios(
            question=question,
            evidence=evidence,
            horizon_days=horizon_days,
            context=context,
        )
        scenarios = normalize_probabilities(scenarios)
        confidence_score = calculate_confidence(
            evidence=evidence,
            scenarios=scenarios,
        )
        if confidence_score >= 0.75:
            confidence = "high"
        elif confidence_score >= 0.45:
            confidence = "medium"
        else:
            confidence = "low"
        return PredictionResult(
            question=question,
            scenarios=scenarios,
            confidence=confidence,
            confidence_score=confidence_score,
            assumptions=[
                "Prediction is probabilistic.",
                "Future events can change when new evidence appears.",
            ],
        )
