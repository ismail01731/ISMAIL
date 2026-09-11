from datetime import datetime, timedelta, timezone
from typing import Optional


class FreshnessEngine:
    """Central TTL policy for cached knowledge."""

    TTL_POLICY = {
        "finance": 15,
        "weather": 60,
        "sports": 60,
        "news": 1440,
        "general_live": 10080,
    }

    @classmethod
    def calculate_expiry(
        cls,
        topic: str,
        knowledge_type: str,
    ) -> Optional[str]:
        """Return an expiry timestamp for temporary knowledge.

        Permanent knowledge never expires. Topic matching is intentionally
        conservative and uses the most time-sensitive matching category.
        """
        if str(knowledge_type or "").strip().lower() == "permanent":
            return None

        topic_clean = str(topic or "").lower().strip()

        if any(k in topic_clean for k in (
            "stock", "price", "crypto", "bitcoin", "finance", "market",
            "শেয়ার", "শেয়ার", "দাম", "মূল্য", "ক্রিপ্টো",
        )):
            minutes = cls.TTL_POLICY["finance"]
        elif any(k in topic_clean for k in (
            "weather", "temperature", "rain", "forecast",
            "আবহাওয়া", "আবহাওয়া", "তাপমাত্রা", "বৃষ্টি", "পূর্বাভাস",
        )):
            minutes = cls.TTL_POLICY["weather"]
        elif any(k in topic_clean for k in (
            "score", "match", "sports", "game", "খেলা", "স্কোর", "ম্যাচ",
        )):
            minutes = cls.TTL_POLICY["sports"]
        elif any(k in topic_clean for k in (
            "news", "today", "event", "current", "latest",
            "খবর", "সংবাদ", "আজ", "সর্বশেষ", "সাম্প্রতিক",
        )):
            minutes = cls.TTL_POLICY["news"]
        else:
            minutes = cls.TTL_POLICY["general_live"]

        return (
            datetime.now(timezone.utc)
            + timedelta(minutes=minutes)
        ).isoformat()
