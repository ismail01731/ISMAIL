import os

from openai import OpenAI


class OpenAIProvider:
    """OpenAI-compatible provider client for OpenAI, OpenRouter and Groq."""

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "").strip().lower()

        if self.provider == "groq":
            self.api_key = os.getenv("GROQ_API_KEY", "").strip()
            self.model = os.getenv(
                "AI_MODEL",
                "openai/gpt-oss-20b",
            ).strip()
            self.base_url = os.getenv(
                "AI_BASE_URL",
                "https://api.groq.com/openai/v1",
            ).strip()
        elif self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
            self.model = os.getenv(
                "AI_MODEL",
                os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            ).strip()
            self.base_url = os.getenv("AI_BASE_URL", "").strip() or None
        elif self.provider == "openrouter":
            self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
            self.model = os.getenv(
                "AI_MODEL",
                os.getenv("OPENAI_MODEL", "openai/gpt-5-mini"),
            ).strip()
            self.base_url = os.getenv(
                "AI_BASE_URL",
                "https://openrouter.ai/api/v1",
            ).strip()
        else:
            self.api_key = ""
            self.model = os.getenv("AI_MODEL", "").strip()
            self.base_url = None

        self.client = None

        if self.api_key:
            kwargs = {
                "api_key": self.api_key,
                "timeout": 60.0,
                "max_retries": 2,
            }
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self.client = OpenAI(**kwargs)

    def status(self) -> dict:
        return {
            "provider": self.provider or None,
            "model": self.model or None,
            "configured": bool(self.client and self.model),
        }

    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if self.client is None:
            raise RuntimeError(
                f"{self.provider or 'AI'} provider is not configured."
            )

        if not self.model:
            raise RuntimeError("AI model is not configured.")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        if not response.choices:
            raise RuntimeError("AI provider returned no choices.")

        content = response.choices[0].message.content

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("AI provider returned an empty response.")

        return content.strip()
