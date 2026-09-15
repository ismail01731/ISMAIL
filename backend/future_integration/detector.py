from __future__ import annotations
import re
class FutureIntentDetector:
    """
    Detect whether a user message is asking for a future-oriented
    prediction/forecast.
    This is intentionally deterministic and lightweight.
    It does not replace the existing ISMAIL AI intent system.
    """
    ENGLISH_MARKERS = (
        "future",
        "predict",
        "prediction",
        "forecast",
        "forecasting",
        "what will happen",
        "what is likely to happen",
        "will it",
        "will they",
        "will he",
        "will she",
        "will this",
        "will the",
        "next week",
        "next month",
        "next year",
        "next few days",
        "next few weeks",
        "next few months",
        "in the next",
        "over the next",
        "coming days",
        "coming weeks",
        "coming months",
        "upcoming",
        "likely to",
        "expected to",
        "where is this trend going",
        "where could this trend go",
        "trend going",
        "trend direction",
        "future trend",
    )
    BANGLA_MARKERS = (
        "ভবিষ্যৎ",
        "ভবিষ্যতে",
        "ভবিষ্যতের",
        "আগামীকাল",
        "আগামী দিন",
        "আগামী দিনে",
        "আগামী সপ্তাহ",
        "আগামী মাস",
        "আগামী বছর",
        "আগামী কয়েক দিন",
        "আগামী কয়েক দিন",
        "আগামী কয়েক সপ্তাহ",
        "আগামী কয়েক সপ্তাহ",
        "আগামী কয়েক মাস",
        "আগামী কয়েক মাস",
        "পরের দিন",
        "পরের সপ্তাহ",
        "পরের মাস",
        "পরের বছর",
        "পরবর্তী দিন",
        "পরবর্তী সপ্তাহ",
        "পরবর্তী মাস",
        "পরবর্তী বছর",
        "কী হতে পারে",
        "কি হতে পারে",
        "কী হবে",
        "কি হবে",
        "কোথায় যেতে পারে",
        "কোথায় যেতে পারে",
        "কোন দিকে যেতে পারে",
        "কোন দিকে যাবে",
        "কী ঘটতে পারে",
        "কি ঘটতে পারে",
        "সম্ভাবনা কী",
        "সম্ভাবনা কি",
        "পূর্বাভাস",
        "প্রেডিকশন",
        "ফোরকাস্ট",
        "ট্রেন্ড কোন দিকে",
        "ট্রেন্ড কোন দিকে যেতে পারে",
    )
    HORIZON_PATTERN = re.compile(
        r"\b(?:next|in|over|within)\s+"
        r"(?:the\s+)?\d+\s+"
        r"(?:day|days|week|weeks|month|months|year|years)\b",
        re.IGNORECASE,
    )
    BANGLA_HORIZON_PATTERN = re.compile(
        r"(আগামী|পরের|পরবর্তী)\s*\d+\s*"
        r"(দিন|দিনে|সপ্তাহ|সপ্তাহে|মাস|মাসে|বছর|বছরে)"
    )
    @classmethod
    def detect(cls, message: str) -> bool:
        text = (message or "").strip().lower()
        if not text:
            return False
        if any(marker in text for marker in cls.ENGLISH_MARKERS):
            return True
        if any(marker in text for marker in cls.BANGLA_MARKERS):
            return True
        if cls.HORIZON_PATTERN.search(text):
            return True
        if cls.BANGLA_HORIZON_PATTERN.search(text):
            return True
        return False
