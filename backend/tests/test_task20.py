import sys
from pathlib import Path
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
from intelligence.adapter import ExistingAIAdapter
from intelligence.orchestrator import FutureIntelligence
from pipeline.automatic import AutomaticFuturePipeline
TEST_TOPIC = "task20_test_topic"
class FakeLiveManager:
    def fetch(self, provider, topic, **kwargs):
        if provider == "manual":
            value = kwargs.get("value")
            return {
                "topic": topic,
                "value": value,
                "source": "manual_test",
                "source_type": "manual",
                "reliability": 1.0,
                "timestamp": "2026-09-15T00:00:00+00:00",
                "metadata": {},
            }
        raise ValueError(f"Unsupported test provider: {provider}")
class FakeHistoricalRepository:
    """
    Mimics HistoricalRepository.list_by_topic().
    Real repository returns newest records first.
    """
    def __init__(self, records):
        self.records = records
    def list_by_topic(self, topic, limit=100):
        filtered = [
            record
            for record in self.records
            if record["topic"] == topic
        ]
        # Same behavior as the real repository:
        # newest timestamp first.
        filtered.sort(
            key=lambda item: item.get("timestamp", ""),
            reverse=True,
        )
        return filtered[:limit]
def build_test_history():
    values = [
        100,
        105,
        108,
        115,
        120,
        125,
        132,
        138,
        142,
        145,
        150,
        154,
    ]
    records = []
    for index, value in enumerate(values):
        day = index + 1
        records.append(
            {
                "id": day,
                "topic": TEST_TOPIC,
                "value": str(value),
                "source": "task20_test",
                "source_type": "test",
                "timestamp": (
                    f"2026-09-{day:02d}"
                    "T00:00:00+00:00"
                ),
                "reliability": 1.0,
                "metadata": {},
                "created_at": (
                    f"2026-09-{day:02d}"
                    "T00:00:00+00:00"
                ),
            }
        )
    return records
def test_historical_loader():
    repository = FakeHistoricalRepository(
        build_test_history()
    )
    pipeline = AutomaticFuturePipeline(
        historical_repository=repository
    )
    values = pipeline.load_historical(
        TEST_TOPIC,
        limit=100,
    )
    assert len(values) == 12
    # Pipeline should convert newest-first DB records
    # into chronological oldest-first values.
    assert values == [
        100.0,
        105.0,
        108.0,
        115.0,
        120.0,
        125.0,
        132.0,
        138.0,
        142.0,
        145.0,
        150.0,
        154.0,
    ]
    print("PASS: historical loader")
def test_manual_live_pipeline():
    repository = FakeHistoricalRepository(
        build_test_history()
    )
    def fake_ai(prompt):
        return (
            "Existing AI received historical data, "
            "live data, forecast and uncertainty context."
        )
    ai_adapter = ExistingAIAdapter(
        fake_ai,
        "test_ai",
    )
    intelligence = FutureIntelligence(
        ai_adapter
    )
    pipeline = AutomaticFuturePipeline(
        intelligence=intelligence,
        live_manager=FakeLiveManager(),
        historical_repository=repository,
    )
    result = pipeline.analyze(
        question="আগামী 30 দিনে এই trend কোন দিকে যেতে পারে?",
        topic=TEST_TOPIC,
        horizon_days=30,
        live_provider="manual",
        live_value=160,
    )
    assert result["pipeline"]["automatic"] is True
    assert result["pipeline"]["topic"] == TEST_TOPIC
    assert result["pipeline"]["historical_count"] == 12
    assert result["pipeline"]["live_count"] == 1
    assert result["pipeline"]["forecast_input_count"] == 13
    assert (
        result["pipeline"]["historical_source"]
        == "HistoricalRepository"
    )
    assert (
        result["pipeline"]["live_provider"]
        == "manual"
    )
    assert result["ai_analysis"]["status"] == "success"
    assert result["integration"]["ai_connected"] is True
    assert result["integration"]["adapter"] == "test_ai"
    assert (
        result["integration"]["existing_ai_preserved"]
        is True
    )
    assert (
        result["integration"]["new_ai_created"]
        is False
    )
    assert "forecast" in result
    assert "natural_answer" in result
    assert (
        result["natural_answer"]["guarantee"]
        is False
    )
    print(
        "PASS: automatic historical + live + AI pipeline"
    )
if __name__ == "__main__":
    test_historical_loader()
    test_manual_live_pipeline()
    print("")
    print("TASK 20 TEST: PASS")
