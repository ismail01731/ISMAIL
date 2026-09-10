from app.agents.modules.weather_agent import WeatherAgent
from app.agents.modules.sports_agent import SportsAgent
from app.agents.modules.news_agent import NewsAgent
from app.agents.modules.response_agent import ResponseAgent


class MultiAgent:

    def __init__(self):

        self.weather = WeatherAgent()
        self.sports = SportsAgent()
        self.news = NewsAgent()
        self.response = ResponseAgent()

    async def execute(self, message):

        results = []

        text = message.lower()

        if "weather" in text or "আবহাওয়া" in text:
            results.append(await self.weather.execute(message))

        if (
            "messi" in text
            or "cricket" in text
            or "football" in text
            or "খেলা" in text
        ):
            results.append(await self.sports.execute(message))

        if "news" in text or "সংবাদ" in text:
            results.append(await self.news.execute(message))

        if not results:
            results.append({
                "agent": "General",
                "result": "No Specialized Agent Needed"
            })

        return await self.response.execute(results)