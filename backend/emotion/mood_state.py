from backend.emotion.emotion_engine import EmotionEngine
from backend.emotion.mood_intent import MoodIntentEngine
from backend.emotion.emotion_models import MoodState
class MoodStateEngine:
    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.intent_engine = MoodIntentEngine()
    def detect(self, message: str, context=None) -> MoodState:
        emotion_result = self.emotion_engine.detect(
            message,
            conversation_context=context or "",
        )
        intent_result = self.intent_engine.detect(message)
        return MoodState(
            emotion=emotion_result.emotion,
            emotion_confidence=emotion_result.confidence,
            intent=intent_result.intent,
            intent_confidence=intent_result.confidence,
            emotion_signals=emotion_result.signals,
            intent_signals=intent_result.signals,
        )
mood_state_engine = MoodStateEngine()
