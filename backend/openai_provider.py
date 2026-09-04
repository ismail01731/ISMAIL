import os
from openai import OpenAI


class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini"
        ).strip()

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key
            )

    def status(self) -> dict:
        return {
            "provider": "openai",
            "model": self.model,
            "configured": self.client is not None,
        }

    def generate(self, prompt: str) -> str:
        if self.client is None:
            raise RuntimeError(
                "OpenAI API key is not configured."
            )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text.strip()