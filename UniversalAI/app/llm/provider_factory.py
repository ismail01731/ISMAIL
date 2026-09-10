import os
from dotenv import load_dotenv

from app.llm.groq_provider import GroqProvider

load_dotenv()


def get_provider():

    provider = os.getenv("LLM_PROVIDER")

    if provider == "groq":
        return GroqProvider()

    raise Exception("LLM Provider Not Found")