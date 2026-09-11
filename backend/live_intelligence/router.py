import re

from backend.live_intelligence.time_engine import TimeEngine


class LiveIntelligenceRouter:
    """
    Routes current-information questions to the correct
    live-information engine.
    """

    TIME_PATTERNS = (
        r"\bwhat time is it\b",
        r"\bwhat's the time\b",
        r"\bcurrent time\b",
        r"\btime now\b",
        r"\btime is it\b",

        r"এখন কয়টা বাজে",
        r"এখন কয়টা বাজে",
        r"এখন কত বাজে",
        r"কয়টা বাজে",
        r"কয়টা বাজে",
        r"এখন সময় কত",
        r"এখন সময় কত",
    )

    DATE_PATTERNS = (
        r"\bwhat date is it\b",
        r"\bwhat's today's date\b",
        r"\btoday's date\b",
        r"\bwhat day is it\b",
        r"\bcurrent date\b",

        r"আজ কত তারিখ",
        r"আজকের তারিখ",
        r"আজ তারিখ কত",
        r"আজকে কত তারিখ",
        r"আজ কী বার",
        r"আজ কি বার",
        r"আজ কোন বার",
    )

    @classmethod
    def _matches(cls, message: str, patterns: tuple[str, ...]) -> bool:
        text = message.strip().lower()

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    @classmethod
    def detect(cls, message: str) -> str:
        """
        Detect the specific live-information category.
        """

        if not message:
            return "none"

        if cls._matches(message, cls.TIME_PATTERNS):
            return "time"

        if cls._matches(message, cls.DATE_PATTERNS):
            return "date"

        return "none"

    @classmethod
    def handle(cls, message: str):
        """
        Handle supported live-information requests.

        Returns:
            dict | None
        """

        route = cls.detect(message)

        if route == "time":
            return TimeEngine.get_time()

        if route == "date":
            return TimeEngine.get_date()

        return None