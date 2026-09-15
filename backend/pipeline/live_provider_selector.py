from __future__ import annotations
import os
import re
from typing import Any
class LiveProviderSelector:
    """
    Automatically selects the best available live provider.
    Rules:
        Symbol-like topic
            -> Alpha Vantage
        General/news topic
            -> NewsAPI
        Missing API key
            -> no automatic provider
    The selector never exposes API keys.
    """
    MARKET_PATTERN = re.compile(
        r"^[A-Z]{2,10}(?:[-.][A-Z0-9]{1,8})?$"
    )
    MARKET_KEYWORDS = {
        "stock",
        "stocks",
        "share",
        "shares",
        "stock price",
        "share price",
        "market",
        "crypto",
        "bitcoin",
        "ethereum",
        "forex",
        "currency",
        "gold",
        "silver",
        "oil",
        "nasdaq",
        "dow",
        "s&p",
    }
    def __init__(
        self,
        news_api_key: str | None = None,
        alpha_vantage_api_key: str | None = None,
    ):
        self.news_api_key = (
            news_api_key
            or os.getenv("NEWS_API_KEY")
            or ""
        )
        self.alpha_vantage_api_key = (
            alpha_vantage_api_key
            or os.getenv("ALPHA_VANTAGE_API_KEY")
            or os.getenv("ALPHAVANTAGE_API_KEY")
            or ""
        )
    @staticmethod
    def _normalize(topic: str) -> str:
        return re.sub(
            r"\s+",
            " ",
            str(topic or "").strip().lower(),
        )
    @classmethod
    def _is_market_topic(
        cls,
        topic: str,
    ) -> bool:
        normalized = cls._normalize(topic)
        if not normalized:
            return False
        upper = normalized.upper()
        if cls.MARKET_PATTERN.fullmatch(upper):
            return True
        return any(
            keyword in normalized
            for keyword in cls.MARKET_KEYWORDS
        )
    def select(
        self,
        topic: str,
        preferred: str | None = None,
    ) -> dict[str, Any]:
        topic = str(topic or "").strip()
        if not topic:
            return {
                "provider": None,
                "reason": "empty_topic",
                "available": False,
            }
        if preferred:
            preferred = (
                str(preferred)
                .strip()
                .lower()
            )
            if preferred == "alphavantage":
                if self.alpha_vantage_api_key:
                    return {
                        "provider": "alphavantage",
                        "reason": "preferred_provider",
                        "available": True,
                    }
            if preferred == "newsapi":
                if self.news_api_key:
                    return {
                        "provider": "newsapi",
                        "reason": "preferred_provider",
                        "available": True,
                    }
        if self._is_market_topic(topic):
            if self.alpha_vantage_api_key:
                return {
                    "provider": "alphavantage",
                    "reason": "market_topic",
                    "available": True,
                }
            if self.news_api_key:
                return {
                    "provider": "newsapi",
                    "reason": (
                        "market_topic_alpha_unavailable"
                    ),
                    "available": True,
                }
            return {
                "provider": None,
                "reason": (
                    "market_topic_no_provider_key"
                ),
                "available": False,
            }
        if self.news_api_key:
            return {
                "provider": "newsapi",
                "reason": "general_topic",
                "available": True,
            }
        if self.alpha_vantage_api_key:
            return {
                "provider": "alphavantage",
                "reason": (
                    "general_topic_news_unavailable"
                ),
                "available": True,
            }
        return {
            "provider": None,
            "reason": "no_provider_key",
            "available": False,
        }
    def status(self) -> dict[str, Any]:
        return {
            "newsapi_configured": bool(
                self.news_api_key
            ),
            "alphavantage_configured": bool(
                self.alpha_vantage_api_key
            ),
        }
