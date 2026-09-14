from .emotion_models import EmotionResult
class EmotionEngine:
    """
    First-stage emotional state detector for ISMAIL AI.
    Detects common Bangla and English emotional expressions.
    This is intentionally lightweight; contextual LLM analysis
    can be added as a later layer.
    """
    EMOTION_KEYWORDS = {
        "sad": [
            "sad",
            "unhappy",
            "depressed",
            "cry",
            "crying",
            "মন খারাপ",
            "মনটা খারাপ",
            "মন খুব খারাপ",
            "মন ভালো নেই",
            "মনটা ভালো নেই",
            "মন ভালো লাগছে না",
            "মনটা ভালো লাগছে না",
            "ভালো লাগছে না",
            "ভালো লাগছে না আজ",
            "খারাপ লাগছে",
            "খুব খারাপ লাগছে",
            "অনেক কষ্ট",
            "খুব কষ্ট",
            "কষ্ট হচ্ছে",
            "কষ্ট লাগছে",
            "দুঃখ",
            "কাঁদতে ইচ্ছা",
            "কান্না পাচ্ছে",
            "কান্না",
        ],
        "lonely": [
            "lonely",
            "alone",
            "feeling alone",
            "একাকী",
            "একাকিত্ব",
            "একা লাগছে",
            "একা লাগে",
            "খুব একা",
            "অনেক একা",
            "একা হয়ে গেছি",
            "একলা লাগছে",
            "একলা লাগে",
            "কেউ নেই",
            "কেউ আমার পাশে নেই",
            "কাউকে পাশে পাচ্ছি না",
            "কাউকে আমার পাশে পাচ্ছি না",
            "আমার পাশে কেউ নেই",
            "কারো সাথে কথা বলার নেই",
            "কারও সাথে কথা বলার নেই",
        ],
        "happy": [
            "happy",
            "glad",
            "good",
            "great",
            "feeling good",
            "ভালো লাগছে",
            "অনেক ভালো",
            "খুব ভালো",
            "মন ভালো",
            "মনটা ভালো",
            "খুশি",
            "অনেক খুশি",
            "খুব খুশি",
            "আনন্দ",
            "সুখী",
        ],
        "excited": [
            "excited",
            "amazing",
            "wow",
            "দারুণ",
            "দারুণ লাগছে",
            "খুব দারুণ",
            "এক্সাইটেড",
            "অনেক excited",
            "খুব excited",
            "রোমাঞ্চিত",
            "অসাধারণ",
        ],
        "angry": [
            "angry",
            "mad",
            "furious",
            "রাগ",
            "রাগ লাগছে",
            "রাগ হচ্ছে",
            "খুব রাগ",
            "অনেক রাগ",
            "রেগে আছি",
            "বিরক্ত",
            "খুব বিরক্ত",
            "অনেক বিরক্ত",
            "ক্ষিপ্ত",
        ],
        "stressed": [
            "stress",
            "stressed",
            "tension",
            "pressure",
            "চাপ",
            "অনেক চাপ",
            "খুব চাপ",
            "টেনশন",
            "অনেক টেনশন",
            "খুব টেনশন",
            "স্ট্রেস",
            "অনেক স্ট্রেস",
            "দুশ্চিন্তা",
            "অনেক দুশ্চিন্তা",
            "চিন্তায় আছি",
            "চিন্তা হচ্ছে",
        ],
        "fun": [
            "joke",
            "funny",
            "fun",
            "মজা",
            "মজা করতে",
            "মজা চাই",
            "হাসাও",
            "হাসাতে",
            "জোক",
            "জোক বলো",
            "হাসতে চাই",
            "মজার",
            "একটু হাসাও",
        ],
        "romantic": [
            "love",
            "romantic",
            "ভালোবাসি",
            "ভালোবাসা",
            "রোমান্টিক",
            "রোমান্টিক কথা",
            "প্রেম",
            "প্রেমের",
            "তোমাকে ভালোবাসি",
        ],
        "confused": [
            "confused",
            "don't understand",
            "do not understand",
            "বুঝতে পারছি না",
            "বুঝি না",
            "কনফিউজড",
            "দ্বিধায়",
            "কী করব বুঝতে পারছি না",
        ],
    }
    # Expressions where "ভালো" does NOT mean happy.
    SAD_PRIORITY_PHRASES = [
        "মনটা খুব খারাপ",
        "???? ?????",
        "মন ভালো নেই",
        "মনটা ভালো নেই",
        "মন ভালো লাগছে না",
        "মনটা ভালো লাগছে না",
        "মনটা খারাপ হয়ে গেছে",
        "মন খারাপ হয়ে গেছে",
        "আবার মনটা খারাপ",
        "ভালো লাগছে না",
    ]
    LONELY_PRIORITY_PHRASES = [
        "কাউকে পাশে পাচ্ছি না",
        "কাউকে আমার পাশে পাচ্ছি না",
        "আমার পাশে কেউ নেই",
        "কেউ আমার পাশে নেই",
        "কারো সাথে কথা বলার নেই",
        "কারও সাথে কথা বলার নেই",
    ]
    def _detect_from_context(
        self,
        text: str,
        conversation_context: str,
    ) -> EmotionResult | None:
        """Infer emotional continuity from recent conversation."""
        if not text or not conversation_context:
            return None
        continuity_phrases = [
            "এখনও",
            "এখনো",
            "আরও",
            "আবার",
            "সেই জন্য",
            "ওটার জন্য",
            "এটার জন্য",
            "আগেরটার জন্য",
            "আগের কথার পর",
            "তাই",
            "still",
            "again",
            "because of that",
            "that's why",
        ]
        if not any(
            phrase in text
            for phrase in continuity_phrases
        ):
            return None
        previous_user_messages = []
        for line in conversation_context.splitlines():
            if line.lower().startswith("user:"):
                content = line[5:].strip()
                if content:
                    previous_user_messages.append(content)
        if not previous_user_messages:
            return None
        previous_text = " ".join(
            previous_user_messages[-5:]
        )
        previous_result = self.detect(previous_text)
        if previous_result.emotion == "neutral":
            return None
        return EmotionResult(
            emotion=previous_result.emotion,
            confidence=min(
                round(previous_result.confidence * 0.85, 2),
                0.80,
            ),
            signals=[
                "context:" + previous_result.emotion
            ],
        )

    def detect(
        self,
        message: str,
        conversation_context: str = "",
    ) -> EmotionResult:
        text = " ".join(
            (message or "").strip().lower().split()
        )
        if not text:
            return EmotionResult(
                emotion="neutral",
                confidence=1.0,
                signals=[],
            )

        # Strong contextual phrases get priority.
        for phrase in self.SAD_PRIORITY_PHRASES:
            if phrase in text:
                return EmotionResult(
                    emotion="sad",
                    confidence=0.90,
                    signals=[phrase],
                )
        for phrase in self.LONELY_PRIORITY_PHRASES:
            if phrase in text:
                return EmotionResult(
                    emotion="lonely",
                    confidence=0.90,
                    signals=[phrase],
                )
        scores = {}
        signals = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            matched = []
            for keyword in keywords:
                keyword = keyword.lower().strip()
                if keyword and keyword in text:
                    matched.append(keyword)
            if matched:
                # Longer phrases carry more meaning than
                # single generic words.
                score = sum(
                    1 + (len(keyword.split()) * 0.25)
                    for keyword in matched
                )
                scores[emotion] = score
                signals[emotion] = matched
        if not scores:
            context_result = self._detect_from_context(
                text,
                conversation_context,
            )
            if context_result is not None:
                return context_result
            return EmotionResult(
                emotion="neutral",
                confidence=0.50,
                signals=[],
            )
        emotion = max(scores, key=scores.get)
        score = scores[emotion]
        # Keep confidence conservative in this first-stage detector.
        confidence = min(
            0.55 + (score - 1) * 0.10,
            0.90,
        )
        return EmotionResult(
            emotion=emotion,
            confidence=round(confidence, 2),
            signals=signals[emotion],
        )
emotion_engine = EmotionEngine()



