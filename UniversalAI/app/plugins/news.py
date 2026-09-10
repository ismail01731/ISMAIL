from app.search.search_engine import search

async def run(message):

    result = search(message)

    news = []

    for item in result["results"]:

        news.append({
            "title": item["title"],
            "content": item["content"],
            "url": item["url"]
        })

    return {
        "tool": "News",
        "result": news
    }


plugin = {
    "name": "news",
    "description": "News Search",
    "capabilities": [
        "news",
        "today news",
        "breaking news",
        "latest news",
        "আজকের খবর",
        "সর্বশেষ খবর",
        "খবর",
        "সংবাদ"
    ],
    "run": run
}