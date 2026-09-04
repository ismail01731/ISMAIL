import os
from openai import OpenAI


class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini"
        ).strip()

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
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
                "OpenRouter API key is not configured."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content.strip()