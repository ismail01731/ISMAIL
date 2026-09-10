import os
from tavily import TavilyClient


class TavilyProvider:

    def __init__(self):

        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def search(self, query):

        result = self.client.search(
            query=query,
            max_results=5
        )

        return result

def search(self, query):

    print("=" * 50)
    print("QUERY:", query)

    result = self.client.search(
        query=query,
        max_results=5
    )

    print("RESULT:")
    from pprint import pprint
    pprint(result)

    print("=" * 50)

    return result