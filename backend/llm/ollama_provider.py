import json
import urllib.error
import urllib.request
from backend.llm.base import BaseLLMProvider
from backend.llm.config import LLMConfig
from backend.llm.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMResponseError,
)
class OllamaProvider(BaseLLMProvider):
    """Local Ollama LLM provider for ISMAIL AI."""
    def __init__(self, config: LLMConfig):
        self.config = config
        self.model = config.model
        self.url = config.ollama_url
    def status(self) -> dict:
        if not self.model:
            return {
                "provider": "ollama",
                "model": None,
                "configured": False,
                "connected": False,
            }
        connected = False
        try:
            tags_url = self.url.rsplit("/api/", 1)[0] + "/api/tags"
            request = urllib.request.Request(
                tags_url,
                method="GET",
            )
            with urllib.request.urlopen(
                request,
                timeout=3,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )
            models = data.get("models", [])
            connected = any(
                isinstance(item, dict)
                and item.get("name") == self.model
                for item in models
            )
        except Exception:
            connected = False
        return {
            "provider": "ollama",
            "model": self.model,
            "configured": bool(self.model),
            "connected": connected,
        }
    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        if not self.model:
            raise LLMConfigurationError(
                "Ollama model is not configured."
            )
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "num_predict": 400,
                "temperature": 0.05,
                "top_p": 0.8,
                "repeat_penalty": 1.15,
            },
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=300,
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )
        except urllib.error.URLError as exc:
            raise LLMProviderError(
                "Unable to connect to Ollama. "
                "Make sure Ollama is running."
            ) from exc
        except json.JSONDecodeError as exc:
            raise LLMResponseError(
                "Ollama returned an invalid response."
            ) from exc
        response_text = str(
            result.get("response", "")
        ).strip()
        if not response_text:
            raise LLMResponseError(
                "Ollama returned an empty response."
            )
        return response_text
