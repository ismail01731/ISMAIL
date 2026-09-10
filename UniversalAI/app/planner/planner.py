from app.planner.task import Task


class Planner:

    def create_plan(self, intent: str):

        if intent == "sports":
            return [
                Task(
                    name="Search Sports",
                    tool="sports"
                )
            ]

        elif intent == "news":
            return [
                Task(
                    name="Search News",
                    tool="news"
                )
            ]

        else:
            return [
                Task(
                    name="General",
                    tool="general"
                )
            ]