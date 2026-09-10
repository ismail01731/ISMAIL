from app.search.search_engine import search


async def run(message):

    result = search(message)

    return {
        "tool": "Sports",
        "result": result
    }


plugin = {
    "name": "sports",
    "run": run
}