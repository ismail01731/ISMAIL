from typing import Any, Dict, List, Optional
from forecast.engine import ForecastEngine
from .adapter import ExistingAIAdapter, existing_ai_adapter
from .answer import FutureAnswerBuilder
from .context import IntelligenceContext
from .prompt import FuturePromptBuilder
class FutureIntelligence:
    def __init__(
        self,
        ai_adapter: Optional[ExistingAIAdapter] = None,
        answer_builder: Optional[FutureAnswerBuilder] = None,
    ):
        # Use the GLOBAL existing AI adapter by default.
        # This allows connect_existing_ai() to work automatically.
        self.ai_adapter = (
            ai_adapter
            if ai_adapter is not None
            else existing_ai_adapter
        )
        self.answer_builder = (
            answer_builder
            if answer_builder is not None
            else FutureAnswerBuilder()
        )
        self.forecast_engine = ForecastEngine()
        self.prompt_builder = FuturePromptBuilder()
    def analyze(
        self,
        question: str,
        values: List[float],
        evidence: Optional[List[Dict[str, Any]]] = None,
        live_data: Optional[List[Dict[str, Any]]] = None,
        horizon_days: int = 30,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        evidence = evidence or []
        live_data = live_data or []
        metadata = metadata or {}
        context = IntelligenceContext(
            question=question,
            values=values,
            evidence=evidence,
            live_data=live_data,
            metadata=metadata,
        )
        clean_values = [
            float(v)
            for v in values
            if v is not None
        ]
        if len(clean_values) >= 3:
            forecast = self.forecast_engine.predict(
                clean_values,
                horizon_days=horizon_days,
                evidence=evidence,
            )
            prompt = self.prompt_builder.build(
                question,
                forecast
            )
            ai_context = {
                **context.to_dict(),
                "forecast": forecast,
            }
            ai_analysis = self.ai_adapter.generate(
                prompt,
                ai_context
            )
            natural_answer = self.answer_builder.build(
                question,
                forecast,
                ai_analysis
            )
        else:
            forecast = {
                "status": "insufficient_data",
                "historical_count": len(clean_values),
                "horizon": horizon_days,
                "confidence": 0.0,
                "confidence_percent": 0.0,
            }
            ai_analysis = {
                "status": "not_run",
                "reason": "insufficient_historical_data",
            }
            natural_answer = {
                "question": question,
                "summary": (
                    "বর্তমান historical data যথেষ্ট নয় "
                    "যাতে নির্ভরযোগ্য future forecast তৈরি করা যায়।"
                ),
                "direction": "unknown",
                "horizon_days": horizon_days,
                "probabilities": {},
                "confidence": "very_low",
                "uncertainty": "very_high",
                "selected_model": None,
                "expected_value": None,
                "latest_value": (
                    clean_values[-1]
                    if clean_values
                    else None
                ),
                "key_factors": [
                    "Historical data পর্যাপ্ত নয়।"
                ],
                "what_to_watch": [
                    "আরও historical data সংগ্রহ করুন।"
                ],
                "ai_reasoning": None,
                "warning": (
                    "পর্যাপ্ত data ছাড়া forecast নির্ভরযোগ্য নয়।"
                ),
                "guarantee": False,
            }
        integration = {
            "ai_connected": self.ai_adapter.connected,
            "adapter": self.ai_adapter.name,
            "existing_ai_preserved": True,
            "new_ai_created": False,
        }
        return {
            "question": question,
            "horizon_days": horizon_days,
            "forecast": forecast,
            "evidence": evidence,
            "live_data": live_data,
            "context": context.to_dict(),
            "ai_analysis": ai_analysis,
            "natural_answer": natural_answer,
            "integration": integration,
        }
