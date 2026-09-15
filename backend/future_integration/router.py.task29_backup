from __future__ import annotations
import re
from typing import Any
from .detector import FutureIntentDetector
class FutureIntegration:
    """
    Bridge between the existing ISMAIL AIEngine and the completed
    Future Intelligence System.
    Existing ISMAIL AI remains the final reasoning / language layer.
    Future System supplies prediction intelligence.
    """
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        self._pipeline = None
    def _build_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline
        from intelligence.adapter import ExistingAIAdapter
        from intelligence.orchestrator import FutureIntelligence
        from pipeline.automatic import AutomaticFuturePipeline
        # Existing ISMAIL LLM is used as the final reasoning layer.
        # We intentionally do NOT call AIEngine.generate() here because
        # that would recursively enter the Future Integration router.
        def existing_ai_generate(prompt: str, context=None):
            if context:
                combined = (
                    f"{prompt}\n\n"
                    "FUTURE SYSTEM CONTEXT:\n"
                    f"{context}"
                )
            else:
                combined = prompt
            return self.ai_engine.llm_router.generate(combined)
        adapter = ExistingAIAdapter(
            generate_function=existing_ai_generate,
            name="ismail_existing_ai",
        )
        intelligence = FutureIntelligence(
            ai_adapter=adapter
        )
        self._pipeline = AutomaticFuturePipeline(
            intelligence=intelligence
        )
        return self._pipeline
    @staticmethod
    def _extract_horizon(message: str) -> int:
        text = (message or "").lower()
        match = re.search(
            r"\b(\d+)\s*(?:day|days)\b",
            text,
        )
        if match:
            return max(1, min(int(match.group(1)), 365))
        match = re.search(
            r"\b(\d+)\s*(?:week|weeks)\b",
            text,
        )
        if match:
            return max(
                1,
                min(int(match.group(1)) * 7, 365),
            )
        match = re.search(
            r"\b(\d+)\s*(?:month|months)\b",
            text,
        )
        if match:
            return max(
                1,
                min(int(match.group(1)) * 30, 365),
            )
        # Bengali numeric horizons.
        match = re.search(
            r"(?:আগামী|পরের|পরবর্তী)\s*(\d+)\s*দিন",
            text,
        )
        if match:
            return max(1, min(int(match.group(1)), 365))
        match = re.search(
            r"(?:আগামী|পরের|পরবর্তী)\s*(\d+)\s*সপ্তাহ",
            text,
        )
        if match:
            return max(
                1,
                min(int(match.group(1)) * 7, 365),
            )
        match = re.search(
            r"(?:আগামী|পরের|পরবর্তী)\s*(\d+)\s*মাস",
            text,
        )
        if match:
            return max(
                1,
                min(int(match.group(1)) * 30, 365),
            )
        return 30
    @staticmethod
    def _extract_topic(message: str) -> str:
        """
        First-pass topic extraction.
        We deliberately avoid inventing a topic. If a clean subject
        cannot be extracted, the remaining question text is used.
        """
        text = (message or "").strip()
        if not text:
            return ""
        patterns = (
            r"(?i)^what will happen to\s+",
            r"(?i)^what is likely to happen to\s+",
            r"(?i)^what could happen to\s+",
            r"(?i)^predict\s+",
            r"(?i)^forecast\s+",
            r"(?i)^future of\s+",
            r"(?i)^outlook for\s+",
            r"(?i)^where is\s+(.+?)\s+going\??$",
        )
        cleaned = text
        for pattern in patterns:
            cleaned = re.sub(
                pattern,
                "",
                cleaned,
            ).strip()
        # Bengali future framing.
        bengali_patterns = (
            r"^আগামী\s+\d+\s+দিনে\s+",
            r"^আগামী\s+\d+\s+সপ্তাহে\s+",
            r"^আগামী\s+\d+\s+মাসে\s+",
            r"^ভবিষ্যতে\s+",
            r"^কী হবে\s+",
            r"^কি হবে\s+",
            r"^কী হতে পারে\s+",
            r"^কি হতে পারে\s+",
            r"^কোন দিকে যেতে পারে\s+",
            r"^কোন দিকে যাবে\s+",
        )
        for pattern in bengali_patterns:
            cleaned = re.sub(
                pattern,
                "",
                cleaned,
            ).strip()
        if len(cleaned) < 3:
            return text
        return cleaned.rstrip("?!। ")
    def analyze(
        self,
        message: str,
        user_id: str = "",
        chat_id: str = "",
    ) -> dict[str, Any] | None:
        if not FutureIntentDetector.detect(message):
            return None
        topic = self._extract_topic(message)
        if not topic:
            topic = message.strip()
        horizon_days = self._extract_horizon(message)
        try:
            pipeline = self._build_pipeline()
            result = pipeline.analyze(
                question=message,
                topic=topic,
                horizon_days=horizon_days,
                metadata={
                    "source": "existing_ismail_ai",
                    "user_id": str(user_id),
                    "chat_id": str(chat_id),
                    "future_integration": True,
                },
            )
            if isinstance(result, dict):
                result.setdefault(
                    "status",
                    "success",
                )
                result.setdefault(
                    "topic",
                    topic,
                )
                result.setdefault(
                    "horizon_days",
                    horizon_days,
                )
                result.setdefault(
                    "existing_ai_preserved",
                    True,
                )
                result.setdefault(
                    "new_ai_created",
                    False,
                )
            return result
        except Exception as exc:
            return {
                "status": "error",
                "reason": str(exc),
                "question": message,
                "topic": topic,
                "horizon_days": horizon_days,
                "existing_ai_preserved": True,
                "new_ai_created": False,
            }
