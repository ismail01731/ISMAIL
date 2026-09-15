from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from database.repositories.historical import HistoricalRepository
from intelligence.orchestrator import FutureIntelligence
from live_data.manager import LiveDataManager
class AutomaticFuturePipeline:
    """
    Automatic Future Intelligence pipeline.
    Historical data is loaded through the existing
    HistoricalRepository. No new database system is created.
    """
    def __init__(
        self,
        intelligence: Optional[FutureIntelligence] = None,
        live_manager: Optional[LiveDataManager] = None,
        historical_repository: Optional[HistoricalRepository] = None,
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
    # --------------------------------------------------------
    # Historical DB
    # --------------------------------------------------------
    def load_historical(
        self,
        topic: str,
        limit: int = 200,
    ) -> List[float]:
        topic = str(topic).strip()
        if not topic:
            return []
        limit = max(
            1,
            min(int(limit), 5000)
        )
        records = self.historical_repository.list_by_topic(
            topic,
            limit=limit,
        )
        # Repository returns newest first.
        # Forecasting needs chronological order.
        records = list(reversed(records))
        values = []
        for record in records:
            try:
                value = float(record.get("value"))
                if value == value:
                    values.append(value)
            except (
                TypeError,
                ValueError,
            ):
                continue
        return values
    # --------------------------------------------------------
    # Historical evidence
    # --------------------------------------------------------
    def load_historical_evidence(
        self,
        topic: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        topic = str(topic).strip()
        if not topic:
            return []
        limit = max(
            1,
            min(int(limit), 1000)
        )
        records = self.historical_repository.list_by_topic(
            topic,
            limit=limit,
        )
        evidence = []
        for record in records:
            evidence.append(
                {
                    "content": (
                        f"{topic}: "
                        f"{record.get('value')}"
                    ),
                    "source": record.get(
                        "source",
                        ""
                    ),
                    "source_type": record.get(
                        "source_type",
                        "unknown"
                    ),
                    "timestamp": record.get(
                        "timestamp",
                        ""
                    ),
                    "reliability": record.get(
                        "reliability",
                        0.50
                    ),
                    "metadata": record.get(
                        "metadata",
                        {}
                    ),
                }
            )
        return evidence
    # --------------------------------------------------------
    # Live data
    # --------------------------------------------------------
    def fetch_live(
        self,
        topic: str,
        provider: str = "manual",
        value: Any = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        provider = str(
            provider
        ).strip().lower()
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
            if isinstance(result, list):
                items = result
            else:
                items = [result]
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
                            "timestamp": datetime.now(
                                timezone.utc
                            ).isoformat(),
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
    # --------------------------------------------------------
    # Automatic analysis
    # --------------------------------------------------------
    def analyze(
        self,
        question: str,
        topic: str,
        horizon_days: int = 30,
        live_provider: Optional[str] = None,
        live_value: Any = None,
        historical_limit: int = 200,
        metadata: Optional[Dict[str, Any]] = None,
        **live_kwargs,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        historical_values = self.load_historical(
            topic,
            historical_limit,
        )
        historical_evidence = (
            self.load_historical_evidence(
                topic,
                min(historical_limit, 100),
            )
        )
        live_data = []
        if live_provider:
            live_data = self.fetch_live(
                topic,
                provider=live_provider,
                value=live_value,
                **live_kwargs,
            )
        # Add numeric live observation to the
        # chronological forecasting input.
        forecast_values = list(
            historical_values
        )
        for item in live_data:
            if not isinstance(item, dict):
                continue
            if item.get("status") == "error":
                continue
            value = item.get("value")
            try:
                numeric_value = float(value)
                if numeric_value == numeric_value:
                    forecast_values.append(
                        numeric_value
                    )
            except (
                TypeError,
                ValueError,
            ):
                continue
        metadata = {
            **metadata,
            "automatic_pipeline": True,
            "topic": topic,
            "historical_count": len(
                historical_values
            ),
            "live_count": len(
                live_data
            ),
            "forecast_input_count": len(
                forecast_values
            ),
        }
        result = self.intelligence.analyze(
            question=question,
            values=forecast_values,
            evidence=historical_evidence,
            live_data=live_data,
            horizon_days=horizon_days,
            metadata=metadata,
        )
        result["pipeline"] = {
            "automatic": True,
            "topic": topic,
            "historical_count": len(
                historical_values
            ),
            "live_count": len(
                live_data
            ),
            "forecast_input_count": len(
                forecast_values
            ),
            "historical_source": (
                "HistoricalRepository"
            ),
            "live_provider": live_provider,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }
        return result
