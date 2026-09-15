import os
from typing import Any
import httpx
from .base import LiveDataProvider
from ..models import LiveData
class AlphaVantageProvider(LiveDataProvider):
    name = "alphavantage"
    reliability = 0.85
    BASE_URL = (
        "https://www.alphavantage.co/query"
    )
    def __init__(self):
        self.api_key = os.getenv(
            "ALPHA_VANTAGE_API_KEY",
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
                "ALPHA_VANTAGE_API_KEY "
                "is not configured."
            )
        function = kwargs.get(
            "function",
            "GLOBAL_QUOTE",
        )
        params = {
            "function": function,
            "symbol": topic,
            "apikey": self.api_key,
        }
        response = httpx.get(
            self.BASE_URL,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data:
            raise RuntimeError(
                data["Error Message"]
            )
        if "Note" in data:
            raise RuntimeError(
                data["Note"]
            )
        return [
            LiveData(
                topic=topic,
                value=data,
                source="Alpha Vantage",
                source_type="api",
                reliability=self.reliability,
                metadata={
                    "function": function,
                },
            )
        ]
