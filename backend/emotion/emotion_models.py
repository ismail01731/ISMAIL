from dataclasses import dataclass
@dataclass
class EmotionResult:
    emotion: str
    confidence: float
    signals: list[str]
@dataclass
class MoodState:
    emotion: str
    emotion_confidence: float
    intent: str
    intent_confidence: float
    emotion_signals: list[str]
    intent_signals: list[str]
@dataclass
class EmotionalContext:
    emotion: str
    confidence: float
    signals: list[str]
    companion_instruction: str

@dataclass
class MoodResult:
    mood: str
    confidence: float
    source_emotion: str
    signals: list[str]

@dataclass
class ConversationEmotionContext:
    emotion: str
    mood: str
    confidence: float
    signals: list[str]
    companion_instruction: str
    conversation_context: str
    intent: str = "general"
    intent_confidence: float = 0.50
@dataclass
class CompanionPersonality:
    name: str
    traits: list[str]
    communication_style: str
    safety_boundaries: list[str]
