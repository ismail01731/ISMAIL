from __future__ import annotations
from typing import Any, Dict, List, Optional
from analytics.engine import HistoricalAnalytics
from forecast.engine import ForecastEngine
from intelligence.adapter import ExistingAIAdapter
from intelligence.prompt import FuturePromptBuilder
from .result import FutureSystemResult
class CompleteFutureSystem:
    """
    End-to-end future intelligence pipeline.
    This system orchestrates the modules created in Tasks 1-9.
    Existing AI remains external and optional.
    """
    def __init__(
        self,
        ai_adapter: Optional[ExistingAIAdapter] = None,
    ):
        self.forecast_engine = ForecastEngine()
        self.analytics_engine = HistoricalAnalytics()
        self.ai_adapter = (
            ai_adapter
            or ExistingAIAdapter()
        )
    # -----------------------------------------------------
    # Historical analytics
    # -----------------------------------------------------
    def _analytics(
        self,
        values: List[float],
    ) -> Dict[str, Any]:
        if not values:
            return {
                "status":
                    "no_historical_data",
                "count": 0,
            }
        try:
            return self.analytics_engine.analyze(
                values=values,
                window=min(
                    5,
                    max(1, len(values)),
                ),
            )
        except Exception:
            # Compatibility fallback if a previous
            # analytics implementation uses a slightly
            # different method signature.
            return {
                "count": len(values),
                "latest": values[-1],
                "status":
                    "analytics_fallback",
            }
    # -----------------------------------------------------
    # Main pipeline
    # -----------------------------------------------------
    def analyze(
        self,
        question: str,
        historical_values: Optional[List[float]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        live_data: Optional[List[Dict[str, Any]]] = None,
        horizon_days: int = 30,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not question or not question.strip():
            raise ValueError(
                "question cannot be empty."
            )
        if horizon_days < 1:
            raise ValueError(
                "horizon_days must be >= 1."
            )
        historical_values = (
            historical_values or []
        )
        historical_values = [
            float(value)
            for value in historical_values
        ]
        evidence = evidence or []
        live_data = live_data or []
        metadata = metadata or {}
        # -------------------------------------------------
        # 1. Historical analytics
        # -------------------------------------------------
        analytics = self._analytics(
            historical_values
        )
        # -------------------------------------------------
        # 2. Forecast
        # -------------------------------------------------
        if historical_values:
            forecast = self.forecast_engine.predict(
                values=historical_values,
                horizon_days=horizon_days,
                evidence=evidence,
            )
        else:
            forecast = {
                "status":
                    "insufficient_historical_data",
                "horizon_days":
                    horizon_days,
                "confidence":
                    0.0,
                "confidence_percent":
                    0.0,
                "scenarios": {},
                "limitations": [
                    "No historical numeric data supplied."
                ],
            }
        # -------------------------------------------------
        # 3. AI reasoning
        # -------------------------------------------------
        prompt = FuturePromptBuilder.build(
            question=question,
            forecast=forecast,
        )
        ai_context = {
            "question": question,
            "historical_values":
                historical_values,
            "analytics":
                analytics,
            "forecast":
                forecast,
            "evidence":
                evidence,
            "live_data":
                live_data,
            "metadata":
                metadata,
        }
        ai_analysis = self.ai_adapter.generate(
            prompt=prompt,
            context=ai_context,
        )
        # -------------------------------------------------
        # 4. Final result
        # -------------------------------------------------
        historical_summary = {
            "count":
                len(historical_values),
            "latest":
                (
                    historical_values[-1]
                    if historical_values
                    else None
                ),
            "values":
                historical_values,
        }
        return FutureSystemResult.build(
            question=question,
            horizon_days=horizon_days,
            historical=historical_summary,
            analytics=analytics,
            forecast=forecast,
            ai_analysis=ai_analysis,
            evidence=evidence,
            live_data=live_data,
        )
