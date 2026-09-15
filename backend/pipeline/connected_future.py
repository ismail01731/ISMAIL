from __future__ import annotations
from typing import Any, Dict, Optional
from database.repositories.historical import HistoricalRepository
from future_system.topic_resolver import HistoricalTopicResolver
from intelligence.orchestrator import FutureIntelligence
from live_data.manager import LiveDataManager
class ConnectedFuturePipeline:
    """
    Connects:
        Future Question
            -> Topic Resolver
            -> Historical Database
            -> Forecast Engine
            -> Existing AI
    Existing AI is not replaced.
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
        """
        Get distinct topics from historical database.
        """
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
        topics = self.available_topics()
        return HistoricalTopicResolver.resolve(
            question,
            topics,
        )
    def load_values(
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
    def analyze(
        self,
        question: str,
        horizon_days: int = 30,
        historical_limit: int = 200,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> dict[str, Any]:
        metadata = metadata or {}
        resolution = self.resolve_topic(
            question
        )
        topic = resolution["topic"]
        # If resolver could not find a DB topic,
        # do not pretend that historical data exists.
        if resolution["method"] == "question_fallback":
            return {
                "status": "insufficient_historical_match",
                "question": question,
                "topic": topic,
                "topic_resolution": resolution,
                "historical_count": 0,
                "reason": (
                    "No matching historical topic "
                    "was found in the database."
                ),
                "existing_ai_preserved": True,
                "new_ai_created": False,
            }
        values = self.load_values(
            topic,
            historical_limit,
        )
        if len(values) < 3:
            return {
                "status": "insufficient_historical_data",
                "question": question,
                "topic": topic,
                "topic_resolution": resolution,
                "historical_count": len(values),
                "reason": (
                    "The matched topic does not have "
                    "enough historical observations "
                    "for a meaningful forecast."
                ),
                "existing_ai_preserved": True,
                "new_ai_created": False,
            }
        combined_metadata = {
            **metadata,
            "connected_future_pipeline": True,
            "resolved_topic": topic,
            "topic_resolution": resolution,
            "historical_count": len(values),
        }
        result = self.intelligence.analyze(
            question=question,
            values=values,
            evidence=[],
            live_data=[],
            horizon_days=horizon_days,
            metadata=combined_metadata,
        )
        if isinstance(result, dict):
            result["topic"] = topic
            result["topic_resolution"] = resolution
            result["historical_count"] = len(values)
            result["existing_ai_preserved"] = True
            result["new_ai_created"] = False
        return result
