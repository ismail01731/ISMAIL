from app.search.search_engine import search

async def run(message):

    result = search(message)

    sports = []

    for item in result["results"]:

        sports.append({
            "title": item["title"],
            "content": item["content"],
            "url": item["url"]
        })

    return {
        "tool": "Sports",
        "result": sports
    }


plugin = {
    "name": "sports",
    "description": "Sports",
    "capabilities": [
        "sports",
        "football",
        "cricket",
        "messi",
        "ronaldo",
        "খেলা"
    ],
    "run": run
}