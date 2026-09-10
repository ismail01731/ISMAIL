async def run(message):

    return {
        "tool": "General",
        "result": "General Response"
    }


plugin = {
    "name": "general",
    "description": "General Knowledge",

    "capabilities": [
        "general",
        "question",
        "chat"
    ],

    "run": run
}