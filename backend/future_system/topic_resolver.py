from __future__ import annotations
import re
from typing import Iterable
class HistoricalTopicResolver:
    """
    Resolves a future question to an existing
    historical database topic.
    Priority:
        1. Exact topic match
        2. Case-insensitive match
        3. Symbol-like token match
        4. Phrase containment
        5. Cleaned question fallback
    """
    STOP_WORDS = {
        "what",
        "will",
        "happen",
        "happens",
        "could",
        "would",
        "should",
        "predict",
        "prediction",
        "forecast",
        "future",
        "next",
        "month",
        "months",
        "week",
        "weeks",
        "day",
        "days",
        "trend",
        "price",
        "the",
        "this",
        "that",
        "is",
        "are",
        "to",
        "in",
        "for",
        "of",
        "on",
        "আগামী",
        "পরের",
        "পরবর্তী",
        "ভবিষ্যতে",
        "ভবিষ্যতের",
        "কী",
        "কি",
        "হবে",
        "হতে",
        "পারে",
        "যাবে",
        "যেতে",
        "দাম",
        "ট্রেন্ড",
        "কোন",
        "দিকে",
    }
    @staticmethod
    def _normalize(value: str) -> str:
        value = str(value or "").strip().lower()
        value = re.sub(r"\s+", " ", value)
        return value
    @classmethod
    def _tokens(cls, value: str) -> list[str]:
        text = cls._normalize(value)
        tokens = re.findall(
            r"[a-zA-Z0-9_.$-]+|[\u0980-\u09FF]+",
            text,
        )
        return [
            token
            for token in tokens
            if token not in cls.STOP_WORDS
            and len(token) >= 2
        ]
    @classmethod
    def resolve(
        cls,
        question: str,
        available_topics: Iterable[str],
    ) -> dict:
        question = str(question or "").strip()
        topics = [
            str(topic).strip()
            for topic in available_topics
            if str(topic).strip()
        ]
        if not question:
            return {
                "topic": "",
                "method": "empty",
                "score": 0.0,
            }
        if not topics:
            return {
                "topic": question,
                "method": "question_fallback",
                "score": 0.0,
            }
        normalized_question = cls._normalize(question)
        # 1. Exact match
        for topic in topics:
            if normalized_question == cls._normalize(topic):
                return {
                    "topic": topic,
                    "method": "exact",
                    "score": 1.0,
                }
        question_tokens = set(cls._tokens(question))
        candidates = []
        for topic in topics:
            normalized_topic = cls._normalize(topic)
            topic_tokens = set(cls._tokens(topic))
            if not topic_tokens:
                continue
            # 2. Direct topic contained in question
            if normalized_topic in normalized_question:
                candidates.append(
                    (1.0, topic, "containment")
                )
                continue
            # 3. Token overlap
            overlap = question_tokens.intersection(
                topic_tokens
            )
            if overlap:
                score = len(overlap) / len(topic_tokens)
                candidates.append(
                    (
                        min(score, 0.95),
                        topic,
                        "token_match",
                    )
                )
        if candidates:
            candidates.sort(
                key=lambda item: item[0],
                reverse=True,
            )
            score, topic, method = candidates[0]
            return {
                "topic": topic,
                "method": method,
                "score": round(score, 4),
            }
        # 4. Symbol-like token fallback
        symbols = re.findall(
            r"\b[A-Z]{2,10}\b",
            question,
        )
        for symbol in symbols:
            for topic in topics:
                if cls._normalize(topic) == symbol.lower():
                    return {
                        "topic": topic,
                        "method": "symbol_match",
                        "score": 0.90,
                    }
        return {
            "topic": question,
            "method": "question_fallback",
            "score": 0.0,
        }
