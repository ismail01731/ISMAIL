async def run(message):

    return {
        "tool": "News",
        "result": "News Plugin"
    }


plugin = {
    "name": "news",
    "run": run
}