from dataclasses import dataclass
@dataclass
class MoodIntentResult:
    intent: str
    confidence: float
    signals: list[str]
class MoodIntentEngine:
    """
    Detects conversational intent after emotion detection.
    """
    INTENT_KEYWORDS = {
        "companionship": [
            "\u0986\u09ae\u09be\u09b0 \u09b8\u09be\u09a5\u09c7 \u0995\u09a5\u09be \u09ac\u09b2\u09cb",
            "\u098f\u0995\u099f\u09c1 \u0995\u09a5\u09be \u09ac\u09b2\u09cb",
            "\u0997\u09b2\u09cd\u09aa \u0995\u09b0\u09bf",
            "\u0986\u09ae\u09be\u09b0 \u09b8\u09be\u09a5\u09c7 \u09a5\u09be\u0995\u09cb",
            "\u0995\u09a5\u09be \u09ac\u09b2\u09a4\u09c7 \u099a\u09be\u0987",
            "talk to me",
            "stay with me",
        ],
        "fun": [
            "joke",
            "\u099c\u09cb\u0995",
            "\u09ae\u099c\u09be",
            "\u09b9\u09be\u09b8\u09be\u0993",
            "funny",
            "\u09b9\u09be\u09b8\u09a4\u09c7 \u099a\u09be\u0987",
        ],
        "comfort": [
            "\u09b8\u09be\u09a8\u09cd\u09a4\u09cd\u09ac\u09a8\u09be",
            "\u09b8\u09be\u09a8\u09cd\u09a4\u09cd\u09ac\u09a8\u09be \u09a6\u09be\u0993",
            "\u0986\u09ae\u09be\u0995\u09c7 \u098f\u0995\u099f\u09c1 \u09ac\u09c1\u099d\u09cb",
            "\u09ae\u09a8\u099f\u09be \u09ad\u09be\u09b2\u09cb \u0995\u09b0\u09c7 \u09a6\u09be\u0993",
            "comfort me",
            "help me feel better",
        ],
        "sharing": [
            "\u09a4\u09cb\u09ae\u09be\u0995\u09c7 \u098f\u0995\u099f\u09be \u0996\u09ac\u09b0 \u09ac\u09b2\u09bf",
            "\u098f\u0995\u099f\u09be \u0996\u09ac\u09b0 \u09ac\u09b2\u09bf",
            "\u09a4\u09cb\u09ae\u09be\u0995\u09c7 \u098f\u0995\u099f\u09be \u0995\u09a5\u09be \u09ac\u09b2\u09bf",
            "\u09b6\u09c7\u09df\u09be\u09b0 \u0995\u09b0\u09a4\u09c7 \u099a\u09be\u0987",
            "share ???? ???",
        ],
        "solution": [
            "\u0995\u09c0\u09ad\u09be\u09ac\u09c7 \u098f\u099f\u09be \u09a0\u09bf\u0995 \u0995\u09b0\u09ac",
            "\u0995\u09bf \u0995\u09b0\u09ac",
            "\u0995\u09c0 \u0995\u09b0\u09ac",
            "\u09b8\u09ae\u09be\u09a7\u09be\u09a8",
            "\u0989\u09aa\u09be\u09df \u09ac\u09b2\u09cb",
            "what should i do",
            "how can i fix",
        ],
    }
    def detect(self, message: str) -> MoodIntentResult:
        text = " ".join(
            (message or "").strip().lower().split()
        )
        if not text:
            return MoodIntentResult(
                intent="general",
                confidence=1.0,
                signals=[],
            )
        scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            matched = [
                keyword
                for keyword in keywords
                if keyword.lower() in text
            ]
            if matched:
                scores[intent] = sum(
                    1 + (len(keyword.split()) * 0.25)
                    for keyword in matched
                )
        if not scores:
            return MoodIntentResult(
                intent="general",
                confidence=0.50,
                signals=[],
            )
        intent = max(scores, key=scores.get)
        score = scores[intent]
        confidence = min(
            0.55 + (score - 1) * 0.10,
            0.90,
        )
        return MoodIntentResult(
            intent=intent,
            confidence=round(confidence, 2),
            signals=[
                keyword
                for keyword in self.INTENT_KEYWORDS[intent]
                if keyword.lower() in text
            ],
        )
mood_intent_engine = MoodIntentEngine()
