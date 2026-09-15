from __future__ import annotations
from typing import Any, Dict, List, Optional
from .adapter import ExistingAIAdapter
from .context import IntelligenceContext
from .prompt import FuturePromptBuilder
from forecast.engine import ForecastEngine
class FutureIntelligence:
    def __init__(
        self,
        ai_adapter: Optional[
            ExistingAIAdapter
        ] = None,
    ):
        self.forecast_engine = (
            ForecastEngine()
        )
        self.prompt_builder = (
            FuturePromptBuilder()
        )
        self.ai_adapter = (
            ai_adapter
            or ExistingAIAdapter()
        )
    def analyze(
        self,
        question: str,
        values: Optional[
            List[float]
        ] = None,
        evidence=None,
        live_data=None,
        horizon_days: int = 30,
        metadata=None,
    ) -> Dict[str, Any]:
        values = values or []
        context = IntelligenceContext(
            question=question,
            values=values,
            evidence=evidence or [],
            live_data=live_data or [],
            metadata=metadata or {},
        )
        if values:
            forecast = (
                self.forecast_engine.predict(
                    values=values,
                    horizon_days=horizon_days,
                    evidence=evidence,
                )
            )
        else:
            forecast = {
                "status":
                    "insufficient_data",
                "message":
                    "Historical values are required.",
            }
        prompt = (
            self.prompt_builder.build(
                question,
                forecast,
            )
        )
        ai_context = {
            "question":
                question,
            "horizon_days":
                horizon_days,
            "historical_values":
                values,
            "forecast":
                forecast,
            "evidence":
                evidence or [],
            "live_data":
                live_data or [],
            "metadata":
                metadata or {},
        }
        ai_analysis = (
            self.ai_adapter.generate(
                prompt=prompt,
                context=ai_context,
            )
        )
        return {
            "question":
                question,
            "horizon_days":
                horizon_days,
            "forecast":
                forecast,
            "evidence":
                evidence or [],
            "live_data":
                live_data or [],
            "ai_analysis":
                ai_analysis,
            "integration": {
                "ai_connected":
                    self.ai_adapter.connected,
                "adapter":
                    self.ai_adapter.name,
                "existing_ai_preserved":
                    True,
                "new_ai_created":
                    False,
            },
            "context": context.to_dict(),
        }
