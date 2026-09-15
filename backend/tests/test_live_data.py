from live_data.manager import LiveDataManager
def test_manager():
    manager = LiveDataManager()
    assert "manual" in (
        manager.available_providers()
    )
def test_manual_data():
    manager = LiveDataManager()
    result = manager.fetch(
        "manual",
        "test_topic",
        value=123,
    )
    assert len(result) == 1
    assert result[0].value == 123
    assert result[0].topic == "test_topic"
