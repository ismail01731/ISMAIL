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


    CONTEXT_PATTERNS = (
        r"^(এটা|এটির|এটার|ওটা|ওটির|ওটার|সেটা|সেটার|আগেরটা|আগেরটির|আগেরটার)",
        r"^(etar|etār|eta|otar|ota|seta|setar|ager ta|ager tar|agerটার)",
        r"\b(this|that|it|the above|previous one)\b",
        r"(এর জন্য|এটার জন্য|ওটার জন্য|সেটার জন্য|আগেরটার জন্য)",
        r"(etar jonno|otar jonno|setar jonno|ager tar jonno)",
        r"(কোনটা ভালো|কোনটি ভালো|কোনটা ভাল|কোনটি ভাল)",
        r"(which one is better|which is better|what is better)",
        r"(কীভাবে করব|কিভাবে করব|কীভাবে করবো|কিভাবে করবো)",
        r"(kivabe korbo|kibhabe korbo|kivabe korbo)",
        r"(তারপর কি|তারপর কী|এরপর কি|এরপর কী|then what|what next)",
    )



    QUESTION_PATTERNS = (
        r"\?$",
        r"^(what|who|when|where|why|how|which|is|are|can|could|do|does|did)\b",
        r"(কি|কী|কেন|কিভাবে|কীভাবে|কোথায়|কোথায়|কখন|কারা|কে)\s*$",
        r"(কেমন|কত|কোন|কোনটা|কোনটি).*\?$",
    )

    COMMAND_PATTERNS = (
        r"\b(open|close|search|find|show|create|make|write|delete|play|stop|send)\b",
        r"(খুলো|খুলে|খুলুন|দাও|দিন|করো|করুন|লিখো|লিখুন|বানাও|বানান|দেখাও|দেখান|খোঁজো|খুঁজে)\s*$",
        r"\b(teaching|teach|explain|write code|create code)\b",
        r"(শেখাও|শেখান|ব্যাখ্যা কর|কোড লিখে)\s*$",
    )



    def detect(self, message: str) -> dict:
        """Classify the user's message and resolve intent conflicts."""

        text = message.strip()

        if not text:
            raise ValueError("Message cannot be empty.")

        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        input_type = self._detect_input_type(normalized)

        conversation_matches = self._find_pattern_matches(
            normalized,
            self.CONVERSATION_PATTERNS,
        )


        context_matches = self._find_pattern_matches(
            normalized,
            self.CONTEXT_PATTERNS,
        )


        live_matches = self._find_keyword_matches(
            normalized,
            self.LIVE_KEYWORDS,
        )

        knowledge_matches = self._find_keyword_matches(
            normalized,
            self.KNOWLEDGE_KEYWORDS,
        )


        if context_matches:
            return self._result(
                intent="contextual",
                route="general",
                confidence="high",
                reason="The message depends on previous conversation context.",
                matches=context_matches,
                normalized=normalized,
                input_type=input_type,
            )




        if conversation_matches:
            return self._result(
                intent="conversation",
                route="general",
                confidence="high",
                reason="The message appears to be conversational.",
                matches=conversation_matches,
                normalized=normalized,
                input_type=input_type,
            )

        intent_scores = self._calculate_scores(
            normalized,
            live_matches,
            knowledge_matches,
        )


        if (
            intent_scores["live"] == 0
            and intent_scores["knowledge"] == 0
        ):
            return self._result(
                intent="general",
                route="general",
                confidence="medium",
                reason="The message does not clearly match a specialized intent.",
                matches=[],
                normalized=normalized,
                input_type=input_type,
            )

        best_intent = max(
            intent_scores,
            key=intent_scores.get,
        )

        if best_intent == "live":
            return self._result(
                intent="live_information",
                route="live",
                confidence=self._score_confidence(
                    intent_scores["live"]
                ),
                reason="The message appears to require current or time-sensitive information.",
                matches=live_matches,
                normalized=normalized,
                input_type=input_type,
            )

        if best_intent == "knowledge":
            return self._result(
                intent="knowledge",
                route="knowledge",
                confidence=self._score_confidence(
                    intent_scores["knowledge"]
                ),
                reason="The message appears to concern stable or general knowledge.",
                matches=knowledge_matches,
                normalized=normalized,
                input_type=input_type,
            )

        return self._result(
            intent="general",
            route="general",
            confidence="medium",
            reason="The message does not clearly match a specialized intent.",
            matches=[],
            normalized=normalized,
            input_type=input_type,
        )


    def _detect_input_type(self, text: str) -> str:
        """Detect whether the user is asking a question or giving a command."""

        command_matches = self._find_pattern_matches(
            text,
            self.COMMAND_PATTERNS,
        )

        question_matches = self._find_pattern_matches(
            text,
            self.QUESTION_PATTERNS,
        )

        # A direct question mark is a strong question signal.
        if text.endswith("?") or text.endswith("؟"):
            return "question"

        if command_matches and not question_matches:
            return "command"

        if question_matches:
            return "question"

        if command_matches:
            return "command"

        return "statement"





    def _calculate_scores(
        self,
        text: str,
        live_matches: list[str],
        knowledge_matches: list[str],
    ) -> dict:
        """Calculate scores and resolve live/knowledge conflicts."""

        live_score = len(live_matches)
        knowledge_score = len(knowledge_matches)

        weak_time_words = {
            "today",
            "tonight",
            "now",
            "আজ",
            "এখন",
        }

        strong_live_words = {
            "weather",
            "temperature",
            "forecast",
            "news",
            "price",
            "prices",
            "stock",
            "score",
            "match",
            "matches",
            "earthquake",
            "outage",
            "latest",
            "current",
            "currently",
            "version",
            "release",
            "আবহাওয়া",
            "আবহাওয়া",
            "তাপমাত্রা",
            "পূর্বাভাস",
            "খবর",
            "দাম",
            "মূল্য",
            "স্কোর",
            "ম্যাচ",
            "ভূমিকম্প",
            "সর্বশেষ",
            "বর্তমানে",
            "সংস্করণ",
            "রিলিজ",
        }

        strong_live_matches = [
            word
            for word in live_matches
            if word in strong_live_words
        ]

        weak_time_matches = [
            word
            for word in live_matches
            if word in weak_time_words
        ]

        if strong_live_matches:
            live_score += 3

        if weak_time_matches and not strong_live_matches:
            live_score -= len(weak_time_matches)

        learning_patterns = (
            "how to learn",
            "how can i learn",
            "learn python",
            "শিখব",
            "শিখতে",
            "শেখাও",
            "শেখান",
        )

        if any(
            pattern in text
            for pattern in learning_patterns
        ):
            knowledge_score += 2

        return {
            "live": max(live_score, 0),
            "knowledge": max(knowledge_score, 0),
            "general": 0,
        }


    @staticmethod
    def _score_confidence(score: int) -> str:
        """Convert an intent score into a confidence label."""

        if score >= 4:
            return "high"

        if score >= 2:
            return "medium"

        return "low"




    
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
        input_type: str,
    ) -> dict:
        return {
            "intent": intent,
            "route": route,
            "input_type": input_type,
            "normalized_question": normalized,
            "confidence": confidence,
            "reason": reason,
            "matches": matches,
        }


        
    
