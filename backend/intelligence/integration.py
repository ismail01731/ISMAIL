from __future__ import annotations
from typing import Any, Callable, Dict, Optional
from intelligence.adapter import (
    existing_ai_adapter,
)
def connect_existing_ai(
    generate_function: Callable[..., Any],
    name: str = "existing_ai",
) -> Dict[str, Any]:
    """
    Connect the user's existing AI.
    Example:
        from intelligence.integration import connect_existing_ai
        connect_existing_ai(
            my_existing_ai_function,
            "my_ai"
        )
    """
    return existing_ai_adapter.connect(
        generate_function,
        name=name,
    )
def disconnect_existing_ai() -> Dict[str, Any]:
    return existing_ai_adapter.disconnect()
def existing_ai_status() -> Dict[str, Any]:
    return existing_ai_adapter.status()
