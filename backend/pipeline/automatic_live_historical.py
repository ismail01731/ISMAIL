from __future__ import annotations
from typing import Any, Dict, Optional
from pipeline.live_historical import (
    LiveHistoricalFuturePipeline,
)
from pipeline.live_provider_selector import (
    LiveProviderSelector,
)
class AutomaticLiveHistoricalPipeline:
    """
    TASK 27
    Connects:
        Topic Resolver
        +
        Automatic Live Provider Selector
        +
        Historical Database
        +
        Future Intelligence
        +
        Existing ISMAIL AI
    """
    def __init__(
        self,
        pipeline: LiveHistoricalFuturePipeline,
        provider_selector: Optional[
            LiveProviderSelector
        ] = None,
    ):
        self.pipeline = pipeline
        self.provider_selector = (
            provider_selector
            if provider_selector is not None
            else LiveProviderSelector()
        )
    def select_provider(
        self,
        topic: str,
        preferred_provider: str | None = None,
    ) -> dict[str, Any]:
        return self.provider_selector.select(
            topic=topic,
            preferred=preferred_provider,
        )
    def analyze(
        self,
        question: str,
        horizon_days: int = 30,
        preferred_provider: str | None = None,
        live_value: Any = None,
        historical_limit: int = 200,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
        **live_kwargs,
    ) -> dict[str, Any]:
        metadata = metadata or {}
        resolution = self.pipeline.resolve_topic(
            question
        )
        topic = resolution.get(
            "topic",
            question.strip(),
        )
        provider_selection = (
            self.select_provider(
                topic,
                preferred_provider,
            )
        )
        provider = provider_selection.get(
            "provider"
        )
        # If no live provider is configured,
        # safely continue with historical data only.
        if not provider:
            result = self.pipeline.analyze(
                question=question,
                horizon_days=horizon_days,
                live_provider=None,
                historical_limit=historical_limit,
                metadata={
                    **metadata,
                    "automatic_live_selection": True,
                    "provider_selection": (
                        provider_selection
                    ),
                },
            )
        else:
            result = self.pipeline.analyze(
                question=question,
                horizon_days=horizon_days,
                live_provider=provider,
                live_value=live_value,
                historical_limit=historical_limit,
                metadata={
                    **metadata,
                    "automatic_live_selection": True,
                    "provider_selection": (
                        provider_selection
                    ),
                },
                **live_kwargs,
            )
        if not isinstance(result, dict):
            result = {
                "status": "error",
                "reason": (
                    "Pipeline returned "
                    "non-dict result."
                ),
            }
        result["automatic_live_selection"] = True
        result["provider_selection"] = (
            provider_selection
        )
        result["selected_live_provider"] = (
            provider
        )
        result.setdefault(
            "existing_ai_preserved",
            True,
        )
        result.setdefault(
            "new_ai_created",
            False,
        )
        return result
