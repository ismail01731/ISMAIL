import os
from typing import Any
import httpx
from .base import LiveDataProvider
from ..models import LiveData
class NewsAPIProvider(LiveDataProvider):
    name = "newsapi"
    reliability = 0.80
    BASE_URL = (
        "https://newsapi.org/v2/everything"
    )
    def __init__(self):
        self.api_key = os.getenv(
            "NEWS_API_KEY",
            "",
        )
        self.timeout = float(
            os.getenv(
                "REQUEST_TIMEOUT",
                "20",
            )
        )
    def fetch(
        self,
        topic: str,
        **kwargs: Any,
    ) -> list[LiveData]:
        if not self.api_key:
            raise RuntimeError(
                "NEWS_API_KEY is not configured."
            )
        params = {
            "q": topic,
            "language": kwargs.get(
                "language",
                "en",
            ),
            "sortBy": kwargs.get(
                "sortBy",
                "publishedAt",
            ),
            "pageSize": min(
                int(
                    kwargs.get(
                        "pageSize",
                        10,
                    )
                ),
                100,
            ),
        }
        response = httpx.get(
            self.BASE_URL,
            params=params,
            headers={
                "X-Api-Key":
                    self.api_key,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            raise RuntimeError(
                data.get(
                    "message",
                    "News API request failed.",
                )
            )
        results = []
        for article in data.get(
            "articles",
            [],
        ):
            title = article.get(
                "title",
                "",
            )
            description = article.get(
                "description",
                "",
            )
            content = (
                f"{title}. "
                f"{description or ''}"
            ).strip()
            results.append(
                LiveData(
                    topic=topic,
                    value=content,
                    source=(
                        article
                        .get("source", {})
                        .get(
                            "name",
                            "unknown",
                        )
                    ),
                    source_type="major_news",
                    timestamp=article.get(
                        "publishedAt"
                    ),
                    reliability=self.reliability,
                    metadata={
                        "url": article.get(
                            "url"
                        ),
                        "title": title,
                        "author": article.get(
                            "author"
                        ),
                        "description":
                            description,
                    },
                )
            )
        return results
