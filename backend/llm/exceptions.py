class LLMError(Exception):
    """Base exception for ISMAIL AI LLM errors."""
class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""
class LLMProviderError(LLMError):
    """Raised when an LLM provider fails."""
class LLMResponseError(LLMError):
    """Raised when an LLM provider returns an invalid response."""
