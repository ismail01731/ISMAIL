import os
from dataclasses import dataclass
@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    openai_api_key: str
    groq_api_key: str
    openrouter_api_key: str
    base_url: str | None
    ollama_url: str
def load_llm_config() -> LLMConfig:
    provider = os.getenv("AI_PROVIDER", "").strip().lower()
    model = os.getenv("AI_MODEL", "").strip()
    if provider == "openai" and not model:
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini").strip()
    elif provider == "groq" and not model:
        model = "openai/gpt-oss-20b"
    elif provider == "openrouter" and not model:
        model = os.getenv(
            "OPENAI_MODEL",
            "openai/gpt-5-mini",
        ).strip()
    return LLMConfig(
        provider=provider,
        model=model,
        openai_api_key=os.getenv(
            "OPENAI_API_KEY",
            "",
        ).strip(),
        groq_api_key=os.getenv(
            "GROQ_API_KEY",
            "",
        ).strip(),
        openrouter_api_key=os.getenv(
            "OPENROUTER_API_KEY",
            "",
        ).strip(),
        base_url=os.getenv(
            "AI_BASE_URL",
            "",
        ).strip() or None,
        ollama_url=os.getenv(
            "OLLAMA_URL",
            "http://127.0.0.1:11434/api/generate",
        ).strip(),
    )
