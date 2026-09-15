from future_system.system import CompleteFutureSystem
def test_complete_future_pipeline():
    system = CompleteFutureSystem()
    result = system.analyze(
        question="What is the likely future trend?",
        historical_values=[
            100,
            105,
            110,
            115,
            120,
            125,
        ],
        evidence=[
            {
                "content":
                    "Historical evidence",
                "source":
                    "test",
                "source_type":
                    "academic",
                "reliability":
                    0.90,
                "relevance":
                    0.90,
                "freshness":
                    0.90,
            }
        ],
        live_data=[
            {
                "topic":
                    "example",
                "value":
                    120,
                "source":
                    "test",
            }
        ],
        horizon_days=30,
    )
    assert (
        result["system"]["name"]
        == "ISMAIL Future Intelligence System"
    )
    assert (
        result["horizon_days"]
        == 30
    )
    assert "analytics" in result
    assert "forecast" in result
    assert "ai_analysis" in result
    assert (
        result["forecast"]["confidence"]
        >= 0
    )
    assert (
        result["forecast"]["confidence"]
        <= 1
    )
def test_pipeline_without_history():
    system = CompleteFutureSystem()
    result = system.analyze(
        question="What happens next?",
        historical_values=[],
        horizon_days=30,
    )
    assert (
        result["forecast"]["status"]
        == "insufficient_historical_data"
    )
    assert (
        result["confidence"]
        == 0.0
    )
def test_pipeline_validation():
    system = CompleteFutureSystem()
    try:
        system.analyze(
            question="",
            historical_values=[1, 2, 3],
        )
        assert False
    except ValueError:
        assert True
