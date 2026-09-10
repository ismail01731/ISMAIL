class ContextManager:

    def build(
        self,
        message,
        history,
        tool_results
    ):

        prompt = f"""
You are Universal AI.

Answer naturally in Bangla.

Conversation History
--------------------
{history}

User Question
-------------
{message}

Tool Results
------------
{tool_results}

Instructions
------------
1. Use Tool Results if available.
2. Use Conversation History.
3. If Tool Results contain live information,
   prefer them.
4. Never say "I cannot access the internet"
   if Tool Results already exist.
5. Answer clearly in Bangla.
"""

        return prompt