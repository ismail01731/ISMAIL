from app.planner.task import Task


class Planner:

    def create_plan(self, intents):

        if isinstance(intents, str):
            intents = [intents]

        tasks = []

        for intent in intents:

            if intent == "news":

                tasks.append(
                    Task(
                        name="Search News",
                        tool="news"
                    )
                )

            elif intent == "weather":

                tasks.append(
                    Task(
                        name="Weather",
                        tool="weather"
                    )
                )

            elif intent == "sports":

                tasks.append(
                    Task(
                        name="Sports",
                        tool="sports"
                    )
                )

            else:

                tasks.append(
                    Task(
                        name="General",
                        tool="general"
                    )
                )

        return tasks