from intelligence.orchestrator import FutureIntelligence
def test_future_intelligence_without_ai():
    system = FutureIntelligence()
    result = system.analyze(
        question="What is the likely future trend?",
        values=[
            100,
            105,
            110,
            115,
            120,
        ],
        horizon_days=7,
    )
    assert result["question"] == "What is the likely future trend?"
    assert "forecast" in result
    assert result["forecast"]["historical_count"] == 5
    assert result["integration"]["existing_ai_connected"] is False
def test_future_intelligence_with_evidence():
    system = FutureIntelligence()
    evidence = [
        {
            "content": "Historical trend is positive.",
            "source": "test",
            "source_type": "academic",
            "reliability": 0.9,
            "relevance": 0.9,
            "freshness": 0.9,
        }
    ]
    result = system.analyze(
        question="Will the value increase?",
        values=[
            100,
            105,
            110,
            115,
            120,
        ],
        evidence=evidence,
        horizon_days=10,
    )
    assert result["forecast"]["confidence"] >= 0
    assert result["forecast"]["confidence"] <= 1
def test_no_history():
    system = FutureIntelligence()
    result = system.analyze(
        question="Predict something",
        values=[],
        horizon_days=30,
    )
    assert (
        result["forecast"]["status"]
        == "insufficient_historical_data"
    )
