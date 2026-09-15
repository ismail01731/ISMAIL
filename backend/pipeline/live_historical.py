from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from database.repositories.historical import HistoricalRepository
from future_system.topic_resolver import HistoricalTopicResolver
from intelligence.orchestrator import FutureIntelligence
from live_data.manager import LiveDataManager
class LiveHistoricalFuturePipeline:
    """
    Combines historical database data with live data
    before sending the prediction context to the
    existing ISMAIL AI.
    """
    def __init__(
        self,
        intelligence: Optional[FutureIntelligence] = None,
        live_manager: Optional[LiveDataManager] = None,
        historical_repository: Optional[
            HistoricalRepository
        ] = None,
    ):
        self.intelligence = (
            intelligence
            if intelligence is not None
            else FutureIntelligence()
        )
        self.live_manager = (
            live_manager
            if live_manager is not None
            else LiveDataManager()
        )
        self.historical_repository = (
            historical_repository
            if historical_repository is not None
            else HistoricalRepository()
        )
    def available_topics(self) -> list[str]:
        with self.historical_repository.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT DISTINCT topic
                FROM historical_data
                WHERE topic IS NOT NULL
                  AND TRIM(topic) != ''
                ORDER BY topic
                """
            ).fetchall()
        return [
            str(row[0]).strip()
            for row in rows
            if row[0]
        ]
    def resolve_topic(
        self,
        question: str,
    ) -> dict[str, Any]:
        return HistoricalTopicResolver.resolve(
            question,
            self.available_topics(),
        )
    def load_historical(
        self,
        topic: str,
        limit: int = 200,
    ) -> list[float]:
        records = (
            self.historical_repository
            .list_by_topic(
                topic,
                limit=max(
                    1,
                    min(int(limit), 5000),
                ),
            )
        )
        records = list(reversed(records))
        values = []
        for record in records:
            try:
                value = float(record["value"])
                if value == value:
                    values.append(value)
            except (
                TypeError,
                ValueError,
                KeyError,
            ):
                continue
        return values
    def fetch_live(
        self,
        topic: str,
        provider: str,
        value: Any = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        try:
            if provider == "manual":
                if value is None:
                    return []
                result = self.live_manager.fetch(
                    provider,
                    topic,
                    value=value,
                    **kwargs,
                )
            else:
                result = self.live_manager.fetch(
                    provider,
                    topic,
                    **kwargs,
                )
            if result is None:
                return []
            items = (
                result
                if isinstance(result, list)
                else [result]
            )
            output = []
            for item in items:
                if hasattr(item, "to_dict"):
                    output.append(
                        item.to_dict()
                    )
                elif isinstance(item, dict):
                    output.append(item)
                else:
                    output.append(
                        {
                            "topic": topic,
                            "value": item,
                            "source": provider,
                            "source_type": "live",
                            "timestamp": (
                                datetime.now(
                                    timezone.utc
                                ).isoformat()
                            ),
                        }
                    )
            return output
        except Exception as exc:
            return [
                {
                    "status": "error",
                    "provider": provider,
                    "topic": topic,
                    "error": str(exc),
                }
            ]
    def analyze(
        self,
        question: str,
        horizon_days: int = 30,
        live_provider: Optional[str] = None,
        live_value: Any = None,
        historical_limit: int = 200,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
        **live_kwargs,
    ) -> dict[str, Any]:
        metadata = metadata or {}
        resolution = self.resolve_topic(
            question
        )
        topic = resolution["topic"]
        if (
            resolution["method"]
            == "question_fallback"
        ):
            return {
                "status": "insufficient_historical_match",
                "question": question,
                "topic": topic,
                "topic_resolution": resolution,
                "historical_count": 0,
                "live_count": 0,
                "reason": (
                    "No matching historical topic "
                    "was found."
                ),
                "existing_ai_preserved": True,
                "new_ai_created": False,
            }
        historical_values = self.load_historical(
            topic,
            historical_limit,
        )
        live_data = []
        if live_provider:
            live_data = self.fetch_live(
                topic=topic,
                provider=live_provider,
                value=live_value,
                **live_kwargs,
            )
        forecast_values = list(
            historical_values
        )
        for item in live_data:
            if not isinstance(item, dict):
                continue
            if item.get("status") == "error":
                continue
            try:
                value = float(
                    item.get("value")
                )
                if value == value:
                    forecast_values.append(
                        value
                    )
            except (
                TypeError,
                ValueError,
            ):
                continue
        if len(forecast_values) < 3:
            return {
                "status": "insufficient_data",
                "question": question,
                "topic": topic,
                "topic_resolution": resolution,
                "historical_count": len(
                    historical_values
                ),
                "live_count": len(live_data),
                "forecast_input_count": len(
                    forecast_values
                ),
                "reason": (
                    "Not enough numeric data "
                    "for forecasting."
                ),
                "existing_ai_preserved": True,
                "new_ai_created": False,
            }
        combined_metadata = {
            **metadata,
            "live_historical_pipeline": True,
            "resolved_topic": topic,
            "topic_resolution": resolution,
            "historical_count": len(
                historical_values
            ),
            "live_count": len(live_data),
            "forecast_input_count": len(
                forecast_values
            ),
        }
        result = self.intelligence.analyze(
            question=question,
            values=forecast_values,
            evidence=[],
            live_data=live_data,
            horizon_days=horizon_days,
            metadata=combined_metadata,
        )
        if isinstance(result, dict):
            result["topic"] = topic
            result["topic_resolution"] = resolution
            result["historical_count"] = len(
                historical_values
            )
            result["live_count"] = len(
                live_data
            )
            result["forecast_input_count"] = len(
                forecast_values
            )
            result["existing_ai_preserved"] = True
            result["new_ai_created"] = False
        return result
