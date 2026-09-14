from .emotion_models import (
    ConversationEmotionContext,
    EmotionalContext,
    MoodResult,
)
class ConversationContextBuilder:
    """
    Combines emotional context with existing conversation context.
    Does not manage or store conversation history.
    """
    def build(
        self,
        emotional_context: EmotionalContext,
        mood_result: MoodResult,
        conversation_context: str,
    ) -> ConversationEmotionContext:
        return ConversationEmotionContext(
            emotion=emotional_context.emotion,
            mood=mood_result.mood,
            confidence=mood_result.confidence,
            signals=emotional_context.signals,
            companion_instruction=(
                emotional_context.companion_instruction
            ),
            conversation_context=conversation_context or "",
        )
conversation_context_builder = ConversationContextBuilder()
