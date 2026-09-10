from app.search.search_engine import search


async def run(message):

    result = search(message)

    return {
        "tool": "Weather",
        "result": result["results"]
    }