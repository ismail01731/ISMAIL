from __future__ import annotations
from typing import Any, Dict, List, Optional
from forecast.engine import ForecastEngine
from .adapter import ExistingAIAdapter
from .context import IntelligenceContext
from .prompt import FuturePromptBuilder
class FutureIntelligence:
    def __init__(
        self,
        ai_adapter: Optional[ExistingAIAdapter] = None,
    ):
        self.forecast_engine = ForecastEngine()
        self.ai_adapter = ai_adapter or ExistingAIAdapter()
    def analyze(
        self,
        question: str,
        values: Optional[List[float]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        live_data: Optional[List[Dict[str, Any]]] = None,
        horizon_days: int = 30,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = IntelligenceContext(
            question=question,
            values=values,
            evidence=evidence,
            live_data=live_data,
            metadata=metadata,
        )
        # Quantitative prediction layer.
        if context.values:
            forecast = self.forecast_engine.predict(
                values=context.values,
                horizon_days=horizon_days,
                evidence=context.evidence,
            )
        else:
            forecast = {
                "status": "insufficient_historical_data",
                "message": (
                    "Numeric historical values are required "
                    "for quantitative forecasting."
                ),
                "horizon_days": horizon_days,
            }
        # Build reasoning prompt for the existing AI.
        prompt = FuturePromptBuilder.build(
            question=question,
            forecast=forecast,
        )
        ai_result = self.ai_adapter.generate(
            prompt=prompt,
            context={
                "forecast": forecast,
                "evidence": context.evidence,
                "live_data": context.live_data,
                "metadata": context.metadata,
            },
        )
        return {
            "question": question,
            "horizon_days": horizon_days,
            "forecast": forecast,
            "evidence": context.evidence,
            "live_data": context.live_data,
            "ai_analysis": ai_result,
            "integration": {
                "existing_ai_connected": self.ai_adapter.connected,
                "forecast_engine": "damped_linear_trend_v1",
                "mode": (
                    "ai_plus_quantitative_forecast"
                    if self.ai_adapter.connected
                    else "quantitative_forecast_only"
                ),
            },
        }
