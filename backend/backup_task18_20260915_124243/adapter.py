from __future__ import annotations
from typing import Any, Callable, Dict, Optional
class ExistingAIAdapter:
    """
    Adapter for the user's existing AI.
    The existing AI is NOT replaced.
    A callable can be supplied from the current AI application.
    Example:
        adapter = ExistingAIAdapter(
            generate=my_existing_ai_function
        )
    """
    def __init__(
        self,
        generate: Optional[Callable[..., Any]] = None,
    ):
        self.generate_function = generate
    @property
    def connected(self) -> bool:
        return self.generate_function is not None
    def generate(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        if self.generate_function is None:
            return {
                "status": "not_connected",
                "message": (
                    "Existing AI adapter is not connected. "
                    "The forecasting system can still return "
                    "structured quantitative results."
                ),
                "prompt": prompt,
                "context": context or {},
            }
        return self.generate_function(
            prompt=prompt,
            context=context or {},
        )
