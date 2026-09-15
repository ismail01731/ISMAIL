from feedback.engine import FeedbackEngine
from feedback.storage import FeedbackStorage
from feedback.metrics import AccuracyMetrics
def test_accuracy_metrics():
    predicted = [100, 110, 120]
    actual = [100, 105, 125]
    result = AccuracyMetrics.summary(
        predicted,
        actual,
    )
    assert result["count"] == 3
    assert result["mae"] >= 0
    assert result["rmse"] >= 0
    assert 0 <= result["directional_accuracy"] <= 1
def test_feedback_record(tmp_path):
    db_path = tmp_path / "feedback.db"
    storage = FeedbackStorage(
        db_path=str(db_path)
    )
    engine = FeedbackEngine(
        storage=storage
    )
    result = engine.record(
        prediction_id=1,
        predicted_value=110,
        actual_value=120,
        confidence=0.80,
    )
    assert result["id"] > 0
    assert result["absolute_error"] == 10
    assert result["percentage_error"] > 0
def test_feedback_summary(tmp_path):
    db_path = tmp_path / "feedback.db"
    storage = FeedbackStorage(
        db_path=str(db_path)
    )
    engine = FeedbackEngine(
        storage=storage
    )
    engine.record(
        prediction_id=1,
        predicted_value=100,
        actual_value=105,
        confidence=0.70,
    )
    engine.record(
        prediction_id=2,
        predicted_value=200,
        actual_value=190,
        confidence=0.80,
    )
    summary = engine.summary()
    assert summary["count"] == 2
    assert "accuracy" in summary
    assert "calibration" in summary
