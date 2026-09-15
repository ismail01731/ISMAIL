from typing import Any
from .models import LiveData
from .providers.manual import ManualProvider
from .providers.newsapi import NewsAPIProvider
from .providers.alphavantage import AlphaVantageProvider
class LiveDataManager:
    def __init__(self):
        self.providers = {}
        self.register(
            ManualProvider()
        )
        self.register(
            NewsAPIProvider()
        )
        self.register(
            AlphaVantageProvider()
        )
    def register(
        self,
        provider,
    ):
        self.providers[
            provider.name
        ] = provider
    def fetch(
        self,
        provider_name: str,
        topic: str,
        **kwargs: Any,
    ) -> list[LiveData]:
        provider = self.providers.get(
            provider_name
        )
        if provider is None:
            raise ValueError(
                f"Unknown provider: "
                f"{provider_name}"
            )
        return provider.fetch(
            topic,
            **kwargs,
        )
    def available_providers(
        self,
    ) -> list[str]:
        return list(
            self.providers.keys()
        )
