from app.plugins.plugin_manager import execute


class Router:

    async def run(self, intent: str, message: str):

        result = await execute(intent, message)

        return result