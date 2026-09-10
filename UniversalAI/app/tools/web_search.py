import httpx


async def search_web(query: str):

    return {
        "success": True,
        "query": query,
        "message": "এখানে পরে Google/Search API যুক্ত হবে।"
    }