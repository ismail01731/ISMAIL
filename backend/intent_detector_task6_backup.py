import re
class IntentDetector:
    """
    Smart intent detection layer for ISMAIL AI.
    This module only understands and classifies a user message.
    It does not call AI providers, databases, web research, or tools.
    """
    KNOWLEDGE_KEYWORDS = {
        "what is",
        "what are",
        "who is",
        "who was",
        "explain",
        "define",
        "meaning of",
        "how does",
        "how do",
        "why does",
        "why do",
        "python",
        "programming",
        "physics",
        "mathematics",
        "math",
        "science",
        "history",
        "grammar",
        "algorithm",
        "database",
        "computer",
        "coding",
        "কি",
        "কাকে বলে",
        "ব্যাখ্যা",
        "ব্যাখ্যা কর",
        "অর্থ",
        "মানে",
        "কিভাবে কাজ করে",
        "কেন",
        "পাইথন",
        "প্রোগ্রামিং",
        "গণিত",
        "বিজ্ঞান",
        "ইতিহাস",
        "ব্যাকরণ",
        "অ্যালগরিদম",
        "ডাটাবেস",
        "কম্পিউটার",
        "কোডিং",
    }
    LIVE_KEYWORDS = {
        "today",
        "tonight",
        "now",
        "currently",
        "current",
        "latest",
        "recent",
        "recently",
        "this week",
        "this month",
        "breaking",
        "news",
        "weather",
        "temperature",
        "forecast",
        "price",
        "prices",
        "stock",
        "score",
        "scores",
        "match",
        "matches",
        "population",
        "fire",
        "earthquake",
        "outage",
        "version",
        "release",
        "available",
        "availability",
        "status",
        "আজ",
        "এখন",
        "বর্তমানে",
        "সর্বশেষ",
        "সাম্প্রতিক",
        "খবর",
        "আবহাওয়া",
        "আবহাওয়া",
        "তাপমাত্রা",
        "পূর্বাভাস",
        "দাম",
        "মূল্য",
        "স্কোর",
        "ম্যাচ",
        "ভূমিকম্প",
        "আগুন",
        "বিদ্যুৎ",
        "সংস্করণ",
        "রিলিজ",
        "স্ট্যাটাস",
    }
    CONVERSATION_PATTERNS = (
        r"^(hi|hello|hey|হাই|হ্যালো|আসসালামু আলাইকুম)",
        r"^(how are you|কেমন আছ|কেমন আছেন)",
        r"^(thank you|thanks|ধন্যবাদ)",
    )
    def detect(self, message: str) -> dict:
        """Classify the user's message into an AI intent."""
        text = message.strip()
        if not text:
            raise ValueError("Message cannot be empty.")
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        conversation_matches = self._find_pattern_matches(
            normalized,
            self.CONVERSATION_PATTERNS,
        )
        live_matches = self._find_keyword_matches(
            normalized,
            self.LIVE_KEYWORDS,
        )
        knowledge_matches = self._find_keyword_matches(
            normalized,
            self.KNOWLEDGE_KEYWORDS,
        )
        if conversation_matches:
            return self._result(
                intent="conversation",
                route="general",
                confidence="high",
                reason="The message appears to be conversational.",
                matches=conversation_matches,
                normalized=normalized,
            )
        if live_matches:
            return self._result(
                intent="live_information",
                route="live",
                confidence="high",
                reason="The message appears to require current or time-sensitive information.",
                matches=live_matches,
                normalized=normalized,
            )
        if knowledge_matches:
            return self._result(
                intent="knowledge",
                route="knowledge",
                confidence="high",
                reason="The message appears to concern stable or general knowledge.",
                matches=knowledge_matches,
                normalized=normalized,
            )
        return self._result(
            intent="general",
            route="general",
            confidence="medium",
            reason="The message does not clearly match a specialized intent.",
            matches=[],
            normalized=normalized,
        )
    @staticmethod
    def _find_keyword_matches(
        text: str,
        keywords,
    ) -> list[str]:
        return sorted(
            keyword
            for keyword in keywords
            if keyword in text
        )
    @staticmethod
    def _find_pattern_matches(
        text: str,
        patterns,
    ) -> list[str]:
        matches = []
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(pattern)
        return matches
    @staticmethod
    def _result(
        intent: str,
        route: str,
        confidence: str,
        reason: str,
        matches: list[str],
        normalized: str,
    ) -> dict:
        return {
            "intent": intent,
            "route": route,
            "normalized_question": normalized,
            "confidence": confidence,
            "reason": reason,
            "matches": matches,
        }
