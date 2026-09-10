class ResponseAgent:

    async def execute(self, results):

        text = ""

        for item in results:
            text += f"{item['agent']}: {item['result']}\n"

        return text