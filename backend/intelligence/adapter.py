from __future__ import annotations
from typing import Any, Callable, Dict, Optional
import inspect
class ExistingAIAdapter:
    """
    Adapter for the user's existing AI.
    IMPORTANT:
    This class does NOT create or replace an AI model.
    The existing AI can be connected using:
        adapter.connect(function)
    or:
        adapter = ExistingAIAdapter(
            generate_function=my_existing_ai
        )
    Supported callable styles include:
        my_ai(prompt)
        my_ai(prompt, context)
        my_ai(prompt=..., context=...)
    If no AI is connected, the adapter safely returns
    status="not_connected".
    """
    def __init__(
        self,
        generate_function: Optional[
            Callable[..., Any]
        ] = None,
        name: str = "existing_ai",
    ):
        self.name = name
        self._generate_function = (
            generate_function
        )
    @property
    def connected(self) -> bool:
        return callable(
            self._generate_function
        )
    def connect(
        self,
        generate_function: Callable[..., Any],
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not callable(
            generate_function
        ):
            raise TypeError(
                "generate_function must be callable."
            )
        self._generate_function = (
            generate_function
        )
        if name:
            self.name = name
        return self.status()
    def disconnect(self) -> Dict[str, Any]:
        self._generate_function = None
        return self.status()
    def status(self) -> Dict[str, Any]:
        return {
            "connected":
                self.connected,
            "name":
                self.name,
            "type":
                "existing_ai_adapter",
            "owns_model":
                False,
            "creates_new_ai":
                False,
        }
    @staticmethod
    def _call_flexible(
        function: Callable[..., Any],
        prompt: str,
        context: Dict[str, Any],
    ) -> Any:
        """
        Try common existing-AI function signatures
        without forcing the user to rewrite their AI.
        """
        try:
            signature = inspect.signature(
                function
            )
        except (
            TypeError,
            ValueError,
        ):
            return function(prompt)
        parameters = signature.parameters
        has_kwargs = any(
            p.kind
            == inspect.Parameter.VAR_KEYWORD
            for p in parameters.values()
        )
        if has_kwargs:
            return function(
                prompt=prompt,
                context=context,
            )
        names = list(
            parameters.keys()
        )
        # Keyword style:
        if (
            "prompt" in parameters
            and "context" in parameters
        ):
            return function(
                prompt=prompt,
                context=context,
            )
        if "prompt" in parameters:
            return function(
                prompt=prompt
            )
        # Generic two-argument function.
        positional = [
            p
            for p in parameters.values()
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        required = [
            p
            for p in positional
            if p.default
            is inspect.Parameter.empty
        ]
        if len(required) >= 2:
            return function(
                prompt,
                context,
            )
        if len(required) == 1:
            return function(
                prompt
            )
        return function()
    def generate(
        self,
        prompt: str,
        context: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        context = context or {}
        if not self.connected:
            return {
                "status":
                    "not_connected",
                "message":
                    "Existing AI is not connected.",
                "adapter":
                    self.name,
                "owns_model":
                    False,
            }
        try:
            result = self._call_flexible(
                self._generate_function,
                prompt,
                context,
            )
            return {
                "status":
                    "success",
                "adapter":
                    self.name,
                "response":
                    result,
                "owns_model":
                    False,
            }
        except Exception as exc:
            return {
                "status":
                    "error",
                "adapter":
                    self.name,
                "error":
                    str(exc),
                "error_type":
                    type(exc).__name__,
                "owns_model":
                    False,
            }
# Global adapter instance.
#
# Your existing AI can be connected from your
# application's startup code.
existing_ai_adapter = (
    ExistingAIAdapter()
)
