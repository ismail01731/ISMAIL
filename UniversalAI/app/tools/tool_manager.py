from app.tools.sports import sports_tool
from app.tools.news import news_tool
from app.tools.weather import weather_tool
from app.tools.general import general_tool


async def execute_tool(intent: str, message: str):

    if intent == "sports":
        return await sports_tool(message)

    elif intent == "news":
        return news_tool(message)

    elif intent == "weather":
        return weather_tool(message)

    else:
        return general_tool(message)