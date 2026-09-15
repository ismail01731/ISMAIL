import math
from typing import Any, Dict, List, Optional
class FutureAnswerBuilder:
    """
    Converts forecast + existing AI reasoning into a
    structured natural-language future answer.
    This is NOT a new AI model.
    """
    WARNING = (
        "এটি একটি সম্ভাব্য forecast, নিশ্চিত ভবিষ্যদ্বাণী নয়। "
        "নতুন data বা external event এলে ফলাফল পরিবর্তিত হতে পারে।"
    )
    def _percent(self, value: Any) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return 0.0
        if number <= 1:
            number *= 100.0
        return round(number, 2)
    def _direction(self, forecast: Dict[str, Any]) -> str:
        trend = forecast.get("trend", {})
        if isinstance(trend, dict):
            direction = trend.get("direction")
        else:
            direction = trend
        if direction:
            return str(direction).lower()
        return "unknown"
    def _confidence_level(self, forecast: Dict[str, Any]) -> str:
        calibration = forecast.get(
            "confidence_calibration",
            {}
        )
        if isinstance(calibration, dict):
            level = calibration.get("level")
            if level:
                return str(level)
        confidence = forecast.get("confidence")
        if isinstance(confidence, (int, float)):
            if confidence >= 0.75:
                return "high"
            if confidence >= 0.55:
                return "moderate"
            return "low"
        return "unknown"
    def _uncertainty_level(
        self,
        forecast: Dict[str, Any]
    ) -> str:
        uncertainty = forecast.get(
            "uncertainty",
            {}
        )
        if isinstance(uncertainty, dict):
            level = uncertainty.get("level")
            if level:
                return str(level)
        return "unknown"
    def _scenario_probabilities(
        self,
        forecast: Dict[str, Any]
    ) -> Dict[str, float]:
        scenarios = forecast.get(
            "scenarios",
            []
        )
        result = {}
        if isinstance(scenarios, list):
            for scenario in scenarios:
                if not isinstance(scenario, dict):
                    continue
                name = str(
                    scenario.get(
                        "name",
                        "unknown"
                    )
                ).lower()
                probability = scenario.get(
                    "probability",
                    0
                )
                result[name] = self._percent(
                    probability
                )
        elif isinstance(scenarios, dict):
            for name, value in scenarios.items():
                if isinstance(value, dict):
                    probability = value.get(
                        "probability",
                        0
                    )
                else:
                    probability = value
                result[str(name).lower()] = self._percent(
                    probability
                )
        return result
    def _summary(
        self,
        direction: str,
        horizon_days: Any
    ) -> str:
        try:
            horizon = int(horizon_days)
        except (TypeError, ValueError):
            horizon = 30
        if direction == "upward":
            return (
                f"বর্তমান data অনুযায়ী আগামী {horizon} দিনে "
                "trend উপরের দিকে যাওয়ার সম্ভাবনাই বেশি।"
            )
        if direction == "downward":
            return (
                f"বর্তমান data অনুযায়ী আগামী {horizon} দিনে "
                "trend নিচের দিকে যাওয়ার সম্ভাবনাই বেশি।"
            )
        if direction == "stable":
            return (
                f"বর্তমান data অনুযায়ী আগামী {horizon} দিনে "
                "trend মোটামুটি স্থিতিশীল থাকার সম্ভাবনা বেশি।"
            )
        return (
            f"আগামী {horizon} দিনের trend সম্পর্কে "
            "বর্তমান data থেকে নির্দিষ্ট direction নিশ্চিত নয়।"
        )
    def _key_factors(
        self,
        forecast: Dict[str, Any]
    ) -> List[str]:
        factors = []
        direction = self._direction(forecast)
        if direction == "upward":
            factors.append(
                "Historical trend বর্তমানে upward."
            )
        elif direction == "downward":
            factors.append(
                "Historical trend বর্তমানে downward."
            )
        elif direction == "stable":
            factors.append(
                "Historical trend বর্তমানে relatively stable."
            )
        selection = forecast.get(
            "selection",
            {}
        )
        if isinstance(selection, dict):
            selected = selection.get(
                "selected_model"
            )
            if selected:
                factors.append(
                    f"Forecast-এর জন্য নির্বাচিত model: {selected}."
                )
        quality = forecast.get(
            "data_quality",
            {}
        )
        if isinstance(quality, dict):
            level = quality.get("level")
            if level:
                factors.append(
                    f"Data quality level: {level}."
                )
        return factors
    def _what_to_watch(
        self,
        forecast: Dict[str, Any]
    ) -> List[str]:
        watch = []
        uncertainty = self._uncertainty_level(
            forecast
        )
        if uncertainty in {
            "high",
            "very_high"
        }:
            watch.append(
                "Forecast uncertainty বেশি, তাই নতুন data নিয়মিত monitor করা উচিত।"
            )
        else:
            watch.append(
                "নতুন data trend-এর direction পরিবর্তন করছে কি না monitor করা উচিত।"
            )
        anomalies = forecast.get(
            "anomalies",
            []
        )
        if anomalies:
            watch.append(
                "Historical data-তে anomaly পাওয়া গেছে; "
                "এগুলো future outcome পরিবর্তন করতে পারে।"
            )
        return watch
    def build(
        self,
        question: str,
        forecast: Dict[str, Any],
        ai_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ai_analysis = ai_analysis or {}
        direction = self._direction(
            forecast
        )
        horizon_days = forecast.get(
            "horizon",
            30
        )
        probabilities = self._scenario_probabilities(
            forecast
        )
        confidence = self._confidence_level(
            forecast
        )
        uncertainty = self._uncertainty_level(
            forecast
        )
        ai_response = ai_analysis.get(
            "response"
        )
        if ai_response is not None:
            ai_response = str(
                ai_response
            )
        return {
            "question": question,
            "summary": self._summary(
                direction,
                horizon_days
            ),
            "direction": direction,
            "horizon_days": horizon_days,
            "probabilities": probabilities,
            "confidence": confidence,
            "uncertainty": uncertainty,
            "selected_model": forecast.get(
                "selected_model"
            ),
            "expected_value": forecast.get(
                "expected_value"
            ),
            "latest_value": forecast.get(
                "latest_value"
            ),
            "key_factors": self._key_factors(
                forecast
            ),
            "what_to_watch": self._what_to_watch(
                forecast
            ),
            "ai_reasoning": ai_response,
            "warning": self.WARNING,
            "guarantee": False
        }
default_answer_builder = FutureAnswerBuilder()
