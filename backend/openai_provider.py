from openai import OpenAI
from backend.llm.base import BaseLLMProvider
from backend.llm.config import LLMConfig
from backend.llm.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMResponseError,
)
class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible provider for OpenAI, Groq and OpenRouter."""
    def __init__(self, config: LLMConfig):
        self.config = config
        self.provider = config.provider
        self.api_key = self._get_api_key()
        self.model = config.model
        self.base_url = self._get_base_url()
        self.client = None
        if self.api_key and self.model:
            kwargs = {
                "api_key": self.api_key,
                "timeout": 60.0,
                "max_retries": 2,
            }
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self.client = OpenAI(**kwargs)
    def _get_api_key(self) -> str:
        if self.provider == "openai":
            return self.config.openai_api_key
        if self.provider == "groq":
            return self.config.groq_api_key
        if self.provider == "openrouter":
            return self.config.openrouter_api_key
        return ""
    def _get_base_url(self) -> str | None:
        if self.config.base_url:
            return self.config.base_url
        if self.provider == "groq":
            return "https://api.groq.com/openai/v1"
        if self.provider == "openrouter":
            return "https://openrouter.ai/api/v1"
        return None
    def status(self) -> dict:
        return {
            "provider": self.provider or None,
            "model": self.model or None,
            "configured": bool(self.client and self.model),
        }
    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        if not self.api_key:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} API key is not configured."
            )
        if not self.model:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} model is not configured."
            )
        if self.client is None:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} provider client is not configured."
            )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        except Exception as exc:
            raise LLMProviderError(
                f"{self.provider or 'AI'} provider request failed."
            ) from exc
        if not response.choices:
            raise LLMResponseError(
                f"{self.provider or 'AI'} provider returned no choices."
            )
        content = response.choices[0].message.content
        if not isinstance(content, str) or not content.strip():
            raise LLMResponseError(
                f"{self.provider or 'AI'} provider returned an empty response."
            )
        return content.strip()


    def generate_stream(self, prompt: str):
        """Generate an AI response as a stream of text chunks."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        if not self.api_key:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} API key is not configured."
            )
        if not self.model:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} model is not configured."
            )
        if self.client is None:
            raise LLMConfigurationError(
                f"{self.provider or 'AI'} provider client is not configured."
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                stream=True,
            )

            for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)

                if isinstance(content, str) and content:
                    yield content

        except Exception as exc:
            raise LLMProviderError(
                f"{self.provider or 'AI'} streaming request failed."
            ) from exc
