from abc import ABC, abstractmethod
class BaseLLMProvider(ABC):
    """Common interface for all ISMAIL AI LLM providers."""
    @abstractmethod
    def status(self) -> dict:
        """Return provider status information."""
        raise NotImplementedError
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        raise NotImplementedError
