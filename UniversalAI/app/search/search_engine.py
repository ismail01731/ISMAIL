from app.search.provider_factory import get_search_provider

provider = get_search_provider()


def search(query):

    return provider.search(query)