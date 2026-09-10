import os

from app.search.tavily_provider import TavilyProvider


def get_search_provider():

    provider = os.getenv(
        "SEARCH_PROVIDER",
        "tavily"
    )

    if provider == "tavily":
        return TavilyProvider()

    raise Exception("Unknown Search Provider")