from backend.llm.base import BaseLLMProvider
from backend.llm.config import LLMConfig
from backend.llm.exceptions import LLMConfigurationError
class LLMRouter:
    """Select and expose the active LLM provider."""
    def __init__(self, config: LLMConfig):
        self.config = config
        self.provider = None
    def set_provider(self, provider: BaseLLMProvider) -> None:
        if not isinstance(provider, BaseLLMProvider):
            raise TypeError("provider must implement BaseLLMProvider.")
        self.provider = provider
    def status(self) -> dict:
        if self.provider is None:
            return {
                "provider": self.config.provider or None,
                "model": self.config.model or None,
                "configured": False,
            }
        return self.provider.status()
    def generate(self, prompt: str) -> str:
        if self.provider is None:
            raise LLMConfigurationError(
                "No LLM provider has been configured."
            )
        return self.provider.generate(prompt)

    def generate_stream(self, prompt: str):
        """Generate a response as a stream when the active provider supports it."""
        if self.provider is None:
            raise LLMConfigurationError(
                "No LLM provider has been configured."
            )

        stream_method = getattr(
            self.provider,
            "generate_stream",
            None,
        )

        if callable(stream_method):
            yield from stream_method(prompt)
            return

        yield self.provider.generate(prompt)

    
    @classmethod
    def create(cls, config: LLMConfig):
        router = cls(config)
        if config.provider == "ollama":
            from backend.llm.ollama_provider import OllamaProvider
            router.set_provider(OllamaProvider(config))
        elif config.provider in (
            "openai",
            "groq",
            "openrouter",
        ):
            from backend.openai_provider import OpenAIProvider
            router.set_provider(OpenAIProvider(config))
        else:
            raise LLMConfigurationError(
                f"Unsupported LLM provider: "
                f"{config.provider or 'none'}"
            )
        return router
