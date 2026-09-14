from .emotion_models import EmotionResult, MoodResult
class MoodDetector:
    """
    Maps an existing EmotionResult to a broader mood state.
    This does not perform emotion detection itself.
    """
    EMOTION_TO_MOOD = {
        "sad": "low",
        "lonely": "low",
        "happy": "positive",
        "excited": "positive",
        "angry": "agitated",
        "stressed": "overwhelmed",
        "fun": "playful",
        "confused": "uncertain",
        "neutral": "neutral",
    }
    def detect(self, emotion_result: EmotionResult) -> MoodResult:
        emotion = emotion_result.emotion
        mood = self.EMOTION_TO_MOOD.get(emotion, "neutral")
        return MoodResult(
            mood=mood,
            confidence=emotion_result.confidence,
            source_emotion=emotion,
            signals=emotion_result.signals,
        )
mood_detector = MoodDetector()
