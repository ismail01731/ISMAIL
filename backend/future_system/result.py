from __future__ import annotations
from typing import Any, Dict
class FutureSystemResult:
    @staticmethod
    def build(
        question: str,
        horizon_days: int,
        historical: Dict[str, Any],
        analytics: Dict[str, Any],
        forecast: Dict[str, Any],
        ai_analysis: Any,
        evidence: list,
        live_data: list,
    ) -> Dict[str, Any]:
        confidence = forecast.get(
            "confidence",
            0.0,
        )
        return {
            "system": {
                "name":
                    "ISMAIL Future Intelligence System",
                "version":
                    "1.0.0",
                "type":
                    "probabilistic_future_analysis",
            },
            "question": question,
            "horizon_days":
                horizon_days,
            "data": {
                "historical": historical,
                "live": live_data,
                "evidence": evidence,
            },
            "analytics":
                analytics,
            "forecast":
                forecast,
            "ai_analysis":
                ai_analysis,
            "confidence": confidence,
            "confidence_percent":
                round(
                    confidence * 100,
                    2,
                ),
            "interpretation": {
                "confidence_level":
                    (
                        "high"
                        if confidence >= 0.75
                        else
                        "medium"
                        if confidence >= 0.50
                        else
                        "low"
                    ),
                "warning":
                    (
                        "This is a probabilistic "
                        "forecast and not a guaranteed "
                        "prediction."
                    ),
            },
            "pipeline": [
                "question",
                "historical_data",
                "live_data",
                "evidence",
                "historical_analytics",
                "forecast_model",
                "scenario_analysis",
                "confidence",
                "existing_ai_reasoning",
                "final_result",
            ],
        }
