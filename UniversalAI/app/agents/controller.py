from app.brain.intent import detect_intent
from app.planner.planner import Planner
from app.brain.router import Router
from app.plugins.capability_matcher import find_plugin


class AgentController:

    def __init__(self):
        self.planner = Planner()
        self.router = Router()

    async def execute(self, message):

        intent = find_plugin(message)

        plan = self.planner.create_plan(intent)

        results = []

        for task in plan:

            result = await self.router.run(
                task.tool,
                message
            )

            results.append(result)

        return {
            "intent": intent,
            "plan": [t.name for t in plan],
            "results": results
        }