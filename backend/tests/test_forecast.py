from forecast.engine import ForecastEngine
def test_forecast_engine():
    engine = ForecastEngine()
    result = engine.predict(
        values=[
            100,
            105,
            110,
            115,
            120,
            125,
            130,
        ],
        horizon_days=10,
    )
    assert result["historical_count"] == 7
    assert len(result["baseline_forecast"]) == 10
    assert "upside" in result["scenarios"]
    assert "base" in result["scenarios"]
    assert "downside" in result["scenarios"]
    total_probability = sum(
        item["probability"]
        for item in result["scenarios"].values()
    )
    assert abs(total_probability - 1.0) < 0.0001
    assert 0.0 <= result["confidence"] <= 1.0
def test_downward_trend():
    engine = ForecastEngine()
    result = engine.predict(
        values=[
            200,
            190,
            180,
            170,
            160,
            150,
        ],
        horizon_days=5,
    )
    assert result["trend"]["direction"] == "downward"
def test_stable_series():
    engine = ForecastEngine()
    result = engine.predict(
        values=[
            100,
            100,
            100,
            100,
            100,
        ],
        horizon_days=5,
    )
    assert result["trend"]["direction"] == "stable"
