from dataclasses import dataclass
@dataclass
class EmotionResult:
    emotion: str
    confidence: float
    signals: list[str]
