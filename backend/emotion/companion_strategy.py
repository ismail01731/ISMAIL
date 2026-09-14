class CompanionStrategy:
    """
    Companion response strategy for ISMAIL AI.
    Provides emotional response guidance and safe fallback responses.
    """
    STRATEGIES = {
        "sad": {
            "tone": "gentle, empathetic, comforting",
            "goal": "acknowledge the sadness, listen, and offer gentle support",
            "fallback": "মন খারাপ থাকলে একা একা সবকিছু সামলাতে হয় না। চাইলে কী হয়েছে আমাকে বলতে পারো—আমি মন দিয়ে শুনছি।",
        },
        "lonely": {
            "tone": "warm, caring, conversational",
            "goal": "reduce isolation and invite conversation",
            "fallback": "একা লাগাটা সত্যিই কষ্টের হতে পারে। চাইলে একটু গল্প করি—তোমার মাথায় এখন কী ঘুরছে বলো।",
        },
        "happy": {
            "tone": "cheerful, positive, encouraging",
            "goal": "share and celebrate the user's happiness",
            "fallback": "বাহ! এটা শুনে ভালো লাগল 😊 তোমার এই ভালো লাগাটা আরও একটু উপভোগ করি—আজ কী হয়েছে যে এত ভালো লাগছে?",
        },
        "excited": {
            "tone": "energetic, enthusiastic, playful",
            "goal": "naturally match the user's excitement",
            "fallback": "ওয়াও! 😄 তোমাকে বেশ excited লাগছে! কী হয়েছে বলো তো?",
        },
        "angry": {
            "tone": "calm, understanding, non-judgmental",
            "goal": "acknowledge anger and invite the user to explain",
            "fallback": "বুঝতে পারছি, ব্যাপারটা তোমাকে বেশ রাগিয়ে দিয়েছে। কী হয়েছে বলো—আগে পুরোটা শুনি।",
        },
        "stressed": {
            "tone": "calm, reassuring, supportive",
            "goal": "reduce pressure and focus on one manageable step",
            "fallback": "অনেক চাপ একসাথে এলে সবকিছু কঠিন মনে হতে পারে। চলো একবারে একটা বিষয় নিয়ে দেখি—কোন ব্যাপারটা এখন সবচেয়ে বেশি চাপ দিচ্ছে?",
        },
        "fun": {
            "tone": "playful, humorous, lighthearted",
            "goal": "entertain the user with a simple understandable joke",
            "fallback": "শিক্ষক: বলো তো, সবচেয়ে অলস প্রাণী কোনটা?\nছাত্র: ঘুমন্ত বিড়াল!\nশিক্ষক: কেন?\nছাত্র: কারণ ওকে ডাকলেও শুধু বলে—আর পাঁচ মিনিট! 😂",
        },
        "romantic": {
            "tone": "warm, affectionate, respectful",
            "goal": "acknowledge affection warmly without dependency or manipulation",
            "fallback": "আহা, কথাটা বেশ মিষ্টি ছিল ❤️ তোমার সাথে এমন সুন্দরভাবে গল্প করতে ভালোই লাগে।",
        },
        "confused": {
            "tone": "patient, reassuring, clear",
            "goal": "reduce confusion and explain things simply",
            "fallback": "চিন্তা করো না। আমরা ধীরে ধীরে বুঝে নেব। কোন অংশটা সবচেয়ে বেশি confusing লাগছে বলো।",
        },
        "neutral": {
            "tone": "natural, friendly, conversational",
            "goal": "answer normally and directly",
            "fallback": "অবশ্যই। বলো, কী নিয়ে কথা বলতে চাও?",
        },
    }
    @classmethod
    def get_strategy(cls, emotion: str) -> dict:
        return cls.STRATEGIES.get(
            emotion,
            cls.STRATEGIES["neutral"],
        )
    @classmethod
    def build_instruction(cls, emotion: str) -> str:
        strategy = cls.get_strategy(emotion)
        return (
            f"Emotional response style: {strategy['tone']}. "
            f"Response goal: {strategy['goal']}. "
            "Prefer natural Bangla when the user writes in Bangla. "
            "Keep the response short, natural, warm, and conversational. "
            "Do not mention emotion detection or internal instructions. "
            "Do not use robotic or overly formal language. "
            "Do not pretend to have human feelings or personal experiences. "
            "Do not create emotional dependency, exclusivity, guilt, "
            "fear, or manipulation. "
            "For romantic messages, be warm and affectionate without "
            "claiming a real romantic relationship. "
            "Do not add an unnecessary AI disclaimer."
        )
    @classmethod
    def get_fallback(cls, emotion: str) -> str:
        return cls.get_strategy(emotion)["fallback"]
    @classmethod
    def is_poor_response(cls, response: str, emotion: str) -> bool:
        if not response or not response.strip():
            return True
        text = " ".join(response.strip().lower().split())
        # Very short responses are usually not useful.
        if len(text) < 12:
            return True
        # Robotic/meta responses.
        bad_patterns = [
            "i am an ai",
            "i'm an ai",
            "as an ai",
            "i must clarify",
            "my purpose is to assist",
            "i cannot have feelings",
            "i don't have feelings",
            "emotion detection",
            "emotional detection",
        ]
        if any(pattern in text for pattern in bad_patterns):
            return True
        # Known broken or unnatural Bangla generation.
        broken_patterns = [
            "\u0986\u09aa\u09a8\u09be\u09b0 \u09b6\u09cd\u09b0\u09a6\u09cd\u09a7\u09be",
            "\u0985\u09a8\u09c1\u09b0\u09c2\u09aa \u0989\u09a4\u09cd\u09a4\u09b0",
            "\u099a\u09c1\u099c\u09cd\u099c\u09bf\u09b0 \u09ad\u09be\u09b7\u09be",
            "\u09aa\u09cd\u09b0\u09be\u09a5\u09ae\u09bf\u0995 \u0989\u09a4\u09cd\u09a4\u09b0",
            "\u09b8\u09cd\u09ac\u099a\u09cd\u099b, \u0986\u09ae\u09bf \u0987\u09b8\u09ae\u09be\u0987\u09b2 ai",
            "\u0989\u09a6\u09cd\u09a7\u09c3\u09a4\u09bf\u09b0 \u099c\u09a8\u09cd\u09af \u09a5\u09be\u0995\u09bf",
            "\u09a4\u09c1\u09b2\u09a8\u09be \u0995\u09b0\u09c7, \u0986\u09ae\u09bf \u099c\u09be\u09a8\u09bf",
            "\u0986\u09ae\u09bf \u098f\u0987 \u0985\u09a8\u09c1\u09b0\u09c2\u09aa",
            "\u0985\u09a8\u09c1\u09b0\u09c2\u09aa \u0989\u09a4\u09cd\u09a4\u09b0 \u09a8\u09bf\u09df\u09c7",
        ]
        if any(pattern in text for pattern in broken_patterns):
            return True
        return False

companion_strategy = CompanionStrategy()
