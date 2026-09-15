from analytics.engine import HistoricalAnalytics
def test_trend():
    engine = HistoricalAnalytics()
    result = engine.analyze(
        [10, 12, 14, 16, 18]
    )
    assert result["success"] is True
    assert (
        result["trend"]["direction"]
        == "upward"
    )
def test_downtrend():
    engine = HistoricalAnalytics()
    result = engine.analyze(
        [100, 90, 80, 70, 60]
    )
    assert (
        result["trend"]["direction"]
        == "downward"
    )
def test_stable():
    engine = HistoricalAnalytics()
    result = engine.analyze(
        [100, 100, 100, 100, 100]
    )
    assert (
        result["trend"]["direction"]
        == "stable"
    )
def test_anomaly():
    engine = HistoricalAnalytics()
    result = engine.analyze(
        [
            10,
            11,
            10,
            12,
            11,
            10,
            100,
        ]
    )
    assert len(
        result["anomalies"]
    ) >= 1
